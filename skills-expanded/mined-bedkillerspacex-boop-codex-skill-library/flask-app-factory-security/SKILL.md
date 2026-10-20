---
name: flask-app-factory-security
description: >
  Secure Flask application factories: config separation, SECRET_KEY handling, debug
  flags, extension init order, blueprint registration, session cookies, and environment
  overlays. Use when scaffolding or reviewing owned Flask apps that use create_app()
  factories, or fixing insecure default config leaking into production.
---

# Flask App Factory Security

## Scope And Authorization

- **In scope:** Flask applications you own or are authorized to harden/review.
- **Out of scope:** attacking third-party Flask deployments without permission.
- Never enable production DEBUG; never commit real `SECRET_KEY`.
- Redact session secrets from logs.
- Pair with `code-quality-standards` and `python-style-and-typing` as needed.

## When To Use

- Apps structured with **`create_app()`** factory pattern and multiple configs.
- Reviews of `Flask(__name__)` monoliths being refactored to factories.
- Ensuring extensions (SQLAlchemy, Login, CSRF, Limiter) init safely per app context.
- Preventing test/dev config from shipping to prod.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Generic Python style | `python-style-and-typing` |
| Secrets inventory program | `secrets-management-hygiene` |
| SSRF/XSS/SQLi class testing | respective injection skills |
| Upload hardening | `file-upload-security-checklist` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Topic | Secure practice |
| --- | --- |
| Factory | `create_app(config_object)` builds isolated app instances |
| Config | Class hierarchy or env-based; prod requires strong secrets |
| SECRET_KEY | From env/KMS; rotate; used for sessions/CSRF/sign |
| DEBUG / TESTING | Never true in prod |
| Sessions | `SESSION_COOKIE_SECURE`, `HTTPONLY`, `SAMESITE` |
| Extensions | `init_app(app)`; no global state leaking across tests |

## Insecure vs secure sketches

```python
# Bad: import-time app, debug on, weak secret
app = Flask(__name__)
app.config["SECRET_KEY"] = "changeme"
app.config["DEBUG"] = True
```

```python
# Better: factory + explicit config
import os
from flask import Flask

def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    name = config_name or os.environ.get("FLASK_CONFIG", "production")
    app.config.from_object(config_by_name[name])
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY required")
    if name == "production" and app.config.get("DEBUG"):
        raise RuntimeError("DEBUG forbidden in production")

    # extensions
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from .blueprints.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
```

```python
class ProductionConfig:
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"  # or Strict
    PREFERRED_URL_SCHEME = "https"
    # SECRET_KEY set from env in create_app or here via os.environ
```

## Workflow

### 1. Confirm scope and success criteria

1. Flask/Werkzeug versions; deployment (gunicorn/uwsgi); config sources.
2. Success: factory creates prod app without DEBUG; missing SECRET_KEY fails boot; cookies flagged; tests use separate app instances.
3. Threat notes: session forgery, config injection via env, accidental `app.run(debug=True)`.

### 2. Inventory

```bash
rg -n "Flask\(|create_app|SECRET_KEY|DEBUG|init_app|register_blueprint" --glob "*.py"
```

1. List config classes and which env vars override them.
2. List extensions and whether they support `init_app`.

### 3. Baseline risks

1. Is `SECRET_KEY` defaulted in repo?
2. Can unit tests mutate global app state affecting others?
3. Is CSRF enabled on cookie session POSTs?
4. Is `JSON_SORT_KEYS` / error handlers leaking stack traces when DEBUG?

### 4. Apply factory security practices

1. **Fail fast** on missing secrets and illegal DEBUG in prod.
2. Load config only from trusted sources (env, not user uploads).
3. Register security headers middleware / Talisman carefully if used.
4. Use application factory in tests: `app = create_app("testing"); client = app.test_client()`.
5. Do not store request-mutable globals on the module-level `app`.
6. Pin `PERMANENT_SESSION_LIFETIME`; regenerate session on login.
7. Disable interactive debugger; ensure `WERKZEUG_DEBUG_PIN` not relevant in prod (DEBUG off).

```python
# wsgi.py
from myapp import create_app
app = create_app("production")
```

### 5. Verify with evidence

```bash
# Boot without SECRET_KEY should fail
env -u SECRET_KEY FLASK_CONFIG=production python -c "from myapp import create_app; create_app()"
# Expect RuntimeError

# Cookie flags (staging)
curl -sS -D - -o /dev/null "https://app.example/login" | rg -i "set-cookie"
```

1. Attempt access to `/console` or debugger paths → not available.
2. CSRF: POST without token rejected if Flask-WTF CSRF on.

### 6. Observe and harden

1. Log config name at boot (not secret values).
2. Alert on DEBUG true in prod telemetry if somehow set.
3. Rotate SECRET_KEY with planned session invalidation.

### 7. Hand off

1. Document config matrix (dev/test/prod) and required env vars.
2. Note extension init order dependencies.
3. Apply `code-quality-standards` for changes.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| App object | Factory per process/tests | Mutable global app |
| SECRET_KEY | Env/KMS required | `secret` in git |
| DEBUG | False prod fail-fast | `debug=True` forever |
| Cookies | Secure/HttpOnly/SameSite | Defaults on HTTP prod |
| Extensions | init_app | Bound only to import-time app |
| Errors | Generic 500 in prod | Stack trace to users |

## Output Checklist

- [ ] Factory entrypoints identified
- [ ] Config classes/env matrix documented
- [ ] SECRET_KEY and DEBUG controls evidenced
- [ ] Session cookie flags verified
- [ ] Extensions init_app pattern reviewed
- [ ] CSRF and auth login session fixation considerations noted
- [ ] Tests use app factory isolation
- [ ] `code-quality-standards` applied

## Rules

- Owned Flask apps only.
- Never ship DEBUG or weak secrets to production.
- Prefer factory isolation for security-relevant extensions.
- Route language style to Python skill; keep this on Flask factory/config security.
