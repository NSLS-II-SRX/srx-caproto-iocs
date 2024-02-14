from __future__ import annotations

import subprocess
import sys
import time as ttime

import pytest

from srx_caproto_iocs.zebra.ophyd import ZebraWithCaprotoIOC


@pytest.fixture()
def zebra_ophyd_caproto():
    dev = ZebraWithCaprotoIOC("XF:05IDD-ES:1{Dev:Zebra2}:", name="zebra_ophyd_caproto")
    yield dev
    dev.ioc_stage.put("unstaged")


@pytest.fixture(scope="session")
def caproto_ioc(wait=3):
    env = {
        "EPICS_CAS_BEACON_ADDR_LIST": "127.0.0.1",
        "EPICS_CAS_AUTO_BEACON_ADDR_LIST": "no",
    }
    command = (
        sys.executable
        + " -m srx_caproto_iocs.zebra.caproto_ioc --prefix=XF:05IDD-ES:1{{Dev:Zebra2}}: --list-pvs"
    )
    print(
        f"Starting caproto IOC in via a fixture using the following command:\n\n  {command}\n"
    )
    p = subprocess.Popen(
        command.split(),
        start_new_session=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=False,
        env=env,
    )
    print(f"Wait for {wait} seconds...")
    ttime.sleep(wait)

    yield p

    p.terminate()

    std_out, std_err = p.communicate()
    std_out = std_out.decode()
    print(std_out)
