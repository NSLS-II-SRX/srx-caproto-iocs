from __future__ import annotations

import textwrap

from caproto.server import run, template_arg_parser

from ..base import GenericSaveIOC


class ZebraSaveIOC(GenericSaveIOC):
    """Zebra Caproto Save IOC"""


if __name__ == "__main__":
    parser, split_args = template_arg_parser(
        default_prefix="", desc=textwrap.dedent(ZebraSaveIOC.__doc__)
    )

    parsed_args = parser.parse_args()
    prefix = parsed_args.prefix
    if not prefix:
        parser.error("The 'prefix' argument must be specified.")

    ioc_options, run_options = split_args(parsed_args)

    ioc = ZebraSaveIOC(**ioc_options)  # TODO: pass libca IOC PVs of interest
    run(ioc.pvdb, **run_options)
