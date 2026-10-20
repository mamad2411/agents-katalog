# Configuration Rules — Python Examples

**Framework basis:** Python 3.11+, `pydantic-settings` (`BaseSettings`), `.env`
loading, environment variables. The rules themselves are framework-agnostic —
these examples only show one concrete stack. **Translation hints:** Django →
`settings.py` reading `os.environ` with `django-environ`; Dynaconf → layered
env/settings files. **Version-sensitive:** `pydantic-settings` is the v2 split-out
of Pydantic v1's `BaseSettings`.

## Rule 1 — No environment-varying value hardcoded
Violation:
```python
BASE = "https://rates.prod.example.com"     # breaks in dev/test
TIMEOUT = 5.0                                # buried literal
```
Correct:
```python
class RatesSettings(BaseSettings):
    base_url: HttpUrl                        # from env / .env
    timeout: float = 5.0
    model_config = SettingsConfigDict(env_prefix="RATES_")
```

## Rule 2 — Config from environment, same code everywhere
Violation:
```python
if os.environ["ENV"] == "prod":
    base = PROD_URL
else:
    base = DEV_URL                           # code branches on env name
```
Correct:
```python
# RATES_BASE_URL supplied per environment; code reads settings.base_url unconditionally
settings = RatesSettings()
```

## Rule 3 — Secrets never in versioned config
Violation:
```python
API_KEY = "sk_live_5f3a..."                  # plaintext secret, committed
```
Correct:
```python
class RatesSettings(BaseSettings):
    api_key: SecretStr                       # from env; .env.example holds a placeholder
```

## Rule 4 — Bind to a typed object
Violation:
```python
url = os.environ.get("RATES_BASE_URL")       # scattered raw reads
timeout = float(os.environ.get("RATES_TIMEOUT", "5"))
```
Correct:
```python
class RatesSettings(BaseSettings):
    base_url: HttpUrl
    timeout: float = 5.0                      # one typed surface
```

## Rule 5 — Required config validated eagerly; boot fails loudly
Violation:
```python
url = os.environ.get("RATES_BASE_URL")       # None → detonates later
client.get(f"{url}/rate")
```
Correct:
```python
settings = RatesSettings()   # missing RATES_BASE_URL → ValidationError at startup, names the field
```

## Rule 6 — Defaults are sane and safe
Violation:
```python
AUTH_DISABLED = os.environ.get("AUTH_DISABLED", "true") == "true"   # insecure default
```
Correct:
```python
class AuthSettings(BaseSettings):
    disabled: bool = False                    # security-sensitive fails closed
```

## Rule 7 — Read config at the edge; inject values inward
Violation:
```python
class RatesClient:
    def __init__(self):
        self.key = os.environ["RATES_API_KEY"]   # env read buried in a component
```
Correct:
```python
class RatesClient:
    def __init__(self, settings: RatesSettings):   # injected typed config
        self._settings = settings
```

## Rule 8 — Don't log or expose raw configuration
Violation:
```python
logger.info("config = %s", settings.model_dump())   # may include api_key
```
Correct:
```python
logger.info("rates configured", base_url=str(settings.base_url))   # SecretStr masks itself
```

## Rule 9 — Document every property
Violation:
```python
class RatesSettings(BaseSettings):
    base_url: HttpUrl                         # no hint of required/default
```
Correct:
```python
class RatesSettings(BaseSettings):
    base_url: HttpUrl = Field(description="Required. URI of the rates service.")
    timeout: float = Field(default=5.0, description="Optional. Per-call read timeout (s).")
```
