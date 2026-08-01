# Contributing to biz.dfch.AsdSte100Nlp

Thank you for your interest in contributing to **biz.dfch.AsdSte100Nlp**!  
This document describes how to propose changes, report bugs, and submit patches.

The project is licensed under the **Affero GNU General Public License v3.0 (AGPLv3)**.  
By contributing, you agree that your contributions will be licensed under the
same license as the project.

To contribute, clone the repository, create a branch, develop your changes and 
then create a pull request.

---

## 1. Code of Conduct

Please be respectful and constructive in all interactions.

This project has a `CODE_OF_CONDUCT.md`, you must follow it.

---

## 2. How to Ask Questions and Report Bugs

- **Bug reports**: Open an issue in the GitHub issue tracker:
  - URL: `https://github.com/dfch/biz.dfch.AsdSte100Nlp/issues`
  - Include:
    - Steps to reproduce
    - Expected behavior
    - Actual behavior
    - Environment details (OS, Python version, biz-dfch-asdste100nlp version)
    - Relevant logs, stack traces, or screenshots where appropriate

- **Feature requests / ideas**: Also use the issue tracker, marking them as
  feature requests or enhancements.

Before opening a new issue, please **search existing issues** to avoid duplicates.

---

## 3. Development Setup

### 3.1. Prerequisites

- Python **3.11** and Python **3.12** and Python **3.13**
- `git`
- Recommended: [`uv`](https://docs.astral.sh/uv/)

### 3.2. Clone and create a virtual environment

```bash
git clone https://github.com/dfch/biz.dfch.AsdSte100Nlp.git
cd biz.dfch.AsdSte100Nlp

uv sync --extra dev
```

Or, without `uv`:

```bash
python3.13 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate[.bat|.ps1]
pip install -e ".[dev]"
```

### 3.3. Run the checks locally

```bash
uv run --frozen ruff format --check
uv run --frozen ruff check
uv run --frozen pylint $(git ls-files '*.py') || true
uv run --frozen python -m unittest discover -v -s tests -t . -p "test_*.py"
```

---

## 4. Submitting Changes

- Keep pull requests focused on a single change.
- Add or update tests for any behavior change.
- Make sure the checks in section 3.3 pass before opening a pull request.
- Follow [Conventional Commits](https://www.conventionalcommits.org/) for
  commit messages (e.g. `fix: ...`, `feat: ...`, `docs: ...`).
