from __future__ import annotations

from ophyd import Component as Cpt
from ophyd import Device, EpicsSignal, EpicsSignalRO


class ZebraWithCaprotoIOC(Device):
    """An ophyd Device which works with the Zebra caproto extension IOC."""

    write_dir = Cpt(EpicsSignal, "write_dir", string=True)
    file_name = Cpt(EpicsSignal, "file_name", string=True)
    full_file_path = Cpt(EpicsSignalRO, "full_file_path", string=True)
    frame_num = Cpt(EpicsSignal, "frame_num")
    ioc_stage = Cpt(EpicsSignal, "stage", string=True)
