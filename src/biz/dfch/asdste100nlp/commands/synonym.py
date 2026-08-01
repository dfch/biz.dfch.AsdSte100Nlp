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

"""``synonym`` find vocabulary entries that are WordNet synonyms of a word."""

from pathlib import Path

import typer

from biz.dfch.asdste100vocab import Vocab, Word

from ..nlp import Nlp
from .args import (
    UseSte100Opt,
    UseSte100TechnicalWordOpt,
    VocabFiles,
    WordArg,
)
from .render import print_word_table


def synonym(
    word: WordArg,
    use_ste100: UseSte100Opt = True,
    use_ste100_technical_word: UseSte100TechnicalWordOpt = False,
    files: VocabFiles = None,
) -> None:
    """
    Find vocabulary entries that are WordNet synonyms of a word.

    Looks up every WordNet synset for *word* (via ``nltk``) and
    cross-references their lemma names, case-insensitively, against the
    built-in STE100 vocabulary and any additional JSONL vocabulary files
    supplied via ``--file`` (approved and rejected entries both included).
    *word* itself is excluded from the results, which are sorted
    alphabetically.
    """

    assert isinstance(word, str) and word.strip(), word

    extra_files: list[Path] = files if files is not None else []

    vocab = Vocab(
        use_ste100=use_ste100,
        use_ste100_technical_word=use_ste100_technical_word,
        files=extra_files,
    )
    nlp = Nlp(vocab)

    results: list[Word] = nlp.synonym(word)

    if not results:
        typer.echo(f"No synonyms found for '{word}'.")
        raise typer.Exit(code=0)

    print_word_table(results)
