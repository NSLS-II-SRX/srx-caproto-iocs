from __future__ import annotations

import textwrap

from caproto import ChannelType
from caproto.server import PVGroup, pvproperty, run, template_arg_parser

from ..base import check_args


class CaprotoStringIOC(PVGroup):
    """Test channel types for strings."""

    common_kwargs = {"max_length": 255, "string_encoding": "utf-8"}

    bare_string = pvproperty(
        value="bare_string", doc="A test for a bare string", **common_kwargs
    )
    implicit_string_type = pvproperty(
        value="implicit_string_type",
        doc="A test for an implicit string type",
        report_as_string=True,
        **common_kwargs,
    )
    string_type = pvproperty(
        value="string_type",
        doc="A test for a string type",
        dtype=str,
        report_as_string=True,
        **common_kwargs,
    )
    string_type_enum = pvproperty(
        value="string_type_enum",
        doc="A test for a string type",
        dtype=ChannelType.STRING,
        **common_kwargs,
    )
    char_type_as_string = pvproperty(
        value="char_type_as_string",
        doc="A test for a char type reported as string",
        report_as_string=True,
        dtype=ChannelType.CHAR,
        **common_kwargs,
    )
    char_type = pvproperty(
        value="char_type",
        doc="A test for a char type not reported as string",
        dtype=ChannelType.CHAR,
        **common_kwargs,
    )


if __name__ == "__main__":
    parser, split_args = template_arg_parser(
        default_prefix="", desc=textwrap.dedent(CaprotoStringIOC.__doc__)
    )
    ioc_options, run_options = check_args(parser, split_args)
    ioc = CaprotoStringIOC(**ioc_options)

    run(ioc.pvdb, **run_options)
