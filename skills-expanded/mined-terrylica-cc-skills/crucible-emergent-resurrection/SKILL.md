---
name: crucible-emergent-resurrection
description: a hypothesis has failed and needs archiving with resurrection conditions, when reviewing dormant ideas for possible revival, when.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Emergent Resurrection — negative-knowledge archive

> **Self-Evolving Skill**: If the failure taxonomy misses a mode, or a resurrection trigger type recurs, update the relevant section AND append to `references/evolution-log.md`. Don't defer.

Failed hypotheses are not waste. They are negative knowledge that:

1. Documents the investigation's boundaries
2. Prevents re-exploring known dead ends
3. Can come back when conditions change

This skill is the genetic-evolutionary mechanism for "**don't rule out anything we have tried, as long as it can emerge through iterative process**".

---

## Why NOT just delete failed ideas

The session accumulated 17 null campaigns. Without negative-knowledge capture, we would:

- Re-explore the same dead ends in future sessions (wasted compute)
- Lose the meta-lesson each failure taught (wrong null, wrong scaling, wrong scope)
- Be unable to detect when conditions have shifted enough to retry

Failed attempts are cheaper to preserve than to re-run.

---

## Failure-mode taxonomy

Each failed campaign fits one or more modes. Classification determines resurrection conditions.

| Failure mode              | Description                                              | Resurrection trigger                                                                            |
| ------------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `null-insignificant`      | Signal exists but below noise floor                      | Noise floor drops (longer backtest, better data, reduced cost)                                  |
| `overfit-in-sample`       | Strong IS, poor OOS                                      | Cross-validation success on a different data regime or architectural redesign                   |
| `wrong-null-applied`      | Correct signal, wrong null type broke it                 | Correct null method discovered (see Skill B §5 orthogonal cascade)                              |
| `cross-asset-failed`      | Works on one asset, breaks on others                     | Same config trial on a DIFFERENT asset passing, OR regime detector enabling per-asset selection |
| `regime-conditional`      | Full-history fails; edge concentrated in specific regime | Causal walk-forward regime classification + train/test both positive within regime + null z>3   |
| `label-leaked`            | Features/labels violated causality                       | Causality re-verified (`bars[:i]` exclusive) and retest OK                                      |
| `agent-overestimation`    | Agent's estimate > reality                               | External oracle or per-bar replay validates a scaled-down version                               |
| `grid-degenerate`         | Parameter grid too narrow                                | Widen grid, OR sensitivity analysis reveals dormant dimension                                   |
| `dormant-low-precedence`  | Valid but lower priority                                 | Higher-priority frontier cleared, revisit                                                       |
| `falsified-comprehensive` | Tested exhaustively; impossible under stated assumptions | Assumptions change (new asset class, new microstructure, regime shift)                          |

Each archived file tags one or more of these.

---

## Archive structure

```
plugins/crucible/skills/d-emergent-resurrection/references/
├── archive/
│   ├── <YYYY-MM-DD>-<slug>.md          Dormant/failed campaign record
│   └── ...
├── falsified/
│   └── <YYYY-MM-DD>-<slug>.md          Permanently falsified (highest bar for resurrection)
└── exhumation-log.jsonl                 Append-only: when ideas moved, why
```

The distinction:

- `archive/` = dormant, not dead. Awaiting the right conditions.
- `falsified/` = tested exhaustively under clear assumptions. Resurrection requires assumption change.

---

## Archive file template

Use this frontmatter structure when moving a failed idea to archive:

```yaml
---
id: "UNIQUE-ID"
title: "Short descriptive title"
status: "dormant"                       # or "falsified"
failure_mode: ["null-insignificant"]    # list; can be multiple
confidence: 0.95                         # how sure we are it's dead NOW
date_dormant: YYYY-MM-DD

verdict: |
  One-paragraph summary of what was tested and why it failed.

linked_ledger_entries:
  - "FINDING-ID-IN-EVOLUTION-JSONL"

linked_audits:
  - "findings/evolution/audits/YYYY-MM-DD-slug/verdict.md"

resurrect_if:
  - condition: "noise_floor_drops"
    trigger_metric: "trade_level_volatility"
    threshold: "< 1.2 bps (was 2.1 bps at dormancy)"
    requires: "6+ month new backtest reducing noise > 30%"

  - condition: "new_asset_regime"
    trigger_metric: "asset_correlation_cluster"
    threshold: "Jaccard(newasset_patterns, eur_patterns) > 0.65"
    requires: "Trial on new asset with fold-shuffle p < 0.05"

whats_blocked:
  - "List of specific reasons it was shelved"

next_agent_checklist:
  - [ ] If noise_floor drops > 30%: re-run config on latest data
  - [ ] Do NOT assume dead — it's 'not now, but perhaps next regime'
---

# Title

<detailed description of why it failed, what was tested, what would be needed to resurrect>
```

---

## The 3-layer exhumation process

Resurrection is deliberate. Never auto-resurrect.

**Layer 1 — Autonomous flag**: periodically (can be a cron job or session-start check), scan `archive/*` for files whose `resurrect_if` conditions might be currently met. Tag with `CANDIDATE_FOR_RESURRECTION_<date>`. This ONLY flags; it does NOT resurrect.

**Layer 2 — Agent review**: next research session or autonomous agent reviews tagged candidates. Picks ONE to trial (prevents thrashing). Runs 1-2 folds to check if signal has genuinely re-emerged. Either:

- Promotes to active campaign (`status: "active"`, new audit folder)
- Updates archive file's frontmatter: "false positive at <date>, conditions looked met but retry failed"

**Layer 3 — Human sign-off**: before deploying anything resurrected to production (or giving it resources beyond initial re-trial), human reviews exhumation report. Confirms the condition-change is real, not a data artifact.

---

## When to archive (triggers)

During a research session, move to `archive/` when:

- A serial-gate failure killed the signal (Skill B §2, Gate C — the Irrecoverable one)
- A shuffled-null test decisively rejected (z < 1 and p > 0.9)
- 20+ parameter combos all failed → the whole approach gets archived, not each combo
- Cross-asset Gate D fails → archive the "universal" interpretation; keep asset-specific as scoped-down live version (see Skill C §3)

Archive ≠ silence. Write the file; append to `exhumation-log.jsonl`:

```json
{
  "date": "YYYY-MM-DD",
  "action": "archive",
  "id": "...",
  "reason": "...",
  "from_audit": "..."
}
```

---

## When NOT to archive

- A finding survives all gates but produces modest economics — that's `live-limited-economics`, not dormant; keep active and look for ensemble partners
- A finding partially fails one gate — see Skill C §3 (scope narrows, doesn't kill)
- A method used in a campaign that gave null results — the method itself isn't archived; only the specific hypothesis
- User interest waned mid-campaign — that's not a failure mode; mark as `paused` elsewhere

---

## Population-level resurrection signals

Beyond individual-file `resurrect_if`, watch for population-level conditions:

- **Multiple failed campaigns share a failure mode** → the common cause may be addressable (e.g., all 5 used wrong null type → invent new null → resurrect all 5)
- **New method/technology emerges** → old failures under old methods may flip
- **Asset microstructure shifts** → asset-specific failures may reverse

---

## Integration with the ledger

`findings/evolution/evolution.jsonl` entries gain a `dormant_refs` field:

```json
{
  "id": "FINDING-ID",
  "status": "null",
  "dormant_refs": [
    {
      "archive_file": "plugins/crucible/skills/d-emergent-resurrection/references/archive/<slug>.md",
      "failure_mode": ["null-insignificant"],
      "resurrect_conditions": ["noise_floor_drops", "new_asset_regime"]
    }
  ]
}
```

Bidirectional: ledger → archive file, archive file → ledger.

---

## Current archive (seed state)

Session `ca9d7ffa-ef5a-41d0-94c8-56f113a132f2` produced:

- 17 null campaigns → each should have an archive file (SEEDING STATE: archive files not yet backfilled; do this when touching individual campaign verdicts)
- 1 positive finding (`NGRAM3FU-STRADDLE-001-FULL-STACK`) → remains active, NOT archived

Backfilling 17 archive entries is a future task; initial `references/archive/` is intentionally empty until each campaign's verdict is reviewed and archive-written.

---

## Post-Execution Reflection

After invoking this skill:

1. Did archiving a failed idea happen cleanly? If the file was too sparse or too detailed, update the template above.
2. Did `resurrect_if:` conditions fire (layer 1)? Were they appropriately specific, or too vague? Refine.
3. New failure mode not in the taxonomy? Add a row; log to `references/evolution-log.md`.
4. A previously-archived idea resurrected successfully? Document the exhumation in `exhumation-log.jsonl` AND note the condition pattern that worked — this is meta-knowledge.
