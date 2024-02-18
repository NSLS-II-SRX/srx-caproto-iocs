from __future__ import annotations

import tempfile
import time as ttime
from pathlib import Path

import h5py
import pytest

from srx_caproto_iocs.utils import now


@pytest.mark.cloud_friendly()
@pytest.mark.parametrize("date_template", ["%Y/%m/", "%Y/%m/%d", "mydir/%Y/%m/%d"])
def test_base_ophyd_templates(
    base_caproto_ioc, base_ophyd_device, date_template, num_frames=50
):
    with tempfile.TemporaryDirectory(prefix="/tmp/") as tmpdirname:
        date = now(as_object=True)
        write_dir_root = Path(tmpdirname)
        dir_template = f"{write_dir_root}/{date_template}"
        write_dir = Path(date.strftime(dir_template))
        write_dir.mkdir(parents=True, exist_ok=True)

        file_template = "scan_{num:06d}_{uid}.hdf5"

        dev = base_ophyd_device
        dev.write_dir.put(dir_template)
        dev.file_name.put(file_template)

        dev.set("stage").wait()

        full_file_path = dev.full_file_path.get()
        print(f"{full_file_path = }")

        for i in range(num_frames):
            print(f"Collecting frame {i}...")
            dev.set("acquire").wait()
            ttime.sleep(0.1)

        dev.set("unstage").wait()

        assert full_file_path, "The returned 'full_file_path' did not change."
        assert Path(full_file_path).is_file(), f"No such file '{full_file_path}'"

        with h5py.File(full_file_path, "r", swmr=True) as f:
            dataset = f["/entry/data/data"]
            assert dataset.shape == (num_frames, 256, 256)

        ttime.sleep(1.0)
