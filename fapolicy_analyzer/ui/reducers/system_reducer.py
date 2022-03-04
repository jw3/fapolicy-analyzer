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

from typing import Sequence

from fapolicy_analyzer import EventLog, Group, Rule, Trust, User
from fapolicy_analyzer.ui.actions import (
    ERROR_SYSTEM_INITIALIZATION,
    SYSTEM_INITIALIZED,
    get_events,
    get_groups,
    get_rules,
    get_system_trust,
    get_users,
)
from fapolicy_analyzer.ui.reducers.resource_reducer import ResourceReducer
from redux import Reducer, combine_reducers, handle_actions

from .ancillary_trust_reducer import ancillary_trust_reducer
from .changeset_reducer import changeset_reducer

event_reducer = ResourceReducer[Sequence[EventLog]](get_events).reducer
group_reducer = ResourceReducer[Sequence[Group]](get_groups).reducer
rule_reducer = ResourceReducer[Sequence[Rule]](get_rules).reducer
system_trust_reducer = ResourceReducer[Sequence[Trust]](get_system_trust).reducer
user_reducer = ResourceReducer[Sequence[User]](get_users).reducer

system_initialized_reducer: Reducer = handle_actions(
    {SYSTEM_INITIALIZED: lambda *_: True}, False
)

system_initialization_error_reducer: Reducer = handle_actions(
    {ERROR_SYSTEM_INITIALIZATION: lambda *_: True}, False
)

system_reducer: Reducer = combine_reducers(
    {
        "initialization_error": system_initialization_error_reducer,
        "initialized": system_initialized_reducer,
        "ancillary_trust": ancillary_trust_reducer,
        "changesets": changeset_reducer,
        "events": event_reducer,
        "groups": group_reducer,
        "rules": rule_reducer,
        "system_trust": system_trust_reducer,
        "users": user_reducer,
    }
)
