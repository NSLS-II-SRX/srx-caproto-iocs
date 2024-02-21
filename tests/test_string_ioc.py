from __future__ import annotations

import string
import subprocess

import pytest

LIMIT = 40 - 1
STRING_39 = string.ascii_letters[:LIMIT]
STRING_LONGER = string.ascii_letters


@pytest.mark.cloud_friendly()
@pytest.mark.parametrize("value", [STRING_39, STRING_LONGER])
def test_strings(
    # caproto_ioc_channel_types,
    ophyd_channel_types,
    value,
):
    ophyd_channel_types.bare_string.put(value)

    if len(value) <= LIMIT:
        ophyd_channel_types.implicit_string_type.put(value)
    else:
        with pytest.raises(ValueError):
            ophyd_channel_types.implicit_string_type.put(value)

    if len(value) <= LIMIT:
        ophyd_channel_types.string_type.put(value)
    else:
        with pytest.raises(ValueError):
            ophyd_channel_types.string_type.put(value)

    if len(value) <= LIMIT:
        ophyd_channel_types.char_type_as_string.put(value)
    else:
        with pytest.raises(ValueError):
            ophyd_channel_types.char_type_as_string.put(value)

    ophyd_channel_types.char_type.put(value)


@pytest.mark.cloud_friendly()
@pytest.mark.needs_epics_core()
@pytest.mark.parametrize("value", [STRING_39, STRING_LONGER])
def test_with_epics_core(ophyd_channel_types, value):
    for cpt in ophyd_channel_types.component_names:
        ret = subprocess.run(
            ["caput", "-S", getattr(ophyd_channel_types, cpt).pvname, value],
            check=False,
        )
        print(f"{cpt=}: {ret.returncode=}\n")
