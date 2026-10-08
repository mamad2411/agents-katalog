---
category: development
description: "Manage Python dependency and packages — virtualenv, pip install, requirements.txt, conflict check (also load: docker, pyprep, shell_scripting, quick-setup, security-audit, signal-cli, swe_bench, tau_testsuite)"
keywords: dependency management, virtualenv, pip install, requirements.txt, package management, python dependencies, pip conflicts, outdated packages
name: dependency_management
---

# Dependency Management

## When
"install package" | "pip install" | "venv setup" | "requirements" | "missing import" | "virtualenv" | "packages" | "install" | "setup" | "configure"

## Tau Project
```bash
cd $HOME/tau
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install ruff black mypy graphifyy  # Tau dev tools
```

## Rules
- NEVER global pip install — use venv
- `pip check` after install — verify conflicts
- `pip list --outdated` — audit regularly

## Helper
```bash
python3 skills/dependency_management/deps_check.py  # dependency_management helper
```

## Related Skills
- `project-onboard` — discover project dependencies
- `python_best_practices` — linting/formatting installed tools
- `graphify` — knowledge graph analysis
- `security-audit` — Security checks
- `tau_testsuite` — test dependencies
- `docker` — docker skill
- `signal-cli` — signal-cli daemon dependencies
- `swe_bench` — benchmark environment setup
- `quick-setup` — project initialization
- `security-audit` — Audit dependencies for conflicts and vulnerabilities; scan secrets
