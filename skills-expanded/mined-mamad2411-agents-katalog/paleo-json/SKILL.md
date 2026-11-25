---
name: paleo-json
description: 'Use when user says "compact json", "minify output", "tight structured", or the agent must emit JSON / structured data. Strip insignificant whitespace, collapse long arrays, shorten keys where safe, keep it parseable. Cuts tokens on structured payloads. Off: "pretty print" / "human-readable".'
version: 2.4.1
license: MIT
metadata:
  hermes:
    tags: [tokens, json, structured, compression, minify]
    related_skills: [paleo]
---

# paleo-json
Compact structured output. JSON / YAML / tables → minimal tokens, still valid.

## Rules
- Minify: remove whitespace between tokens (valid JSON stays parseable).
- Collapse arrays of repeated shapes into a count + 1 example when the consumer allows.
- Keep keys verbatim unless a documented short alias exists — never invent keys.
- Preserve: values, types, order where it matters, escaping.
- YAML: drop comments, shorten, keep indentation minimal but valid.
- Numbers/booleans/null: never reformat in ways that change type.

## Levels
- `lite`: minify whitespace only (safest).
- `full` (default): minify + collapse repetitive array tails.
- `ultra`: minify + alias keys per a provided map.

## Switch
- `paleo-json` / `compact json` / `minify` on. `pretty print` off.

## Gotchas
- Always return valid, parseable output — a broken payload costs more than the tokens saved.
- Don't alias keys unless the consumer expects them; default = keep keys.
- Streaming/chunked JSON: minify only after the full object is known.
