---
name: smoke-test
description: Run post-restart smoke tests for the local GStack/GBrain Codex port and repair obvious setup issues.
---

# Smoke Test

Use this skill after restart, install, or upgrade to verify the local skillpack still works.

## Workflow

1. Run `python3 scripts/validate_repo.py`.
2. Run `python3 -m unittest discover -s tests`.
3. Run `python3 scripts/brain_doctor.py`.
4. Check key local skill symlinks.
5. Run a small `query` or `brain_search.py` check if brain search is in scope.
6. Report results and fix only low-risk setup issues.

## Guardrails

- Do not modify user brain content during smoke tests.
- Do not hide failing checks.
- Do not start long-running services unless the user asked.
