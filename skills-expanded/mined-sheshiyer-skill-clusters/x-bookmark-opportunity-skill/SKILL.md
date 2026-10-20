---
name: x-bookmark-opportunity-skill
description: Convert X bookmark intake into practical implementation opportunities using Enneagram+PARA mapping and produce cadence-based daily/weekly digests for Discord (tattva-stream pulse, akashic-records action digest, kala-time scheduling, kriya-logs telemetry). Use when processing `<VAULT>/processing/x-bookmarks/` and when the user asks for actionable next steps instead of summaries.
cluster: social-media
version: 1.0.0
---

# X Bookmark Opportunity Skill

Run the script to generate an actionable digest from new bookmark wrappers.

## Execute

```bash
python3 scripts/action_digest.py
```

Optional:

```bash
python3 scripts/action_digest.py --max-do-now 5 --max-schedule 5
```

## Output

The script writes JSON to:
- `<VAULT>/processing/x-bookmarks/reports/action-digest-YYYYMMDD-HHMMSS.json`

It updates state at:
- `<VAULT>/processing/x-bookmarks/.state/action-digest-state.json`

## Routing policy

- `tattva-stream` (`1470203565401178253`): pulse only, no burst dumps
- `akashic-records` (`1470203594077634708`): daily practical digest
- `kala-time` (`1472227428272439427`): top scheduled opportunities
- `kriya-logs` (`1472217605707399220`): telemetry only

## Practical framing

Always emit implementation-oriented candidates:
- Why it matters (1 line)
- 1–3 concrete next steps
- Effort bucket (`20m`, `60m`, `2-4h`, `multi-day`)
- Lane recommendation (`vishwakarma-build` / `chitta-track` etc.)

Do not emit generic summaries.

## Taxonomy references

Use:
- `<VAULT>/_System/TAXONOMY-REFERENCE.md`
- `<VAULT>/.Codex/skills/shared/controlled-vocabulary.yaml`

If confidence is low, default to:
- Domain: `Knowledge/Research`
- Enneagram: `Type 5`
- PARA: `Resources`
