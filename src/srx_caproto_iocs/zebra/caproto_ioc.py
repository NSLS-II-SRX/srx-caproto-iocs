from __future__ import annotations

import textwrap

from caproto.asyncio.client import Context
from caproto.server import run, template_arg_parser

from ..base import CaprotoSaveIOC, check_args
from ..utils import now

# def export_nano_zebra_data(zebra, filepath, fastaxis):
#     j = 0
#     while zebra.pc.data_in_progress.get() == 1:
#         print("Waiting for zebra...")
#         ttime.sleep(0.1)
#         j += 1
#         if j > 10:
#             print("THE ZEBRA IS BEHAVING BADLY CARRYING ON")
#             break

#     time_d = zebra.pc.data.time.get()
#     enc1_d = zebra.pc.data.enc1.get()
#     enc2_d = zebra.pc.data.enc2.get()
#     enc3_d = zebra.pc.data.enc3.get()

#     px = zebra.pc.pulse_step.get()
#     if fastaxis == 'NANOHOR':
#         # Add half pixelsize to correct encoder
#         enc1_d = enc1_d + (px / 2)
#     elif fastaxis == 'NANOVER':
#         # Add half pixelsize to correct encoder
#         enc2_d = enc2_d + (px / 2)
#     elif fastaxis == 'NANOZ':
#         # Add half pixelsize to correct encoder
#         enc3_d = enc3_d + (px / 2)

#     size = (len(time_d),)
#     with h5py.File(filepath, "w") as f:
#         dset0 = f.create_dataset("zebra_time", size, dtype="f")
#         dset0[...] = np.array(time_d)
#         dset1 = f.create_dataset("enc1", size, dtype="f")
#         dset1[...] = np.array(enc1_d)
#         dset2 = f.create_dataset("enc2", size, dtype="f")
#         dset2[...] = np.array(enc2_d)
#         dset3 = f.create_dataset("enc3", size, dtype="f")
#         dset3[...] = np.array(enc3_d)


# class ZebraPositionCaptureData(Device):
#     """
#     Data arrays for the Zebra position capture function and their metadata.
#     """
#     # Data arrays
#     ...
#     enc1 = Cpt(EpicsSignal, "PC_ENC1")  # XF:05IDD-ES:1{Dev:Zebra2}:PC_ENC1
#     enc2 = Cpt(EpicsSignal, "PC_ENC2")  # XF:05IDD-ES:1{Dev:Zebra2}:PC_ENC2
#     enc3 = Cpt(EpicsSignal, "PC_ENC3")  # XF:05IDD-ES:1{Dev:Zebra2}:PC_ENC3
#     time = Cpt(EpicsSignal, "PC_TIME")  # XF:05IDD-ES:1{Dev:Zebra2}:PC_TIME
#     ...

# class ZebraPositionCapture(Device):
#     """
#     Signals for the position capture function of the Zebra
#     """

#     # Configuration settings and status PVs
#     ...
#     pulse_step = Cpt(EpicsSignalWithRBV, "PC_PULSE_STEP")  # XF:05IDD-ES:1{Dev:Zebra2}:PC_PULSE_STEP
#     ...
#     data_in_progress = Cpt(EpicsSignalRO, "ARRAY_ACQ")  # XF:05IDD-ES:1{Dev:Zebra2}:ARRAY_ACQ
#     ...
#     data = Cpt(ZebraPositionCaptureData, "")

# nanoZebra = SRXZebra(
#    "XF:05IDD-ES:1{Dev:Zebra2}:", name="nanoZebra",
#    read_attrs=["pc.data.enc1", "pc.data.enc2", "pc.data.enc3", "pc.data.time"],
# )


class ZebraSaveIOC(CaprotoSaveIOC):
    """Zebra caproto save IOC."""

    #     enc1 = Cpt(EpicsSignal, "PC_ENC1")
    #     enc2 = Cpt(EpicsSignal, "PC_ENC2")
    #     enc3 = Cpt(EpicsSignal, "PC_ENC3")
    #     enc4 = Cpt(EpicsSignal, "PC_ENC4")

    # data_in_progress = pvproperty()  # +
    # time_d = pvproperty()
    # enc1_d = pvproperty()
    # enc2_d = pvproperty()
    # enc3_d = pvproperty()
    # pulse_step = pvproperty()

    def __init__(self, *args, external_pvs=None, **kwargs):
        """Init method.

        external_pvs : dict
            a dictionary of external PVs with keys as human-readable names.
        """
        super().__init__(*args, **kwargs)
        self._external_pvs = external_pvs

    # async def _stage(self, *args, **kwargs):
    #     ret = await super()._stage(*args, **kwargs)
    #     return ret

    async def _get_current_dataset(self, frame, external_pv="enc1"):
        client_context = Context()
        (pvobject,) = await client_context.get_pvs(self._external_pvs[external_pv])
        print(f"{pvobject = }")
        # pvobject = pvobjects[0]
        ret = await pvobject.read()

        dataset = ret.data

        print(f"{now()}:\n{dataset} {dataset.shape}")

        return dataset

    @acquire.putter
    @no_reentry
    async def acquire(self, instance, value):
        """The acquire method to perform an individual acquisition of a data point."""
        if (
            value != AcqStatuses.ACQUIRING.value
            # or self.stage.value not in [True, StageStates.STAGED.value]
        ):
            return False

        if (
            instance.value in [True, AcqStatuses.ACQUIRING.value]
            and value == AcqStatuses.ACQUIRING.value
        ):
            print(
                f"The device is already acquiring. Please wait until the '{AcqStatuses.IDLE.value}' status."
            )
            return True

        await self.acquire.write(AcqStatuses.ACQUIRING.value)

        # Delegate saving the resulting data to a blocking callback in a thread.
        payload = {
            "filename": self.full_file_path.value,
            "data": await self._get_current_dataset(frame=self.frame_num.value),
            "uid": str(uuid.uuid4()),
            "timestamp": ttime.time(),
            "frame_number": self.frame_num.value,
        }

        await self._request_queue.async_put(payload)
        response = await self._response_queue.async_get()

        if response["success"]:
            # Increment the counter only on a successful saving of the file.
            await self.frame_num.write(self.frame_num.value + 1)

        # await self.acquire.write(AcqStatuses.IDLE.value)

        return False

    @staticmethod
    def saver(request_queue, response_queue):
        """The saver callback for threading-based queueing."""
        while True:
            received = request_queue.get()
            filename = received["filename"]
            data = received["data"]
            frame_number = received["frame_number"]
            try:
                save_hdf5_1d(fname=filename, data=data, mode="x", group_path="enc1")
                print(
                    f"{now()}: saved {frame_number=} {data.shape} data into:\n  {filename}"
                )

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
        default_prefix="", desc=textwrap.dedent(ZebraSaveIOC.__doc__)
    )
    ioc_options, run_options = check_args(parser, split_args)

    external_pv_prefix = ioc_options["prefix"].replace("{{", "{").replace("}}", "}")  # "XF:05IDD-ES:1{Dev:Zebra2}:"

    external_pvs = {
        "pulse_step": external_pv_prefix + "PC_PULSE_STEP",
        "data_in_progress": external_pv_prefix + "ARRAY_ACQ",
        "enc1": external_pv_prefix + "PC_ENC1",
        "enc2": external_pv_prefix + "PC_ENC2",
        "enc3": external_pv_prefix + "PC_ENC3",
        "enc4": external_pv_prefix + "PC_ENC4",
        "time": external_pv_prefix + "PC_TIME",
    }

    ioc = ZebraSaveIOC(external_pvs=external_pvs, **ioc_options)
    run(ioc.pvdb, **run_options)
