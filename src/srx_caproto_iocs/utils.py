from __future__ import annotations

import datetime

import h5py
import numpy as np


def now(as_object=False):
    """A helper function to return ISO 8601 formatted datetime string."""
    _now = datetime.datetime.now()
    if as_object:
        return _now
    return _now.isoformat()


def save_hdf5(
    fname,
    data,
    group_name="/entry",
    group_path="data/data",
    dtype="float32",
    mode="x",
    update_existing=False,
):
    """The function to export the data to an HDF5 file."""
    h5file_desc = h5py.File(fname, mode, libver="latest")
    frame_shape = data.shape
    if not update_existing:
        group = h5file_desc.create_group(group_name)
        dataset = group.create_dataset(
            "data/data",
            data=np.full(fill_value=np.nan, shape=(1, *frame_shape)),
            maxshape=(None, *frame_shape),
            chunks=(1, *frame_shape),
            dtype=dtype,
        )
        frame_num = 0
    else:
        dataset = h5file_desc[f"{group_name}/{group_path}"]
        frame_num = dataset.shape[0]

    h5file_desc.swmr_mode = True

    dataset.resize((frame_num + 1, *frame_shape))
    dataset[frame_num, :, :] = data
    dataset.flush()
