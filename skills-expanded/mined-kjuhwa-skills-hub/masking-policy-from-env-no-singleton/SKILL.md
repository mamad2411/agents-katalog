---
name: masking-policy-from-env-no-singleton
description: Build a fresh policy object from environment variables on every investigation (no module-level singleton) so toggling env vars between runs takes effect without restarting the process.
category: configuration
version: 1.0.0
version_origin: extracted
tags: [config, env-vars, no-singleton, policy]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/masking/policy.py
imported_at: 2026-04-18T00:00:00Z
---

# Masking Policy Built Fresh per Run from Env

## When to use
Your library reads several related env vars (enabled flag + comma-list of kinds + JSON object of extras). You want each invocation to see the current values, and you want users to be able to flip behaviour from a Jupyter notebook without restarting the kernel.

## How it works
- `MaskingPolicy.from_env(env=None)` accepts an injectable env dict (default `os.environ`).
- Comma-string and list/tuple inputs are both accepted via a `field_validator(mode="before")`.
- Invalid identifier kinds are filtered out with a warning, but the model never raises — a typo in env doesn't kill the run.
- Extra regex patterns are read from a JSON env var and validated at parse time so a bad regex fails early, not at first match.

## Example
```python
class MaskingPolicy(StrictConfigModel):
    enabled: bool = False
    kinds: tuple[IdentifierKind, ...] = ALL_KINDS
    extra_patterns: dict[str, str] = Field(default_factory=dict)

    _ENV_ENABLED: ClassVar[str] = "OPENSRE_MASK_ENABLED"
    _ENV_KINDS: ClassVar[str] = "OPENSRE_MASK_KINDS"
    _ENV_EXTRA_REGEX: ClassVar[str] = "OPENSRE_MASK_EXTRA_REGEX"

    @field_validator("kinds", mode="before")
    @classmethod
    def _coerce_kinds(cls, value):
        if value is None or value == "":
            return ALL_KINDS
        if isinstance(value, str):
            parts = tuple(p.strip() for p in value.split(",") if p.strip())
            return cls._filter_valid_kinds(parts)
        # tuple/list path...

    @field_validator("extra_patterns")
    @classmethod
    def _validate_extra_patterns(cls, value):
        for label, pattern in value.items():
            try:
                re.compile(pattern)
            except re.error as exc:
                raise ValueError(f"extra_patterns[{label!r}] invalid: {exc}") from exc
        return value

    @classmethod
    def from_env(cls, env=None):
        source = env if env is not None else os.environ
        return cls.model_validate({
            "enabled": _parse_bool(source.get(cls._ENV_ENABLED, "")),
            "kinds": source.get(cls._ENV_KINDS, ""),
            "extra_patterns": _parse_json_dict(source.get(cls._ENV_EXTRA_REGEX, "")),
        })
```

## Gotchas
- Avoid `lru_cache` here. Caching defeats the whole "fresh per run" property.
- Compile regex once *per context*, not per call — see `compile_extra_patterns(policy)`.
- Always log a warning instead of raising for unknown kinds, so a future identifier kind in env doesn't break older deploys.
