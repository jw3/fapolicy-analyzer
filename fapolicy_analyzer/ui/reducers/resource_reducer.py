# Copyright Concurrent Technologies Corporation 2022
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

from typing import Any, Generic, NamedTuple, Optional, TypeVar, cast

from fapolicy_analyzer.ui.resource import Resource
from redux import Action, Reducer, handle_actions

T = TypeVar("T")


class ResourceState(NamedTuple):
    error: Optional[str]
    loading: bool
    resource: Any


class ResourceReducer(Generic[T]):
    def __init__(self, resource: Resource):
        self.__reducer: Reducer = handle_actions(
            {
                resource.request_type: self.__handle_request,
                resource.receive_type: self.__handle_received,
                resource.error_type: self.__handle_error,
            },
            ResourceState(error=None, resource=[], loading=False),
        )

    @property
    def reducer(self) -> Reducer:
        return self.__reducer

    def __create_state(
        self, state: ResourceState, **kwargs: Optional[Any]
    ) -> ResourceState:
        return ResourceState(**{**state._asdict(), **kwargs})

    def __handle_request(self, state: ResourceState, _: Action) -> ResourceState:
        return self.__create_state(state, loading=True, error=None)

    def __handle_received(self, state: ResourceState, action: Action) -> ResourceState:
        payload = cast(T, action.payload)
        return self.__create_state(state, resource=payload, error=None, loading=False)

    def __handle_error(self, state: ResourceState, action: Action) -> ResourceState:
        payload = cast(str, action.payload)
        return self.__create_state(state, error=payload, loading=False)
