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

from fapolicy_analyzer import *


def show_event(e):
    sub = e.subject
    obj = e.object
    print(f"\t - {e.uid}:{e.gid} {sub.file} => {obj.file}")


s = System()
log = s.load_debuglog("tests/data/events2.log")

users_in_log = []
for u in s.users():
    if log.by_user(u.id):
        users_in_log.append(u.id)

groups_in_log = []
for g in s.groups():
    if log.by_group(g.id):
        groups_in_log.append(g.id)

print(f"## Users in log: {users_in_log}")
print(f"## Groups in log: {groups_in_log}")
print(f"## Subjects in log: {len(log.subjects())}")
print()

print("## User events")
for uid in users_in_log:
    for e in log.by_user(uid):
        show_event(e)

print("## Group events")
for gid in groups_in_log:
    for e in log.by_group(gid):
        show_event(e)
