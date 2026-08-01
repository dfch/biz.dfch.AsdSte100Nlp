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

"""
Shared ``Annotated`` parameter definitions for CLI sub-commands.
"""

from pathlib import Path
from typing import Annotated, List, Optional

import typer

WordArg = Annotated[
    str,
    typer.Argument(
        help="The word to search synonyms for.",
    ),
]

UseSte100Opt = Annotated[
    bool,
    typer.Option(
        "--ste100/--no-ste100",
        help="Include (--ste100) or exclude (--no-ste100) the built-in STE100 base vocabulary.",
    ),
]

UseSte100TechnicalWordOpt = Annotated[
    bool,
    typer.Option(
        "--technical/--no-technical",
        help="Include (--technical) or exclude (--no-technical) the STE100 technical words (TN/TV).",
    ),
]

VocabFiles = Annotated[
    Optional[List[Path]],
    typer.Option(
        "--file",
        "-f",
        envvar="VOCAB_FILE",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help=(
            "Path to an existing JSONL vocabulary file."
            " Repeat for multiple files,"
            " e.g. ``--file a.jsonl --file b.jsonl``."
        ),
    ),
]
