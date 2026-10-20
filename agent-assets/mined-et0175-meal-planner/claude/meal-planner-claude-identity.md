# Identity Service — Claude context

## Purpose
FastAPI microservice for authentication in Meal Forge. Owns account lifecycle
(register, sign-in, sign-out), password reset, and the `/auth/session` endpoint
that other services call to validate Bearer tokens.

## Key architecture decisions
- **Role**: always hardcoded `RoleEnum.user` at registration — never caller-controlled (security)
- **bcrypt**: direct usage, `_BCRYPT_ROUNDS = 10`; `passlib` is NOT in requirements
- **Rate limiting**: 10 failures → 1-hour lockout (configurable via env, ADR-0006)
- **Reset tokens**: 256-bit urlsafe, single-use, 1 h TTL, atomic TOCTOU-safe mark (ADR-0005)
- **Session invalidation**: all sessions for an account are invalidated on password reset
- **sign_in() return**: returns `tuple[Session, RoleEnum]` — no second DB round-trip in the router
- **Cross-service auth**: other services call `GET /auth/session` (HTTP); they do NOT import
  from this service. See `backend/shared/auth_middleware.py` for the documented pattern.

## File map
| Path | Role |
|------|------|
| `db/models.py` | `Account`, `Session`, `ResetToken` — SQLAlchemy 2.0 mapped classes |
| `db/engine.py` | `AsyncEngine`, `get_db` dependency, `DATABASE_URL` env fallback |
| `db/migrations/env.py` | Alembic async runner — **import new models into `target_metadata` here** |
| `db/migrations/versions/` | Alembic migrations |
| `account/service.py` | `register_account`, `sign_in` → `(Session, RoleEnum)`, `sign_out`, `LockoutError` |
| `account/schemas.py` | `RegisterRequest` (no `role` field), `SignInResponse`, etc. |
| `account/router.py` | POST `/auth/register`, `/auth/sign-in`, `/auth/sign-out` |
| `reset/service.py` | `request_password_reset`, `confirm_password_reset` |
| `reset/router.py` | POST `/auth/reset-request`, `/auth/reset-confirm` |
| `session/service.py` | `validate_token` — queries DB, returns `Account` or `None` |
| `session/router.py` | GET `/auth/session` — uses `verify_token` from `auth_guard.py` |
| `auth_guard.py` | `verify_token` FastAPI dep — **identity-internal only**, not importable by other services |
| `email_adapter/sender.py` | Stub email sender; set `EMAIL_BACKEND=stdout` for dev |

## Adding a migration
1. Edit `db/models.py`
2. In `db/migrations/env.py` ensure the new model class is imported into `target_metadata`
3. `alembic revision --autogenerate -m "describe the change"`
4. Review the generated file in `db/migrations/versions/`
5. `alembic upgrade head`

## Running tests
```bash
cd backend/identity
python3 -m pytest tests/ -v
# Uses in-memory SQLite (aiosqlite) — no Postgres required
```

## Environment variables
| Variable | Default | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./identity.db` | Postgres in prod: `postgresql+asyncpg://...` |
| `RATE_LIMIT_MAX_ATTEMPTS` | `10` | Failed attempts before lockout |
| `RATE_LIMIT_LOCKOUT_MINUTES` | `60` | Lockout duration in minutes |
| `RESET_TOKEN_EXPIRY_MINUTES` | `60` | Password-reset token TTL |
| `EMAIL_BACKEND` | `stdout` | `stdout` prints reset links to console |
