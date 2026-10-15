---
name: skill-localization-packager
description: >-
  Scaffold for packaging localized skill variants (planned).
  Use when designing i18n skill bundles. NOT for live catalog edits.
user-invocable: false
license: MIT
metadata:
  author: wyattowalsh
  version: "0.1.0"
  internal: true
---

# Skill Localization Packager

Later-tier scaffold for localized skill bundle packaging.

**Scope:** Design placeholder only. Does not translate content or publish catalog rows.

## Planned Workflow

1. Identify base skill under `skills/<name>/`.
2. Collect locale overlays (TBD directory convention).
3. Emit portable ZIP output with locale metadata through the repo packaging command.

Pair with `i18n-localization` for translation workflow until packaging ships.

## Validation Contract

```bash
uv run python skills/skill-localization-packager/scripts/check.py
```

## Critical Rules

1. Keep portable `name` field stable across locales.
2. Do not hand-edit generated catalog MDX for localized variants.
3. Route translation quality review to i18n-localization.
