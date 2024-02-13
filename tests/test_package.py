from __future__ import annotations

import importlib.metadata

import srx_caproto_iocs as m


def test_version():
    assert importlib.metadata.version("srx_caproto_iocs") == m.__version__
