from __future__ import annotations

import pytest

from srx_caproto_iocs.zebra.ophyd import ZebraWithCaprotoIOC


@pytest.fixture()
def zebra_ophyd_caproto():
    dev = ZebraWithCaprotoIOC("XF:05IDD-ES:1{Dev:Zebra2}:", name="zebra_ophyd_caproto")
    yield dev
    dev.ioc_stage.put("unstaged")
