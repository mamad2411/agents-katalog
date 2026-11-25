---
name: track-qa
description: Manual QA tracking — things tests can't verify. Use when asked to "create a QA list", "set up QA for this project", "what should I QA", "track manual QA", "audit the QA list", or "start manual QA".
license: MIT
argument-hint: "[generate|update|audit|migrate|resume]"
metadata:
  author: Antonin Januska
  version: "1.2.1"
---

# Track QA

Maintain `QA.md` in the project root — the manual checklist of things a human must exercise (visual rendering, multi-step flows, race conditions, real integrations) before a release is ready. **Core principle:** tests prove correctness; QA proves shippability. The `cc-dash/qa@1` schema lets dashboards ingest the file into a portfolio queue with approve/fail/skip workflows. Don't duplicate test coverage — if a unit/integration test can verify it, write the test instead.

## Modes

| Mode | Command | Essence |
|------|---------|---------|
| **Generate** | `/track-qa` or `generate` | Scan for QA-worthy surfaces, ask 4 discovery questions (incl. the Setup command), write QA.md after the user confirms |
| **Update** | `/track-qa update` | Read current file, ask what changed, apply after confirmation (new IDs for new items) |
| **Audit** | `/track-qa audit` | Re-evaluate each item against current code; flag stale/obsolete/missing checks |
| **Migrate** | `/track-qa migrate` | Convert ad-hoc QA notes (CLAUDE.md, README, scratch, QA_BACKLOG.md) into a compliant QA.md |
| **Resume** | `/track-qa resume` | Report pending/passed/failed counts, surface the next pending item |

Full per-mode procedures (discovery questions, audit signals, migrate steps): **[reference/MODES.md](./reference/MODES.md)**.

## QA.md format

```markdown
---
schema: cc-dash/qa@1
project: project-name-here
last_updated: YYYY-MM-DDTHH:MM:SS-TZ
---

# Manual QA — project-name-here

## Setup

Run: `cd project-name && npm run dev`
(Free-form — multiple commands, env vars, prerequisites all welcome.)

## Checklist

- <!-- id:q_XXXXX status:pending --> One observable behavior, stated as a verifiable claim.
- <!-- id:q_XXXXX status:passed at:YYYY-MM-DDTHH:MM:SS-TZ --> An item that was verified.
- <!-- id:q_XXXXX status:failed at:YYYY-MM-DDTHH:MM:SS-TZ ref:r_xxxxx --> An item that failed.
  > **Note (YYYY-MM-DD):** What was wrong. Filed as r_xxxxx in ROADMAP.md.
- <!-- id:q_XXXXX status:needs-decision at:... --> Blocked on a design conversation.
- <!-- id:q_XXXXX status:skipped at:... --> Intentionally bypassed (e.g., env-dependent).
```

**Format rules** (cc-dash schema is dashboard-parsed — don't omit the markers):

- Frontmatter requires `schema`, `project`, `last_updated`.
- Every item: `q_` + 5 random `[a-z0-9]` (**permanent**) and a status: `pending | passed | failed | needs-decision | skipped`.
- Non-pending items record `at:` (ISO timestamp); failed items record `ref:r_xxxxx` (the roadmap issue filed).
- Notes are blockquotes immediately after the item (`  > Note text`).
- Two parsed sections only: `## Setup` (free-form) and `## Checklist`. Other sections round-trip but aren't interpreted.

## What makes a good QA item

- **One observable behavior** — "settings page persists changes across reload", not "everything in settings works".
- **Verifiable in <2 minutes** — split anything longer.
- **Phrased as a claim** — "First major upgrade reachable in 10-15 min of play" beats "playtest".
- **Specific to this project** — "test all features" helps no one.

## Rules

- **User drives the list** — never add items without confirmation.
- **One observable behavior per item** — composite items hide failures.
- **QA.md is the source of truth.** Failed items need a note — a "failed" without context is unactionable.
- **The Setup command must work** — verify it before the first write.
- **Audit regularly** — QA lists drift. Healthy size is 5-30 items; most reviewed within 30 days.

## Example

✅ **Good:** `<!-- id:q_a1b2c status:pending --> Save a session, reload the page, confirm gold/inventory/equipped items all restore.` — one observable behavior, under a minute, unambiguous pass/fail, specific to the domain.

❌ **Bad:** `<!-- id:q_a1b2c status:pending --> Test save/load.` — test what, in what state, with what expected outcome? Two QAers check different things.

Full ✅/❌ walkthroughs for every mode: **[reference/EXAMPLES.md](./reference/EXAMPLES.md)**.

## Integration

- **track-roadmap** — failed QA items file roadmap issues (a "QA Issues" category); after fixing, mark the roadmap item done and reset the QA item to pending.
- **track-session** — drive a focused QA pass over many items at once; reference QA item IDs in the session plan.
- **`cc-dash/qa@1` dashboards / MCP** — render a portfolio queue, inline approve/fail/skip, focus mode; expose tools like `list_qa_pending`, `approve_qa_item`, `fail_qa_item`.

```
generate → write QA.md   ·   migrate → convert ad-hoc notes
resume   → next item     ·   audit   → relevance review   ·   update → add as features ship
```

## Troubleshooting

- **Items don't appear on a dashboard after writing QA.md** — verify `schema: cc-dash/qa@1` is exact, the file lives in the project root, and each item matches the `- <!-- id:q_xxxxx status:... --> Description` shape (malformed items are silently skipped by the parser).
- **A failed item stays failed after the linked roadmap fix ships** — the failed→pending reset is intentionally one-way; re-verify manually with `/track-qa update`, don't assume the fix worked.
- **Migrate mode chokes on an unfamiliar file layout** — it expects ad-hoc per-repo notes or `### project-name` headings; other layouts need manual splitting first.

Extended edge cases (ID collisions, audit staleness tuning, needs-decision items piling up, dangling roadmap refs): **[reference/TROUBLESHOOTING.md](./reference/TROUBLESHOOTING.md)**.
