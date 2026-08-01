# Copyright (C) 2026 Ronald Rink, d-fens GmbH, http://d-fens.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116

import unittest

from src.biz.dfch.asdste100nlp.cli import app


class TestCli(unittest.TestCase):
    def test_app_is_a_typer_application(self):
        import typer  # pylint: disable=import-outside-toplevel

        self.assertIsInstance(app, typer.Typer)

    def test_synonym_command_is_registered(self):
        names = {command.name or command.callback.__name__ for command in app.registered_commands}
        self.assertIn("synonym", names)

    def test_exactly_one_command_is_registered(self):
        self.assertEqual(1, len(app.registered_commands))


if __name__ == "__main__":
    unittest.main()
