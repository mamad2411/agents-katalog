# Agent Instructions

This repository contains the portable `Mouse Trail Masking Reveal` Agent Skills package.

## Canonical Skills

- `skills/image-layer-alignment-validator`
- `skills/cursor-reveal-hero`

Use the canonical skill folders as the source of truth. Provider adapter folders should document installation paths and invocation style, not duplicate the skill contents.

## Editing Rules

- Keep skills provider-neutral.
- Do not add credentials, API keys, tokens, or local absolute paths.
- Keep image/video media attribution in `docs/media-and-attribution.md`.
- Run `bash scripts/validate-package.sh` and `bash scripts/sanitize-check.sh` before release.
