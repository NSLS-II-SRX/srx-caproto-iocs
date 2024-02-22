#!/bin/bash

set -vxeuo pipefail

PYTHON_VERSION="${1:-3.11}"

act -W .github/workflows/ci.yml -j checks --matrix python-version:"${PYTHON_VERSION}"
