---
name: debt
description: Use when mapping a repository's technical debt — finding hotspots, files that break the layer rules of the project's instruction file or the invariants of its docs/ARCHITECTURE.md, duplicated code, over-engineering, or rules that the instruction files and docs/ARCHITECTURE.md repeat or contradict — and filing or re-measuring debt issues for refactoring.
---

# Technical debt map

The map measures where the structural debt sits — hotspots, broken layer
rules, copies, the repeats and contradictions of the instruction files and,
with ponytail installed, over-engineering — and files at most three places a
run as issues labelled `debt`, and one more for the instruction files.
Take-in in the `craft:github` skill then checks those issues whenever a
task touches their area, so one pull request can remove the debt next to the
task. A place larger than one pull request becomes steps that the
`craft:roadmap` skill offers in order.

First check that the project has no debt skill of its own: a skill named
`debt` in your skill list other than this one, or a file that
`git ls-files ':(top,glob)**/.*/**/skills/debt/SKILL.md'` prints from any
directory of the checkout. When it has one, follow that one instead, with its
own rules and tools, and stop here.

The map changes no file in the working tree and opens no pull request. Every
number in an issue comes from a command's output in this run, never from
memory of an earlier one. `<dir>` is this skill's base directory, and
`<skills>` is the directory above it.

## Measure

Run `git -c core.hooksPath=/dev/null fetch -q origin` first, when there is an
`origin`. The scope is a path from the repository's root, or the whole tree.

Step 1 runs in your checkout. Every later step runs in `<tree>`, a checkout of
the SHA on the "Measured on" line of step 1, and not in the working tree: a
local commit or edit is not debt on the default branch. When that line says
`HEAD`, the clone has no `origin/HEAD`, and local commits count. Put `<tree>`
in your scratch directory, outside the repository. When a `<tree>` from an
earlier run is there, remove it first, with
`git worktree remove --force <tree>`. Then make it right after step 1, with no
hook and no LFS download:

```bash
git worktree prune
GIT_LFS_SKIP_SMUDGE=1 git -c core.hooksPath=/dev/null worktree add --detach <tree> <sha>
```

No step runs a package manager (`npm`, `npx`, `bun`, `pnpm`, `yarn`) or a
script of the project, in `<tree>` or in your checkout: a project's `.npmrc`
or scripts can run its code. `clones.sh` of step 4 runs `jscpd` outside both,
in a temporary directory of its own. Remove `<tree>` the same way when the map
ends. Run every command from the root of its checkout, so that all paths
start there.

1. **Hotspots.** `bash <dir>/scripts/measure.sh [path]` prints the code files
   by lines × the commits that touched them in 60 days, the top 15, and the SHA
   it read. Tests and migrations are code and count; documents, lockfiles,
   fixtures and ignore files are data and are left out. It does not follow
   renames, and its last line counts the code files the window moved. When
   they are a large share of the scope, the commit counts start at the move,
   and a score is close to the file's size: say so in the report.
2. **Layer rules.** Read the project's instruction files in `<tree>` —
   `CLAUDE.md`, `AGENTS.md` and the ones in the scope's directories — for what
   a directory may import or hold, with its exceptions. Turn each rule into one
   `git grep -n` over the scope. For a whole word use `-w`: `\b` does not work
   with `-E` on macOS. A broken pattern finds nothing, and that looks like a
   pass. Before you trust an empty result, run the pattern over a file you
   have read, with a line it must find, such as an import that the rule
   allows, and check that this line is in the output.
   A rule that a grep cannot test, such as a size or a mirrored layout, gets
   the command that can (`wc -l`, a listing), or is left out and named in the
   report.

   The architecture file, `docs/ARCHITECTURE.md` or `ARCHITECTURE.md` at the
   root, holds the project's rules too. Run
   `bash <skills>/architecture/scripts/invariants.sh` from the root of
   `<tree>`, and keep the hits under the scope:
   - a hit under `I-<n> FAIL`, with no `debt` before it, is a broken rule,
     and its issue cites `I-<n>`;
   - a `debt` hit of a `grep` check is a broken rule too. A `debt` hit of a
     `lines` or `files` check is a hotspot, which *Choose the places* makes a
     place or puts into *next*. A path can be on a `debt` list with no
     issue: a first architecture file puts it there without one;
   - an invariant that the script prints as `review only` has no `Check:`
     line: name it in the report, as a rule that a grep cannot test.

   When the script exits with 2, it gives the causes on stderr, and each
   invariant that it did not print did not run. Give the messages, and name
   those invariants in the report as not checked.

   The architecture file can also name the one way to do a kind of work, as
   the one HTTP client. A second way competes with it when it does the same
   work without the named way, and is code of its own that other modules
   import, as a second client, a wrapper of another client or a dependency:
   then the fix must choose which way stays. Find it with
   `git grep -n` over the scope, as for a rule above. It is a place of its
   own, or it joins the place of the invariant that covers it. The issue of
   that place says that the fix writes an ADR through
   `craft:architecture`, and that the other hits move to the way that
   the ADR keeps. A place whose hits are only direct calls where the named
   way already serves, as one module that calls `fetch`, has no second way:
   its issue asks for no ADR.

   Keep a hit only when the rule's text, its exceptions included, forbids it.
   A hit that the text leaves open is *borderline*: name it in the report,
   and file none. The map carries no rules of its own: with no such rule in
   the instruction files and no architecture file, skip this step and say so.
3. **Over-engineering**, when the ponytail plugin's `ponytail-audit` skill is
   in your skill list; else skip this step and say so. It takes no path and
   loads as instructions, so in Claude Code send it to one subagent right
   after you make `<tree>`, before step 2 reads the project's rules: "Invoke
   the `ponytail:ponytail-audit` skill, audit only `<scope>` of `<tree>`, and
   return its lines as it prints them, every path of each finding in its
   `[path]` and relative to `<tree>`. File nothing, change no file, and run no
   package manager and no script of the project, in any directory." In Codex,
   run it yourself at that point, with the same limits. Then sort its
   findings, in this order, each part of a bundled finding on its own:
   1. **Against the project's rules.** Drop a part that a rule of the files
      of step 2 contradicts or requires: ponytail counts a file that exports
      one thing as bloat, and a project with one entity per file keeps it.
      Quote the rule in the report.
   2. **Already a broken rule** of step 2: it counts once, there.
   3. **A place or a small cut.** A place is a fix that is a pull request of
      its own: a dependency the platform covers, an abstraction with one
      implementation, a layer that only delegates and that no rule requires. A
      fix of a few lines, in one file or in a few, is a small cut: it goes into
      the report, for the Boy Scout Rule when someone next works there.
4. **Duplication.** `bash <dir>/scripts/clones.sh <tree> [path]` runs
   `jscpd`, at the version the script pins, on a copy of the scope's code
   files, by the data rule of step 1 and with SQL left out, so that a copy in
   a document or a fixture cannot hide a clone. It prints the clones of 15
   lines or more, longest first, with paths from the root: each one is a
   finding. *Lines* is jscpd's length, the length of the first file's range.
   jscpd gives pairs: read the ranges, and rows that copy the same block are
   one place, which the fewest shared helpers that remove all its rows fix.
   Sort a clone place as the findings of step 3: a rule of step 2's files that
   requires the copies drops it, and one that forbids them makes it a broken
   rule, counted once. Then check each clone place that no rule drops or
   forbids against the three conditions of *Shared code or a copy*, under
   *Decomposition* in `<skills>/architecture/SKILL.md`. The number of copies
   does not decide here. A place that fails one of the three is a copy kept
   on purpose: name it in the report, and file none. When `clones.sh`
   exits with an error, as with neither `npx` nor `bunx` or with a shared
   `TMPDIR`, skip this step and give its message in the report. `jscpd` never
   goes into a `package.json`.
5. **Instruction files.** With no `CLAUDE.md` and no `AGENTS.md` in `<tree>`,
   skip this step and say so. Otherwise send two readers right after you
   make `<tree>`, beside the subagent of step 3, as for a spec in
   `craft:review-loop`: in one message, an `Agent` call with
   `model: "fable"`, and Codex in the background from the root of `<tree>`.
   Both get this prompt:

   ```
   Read <dir>/instructions-lens.md and do what it says.
   Tree: <tree>
   You are one reviewer that another agent runs: start no skill, change no file, and file nothing.
   ```

   For Codex, write the prompt to a new file with the Write tool, in the
   session's scratchpad directory, or in a new folder from `mktemp -d` when
   there is none, and give Codex the file. The prompt never goes
   into a shell command: text from outside can hold a line that ends it.

   ```bash
   bash <skills>/review-loop/scripts/time-limit.sh 1200 codex exec -s read-only --ephemeral -C <tree> - < <file>
   ```

   When there is no `codex` command, `codex login status` fails, or the run
   fails, go on with Fable alone, and say so in the report. In Codex, do the
   job of `instructions-lens.md` yourself. A finding that both readers give
   counts once. Read the two places of each finding, and drop one that they
   do not bear out. With a scope, keep a finding only when one of its
   places is under the scope. The findings that hold are one place.

## Choose the places

A place is one fix: a file to split, a broken rule, the clones that one
shared helper removes, or a piece of over-engineering to remove. The hits
of one `grep` rule, its `debt` hits included, are one place over several
files. Each path of a `lines` or `files` check is weighed as a place of its
own: a file with its own score, and a folder with the highest score of its
own files, not those of its subfolders, as the check counts them. Rank the
places by their file's score from `measure.sh`: a
broken rule takes the importer's score, and a place over several files —
the hits of one rule, clones, a dependency and its importers, a bundled
finding — the highest of its files. A file outside the table gets its score
from `measure.sh <file>`.

The findings of step 5 are one place of their own: it has no score, and it
does not count towards the three below. The `## Where` of its issue starts
with the line `Instruction files.`, and an open debt issue whose `## Where`
starts with that line covers it. Its re-measure, below, writes the issue
again from this run's findings and the old findings outside the scope, and
ends it with the line of a re-measure.

A hotspot, a file or a folder from a `debt` hit of a `lines` or `files`
check included, is a place only when it holds more than one concern, the
split can be named, and no rule of the files of step 2 keeps it whole. For
example, a rule that puts all of a module's rules in its service keeps that
service whole. A high score alone is not a place: a short file
that changes often, a large file of one concern, or a file that a rule keeps
whole goes into *next*, with the rule quoted.

Then read what already covers each place. `collect.sh filing` from the
`craft:github` skill (`<skills>/github/tracker.md`), with the place's
files and symbols, finds every issue that names them, closed ones too. When
the scout asks for `path:line`, give paths only: a debt issue names no line.
Sort the hits as `filing.md` does — *Already decided*, as a closed issue that
settles a size cap or a layout; *Already filed*; *Fixed before* — and then:

- **An open debt issue** whose `## Where` names the same file covers it. A
  directory or a whole app named there does not. A folder of a `files` check
  is covered only by an issue whose `## Where` names the same folder as its
  place. That issue covers no file in the folder, and the issue of a file in
  it does not cover the folder. Re-measure the issue that covers the place: put this run's
  table in its `## Where`, in place of the old one or as the first, end the
  body with "Re-measured on <date> at <sha>.", and comment one line on what
  moved. It does not count towards the three. A busy issue, by
  `<skills>/github/tracker.md`, or a parent with open steps, is named in the
  report and not edited.
- **An open issue with another label** that already proposes the same change:
  name it in the report, and file nothing.
- **An issue closed as not planned:** name it in the report, and do not file
  the place again.
- **File the three highest of the rest.** Give the others in the report as
  *next*, with their scores.

When nothing is left, file nothing, and say what was measured and why nothing
qualified.

## The label

The label is `debt`, or the repository's own name for it in `gh label list`.
When there is neither, create it once:
`gh label create debt --description "Structural debt to refactor" --color 5319e7`.
An agent that files a debt finding through `filing.md` creates the label the
same way.

## The issue

The title states the problem as a sentence: "`collect.sh` holds four jobs in
315 lines and changes in every take-in fix". The issue gets the `debt` label
and no assignee. Its body has these parts, each under its own `##` heading, in
at most 600 words, tables and code blocks not counted:

1. `## Where`: the rows of `measure.sh` for the place's files, and the
   "Measured on" line of the scope's run. A folder of a `files` check is
   named as the place by its path, above the rows of its own files. No line
   numbers: a hot file's lines
   move with the next pull request, and the SHA dates the evidence.
2. `## What is broken`: the rule, quoted with its file and heading, or with
   its `I-<n>` for an invariant, or the
   measurement that makes the place a hotspot. The evidence names each file
   and symbol, with the command and its count. A clone is named by its two
   files and its length in lines, from `clones.sh`, without its line ranges.
3. `## The split`: the modules after the change, and what each one owns.
4. `## The order`: one pull request per step, each with the tests and checks
   that prove it unchanged, by name. Run none of them here: their counts belong
   to the step's own pull request.
5. `## Risks`: what can break, and which test would show it.
6. `## Out of scope`.

The issue of the instruction files has the same parts. Its `## Where` starts
with the line `Instruction files.`, then names the places of each finding, by
path and heading, in place of the rows of `measure.sh`. Its `## The split`
gives the fix that the readers name for each finding, by step 4 of
`instructions-lens.md`. No fix of a repeat or a contradiction takes a rule
from a host: Claude Code reads the `CLAUDE.md` files, and Codex the
`AGENTS.md` files. So the text stays in a file that the host reads, or the
root file of the host gets the line that points to the architecture file, as
`first-file.md` of `craft:architecture` gives it. Its `## The order`
names the files whose citations the fix corrects, and puts each
contradiction that a person must choose into a step of its own: when the
choice is architectural, that step writes an ADR through
`craft:architecture`.

The last line is "Found by `craft:debt` on <date> at <sha>." Another
open issue on the same code is named in the body, and its side is corrected
as `filing.md` says under *Filing one next to an existing issue*. A closed
issue on the same code that does not settle the place is named as history.

## Steps

A place that takes more than one pull request is a parent issue, and each step
a sub-issue labelled `debt`, at most 150 words: "Part of #<parent>, step
<n>.", then what moves, where the pull request ends, and what proves it. File
the parent first, then each step in order, and link each one as it is filed,
with the roadmap skill's script:

```bash
bash <skills>/roadmap/scripts/plan.sh sub <parent> <step>
bash <skills>/roadmap/scripts/plan.sh block <step> <the step before>
```

Set no "blocked by" on an issue the map did not file: that order is a
person's call. When a call fails half way, stop, and report what was filed
and linked so far.

## The report

The issues filed, re-measured and named, with their numbers and titles; *next*, with
scores; the borderline hits; the invariants with no `Check:` line; the
invariants that an exit 2 of `invariants.sh` left unchecked, with its
messages; the copies kept on purpose; the small cuts, one line each with the score of
the file it names, or of its highest file; the ponytail findings dropped, with
the rule; the lines the kept findings would save, marked as your estimate,
not ponytail's own `net:`; the findings of step 5 that their places did not
bear out, and whether Codex read; the steps skipped and
why; the share of moved code files when it was large; the SHA measured, and
that it was `HEAD` when it was.
