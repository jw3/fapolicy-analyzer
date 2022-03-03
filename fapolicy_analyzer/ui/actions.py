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

from enum import Enum
from itertools import count
from typing import Any, Iterator, NamedTuple

from fapolicy_analyzer import Changeset
from fapolicy_analyzer.ui.resource import Resource
from redux import Action, create_action

INIT_SYSTEM = "INIT_SYSTEM"
SYSTEM_INITIALIZED = "SYSTEM_INITIALIZED"
ERROR_SYSTEM_INITIALIZATION = "ERROR_SYSTEM_INITIALIZATION"

ADD_NOTIFICATION = "ADD_NOTIFICATION"
REMOVE_NOTIFICATION = "REMOVE_NOTIFICATION"

SET_SYSTEM_CHECKPOINT = "SET_SYSTEM_CHECKPOINT"
RESTORE_SYSTEM_CHECKPOINT = "RESTORE_SYSTEM_CHECKPOINT"
ERROR_RESTORE_SYSTEM_CHECKPOINT = "ERROR_RESTORE_SYSTEM_CHECKPOINT"

ADD_CHANGESETS = "ADD_CHANGESETS"
APPLY_CHANGESETS = "APPLY_CHANGESETS"
CLEAR_CHANGESETS = "CLEAR_CHANGESET"


def _create_action(type: str, payload: Any = None) -> Action:
    return create_action(type)(payload)


_ids: Iterator[int] = iter(count())


class NotificationType(Enum):
    ERROR = "error"
    WARN = "warn"
    INFO = "info"
    SUCCESS = "success"


class Notification(NamedTuple):
    id: int
    text: str
    type: NotificationType


deploy_ancillary_trust = Resource("DEPLOY_ANCILLARY_TRUST")
get_ancillary_trust = Resource("GET_ANCILLARY_TRUST")
get_events = Resource("GET_EVENTS")
get_groups = Resource("GET_GROUPS")
get_rules = Resource("GET_RULES")
get_system_trust = Resource("GET_SYSTEM_TRUST")
get_users = Resource("GET_USERS")


def add_notification(text: str, type: NotificationType) -> Action:
    return _create_action(ADD_NOTIFICATION, (Notification(next(_ids), text, type)))


def remove_notification(id: int) -> Action:
    return _create_action(REMOVE_NOTIFICATION, (Notification(id, "", None)))


def add_changesets(*changesets: Changeset) -> Action:
    return _create_action(ADD_CHANGESETS, *changesets)


def apply_changesets(*changesets: Changeset) -> Action:
    return _create_action(APPLY_CHANGESETS, changesets)


def clear_changesets() -> Action:
    return _create_action(CLEAR_CHANGESETS)


def set_system_checkpoint() -> Action:
    return _create_action(SET_SYSTEM_CHECKPOINT)


def restore_system_checkpoint() -> Action:
    return _create_action(RESTORE_SYSTEM_CHECKPOINT)


def error_restore_system_checkpoint() -> Action:
    return _create_action(ERROR_RESTORE_SYSTEM_CHECKPOINT)


def init_system() -> Action:
    return _create_action(INIT_SYSTEM)


def system_initialized() -> Action:
    return _create_action(SYSTEM_INITIALIZED)


def system_initialization_error() -> Action:
    return _create_action(ERROR_SYSTEM_INITIALIZATION)
