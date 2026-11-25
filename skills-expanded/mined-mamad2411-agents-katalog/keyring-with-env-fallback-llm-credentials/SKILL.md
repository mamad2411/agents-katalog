---
name: keyring-with-env-fallback-llm-credentials
description: Resolve API keys from environment variables first, then fall back to the system keychain (keyring), with a kill-switch env var to disable keyring entirely for CI and Docker builds.
category: configuration
version: 1.0.0
version_origin: extracted
tags: [credentials, keyring, security, llm, api-keys]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/llm_credentials.py
imported_at: 2026-04-18T00:00:00Z
---

# Keyring + Env-Var Fallback for LLM Credentials

## When to use
You want CLI users to store API keys in the OS keychain (no `.env` lying around) but still respect `ANTHROPIC_API_KEY` if it's exported in the shell, and gracefully degrade in CI/containers where keyring isn't available.

## How it works
- `resolve_llm_api_key(env_var)` checks env first; if empty, it tries `keyring.get_password(SERVICE, env_var)`.
- A single env flag `OPENSRE_DISABLE_KEYRING=1` (compared against `{1,true,yes,on}`) skips the keyring path entirely — required for containers where dbus / Secret Service isn't running.
- All keyring calls are wrapped in `try/except keyring.errors.KeyringError` and return `""` on failure, so a missing keychain never crashes the app.
- `save_llm_api_key(env, "")` deletes; raising `RuntimeError` if keyring is disabled but the user requested save.

## Example
```python
import keyring, keyring.errors, os
from typing import Final

_KEYRING_SERVICE: Final = "myapp.llm"
_DISABLED_VALUES: Final = frozenset({"1", "true", "yes", "on"})

def _keyring_is_disabled() -> bool:
    return os.getenv("MYAPP_DISABLE_KEYRING", "").strip().lower() in _DISABLED_VALUES

def resolve_llm_api_key(env_var: str) -> str:
    env_value = os.getenv(env_var, "").strip()
    if env_value:
        return env_value
    if _keyring_is_disabled():
        return ""
    try:
        return (keyring.get_password(_KEYRING_SERVICE, env_var) or "").strip()
    except keyring.errors.KeyringError:
        return ""

def save_llm_api_key(env_var: str, value: str) -> None:
    normalized = value.strip()
    if not normalized:
        delete_llm_api_key(env_var); return
    if _keyring_is_disabled():
        raise RuntimeError(
            f"Secure local credential storage is disabled. Set {env_var} in your shell instead."
        )
    try:
        keyring.set_password(_KEYRING_SERVICE, env_var, normalized)
    except keyring.errors.KeyringError as exc:
        raise RuntimeError("Secure local credential storage is unavailable.") from exc
```

## Gotchas
- Always strip whitespace — copy/paste from a browser often adds trailing newlines that look invisible in terminals.
- `keyring` raises a wide variety of platform-specific exceptions; catching only the documented base class (`KeyringError`) keeps cross-platform behavior consistent.
- The single SERVICE name (`myapp.llm`) namespaces keys so users can host multiple apps without collisions; pair with the env-var name as the "username" entry.
- Provide an explicit `_DISABLED_VALUES` frozenset rather than `value.lower() in ("1","true",...)` so the truthy check is consistent with other env-var conventions in your codebase.
