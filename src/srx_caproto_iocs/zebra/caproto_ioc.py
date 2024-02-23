from __future__ import annotations

import textwrap

from caproto.server import run, template_arg_parser

from ..base import CaprotoSaveIOC, check_args


class ZebraSaveIOC(CaprotoSaveIOC):
    """Zebra caproto save IOC."""


if __name__ == "__main__":
    parser, split_args = template_arg_parser(
        default_prefix="", desc=textwrap.dedent(ZebraSaveIOC.__doc__)
    )
    ioc_options, run_options = check_args(parser, split_args)
    ioc = ZebraSaveIOC(**ioc_options)  # TODO: pass libca IOC PVs of interest
    run(ioc.pvdb, **run_options)
