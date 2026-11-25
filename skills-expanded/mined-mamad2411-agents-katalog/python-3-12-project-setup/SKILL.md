---
name: python-3-12-project-setup
description: Helps agents create, inspect, or normalize Python 3.12 project structure, virtual environments, packaging metadata, and baseline quality tooling.
---
# Python 3.12 Project Setup

Use this skill when creating a new Python 3.12 project, modernizing an existing project, validating `pyproject.toml`, or preparing a repository for tests, linting, formatting, and packaging.

## Operating Principles

- Verify the active interpreter is Python 3.12 before changing runtime-sensitive files.
- Prefer `pyproject.toml` as the central configuration file.
- Respect the existing dependency manager. Do not migrate tools without explicit approval.
- Keep framework, database, cloud, container, and CI choices out of the base language setup unless they already exist.
- Separate application runtime dependencies from development dependencies.
- Prefer reproducible environments and explicit commands.

## Use the Helper Script

Before relying on a local interpreter, run the script with `--help`:

```bash
.agents/plugins/python-3-12/skills/python-3-12-project-setup/scripts/verify-python-3-12.sh --help
````

Then run it from the repository root:

```bash
.agents/plugins/python-3-12/skills/python-3-12-project-setup/scripts/verify-python-3-12.sh
```

## Workflow

Use `workflows/project-bootstrap-workflow.md` when starting a project or normalizing an incomplete Python 3.12 setup.

## Project Structure Guidance

For a package or library, prefer:

```text
project-root/
├── pyproject.toml
├── README.md
├── src/
│   └── package_name/
│       └── __init__.py
└── tests/
    └── test_package_name.py
```

For an application, prefer:

```text
project-root/
├── pyproject.toml
├── README.md
├── app/
│   └── __init__.py
└── tests/
```

Do not force `src/` layout if the project already has a consistent structure and migration is not part of the task.

## `pyproject.toml` Guidance

Use `resources/pyproject-template.md` as a reference. Adapt it to the existing project and selected tools.

Recommended baseline categories:

* Build system metadata.
* Project metadata.
* Python version requirement.
* Test configuration.
* Lint and format configuration, if the project uses those tools.
* Type-check configuration, if the project uses type checking.

## Completion Checklist

* Python 3.12 interpreter verified.
* Virtual environment guidance provided or existing environment respected.
* Packaging metadata is consistent.
* Test command is documented.
* Lint, format, and type-check commands are documented when tools exist.
* No framework-specific assumptions were introduced.