from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from ophyd.status import SubscriptionStatus

from srx_caproto_iocs.utils import now


# TODO: use pytest.mark.parametrize to implement many use cases.
@pytest.mark.parametrize("date_template", ["%Y/%m/", "%Y/%m/%d", "mydir/%Y/%m/%d"])
def test_zebra_ophyd_caproto(zebra_ophyd_caproto, date_template):
    with tempfile.TemporaryDirectory() as tmpdirname:
        date = now(as_object=True)
        write_dir_root = Path(tmpdirname)
        dir_template = f"{write_dir_root}/{date_template}"
        write_dir = Path(date.strftime(dir_template))
        write_dir.mkdir(parents=True, exist_ok=True)

        print(f"{write_dir = }")

        file_template = "scan_{num:06d}_{uid}.hdf5"

        dev = zebra_ophyd_caproto
        dev.write_dir.put(dir_template)
        dev.file_name.put(file_template)

        def cb(value, old_value, **kwargs):
            if value == "staged" and old_value == "unstaged":
                return True
            return False

        st = SubscriptionStatus(dev.ioc_stage, callback=cb, run=False)
        dev.ioc_stage.put("staged")
        st.wait()

        full_file_path = dev.full_file_path.get()
        print(f"{full_file_path = }")
