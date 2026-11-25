---
name: strict-pydantic-config-with-suggestions
description: Forbid unknown fields on every config model and reject misspellings with a "did you mean ..." suggestion drawn from difflib.get_close_matches, while stripping whitespace from all string values automatically.
category: configuration
version: 1.0.0
version_origin: extracted
tags: [pydantic, validation, fail-fast, config]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/strict_config.py
imported_at: 2026-04-18T00:00:00Z
---

# Strict Pydantic Config Base with "Did You Mean" Suggestions

## When to use
You want every YAML/JSON config in your project to fail loudly on typos like `endpiont` instead of `endpoint`, and surface the suggestion inline so users don't have to grep docs. Inherit a single base class and you get whitespace stripping for free.

## How it works
- `model_config = ConfigDict(extra="forbid")` rejects unknown fields.
- A `model_validator(mode="before")` intercepts the raw dict, computes the unknown keys, and uses `difflib.get_close_matches` to attach a suggestion per offender. It raises a single `ValueError` with all suggestions inline — much friendlier than Pydantic's default unknown-field error.
- A `field_validator("*", mode="before")` strips whitespace from any string value globally.
- Field aliases are honored when computing the allowed-set so YAML keys match without surprises.

## Example
```python
from difflib import get_close_matches
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

class StrictConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    @field_validator("*", mode="before")
    @classmethod
    def _strip_string_values(cls, value):
        return value.strip() if isinstance(value, str) else value

    @model_validator(mode="before")
    @classmethod
    def _reject_unknown_fields(cls, data):
        if not isinstance(data, dict):
            return data
        allowed = set(cls.model_fields) | {
            f.alias for f in cls.model_fields.values()
            if f.alias and f.alias != cls._name(f)
        }
        extras = sorted(k for k in data if k not in allowed)
        if not extras:
            return data
        details = []
        for name in extras:
            suggestion = get_close_matches(name, list(allowed), n=1)
            if suggestion:
                details.append(f"'{name}' (did you mean '{suggestion[0]}'?)")
            else:
                details.append(f"'{name}'")
        raise ValueError(
            f"Unexpected field {details[0]}." if len(details) == 1
            else f"Unexpected fields {', '.join(details)}."
        )
```

## Gotchas
- Whitespace stripping affects *every* string field; if you have a field that legitimately needs leading whitespace, override the validator on that subclass.
- `extra="forbid"` cascades — every subclass gets it; opt out per-subclass if you genuinely need extras.
- The "before" model validator runs on the raw input dict, so it sees alias keys and field names side-by-side; build the allowed set from both.
