from __future__ import annotations

from ophyd.status import SubscriptionStatus

from srx_caproto_iocs.utils import now


# TODO: use pytest.mark.parametrize to implement many use cases.
def test_zebra_ophyd_caproto(tmp_path, zebra_ophyd_caproto):
    date = now(as_object=True)
    write_dir_root = tmp_path / "zebra/"
    dir_template = f"{write_dir_root}/%Y/%m/"
    write_dir = date.strftime(dir_template)
    write_dir.mkdir()

    print(f"{write_dir = }\n{type(write_dir) = }")

    file_template = "scan_{num:06d}_{uid}.hdf5"

    dev = zebra_ophyd_caproto
    dev.write_dir.put(dir_template)
    dev.file_name.put(file_template)

    def cb(value, old_value, **kwargs):
        if value == "staged" and old_value == "unstaged":
            return True
        return False

    st = SubscriptionStatus(dev.ioc_stage, callback=cb, run=False)
    dev.ioc_stage.set("stage").wait()
    st.wait()

    full_file_path = dev.full_file_path.get()
    print(f"{full_file_path = }")

    assert full_file_path
