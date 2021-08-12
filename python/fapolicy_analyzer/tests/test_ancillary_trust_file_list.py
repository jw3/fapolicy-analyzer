import context  # noqa: F401
import pytest
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from unittest.mock import MagicMock
from ui.ancillary_trust_file_list import AncillaryTrustFileList
from ui.configs import Colors
from ui.strings import CHANGESET_ACTION_ADD, CHANGESET_ACTION_DEL
from ui.state_manager import stateManager

_trust = [
    MagicMock(status="d", path="/tmp/foo"),
    MagicMock(status="t", path="/tmp/baz"),
    MagicMock(status="u", path="/tmp/bar"),
]


def _trust_func(callback):
    callback(_trust)


@pytest.fixture
def widget():
    widget = AncillaryTrustFileList(trust_func=_trust_func)
    return widget


@pytest.fixture
def state():
    stateManager.del_changeset_q()
    yield stateManager
    stateManager.del_changeset_q()


def test_creates_widget(widget):
    assert type(widget.get_ref()) is Gtk.Box


def test_uses_custom_trust_func():
    trust_func = MagicMock()
    AncillaryTrustFileList(trust_func=trust_func)
    trust_func.assert_called()


def test_uses_custom_markup_func(widget):
    AncillaryTrustFileList(trust_func=_trust_func)
    view = widget.get_object("treeView")
    assert ["T/<b><u>D</u></b>", "<b><u>T</u></b>/D", "T/D"] == [
        x[0] for x in view.get_model()
    ]
    assert [Colors.LIGHT_RED, Colors.LIGHT_GREEN, Colors.LIGHT_YELLOW] == [
        x[3] for x in view.get_model()
    ]


def test_fires_files_added(widget, mocker):
    mockHandler = MagicMock()
    widget.files_added += mockHandler
    widget.on_addBtn_files_added(["foo"])
    mockHandler.assert_called_with(["foo"])


def test_trust_add_actions_in_view(widget, state):
    mockChangeset = MagicMock(
        get_path_action_map=MagicMock(return_value=({"/tmp/foo": "Add"}))
    )
    state.add_changeset_q(mockChangeset)
    widget.load_trust(_trust)
    model = widget.get_object("treeView").get_model()
    row = next(iter([x for x in model if x[1] == "/tmp/foo"]))
    assert CHANGESET_ACTION_ADD == row[4]


def test_trust_delete_actions_in_view(widget, state):
    mockChangeset = MagicMock(
        get_path_action_map=MagicMock(return_value=({"/tmp/foz": "Del"}))
    )
    state.add_changeset_q(mockChangeset)
    widget.load_trust(_trust)
    model = widget.get_object("treeView").get_model()
    row = next(iter([x for x in model if x[1] == "/tmp/foz"]))
    assert CHANGESET_ACTION_DEL == row[4]
