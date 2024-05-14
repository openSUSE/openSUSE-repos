#!/bin/bash
#
# Copyright (C) 2024 SUSE LLC
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see <http://www.gnu.org/licenses/>.

last=${@:$#} # last parameter
other=${*%${!#}} # all parameters except the last
other=$(echo $other) # remove trailing space
image="${other##* }"

set -euo pipefail

test "$image" != "" || (echo empty image, exiting; exit 1)

testcase=$last

PODMAN=podman
(
PODMAN_info="$($PODMAN info >/dev/null 2>&1)" || $PODMAN info
[ -n "$testcase" ] || (echo No testcase provided; exit 1)
[ -f "$testcase" ] || (echo Cannot find file "$testcase"; exit 1 )
) >&2

thisdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
basename=$(basename "$testcase")
basename=${basename,,}
basename=${basename//:/_}


ident=opensuse.repo.t.$image
containername="$ident.${basename,,}"

echo image=$image
(
echo image2=$image
)

(
echo FROM registry.opensuse.org/opensuse/$image
cat << EOF
ENV container podman

ENV LANG en_US.UTF-8

RUN zypper -vvvn install systemd

WORKDIR /opt/project

# ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT ["/usr/lib/systemd/systemd"]
EOF
) | $PODMAN build -t $ident.image -f - $thisdir/../..

$PODMAN run --privileged --rm --name "$containername" -d -v"$thisdir/../..":/opt/project -- $ident.image

in_cleanup=0

ret=111

function cleanup {
    [ "$in_cleanup" != 1 ] || return
    in_cleanup=1
    if [ "$ret" != 0 ] && [ -n "${T_PAUSE_ON_FAILURE-}" ]; then
        read -rsn1 -p"Test failed, press any key to finish";echo
    fi
    [ "$ret" == 0 ] || echo FAIL $basename
    $PODMAN stop -t 0 "$containername" >&/dev/null || :
}

trap cleanup INT TERM EXIT
counter=1

# wait container start
until [ $counter -gt 10 ]; do
  sleep 0.5
  $PODMAN exec "$containername" pwd >& /dev/null && break
  ((counter++))
done

$PODMAN exec "$containername" pwd >& /dev/null || (echo Cannot start container; exit 1 ) >&2

set +e
$PODMAN exec -e TESTCASE="$testcase"  -i "$containername" bash -xe < "$testcase"
ret=$?
( exit $ret )

