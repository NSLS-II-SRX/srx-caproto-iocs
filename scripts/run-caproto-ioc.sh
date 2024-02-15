#!/bin/bash

# shellcheck source=/dev/null
. /etc/profile.d/epics.sh

export EPICS_CAS_AUTO_BEACON_ADDR_LIST="no"
export EPICS_CAS_BEACON_ADDR_LIST="${EPICS_CA_ADDR_LIST}"

python -m srx_caproto_iocs.base --prefix="BASE:{{Dev:Save1}}:" --list-pvs
