---
applyTo: '**'
---

# Instructions

## General Information

This python (3.13) repo uses the astral.sh stack along other tools:
1. `pre-commit` - local automation
2. `uv` - venv and tools management
3. `ruff` - format and lint
4. `ty` - type checking
5. `pytest` - testing
6. `typos` - spell checking
7. `yamlfmt` - yaml format and lint
8. `biomejs` - json format and lint
9. `rumdl` - markdown format and lint
10. `taplo` - general toml format and lint
11. `pyproject-fmt` - pyproject.toml format and lint
12. `tox-toml-fmt` - tox.toml format and lint
13. `claude` - for an objective AI review

## Code generation Guidelines

After any code generation or edit, first use `git add` to add all changes,
then use `pre-commit run` shell command to sync the venv, apply formatting,
run tests and to check yourself.  
When you are asked to "check" a file, you should also run `pre-commit` on it.

## Git

Commit changes with a `--signoff`.
Commit messages must follow the pattern
`<type>: <sentence>\n[<details>]\n\nAssisted-by: <name-of-code-assistant>`,
where the `<type>` is `feat` or `fix`, the `<sentence>` is no more than 60
characters and the `<details>` are optional.  
Use the `Git push` task after every successful commit on an existing branch.
