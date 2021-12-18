#!/bin/sh -e
#
# Copyright Concurrent Technologies Corporation 2021
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

if [ $# -lt 2 ]; then
  echo "Usage: $(basename "$0") rpm_directory image1 [ image2 ... ]"
  exit 1
fi

_rpmdir="${1}"
shift

for I in $@; do
  docker run --rm -i \
    -v "$(realpath "${_rpmdir}")":/rpms \
    "$I" timeout 900 sh -e <<-RUN
			echo "Installing..."
			dnf install -qy fapolicyd /rpms/fapolicy-analyzer-*."$(echo "$I" | fgrep -q fedora && printf "fc$(echo "$I" | sed -e 's/^[^:]\+://')" || printf "el8")".x86_64.rpm > /dev/null
			sed -i -e 's/id = fapolicyd/id = root/' /etc/fapolicyd/fapolicyd.conf > /dev/null
			fapolicyd --debug > /dev/null || true
			echo ""
			rpm -q  fapolicyd
			rpm -q  fapolicy-analyzer
			echo ""
			rpm -qi fapolicy-analyzer
			echo ""
			echo "Testing..."
			python3 <<-TEST
				from fapolicy_analyzer import *
				s1 = System()
				print(f"found {len(s1.system_trust())} system trust entries\n")
			TEST
		RUN
done
