---
name: checkout
description: End-of-day close-out — writes daily log, surfaces tomorrow's top 3 priorities, optional reflection prompt. Bookend to /standup.
argument-hint: ""
user-invocable: true
allowed-tools: Read(*), Glob(data/*), Glob(output/**), Write(data/job-todos-daily-log.md), Write(data/job-todos.md), Bash(python3 tools/todo_daily_metrics.py:*), Bash(python3 tools/granola_cli.py:*), Bash(find:*), Bash(grep:*), Bash(bash tools/backup-data.sh:*), TaskList
---

# Checkout — End-of-Day Close-Out

End-of-day bookend to `/standup`. Owns the daily log entirely — writes today's snapshot, calculates progress trends, and surfaces tomorrow's top 3 priorities. Nothing is re-derived elsewhere; this is the single source of truth for daily progress data.

Takes no arguments. Always runs for today's date.

## Instructions

### Step 1: Pre-Process Data

Run the preprocessing script to extract all daily metrics in one call:

```bash
python3 tools/todo_daily_metrics.py --target-date $(date +%Y-%m-%d)
```

Parse the JSON output. The script reads all source files and returns:
- `completed_today[]` — tasks with today's date in their completion notes (separator rows filtered)
- `active_remaining[]` — all active (non-done) tasks (`---` separator rows filtered out)
- `overdue[]` — tasks past their due date
- `outreach_sent_today[]` — **UNION** of outreach-log entries + today's blockquoted networking touches (de-duped by name+channel). Each entry has a `source` field: `"outreach-log"` or `"networking.md"`.
- `outreach_touches_today_from_networking[]` — raw subset (the networking-only side of the union, for transparency)
- `research_completed_today[]` — dossier files updated today
- `changelog_today[]` — changelog entries for today
- `metrics{}` — streak (corrected to count today's pre-log completions), this_week, last_7, last_30, all_time, avg_per_day, overdue_trend
- `pipeline_snapshot{}` — **BUCKETED**: `{ active_process: [], evaluation_backlog: [], terminal: [] }`. Use `active_process` for the displayed snapshot. `evaluation_backlog` is the "To Evaluate / To Apply / Researching" surface (count it, don't list it). `terminal` is Closed/Rejected/Withdrawn/Skipped/Archived (don't display).
- `networking_activity[]` — contacts with pending todos (separator rows filtered)
- `substantive_work{}` — `{ outputs_today, outputs_by_entity{}, outputs_paths_by_entity{}, reflections_today, reflections_paths[], memories_today, memories_names[], inbox_entries_today }`. **Treat this as a first-class progress signal**, not optional decoration — heavy work-up days (deep reviews, agent runs, memory captures, drafts) show up here when `completed_today` undercounts them.

**Do not re-read the source files** — use these values directly in Steps 3–7. Specifically: **do NOT call Read on `data/job-todos.md` with a `limit:` parameter** — silent truncation past line 120 produces wrong rankings (origin: 2026-05-13 /standup miss + same-day /checkout fix; see `memory/feedback_todos_full_file_read_required.md`).

Also read separately (not covered by the metrics script):
- `data/weekly-review-log.md` — for tomorrow's top 3 cross-reference (Step 6)
- `data/reflections/_longitudinal.md` (if present) — read the TOP entry only (newest). Surface 1-2 headline lines from its three axes (thinking patterns / decision biases / communication tendencies) as the longitudinal read in the checkout summary. This is the `/my-world` deep-pass output; skip silently if the file does not exist.

### Step 1b: (Deprecated — now in todo_daily_metrics.py)

The artifact scan is now part of the Step 1 metrics script. The `substantive_work` field returns the same data the bash find commands used to produce: outputs by entity, reflection paths, memory names, inbox entries today. Use that directly. No separate `find` invocations needed.

Heavy-work-up signal: if any entity has 3+ files modified today (`substantive_work.outputs_by_entity[entity] >= 3`), list the files individually from `substantive_work.outputs_paths_by_entity[entity]`. Otherwise just show the count.

### Step 2: Check for Existing Entry

Check `data/job-todos-daily-log.md` for an entry with today's date header (`### YYYY-MM-DD`):
- If found: replace that entry when writing in Step 3.
- If not found: prepend a new entry after the log header.

### Step 3: Write Daily Log Entry

Write today's entry to `data/job-todos-daily-log.md` in this exact format:

```markdown
### YYYY-MM-DD (Weekday)

**Completed today: N** | Active remaining: N | Overdue: N

#### Done
- [x] Task description (Priority)
- [x] Task description (Priority)
(or "Nothing completed yet today." if zero)

#### Still Active
- [ ] Task description [Priority | Due: date]
- [ ] Task description [Priority | Due: date]

#### Research Completed
- Company: [Name] (output/[slug]/[slug].md)
- Industry: [Name] (output/[slug]/[slug].md)
(omit section entirely if no research completed today)

#### Outreach Sent
- [Name] @ [Company] — [channel] — "[subject/summary]"
(omit section entirely if no outreach sent today)

#### System Changes
- [Entry title] — [one-line summary]
(omit section entirely if no changelog entries match today)

#### Artifacts Produced Today
**Outputs (N files across M entities):**
- `output/<entity>/` — N files (list paths if heavy work-up, otherwise count only)
**Reflections:** N files (list paths)
**Memories:** N captured (list names)
**Inbox:** N new entries today
(omit each line if zero; omit section entirely if all four are zero)

#### Pipeline Snapshot (Active Process Only)
| Company | Role | Stage |
|---------|------|-------|
| [Company] | [Role] | [Stage] |

(Use `pipeline_snapshot.active_process` from the script — roles actively moving forward. Do NOT include the To-Evaluate backlog or Closed/Rejected/Withdrawn here.)

> Evaluation backlog: N entries pending screening (from `pipeline_snapshot.evaluation_backlog.length`)
> Terminal (closed/rejected/withdrawn) this cycle: N (from `pipeline_snapshot.terminal.length`) — historical only

#### Networking Activity
- [Name] ([Company], [relationship]) — last: [date], pending to-dos: N
(omit section if no relevant activity)

---
```

**If `data/job-todos-daily-log.md` doesn't exist:** Create it with this header before writing:
```markdown
# Job Search — Daily Progress Log

> Auto-generated by `/checkout`. One entry per day.
> Newest entries first. Do not delete entries — they power progress tracking.

---
```

### Step 4: Use Trend Metrics from Script Output

The `metrics{}` block from Step 1 already contains all trend data — use it directly:

- `metrics.streak` — consecutive days with completions
- `metrics.this_week` — completed items in the last 7 days
- `metrics.avg_per_day` — average completions per active day
- `metrics.overdue_trend` — `↑`, `→`, or `↓`
- `metrics.entry_count` — if 0, display "N/A — first day tracked" for history-dependent metrics

### Step 4b: Auto-close prep todos with completion evidence (mandatory)

Before computing Tomorrow's Top 3, sweep for `Pending` todos whose trigger event happened today but were never closed by their owning skill. This is the catch-all gate that fixes drift when `/debrief` or `/standup` didn't run or didn't close their trigger todos.

Patterns to sweep (run each in parallel, treat absent matches as no-op):

1. **Call-prep todos with debrief evidence:** for each file in `coaching/progress/$(date +%Y-%m-%d)-*.md`, extract the slug from the filename and run `tools/todo_write.py done "<slug> call"`. Report any closures.
2. **Morning-starter read todo:** if `data/workbooks/_morning-starter-$(date +%Y-%m-%d).md` exists, run `tools/todo_write.py done "READ FIRST: data/workbooks/_morning-starter-$(date +%Y-%m-%d).md"`. If status is "No task found," skip (already closed by `/standup`). If "ok," report closure.
3. **Print-before-call todos:** if a `Print [Company] [doc] PDF before [Person] call` todo exists and the corresponding call file exists in `coaching/progress/$(date +%Y-%m-%d)-*.md`, close it.

Display closures under `#### System Changes` in the checkout summary as: `Auto-closed N prep todo(s): [task fragments]`.

If `status: error, "Multiple matches"` is returned by any sweep, surface the matches and ask Nick before closing. Don't guess.

Origin: 2026-05-14 audit (a 5/13 phantom-overdue prep todo). Skill workflows can fail to close their trigger todos; `/checkout` is the daily safety net.

### Step 4c: Audit unexpected state — diagnose, don't close (mandatory)

Before declaring checkout complete, audit any tracked items in unexpected state. **Don't reflexively close anything in this step.** The point is to surface gaps, name causes, and let Nick decide.

Origin: 2026-05-27 task #4 reflexive close — see `memory/feedback_diagnose_unexpected_state_before_closing.md`. Family N=3 with `feedback_audit_before_claiming_done_at_session_end` + `feedback_end_of_session_gap_audit`.

**Audit surfaces (run each):**

1. **Claude Code session task state.** Call `TaskList` **if it is available in this session** — it is not present in every harness build. If the tool does not exist, do NOT silently skip: state one line in the State Audit section ("`TaskList` unavailable this session — stuck-task surface not audited") and continue with the other four surfaces. An unaudited surface reported as clean is the failure this whole step exists to prevent. When available, for each task with `status: in_progress`:
   - Note when it was last updated (from the task data).
   - State your best guess at root cause: "work completed but never closed," "work blocked," "abandoned," "actively in progress."
   - Surface the task + cause to Nick. Do NOT close it without explicit confirmation.

2. **Job-todos overdue >7 days.** From `active_remaining` (Step 1 output), filter for items where `due` is more than 7 days in the past AND status is still `Pending`. For each:
   - State why it's overdue (trigger event happened but skill didn't close? skill never ran? trigger never fired?).
   - Don't auto-close. Surface for Nick's decision.

3. **Pipeline entries with no movement in 14+ days.** From `pipeline_snapshot.active_process`, identify stages that haven't changed in 2+ weeks. State whether this is normal cadence (recruiter ghosting) or unexpected (mid-process stall). Don't change stages — just flag.

4. **Networking contacts with pending follow-ups overdue.** From `networking_activity`, identify contacts with pending to-dos past their due date. Surface for follow-up decision.

5. **Overdue todos that read as already-done.** For each `Pending` todo in `active_remaining` overdue by 7+ days (same set as audit #2), fuzzy-match its text against the top 5 entries of `data/accomplishments.md` and `data/decisions.md`, plus today's `substantive_work` output paths — not just today's Done list, since this catches work completed on an earlier day whose todo was never closed (e.g. a "ship N projects" todo left open for weeks after the last of N shipped). A match is a strong keyword/entity overlap (same project name, same deliverable noun), not a topic-level resemblance. Surface each candidate match for Nick's confirm; on "yes, close it," run `todo_write.py done`. Never auto-close — this is a fuzzy match, more error-prone than the exact-slug patterns in Step 4b. Origin: 2026-07-09 — two High-priority todos (a shipped-project todo and a completed voice-pass todo) sat open for weeks/a day respectively and surfaced as false "Today's Top 3" items in `/standup` before Nick caught it.

**Display under a new section `#### State Audit (diagnose, don't close)`** in the checkout summary. Format:

```
#### State Audit (diagnose, don't close)
- **Stuck Claude task #N** ([subject]) — in_progress since [time]. Likely cause: [diagnosis]. Action: [proposed; awaiting decision].
- **Long-overdue todo:** "[task]" — [N days overdue]. Cause: [diagnosis].
- **Stalled pipeline:** [Company] at [Stage] since [date] — [normal/unexpected].
(omit section entirely if all four audits return clean)
```

**The discipline: name the cause before naming the action.** If you can't diagnose, say so explicitly ("I don't know why this is stuck — need your input"). Reflexive closure is the failure mode this step exists to prevent.

### Step 4d: Granola debrief cascade (propose only)

Scan today's Granola meetings for calls that were never debriefed, and surface them so the day's residue is visible before checkout closes. **Propose only. Never auto-run `/debrief`** — `/debrief` is Nick-first cold-scoring, and auto-running it inside `/checkout` would corrupt that methodology.

Origin: an external personal-OS system's `/eod` cascade (E3, build queue 2026-05-28). Composes with the T7 raw-Granola precondition gate in `/debrief`.

**Steps:**

1. List recent meetings:
   ```bash
   python3 tools/granola_cli.py list --hours 24 --format json
   ```
   Parse the JSON array (each entry has `id`, `title`, `created_at`, `local_time`).

2. **Exclude therapy-classified calls silently.** A meeting whose title matches the therapy keywords in `tools/granola_auto_debrief.py` (`THERAPY_TITLE_KEYWORDS`: therapy, couples, psychiatrist, and the recurring therapist first names) is sealed personal context. Drop it from the cascade without listing it. Do not name it, count it, or hint at it in the checkout summary.

3. **Cross-reference each remaining meeting against existing debrief artifacts.** A meeting is "debriefed" if either:
   - a debrief file exists in `coaching/progress/` whose date matches the meeting's local date AND whose filename slug fuzzy-matches the meeting title (e.g. "recruiter screen" matches `2026-06-01-recruiter-acme.md`), OR
   - a raw transcript for it already lives in `data/voice-corpus/granola/` for that date (secondary signal that it was at least pulled).

   A meeting with neither is **un-debriefed**.

4. **Surface un-debriefed meetings** under a `#### Granola Debrief Cascade` section in the checkout summary (Step 6). For each: `[local_time] — [title]` plus the exact next-step command. Do not run the command.

5. If every non-therapy meeting is already debriefed, or none were found, **omit the section entirely.**

**Graceful degradation:** if `granola_cli.py` errors (no auth, network, Granola unavailable), skip the cascade and note one line in the summary: `Granola cascade skipped (unavailable).` Do not block checkout on it.

### Step 4e: Surface accomplishment candidates (propose, never auto-log)

Scan the day's work for milestone-level wins worth logging to `data/accomplishments.md`, and PROPOSE them for Nick's confirmation. This is the evidence-grounded counterpart to the silent-failure probe: checkout already computed the day's artifacts, so a real win should not depend on Nick remembering to mention it.

**Inputs (all from Step 1 — no new reads):** `substantive_work` (outputs, memories, reflections, inbox), the day's `#### System Changes`, and any win-shaped reflection in `substantive_work.reflections_paths`.

**The milestone bar (apply strictly — default to ZERO candidates).** `data/accomplishments.md` holds *milestone-level job-search-PROCESS wins* — the kind worth a retro or a LinkedIn post. It is NOT a daily-task log and NOT career-history. A candidate qualifies ONLY if it clears all three:
1. **Milestone, not maintenance.** A landed onsite, a shipped dossier/artifact, a new system or capability that compounds, a relationship ladder built — not "wrote a log entry," "fixed a hook," "triaged todos."
2. **Process win, not career-history.** About the *search* (or a builder-credibility asset for it), not a resume bullet (those live in `data/projects/`).
3. **Stands on its own a week from now.** If it reads as routine in seven days, it is daily work, not an accomplishment.

**Anti-inflation is the whole point.** Most days produce ZERO accomplishment candidates — that is the correct, common output. A heavy build day is still usually maintenance. Propose at most 1-2. When unsure, do NOT propose; the silent-failure probe and `/remember` remain the catch-alls. Never auto-write — logging routine work as wins corrupts the retro substrate (CLAUDE.md "never inflate").

**De-dupe:** read the top entries of `data/accomplishments.md` and skip anything already logged today or already proposed this session.

**Output:** feed candidates into the `#### Accomplishments check` block in Step 6. On Nick's explicit confirmation, append via:

```bash
PYTHONIOENCODING=utf-8 python3 tools/remember_apply.py \
  --note-file <tmpfile> --destinations '[{"type":"accomplishment"}]' --repo-root .
```

Match the file's entry style: a `What landed:` / `Why it matters:` / `Source:` body. The script writes a bare `## YYYY-MM-DD` header with the title on the next line; after writing, merge them into `## YYYY-MM-DD: <title>` to match the existing entries (sibling-format drift observed 2026-06-13). Wait for explicit approval before writing; if Nick declines or edits the wording, honor that verbatim.

### Step 4f: Resolve day context BEFORE any cadence or displacement line (mandatory)

Run `date "+%A %Y-%m-%d"` and classify the day: **working day**, **weekend**, **holiday**
(name it), or **holiday weekend**. Render it on the `**Day context:**` line of the summary.
That line is not optional — a checkout summary without it is incomplete.

**Then apply the gate to everything downstream** — the Progress block, the State Audit, the
"nothing moved outward" style of read, and Tomorrow's Top 3. Every cadence, streak,
overdue-count, and displacement observation carries an implicit "during working days" scope,
because that is the context those patterns were recorded in.

On a non-working day:

- **Report the observation, hold the recommendation.** "A pipeline row's gate date passed and no
  reply came" is a fact and belongs in the log. "You should have spent tonight on it instead" is the
  part that needs the calendar check. Frame it "for Monday" and move on.
- **Never count a non-working day toward a zero-activity streak,** and never read zero outreach
  on a holiday as a signal. Outreach sent on a holiday has near-zero expected value.
- **The daily log is the longitudinal substrate.** If the entry records a holiday as a
  displacement day, `/weekly-review` and `/my-world` will read it back as one. Write the day
  context into the log entry itself, not only into the chat summary.
- `data/goals.md` Search Principle 4 governs the infrastructure-vs-outreach pattern
  specifically. **Read it, do not recall it** — it is a weekday-morning test by construction
  and it states the energy is "a signal, not a guilt trigger."
- Nick's own recorded ordering is evidence about his priorities, not a schedule he owes
  compliance to on his own time.

**Also check the session boundary, not just the calendar boundary.** `/checkout` metrics are
date-bounded, so a session running past midnight is split in half and the entry undercounts it.
Before writing "Completed today: 0", run
`git log --since="<yesterday> 12:00" --pretty="%h %ad %s" --date=format:'%H:%M'` and, if the
commit stream is continuous across midnight, say so in the entry and characterize the whole
block. Origin 2026-09-07: a 22-commit, ~7-hour session was logged as a 10-commit tail.

Origin: `feedback_check_calendar_context_before_surfacing_a_cadence_pattern`, fired 2026-09-06
and again 2026-09-07 (both Labor Day weekend, same failure, second one after the rule was
already written). Promoted to skill tier on the 2nd fire.

### Step 5: Identify Tomorrow's Top 3 (from active_remaining)

From the current Active to-dos in `data/job-todos.md`, rank tomorrow's top 3:

**Step 5a — Pin imminent scheduled events FIRST (mandatory).** Before ranking todos, read `upcoming_scheduled[]` from the Step 1 metrics output. These are interviews/screens/calls parsed from the pipeline **Next-Action** column within the next 3 days — they live in free text, not dated todos, so the todo ranker is blind to them. **Any entry with `is_event: true` is a fixed commitment and outranks every todo: it takes Top-3 slot #1 (earliest date first).** Show it as `[Company] [role] — [event] ([date], [days_until]d)`. A `false` entry (a dated follow-up) is a strong candidate but doesn't auto-pin. If `upcoming_scheduled` is empty, skip and rank from todos only. Origin 2026-06-11: a next-day interview sat in the pipeline Next-Action and was invisible to both /standup and /checkout — see `memory/feedback_surface_scheduled_events_in_ranking.md`.

**Step 5b — Reconcile against recent intel before surfacing any "reach out / apply / warm-intro" todo.** If a candidate todo is an outbound action toward a named entity, check `networking_activity[]` (and the pipeline Next-Action) for that entity's most recent touch. If a touch within ~the last few days already covers it (e.g. the warm-intro message was already sent), DO NOT surface the redundant action — surface the actual next move (await reply / nudge on its gate date) or drop it. Generic-stale pipeline stage ("To Apply") must not override specific-recent networking reality. This is the `[[feedback_reconcile_stale_gate_against_specific_intel]]` pattern at the Top-3 surface. Origin 2026-06-11: surfaced a "reach out to [contact] re [company]" warm-intro action when that reach-out had been logged the day before.

**Ranking logic (todos, after the pins above):**
1. Overdue items first (due date < today, status ≠ Done/Withdrawn)
2. High priority, earliest due date
3. Med priority, earliest due date
4. Low priority, earliest due date (rarely surfaces unless nothing higher)

**Cross-reference with weekly review:**
- Read the most recent Top 5 from `data/weekly-review-log.md` (look for the latest `#### Top 5 Priorities` section).
- For each item in the Top 5 that hasn't been completed (not in the Done section of today's log), annotate it in the top 3 list if it matches — add `(⭐ weekly priority)`.

**Display:** Show 3 items maximum. For each: the task, priority, due date (if set), and a brief "why" (overdue / priority / weekly goal).

### Step 6: Display Checkout Summary

Output in this exact format:

```markdown
## Checkout — [Day, Date spelled out: e.g., Thursday, February 26]

**Day context:** [Working day | Weekend | Holiday — <name> | Holiday weekend] — MANDATORY, never omit
**Today:** [N] done · [N] active · [N] overdue · Active Process: [N] · Eval Backlog: [N]

#### Done Today
- [x] Task 1 (Priority)
- [x] Task 2 (Priority)
(or "> Nothing completed yet today." if zero)

#### Substantive Work (first-class signal — does NOT depend on todo completion)
- **Outputs:** N files across M entities — [entity1: N], [entity2: N]. List paths inline if any entity has 3+ files.
- **Memories captured:** N — [list memory names, or "(none)" if zero]
- **Reflections:** N — [list paths or "(none)"]
- **Inbox entries:** N today
- **Outreach touches (union):** N — [list "Name @ Company (channel)" for each, marking source where useful]

If all five rows are zero, show: "> No substantive artifacts today — light day or maintenance work."

#### Research / Outreach (legacy bucket — keep if filled)
- [Research dossier updates if any in `research_completed_today`]
- [Outreach-log specifics if useful detail beyond the Substantive Work block]

#### System Changes
- [Changelog entry — omit section entirely if none]

#### State Audit (diagnose, don't close)
- [Stuck Claude tasks, long-overdue todos, stalled pipeline, overdue networking follow-ups — see Step 4c. Omit section entirely if all audits clean.]

#### Granola Debrief Cascade
- [local_time] — [meeting title] → `/debrief` (or `tools/granola_cli.py pull <id>`)
(Un-debriefed non-therapy calls from the last 24h, per Step 4d. Propose only. Omit section entirely if all debriefed or none found.)

#### Progress
Streak: **N days** | This week: **N** | Velocity: **N.N/day** | Overdue: **↑/→/↓**

> Note: "Done" count reflects formal todo completions only. Substantive Work above is the real volume signal — a heavy work-up day with low "Done" count + high Outputs/Memories/Outreach is a high-output day, not a low-output day. Don't conflate the two.

---

#### Tomorrow's Top 3
1. **[Task]** — [Priority | Due: date | why: overdue / weekly priority / etc.]
2. **[Task]** — [Priority | Due: date]
3. **[Task]** — [Priority]

---

> Private backup: [pushed (`<short SHA>`) / up to date / skipped (`<reason>`)] — see Step 7.

#### Accomplishments check
[0-2 milestone candidates from Step 4e. For each: the win in one line + the evidence behind it.]
[If a candidate clears the bar:]
Today may hold a milestone win:
- **[Win]** — [evidence: the artifacts / system change / reflection behind it]

Milestone-level (retro- or LinkedIn-worthy), or just good daily work? If it clears the bar I'll log it to `accomplishments.md`. (Default: none.)
[If no candidate clears the bar: omit this section entirely — most days have no milestone.]

Anything to capture? Run `/remember "..."` for insights, contacts, or decisions from today.

**Silent-failure probe:** Did anything happen today the system didn't catch? A call that never got logged, a decision made in your head, a setback, an idea you didn't write down? If so, let's route it now.
```

**On the silent-failure probe (Step 6 close):** this is an open-ended, reflective human prompt, not another automated scan. Step 4c audits *known* surfaces (stuck tasks, overdue todos, stalled pipeline); this probe catches what no structured audit can see because the system was never told about it. Ask it plainly, then stop and let Nick answer. Don't pre-fill guesses, don't turn it into a checklist. If Nick names something, route it via `/remember`, the relevant write script, or the right skill.

**On the accomplishments check (Step 4e / Step 6):** evidence-grounded by design (Nick's call, 2026-06-13) — checkout proposes from the day's real artifacts so a win isn't lost to faulty recall. Distinct from the silent-failure probe in valence (wins, not gaps) and method (grounded proposal, not open-ended). But the milestone bar is strict and ZERO candidates is the common, correct output: do NOT manufacture a win to fill the section, and never auto-log. Origin: 2026-06-13 — the commonplace-book launch was a genuine compounding win that only got captured because Nick volunteered it after the silent-failure probe; this step makes that capture structural without turning every build into an "accomplishment." Composes with the `accomplishments.md` boundary (milestone-level process wins, not daily tasks) and CLAUDE.md "never inflate."

### Step 7: Back up private data (closing action — mandatory, non-blocking)

Run this once all writes are done (after the daily log in Step 3 and the auto-closes in Step 4b) and just before rendering the Step 6 summary, so its result can fill the `Private backup:` line. This is the end-of-day private snapshot.

```bash
bash tools/backup-data.sh
```

What it does: force-adds the private path-set (`data/ output/ coaching/ memory/ inbox/ _archive/` + the tracked private `framework/*.md` docs + the 2 sidebiz tools), commits (`--allow-empty`), and pushes a fast-forward to the **private backup repo via an overlay git-dir outside the working tree**. **It does NOT touch the public repo.** Safe to run multiple times a day — each push is an idempotent fast-forward. (Concrete repo name, account, and overlay path live in the gitignored `memory/reference_private_data_backup_mechanism.md`; `backup-data.sh` reads them itself, so nothing here needs them inline.)

**Non-blocking / graceful (mandatory):** a backup failure must never abort checkout. Read the tail of the output and set the `Private backup:` line in the Step 6 summary accordingly. Note git's push format is `<old>..<new>  master -> master` (the SHAs come *before* `master`, e.g. `   42ca07c..202cb8b  master -> master`):
- A range `<old>..<new>` is present → `pushed (`<new short SHA>`)`. The new SHA is the part after `..` (since `backup-data.sh` commits with `--allow-empty`, this is the normal/expected case on every run).
- `Everything up-to-date` (no range) → `up to date`.
- `! [rejected]`, `fatal:`, network/auth error, or non-zero exit → `skipped (<one-line reason>)`, and add: run `bash tools/backup-data.sh` later. Do NOT retry, do NOT block, do NOT touch the public repo to "fix" it.

Origin: wired into `/checkout` 2026-06-11, replacing the manual-only backup. The overlay git-dir is the canonical private backup (per the 2026-06-11 reconcile); `backup-data.sh` is its driver. This makes the end-of-day private snapshot automatic.

## Edge Cases

- **job-todos.md missing or empty:** Note "No to-dos tracked yet" — skip snapshot sections. Still write a minimal log entry and display the checkout summary.
- **No completions today:** Show "Nothing completed yet today." — still write the log entry. This is valid data (streak resets if this was the only entry).
- **Existing entry for today:** Replace it in place — do not append a duplicate. This supports running `/checkout` multiple times in a day (last run wins).
- **No weekly-review-log.md:** Skip the weekly priority cross-reference silently. Display Tomorrow's Top 3 based on todo priority/date only.
- **No active to-dos:** Display "No active to-dos — run `/todo add` to capture tomorrow's work" instead of the Top 3 section.
- **All files missing:** Display a setup message: "No data files found yet. Start with `/import-cv` to populate your profile, then `/pipe add` to track your first application."
- **Daily log file doesn't exist:** Create it with the standard header (see Step 4) before writing the first entry.
- **Backup fails (offline / push rejected / auth):** Never block checkout. Set the `Private backup:` line to `skipped (<reason>)` and finish the summary normally (see Step 7).
