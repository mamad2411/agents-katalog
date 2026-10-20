# AI Service Test Instructions

## Commands

Run from `ai-service/`:

```sh
python -m pytest
python -m pytest tests/test_health.py
python -m pytest tests/test_consents.py
```

## Rules

- Keep tests focused on externally visible behavior and domain contracts.
- Cover consent and privacy-sensitive behavior conservatively.
- Prefer clear test names that describe the expected behavior.
- Add regression tests when fixing bugs in API routes, schemas, or domain services.
- If a test fails, fix the root cause and rerun the smallest failing test before broader checks.
