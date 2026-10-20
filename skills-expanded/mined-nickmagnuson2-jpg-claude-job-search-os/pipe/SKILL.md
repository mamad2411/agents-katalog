---
name: pipe
description: Track job applications through stages with auto-generated action items per stage
argument-hint: [add|update|remove <company> [role|stage] [url]]
user-invocable: true
allowed-tools: Read(*), Glob(data/*), Grep(data/*), Bash(PYTHONIOENCODING=utf-8 python3 tools/pipe_read.py:*), Bash(PYTHONIOENCODING=utf-8 python3 tools/pipe_write.py:*)
---

# Job Application Pipeline

Track job applications through a stage-based pipeline with auto-generated action items per stage transition.

## Arguments

- `$ARGUMENTS`: Optional. If empty, show the current pipeline summary.
  - `add <company> <role> [url]` — add a new application
  - `update <company> <new-stage>` — advance an application to a new stage
  - `remove <company>` — remove/archive an application

Examples:
- `/pipe` — show pipeline summary and what needs attention
- `/pipe add Stripe "Senior PM"` — add new application at Researching stage
- `/pipe add Notion "Product Manager" https://notion.so/careers/pm` — add with URL
- `/pipe update Stripe "Phone Screen"` — advance Stripe to Phone Screen
- `/pipe remove Stripe` — archive the Stripe application

## Data File

All pipeline data lives in `data/job-pipeline.md`.

## Instructions

### Command: Show Pipeline (no arguments)

1. Read `data/job-pipeline.md`.
2. If the file is empty or has no entries, display a welcome message:
   ```
   Pipeline is empty. Add your first application:
     /pipe add <company> <role> [url]

   Stages: Researching → Applied → Phone Screen → Interview → Offer → Accepted/Rejected/Withdrawn
   ```
3. Run `pipe_read.py` to get structured pipeline data:
   ```bash
   PYTHONIOENCODING=utf-8 python3 tools/pipe_read.py
   ```
   Use the JSON output to build the display:
   - `needs_attention[]` → "Needs Attention" table (above Full Pipeline); use `stale_label` for the Days Since Update column and note `missing_action` entries
   - `active_entries[]` → "Full Pipeline" table, most recently updated first; use each entry's `stale_label` for inline Stage annotations
   - `metrics` → summary stats header (total_active, total_stalled)
   - `stage_distribution` (top-level key, NOT under `metrics`) → per-stage counts
   - `metrics.archived_count` → Archived section count (collapsed)
   - `company_index` → use in `add` command to check for duplicates before writing

### Command: `add <company> <role> [url]`

0. **Fit-reason capture (do this first).** Ask Nick a one-line fit read: *"Quick fit read — why is (or isn't) this in your lane?"* If he gives one, pass it through in step 1 as `--fit-reason "<his words>"`, plus `--fit-verdict {fit|not-fit|neutral|unknown}` if he names a verdict. Keep it optional and light (one prompt, accept a skip) — do NOT block the add on it. Rationale: this one line is the source-coverage input the calibration loop was starving for — the blind machine re-run abstained on 9 of 52 of Nick's fit calls purely because his reasoning lived only in his head (`output/analysis/071526-machine-vs-human-agreement.md`).
1. Call `pipe_write.py add`:
   ```bash
   PYTHONIOENCODING=utf-8 python3 tools/pipe_write.py --repo-root . add "<company>" "<role>" [--url URL] [--fit-reason "..."] [--fit-verdict fit|not-fit|neutral|unknown]
   ```
2. If result `action == "duplicate_warning"`: warn user and show `existing_roles[]`. Ask if they want to add a second role anyway (if yes, re-run with `--stage` override) or update the existing entry.
3. On success: display the new entry and its auto-generated action items (see Stage Actions below).
4. **Cross-reference**: Check if this company/role appears in `.claude/skills/scan-jobs/cache.md` — if found, mention the fit score from the scan.

### Command: `update <company> <new-stage>`

0. ⛔ **`update` NEVER closes a row. Closing is `remove --stage`.** If the new stage is terminal —
   anything meaning the opportunity is over (`Closed`, `Closed - they passed`, `Considered - passed`,
   `Declined`, `Skipped`, `Withdrawn`, `Rejected`) — **stop and use the `remove` command below
   instead.** `update` leaves the row in `## Active Pipeline` with a freeform stage string, which:
   - keeps it counted as a live company by `todo_write.py sync`, so its prep/research to-dos can
     never be auto-withdrawn, and
   - puts it in sync's "still live" set, which **blocks that company from ever syncing** even after a
     later correct archive.

   Measured 2026-08-14: **30 companies** were in this state, some for four months, because this step
   used to list close stages as valid `update` targets. A `check_pipe_close_via_update.py` hook now
   BLOCKs it. See `docs/CHANGELOG.md` 2026-08-14.

1. **Fit-reason capture on fit-forming stage changes.** When Nick declines, self-passes, or a company
   passes — his **highest-signal fit-negatives** — OR he volunteers a fit read, ask one line: *"One-line
   fit read for the ledger — why did this fit or not?"* and pass it as `--fit-reason "<his words>"`
   (+ `--fit-verdict` if named) **on the `remove` call**. Light and optional (accept a skip); do not
   block. Skip the prompt for routine mechanical advances (e.g. Researching → Applied) unless Nick
   offers a read.
1. Call `pipe_write.py update`:
   ```bash
   PYTHONIOENCODING=utf-8 python3 tools/pipe_write.py --repo-root . update "<company>" "<new-stage>" [--role ROLE] [--new-role ROLE] [--next-action TEXT] [--fit-reason "..."] [--fit-verdict fit|not-fit|neutral|unknown]
   ```
   `--role` SELECTS which row when a company has several; `--new-role` SETS the Role cell.
   Use `--new-role` to correct a title that arrived after the row was created. Do NOT
   remove-and-re-add for a rename: `remove` soft-deletes, so it leaves a duplicate company
   row behind, and the next `update` then fails with `ambiguous_match`.
2. If result `code == "ambiguous_match"`: show the `matches[]` list and ask user to specify `--role`.
3. If result `code == "not_found"`: tell user no active entry was found.
4. On success: display the updated entry with stage-appropriate action items and any relevant coaching links.

### Command: `remove <company>` — this is also how you CLOSE a row

1. **Ask which terminal stage, do not derive it.** `--stage` takes exactly one of
   `Withdrawn | Rejected | Accepted`, and the distinction is a fact about what happened:

   | Stage | Means | Use when |
   |---|---|---|
   | `Rejected` | **They** passed on Nick | company declined, ghosted an application, or stopped advancing him |
   | `Withdrawn` | **Nick** passed on them | self-pass, failed a hard filter, or the role evaporated |
   | `Accepted` | offer taken | — |

   ⛔ **Never infer this from the row's Notes.** Classifying 30 closes from their notes on 2026-08-14
   was right ~28/30, and the misses *inverted a fact about someone else's decision*. `Closed - no
   response` meant Withdrawn for one company and Rejected for three others on the same day; only Nick
   knows whether he actually applied and how far they engaged. Present the classification for
   confirmation, in one batch. Per [[feedback_pipeline_applied_status_must_be_user_confirmed]].
   The tool's own help says it: *"archiving a rejection as a withdrawal inverts the fact."*

2. Call `pipe_write.py remove`:
   ```bash
   PYTHONIOENCODING=utf-8 python3 tools/pipe_write.py --repo-root . remove "<company>" \
     [--role ROLE] --stage Withdrawn|Rejected|Accepted [--fit-reason "..."] [--fit-verdict ...]
   ```
   `--stage` defaults to `Withdrawn` if omitted — do not rely on the default when the company passed.
3. If `code == "ambiguous_match"`: show `matches[]` and ask user which role to remove. A company with
   two roles can have two different outcomes; resolve each separately.
4. On success: confirm the archive (moved to `## Archived` under the chosen terminal stage).

## Pipeline Stages

```
Researching → Applied → Phone Screen → Interview → Offer → Accepted
                                                         → Rejected
                                                   → Withdrawn (at any point)
```

Terminal stages: `Accepted`, `Rejected`, `Withdrawn`

## Stage Actions

Auto-generated action items when entering each stage:

### → Researching
- Research the company (product, culture, recent news)
- Check fit against your profile (`data/profile.md`)
- Identify the right CV angle for this role
- Find the job posting URL if not already captured

### → Applied
- Note which CV was used (update CV Used column)
- Set a follow-up reminder for 1 week out
- Save the job posting text for interview prep

### → Phone Screen
- Review `framework/answering-strategies/anti-patterns.md` (60-second checklist)
- Prep your recruiter pitch using `coaching/coached-answers/recruiter-pitch.md`
- Review relevant coached answers for this role type
- Run `/voice-export` to practice if time allows

### → Interview
- Prep technical/behavioral answers for this specific role
- Research the team and interviewer(s) if known
- Review company-specific notes from the Researching stage
- Run a mock interview session with `/debrief` workflow

### → Offer
- Review compensation expectations from `data/profile.md`
- Compare against market rates
- Prepare negotiation points

### → Accepted
- Archive other active applications or mark as Withdrawn
- Update `data/profile.md` with new role details

### → Rejected
- Note rejection reason if known (for pattern tracking)
- Review what could be improved for similar roles
- **Close linked networking threads (mandatory):** grep `data/networking.md` for contacts whose Company column matches this entry (or a recruiter/agency tied to it, e.g. a marketplace recruiter for a recruiter-sourced role). For each contact with an open follow-up on this thread, append a dated Interaction Log entry ending `**Follow-up:** — (closed)`. Without this, `networking_followup.py` keeps resurfacing a dead thread in every future `/standup` (origin: 2026-07-09 — a pipeline entry closed but a contact's networking follow-up kept surfacing as due for 2+ days after).

### → Withdrawn
- Note reason for withdrawing
- **Close linked networking threads** — same sweep as Rejected above.

## Display Format

When showing the pipeline, use this format:

```markdown
## Job Pipeline — [date]

**Active: N applications** | Researching: X | Applied: X | Phone Screen: X | Interview: X | Offer: X | Stalled: X

### Needs Attention
| Company | Role | Stage | Days Since Update | Next Action |
|---------|------|-------|------------------|-------------|
| Acme AI | Strategy & Ops | Researching ⚠️ | 5 days | — |
| Northwind | Chief of Staff | Researching ⚠️ | 9 days | Follow up with recruiter |

### Full Pipeline
| Company | Role | Stage | Updated | Next Action | CV | URL |
|---------|------|-------|---------|-------------|-----|-----|
| Acme AI | Strategy & Ops | Researching ⚠️ [5 days stale] | 2026-02-18 | — | — | — |
| Northwind | Chief of Staff | Researching ⚠️ [9 days stale] | 2026-02-14 | Follow up | — | — |
| Beacon | CoS | Researching | 2026-02-23 | Research role | — | — |

### Archived (N)
[collapsed — show count only unless user asks]
```

Sort by Date Updated descending (most recent first).

**Staleness and attention logic is computed by `pipe_read.py`** — use `stale_label` and `missing_action` fields from the JSON output. Do not re-compute dates inline.
