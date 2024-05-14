#!/bin/bash

set -vxeuo pipefail

SCRIPT_DIR="$(dirname "$0")"

bash "${SCRIPT_DIR}/run-caproto-ioc.sh" srx_caproto_iocs.zebra.caproto_ioc "XF:05IDD-ES:1{{Dev:Zebra2}}:"
