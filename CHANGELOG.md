# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-08-01

### Added

- CLI (`nlp` console script, `biz.dfch.asdste100nlp.cli:app`), modeled after
  the sibling `biz-dfch-asdste100vocab` package's `vocab` CLI: a
  `typer.Typer` application in `cli.py`, with one sub-command module per
  command under `commands/`.
- `synonym` command: finds vocabulary entries that are WordNet synonyms of a
  word, via `Nlp.synonym()`, cross-referenced against the built-in STE100
  vocabulary and/or additional JSONL files (`--ste100`/`--no-ste100`,
  `--technical`/`--no-technical`, `--file`), rendered as a Rich table.
- `typer` and `python-dotenv` added as direct dependencies (CLI framework and
  `.env` loading, following the sibling package's `--env` option convention).
- Initial project scaffolding.
- `Nlp` class (`biz.dfch.asdste100nlp.nlp.Nlp`), constructed from a
  `biz-dfch-asdste100vocab` `Vocab` instance, with a `synonym(value)` method
  that looks up WordNet synsets (via `nltk`) and cross-references their
  lemma names against the bound vocabulary (approved and rejected entries),
  returning a deduplicated, alphabetically sorted `list[Word]`.
- `nltk` added as a direct dependency; the WordNet 3.0 corpus is vendored as
  static package data under `src/biz/dfch/asdste100nlp/data/nltk_data/`, so
  lookups work fully offline (`nltk.download()` is never called).
- `biz-dfch-asdste100vocab` added as a direct dependency.
- `NOTICE` file added, covering `nltk` (Apache-2.0), the vendored WordNet 3.0
  corpus (Princeton University license), and `biz-dfch-asdste100vocab`
  (AGPL-3.0-or-later).

### Changed

- `synonym` command: the "no synonyms found" message is now printed with
  plain `typer.echo` instead of a `rich.Console`-styled (yellow) message,
  dropping the direct `rich` import from the command module (the shared
  `commands/render.py` table renderer still uses `rich`).

### Fixed

- `rich` moved from the `dev` optional-dependency extra to the main
  `dependencies` in `pyproject.toml`: it is imported unconditionally by
  `commands/render.py` at CLI runtime (not just by dev/test tooling), so it
  was missing from installs of the published package.
- `NOTICE` updated to also cover `typer` (MIT), `python-dotenv`
  (BSD-3-Clause), and `rich` (MIT), which were direct/runtime dependencies
  not yet reflected there.
- `nlp.py`: silenced a `mypy` "missing library stubs or py.typed marker"
  warning on the `import nltk` statement with a
  `# type: ignore[import-untyped]` comment, matching the existing pattern
  already used for `from nltk.corpus import wordnet`.
