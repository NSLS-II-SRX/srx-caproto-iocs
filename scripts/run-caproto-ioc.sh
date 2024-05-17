#!/bin/bash

set -vxeuo pipefail

CAPROTO_IOC="${1:-srx_caproto_iocs.base}"
DEFAULT_PREFIX="BASE:{{Dev:Save1}}:"
CAPROTO_IOC_PREFIX="${2:-${DEFAULT_PREFIX}}"
# shellcheck source=/dev/null
if [ -f "/etc/profile.d/epics.sh" ]; then
    . /etc/profile.d/epics.sh
fi

export EPICS_CAS_AUTO_BEACON_ADDR_LIST="no"
export EPICS_CAS_BEACON_ADDR_LIST="${EPICS_CA_ADDR_LIST:-127.0.0.255}"

python -m "${CAPROTO_IOC}" --prefix="${CAPROTO_IOC_PREFIX}" --list-pvs
