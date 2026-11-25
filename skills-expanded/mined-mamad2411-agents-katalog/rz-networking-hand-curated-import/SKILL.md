---
name: rz-networking-hand-curated-import
description: >
  Use when given a manually-curated Sales Navigator lead CSV to enrich, dedupe, score, and load into HubSpot. Trigger phrases: "import this CSV," "run hand-curated import," "process Sales Nav leads," "load these leads into HubSpot." Stages contacts at HubSpot Lifecycle Stage = Lead with a warm opener seed; never auto-sends DMs and never creates deals.
---

# Networking Hand-Curated Import

Companion to the 6 automated networking prompts. Different entry point: Riché has already applied judgment in Sales Nav. This skill does the enrichment, the dedupe, and the data entry.

HubSpot portal: `245808914`. Networking uses the **contact** object only; no deals.

## Before beginning work

The corpus has migrated to Notion. Notion is the source of truth — the local `corpus/*` paths cited below are historical and may drift. Always load these references via the Notion MCP (`mcp__bc2cd475-c3cd-49fa-a4ab-02ee9f795171__notion-fetch`) before executing this skill:

1. **Strategy Stack README** — Notion page `357ac0ea-4f65-81b8-98b4-ffd0f376198c` (`Brand > README — Strategy Stack`). Doc ownership, canonical constants, and the Decision-of-Record log. Honor it; flag drift.
2. **Your sections of the Corpus** at `Projects > RZ Claude Skills > Corpus`:
   - `networking` → page `357ac0ea-4f65-8140-8b76-f1d2e745abd3` (canonical: import-pipeline pacing, fit-score, warm-opener-seed, tiers, outreach)
   - `voice` → page `357ac0ea-4f65-8194-ae1e-e5147adad60c` (voice guardrails for warm-opener seeds)

Each Corpus directory page lists its child entries. Fetch only the specific entries you need.

## Quick Reference

| Situation | Load / Do | Notes |
|---|---|---|
| User says "import this CSV" or "process Sales Nav leads" | Run the per-row pipeline (steps 1 to 8) | Respect pacing in `corpus/networking/import-pipeline/pacing-and-friction.md` |
| CAPTCHA or rate-limit banner appears | Stop, post status to #brand, save row index | Riché resumes with `--resume <notion_log_url>` |
| Profile shows zero signals in last 60 days | Mark `no_signal`, draft seed against company or title | Set `seed_basis = company` in log, still create at scores 3+ |
| Score is 1 or 2 | Send to review queue, do not auto-create | Riché replies `approve N` to force-add |
| Drafting `warm_opener_seed` | Apply voice guardrails (hard constraints, not style) | See `corpus/networking/import-pipeline/warm-opener-seed.md` |
| Existing HubSpot contact (dedupe match) | Skip; do NOT update | Refreshing existing contacts is `rz-networking-refresh-contacts`'s job |

## Input contract

CSV with exact header names:

- `name` (required)
- `title` (required)
- `company` (required)
- `linkedin_url` (required)
- `notes` (optional, Riché's reason for including them)

Skill accepts the path as the first positional argument. Optional `--resume <notion_log_url>` flag skips rows already logged.

## Output contract

1. HubSpot **contacts** (no deals) at Lifecycle Stage `Lead` for confident matches (fit score 3+)
2. Slack digest to #brand (`C0APLNNAGJY`) with per-row status
3. Child page under Notion `Networking Reports` (`34aac0ea-4f65-815e-8e1d-f70598cd7afc`) titled `Manual Import [Mon date]` with the full run log

## The pipeline (per row)

Every step has a corpus entry under `corpus/networking/import-pipeline/`. Load the entry for the step you are executing.

1. **Dedupe.** Match on full name OR `linkedin_url` substring. On match, log `dedupe_match` and skip. See `corpus/networking/import-pipeline/dedupe.md`.
2. **Open the profile.** Use the Claude-in-Chrome MCP to open `linkedin_url`. Wait for DOM to settle. Pacing rules apply (see `corpus/networking/import-pipeline/pacing-and-friction.md`).
3. **Relevance scan.** Capture up to 3 signals from the last 30-60 days. See `corpus/networking/import-pipeline/relevance-scan.md`.
4. **Company check.** Headcount, funding stage, recent news. See `corpus/networking/import-pipeline/company-check.md`.
5. **Fit score (1-5).** Combine signal strength, title fit, company stage. Auto-create for 3+; queue for 1-2. See `corpus/networking/import-pipeline/fit-score.md`.
6. **Warm opener seed.** One sentence, voice-locked, references the strongest signal. No-signal fallback uses company. See `corpus/networking/import-pipeline/warm-opener-seed.md`.
7. **Create in HubSpot.** Contact only, Lifecycle Stage = `Lead`. No deal creation. See `corpus/networking/import-pipeline/hubspot-write.md` for the full property list and write rules.
8. **Log.** Append the row to the Notion run log page with all captured fields.

## Slack output (post after full CSV processed)

```
Manual Import [date]
CSV: [filename] | Rows: N | Added: N | Skipped: N | Review: N

ADDED TO HUBSPOT (N):
1. [Name], [Title] at [Company] | Score: X/5
   Seed: [first 100 chars]
   HubSpot: [link] | LinkedIn: [link]

DEDUPE MATCHES (N):
- [Name], already in HubSpot at Lifecycle Stage [stage] | HubSpot: [link]

REVIEW QUEUE (score 1 or 2) (N):
- [Name], [Title] at [Company] | Flagged: [reason]
  Reply `approve N` to force-add at Lifecycle Stage Lead

NO SIGNAL (N, added with company-based seed):
- [Name], [Title] at [Company]

Run log: [Notion link]
```

## On `approve N` reply in-thread

Force-add the flagged row using the same step 7 pattern (contact only, Lifecycle Stage = `Lead`), with `relevance_score = override_approved` and `trigger_source = Sales Navigator`.

## Common Mistakes

| Mistake | What goes wrong | Fix |
|---|---|---|
| Inventing signals not on the profile | Bad data lands in HubSpot, opener feels off, trust erodes | Mark `no_signal` and use company-based seed |
| Auto-DMing instead of staging | Violates the core skill contract | Stage in `warm_opener_seed`; Riché sends or edits from HubSpot |
| Parallelizing profile fetches or batch-opening tabs | LinkedIn TOS risk, triggers rate-limit and lockout | Human-pace pacing only, one profile every 8 to 15 seconds |
| Pushing through a CAPTCHA or warning banner | Account flag risk, lost session | Stop immediately, post to #brand, save index, exit |
| Creating a deal alongside the contact | Doubles the record set; networking is not revenue | Contact only. Lifecycle Stage on the contact tracks relationship state. |
| Updating an existing contact on dedupe match | Out of scope for this skill | Skip; refresh is `rz-networking-refresh-contacts`'s job |

## Required HubSpot setup (one-time)

Custom properties on the Contact object (verify before first run, create via HubSpot MCP if missing):

- `linkedin_url` (single_line_text)
- `trigger_source` (enum; include `Sales Navigator` option)
- `warm_opener_seed` (rich_text)
- `last_sequence_action_date` (date)
- `relevance_score` (enum: `1`, `2`, `3`, `4`, `5`, `override_approved`)

Lifecycle Stage values used (Riché's custom set): `Subscriber`, `Lead`, `Engaged`, `Active`, `Opportunity`, `Customer`, `Evangelist`, `Dormant`. This skill only ever sets `Lead`.

## Cross-skill connections

**Upstream (reads from these for canonical knowledge):**
- `rz-copywriting`. Owns voice. Warm opener seed must pass `corpus/voice/` rules and the Fatal Fifteen.
- `rz-networking`. Owns the philosophy (read-aloud test, mutual value). Outreach templates for follow-up sends live in `corpus/networking/outreach/`.

**Downstream (hands off to these for execution):**
- `rz-networking-refresh-contacts`. The companion skill that re-scores and refreshes contacts already in HubSpot. Both skills load the same `corpus/networking/import-pipeline/` entries.
- HubSpot. Output staging. Riché sends or edits from HubSpot directly; the skill never auto-sends.

## Related

- Networking Scheduled Task Prompts (Notion `34aac0ea-4f65-811c-b137-cde78dd064aa`): the 6 automated flows this skill complements
- Networking Reports (Notion `34aac0ea-4f65-815e-8e1d-f70598cd7afc`): where run logs go
- Networking Approach, Principles and Decisions (Notion `348ac0ea-4f65-8113-85d6-dee4fa4d7063`): governing doc
