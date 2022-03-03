from typing import Any

from redux import Action, create_action


class Resource:
    def __init__(self, namespace: str):  # , action: Callable):
        # self.__action = action
        self.__namespace = namespace
        self.__request_type = f"{self.__namespace}_BEGIN"
        self.__receive_type = f"{self.__namespace}_SUCCESS"
        self.__error_type = f"{self.__namespace}_FAILURE"

    @property
    def request_type(self) -> str:
        return self.__request_type

    @property
    def receive_type(self) -> str:
        return self.__receive_type

    @property
    def error_type(self) -> str:
        return self.__error_type

    def request(self, *args) -> Action:
        return create_action(self.__request_type)(args)

    def receive(self, res: Any) -> Action:
        return create_action(self.__receive_type)(res)

    def error(self, err: str) -> Action:
        return create_action(self.__error_type)(err)

    def execute(self, *args):
        from fapolicy_analyzer.ui.store import dispatch

        dispatch(self.request(*args))

        # return dispatch => {
        #   dispatch(this.request())

        #   // not sure if `null` is right arg, but it seems to work
        #   return this.action.apply(null, arguments)
        #     .then(res => dispatch(this.receive(res)))
        #     .catch(err => dispatch(this.error(err)))
        # }
