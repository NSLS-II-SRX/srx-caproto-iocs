from __future__ import annotations

from ophyd import Component as Cpt
from ophyd import Device, EpicsSignal, EpicsSignalRO


class ZebraWithCaprotoIOC(Device):
    write_dir = Cpt(EpicsSignal, "write_dir")
    file_name = Cpt(EpicsSignal, "file_name")
    full_file_path = Cpt(EpicsSignalRO, "full_file_path")
    frame_num = Cpt(EpicsSignal, "frame_num")
    ioc_stage = Cpt(EpicsSignal, "ioc_stage")
