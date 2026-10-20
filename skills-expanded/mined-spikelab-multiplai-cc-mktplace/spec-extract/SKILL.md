---
name: spec-extract
description: Writes BDD capability specs, in the format of buildme's specs/registry/, from the Python code of a commit, a directory or a PR, with every scenario citing lines a gate re-read at that commit. This version resolves the target, chooses and locks its run folder, lists the Python files and their public symbols, and asks one read-only agent per slice of code what it does, keeping only facts whose cited lines are at the commit; then groups the symbols into capabilities, asks one agent per capability for its requirements and scenarios, drops every scenario whose citations fail, and writes one registry file per capability. With --apply it then copies each new file into the repository's specs/registry/, after checking that nobody else's uncommitted work is there, and commits nothing.
when_to_use: 'Triggers: spec-extract, reverse-engineer specs, write specs from code, /multiplai-dev:spec-extract'
---

# spec-extract

Reads the Python code of one target and writes one capability file per
capability into a run folder, and with `--apply` copies the new ones into a
repository's `specs/registry/`:

1. **Resolve.** Resolves the target, chooses and locks the run folder, writes
   `state.json`, extracts the commit into `snapshot/`, and prints
   `SPEC_EXTRACT:RESOLVED <run>`.
2. **Scope.** Lists the `.py` files of the target (for `--pr`, those the PR
   changed that exist at its head, read whole), leaving out binary files, files
   over 200,000 characters, files marked `linguist-generated` or
   `linguist-vendored`, submodules and symbolic links. `ast` lists each
   module's public functions, classes and methods; a file it cannot parse is
   "not analysed". Test files are read as evidence, never specified. The files
   are split into explore units (at most 6,000 lines each); more than
   `--max-units` units is refused. Writes `plan.txt`.
3. **Explore.** One agent per unit, four at a time, with `Read`, `Glob` and
   `Grep` on `snapshot/` only. A unit whose agent run fails is asked once
   more; one with no answer after two attempts is listed as not analysed. An
   answer that does not parse is sent back once to be reformatted (one turn,
   no tools); when the budget or the backend stops that reformat, the attempt
   still counts, since its first run was paid for. A model setting no call can run with (an unknown provider,
   `claude-agent-sdk` missing, or for a `pi:` model the `pi` binary missing or
   failing to start) stops the run with exit 1 and counts no attempt, so the
   same command works once the setting is fixed. Every fact must cite lines
   a program re-reads at the commit with `git show`; the rest are dropped.
   Writes `facts.json` and `report.md`, and prints
   `SPEC_EXTRACT:EXPLORED <answered>/<units>`.
4. **Group.** One call with no tools reads the checked facts and the symbol
   list and puts the symbols into capabilities. A program then fixes the
   answer: kebab-case unique names, every public symbol in exactly one
   capability (one the answer left out goes to `unassigned`), at most 40
   symbols per capability (a larger one is split by module). Writes
   `capabilities.json`. No answer after two attempts: no capability file,
   `SPEC_EXTRACT:NOT_GROUPED`, exit 1.
5. **Write.** One agent per capability, four at a time, with `Read`, `Glob`
   and `Grep` on `snapshot/`, writes requirements with WHEN/THEN scenarios,
   each citing lines. Same retry rule as explore; a capability with no answer
   after two attempts is "not written".
6. **Gate.** Every citation is re-read at the commit. A scenario with no
   citation that passes is dropped and listed with the reason; so is a
   requirement left with no scenario. A scenario citing a test file is
   "pinned by test", else "read from code only". A public symbol no kept
   scenario cites is listed as not specified.
7. **Render.** Writes `registry/<capability>.md` in buildme's
   `specs/registry/` format, `report.md` and `summary.json`, deletes
   `snapshot/`, and prints `SPEC_EXTRACT:RENDERED <files> <run>/registry`.
8. **Apply** (only with `--apply`). Copies each `<run>/registry/<capability>.md`
   into `<specs-dir>/registry/` (created when absent) and commits nothing. A
   file already there with the same bytes counts as applied; one with other
   bytes is left untouched, and the run prints
   `SPEC_EXTRACT:SKIPPED_EXISTING <capability> <run>/registry/<capability>.md`.
   First it runs buildme's uncommitted-work check on `<specs-dir>/registry/`:
   any uncommitted change there (an edit, a deletion, a new file) is refused
   with exit 2 naming the files, and nothing is written. On a re-run after a
   stopped apply, the files that apply already wrote, unchanged since, are
   not counted as changes. Prints `SPEC_EXTRACT:APPLIED <n>`, `n` counting
   the files copied and those already there with the same bytes. The registry
   files are copied as they are in `<run>/registry/`, so an edit made there
   after render is copied too. Running `--apply` again on a finished run makes
   no model call.

**It sends the target's code to a model.** The repository's own files become
part of what the model reads, so the run needs the user to say they trust it:
`--trust-repo`, or `SPEC_EXTRACT_TRUST_REPO=1`. Without it the run stops
before its first model call with exit 4. Never pass `--trust-repo` on your
own judgment: if the run exits 4, ask the user whether they trust the
repository, and re-run with `--trust-repo` only on a yes. `--plan-only` makes
no model call and needs no trust.

## Command

```bash
uv run --directory "${CLAUDE_PLUGIN_ROOT}/skills/spec-extract/scripts" python -m spec_extract_pipeline run \
  --repo /abs/path/to/repo --tree HEAD [options]
```

**Pass absolute paths, and always pass `--repo` for `--tree` and `--pr`.**
`uv run --directory` runs the command from the skill's `scripts/` folder, so a
relative `--repo`, `--dir` or `--out`, or a missing `--repo`, would name that
folder, not the user's checkout.

| Target | Reads |
|---|---|
| `--tree <commit> [--path <dir>]` | the commit, or one directory of it, in `--repo` |
| `--pr <n>` | the PR's head commit, in `--repo`; needs `gh`. The PR is read from `origin`'s repository, which is also where `--fetch` fetches from |
| `--dir <dir>` | a directory that is not under git: copied into `<run>/source/` and committed there, including files its `.gitignore` names; never written to |

| Option | Does |
|---|---|
| `--out <root>` | Where run folders go. Default `<data_dir>/spec-extract` (the multiplai data directory). |
| `--repo <dir>` | The checkout for `--tree` and `--pr`, as an absolute path. Without it the run reads the current directory, which under `uv run --directory` is the skill's `scripts/` folder. |
| `--fetch` | For `--pr`, fetch `origin` and the PR's head first. Without it, a commit missing from the clone is refused with the `git fetch` command to run. |
| `--restart` | Renames the run folder to `<object>.old-<YYYYmmddHHMMSS>` (never deletes) and starts it again. |
| `--trust-repo` | Say the repository is trusted: its code is sent to a model (same as `SPEC_EXTRACT_TRUST_REPO=1`). |
| `--max-usd <usd>` | Spend cap for this run folder, default 80. It counts every run that resumes the folder, so re-running never gets a fresh cap. |
| `--max-units <n>` | Refuse a target that splits into more than n explore units (default 20); narrow it with `--path`. |
| `--plan-only` | Resolve and scope, print the units and how many calls a run would make, write `plan.txt`, and stop before any model call. |
| `--apply` | After render, copy each new registry file into `<specs-dir>/registry/` (step 8). Commits nothing. |
| `--specs-dir <dir>` | With `--apply`: the specs directory, as an absolute path. Default `<repo>/specs` for `--tree` and `--pr`; required with `--dir` (without it the run prints `SPEC_EXTRACT:APPLY_NEEDS_SPECS_DIR`, exits 2 and writes nothing). It must be in a git work tree and not inside the run folder, checked before any model call. |

Running the same command again resumes the run in the same folder: it asks
only the units with no answer, and pays for no call whose answer was saved.

Models: `multiplai.conf` keys `spec_extract_explore_model` (explore) and
`spec_extract_write_model` (group and write); unset means the session's model.

## Where results land

`<root>/<repo>/<object>/`:

- `<repo>` is the repository name from `origin`, without the owner (the
  directory name when there is no `origin`). A repository named `legacy` or
  `.locks` becomes `<name>@<owner>`.
- `<object>` is `tree@<sha12>`, `tree-<path>@<sha12>`, `pr-<n>@<head12>`, or for
  `--dir`, `dir-<basename>-<6 hex>`.
- A folder another remote's run wrote is left alone: the run uses
  `<repo>@<owner>/<object>/`. A folder another `--path` wrote (two paths that
  clean to one name) gives way to `tree-<path>-<6 hex>@<sha12>`.

Only one run may write a folder at a time: a run holds
`<root>/<repo>/.locks/<object>.lock` until it ends.

## Exit codes

On every exit but a kill, the last line printed is `SPEND:<usd>:<tokens>`: what
this invocation's model calls cost (a resume's earlier spend is not in it).
buildme adds it to its own `SPEND:` line when it runs spec-extract.

| Code | Means |
|---|---|
| 0 | Done. |
| 1 | Failed, including no group answer after two attempts (`SPEC_EXTRACT:NOT_GROUPED`; re-running makes no call and exits 1 again; `--restart` starts the run over), a model setting no call can run with (nothing is counted), a `state.json` that cannot be read, or a `--dir` run whose `<run>/source/` no longer holds its import commit (the message names `--restart`). |
| 2 | Refused: a bad target, a commit not in the clone, a `--dir` run folder that would be inside its source (for example `--out` the source's parent), every candidate folder holds another target's run (pass `--out`), no Python file to read (`SPEC_EXTRACT:NO_PYTHON`), or more explore units than `--max-units`. With `--apply`: `--dir` without `--specs-dir`, a `--specs-dir` outside any git work tree or inside the run folder, uncommitted changes in `<specs-dir>/registry/` (the message names them; nothing is written), or an uncommitted-work check that could not run (`uv` missing, no answer within 300 seconds, or an answer that is not one JSON line; its last error lines are shown). A repository with no commit is refused too, since the check compares with `HEAD`. |
| 3 | The run folder's spend reached `--max-usd`. Everything paid for is saved; re-run with a higher `--max-usd` to continue. |
| 4 | The repository was not marked trusted. Ask the user whether they trust it, and re-run with `--trust-repo` only on a yes. |
| 5 | Another process is running this target now. The message names its pid, host and start time. |

## What it writes in the run folder

`state.json` (the target, the scope, every answer and the spend so far),
`snapshot/` (deleted once the registry files are written), `plan.txt`,
`facts.json` (the checked facts, in review's `facts.v1` format),
`capabilities.json`, `registry/<capability>.md` (one per capability: a first
line naming the run and the commit, then `### Requirement:` blocks whose
scenarios carry `- **CITES** \`path:start-end\`` and `- **EVIDENCE**` lines),
`report.md` (the target and commit, the files left out and why, the files not
analysed, counts, every dropped item with its reason, the symbols not
specified, not grouped or not written) and `summary.json` (the same lists).
Only `state.json` holds the spend, and only it and `facts.json` (its
`generated_at`) a timestamp. Only `state.json` is read back; until the
registry files are written the others are rewritten from it, so editing them
changes nothing. After that a re-run makes no call and leaves them as they are.

## What it writes outside its output

Without `--apply`, nothing. With it, only the new files in
`<specs-dir>/registry/` (through a temporary `<specs-dir>/registry/.spec-extract-tmp/`,
deleted when the apply ends); it never changes an existing file there and
never commits, and the check it runs first only reads. `--tree` and `--pr` read git objects with `git ls-tree`,
`git cat-file` and `git show`; `--fetch` adds refs to the clone. `--dir` reads
the directory only.

`snapshot/` holds each file's bytes as git stores them, whatever the commit's
`.gitattributes` export rules say. A link that is absolute or leads out of the
tree is left out of `snapshot/`, and the run names it on stderr.
