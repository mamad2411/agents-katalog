---
name: api-yandex-oauth-run
description: 'Research Yandex OAuth token flows, exchange or refresh tokens and diagnose authorization through approved interfaces. Use for Yandex token, Metrika or refresh problems. RU: яндекс токен, metrika, refresh token.'
---

# Yandex OAuth token handling

Identify the requested resource, account, application, scopes, permitted action and current provider contract. Use the authoritative Yandex documentation for the exact API and version; an HTTP status alone does not prove its cause or the token owner's access. Protect credentials, authorization codes and token responses from command arguments, logs, chat, history and unintended processes. Never print them.

`scripts/yandex-oauth.sh` keeps secrets off every command line: `authorize-url` prints the public URL; `exchange` reads the authorization code from stdin; `refresh` and `check` read the token file named by `ENV_FILE`. Requests go from one process to fixed Yandex HTTPS hosts (no proxy, no redirect) and output carries lengths and status only. Run `exchange`, `refresh` and `check` only when the user authorized that live operation for that account and file; discovery or a failing request is not permission. Use `--dry-run` to validate configuration without network or writes. Never put a real code, token or client secret in an argument, message or log.

For resource, provider and operational boundaries, see [reference.md](reference.md). Confirm any rotation and reload requirements from the actual provider response and consuming service; preserve existing secret state and unrelated configuration.
