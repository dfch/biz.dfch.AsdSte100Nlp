# biz.dfch.AsdSte100Nlp

[![ASD-STE100: Issue 9](https://img.shields.io/badge/ASD--STE100-Issue%209-blue.svg)](https://www.asd-ste100.org/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)
[![Pylint and unittest](https://github.com/dfch/biz.dfch.AsdSte100Nlp/actions/workflows/ci.yml/badge.svg)](https://github.com/dfch/biz.dfch.AsdSte100Nlp/actions/workflows/ci.yml)
[![TestPyPI version](https://img.shields.io/badge/dynamic/json?url=https://test.pypi.org/pypi/biz-dfch-asdste100nlp/json&label=TestPyPI&query=$.info.version&color=orange)](https://test.pypi.org/project/biz-dfch-asdste100nlp/)
[![PyPI version](https://img.shields.io/badge/dynamic/json?url=https://www.pypi.org/pypi/biz-dfch-asdste100nlp/json&label=PyPI&query=$.info.version&color=blue)](https://www.pypi.org/project/biz-dfch-asdste100nlp/)
[![PyPI downloads](https://img.shields.io/pypi/dm/biz-dfch-asdste100nlp.svg)](https://pypistats.org/packages/biz-dfch-asdste100nlp)

## Introduction

This is a Python library that implements natural language processing helpers
for [ASD-STE100 Issue 9](https://www.asd-ste100.org/) (Simplified Technical
English) tooling. The `Nlp` class is a plain domain object, reusable
directly or as the backend for other tools; a `typer`-based CLI (`nlp`) is
also included for interactive/scripted use.

The `Nlp` class is constructed from a
[`biz-dfch-asdste100vocab`](https://github.com/dfch/biz.dfch.AsdSte100Vocab)
`Vocab` instance and currently offers `synonym(value)`, a WordNet-based
(`nltk`) thesaurus lookup cross-referenced against the vocabulary. The
WordNet 3.0 corpus is vendored as static package data, so lookups work fully
offline -- `nltk.download()` is never called at runtime.

ASD-STE100: Copyright by (c) [ASD](https://www.asd-europe.org/).

I am in no way affiliated with ASD. ASD does not endorse my work.

## CLI usage

Install the `dev` dependencies (see below), then run the `synonym` command:

```
uv run nlp synonym quick
```

By default, the built-in STE100 vocabulary is searched. Add your own JSONL
vocabulary file(s) with `--file` (repeatable), and toggle the built-in
vocabulary/technical words with `--ste100`/`--no-ste100` and
`--technical`/`--no-technical`:

```
uv run nlp synonym quick --no-ste100 --file ./vocab.jsonl
```

Use `--help` on the application or any sub-command for the full option list,
and `--env` to load a specific `.env` file.

Related projects in this family:

* [biz.dfch.AsdSte100Vocab](https://github.com/dfch/biz.dfch.AsdSte100Vocab) — the ASD-STE100 Issue 9 vocabulary
* [biz.dfch.AsdSte100Rules](https://github.com/dfch/biz.dfch.AsdSte100Rules) — the ASD-STE100 Issue 9 ruleset
* [biz.dfch.AsdSte100Lookup](https://github.com/dfch/biz.dfch.AsdSte100Lookup) — an interactive lookup CLI
* [biz.dfch.AsdSte100Mcp](https://github.com/dfch/biz.dfch.AsdSte100Mcp) — an MCP server exposing vocabulary/rules lookup

## Installation

[biz-dfch-asdste100nlp](https://pypi.org/project/biz-dfch-asdste100nlp/) is on [PyPI](https://pypi.org). Create a virtual environment and install the library with `pip`:

```
pip install biz-dfch-asdste100nlp
```

Or install with `uv`:

```
uv add biz-dfch-asdste100nlp
```

## Development

Install the `dev` dependencies:

```
uv sync --extra dev
# or
uv pip install -e ".[dev]"
# or
pip install -e ".[dev]"
```

Run the checks:

```
uv run --frozen ruff format --check
uv run --frozen ruff check
uv run --frozen pylint $(git ls-files '*.py') || true
uv run --frozen python -m unittest discover -v -s tests -t . -p "test_*.py"
```

See [CONTRIBUTING.md](./CONTRIBUTING.md) for more information.

## Make a Release

### 1. Make sure that all tests are satisfactory

Before you make the release, make sure the CI pipeline is green on the `dev` branch:

```
uv run --frozen ruff format --check
uv run --frozen ruff check
uv run --frozen pylint $(git ls-files '*.py') || true
uv run --frozen python -m unittest discover -v -s tests -t . -p "test_*.py"
```

### 2. Increase the version

Update the version in `pyproject.toml`:

```toml
version = "x.y.z"
```

### 3. Commit and push to `dev`

```
git add pyproject.toml
git commit -m "chore: bump version to vx.y.z"
git push origin dev
```

### 4. Merge `dev` into `main`

```
git checkout main
git merge dev
git push origin main
```

### 5. Create and push a version tag

This will create a binary artifact of the application and add it to the `release`.

```
export VERSION=x.y.z
git tag v${VERSION}
git push origin v${VERSION}
```

Then, select the `dev` branch to continue your work.

```
git checkout dev
```

Pushing the tag automatically triggers the `publish.yml` workflow, which will:
* build the `sdist` and `wheel` with `uv build`
    (**this step creates the artifact**)
* create a GitHub Release with auto-generated release notes
* upload the files as a release artifact
    (**this step adds the artifact to the release**)

## License

This library is licensed under the [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0). See [LICENSE](./LICENSE) for more information.

ASD-STE100 Simplified Technical English (Standard for Technical Documentation), Issue 9

Copyright 2025 [Aerospace, Security and Defence Industries Association of Europe (ASD)](https://www.asd-europe.org), https://www.asd-europe.org.

This library or the maintainer is not affiliated with ASD. ASD does not endorse this library or the maintainer.
