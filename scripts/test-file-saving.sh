#!/bin/bash

set -vxeuo pipefail

# shellcheck source=/dev/null
if [ -f "/etc/profile.d/epics.sh" ]; then
    . /etc/profile.d/epics.sh
fi

num="${1:-50}"

data_dir="/tmp/test/$(date +%Y/%m/%d)"

if [ ! -d "${data_dir}" ]; then
	mkdir -v -p "${data_dir}"
fi

caput "BASE:{Dev:Save1}:write_dir" "${data_dir}"
caput "BASE:{Dev:Save1}:file_name" "saveme_{num:06d}_{uid}.h5"
caput "BASE:{Dev:Save1}:stage" 1
caget -S "BASE:{Dev:Save1}:full_file_path"
for i in $(seq "$num"); do
    echo "$i"
    sleep 0.1
    caput "BASE:{Dev:Save1}:acquire" 1
done

caput "BASE:{Dev:Save1}:stage" 0

caget -S "BASE:{Dev:Save1}:full_file_path"

exit 0
