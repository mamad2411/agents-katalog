---
name: prune-comments
description: Audit code comments and plan which to delete, keep, rewrite or replace with a refactor. Use when asked to prune a codebase's comments, or to sort workaround comments into root-cause fixes and safe deletions.
---

# Prune comments

Agents copy what a codebase already does, so every comment is a _precedent_.
A comment that narrates the code teaches narration; one that excuses a
temporary workaround teaches that workarounds are fine here. Prune until the
comments that remain are precedents worth copying: each says what the code
cannot.

The first deliverable is a plan. Edit code only after the user approves it.

## 1. Scope

Use the scope the user gave; with several apps and no hint, ask which. Cover
files tracked by git and any untracked file the user names, marked as
untracked, and report the revision you read. Leave out generated,
vendored and third-party code, lockfiles, snapshots and test fixtures, and
say what you left out.

Read the repository's own comment rules (`AGENTS.md`, CONTRIBUTING, lint
config that requires doc comments). They override this skill. Then list the
tools that read comments here: linters, type checkers, bundler, coverage,
test runner, codegen, migrations, i18n extraction, docs build.

Find comments with a parser: `ast-grep` with `kind: comment`, or the
language's own. `kind: comment` misses docstrings (string nodes in Python)
and doc attributes (`#[doc]`, `@doc`); query those too. List a file with no
parser for its language as unparsed: text search also matches `#` and `//`
in strings, URLs and `${#arr}`.

Done when every in-scope file is parsed or listed as unparsed.

## 2. Classify every comment

Give each comment one verdict. Judge it against the code it constrains, the
history of those lines (`git log -L`, `git blame`) and any linked issue.
When several verdicts fit, the first in this order wins: Keep, Rewrite,
Refactor, Delete. Judge a block claim by claim: a comment with one narrating
line and one constraint is a Rewrite.

**Keep**: the comment says what the code cannot, or a tool reads it.

- An external quirk: browser, OS, runtime, library or API behaviour, with a
  link or version.
- A constraint (ordering, concurrency, security, performance, protocol) and
  what breaks without it.
- Why the obvious alternative was rejected.
- API docs that another file, an editor or a doc site reads: parameters,
  results, errors, `@deprecated`, doctests. They say _what_ by design.
- A comment a tool reads, in the form that tool requires: suppressions,
  pragmas and directives (`//go:`, `# frozen_string_literal:`, `@__PURE__`,
  `webpackChunkName`, SQL hints), migration and coverage markers, translator
  notes, shebangs, license and SPDX headers, generated-file markers. A
  comment shaped like a directive whose reader you cannot name is Keep.
- The only body of a block: an empty `catch`, `else` or stub.
- Commented examples and disabled options in config files, templates and
  `.env.example`: they document that file.
- A TODO or FIXME that cites a ticket, or names a defect that is still real.
  The plan lists a ticket to file for the latter.

**Rewrite**: the comment should exist but is vague or wrong. Give the
replacement text. On API docs, correct the claim and keep the contract. A
suppression without a reason gets one in the tool's own syntax
(`// eslint-disable-next-line rule -- reason`). When comment and code
disagree, first check whether the code regressed; a regression is a ticket.

**Refactor**: the code can carry the comment's whole content, through a name,
an extracted function, a named constant, or a type for "may be null" and
"call init first". The comment goes in the same change. Renaming an
exported, serialised or reflected name, replacing a runtime check with a
type, or extracting a block that moves `return`, `break` or `this` changes
behaviour; the plan marks it.

**Delete**: nothing above fits, and removing it loses nothing.

- It restates the code or narrates the next line.
- Commented-out code from a live path; git keeps it.
- Change history and authorship that give no reason.
- Section banners in a file short enough to read whole.
- A TODO or FIXME whose reason is gone.

### Workarounds

Decide each workaround or hack comment together with the code it excuses:

- **Cause in this repository**: Refactor to fix the root cause. If that fix
  is too large, the code stays and the comment is rewritten to name the
  cause and a ticket.
- **External cause, present on any version the project supports**: Keep, and
  make the comment name the cause.
- **External cause gone on every supported version**: delete the code and
  the comment. Check the supported range (lockfile, `engines`, browserslist,
  CI matrix), not the copy installed here. A check that still enforces a
  security or protocol rule stays, with a comment that states the rule.

Done when every comment found in step 1 has a verdict or is listed as
unreviewed with the reason. On a large codebase, use patterns and samples to
find and count candidates, and still read each Delete in its context. Check
history for workarounds, TODOs and comments that look stale. Report sampled
estimates apart from reviewed counts.

## 3. Plan

Write in the user's language:

1. Summary: reviewed counts per verdict and area, estimates marked as such,
   and what was not covered.
2. Workarounds, as a table: `path:line`, cause, what happens to the code
   (delete / refactor / keep), to the comment (delete / rewrite / keep),
   effort (S/M/L), behaviour change, and the check that proves it safe.
   Group items that share one fix.
3. Other refactors, with the same fields.
4. Delete, grouped by pattern: count and two or three examples.
5. Rewrite: `path:line`, current text, replacement.
6. Keep: the patterns kept and why, with an example each.
7. Tickets to file.

Then ask which parts to apply.

## 4. Apply, when asked

Before the first batch, run the checks once as the baseline: formatter in
check mode, linter, type check, tests, and the tools from step 1 that read
the comments being removed (build, docs build, coverage, i18n extraction,
codegen). With uncommitted changes in the tree, run the tools that write
files (build, codegen, i18n extraction) in a copy of the tree that includes
those changes and each applied batch, or ask first. Confirm each approved item still points at the same comment; a
moved one goes back to unreviewed. Leave files with the user's uncommitted
changes untouched, and commit only when the user or the project's workflow
asks for it.

Order: comment deletions one pattern per batch, then rewrites, then each
refactor and each removal of workaround code as its own change with a test
for the case it handled.

After each batch, rerun the checks and compare with the baseline. After a
deletion or rewrite batch, any difference, including a check that now
passes, means something read a removed comment: narrow the batch down to
that comment and restore it. A refactor or workaround change should pass
its own new test; any other difference is a regression to fix or revert.

Done when every approved item is applied or skipped with a reason and no
check differs from the baseline except the intended ones; report the checks
you could not run.

## 5. Keep it pruned

Offer a comment rule for the repository's `AGENTS.md` or `CLAUDE.md`, built
from the Keep patterns, for example:

> Comments say what the code cannot: an external quirk with a link, a
> constraint and what breaks without it, a rejected alternative, an API
> contract that other files or docs read. Comments a tool reads stay in the
> form it requires. Names, types and functions carry the rest. A TODO cites
> its ticket.

Add it only when the user agrees.
