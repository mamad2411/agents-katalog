---
name: codependix-triage
description: Act on a codependix run that failed or reported drift — a boundary violation, a --check reports run that found stale exports, a project that failed its export, a missing anchor block, a NestJS container that failed to boot, a rejected command line, or a --write that produced no files at all. Use when codependix exits non-zero, when an edge or a cycle breaks a declared rule, when a committed Mermaid block disagrees with a fresh run, when a graph export is missing for one project but not others, or before hand-editing an exported diagram or loosening a rule to make a check pass.
license: MIT
---

# Acting on a codependix failure

Codependix reports a handful of distinct outcomes, and reading which one
occurred is most of the work. Start by separating them: a **boundary
violation** is a real edge in real code, a **stale export** is drift, a
**failure** is a project that never got as far as producing one, and a run that
wrote nothing at all is usually neither.

## A boundary violation

`--check boundaries` found an edge, or a cycle, that a declared rule
condemns. Each violation names the graph level, the scope it was found in, the
rule, both endpoints, and whatever the rule says about why it exists.

**This is the one finding a re-run never fixes.** Nothing is stale and nothing
needs regenerating: the edge is in the code, and one of two things has to give.

1. **Remove the edge.** Usually the right answer, and usually smaller than it
   looks — move a type into a `*.types.ts` file, invert a dependency, or lift
   a shared piece into a package both ends may reach.
2. **Change the rule**, when the rule is what is wrong. That is a deliberate
   decision to write down in `codependix.config.ts`, with the reason, not a
   quiet widening of a selector until the run goes green.

Never narrow a selector, add an exclusion, or delete a rule purely to make a
failing check pass. A gate loosened to pass is a gate that no longer protects
anything, and the next reader has no way to tell it was ever meant to.

If the violation is at the `nx` level and mentions an edge with no import
statement behind it, that is the point of the level: an
`implicitDependencies` entry is a real project-graph edge, and
`@nx/enforce-module-boundaries` cannot see it. Remove the entry, or the rule
has to change.

## A stale `--check reports`

One or more configured exports disagree with a freshly built graph. The run
names the projects.

**Re-run `--write`. That is the entire fix.** The graphs move with the
workspace they describe, so a project graph that changed makes every export
that drew it stale — which is drift to refresh, not a defect to investigate.

**Never hand-edit inside the anchor markers.** The next `--write` replaces the
block wholesale, so an edited diagram is a diff that silently disappears on the
following run. The same goes for a standalone Markdown file: codependix owns
its whole contents.

Two more things a stale check does _not_ mean:

- **It is not a conformetry conformance difference.** The `codependix:start` /
  `codependix:end` markers are codependix's own syntax and carry no dependency
  on any `conformetry-*` package. Running a conformance check, or reaching for a
  conformetry generator, fixes nothing here.
- **It is not evidence of a missing anchor.** A project that has never been
  exported has no block to compare, and reports stale like any other drift.

## A project that failed

A failure is collected per project and reported by name. **One project failing
does not stop the rest** — every remaining project in that pass still runs, and
all four graph-type passes are attempted regardless of whether an earlier one
failed. So a run naming three failures is three things to fix, not one flaky
run to retry.

### The Markdown file does not exist

The only anchor problem that fails outright. A **missing anchor block** is
auto-created on `--write`; a **missing file** is not, because a project with no
readme at all is a more serious problem than an unplaced block, and inventing
the file would mean authoring a document nobody asked for.

Create the file — a project readme with at least a heading — and re-run.

### A missing anchor block, on `--write`

Not a failure. `--write` creates it, at one of exactly two safe places:

- Appended to the end of the file as a new `## 🕸️ Codependix` section, with an
  intro line and a `### <Subheading>` for the graph type.
- Inserted as a new `### <Subheading>` at the end of an existing
  `## 🕸️ Codependix` section, when an earlier graph type already created one.

It never places a block anywhere else in a document someone else is authoring,
and never duplicates the heading. If the block landed somewhere you did not
want it, move the whole marker pair by hand once and every later `--write`
replaces the content in place.

### A NestJS project that failed to boot its container

The NestJS pass explores a project's container in **preview mode**, which
registers every module and provider without instantiating any of them. A
project building a `TypeOrmModule.forRootAsync` options factory never has a
database contacted, so what breaks this pass is always something that throws
while modules are being _registered_ — a module whose static `forRoot` argument
reads a variable that is absent, a top-level throw in a module file, or a
project whose root module does not export what the pass expects. Look there.

An application is rooted in `src/main.module.ts` and its `MainModule` export; a
library package with no such file is rooted in a synthetic module built from
every `*.module.ts` it defines, so a module file that cannot be imported on its
own fails a library that an application would not notice.

Two fixes that look plausible and are not: starting or seeding a database (the
pass never contacts one), and building the project first (it imports the
project's own TypeScript module sources directly).

If the CLI is being run from TypeScript sources through some other loader,
check that decorator metadata survives it: NestJS constructor injection reads
metadata that plain type-stripping erases, and the failure looks like a
container that cannot resolve its own providers. The published `codependix`
binary registers a decorator-preserving loader itself; a hand-rolled invocation
has to do the same.

## A rejected command line

`--check` takes a comma-separated set drawn from `boundaries` and `reports`,
and the whole command line is read before anything else happens:

- **`--check needs a value`** — a bare `--check`, or one whose value is only
  separators. Name the set; do not drop the flag. Read as "gate nothing" it
  would be a gate that cannot fail.
- **`--check does not accept "..."`** — a name from another tool. `limits` is
  codometer's and `depth` is callidescope's; only `reports` is shared.
- **`--write cannot be combined with --check reports`** — an export cannot be
  stale in the run that just wrote it. `--write --check boundaries` is legal.
- **Naming neither `--check` nor `--write`** is asked about at a terminal, and
  refused everywhere else — including any run an agent or a CI job makes,
  since neither has a terminal to answer on. Nothing is inferred and no
  default write happens.

Every mistake on one command line is collected before any is reported, so two
complaints are two things to fix rather than two runs.

The command is `codependix map`, not bare `codependix`: a command line with no
subcommand is rejected by the argument parser before any of this applies.

## A `--write` that produced no files

The quietest outcome, and almost never a bug: the run exits 0, reports that
every configured export is current, and writes nothing, because **nothing was
configured**. Every unset `target` defaults to `"none"`, and a project
resolving to `"none"` is left out of the results entirely rather than reported
as up to date — so `0` projects in the report means codependix was configured
to produce nothing.

Work down this list before suspecting the tool:

1. **Was a configuration file found at all?** An absent one is legal and
   silent. Name it with `--config` to make its absence fail loudly instead.
2. **Is `target` set?** A graph type carrying destinations but no `target`
   still resolves to `"none"`.
3. **Is the field spelled `defaults`?** `default` is stripped as an unknown
   key and has no effect.
4. **Does the configuration name an `include` at all?** It defaults to
   nothing, so a configuration naming only `defaults` selects no project and
   exports nothing. The run warns — `🕸️ Selected no project to export` — and
   still exits zero, and `--check boundaries` stays green either way, because
   it judges every project regardless of `include`. Write `include: ["**"]`
   for whole-workspace coverage.
5. **Do the projects match `include`, and escape `exclude`?** Both match
   against a project's Nx name _and_ its workspace-relative root.
6. **Is `--directory` the workspace root?** It is what every project's path
   resolves against, not a subtree to scan — Nx resolves the graph itself from
   the process working directory. Pointed at a single project's folder, the
   run still reads the whole graph but resolves every project underneath that
   folder, so exports land somewhere unexpected or fail on a readme that is
   not there.

The `codependix-configure` skill covers each of those fields.

## A configuration that was rejected

Validation refuses two destination mismatches rather than silently exporting
half of what was asked for: a `"both"` or `"json"` target with no `json`
destination, and a `"both"` or `"markdown"` target with no `markdown`
destination. A `markdown` destination naming neither an `anchor` nor a `path`
is refused for the same reason — nothing would say where the export goes.

## Whose problem the graph is

A finished export is a description, not a verdict — an export gates nothing
about a codebase's shape, and only a declared boundary rule does. A diagram
that shows something alarming (a cycle, a project depending on far more than
expected) is a real finding about the code even when no rule condemns it, and
the fix belongs in the code rather than in the configuration that exported
it. Reach for the `codependix-navigate` skill to read what the graph is
actually saying before changing anything.
