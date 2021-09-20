import context  # noqa: F401
import pytest
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from unittest.mock import MagicMock
from time import localtime, strftime, mktime
from ui.trust_file_list import TrustFileList, epoch_to_string


_trust = [
    MagicMock(status="u", path="/tmp/bar", actual=MagicMock(last_modified=123456789)),
    MagicMock(status="t", path="/tmp/foo", actual=MagicMock(last_modified=123456789)),
]


def _trust_func(callback):
    callback(_trust)


@pytest.fixture
def widget():
    widget = TrustFileList(trust_func=_trust_func)
    return widget


def test_creates_widget(widget):
    assert type(widget.get_ref()) is Gtk.Box


def test_uses_custom_trust_func():
    trust_func = MagicMock()
    TrustFileList(trust_func=trust_func)
    trust_func.assert_called()


def test_uses_custom_markup_func():
    markup_func = MagicMock(return_value="t")
    TrustFileList(trust_func=_trust_func, markup_func=markup_func)
    markup_func.assert_called_with("t")


def test_loads_trust_store(widget):
    widget.load_trust(_trust)
    view = widget.get_object("treeView")
    assert [t.status for t in _trust] == [x[0] for x in view.get_model()]
    assert [t.path for t in _trust] == [x[2] for x in view.get_model()]


def test_fires_trust_selection_changed(widget):
    mockHandler = MagicMock()
    widget.trust_selection_changed += mockHandler
    view = widget.get_object("treeView")
    view.get_selection().select_path(Gtk.TreePath.new_first())
    mockHandler.assert_called_with(_trust[0])


def test_epoch_to_string():
    secsEpochCurrent = int(mktime(localtime()))
    secsEpochOneDayOld = secsEpochCurrent - (24 * 60 * 60)

    # Verify timestamps from today are display in hour:minute:sec format
    strExpected = strftime("%H:%M:%S", localtime(secsEpochCurrent))
    strFromEpochToString = epoch_to_string(secsEpochCurrent)
    assert strExpected == strFromEpochToString

    # Verify timestamps older than today are displayed as calendar date
    strExpected = strftime("%Y-%m-%d", localtime(secsEpochOneDayOld))
    strFromEpochToString = epoch_to_string(secsEpochOneDayOld)
    assert strExpected == strFromEpochToString

    # Verify a NULL string input outputs "Missing"
    assert epoch_to_string(None) == "Missing"
