---
name: "kong-config-validation"
description: "Validate Kong declarative config in build/validation: deck gateway validate, kong config parse, schema/lint, diff against target. Use during build/validation for a Kong gateway."
version: 1
created: "2026-06-27"
updated: "2026-06-27"
---

# Kong Config Validation

## Commands (run in build/validation)
- `deck gateway validate kong.yaml`  (or `deck file validate`) — schema + plugin config validation, no running gateway needed.
- `deck file lint kong.yaml ruleset.yaml` — style/policy lint where a ruleset exists.
- `kong config parse kong.yaml` — alternative parse via Kong CLI (or dockerized `kong/kong`).
- `deck gateway diff` — preview against a running gateway (optional, needs connectivity).

## Gate
- Validate passes; every service has a reachable `url`/upstream; every route has a path; required plugins present; no inline secrets; YAML lints clean.
- Treat validation failure as a build failure; fix config, re-validate. No deploy on failed validate.
