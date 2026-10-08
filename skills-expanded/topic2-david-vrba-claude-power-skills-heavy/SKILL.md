---
name: heavy
description: Launch a pre-engineered "heavy prompt" from your local library in the current interactive session — big self-contained research/build/optimize jobs that write line-addressable structured output. /heavy lists the library; /heavy NN launches or resumes run NN.
---

# Heavy-prompt launcher

Runs one big self-contained prompt from your `heavy/library/` in **this interactive session** (so it
uses your interactive subscription, not metered/headless API billing). A heavy prompt is meant to be
launched and left — so once a prompt is running, **do not stop to ask the user anything.**

The library, outputs, and conventions live in your project repo under `heavy/` (you can also keep it
at `~/.claude/heavy/`). Read `heavy/README.md` once for the full model. Paths below are relative to
your repo root (the current working directory):

- `heavy/library/` — the heavy prompts (`NN-slug.md`) + `INDEX.md` + `_TEMPLATE.md`
- `heavy/output/` — one run folder per launch, plus `output/INDEX.md`
- `heavy/state/runs.ndjson` — append-only event log of launches/resumes/completions

The argument `$ARGUMENTS` is the heavy-prompt number `NN` (may be empty).

---

## Step 1 — Route on the argument

- **No argument:** read `heavy/library/INDEX.md`, print the catalog (ID, Title, Goal, Cost), and
  ask the user which to run (this is the ONLY place a question is allowed — the human is present
  at launch). Then stop and wait. Do not auto-pick.
- **`NN` given:** proceed unattended through the steps below and **never** use `AskUserQuestion`
  again for the rest of the run.

## Step 2 — Load the prompt

- Resolve the library file: `heavy/library/NN-*.md` (the file whose stem starts with `NN-`).
  If none matches, list the catalog and stop.
- Read its frontmatter: `id`, `output_dir`, `phases`, `subagents`, `websearch_max`, `est_cost`.
- If `subagents: false` (the default), you MUST do all work yourself in this session — do **not**
  spawn the Agent tool or any sub-workflow.

## Step 3 — Resolve the run folder (resume or init)

- Run folder is the prompt's `output_dir` (e.g. `heavy/output/01-some-study/`).
- **If `output_dir/STATUS.json` exists and `status == "in_progress"`:** this is a RESUME.
  Read it, note `completed_steps` and `current_step`, append a `resume` event to
  `heavy/state/runs.ndjson`, and continue execution skipping completed steps. Reuse this same
  folder — never create a new dated one.
- **Else (new run):** create `output_dir`, write the initial `STATUS.json`:
  ```json
  {
    "prompt_id": "NN-slug",
    "started": "<ISO8601>",
    "phases": [...from frontmatter...],
    "current_phase_index": 0,
    "current_step": null,
    "completed_steps": [],
    "last_commit": null,
    "lock": {"started": "<ISO8601>"},
    "status": "in_progress"
  }
  ```
  Create `00-summary.md` with the opening ```yaml``` block (`status: in_progress`), append a
  `launch` event to `heavy/state/runs.ndjson`, add an `in_progress` row to
  `heavy/output/INDEX.md`, then `git add heavy/ && git commit` (the commit is the first checkpoint).
  (Get the timestamp from `date -u +%Y-%m-%dT%H:%M:%SZ` — do not invent times.)

  **Never `git add -A`** — other concurrent work may have unrelated uncommitted changes, and `-A`
  would sweep them into the heavy commit. Everything a run writes lives under `heavy/`, so
  `git add heavy/` is the correct, complete, scoped stage.

## Step 4 — Execute the phases

Follow the prompt body's PHASES/STEPS in order. For **each step**:
1. **Advance before work:** set `current_step` and (if entering a new phase) bump
   `current_phase_index` in `STATUS.json`.
2. **Do the step**, writing output as **anchored, append-only** sections
   (`<!-- SEC:id -->` … `<!-- /SEC:id -->`) into the prompt's specified files. Never rewrite a
   completed earlier section; only append new ones (re-running a partial step may rewrite that
   step's own anchored block).
3. **Commit after:** add the step id to `completed_steps`, set `last_commit`, then
   `git add heavy/ && git commit -m "heavy(NN): <step id>"` (scoped — never `-A`). This is the durable checkpoint.
4. At the **end of each phase**, regenerate `MAP.md` (table: `| id | title | file | lines | ~tokens | one-liner |`)
   and append a `phase_done` event to `heavy/state/runs.ndjson`.

Discipline while running:
- **Never** use `AskUserQuestion`. When a decision is unclear, take the documented default and
  record it under `<!-- SEC:assumptions -->` in `00-summary.md`.
- **WebSearch ≤ `websearch_max`** for the whole run.
- Respect the prompt's GUARDRAILS (security, low-risk-edits-only, verify external facts).
- Run `/compact` at ~70% context. If the session is cut off, the next `/heavy NN` resumes from
  `STATUS.json`.

## Step 5 — Finish cleanly

When the prompt's DONE criteria are met:
- Finalize `00-summary.md` (set yaml `status: done`), regenerate `MAP.md`.
- Set `STATUS.json` `status: "done"`, clear `lock`.
- Update the run's row in `heavy/output/INDEX.md` to `done` with a one-line summary + folder link.
- Append a `done` event to `heavy/state/runs.ndjson`.
- Final `git add heavy/ && git commit -m "heavy(NN): done"` (scoped — never `-A`).
- Print a short banner: prompt id, status, output folder, top findings, how many commits.
- **Stop.** A heavy run is one bounded job — do not loop or relaunch.

## Notes

- This is launched in an interactive session on purpose (your interactive subscription, not metered
  API billing). It is human-launched every time — do not schedule it to fake a human.
- All run state lives under the run folder (`STATUS.json`) and `heavy/state/` — there is no other
  state store to keep in sync.
