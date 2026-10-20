---
description: Health-check the wiki and auto-fix what's fixable.
when_to_use: Run weekly, or after a batch of ingests. Uses staleness-gated scans — frontmatter-only by default, full-body only where needed. Auto-fixes the easy ones; reports contradictions, orphans, stale content, and synthesis candidates for human decision. Also triggered by phrases like "audit the wiki", "check wiki health", "run lint".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
---

# Wiki Lint

Read `CLAUDE.md` for conventions. Follow the LINT operation exactly as specified there.

## Pre-flight

1. Rebuild the sidecar cache:
   ```bash
   python3 scripts/build_meta.py --embed-if-enabled
   ```
2. Run the cheap invariant suite first — if it fails, fix the
   filesystem before running heavier checks:
   ```bash
   bash scripts/check_invariants.sh
   ```

## Staleness gate (context-engineering)

LINT reads in tiers, cheapest first. A page read in the most
recent 7 days (by `last_seen` frontmatter) stays in the frontmatter
tier unless a frontmatter problem signals the body might be wrong.

- **Tier 1 — frontmatter only.** Read the first ~30 lines of every
  page. Check required fields, shape, `source_count` / `inbound_refs` /
  `inbound_refs_primary` against the sidecar. Fix in place.
- **Tier 2 — full body.** Only for pages that failed Tier 1, or
  whose `last_seen` is older than 7 days, or that are new since the
  last lint. Check wikilink resolution, callout syntax, and
  contradictions.
- **Tier 3 — cross-page contradictions.** Dispatched as a
  **subagent** (see `.claude/skills/context-engineering/SKILL.md`).
  The subagent reads every pair of pages that share ≥2 cited
  sources and returns a structured contradiction report. Parent
  session never sees the raw bodies.

## Auto-fix without asking

- Missing or malformed frontmatter (add required fields, preserve
  existing values).
- Broken `[[wikilinks]]` → create stubs from `templates/stub.md`.
- Filenames not in kebab-case → rename the file and update every
  inbound reference.
- Two pages describing the same subject under different names →
  merge, keeping the more common name.
- `source_count` / `inbound_refs` / `inbound_refs_primary` drift on
  concept/entity pages → recount from `wiki/.meta/backlinks.json` and
  update frontmatter.
- `wiki/views/**/*.base` YAML validity.
- `wiki/canvases/**/*.canvas` JSON validity.

## Promote candidates, do NOT auto-promote

Stubs that cross the promotion threshold (`source_count >= 2` or
`inbound_refs_primary >= 5`) are listed as candidates. LINT **does not**
promote them automatically — that is `/wiki-promote`'s job. This
keeps LINT cheap and predictable; promotion is where real cost
lives. The unscoped `inbound_refs` is never used for promotion (it
counts outputs/syntheses, which are Claude-authored downstream
artifacts).

## Do not auto-fix — report instead

- Contradictions between pages (list both sides, with file paths).
- Orphan pages (no inbound `[[wikilinks]]`).
- Stale content: `last_seen` older than 180 days.
- **Synthesis candidates:** any cluster of ≥3 outputs sharing ≥2
  cited pages. Propose a synthesis topic in the report; user decides
  whether to promote.

## After fixes

- Re-run `python3 scripts/build_meta.py --embed-if-enabled` so the sidecar reflects
  any renames / merges.
- Re-run `python3 scripts/shard_index.py` to refresh catalogs.
- Re-run `bash scripts/check_invariants.sh` — all tests must pass
  after a clean lint. Failing: report as critical.

## Output

- `wiki/outputs/lint-report-{today}.md` from `templates/output.md`,
  with sections: Auto-fixed / Needs my attention / Promotion
  candidates / Suggested next sources / Suggested next questions.
- Update `wiki/index.md` (via `shard_index.py`) and append to
  `wiki/log.md`.

## Reporting

- Tier-1 checks: fields fixed, pages touched
- Tier-2 checks: wikilinks fixed, stubs created
- Tier-3 subagent report: contradictions surfaced
- Invariant suite: pass/fail summary
- Promotion candidates (list, with thresholds)
- Orphans, stale pages, synthesis candidates
