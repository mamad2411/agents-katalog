---
name: ruby-antipatterns
description: Forbidden Ruby/Rails patterns — eval with user input, YAML.load, mass assignment without permit, shell injection. Applies when editing Ruby files.
paths: ["**/*.erb","**/*.rake","**/*.rb"]
user-invocable: false
---

# Ruby anti-patterns — do not write these

Checks run automatically after each edit. Findings reference the IDs below.

## Blockers
- AP-RB-SEC-001 — Never `eval`/`send`/`constantize` with user input; use an explicit allowlist.
- AP-RB-SEC-002 — Always use `YAML.safe_load` instead of `YAML.load` on external data.
- AP-RB-SEC-004 — Use `Open3.capture2e('prog', arg1, arg2)` with separate args; never interpolate into backticks.
- AP-RB-SEC-005 — Use `where(email: email)` or `where('email = ?', email)`; never interpolate into `where`.

## Errors
- AP-RB-SEC-003 — Always use `params.require(:resource).permit(:allowed_fields)` in Rails controllers.
- AP-RB-SEC-006 — Use `SecureRandom.hex(32)` or `SecureRandom.urlsafe_base64` for all security tokens.
- AP-RB-MAINT-001 — Rescue `StandardError` at most; prefer specific exception types; log before retrying or re-raising.

Details for any ID: `reference/<ID>.md`
