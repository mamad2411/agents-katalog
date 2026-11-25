---
name: dream
description: Run the AutoDream synthesis pipeline — tension detection + pattern synthesis over recent KB atoms
---

@markdownai v1.0

# /dream — AutoDream Synthesis

AutoDream is the Soul mechanic that synthesises patterns across recent KB atoms, detects
tensions between hypothesis/observed-tier knowledge, and records the reflection as a KB atom.

## When to run

AutoDream fires automatically when **both** conditions are met:
- 24+ hours since last dream
- 5+ Willow sessions (willow.runs rows) since last dream

Check conditions first: `dream_check(app_id)` — returns `{should_dream, hours_since_dream, sessions_since_dream}`.

## Sequence

1. **Check conditions** — call `dream_check`. If `should_dream` is false, report the reason and stop unless the user explicitly asks to run anyway.

2. **Run the pipeline** — call `dream_run(app_id)`. Optionally pass `force=True` to skip the 24h/5-session gate.

   > **Known issue #11:** `dream_run` may time out on the synthesis step. If it does, run `tension_scan` standalone (step below) and call `infer_chat` directly with mistral:7b for the synthesis narrative.

   The pipeline:
   - Scans the 20 most recent valid KB atoms
   - Runs lightweight tension detection (10 atoms × top-3 semantic neighbors via mistral:7b)
   - Generates a 3-4 sentence synthesis via mistral:7b: patterns, connections, gaps
   - Writes a KB atom with `category='dream'`, containing `synthesis`, `tensions_found`, `tension_pairs`, `atoms_scanned`
   - Updates SOIL `{agent}/dream/state`: `last_dream_at`, `last_dream_atom`

3. **Review findings** — read the dream atom via `kb_get`. If tensions were found, consider:
   - Are the conflicting atoms actually contradictory? If so, retire the weaker one via `kb_ingest` (framework retirement will trigger automatically)
   - Are the atoms redundant? Retire the older one
   - Any synthesis insights worth acting on? Ingest them as KB atoms

4. **Surface to user** — share the synthesis and any tensions that need human judgment.

## Standalone tension scan

To scan for tensions without running the full dream pipeline:

```
tension_scan(app_id, write_kb=False)   # dry run — returns pairs only
tension_scan(app_id, write_kb=True)    # saves findings as KB atom (category='tension')
```

## Dream state in SOIL

Dream state is stored at SOIL key `{agent}/dream/state`:
```json
{
  "last_dream_at": "2026-05-18T...",
  "locked": false,
  "last_dream_atom": "XXXXXXXX"
}
```

Sessions since last dream are counted from `willow.runs` rows — no manual counter needed.

## Rules

- Never force-run if already locked (`dream_state.locked == true`) — another session is mid-dream.
- Dream atoms are category='dream', not category='handoff' — don't confuse them.
- Tensions surfaced by dream are suggestions, not automatic retirements — use judgment before retiring.
- The synthesis is from a local model (mistral:7b) — treat it as a thinking aid, not ground truth.
