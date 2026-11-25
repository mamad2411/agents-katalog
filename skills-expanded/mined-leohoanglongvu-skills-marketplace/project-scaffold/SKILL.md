---
name: project-scaffold
description: >-
  Use when a repository's folder structure is enforced policy rather than taste: a CLAUDE.md
  directory map, ID registers (REQ, ADR, DEC, RISK, ISS, CR...), and a traceability matrix
  that a wrong path silently breaks. Two things it does. First, stand up a new project to that
  standard - start, scaffold, bootstrap, or lay out a repo the way our other repos are laid
  out. Second, and more often, decide and enforce placement afterwards: where does this file
  belong, what's the naming format, what's the next ID; adding or amending a requirement, ADR,
  decision, risk, issue, change request, design doc, runbook, schema, or diagram; auditing
  drift; and - importantly - any request to stop files landing in the wrong place at all,
  whether by making the map binding, wiring a guardrail or hook, or blocking bad writes so
  nothing has to be moved back. Skip if the user just wants a framework's stock starter
  template, or the repo has no such map.
---

# Project scaffold

In this structure a file's path is part of its meaning, not a filing preference.

`requirements/software/REQ-SW-0012-import-csv-files.md` says: a software
requirement, derived from a system requirement, holding ID 0012, listed in
`requirements/software/index.md`, and traced in `rtm.md` to the ADR, the source
file and the test that satisfy it. Put the same words in `docs/notes.md` and
every one of those relationships disappears. Nothing errors and no test fails —
the requirement simply stops being findable by the register, the traceability
matrix, and the next person to look.

That asymmetry is why placement gets decided deliberately here. Getting it right
costs one lookup. Getting it wrong costs someone else a search they do not know
they need to run.

## What this skill covers

1. **Creating a new project** from the contract — the interview, the scaffold,
   and what deliberately does not get created.
2. **Placing every file** that goes into such a project afterwards.

The second is the larger job. A project is scaffolded once and written into for
years.

## Mode 1 — Creating a new project

### Interview before scaffolding

Five answers cannot be guessed, and the scaffold refuses without them:

| Answer | Why it cannot be defaulted |
|---|---|
| Project name | names the repo, the map, the build file |
| One-paragraph summary | the first thing every future session reads |
| Stack: `python`, `dotnet` or `other` | selects the commands block and the code rules |
| Stack description, e.g. "Python 3.12, FastAPI, PostgreSQL 16" | tells a reader what they are joining |
| Today's date | stamps every seeded document |

Worth asking, but defaulted if the user does not care: document owner, phase
(`discovery` … `operations`), issue tracker, secret manager, sample-data size
cap, where contracts live, licence.

Do not write the summary paragraph yourself from a one-line brief. Ask what the
system does, who it is for, and where the project stands. A vague summary is
copied forward into every future session unchallenged.

For `--stack other`, the template also needs the formatter, type checker,
docstring style, test-tagging syntax, workspace linking, logging library and
configuration mechanism. The script lists whichever are missing rather than
inventing them.

### Run the scaffold

Preview first — `--dry-run` prints the file list without touching the disk:

```bash
python scripts/scaffold.py --dry-run \
  --path ~/projects/falcon-telemetry \
  --name "Falcon Telemetry" \
  --summary "Ingests flight telemetry from the ground station, normalises it, and serves it to the operations dashboard. Built for the flight-ops team." \
  --stack python \
  --stack-desc "Python 3.12, FastAPI, PostgreSQL 16, uv" \
  --today 2026-09-02 \
  --owner "Long VH" \
  --phase discovery \
  --tracker "https://jira.example.com/projects/FT" \
  --secrets "1Password Secrets Automation"
```

Drop `--dry-run` to write. The script fails loudly if any `{{placeholder}}`
would survive into a project file — an unfilled slot in `CLAUDE.md` reads as an
instruction and quietly corrupts every later placement decision.

Use the script rather than writing these files by hand. It reproduces the
200-line map verbatim from `assets/`, and a paraphrased map is a different
contract.

### What lands, and what deliberately does not

Twenty files: `CLAUDE.md`, `.claude/rules/documents.md`, `.claude/rules/code.md`,
`.claude/settings.json`, `README.md`, `CHANGELOG.md`, `.gitignore`,
`.editorconfig`, the build file, `requirements/traceability/rtm.md`, and an
`index.md` for each of the ten ID registers.

No other directories are created, and this surprises people who asked for "the
folder structure". It is rule 2 of the contract: *create a directory only when
its first artifact exists*. Seventy empty folders assert seventy kinds of work
in progress, none of which has started, and a reader cannot tell an unstarted
area from a finished one. The map in `CLAUDE.md` is the structure; the tree on
disk is the subset that has been earned.

If the user pushes back and wants the whole tree, say what they lose and then do
it — it is their repository.

The registers are the exception, and are seeded because ID allocation has to
work from the first document: the next ID is the highest in `index.md` plus one,
which needs an `index.md` to exist.

### Offer the enforcement hook

`--enforce-hook` additionally copies `check_path.py` into `.claude/scripts/` and
registers a `PreToolUse` hook that blocks any Write or Edit to a path the map
disallows, with the reason and the correct location. It fails open on any
internal error, so a bug in the checker cannot stop legitimate work.

Offer it; do not assume it. It is right for a repository several people and
several agents will write to, and heavy-handed for a solo prototype.

### After scaffolding

Tell the user what to do next — usually `git init`, then the charter or the
first requirements. From that point the project's own `CLAUDE.md` is the
authority; this skill supplies the procedure and the tools.

## Mode 2 — Placing a file, every file, every time

**Before creating any file in a project built from this contract, resolve its
path from the map — never from memory or from what looks tidy.** This holds for
every file: a one-line note, a diagram export, a test fixture, a scratch script.
There is no size below which the map stops applying, because the cost of a
misfiled artifact does not scale with its size — a lost two-line decision record
is as lost as a lost design document.

The sequence, which is rule 1 of the contract:

1. **The directory map** in `CLAUDE.md`. Most files are resolved here.
2. **The look-alike table** beneath it, if two folders both look right. It exists
   because certain pairs genuinely confuse everyone.
3. **`references/placement.md`** in this skill, for the reasoning behind the hard
   cases — the four homes for "interfaces", ADR versus DEC, the five homes for
   anything about data, where security artifacts split, prototype versus tool.
4. **Ask.** Rule 1 ends with it, and it is the cheapest step in the sequence.

Never invent a top-level directory. A new top level asserts a class of artifact
the project has not agreed exists, and it is the one placement error the
contract calls out by name.

### Confirm before writing

```bash
python scripts/check_path.py architecture/adr/ADR-0007-use-postgresql.md
```

The checker knows the mechanical half of the contract — which folders exist, how
records are named, which prefix belongs to which register, which IDs are already
taken, where dates lead a filename, where kebab-case applies and where language
conventions rule instead. It reports errors (placements the map disallows) and
warnings (conventions worth following), and prints the correct location for each.

It does not make the judgement call between two plausible homes. That stays with
you; `references/placement.md` is how you make it.

Useful modes:

```bash
python scripts/check_path.py --next-id ADR      # next free ID in a register
python scripts/check_path.py --audit            # every file in the repo
```

Run `--audit` when picking up an unfamiliar project, or when the user suspects
drift.

### Working the registers

Every ID-bearing record has three parts that move together:

1. The file, named `PREFIX-nnnn-kebab-title.md`.
2. A row in that folder's `index.md`.
3. Wherever it is traced — `rtm.md` for requirements, the `relates-to` frontmatter
   for everything else.

Write all three in the same change. A file without its index row leaves the next
author to allocate an ID that is already taken; an index row without its file is
a dangling reference. `--next-id` reads both, so a half-finished record makes it
wrong.

Skeletons with the right frontmatter and section order are in
`assets/doc-templates/`: `adr.md`, `requirement.md`, `decision.md`, `risk.md`,
`issue.md`, `change-request.md`, `design-component.md`, `report.md`. Copy the
relevant one rather than reconstructing the structure — `.claude/rules/documents.md`
fixes the section order for ADRs and requirements, and a reordered ADR is harder
to review.

### Two rules that catch people out

**Approved documents are not edited in place.** Raise a `CR-nnnn` in
`management/changes/` with its impact analysis, then update the document, bump
`updated:`, and add a line under `## History`. Only a human moves a document to
`approved` — never set that status yourself.

**Superseding is a move, not a delete.** The old file goes to `archive/` at the
same relative path with `status: superseded` and `superseded-by:` set; the new
file sets `supersedes:`; the register's `index.md` reflects both. Superseded
*code* is handled by git history — `archive/` is for documents.

## Working in a project you did not scaffold

If it has a `CLAUDE.md` with a directory map, that file is the authority and
overrides anything here that differs — a project may have amended its own map.
Read it first. This skill's checker reads the same map it was built from, so if
the project's map has been extended, trust the project and tell the user the
checker is behind.

If it has no such map, this structure does not apply. Do not impose it.

## Files in this skill

| Path | What it is |
|---|---|
| `scripts/scaffold.py` | creates the project root; `--dry-run`, `--enforce-hook` |
| `scripts/check_path.py` | validates paths; `--audit`, `--next-id`, `--hook` |
| `references/placement.md` | how to decide between plausible homes, with worked examples |
| `assets/CLAUDE.md` | the contract template, verbatim — the source of truth for the map |
| `assets/rules/` | `documents.md` and `code.md`, verbatim |
| `assets/doc-templates/` | eight document skeletons with correct frontmatter |

`assets/CLAUDE.md` and `assets/rules/` are the contract as given. Changing them
changes every project scaffolded afterwards, so treat an edit there as a
decision, not a tidy-up.
