---
name: feature-list
description: List the features tracked under features/ in the current repo and how far each has travelled through the storm → design → plan → implement chain, as a table in reverse date order. Use when the user asks what features are open, what is in flight, where a feature got to, which features still need designing/planning/implementing, or simply "list the features". Takes one optional argument, which may only be `all`- with no argument it lists only open features (those whose implementation is not complete); with `all` it lists every feature, finished ones included. Per-stage status is read from each feature's tracker (data-stage / data-state) corroborated by the stage .md files on disk, and in-progress implementations are detected from the plan-stage commits on the current branch. Strictly read-only - never creates folders, never seeds or edits trackers, never writes, commits, or pushes anything, and never calls feature-resolve.
user-invocable: true
disable-model-invocation: false
argument-hint: "all" to include completed features, or omit to list only open ones
allowed-tools: Read, Grep, Glob, Bash(ls *), Bash(find *), Bash(test *), Bash(pwd), Bash(git log *), Bash(git rev-parse *), Bash(basename *)
---

# feature-list — Report on the features tracked in this repo

You are running the `feature-list` skill. Your job is to report, as a single table in **reverse date order** (newest activity first), which features exist under `features/` in the current repo and which chain stages each of them has completed.

**Terminology (plugin-wide).** A **step** is a numbered step of this skill's own procedure (the `## Step …` headings below). A **stage** here always means a **chain stage** — one of `storm → design → plan → implement`. The plan stages *inside* an implementation plan (`Stage 1`, `Stage 2`, …) appear only in Step 3's in-progress detection, and are never a column of the table.

This skill is a **reporter, not a participant**. It is strictly read-only: it never creates a feature folder, never seeds or edits a tracker, never writes a stage file, and never commits or pushes. In particular it locates feature folders by read-only globbing and **deliberately does not call `feature-resolve`** — the resolver creates folders and seeds trackers as a side effect, which would make merely listing features mutate the repo. That also means there is no proactive-invocation confirmation step: with nothing written and nothing spent beyond a few file reads, a gate would cost a round-trip and buy nothing.

This skill has six steps (Steps 1–6). Execute them in order.

## Step 1 — Parse and validate `$ARGUMENTS`

The skill takes **one optional argument, and its only legal value is `all`**.

- `$ARGUMENTS` empty (or whitespace only) → `scope = open`. List only features whose implementation is not complete.
- `$ARGUMENTS` is `all` after trimming, compared case-insensitively → `scope = all`. List every feature.
- Anything else → stop immediately with exactly one line and list nothing:

  ```
  feature-list: unknown argument "<what they typed>" — the only accepted argument is `all` (omit it to list open features only).
  ```

  Do not guess an intent, do not treat it as a version or a search term, and do not fall back to a default scope.

## Step 2 — Find the feature folders (read-only)

1. Establish the project root: `pwd` (and `git rev-parse --show-toplevel` when inside a git work tree — prefer the repo root so the report is the same from any subdirectory).
2. If `features/` does not exist (`test -d features`), stop with one line: `No features found — this repo has no features/ folder yet. Start one with /feature-storm or /feature-design.`
3. Enumerate feature folders, exactly as the rest of the plugin names them:

   ```bash
   find features -maxdepth 1 -type d -iname 'feature-v[0-9]*-*'
   ```

   For each match parse `N` (the integer version — **numeric** compare, so `v10` > `v9`) and `description` (everything after `feature-v<N>-`, verbatim). If there are no matches, stop with the same "no features" line as above.
4. For each folder, list its files (`ls`) and record which stage files are present. Stage files are named `feature-<stage>-v<N>-<description>.md` — the pattern `feature-resolve` mints — for `stage` in `storm`, `design`, `plan`. There is no implement stage file today (`/feature-implement` does not emit one), so never infer implementation from a file's absence. Record the tracker path `feature-v<N>-tracker.html` if it exists.

Never create anything in this step: no `mkdir`, no template copy, no tracker seeding. A missing `features/`, a missing tracker, or an empty folder is a finding to report, not a gap to fill.

## Step 3 — Resolve each feature's per-stage status

For every feature, resolve one status per stage from two independent signals.

**Signal A — the tracker (authoritative).** Read `feature-v<N>-tracker.html` and find the four progress-bar entries:

```
data-stage="storm"      data-state="pending|complete"
data-stage="design"     data-state="pending|complete"
data-stage="plan"       data-state="pending|complete"
data-stage="implement"  data-state="pending|complete"
```

Each stage is flipped to `data-state="complete"` by the skill that owns it, and there is no in-flight state — a stage is either pending or complete. Ignore the copies of these attributes that appear inside the template's top-of-file documentation comment; only the live `<li class="step" …>` elements count.

**Signal B — the filesystem.** The stage `.md` files found in Step 2 (`storm`, `design`, `plan` only).

Combine them:

| Situation | Status |
|---|---|
| Tracker says `complete` (and, for storm/design/plan, the stage file exists) | **complete** |
| Stage file exists but the tracker still says `pending`, or the tracker is missing / still holds literal `{{…}}` tokens | **complete†** — the work landed but the tracker was never flipped; flag with `†` |
| Tracker says `complete` but the stage file is absent (storm/design/plan) | **complete†** — flag the same way; the tracker is authoritative, the file may have been moved or deleted |
| Neither signal | **not started**, except: storm counts as **skipped** (not pending) whenever a later stage has completed, since `/feature-storm` is optional |

**Implement is the special case.** There is no implement stage file, so completion comes from the tracker alone, and partial progress comes from git. When the tracker does not say `complete`, check the current branch for this feature's plan-stage commits:

```bash
git log --oneline -F --grep="(plan v<N>): Stage "
```

(`-F` matches the pattern literally — without it the parentheses would be read as a regex group.)

- Commits found → **in progress**, reported with the highest plan-stage number seen (e.g. `in progress — Stage 3`). `/feature-implement` resumes at the lowest *uncommitted* stage, which a parallel batch that landed only some of its stages can leave below this number — so report the highest, never infer the next.
- No commits and no tracker completion → **not started**.
- Not a git work tree, or git fails → treat as **not started** and say so once in the closing note rather than failing the run.

## Step 4 — Date each feature and sort

Each tracker panel carries a timestamp chip written by the stage that filled it, in the shape `Updated <YYYY-MM-DD HH:MM UTC>` (panels map to stages as brainstorming → storm, design → design, plan → plan, implementation → implement). Unfilled panels read `Awaiting /feature-<stage>` — ignore those.

- **`last_activity`** = the newest `Updated …` timestamp in the feature's tracker.
- If no timestamp can be parsed (tracker missing, unseeded, or hand-edited), fall back in this order: the last commit touching the folder (`git log -1 --format=%cI -- features/feature-v<N>-<description>`), then the newest file modification time in the folder, then `unknown`.

Sort **descending by `last_activity`** — newest first, which is the required reverse date order. Break ties on version descending. Features whose date is `unknown` go last, ordered among themselves by version descending, and show `—` in the date column.

## Step 5 — Select and render

Filter by the Step 1 scope:

- `scope = open` → keep only features whose implement stage is **not** complete (that is: not started, in progress, or complete† where the completion signal is missing). These are the features with work left.
- `scope = all` → keep every feature.

Render exactly one markdown table, in the sorted order:

```
**Open features — 3 of 7** (features/ in <repo root>)

| Feature | Storm | Design | Plan | Implement | Last activity | Next step |
|---|---|---|---|---|---|---|
| v7 — Payments-checkout | ✅ | ✅ | ✅ | 🔄 Stage 2 | 2026-07-29 14:02 UTC | /feature-implement (highest committed: Stage 2) |
| v6 — Add-Reminders | – | ✅ | ⬜ | ⬜ | 2026-07-24 09:15 UTC | /feature-plan |
| v4 — Export-CSV | ✅ | ✅ | ✅ | ⬜ | 2026-07-11 17:40 UTC | /feature-implement |

✅ complete · 🔄 in progress · ⬜ not started · – storm skipped · † stage file and tracker disagree
```

Rules for the table:

- **Header line** — `**Open features — <shown> of <total>**` for `scope = open`, `**All features — <total>**` for `scope = all`.
- **Feature** — `v<N> — <description>`, description verbatim from the folder name (hyphens kept, so it stays greppable).
- **Stage cells** — the Step 3 statuses as the symbols in the legend, with `†` appended where the signals disagreed. The implement cell carries the plan-stage number when in progress.
- **Last activity** — the Step 4 timestamp, or `—` when unknown.
- **Next step** — the slash command that advances the feature: `/feature-design` when design is missing, `/feature-plan` when the design is done and the plan is not, `/feature-implement` (adding `(highest committed: Stage <M>)` when partly implemented) when the plan is done. For a fully implemented feature in `all` scope, write `Done`.
- **Legend** — print it once, directly under the table, and only for the symbols that actually appear.
- Emit only the header line, the table, the legend, and (when warranted) the closing note. No per-feature prose, no file dumps, no summaries of what each feature does.

Close with a note **only if** something needs saying — e.g. `† v6: plan file present but the tracker was never flipped.`, `Not a git work tree — in-progress implementations could not be detected.`, or, when `scope = open` found nothing, `All 7 features are fully implemented — run /feature-list all to see them.`

## Step 6 — Handle the empty cases

- No `features/` folder, or no `feature-v<N>-*` folders → the single "no features" line from Step 2. Nothing else.
- `scope = open` with every feature implemented → print no table; print the "all implemented" line from Step 5 instead.
- A folder that matches the naming pattern but contains no stage files and no tracker → still list it, with every stage `⬜` and `Next step` = `/feature-design` (or `/feature-storm` if the description suggests it is still unshaped). A seeded-but-empty folder is exactly the kind of stranded state worth surfacing.

## Constraints (non-negotiable)

- **Never write anything.** No file creation, no edits, no `mkdir`, no template copy, no tracker seeding, no commits, no pushes. If the report would be nicer with a repaired tracker, say so — do not repair it.
- **Never call `feature-resolve`** (or any other skill via the `Skill` tool). The resolver creates folders and seeds trackers; listing must not mutate. Locate folders by globbing, exactly as `evals-e2e-run` does and for the same reason.
- **Never call `lessons-capture`.** This is a read-only reporter, like the two eval skills; there is no run to reflect on.
- **`all` is the only argument.** Anything else stops the skill with the Step 1 error line — never a best-effort guess.
- **Report what is on disk.** Never infer a stage from the feature's description, from conversation history, or from what "should" have happened. Every cell traces to a tracker attribute, a stage file, or a commit.
- **Integer versions, numeric compare.** `v10` sorts above `v9`, never lexicographically. Never invent minor versions.
- **Degrade, don't fail.** A missing tracker, an unparseable timestamp, or an absent git repo downgrades a cell or a date to its fallback and earns one closing note — it never aborts the report.
