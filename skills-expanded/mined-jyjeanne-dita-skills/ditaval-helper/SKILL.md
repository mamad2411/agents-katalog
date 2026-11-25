---
name: ditaval-helper
description: Assists with DITAVAL conditional processing files for filtering and flagging DITA content at build time. Use this skill to validate an existing DITAVAL file, generate a new DITAVAL template from a list of conditions, or understand action priority and style-conflict resolution rules. Returns structured JSON for validation or XML output for generation.
compatibility: Python 3.9+. No third-party dependencies.
---

## Overview

Two modes: **validate** an existing DITAVAL file, or **generate** a new one from conditions.

## Usage

```bash
# Validate an existing DITAVAL file
python scripts/ditaval_helper.py validate path/to/filter.ditaval

# Generate a DITAVAL template
python scripts/ditaval_helper.py generate \
  --exclude audience=internal \
  --include platform=linux \
  --flag product=enterprise:color=#0055CC \
  --revflag rev=2.1:style=underline

# Pipe a DITAVAL file for validation
cat filter.ditaval | python scripts/ditaval_helper.py validate -
```

## Validation output schema

```json
{
  "is_valid": true,
  "errors": [{ "element": "string", "rule": "string", "message": "string" }],
  "warnings": [{ "element": "string", "rule": "string", "message": "string" }]
}
```

## Rules applied

See [references/RULES.md](references/RULES.md) for the full catalogue.

| Rule | Level |
|---|---|
| Root must be `<val>` | Error |
| `<prop>` must have `att` and `action` | Error |
| `action` must be `include`, `exclude`, `flag`, or `passthrough` | Error |
| `flag` with no visual attributes and no `<startflag>`/`<endflag>` | Warning |
| Duplicate `att`+`val` combination | Error |
| `<revprop>` must have `action` | Error |
| `<style-conflict>` appears more than once | Error |
| `imageref` path does not exist relative to the DITAVAL file | Warning |

## Common edge cases

- A `<prop att="audience">` without `val` sets the **default action** for all audience values not otherwise listed
- `exclude` always wins: if any rule excludes a value, it is excluded regardless of other rules
- Multiple DITAVAL files in a build are merged; `exclude` from any file excludes the content
