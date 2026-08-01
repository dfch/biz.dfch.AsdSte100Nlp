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

from biz.dfch.asdste100vocab.vocab import Vocab
from biz.dfch.asdste100vocab.word import Word

from src.biz.dfch.asdste100nlp.nlp import Nlp

_WORD_LIST_1 = "test_nlp_word_list1.jsonl"


class TestNlpSynonym(unittest.TestCase):
    def _make_sut(self, vocab_file: str = _WORD_LIST_1) -> Nlp:
        fullname = Path(__file__).parent / vocab_file
        vocab = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )
        return Nlp(vocab)

    # ------------------------------------------------------------------
    # Return type
    # ------------------------------------------------------------------

    def test_synonym_returns_list(self):
        sut = self._make_sut()

        result = sut.synonym("quick")

        self.assertIsInstance(result, list)

    def test_synonym_returns_list_of_words(self):
        sut = self._make_sut()

        result = sut.synonym("quick")

        for item in result:
            self.assertIsInstance(item, Word)

    # ------------------------------------------------------------------
    # WordNet cross-referencing
    # ------------------------------------------------------------------

    def test_synonym_finds_approved_wordnet_synonyms(self):
        sut = self._make_sut()

        result = sut.synonym("quick")

        names = [item.name.lower() for item in result]
        self.assertIn("fast", names)
        self.assertIn("speedy", names)

    def test_synonym_includes_rejected_entries(self):
        sut = self._make_sut()

        result = sut.synonym("quick")

        names = [item.name.lower() for item in result]
        self.assertIn("nimble", names)

    def test_synonym_excludes_unrelated_words(self):
        sut = self._make_sut()

        result = sut.synonym("quick")

        names = [item.name.lower() for item in result]
        self.assertNotIn("aeroplane", names)

    def test_synonym_excludes_the_word_itself(self):
        sut = self._make_sut()

        result = sut.synonym("quick")

        names = [item.name.lower() for item in result]
        self.assertNotIn("quick", names)

    # ------------------------------------------------------------------
    # Sort order
    # ------------------------------------------------------------------

    def test_synonym_returns_alphabetically_sorted_results(self):
        sut = self._make_sut()

        result = sut.synonym("quick")

        names = [item.name.lower() for item in result]
        self.assertEqual(sorted(names), names)

    # ------------------------------------------------------------------
    # No match / out-of-vocabulary
    # ------------------------------------------------------------------

    def test_synonym_out_of_vocabulary_word_returns_empty_list(self):
        sut = self._make_sut()

        result = sut.synonym("zzzzzzzzzznotaword")

        self.assertEqual(0, len(result))

    def test_synonym_no_vocabulary_match_returns_empty_list(self):
        sut = self._make_sut()

        # "aeroplane" has WordNet synonyms (e.g. "airplane"), but none of
        # them are present in the fixture vocabulary.
        result = sut.synonym("aeroplane")

        self.assertEqual(0, len(result))

    # ------------------------------------------------------------------
    # Case-insensitivity
    # ------------------------------------------------------------------

    def test_synonym_is_case_insensitive(self):
        sut = self._make_sut()

        result = sut.synonym("QUICK")

        names = [item.name.lower() for item in result]
        self.assertIn("fast", names)

    # ------------------------------------------------------------------
    # Guard assertions
    # ------------------------------------------------------------------

    def test_synonym_none_value_throws(self):
        sut = self._make_sut()

        with self.assertRaises(AssertionError):
            sut.synonym(None)  # type: ignore
