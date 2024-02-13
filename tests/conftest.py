from __future__ import annotations

import subprocess
import time as ttime

import pytest

from srx_caproto_iocs.zebra.ophyd import ZebraWithCaprotoIOC


@pytest.fixture()
def zebra_ophyd_caproto():
    dev = ZebraWithCaprotoIOC("XF:05IDD-ES:1{Dev:Zebra2}:", name="zebra_ophyd_caproto")
    yield dev
    dev.ioc_stage.put("unstaged")


@pytest.fixture(scope="session")
def _caproto_ioc():
    command = 'EPICS_CAS_BEACON_ADDR_LIST=127.0.0.1 EPICS_CAS_AUTO_BEACON_ADDR_LIST=no python -m srx_caproto_iocs.zebra.caproto_ioc --prefix="XF:05IDD-ES:1{{Dev:Zebra2}}:" --list-pvs'
    p = subprocess.Popen(
        command.split(),
        start_new_session=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
    )
    ttime.sleep(2.0)

    yield

    std_out, std_err = p.communicate()
    std_out = std_out.decode()
    print(std_out)
    p.terminate()
