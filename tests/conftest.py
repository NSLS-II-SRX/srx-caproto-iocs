from __future__ import annotations

import os
import socket
import subprocess
import sys
import time as ttime
from pprint import pformat

import netifaces
import pytest

from srx_caproto_iocs.base import OphydDeviceWithCaprotoIOC

CAPROTO_PV_PREFIX = "BASE:{{Dev:Save1}}:"
OPHYD_PV_PREFIX = CAPROTO_PV_PREFIX.replace("{{", "{").replace("}}", "}")


@pytest.fixture()
def base_ophyd_device():
    dev = OphydDeviceWithCaprotoIOC(
        OPHYD_PV_PREFIX, name="ophyd_device_with_caproto_ioc"
    )
    yield dev
    dev.ioc_stage.put("unstaged")


@pytest.fixture(scope="session")
def base_caproto_ioc(wait=3):
    first_three = ".".join(socket.gethostbyname(socket.gethostname()).split(".")[:3])
    broadcast = f"{first_three}.255"

    print(f"{broadcast = }")

    env = {
        "EPICS_CAS_BEACON_ADDR_LIST": os.getenv("EPICS_CA_ADDR_LIST", broadcast),
        "EPICS_CAS_AUTO_BEACON_ADDR_LIST": "no",
    }

    print(f"Updating env with:\n\n{pformat(env)}\n")
    os.environ.update(env)

    interfaces = netifaces.interfaces()
    print(f"{interfaces = }")
    for interface in interfaces:
        addrs = netifaces.ifaddresses(interface)
        try:
            print(f"{interface = }: {pformat(addrs[netifaces.AF_INET])}")
        except Exception as e:
            print(f"{interface = }: exception:\n  {e}")

    command = f"{sys.executable} -m srx_caproto_iocs.base --prefix={CAPROTO_PV_PREFIX} --list-pvs"
    print(
        f"\nStarting caproto IOC in via a fixture using the following command:\n\n  {command}\n"
    )
    p = subprocess.Popen(
        command.split(),
        start_new_session=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=False,
        env=os.environ,
    )
    print(f"Wait for {wait} seconds...")
    ttime.sleep(wait)

    yield p

    p.terminate()

    std_out, std_err = p.communicate()
    std_out = std_out.decode()
    sep = "=" * 80
    print(f"STDOUT:\n{sep}\n{std_out}")
    print(f"STDERR:\n{sep}\n{std_err}")
