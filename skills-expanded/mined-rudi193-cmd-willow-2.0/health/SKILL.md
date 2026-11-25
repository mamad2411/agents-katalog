---
name: health
description: Willow stack health check — boot/daily/weekly tiers + memory audit. Works without an active MCP session.
---

@markdownai v1.0

# /health [mode]

Modes: `boot` (default) · `daily` · `weekly` · `memory`

Scripts live at `${WILLOW_FYLGJA_ROOT:-${WILLOW_ROOT:-~/github/willow-2.0}/willow/fylgja}/skills/scripts/`.

## System checks (boot / daily / weekly)

```bash
SCRIPTS="${WILLOW_FYLGJA_ROOT:-${WILLOW_ROOT:-~/github/willow-2.0}/willow/fylgja}/skills/scripts"
python3 "$SCRIPTS/system_health.py" --check boot    # every session
python3 "$SCRIPTS/system_health.py" --check daily   # once per day
python3 "$SCRIPTS/system_health.py" --check weekly  # once per week
```

| Status   | Action                                                           |
|----------|------------------------------------------------------------------|
| HEALTHY  | No action needed                                                 |
| WARN     | Review and offer fix                                             |
| CRITICAL | Service down — fix before proceeding with memory-dependent tasks |

Cleanup actions (offer after reporting — always confirm first):
1. Merge or delete orphaned forks
2. Clean old jeles sessions (`willow jeles cleanup`)
3. Remove dead Ollama models (`ollama rm <model>`)
4. Run Postgres VACUUM ANALYZE
5. Skip — report only

## Memory audit (`/health memory`)

```bash
SCRIPTS="${WILLOW_FYLGJA_ROOT:-${WILLOW_ROOT:-~/github/willow-2.0}/willow/fylgja}/skills/scripts"
python3 "$SCRIPTS/memory_health.py" --dir ~/.claude/projects/<project>/memory --limit 50
python3 "$SCRIPTS/memory_health.py" --dir ~/.claude/projects/<project>/memory --limit 50 --qmd
```

| Bucket       | Age        | Action                                     |
|--------------|------------|--------------------------------------------|
| HOT          | < 7 days   | Healthy — no action                        |
| WARM         | 7–30 days  | Healthy — no action                        |
| STALE        | 30–90 days | Review — update or archive                 |
| DEAD         | > 90 days  | Archive — move to memory/archive/          |
| REDUNDANT    | —          | Merge — show both files, ask which to keep |
| DARK         | —          | Re-index — run `qmd update`                |
| CONTRADICTION| —          | Clarify — show conflicting phrases, ask    |

Run memory audit before every handoff and after major refactoring.

## Rules

- Postgres down = hard stop. Everything downstream is degraded.
- Boot check is safe to run frequently. Weekly check does full DB scans — expensive.
- Always confirm before any destructive action (archive, delete, reindex).
