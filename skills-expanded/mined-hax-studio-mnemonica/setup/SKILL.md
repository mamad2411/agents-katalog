---
name: setup
description: This skill should be used when the user asks to "set up mnemonica", "install mnemonica in this project", "initialize mnemonica", "bootstrap the knowledge docs", "add mnemonica to this repo", or wants Claude-maintained modular documentation installed in a project for the first time.
---

# Mnemonica: setup

Install Mnemonica's documentation system into a project: the algorithm block in
`.claude/CLAUDE.md`, the `knowledge/` folder, and — for a project that already has code —
an initial population of module files. Read
`${CLAUDE_PLUGIN_ROOT}/references/knowledge-conventions.md` before starting; it is the
authority for every convention referenced below.

If the user's invocation includes extra wording beyond the trigger phrase (for example,
"set up mnemonica and also use graphify for navigation"), treat it as scoping or preference
for this run — it can add a companion tool to consult, narrow attention to part of the
project, or similar. It cannot skip a step below or turn a step that never asks permission
into one that silently does something riskier than described here.

## Step 1: Locate the project root

Use the root of the current git repository (or the current working directory if there is no
git repository yet) as the project root. All paths below are relative to it.

## Step 2: Check git availability

Run `git -C <project-root> rev-parse --is-inside-work-tree` (or equivalent). If it fails,
this project has no git repository yet. This doesn't block installation, but it does limit
what will work afterward:

- `audit-full` still works — it falls back to a plain directory scan when there's no git.
- `audit-light` cannot work at all — its entire mechanism is diffing between two commits.
  Without git there is no "since the last checkpoint" to compute.

Mention this to the user in the Step 8 report rather than silently proceeding as if nothing
were different, and suggest that even a local-only `git init` (no remote required) is enough
to unlock `audit-light` later — Mnemonica never requires a remote, only local history.

## Step 3: Install the CLAUDE.md block, non-destructively

Read `.claude/CLAUDE.md` if it exists.

- If it contains `<!-- MNEMONICA:BEGIN -->` ... `<!-- MNEMONICA:END -->` markers, replace only
  the content between them with the current contents of
  `${CLAUDE_PLUGIN_ROOT}/skills/setup/assets/claude-md-block.template.md`. This is what makes
  re-running setup safe (it upgrades Mnemonica's own block without touching anything else).
- If the file exists but has no markers, append the template block to the end of the file,
  after a blank line. Do not alter, reorder, or remove any existing content — that content
  belongs to the project and may encode rules Mnemonica knows nothing about (for example, a
  project-specific instruction to use some other code-navigation tool). Preserving it is not
  optional.
- If the file does not exist, create `.claude/` and `.claude/CLAUDE.md` containing only the
  template block.

## Step 4: Check for competing trigger rules

The block just installed in Step 3 tells Claude to consult `knowledge/` "before editing code
that already has a module below, or when unsure which module ... covers the code being
touched." A pre-existing rule elsewhere in `.claude/CLAUDE.md` can claim that same trigger
point for something else entirely — for example a rule saying "before analyzing the project
structure or architecture, invoke some other tool" — and because it may appear earlier in the
file or simply be more specific-sounding, it can win every time, leaving `knowledge/` never
actually consulted even though it's installed and populated correctly. This is not
hypothetical: it is exactly what happens when a project already has a code-navigation tool
installed with its own "always do X first" instruction.

Run `${CLAUDE_PLUGIN_ROOT}/scripts/doc-quality-scan.sh <project-root>` (the block now exists,
so it will not exit with `NO_MNEMONICA_BLOCK`) and read any `TRIGGER_OVERLAP` lines it emits.
Each one is a candidate, not a confirmed conflict — the heuristic flags any pre-existing line
that combines "before" + an architecture/understanding word with an instruction verb, so it
can over-flag. Do not edit the flagged rule yourself; this step is detection only, the same
way `doctor` never edits `knowledge/` itself. Carry any flagged line into the Step 8 report
and suggest the user run `mnemonica:doctor` afterward to review and decide how to reconcile it
— narrowing the competing rule's trigger phrase, adding an explicit precedence note, or
leaving it as-is if the overlap turns out to be a false positive.

## Step 5: Check whether this project is already managed

Before deciding whether to populate `knowledge/`, check whether Mnemonica already has a
checkpoint here: does `knowledge/.mnemonica-state.json` exist?

- **Yes:** this project has already been set up and audited before (setup is being re-run —
  typically after a plugin upgrade). Do not re-invoke `audit-full`; a full rescan of a project
  that is already tracked is wasted work every time someone re-runs setup. The CLAUDE.md block
  refresh in Step 3 already brought the algorithm text up to date, which is all a re-run needs
  to do. Skip to Step 7 and, in the report, suggest the user run `mnemonica:audit-light` (or
  `audit-full` if it has been a long time) themselves if they want a content check — don't run
  it automatically.
- **No:** continue to Step 6 — this is either a genuinely new install or a project that had its
  checkpoint file removed some other way; either way, treat it as needing classification.

## Step 6: Classify the project

Decide whether the project is **new** (essentially no code yet — a freshly initialized repo,
or only scaffolding/config/README present) or **existing** (there is already a working
codebase with real logic in it). Use judgment on the actual file tree; a project with even a
modest amount of real application code counts as existing — when in doubt, treat it as
existing, since scanning a small codebase costs little and skipping a real one leaves
`knowledge/` uselessly empty.

## Step 7: Populate, conditionally

- **New project, or already-managed project (Step 5 said yes):** stop here without invoking
  `audit-full`. For a genuinely new project, `knowledge/` stays empty and module files will
  appear organically as the independence test in `knowledge-conventions.md` gets applied
  during normal future work — do not pre-create placeholder module files for systems that do
  not exist yet.
- **Existing project, not yet managed:** invoke the `audit-full` skill now, in bootstrap mode,
  to scan the codebase and populate `knowledge/` from scratch. `audit-full`'s reconciliation
  logic is the same whether it is filling an empty `knowledge/` for the first time or
  correcting an already-populated one — do not reimplement scanning logic here. If
  `mnemonica:audit-full` cannot be invoked directly as a skill in the current environment,
  follow its SKILL.md instructions manually instead of skipping population. If Step 2 found no
  git repository, `audit-full` will still run — it uses its non-git fallback scan — just
  mention in the report that only `audit-full`, not `audit-light`, will be usable until the
  project has a git history.

## Step 8: Report

Tell the user, briefly: whether the project was treated as new, existing, or already-managed;
whether `.claude/CLAUDE.md` was created or amended; whether git is available and what that
means for `audit-light`; any `TRIGGER_OVERLAP` finding from Step 4, with the flagged line and
a suggestion to follow up with `mnemonica:doctor`; and — for an existing project that was
populated — which module files were created and what each one covers. Do not ask for
confirmation before any of this; installing the algorithm block, creating/populating
`knowledge/`, and reporting a trigger-overlap candidate are exactly the low-risk, reversible,
non-blocking actions `knowledge-conventions.md` says never require asking.
