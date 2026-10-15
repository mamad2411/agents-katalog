---
name: harness-scaffold
description: |
  Given a /goal prompt (from meta-loss-function-development) and
  a project root, scaffold the harness tree: verifiers/,
  instruments/, design tasks with deterministic graders,
  AGENTS.md, GOAL.md, README.md, and the held-out grader
  directory. The output is a runnable project in <5 minutes
  for a fresh human or agent.

  Load this skill whenever the user pastes a /goal prompt and
  says "scaffold the project", "set up the harness", or
  describes a fresh project root to use. Also load it when
  the user wants to add a new design task or held-out task
  to an existing project.

  Companion skills (install separately if not present):
  - meta-loss-function-development: produces the /goal prompt
  - loss-function-design: the 4-piece loss anatomy
  - harness-engineering: what the agent sees
  - cline-orchestration: the Cline runtime (substitute your
    own if not using Cline)
version: 1.0.0
author: open source
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [harness, scaffold, scaffolding, loss-function-development, lfd, project-setup]
    related_skills: [meta-loss-function-development, loss-function-design, harness-engineering, cline-orchestration]
---

# Harness Scaffold

Given a /goal prompt and a project root, this skill scaffolds
the harness tree. Output is a runnable project: `verifiers/`,
`instruments/`, `AGENTS.md`, `GOAL.md`, `README.md`, design
tasks with deterministic graders, and the held-out grader
directory (off-limits to the agent).

The scaffold is **driven entirely by the /goal prompt** —
nothing is hard-coded. The skill parses the prompt for the
target, constraints, runtime, design tasks, and held-out
tasks, and produces the matching tree.

## How the user invokes this

The user has a /goal prompt (from `meta-loss-function-development`)
and a project root path. They say:

> "Scaffold the harness at `<project-root>` from this
> /goal prompt: <paste>"

The skill:

1. Parses the prompt to extract the design tasks, held-out
   tasks, runtime (which agent), and budget.
2. Creates the project tree at the project root.
3. Generates `AGENTS.md`, `GOAL.md` (the prompt itself),
   `README.md`.
4. Generates `verifiers/cline-wrapper.sh` (or the runtime
   equivalent), `verifiers/run-design-set.sh`,
   `verifiers/instruments/*.sh`,
   `verifiers/compute_sub_losses.py`,
   `verifiers/parse_cline_output.py`.
5. Generates `verifiers/private/grader.sh` (chmod 700) with
   stubs the user fills in.
6. Generates the design tasks at `test-tasks/design/01..05/`
   with `prompt.txt`, `<starting-file>`, and `grade.sh`
   stubs.
7. Generates the held-out task placeholders at
   `test-tasks/held-out/h01..h10/` (just the directory
   structure — the user fills in the actual files).
8. Writes a `README.md` with run instructions.

The fresh session that runs the loop doesn't have to do any
of this by hand.

## The scaffold's output layout

After this skill runs, the project root has:

```
<PROJECT_ROOT>/
├── AGENTS.md                          # loop driver rules
├── GOAL.md                            # the /goal prompt itself
├── README.md                          # run instructions
├── verifiers/
│   ├── cline-wrapper.sh               # the only way to invoke Cline
│   ├── parse_cline_output.py          # NDJSON parser
│   ├── compute_sub_losses.py          # 7 sub-losses
│   ├── run-design-set.sh              # runs the 5 design tasks
│   ├── instruments/
│   │   ├── time-remaining.sh
│   │   ├── tokens-remaining.sh
│   │   ├── tokens-this-iter.sh
│   │   ├── cline-version.sh
│   │   ├── cline-skills-dir.sh
│   │   └── sub-loss-readout.sh
│   └── private/                       # HELD-OUT — chmod 700
│       └── grader.sh
├── test-tasks/
│   ├── design/                        # 5 tasks
│   │   ├── 01-<name>/
│   │   │   ├── prompt.txt
│   │   │   ├── <starting-file>
│   │   │   └── grade.sh
│   │   ├── 02-<name>/...
│   │   └── ...
│   └── held-out/                      # 10 tasks (off-limits)
│       ├── h01/...
│       └── h10/...
├── skills/<artifact-name>/            # the agent's candidate skill
│   └── SKILL.md
└── logs/                              # the loop's running trace
```

## What this skill does NOT do

- **Does not implement the design task graders.** The user
  (or the fresh session running the loop) writes the
  actual `grade.sh` scripts based on the per-task
  description. The scaffold writes *stubs* that exit 1 with
  a TODO.
- **Does not implement the held-out tasks.** Same reason —
  the user provides them. The scaffold creates empty
  directories with a `README.md` placeholder.
- **Does not write the candidate skill.** That's the
  agent's job during the loop.
- **Does not run the loop.** That's a separate skill
  (`loop-driver` — out of scope for this skill, but
  documented in the meta-loss-function-development skill).

## Parsing the /goal prompt

The scaffold uses regex to extract the structured sections
of the /goal prompt. The format is the one from
`meta-loss-function-development/templates/goal-prompt.md`:

- `**Target.**` block → design set + held-out set
- `**Constraints.**` block → budget
- `**Instruments.**` block → instrument names
- `Design-set tasks` numbered list → design task paths
- `Held-out tasks` named `h01`...`hN` → held-out task paths
- `Harness layout` code block → file tree
- `First action` numbered list → bootstrap steps

If parsing fails on a section, the scaffold emits a default
and a `// TODO: user-fill` comment in the file.

## Per-platform behavior

The scaffold is shell-and-Python only. No `cline`-specific
runtime calls during scaffolding. The wrapper script
(`verifiers/cline-wrapper.sh`) calls Cline at loop time, not
at scaffold time.

The instrument scripts use `mktemp` and `/bin/bash` (POSIX
shell). They work on macOS, Linux, and WSL. Windows native
(not WSL) is not supported by the harness itself; use WSL or
WSL2.

## When to load this skill

- The user has a /goal prompt and wants the harness
  scaffolded.
- The user says "set up the loop project at <path>" with a
  goal in mind.
- The user wants to add a new design or held-out task to an
  existing project.
- The user wants to migrate a /goal prompt from one
  project root to another.

## How the skill's scripts work

`scripts/scaffold.py` (in this skill) is the executable that
the user runs. It takes:

- `--project-root PATH` (required)
- `--goal-prompt PATH` (default: `GOAL.md` in project root)
- `--runtime {cline|codex|aider}` (default: `cline`)
- `--no-private` (skip the held-out grader scaffold — for
  internal-only projects that don't need it)

The script reads the goal prompt, extracts the sections, and
writes the tree. Idempotent: re-running updates the existing
files without overwriting user-modified ones (a heuristic;
  user-modified files are detected by an `agent-edited:` marker
  in the first 5 lines).

## Idempotency and the agent-edited marker

Every file the scaffold writes starts with a header comment
like:

```
# auto-generated by harness-scaffold v1.0
# DO NOT EDIT — overwriting will lose your customizations
# re-run `harness-scaffold` with --goal-prompt to regenerate
```

Files the agent has edited during the loop get a marker:

```
# agent-edited: yes
```

When the scaffold is re-run, files with `agent-edited: yes`
are skipped. Files without it are regenerated. This keeps the
scaffold honest (you can re-run to add a new task without
losing the agent's work) and the loop safe (the scaffold
won't clobber the agent's tuning).

## Pitfalls when using this skill

- **The scaffold is a starting point, not a finished
  project.** The graders are stubs. The user (or the loop
  driver) writes the real graders based on the task
  descriptions.
- **The /goal prompt must follow the template.** Free-form
  prompts won't parse cleanly. If parsing fails, the
  scaffold emits a default and a TODO. Use the
  `meta-loss-function-development` skill to emit a
  well-formed prompt.
- **The held-out tasks are user-provided.** The scaffold
  creates empty directories. The user (or a research skill)
  fills in the actual task files. The agent must not be
  able to read these directories; the scaffold sets
  permissions accordingly (`chmod 700` on `private/`,
  `chmod 600` on `grader.sh`).
- **The wrapper script depends on the runtime.** The
  scaffold generates the Cline wrapper by default. For
  Codex or Aider, the user (or the loop driver) replaces
  the wrapper with the appropriate invocation. The
  contract is the same; only the executable path and
  flags differ.
- **Don't run the scaffold over an existing project without
  reading the diff first.** The scaffold regenerates files
  without the `agent-edited: yes` marker. If the user has
  manually edited those, those edits are lost. Use `git
  diff` after the run.
- **If you change a shell template in `scaffold.py`, the
  emitted bash can break in three subtle ways.** Empty
  `if/else/fi` clauses (syntax error), backslash-escaped
  quotes inside `python3 -c "..."` invocations (runtime
  quoting bug), and GNU-isms like `grep -P` or `sed \w`
  that fail on macOS BSD userland. See
  `references/bash-emission-pitfalls.md` for the three
  bug classes and the post-change verification recipe.

## Related skills (install separately if not present)

- `meta-loss-function-development` — produces the /goal
  prompt this skill consumes.
- `loss-function-design` — the 4-piece loss anatomy.
- `harness-engineering` — what the agent sees.
- `cline-orchestration` — the Cline runtime (substitute
  your own if not using Cline).

## References in this skill

- `references/scaffold-flow.md` — the step-by-step scaffold
  flow with examples.
- `references/regex-extract.md` — the regex patterns used
  to parse the /goal prompt.
- `references/bash-emission-pitfalls.md` — the three
  classes of bug in `scaffold.py`'s emitted bash
  (empty `if/else/fi`, `python3 -c "..."` quoting,
  GNU-isms on macOS) and the verification recipe to
  catch them.
- `templates/` — file templates the scaffold uses (verifier
  scripts, grader stubs, etc.). Templates are inlined as
  Python string constants in `scripts/scaffold.py` (see
  `templates/README.md` for why and how to override).
- `scripts/scaffold.py` — the executable.
- `examples/goal-prompt-samples.md` — sample /goal prompts
  the scaffold has been tested against.
