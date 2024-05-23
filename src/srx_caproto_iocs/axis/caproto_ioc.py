from __future__ import annotations

import textwrap
from io import BytesIO

import requests
from caproto import ChannelType
from caproto.server import pvproperty, run, template_arg_parser
from PIL import Image

from ..base import CaprotoSaveIOC, check_args
from ..utils import now, save_image

DEFAULT_MAX_LENGTH = 10_000_000


class AxisSaveIOC(CaprotoSaveIOC):
    """Axis caproto save IOC."""

    common_kwargs = {"max_length": 255, "string_encoding": "utf-8"}

    key1 = pvproperty(
        value="",
        string_encoding="utf-8",
        dtype=ChannelType.CHAR,
        doc="key 1 for data 1",
        max_length=255,
    )
    data1 = pvproperty(
        value=0,
        dtype=ChannelType.DOUBLE,
        doc="data 1",
        max_length=DEFAULT_MAX_LENGTH,
    )

    def __init__(self, *args, camera_host=None, **kwargs):
        self._camera_host = camera_host
        print(f"{camera_host = }")
        super().__init__(*args, **kwargs)

    async def _get_current_dataset(self, *args, **kwargs):
        url = f"http://{self._camera_host}/axis-cgi/jpg/image.cgi"
        resp = requests.get(url)
        img = Image.open(BytesIO(resp.content))

        dataset = img
        print(f"{now()}:\n{dataset.size}")

        return dataset

    @staticmethod
    def saver(request_queue, response_queue):
        """The saver callback for threading-based queueing."""
        while True:
            received = request_queue.get()
            filename = received["filename"]
            data = received["data"]
            # 'frame_number' is not used for this exporter.
            frame_number = received["frame_number"]  # noqa: F841
            try:
                save_image(fname=filename, data=data, file_format="jpeg", mode="x")
                print(f"{now()}: saved data into:\n  {filename}")

                success = True
                error_message = ""
            except Exception as exc:  # pylint: disable=broad-exception-caught
                success = False
                error_message = exc
                print(
                    f"Cannot save file {filename!r} due to the following exception:\n{exc}"
                )

            response = {"success": success, "error_message": error_message}
            response_queue.put(response)


if __name__ == "__main__":
    parser, split_args = template_arg_parser(
        default_prefix="", desc=textwrap.dedent(AxisSaveIOC.__doc__)
    )

    parser.add_argument(
        "-c",
        "--camera-host",
        help="The camera hostname, e.g., 'xf06bm-cam5'",
        required=True,
        type=str,
    )

    ioc_options, run_options = check_args(parser, split_args)

    print(f"{ioc_options = }")
    print(f"{run_options = }")

    ioc = AxisSaveIOC(camera_host=parser.parse_args().camera_host, **ioc_options)
    run(ioc.pvdb, **run_options)
