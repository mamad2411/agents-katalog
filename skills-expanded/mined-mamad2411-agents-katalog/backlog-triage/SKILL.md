---
name: backlog-triage
argument-hint: "[collect|relate|stale|report|apply] [options]"
description: Interactive backlog grooming for open GitHub Issues. Classifies, relates, flags stale/obsolete, and proposes priorities — produces a markdown triage report you review before applying. Advisory by default; mutations require explicit --apply. Use for backlog review, issue grooming, stale cleanup, priority re-ranking, 백로그 정리, 이슈 검토, 트리아지, 정리.
compatibility: Requires gh CLI and git. Works on Claude Code and Codex.
metadata:
  related-skills: "dev-backlog, relay, relay-plan"
---

# Backlog Triage

Open-issue grooming as a two-phase loop:

```
Phase 1 — Report (advisory)          Phase 2 — Apply (explicit)
  collect → relate → stale              review report → --apply
      ↓                                       ↓
  single markdown report                gh mutations via anchors
```

Sibling skill to dev-backlog, not a replacement. dev-backlog is the execution hub (sprints, progress, milestones). backlog-triage is advisory: it inspects the open issue set and proposes changes. You decide; it applies only what you've approved.

---

## Two-Phase Model

### Phase 1 — Report (default, no mutations)

1. **Collect** open issues → snapshot JSON (one `gh` fetch per run)
2. **Analyze** — classification, relationships, stale/obsolete signals
3. **Render** — one markdown report with anchored proposals

Every script in this phase is read-only. Running any number of times is safe. The snapshot is the canonical artifact; all downstream analysis consumes it via `--snapshot PATH` (no re-fetch).

### Phase 2 — Apply (opt-in, explicit)

Humans review the report and mark accepted proposals (flip `[ ]` → `[x]`). Then:

```bash
# Run from the target project root; scripts live under ${CLAUDE_SKILL_DIR}/scripts/.
node "${CLAUDE_SKILL_DIR}/scripts/triage-apply.js" backlog/triage/YYYY-MM-DD-report.md               # dry-run
node "${CLAUDE_SKILL_DIR}/scripts/triage-apply.js" backlog/triage/YYYY-MM-DD-report.md --apply       # with confirmation
node "${CLAUDE_SKILL_DIR}/scripts/triage-apply.js" backlog/triage/YYYY-MM-DD-report.md --apply --yes # CI-safe

# Live integration coverage (opt-in only; disposable sandbox repo + write token required)
GH_TOKEN="$(gh auth token)" TRIAGE_APPLY_INTEGRATION=1 \
  node --test "${CLAUDE_SKILL_DIR}/scripts/triage-apply.integration.test.js"
```

Default is **dry-run**. `--apply` requires confirmation unless `--yes`. Idempotent: re-running after a partial apply emits `already-applied` log entries for actions already executed.
The integration test is intentionally separate from the default `node --test` path. It mutates the dedicated sandbox repo `sungjunlee/triage-apply-sandbox`, so it only runs when `TRIAGE_APPLY_INTEGRATION=1` and `GH_TOKEN` are both present.

---

## Directory Layout

```
backlog/
├── triage/
│   ├── .cache/                       # Snapshots (downstream scripts read from here)
│   │   └── 2026-04-18T01-30-00Z.json
│   ├── 2026-04-18-report.md          # Triage report (human entry point)
│   └── 2026-04-18-apply.log          # JSONL audit trail of apply run
└── triage-config.yml                 # Thresholds, theme keywords, weights
```

The triage report is a **derived artifact**. GitHub Issues remain the source of truth. Regenerating from the snapshot must reproduce the same proposals.

---

## Anchor-Comment Apply Contract

Every actionable proposal in the report carries a stable anchor comment paired with a visible checkbox:

```markdown
<!-- triage:close #42 reason="merged PR #87 already exists" -->
- [ ] close #42 — merged PR #87 already exists
```

- The **anchor comment** is the machine contract.
- The **checkbox** is the human confirmation surface.
- An action is accepted when **both** the anchor exists AND its paired checkbox is `[x]`.

This mirrors dev-backlog's `<!-- AC:BEGIN --><!-- AC:END -->` convention and survives markdown reformatting, so a human editing the report cannot silently break the parse.

See `references/apply.md` for the full anchor grammar, parse rules, and audit-log schema.

---

## Report Shape

```markdown
---
generated: 2026-04-18
repo: owner/name
snapshot: backlog/triage/.cache/2026-04-18T01-30-00Z.json
open_issues: 12
---

# Backlog Triage — 2026-04-18

## Classification
By theme / label / age — grouped tables.

## Relationships
Edges list (mentions, blocks, depends-on, duplicate candidates).

## Obsolete Candidates
anchor + checkbox + evidence per item.

## Priority Proposals
anchor + checkbox + rationale per item.

## Milestone Suggestions
Unplanned issues grouped into candidate next sprints.

## Apply Checklist
Consolidated list of every anchored action for scan-and-check review. The apply step parses
the whole report and dedupes by `(verb, issueNumber, normalizedArgs)` — this section and the
source sections above both count as acceptance surfaces (see `references/apply.md`).
```

---

## Relationship to dev-backlog

| Concern | Owner |
|---------|-------|
| Sprint files, execution plan, Running Context | dev-backlog |
| Milestone lifecycle, monthly progress issue | dev-backlog |
| AC checkboxes inside issue bodies (`AC:BEGIN`/`END`) | dev-backlog |
| Open-issue classification, relationships, stale flags | backlog-triage |
| Priority / milestone **proposals** | backlog-triage (report) |
| Priority / milestone **mutations** | backlog-triage (`--apply`) |
| Post-triage sprint planning | dev-backlog (reads report, edits sprint file) |

Recommended cadence: run backlog-triage weekly or bi-weekly. Feed the report's Milestone Suggestions into the next dev-backlog sprint.

---

## Process

**Collect → Analyze → Report.** One `gh` fetch, one snapshot, downstream scripts consume it via `--snapshot`. Re-fetching in each script is a bug — it creates drift across signals.

**Review the report.** Read each proposal. Check the ones you accept (flip `[ ]` → `[x]`). Leave rejected ones unchecked. Do not delete anchor comments; unchecked anchors are ignored by apply.

**Apply (opt-in).** Run dry-run first, confirm the pseudo-`gh` commands match intent, then `--apply`. The apply log is append-only JSONL; keep it alongside the report in git for audit.

**Re-run safely.** A second `--apply` on the same report is idempotent — already-applied actions log `already-applied` and no duplicate mutation hits GitHub.

---

## Config

`backlog/triage-config.yml` (YAML, config-as-data — docs live in `references/classification.md`):

```yaml
theme_keywords:
  auth: [auth, oauth, token, session]
  docs: [docs, readme, guide]
activity_days:
  warm: 14
  cold: 60
stale_days: 60
duplicate_threshold: 0.75
```

Flags on individual scripts override config.

---

## References (load on demand)

- `references/classification.md` — bucketing rules (label, theme, age, activity) + YAML schema
- `references/relationships.md` — mention / blocks / depends-on / duplicate heuristics, evidence format
- `references/stale.md` — obsolescence signals, thresholds, suggested-action grammar
- `references/apply.md` — anchor grammar, parse rules, idempotency contract, apply-log schema

---

## Scripts (deterministic, no LLM needed)

All scripts live in `${CLAUDE_SKILL_DIR}/scripts/` and run from the target project root. Every script emits `--json` for composition.

- `scripts/triage-collect.js [--repo OWNER/REPO] [--limit N] [--json] [--dry-run]` — fetch open issues, write snapshot to `backlog/triage/.cache/<ISO-timestamp>.json`. Read-only.
- `scripts/triage-relate.js --snapshot PATH [--json]` — detect mentions / blocks / depends-on / duplicates. Errors if snapshot missing or malformed.
- `scripts/triage-stale.js --snapshot PATH [--since N] [--json]` — flag stale / obsolete candidates with evidence.
- `scripts/triage-report.js --snapshot PATH [--relate PATH] [--stale PATH] [--out PATH] [--json]` — render the markdown report with anchor comments. Re-runnable; creates `.bak` on overwrite.
- `scripts/triage-apply.js <report.md> [--apply] [--yes] [--json]` — parse anchor+checkbox pairs, execute accepted actions via `gh`. Default dry-run. Idempotent. Appends to `backlog/triage/<date>-apply.log` (JSONL).
- `scripts/triage-apply.integration.test.js` — opt-in live integration coverage for `triage-apply.js` against the disposable sandbox repo `sungjunlee/triage-apply-sandbox`. Requires `TRIAGE_APPLY_INTEGRATION=1` and `GH_TOKEN` with write access.

Scripts land in #61–#65; this file is the contract they must honor.
