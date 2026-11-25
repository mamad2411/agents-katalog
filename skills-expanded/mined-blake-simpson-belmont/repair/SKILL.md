---
name: repair
description: Repair a PROGRESS.md whose task states no longer parse — unreadable markers, task lines outside every milestone, tasks filed under the wrong milestone. Uses commit evidence and the current code, never memory.
alwaysApply: false
---

# Belmont: Repair

You are the repair reviewer. A PROGRESS.md has entries Belmont cannot act on, and
your job is to work out what each one should say — **from the repository, not
from anyone's recollection**.

This skill runs in two situations. Read the next two sections and decide which
one you are in before doing anything else.

## Mode A — the CLI called you (proposal mode)

If the prompt you were invoked with contains a **`REPAIR BRIEF`** block:

- The mechanical tier has already run. Anything the commit log settled has
  already been applied and is not in your brief.
- **Do not edit `PROGRESS.md`, or any other file.** Investigate, then write the
  JSON proposal to the path the brief names. The CLI validates every action,
  applies what passes, and shows the user each edit before making it.
- The brief carries the full rules and the exact JSON shape. Follow them; they
  are the same ones repeated under *How to decide* below.

## Mode B — a person typed `/belmont:repair` (interactive mode)

Run the two tiers yourself, in this order. **Do not skip tier 1** — it costs
nothing and answers most of the findings without you reading a line of code.

## Feature Selection

Belmont organizes work into **features** — each feature gets its own directory under `.belmont/features/<slug>/` with its own PRD, PROGRESS, TECH_PLAN, and MILESTONE files.

### Select the Active Feature

1. List all feature directories under `.belmont/features/`
2. If features exist: read each feature's `PRD.md` for its name and status, then ask which feature to repair, or auto-select the only one
3. If no features exist: tell the user to run `/belmont:product-plan` to create their first feature, then stop
4. Set the **base path** to `.belmont/features/<selected-slug>/`

### Base Path Convention

Once the base path is resolved, use `{base}` as shorthand:
- `{base}/PRD.md` — the feature PRD
- `{base}/PROGRESS.md` — the feature progress tracker
- `{base}/TECH_PLAN.md` — the feature tech plan
- `{base}/MILESTONE.md` — the active milestone file
- `{base}/MILESTONE-*.done.md` — archived milestones
- `{base}/NOTES.md` — learnings and discoveries from previous sessions

**Master files** (always at `.belmont/` root):
- `.belmont/PR_FAQ.md` — strategic PR/FAQ document
- `.belmont/PRD.md` — master PRD (feature catalog)
- `.belmont/PROGRESS.md` — master progress tracking (feature summary table)
- `.belmont/TECH_PLAN.md` — master tech plan (cross-cutting architecture)

### Tier 1 — the CLI, at zero token cost

```bash
belmont repair --feature <slug> --dry-run --format json
```

That reports every finding with its line number, the marker as written, and
whether a commit names the task. Nothing is written.

Then apply what the commit log settles:

```bash
belmont repair --feature <slug> --mechanical-only
```

This marks `[x]` — and only `[x]` — where a commit names the task ID. It prints
the commit it relied on for each change.

If the CLI is not installed, do the same by hand: read
`.belmont/features/<slug>/PROGRESS.md` and find the task lines Belmont cannot
read (see *What counts as a finding*). To check an ID, match the commit log with
a **word boundary** around it and search **HEAD's history only** —

```bash
git log --format='%H %s' | grep -E '(^|[^A-Za-z0-9-])P1-M2-3([^A-Za-z0-9-]|$)'
```

Not `--grep P1-M2-3`, which is an unanchored substring match and credits `P1-M2-3`
with a commit for `P1-M2-30`; and not `--all`, which searches dead branches. If
the newest matching commit is a revert, the task is **not** settled.

**And check no sibling feature claims the same ID first.** Task IDs are
feature-local — `P1-M1-1` exists in essentially every feature — while the commit
log is not, so a bare ID match can be about entirely different work:

```bash
grep -l 'P1-M2-3:' .belmont/features/*/PROGRESS.md
```

More than one file means the commit proves nothing about *this* feature. Read the
code instead; do not mark it `[x]` on that commit.

### Tier 2 — read the survivors against the code

For everything still outstanding, follow *How to decide* below. Present your
conclusions to the user **as a list, with the evidence for each** — name the
file, route or test you looked at, not just the verdict — and ask them to
confirm before anything is written.

Then write the confirmed ones as a proposal and hand it back to the CLI:

```bash
cat > /tmp/belmont-repair.json <<'JSON'
{"repairs":[
  {"line": 14, "task_id": "P1-M2-3", "action": "withdraw", "reason": "the /admin/reports route was removed in M3; nothing references it"}
]}
JSON
belmont repair --feature <slug> --apply-proposal /tmp/belmont-repair.json
```

**Use that rather than editing `PROGRESS.md` yourself.** It is the same
validation the CLI-dispatched path goes through, so the rules under *Hard
limits* are enforced rather than merely remembered, and every refusal is
explained. Without `--yes` it walks you through each edit for confirmation.
The `line` values are the ones tier 1 reported.

Only edit the file by hand if the CLI is not installed — and then obey every
rule under *Hard limits* yourself.

Finish by running `belmont validate --feature <slug>` and reporting the result.

## What counts as a finding

Three things Belmont cannot act on:

| | What it looks like | Why Belmont cannot act on it |
|---|---|---|
| Unreadable marker | `- [?] P1-M2-3: …` — anything outside `[ ] [>] [x] [v] [!] [-]` | excluded from every count, never scheduled, and its milestone can never read complete |
| Outside every milestone | a task line below a column-zero `## ` heading | counted by nothing, rendered nowhere, never scheduled |
| Filed under the wrong milestone | `P1-M3-9` sitting under `### M2:` | a dependency-graph lie: the parallel scheduler believes the wrong thing about what blocks what |

…and one **audit**, reported separately under `verified_without_evidence`:

| | What it looks like | Why it is worth a look |
|---|---|---|
| Verified with nothing behind it | `- [v] P1-M2-3: …` and no commit in the repository names `P1-M2-3` | nothing audits this. The commit-evidence guard only compares one phase's before and after, so a `[v]` already on disk when a run started was never checked by anything |

Nothing else. A task that is merely old, or wrong, or badly worded is not a
repair finding.

### Reading the evidence on a finding

| Field | What it means |
|---|---|
| `checked: false` | the commit log could not be read at all — weigh the code alone |
| `found: true` | a commit names this task ID |
| `ambiguous: true` | …but another feature's PROGRESS.md claims the same ID. Task IDs are feature-local and the commit log is not, so **treat it as no evidence** and read the code. It is why the finding reached you with a SHA attached instead of being settled without you |
| `also_verified_without_evidence: true` | the line is **both** the parse problem named by `rule` **and** a verified marker no commit proves. You get one action for it: decide the parse problem, and say in your reason whether the verified claim still stands |

## How to decide

**Evidence, never memory.** Do not ask the user "did this ship?", "was this
withdrawn?", "was this blocked?" A damaged file carries dozens of these at once
and nobody remembers what a marker meant six weeks ago — you will get "I don't
know" followed by a guess, which is precisely the failure that put the file in
this state. Ask the repository instead.

For each finding, read the task text, then look for what it names in the
**current** code: the route, component, table, endpoint, flag, migration, test.

| What you find | Action |
|---|---|
| The thing exists and does what the task describes | `set_marker` `"x"` |
| The thing does not exist and nothing supersedes it | `set_marker` `" "` |
| Something replaced it, it was folded into other work, or the feature it belonged to is gone | `withdraw` (+ reason) |
| It is waiting on something you can name | `set_marker` `"!"` |
| It is not a task at all — a retro bullet, a quoted log line, a table row shaped like a checkbox | `leave` |
| It is a real task sitting in the wrong place | `move_milestone` (see below) |
| The code does not settle it | `escalate` |

`escalate` is a real answer and is always better than a marker you cannot
justify. A wrong state here is the exact bug this command exists to fix.

### Where a misplaced task goes

This is the step people loop on, so it has a rule.

A task **outside every milestone**, or one **filed under the wrong milestone**,
needs somewhere to land:

- **Its ID names a milestone the file already has** → `move_milestone` to that
  milestone. Nothing else to decide.
- **Its ID names no milestone, or names one this file does not have** — a
  follow-up produced by a cross-cutting sweep is the usual case, and an ID saying
  `M9` in a plan that stops at M5 is the other. Repair cannot create a milestone,
  so such an ID settles nothing. It still needs a destination. Do **not** escalate to
  `/belmont:tech-plan` expecting a new milestone: that skill forbids creating one
  for follow-ups, so the task returns here still counted by nothing. File it
  under the **highest-numbered existing milestone whose work it touches** — the
  last one whose outputs the fix depends on — or the final milestone in the plan
  when it is genuinely global. Say which milestones it touches in your reason.
- **Only when you cannot tell what it touches** → `escalate`.

Filing it under the *earliest* milestone it touches instead re-opens work that
later milestones already built on — the same dependency-graph lie the
milestone-immutability rule bans a "polish from M\<N>" milestone for.

**A commit naming the task ID proves the work happened.** That is what tier 1
already used. It cannot prove the reverse — no commit means no commit, not "not
done" — so a task with no commit still needs the code read.

### The `verified_without_evidence` audit decides differently

These lines parse; only the *claim* is in question. Look for the work, then:

| What you find | Action |
|---|---|
| The work is there and the code or a test plainly shows it — the commit convention just was not followed | `leave` |
| The work is there but nothing shows it was verified | `set_marker` `"x"` |
| The work is not there at all | `set_marker` `" "` |
| You cannot tell | `escalate` |

`leave` is a **common and correct** answer here. Documentation-only and
configuration-only tasks routinely leave no commit naming them, and treating a
missing commit as proof of missing work would re-open finished work — which is
the failure this whole command exists to prevent, pointed the other way.

Demoting to `[x]` is the useful move when the claim does not hold: `belmont
reverify` then re-earns the `[v]` under its own evidence contract. Repair still
never writes a `[v]`.

## Hard limits

In Mode A the CLI enforces every one of these and refuses a proposal that breaks
them. In Mode B nothing enforces them but you, and they matter more, not less.

- **Never write `[v]`.** Repair stops at `[x]`. The verified flip has its own
  evidence contract and `belmont reverify` is the only thing allowed to write
  it. Tell the user to run that afterwards.
- **Withdrawal is `[-]` plus the reason in `## Decisions Log`.** A marker cannot
  carry why. Never express withdrawal by deleting the line: a deletion does not
  survive a sibling worktree merge, so the task comes back as outstanding work
  and the next person deletes it again.
- **A `[v]` task cannot be withdrawn in one step.** Nothing in Belmont writes
  that marker back — `belmont reverify` only ever promotes `[x]` — so demote it
  with `set_marker` `"x"` first. Withdrawing from there is unrestricted.
- **Never create, rename or remove a `### M<n>:` milestone.** That is
  `/belmont:tech-plan`'s job alone. Moving a task between milestones that
  already exist is fine here — repair runs outside the auto loop, where the
  scope guard would revert it — but the destination must already exist and must
  not already hold that task ID.
- **A task is its bullet PLUS its indented body — move both.** The
  `**Verification**` / `**Evidence**` lines under a task belong to it. Move the
  bullet alone and they stay behind and re-attach to the task now above them,
  which is then credited with evidence it never earned while the task you moved
  asserts done with nothing behind it. Nothing catches this: the file still
  parses, the count is unchanged, `belmont validate` still reports clean. The CLI
  moves the whole block for you — this bullet is for the hand-edit path, where
  nothing does.
- **Only touch the lines that were flagged.** Every other task in the file is
  none of this skill's business, however wrong it looks. A nested sub-bullet is a
  task too: when you move its parent, it travels with it — that is correct, but
  say so in your report rather than letting it move unremarked.
- **Never change a task's text**, only its marker or its milestone. If the text
  is wrong, say so in your summary and leave it.

## Report

State, in this order:

1. What the commit log settled, and the commit each conclusion rests on.
2. What you read the code for, with the evidence per finding — name the file or
   route you looked at, not just the verdict.
3. Anything escalated, and precisely what you could not determine.
4. `belmont validate --feature <slug>` output.
5. If any task is now `[x]`: `belmont reverify --feature <slug>` earns the `[v]`.

Do not report a file as repaired while findings remain escalated. Say how many
are left.
