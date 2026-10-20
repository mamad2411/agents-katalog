---
name: normalize-repo
description: Standardize repository structure and conventions — setup, consistency, automation
triggers: [normalize, standardize, structure, setup, repository, consistency, automation]
---

# SKILL: Normalize Repository

## Repository Standard Structure

```
project/
├── src/                 ← application code
│   ├── main.py
│   └── services/
├── tests/               ← test code
│   ├── test_services.py
│   └── fixtures/
├── scripts/             ← utility scripts
│   ├── bootstrap.py
│   └── deploy.sh
├── docs/                ← documentation
│   ├── README.md
│   ├── API.md
│   └── ARCHITECTURE.md
├── .github/
│   ├── workflows/       ← CI/CD
│   └── copilot-instructions.md
├── docker/              ← Docker files
│   └── Dockerfile
├── .env.example         ← environment template
├── pyproject.toml       ← dependencies
├── pytest.ini           ← test config
├── Makefile             ← common commands
└── .gitignore

NEVER:
  ❌ src/test_*.py (tests go in tests/)
  ❌ test.py in root (goes in tests/)
  ❌ config.py with passwords (use .env)
  ❌ Scripts in root (use scripts/ directory)
```

## Normalization Checklist

```
Code:
  [ ] All imports absolute (from src.models import...)
  [ ] Type hints throughout
  [ ] Docstrings on public functions
  [ ] No print() statements (use logging)
  [ ] Constants UPPERCASE in config

Tests:
  [ ] tests/ directory exists
  [ ] conftest.py with shared fixtures
  [ ] Tests named test_*.py
  [ ] Each function tested

Configuration:
  [ ] .env.example with all required vars
  [ ] Config loading from environment
  [ ] No hardcoded secrets
  [ ] Separate configs per environment

Documentation:
  [ ] README with setup instructions
  [ ] API documentation
  [ ] Architecture decisions documented
  [ ] Contributing guide

Automation:
  [ ] Makefile with setup, test, deploy
  [ ] pre-commit hooks
  [ ] CI/CD pipeline
  [ ] Linting configuration
```

## Quality checks
- [ ] Directory structure matches standard
- [ ] All code in src/ (not scattered)
- [ ] All tests in tests/
- [ ] .env.example complete and up to date
- [ ] Makefile with common commands
- [ ] CI/CD configured
- [ ] Pre-commit hooks enabled
