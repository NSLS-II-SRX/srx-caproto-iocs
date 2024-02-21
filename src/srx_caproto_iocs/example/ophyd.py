from __future__ import annotations

from ophyd import Component as Cpt
from ophyd import Device, EpicsSignal


class OphydChannelTypes(Device):
    """An ophyd Device which works with the CaprotoIOCChannelTypes caproto IOC."""

    bare_string = Cpt(EpicsSignal, "bare_string", string=True)
    implicit_string_type = Cpt(EpicsSignal, "implicit_string_type", string=True)
    string_type = Cpt(EpicsSignal, "string_type", string=True)
    string_type_enum = Cpt(EpicsSignal, "string_type_enum", string=True)
    char_type_as_string = Cpt(EpicsSignal, "char_type_as_string", string=True)
    char_type = Cpt(EpicsSignal, "char_type", string=True)
