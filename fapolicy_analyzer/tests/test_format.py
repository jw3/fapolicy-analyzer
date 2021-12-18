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

import context  # noqa: F401
from util.format import snake_to_camelcase, f


def test_snake_to_camelcase():
    assert snake_to_camelcase("foo_baz_test") == "fooBazTest"


def test_snake_to_camelcase_empty_string():
    assert snake_to_camelcase("") == ""


def test_snake_to_camelcase_none():
    assert snake_to_camelcase(None) is None


def test_snake_to_camelcase_leading_underscore():
    assert snake_to_camelcase("_foo") == "_foo"


def test_f():
    insert = "foo"
    assert f(f"insert is {insert}") == "insert is foo"


def test_f_none():
    assert f(None) is None
