---
name: workspace-cleanup
description: >-
  Safely clean up a sprawling repository or multi-project workspace (stray folders, duplicate copies,
  stashes, dead docs, crash dumps, misplaced files) without losing anything. Inventory first (size, git
  state, last touched, who references it), classify every item keep / move / archive / delete / ask,
  settle the plan with the human before any destructive step, write a manifest row before every move,
  repoint references, prove nothing broke (tests, build, reference re-scan, manifest check), then
  reconcile the docs with reality. Ships a stdlib Python helper for inventory, reference search, tree
  hashing, write-ahead manifest logging and manifest verification. Use when the user says "clean up
  this repo", "tidy the workspace", "reorganize these folders", "this repo is a mess", "dedupe these
  copies", "archive the old stuff", "what can I delete", "move X into Y and fix the references", or
  before any large folder restructure.
---

# Workspace Cleanup

A cleanup is a migration that happens to have a delete button. Most of the damage done by cleanups
comes from three things: deleting something nobody opened, moving something that other files point
at, and not writing down what moved so a loss cannot even be detected later. This skill exists to
make those three impossible, and to finish with proof rather than a claim.

## Five rules (non-negotiable)

1. **Never delete what you have not looked at.** Open it, list it, hash it. "It looks like a copy"
   is not evidence; a matching content hash is.
2. **Reference-check before moving, re-scan after.** Search for every spelling of the old path before
   the move; a step is not done until the re-scan shows zero stale references, or each survivor is
   explicitly justified (a changelog, a dated log entry).
3. **Destructive steps need explicit human approval per item.** Deleting, overwriting, rewriting
   history, touching anything outside the agreed roots. Approval of the plan does not cover things you
   discover while executing it; those go back to the human.
4. **Write the manifest row before the action.** Write-ahead, not after-the-fact. A cleanup whose log
   is missing cannot prove it did not lose something, and "already gone" becomes indistinguishable
   from "lost by the move".
5. **Done means proven.** The project's own tests/build pass, the manifest check passes, the docs
   match the disk. Anything you checked only yourself is labelled self-checked in the report.

## What this skill creates in the user's repo

One working folder per cleanup, at the repository root (create it; ask whether to commit or ignore it,
the manifest and report are worth committing as history):

```
.cleanup/{YYYY-MM-DD}/
  inventory.tsv    phase 1 output (regenerable)
  plan.md          plan of record: homes, one row per item, verdicts, step statuses
  manifest.jsonl   write-ahead log of every move / archive / delete (append-only)
  report.md        final report: what changed, proofs, losses, deferred items
```

## The helper script

`scripts/cleanup.py` in this skill's folder. Python 3 standard library only; uses `git` if it is on
PATH and the root is a work tree, and degrades to `git=no-git` columns otherwise. Run it with
`python {this-skill-dir}/scripts/cleanup.py <subcommand> --help` for all flags. Reference scans always
skip `.cleanup/` (cleanup records mention old paths by design) and this skill's own folder.
`scripts/selftest.py` runs a full cleanup in a throwaway folder with seeded failures (21 assertions);
run it once after installing or changing the script.

| Subcommand | What it does |
|---|---|
| `inventory ROOT [--depth N] [--refs] [--last-commit] [--format tsv\|md\|json]` | One row per entry: path, kind, bytes, files, newest mtime, git state (tracked / untracked / ignored / mixed / no-git), last commit date, number of files outside the entry that mention it (same matcher as `refs`) |
| `refs TARGET [--root R] [--basename] [--kind file\|dir]` | Every line in every text file that mentions TARGET as a path: repo-relative (both slash styles, also after `./`, a parent-relative prefix, a root variable like `$ROOT/` or `${workspaceFolder}/`, or a repository URL), quoted, and absolute. Loud over silent: a mention after another path segment counts unless that longer path exists as a different folder or file (`site/docs/` is not root `docs/`). Files match by plain name (`[setup](SETUP.md)`, `cat SETUP.md`). A top-level FOLDER only matches path-shaped (`docs/`, `"docs"`), so prose "read the docs" is not a hit; `--basename` adds bare-word matches. Lines inside TARGET itself are included and marked `[inside target]` |
| `hash PATH...` | Stable content hash of a file or tree (the root's own name does not count). Two trees are byte-identical iff their hashes match |
| `log --manifest M --step N --op move\|archive\|delete\|keep --src S [--dst D] ...` | Appends an `intent` row (per-file content hashes of the source) BEFORE acting; `--done` appends the completion row after, with `--edited FILE` for each file inside the destination you changed on purpose; `--absent` records that a source was already gone. Refuses: a missing source; a delete with neither `--covered-by` nor `--approved-by`; a `--covered-by` whose content does not match the source file for file |
| `check M [--exclude GLOB]` | Verifies every row against the disk: sources gone; every source file present at the destination with the same content (except declared `--edited` files, and files a later logged step moved on; extra files are fine); covers still matching; no intent left without a done row; zero stale references to any moved or deleted path. Exit 1 on any failure |

The script is a tool, not the judgment. It cannot tell you whether a folder matters; it tells you
what is there, who points at it, and whether what you did matches what you said you would do.

## Workflow

Work in phases. Do not start a phase until the previous one is finished; do not start executing until
the human has ruled on the plan.

### Phase 0 - Scope and freeze

- Agree the **roots** (which folders are in scope) and the **no-touch list**. Default no-touch, even if
  in scope: secrets and credentials (`.env*`, keys, certificates, `*.pem`), anything owned by another
  person or tool, generated outputs you would regenerate anyway, vendored dependencies, and live data.
- Record the starting state: `git status` for each repo in scope (dirty files belong to someone; never
  sweep them into your commits), current branch, and whether anything else is writing to these
  folders right now (other sessions, watchers, builds, a running server whose files live in a folder
  you plan to move). Concurrent writers are the most common source of "the verifier saw something
  different from what I did".
- Find the project's proof commands now, before anything moves: test suite, build, lint, link
  checker, any script that reads paths. If there are none, say so; the reference re-scan and manifest
  check become the only proof and the report must say that.

### Phase 1 - Inventory

```
mkdir -p .cleanup/{date}
python {skill}/scripts/cleanup.py inventory . --refs --last-commit > .cleanup/{date}/inventory.tsv
```

(`.cleanup/` is skipped by the reference count, so re-running the inventory does not count itself.)

Go one level deep first, then `--depth 2` on the big or confusing entries. Read the inventory for
signals (details in `references/classification.md`): huge untracked trees, folders nobody references,
things last touched long ago, `copy`/`old`/`backup`/`tmp` names, the same name in several places,
ignored directories that hold real work.

**Anything untracked that you might move or delete gets recorded first**: commit it as-is (in its own
commit, before any move) or hash it into the manifest. Moving an untracked folder is moving something
with no history and no undo.

### Phase 2 - Look, then classify

For every entry, open it. List a directory and read enough of it (README, a few files, the newest
files) to say in one sentence what it is and who owns it. Then give it exactly one verdict:

| Verdict | Meaning | Evidence required before it may be executed |
|---|---|---|
| **keep** | Stays where it is | None; say why in one line |
| **move** | Belongs somewhere else in the workspace | Destination agreed; reference list from `refs` |
| **archive** | Out of the way but kept (an `archive/` folder, a dated attic) | Destination agreed; reference list |
| **delete** | Gone | Proof the content survives elsewhere (matching `hash`, or it is fully regenerable, or committed history holds it) OR explicit human approval to discard it |
| **ask** | You cannot decide from evidence | A specific question for the human |

"Duplicate" means byte-identical by content hash. Same name with different content is two things, not
one; keep both until a human decides. When the only copy of something is in an archive or backup
format that captures only part of it (a skill archive that stores only skill folders, a package
cache, an export), the archive does not cover the original; keep the original.

Define the **homes** before assigning destinations: one line per top-level location saying what it
is FOR. Most "where does this go" questions answer themselves once homes are written down, and most
bad plans are bad because two places were silently doing the same job.

### Phase 3 - Plan of record, and the question round

Write `.cleanup/{date}/plan.md` (template in `references/classification.md`): homes, a table of every
non-keep item (what it is, verdict, destination, evidence, references found, risk), the ordered steps,
and the open questions.

Then ask the human, in one round, grouped by topic, with your recommendation on each. Specifically ask
about: every `ask`, every `delete` without a content-hash proof, anything outside the agreed roots,
anything touching another person's work, and any premise of an earlier plan that the inventory
contradicts. Plans written before an inventory are frequently wrong about where things live and what
counts as a duplicate; checking premises here is the cheapest step in the whole cleanup.

Record the rulings in plan.md, dated. The rulings, not your original proposal, are what you execute.

### Phase 4 - Execute, one step at a time

For each step, in order (mechanics and platform traps in `references/execution.md`):

1. Re-check the source still looks like the plan says (someone may have changed it since).
2. `refs` for the source; note every file you will need to repoint, including `[inside target]` lines
   (the moved tree's own mentions of its old path).
3. `log` the intent row (records per-file hashes; refuses a missing source; if it is already gone,
   stop and record `--absent` instead, and tell the human, never skip silently).
4. Act. Prefer version-control-aware moves (`git mv`) for tracked content so history follows.
   Delete only paths you enumerated; never a glob in a shared or system folder.
5. Repoint references (Phase 5 for this step).
6. `log --done`, with `--edited <new path>` for each file inside the destination you repointed.
   Undeclared changes inside a destination make `check` fail; that is the point.
7. Commit the step on its own, staging only the paths it touched; unrelated dirty files stay unstaged.
8. Mark the step in plan.md: DONE + commit id, or the reason it stopped.

If anything surprises you mid-step (a source differs from the plan, a delete candidate turns out to
be unique, a lock prevents a move), stop that step, record it, and ask. Do not improvise a new
destructive action.

### Phase 5 - Repoint references

Search for the old path in every spelling (`refs` does relative with both slash styles and absolute;
add `--basename` when a bare name is used in config). Update: config files, import paths, scripts,
CI workflows, docs and indexes, symlinks, tool manifests that pin absolute paths, and ignore files.
Then re-run `refs`; the result should be empty except for justified historical mentions (dated logs,
changelogs), which you pass to `check --exclude '<glob>'`. Excluding a file hides real stale references
in it too, so exclude history files only, never a whole working folder. Ignore-file lines are not
reported for deleted paths (a deleted, regenerable `build/` keeps its ignore line on purpose); for moved
paths they are, because the ignore rule should usually follow the move.

Watch ignore rules: moving content under a path that an ignore pattern matches (a bare `scripts/` or
`build/` line matches at every depth) silently drops it from the next commit while it still looks
correct on disk. After committing a move, compare the committed tree with the working tree, not the
working tree with itself.

### Phase 6 - Prove nothing broke

1. Run the project's proof commands from Phase 0 (tests, build, link check, any script that reads
   moved paths). Record the actual output line, not "passed".
2. `cleanup.py check .cleanup/{date}/manifest.jsonl [--exclude '<historical glob>']` must exit 0,
   without `--no-hash` (that flag turns off the completeness proof; if you ever need it, the report
   says so).
3. For every moved tracked tree: the committed files at the destination equal the source files
   (compare `git ls-files` counts and content hashes, not directory listings).
4. **Independent verification**, when your environment can spawn a separate agent or a human can
   review: hand it the plan, the manifest and the checklist in `references/verification.md`, with
   default verdict REJECT and full comparison rather than sampling. It must not be told what you think
   the answer is. If no independent check is possible, the report says every step was self-checked.

### Phase 7 - Reconcile and report

- Recompute every number you will write from the disk now (counts of files, folders, items), and say
  what each number counts. A figure copied from an earlier message is how a count of index rows gets
  reported as a count of stored folders, and the two differ.
- Update every doc that describes the layout: READMEs, indexes, the plan's step statuses, onboarding
  docs, anything that lists folders. Docs describing the old layout are the most common leftover.
- Re-scan the roots for new litter created during the cleanup (crash dumps, temp files from
  concurrent tools) and list it rather than silently sweeping it.
- Write `report.md` (template in `references/verification.md`) and end in exactly one terminal state.

## Terminal states

| State | When |
|---|---|
| **done** | Every approved step executed, all proofs pass, docs reconciled |
| **partial** | Some steps executed and proven; the rest deferred with a reason and an owner |
| **blocked** | Waiting on a human ruling or on something outside your control (a lock, a missing permission) |
| **rolled back** | A proof failed and the affected steps were reverted from the manifest |
| **no-op** | The inventory showed nothing worth changing; say so in one line |

A loss (something that existed and now cannot be found, or cannot be proven not lost) is always
reported at the top of the report, whatever the terminal state.

## Anti-patterns

- **Delete by resemblance.** Folder names, sizes and dates suggest duplicates; only hashes prove them.
- **Guarded moves that skip silently.** `if exists(src): move(src)` turns a missing source into a
  silent no-op and destroys the evidence of whether it was lost. Missing sources are loud.
- **The log written at the end.** A script that crashes before writing its log leaves you unable to
  say what it did. The manifest row goes first.
- **Glob deletes in shared places.** `rm -rf /tmp/*.py` to clean up your own files removes everyone's.
  Delete only enumerated paths you created or were approved to remove.
- **Executing the old plan.** A plan written before the inventory encodes guesses; re-check its
  premises in the question round instead of carrying them out.
- **Sweeping dirty files into the cleanup commit.** Uncommitted changes in a repo are someone's work
  in progress; stage only the paths your step touched.
- **Verifying the working tree instead of the commit.** Ignore rules, case-only renames and line-ending
  filters can make the disk right and the commit wrong.
- **Treating a partial archive as a backup.** An archive that captures only some file types or only
  some folders does not cover the original; the original stays.
- **Counting from memory.** Every number in the report is re-derived from the disk at report time.
- **Quiet scope creep.** Something discovered mid-cleanup that looks deletable goes into the plan as
  an `ask`, not into the current step.

## References

- `references/classification.md` - inventory signals, verdict rubric by kind of thing, homes, and the
  plan.md template with the question-round format.
- `references/execution.md` - moving safely: untracked content, version-control moves, per-step
  commits, locks and platform traps, bulk moves, rollback from the manifest.
- `references/verification.md` - manifest schema, what `check` proves and does not, the independent
  verifier brief, and the report.md template.
