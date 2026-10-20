---
description: Testing conventions and patterns
globs: ["tests/**/*.py"]
alwaysApply: false
---

# Testing Rules

## Fixture Usage
- `client` — async HTTP client with dependency overrides
- `db_session` — isolated async SQLAlchemy session (rolled back after each test)
- `make_auth_headers(user_id)` — generates JWT Bearer headers for any user
- `auth_headers` — pre-made headers for user_id=1

## Test Organization
```
tests/
├── unit/           # Fast, no external deps, mock as needed
│   ├── services/
│   └── repositories/
├── integration/    # Full stack with test DB
│   └── api/
└── e2e/            # End-to-end (Docker required)
```

## Conventions
- One test class per module: `TestUserService`, `TestAuthEndpoints`
- Test method naming: `test_<action>_<condition>` (e.g., `test_create_user_duplicate_email_raises`)
- Use factories from `tests/factories/` to create test data
- Mark tests: `@pytest.mark.unit`, `@pytest.mark.integration`
- Assert specific status codes and response shapes, not just "not 500"
