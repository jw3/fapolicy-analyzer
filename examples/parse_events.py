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

import  sys
import logging
logging.basicConfig(level=logging.WARNING)
import argparse
from fapolicy_analyzer import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("-i", "--input", default="events0.log", help="Specify the fapolicyd event debug log [default: events0.log ]")

    args = parser.parse_args()

    # Set Verbosity Level
    if args.verbose:
        logging.root.setLevel(logging.DEBUG)
        logging.debug("Verbosity enabled.")

    # Set input fapolicyd event log [default: events0.log]
    if args.input:
        fapd_debug_log=args.input
    
    # config loaded from $HOME/.config/fapolicy-analyzer/fapolicy-analyzer.toml
    s1 = System()
    print(f"found {len(s1.users())} system users")
    print(f"found {len(s1.groups())} system groups")

    umap = {u.id: u.name for u in s1.users()}
    gmap = {g.id: g.name for g in s1.groups()}

    # Only iterate and print maps if in verbose mode
    if args.verbose:
        logging.debug("\n\nUser Map:")
        for u in umap:
            logging.debug(f"{u}:\t{umap[u]}")

        logging.debug("\n\nGroup Map:")
        for g in gmap:
            logging.debug(f"{g}:\t{gmap[g]}")

    debug_log = s1.load_debuglog(args.input)
    for s in debug_log.subjects():
        logging.debug(f" - Getting all events associated with subject: {s}")
        for e in debug_log.by_subject(s):
            print({"u": umap[e.uid],
                   "g": gmap[e.gid], 
                   "s": {
                       "file": e.subject.file,
                       "trust": e.subject.trust,
                       "access": e.subject.access
                   },
                   "o": {
                       "file": e.object.file,
                       "trust": e.object.trust,
                       "access": e.object.access,
                       "mode": e.object.mode
                   }})
        print("...")


if __name__ == "__main__":
    main()
