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

"""Nlp class."""

from __future__ import annotations

import os
from pathlib import Path

# `nltk` >= 3.10 installs a meta-path finder (`nltk.inisec`) that blocks any
# import it initiates (directly or transitively, e.g. `nltk` -> `regex`) when
# that import resolves to a path under the current working directory -- a
# mitigation against CWE-427 (untrusted-CWD module hijacking). This produces
# a false positive whenever the host application's own virtual environment is
# nested inside its working directory (e.g. a `.venv` at the project root,
# the default layout for `uv`/in-project venvs), because the dependency then
# genuinely resolves from a path under `cwd`, even though it is the trusted
# venv, not an attacker-planted file. We vendor WordNet ourselves and never
# read anything from `cwd`, so this project's specific threat model is not
# improved by the check; disable it (only if the host application has not
# already made an explicit choice) before `nltk` installs the hook.
os.environ.setdefault("NLTK_DISABLE_IMPORT_SECURITY", "1")

import nltk  # type: ignore[import-untyped]
from biz.dfch.asdste100vocab import Vocab
from biz.dfch.asdste100vocab import Word

# The WordNet corpus is vendored as static package data (see `data/nltk_data`)
# so this library works fully offline -- `nltk.download(...)` is never called.
_WORDNET_DATA_DIR = Path(__file__).resolve().parent / "data" / "nltk_data"
if str(_WORDNET_DATA_DIR) not in nltk.data.path:
    nltk.data.path.insert(0, str(_WORDNET_DATA_DIR))

# `wordnet` is imported only after `nltk.data.path` above has been extended
# with the vendored corpus location, so its lazy corpus loader finds it.
from nltk.corpus import wordnet  # type: ignore[import-untyped]  # noqa: E402  pylint: disable=wrong-import-position,wrong-import-order


class Nlp:
    """Natural-language processing helpers layered on top of a `Vocab` instance."""

    # pylint: disable=too-few-public-methods
    # More methods (e.g. a future vector/embedding-based `similar` lookup)
    # are expected to be added alongside `synonym`.

    _vocab: Vocab

    def __init__(self, vocab: Vocab) -> None:
        """
        Instantiates an `Nlp` helper bound to a vocabulary.

        Parameters
        ----------
        vocab:
            The `Vocab` instance whose entries are used as the comparison
            universe for the methods on this class.
        """

        assert isinstance(vocab, Vocab), type(vocab)

        self._vocab = vocab

    def synonym(self, value: str) -> list[Word]:
        """
        Search for synonyms of a word in the vocabulary using WordNet
        synsets (`nltk`).

        Every WordNet synset for *value* is collected and its lemma names
        are cross-referenced, case-insensitively, against the bound
        vocabulary's entries by name -- the same scope as `Vocab.find`/
        `Vocab.match`/`Vocab.similar` (approved and rejected entries both
        included). *value* itself is excluded from the result. Because
        strict same-synset synonymy has no meaningful similarity gradient,
        results are sorted alphabetically (the same convention
        `Vocab.examine` uses) rather than by WordNet's internal, not
        guaranteed stable, iteration order.

        Parameters
        ----------
        value:
            The word to search synonyms for.

        Returns
        -------
        list[Word]
            A deduplicated, alphabetically sorted list of matching `Word`
            objects. Empty if *value* has no WordNet synsets (out-of-
            vocabulary) or none of its synonyms are present in the bound
            vocabulary.
        """

        assert isinstance(value, str), type(value)

        synsets = wordnet.synsets(value)
        lemma_names = {
            lemma.name().replace("_", " ").lower()
            for synset in synsets
            if synset is not None
            for lemma in synset.lemmas()
        }
        lemma_names.discard(value.lower())

        seen: set[int] = set()
        result: list[Word] = []
        for item in self._vocab:
            if item.name.lower() in lemma_names and id(item) not in seen:
                seen.add(id(item))
                result.append(item)

        result.sort(key=lambda word: word.name.lower())
        return result
