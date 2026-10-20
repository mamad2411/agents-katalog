---
name: rz-networking-refresh-contacts
description: >
  Use when re-scoring and refreshing contacts already in HubSpot. Trigger phrases: "refresh stale contacts," "re-score Network Building," "refresh contacts in HubSpot," "rescore Lifecycle Stage Lead." Pulls a set of existing contacts (by HubSpot list ID, Lifecycle Stage filter, or stale-since-N-days), re-runs the LinkedIn relevance scan, updates the fit score, and conditionally drafts a warm opener seed if the existing seed is empty. Never auto-sends DMs and never creates deals.
---

# Networking Refresh Contacts

Sibling to `rz-networking-hand-curated-import`. Same per-row pipeline (steps 2-5 + 7), different entry point: a set of contacts already in HubSpot. Both skills load the same `corpus/networking/import-pipeline/` entries; this skill never creates contacts and never deals.

HubSpot portal: `245808914`. Networking uses the **contact** object only; no deals.

## Before beginning work

The corpus has migrated to Notion. Notion is the source of truth — the local `corpus/*` paths cited below are historical and may drift. Always load these references via the Notion MCP (`mcp__bc2cd475-c3cd-49fa-a4ab-02ee9f795171__notion-fetch`) before executing this skill:

1. **Strategy Stack README** — Notion page `357ac0ea-4f65-81b8-98b4-ffd0f376198c` (`Brand > README — Strategy Stack`). Doc ownership, canonical constants, and the Decision-of-Record log. Honor it; flag drift.
2. **Your sections of the Corpus** at `Projects > RZ Claude Skills > Corpus`:
   - `networking` → page `357ac0ea-4f65-8140-8b76-f1d2e745abd3` (canonical: import-pipeline pacing, fit-score, warm-opener-seed, tiers)
   - `voice` → page `357ac0ea-4f65-8194-ae1e-e5147adad60c` (voice guardrails for any drafted seed)

Each Corpus directory page lists its child entries. Fetch only the specific entries you need.

## Quick Reference

| Situation | Load / Do | Notes |
|---|---|---|
| User says "refresh stale contacts" or "re-score Network Building" | Pull contacts by filter, run pipeline 2-5 + 7 | Default filter: Lifecycle Stage = Lead AND `last_sequence_action_date` > 30 days ago |
| Profile shows new signals since last scan | Update relevance_score, append signals to Notes | Flag in Slack digest if score changes by 2+ |
| Existing `warm_opener_seed` is empty or null | Draft fresh seed using current signals | One-time backfill; preserved on subsequent runs |
| Existing `warm_opener_seed` is populated | Preserve it. Update other fields normally. | Riché's manual edits are higher signal than regeneration |
| Profile shows zero signals in last 60 days | Update `last_sequence_action_date` only; do not change score downward | Stale data is not signal; absence of new posts is not the same as relevance loss |
| Title or company changed since last scan | Apply the change, flag `job_change` in Slack digest | Only if unambiguous on the LinkedIn profile |

## Input contract

Four ways to scope the run, in order of precedence:

1. `--list-id <hubspot_list_id>`. Refresh every contact in a saved HubSpot list
2. `--lifecycle-stage <stage>`. Refresh every contact at the named stage (e.g., `lead`)
3. `--stale-days <N>`. Refresh every contact where `last_sequence_action_date` is older than N days
4. `--task-window <window>`. Refresh every contact associated with a HubSpot task whose `hs_timestamp` falls within the named window. Values:
   - `current-month` — first day of current month through last day inclusive
   - `current-week` — Monday through Sunday of current week
   - `next-N-days` — today through today+N (e.g., `next-7-days`)

   The skill resolves the date range at execution time, queries the `tasks` object via `search_crm_objects` (filter `hs_timestamp` GTE start, LTE end), maps to associated contacts via the `tasks → contacts` association (use `associatedWith` filter, `IN` operator, ≤30 task IDs per call to avoid HubSpot internal errors), dedupes by contact ID, then runs the standard per-contact pipeline.

Combinable: `--lifecycle-stage lead --stale-days 30` is the default invocation pattern (every Lead contact untouched in the last 30 days). `--task-window current-month --lifecycle-stage lead` is the standard monthly-routine pattern (every Lead contact with a task due this month).

Optional flags:
- `--regenerate-opener`. Force-redraft the warm opener seed even if populated. Use sparingly; the default conditional behavior preserves Riché's edits.
- `--resume <contact_id>`. Resume a stopped run starting from the given contact ID
- `--dry-run`. Emit the plan (which contacts would be touched, what would change) without writing to HubSpot

## Output contract

1. HubSpot **contact updates** (no deals, no Lifecycle Stage progression)
2. Slack digest to `#brand` (`C0APLNNAGJY`) with per-contact status
3. Child page under Notion `Networking Reports` (`34aac0ea-4f65-815e-8e1d-f70598cd7afc`) titled `Refresh [Mon date]` with the full run log

## The pipeline (per contact)

Loads from `corpus/networking/import-pipeline/`. Same entries as `rz-networking-hand-curated-import`, minus dedupe (the contact already exists) and minus contact creation (this skill only updates).

1. **Pull contact from HubSpot.** Read all relevant properties: `firstname`, `lastname`, `jobtitle`, `company`, `hs_linkedin_url`, `warm_opener_seed`, `last_sequence_action_date`, `relevance_score`, `lifecyclestage`, plus existing `Notes`. Note: this portal uses HubSpot's standard `hs_linkedin_url` field (not a custom `linkedin_url` property). The standard `lifecyclestage` field is queryable; `hs_lifecyclestage` is not.
2. **Open the LinkedIn profile.** Use `hs_linkedin_url` from the contact. Pacing rules apply (see `corpus/networking/import-pipeline/pacing-and-friction.md`). Sales Navigator obfuscated URLs (`/in/ACwAA...`) redirect to canonical handles when opened in a logged-in LinkedIn session.
3. **Relevance scan.** Capture up to 3 signals from the last 30-60 days. See `corpus/networking/import-pipeline/relevance-scan.md`.
4. **Company check.** Headcount, funding stage, recent news. See `corpus/networking/import-pipeline/company-check.md`. Compare against any company context already in Notes; flag material changes.
5. **Fit score.** Recompute the 1-5 score using the same rubric. See `corpus/networking/import-pipeline/fit-score.md`. Compare against the existing `relevance_score`; flag changes of 2+.
6. **Warm opener seed (conditional).** Check the existing `warm_opener_seed`:
   - If empty or null: draft a fresh seed using the latest signals. See `corpus/networking/import-pipeline/warm-opener-seed.md`.
   - If populated: preserve. Skip drafting.
   - If `--regenerate-opener` flag: redraft regardless.
7. **Update HubSpot contact.** Write the updated fields per `corpus/networking/import-pipeline/hubspot-write.md`. Lifecycle Stage stays at its current value; this skill never auto-progresses or auto-regresses.
8. **Log.** Append the contact to the Notion run log page with all captured fields and any changes flagged.

## What this skill does NOT do

- Does not create contacts. New contacts come from `rz-networking-hand-curated-import` (CSV) or manual HubSpot entry.
- Does not auto-progress Lifecycle Stage. Stages beyond `Lead` are Riché's manual call after real engagement.
- Does not auto-regress Lifecycle Stage to `Dormant`. A separate dormancy sweep handles that explicitly.
- Does not overwrite existing `warm_opener_seed` unless `--regenerate-opener` is set. Riché's edits are higher signal.
- Does not auto-DM. The seed sits in HubSpot; Riché sends or edits from there.
- Does not create deals. Networking is contact-only.

## Slack output (post after full refresh processed)

```
Refresh [date]
Filter: [filter description] | Contacts: N | Updated: N | Flagged: N | Skipped: N

UPDATED (N):
1. [Name], [Title] at [Company]
   Score: X -> Y | Lifecycle Stage: [stage]
   New signals: [count] | Seed: [drafted | preserved | regenerated]
   HubSpot: [link]

FLAGGED (N):
- [Name], [Title] at [Company] | Reason: [score_drop_2plus | job_change | company_change]
  Old: [X] | New: [Y]
  HubSpot: [link]

NO SIGNAL (N, last_sequence_action_date refreshed only):
- [Name] at [Company]

Run log: [Notion link]
```

## Common Mistakes

| Mistake | What goes wrong | Fix |
|---|---|---|
| Auto-overwriting `warm_opener_seed` | Loses Riché's manual edits | Conditional rule: preserve if populated; draft only if empty (see `warm-opener-seed.md`) |
| Auto-progressing Lifecycle Stage past Lead | Skill cannot tell when Riché actually engaged | Stage progression is manual, period |
| Auto-regressing to Dormant after N days no signal | Conflates "no new posts" with "relationship lapsed" | Dormancy is a separate manual or sweep skill, not a refresh side-effect |
| Refreshing every contact every run | Wastes the LinkedIn pacing budget; hits rate limits | Default to stale-only (`last_sequence_action_date` > 30 days); narrower filters for targeted reruns |
| Updating fields that did not change | Notes blow up with redundant entries | Diff before write; only update fields with material change |
| Skipping the dry-run on a new filter | Bad filters can touch hundreds of contacts unintentionally | Always `--dry-run` first when introducing a new filter pattern |

## Required HubSpot setup

Same as `rz-networking-hand-curated-import`. Required custom properties on the Contact object:
- `trigger_source`
- `warm_opener_seed`
- `last_sequence_action_date`
- `relevance_score`

Plus this standard HubSpot field, which must be populated (not custom-created):
- `hs_linkedin_url` — HubSpot's built-in LinkedIn URL field. The skill reads from this property, not from a custom `linkedin_url`.

Verify the custom properties exist before first run; the skill will not create them. HubSpot also caps `manage_crm_objects` batch updates at 10 records per call — the skill must split larger waves accordingly.

## Cross-skill connections

**Upstream (reads from these for canonical knowledge):**
- `rz-copywriting`. Owns voice. Any drafted opener (when seed is empty) must pass `corpus/voice/` rules and the Fatal Fifteen.
- `rz-networking`. Owns the philosophy (read-aloud test, mutual value). Frames whether a contact is worth refreshing at all.

**Downstream (hands off to these for execution):**
- `rz-networking-hand-curated-import`. Sibling skill that handles new contact creation from CSV. Shares the same `corpus/networking/import-pipeline/` entries.
- HubSpot. Output staging. Riché reviews flagged changes (score drops, job changes) and acts from HubSpot directly.

## Related

- Networking Reports (Notion `34aac0ea-4f65-815e-8e1d-f70598cd7afc`): where run logs go
- Networking Approach, Principles and Decisions (Notion `348ac0ea-4f65-8113-85d6-dee4fa4d7063`): governing doc
- The 6 automated networking prompts (Notion `34aac0ea-4f65-811c-b137-cde78dd064aa`): triggered flows that complement this batch refresh
