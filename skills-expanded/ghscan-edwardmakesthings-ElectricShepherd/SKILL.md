---
description: File a skill definition as a drawer in the skills room and stamp es-source-type: skill (bounded, dry-run default)
agent: dreamer
subtask: false
---
File a skill procedure into the palace.

Arguments: $ARGUMENTS = `<procedure text or path to a file containing it>` — the full skill definition: goal, preconditions, numbered steps, failure modes, verification step. One skill drawer per recurring task; the content is stored verbatim and is never rewritten afterwards (refinement happens via `refined-by` edges, or a new drawer + `merged-into`).

Execution:

1. Call `file_skill` with `content` and `dry_run: true` (the default).
2. The tool resolves the project wing, picks the destination room via `get_taxonomy` (reuses an existing skill-like room before minting `skills`), runs a read-only exact-duplicate guard, and returns a bounded preview of the destination room's current drawer count.
3. Show the user the dry-run summary: resolved wing/room, whether the room was reused or minted, duplicate-guard result.
4. Only after approval, call again with `dry_run: false`.

What apply does:

- Exact-duplicate guard first: if identical content is already filed in the wing, nothing is written (`skipped-duplicate`). Re-file only when the procedure genuinely changed — then file a NEW drawer and merge old → new; never rewrite.
- Files the procedure verbatim into `<wing>/<skills room>` via `add_drawer`.
- Stamps the new drawer `es-source-type: skill` so procedural-intent retrieval boosts it. If the stamp fails, the report says so with a retry next_step — re-running is safe (identical content maps to the same deterministic drawer ID).

Useful args:

- `desc <text>` (one-line description for discoverability)
- `wing <wing>` (defaults to the project wing)
- `room <room>` (explicit destination room; default reuse-or-mint `skills`)
- `dry_run false` (apply; default true)

This tool does not touch the `es-status` axis — it stays orthogonal to `es-source-type`. A skill is authoritative on arrival, like a doc.
