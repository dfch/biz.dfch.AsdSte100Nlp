# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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
