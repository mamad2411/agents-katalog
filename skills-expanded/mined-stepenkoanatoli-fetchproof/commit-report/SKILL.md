---
name: commit-report
description: Writes the five-part commit report the standing protocol requires - what changed, why, what it touched, what was verified, and what was gotten wrong and fixed - with a status word (verified, untested, expected) on every verification claim and six fields per mistake, and the got-wrong line never omitted. Use for every commit or pull request in a Fetchproof project, when the user asks for a commit message, a PR description or a status summary.
---

# Commit report

Someone who never saw the brief that produced the work must be able to read it.

## The five parts, named

- **What changed** - the modules and the shape of the change.
- **Why** - the defect, decision or order that made it necessary; any alternative set
  aside (a design choice with a rejected alternative also gets an ADR - `adr-writer`).
- **What it touched** - the files, the architecture-map rows and ADRs it owes, the domain
  terms it added or sharpened.
- **What you verified** - each command and its state, each with one word:
  - **verified** - run, and the result seen;
  - **untested** - written, not run;
  - **expected** - reasoned, not run.
- **What you got wrong and fixed** - each mistake in six fields: **mistake**, **where**
  (file and line, or the step), **impact** (what it broke or would have broken, and
  whether anything delivered is affected), **cause** (one line), **fix**, **verified**
  (the command re-run, and its result). If there was none: "nothing to report" - never
  omitted.

## The short form

A commit that touches no declared code path (`research/kit.json`) - tests, docs, wording,
a fixture - may carry one line each: what changed, why, what you verified, what you got
wrong.

## Rules

- One commit per task: `git revert <sha>` undoes it alone.
- Never `--no-verify`. A red suite stops work and is reported first, alone, with the cwd.
