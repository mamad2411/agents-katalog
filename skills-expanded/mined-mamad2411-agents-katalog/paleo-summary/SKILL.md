---
name: paleo-summary
description: 'Use when user says "summarize output", "condense this", "tldr", or a tool result / log / file dump / long stdout is large. Reduce long content (tool output, logs, diffs, docs) to a concise intisari with key fields preserved. Saves context tokens on bulky payloads. Off: "full output" / "no summary".'
version: 2.4.1
license: MIT
metadata:
  hermes:
    tags: [tokens, summary, compression, logs, tools]
    related_skills: [paleo, paleo-converse]
---

# paleo-summary
Condense bulky content. Tool results, logs, diffs, dumps → tight intisari.

## Rules
- Lead with the answer/result, then supporting detail.
- Preserve: status codes, error messages, IDs, paths, numbers, key fields.
- Drop: stack traces beyond the root-cause line, repeated rows, boilerplate banners.
- Logs: keep first error + last N lines + counts (e.g. "12 WARN, 3 ERROR").
- Diffs: summarize file set + net change; show only consequential hunks.
- Tables/lists: keep header + outliers, summarize the rest.

## Levels
- `lite`: trim noise, keep structure.
- `full` (default): intisari + preserved key fields.
- `ultra`: one-line result + the single most important detail.

## Switch
- `paleo-summary` / `tldr` / `condense this` on. `full output` off.

## Gotchas
- Never drop the actual error string — that's the diagnosis.
- If the content is the deliverable (a generated file), don't summarize it; deliver as-is.
- Security/credential output: summarize counts, never echo secrets.
