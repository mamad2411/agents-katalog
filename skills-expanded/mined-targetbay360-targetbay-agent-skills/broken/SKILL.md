---
name: Broken Skill
display_name: Broken Skill
description: too short
license: WTFPL
metadata:
  targetbay.version: 1.0
  targetbay.category: magic
  targetbay.requires: get_customer_360
  targetbay.risk_level: whenever
  targetbay.execution_mode: just_do_it
---

# Broken Skill

This fixture exists so that `tests/validate.py` proves it actually rejects bad skills.

Every item below is wrong on purpose, and the validator must report them:

- `display_name` is a top-level key, which the Agent Skills specification does not allow
- `name` is not lowercase-hyphenated and does not match the directory name
- `description` is under the minimum length and is not in trigger form
- `license` is not the package constant
- `targetbay.display_name` and `targetbay.status` are missing
- `targetbay.version` is not semver
- `targetbay.category`, `targetbay.risk_level` and `targetbay.execution_mode` are not in their enums
- `targetbay.requires` names a tool rather than a `email_sms.*` capability
- all thirteen required sections are missing

## Purpose

Only one section is present, and the rest are absent.
