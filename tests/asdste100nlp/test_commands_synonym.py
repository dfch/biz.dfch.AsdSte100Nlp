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

from pathlib import Path
import unittest

from typer.testing import CliRunner

from src.biz.dfch.asdste100nlp.cli import app

_WORD_LIST_1 = "test_nlp_word_list1.jsonl"
_runner = CliRunner()


class TestCommandsSynonym(unittest.TestCase):
    def _vocab_file(self, name: str = _WORD_LIST_1) -> str:
        return str(Path(__file__).parent / name)

    def test_synonym_prints_approved_and_rejected_matches(self):
        result = _runner.invoke(
            app,
            ["synonym", "quick", "--no-ste100", "--file", self._vocab_file()],
        )

        self.assertEqual(0, result.exit_code)
        self.assertIn("fast", result.stdout)
        self.assertIn("speedy", result.stdout)
        self.assertIn("nimble", result.stdout)

    def test_synonym_excludes_unrelated_words(self):
        result = _runner.invoke(
            app,
            ["synonym", "quick", "--no-ste100", "--file", self._vocab_file()],
        )

        self.assertEqual(0, result.exit_code)
        self.assertNotIn("aeroplane", result.stdout)

    def test_synonym_no_match_prints_message_and_exits_zero(self):
        result = _runner.invoke(
            app,
            ["synonym", "zzzzzzzznotaword", "--no-ste100", "--file", self._vocab_file()],
        )

        self.assertEqual(0, result.exit_code)
        self.assertIn("No synonyms found", result.stdout)

    def test_synonym_missing_word_argument_fails(self):
        result = _runner.invoke(app, ["synonym"])

        self.assertNotEqual(0, result.exit_code)

    def test_synonym_help_shows_command_description(self):
        result = _runner.invoke(app, ["synonym", "--help"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("synonyms", result.stdout.lower())

    def test_app_shown_help_lists_synonym_command(self):
        result = _runner.invoke(app, ["--help"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("synonym", result.stdout)


if __name__ == "__main__":
    unittest.main()
