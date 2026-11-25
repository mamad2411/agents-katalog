---
name: write-ai-docs
description: Create and maintain the numbered design and decision records under docs/ai/ (000-plan.md or 000-investigation.md before the work, 001-action.md after, numbered amendments for follow-ups). Use when you start a substantial feature, a cross-cutting change, or a non-trivial root-cause fix in sim-use, when an investigation ends in a decision, or when a later change revises a decision that a docs/ai entry recorded. Do not use for typo fixes, dependency bumps, test-only changes, or status reports.
---

# Write AI docs

sim-use uses AI-docs-driven development. A substantial change starts with a
record in `docs/ai/`, and each decision is written down when it is made, not
reconstructed later. The record answers "why is it built this way?" for the
next human or agent. Read `docs/ai/README.md` first: it has the index and the
folder layout.

## When to write

A **new entry** (`docs/ai/NNN-<slug>/`) is necessary when the work:

- adds a verb, a platform, a transport, or a backend, or changes how a verb
  reaches a device (dispatch, daemon, HID transport, bridge);
- changes a contract: the daemon wire protocol, the bridge wire protocol
  (`PROTOCOL_VERSION`), the `--json` envelope, the bundled skill's compatibility
  floor (`MINIMUM_SIM_USE_VERSION`), or the host-environment matrix;
- starts as an investigation (a new Xcode, a reproducible failure, an upstream
  idb change) and ends in a decision;
- fixes a bug whose root cause or fix shape must guide later code (for example,
  "HID from a short-lived process is lost on the dtuhidd transport").

An **amendment** to an existing entry is necessary when follow-up work, a
review round, or a later finding changes what the entry says. Look for an
existing entry on the topic before you open a new one.

**No record** is necessary for typo or formatting fixes, dependency bumps,
test-only or fixture-only changes, small fixes that need no separate design
record, reviews, and status reports. Keep changelog entries focused on user
impact, not root-cause detail. If you are not sure, ask: will someone later
need the reasoning to change this code safely? If yes, write it down.

## Workflow

### 1. New entry: plan first

1. Get the next number: `ls docs/ai | sort`, then take the highest `NNN` + 1
   (three digits). Numbers are never reused.
2. Before you write code, create `docs/ai/NNN-<kebab-slug>/000-plan.md` from
   the template below, with `Status: Planned`. Use `000-investigation.md` when
   the work starts as a root-cause hunt: record the reproduction, the evidence
   and the hypotheses, then the decision.
3. Add the entry to the index table in `docs/ai/README.md`.
4. Implement the work in the normal branch and PR flow. When you make a
   decision that the plan did not foresee, record it at once in the plan's
   **Decisions** table, or in an amendment.
5. After the work lands, write `001-action.md`: what shipped, the PRs, the key
   files, and the deviations from the plan. Set the plan status to
   `Implemented`. Ship the docs in the same PR as the code when you can.

### 2. Follow-up on an existing entry

1. Add the next free numbered file in the folder, for example
   `002-review-round-1.md`. `001` is the action log when the entry has one; a
   design or investigation record that already holds its outcome has no
   action log, and its first amendment is `001-<topic>.md`.
2. Append one line to the **Amendments** section of the `000-*.md` file:
   `- Updated YYYY-MM-DD: <one line> — see [00N-topic.md](00N-topic.md)`.
3. When the follow-up makes earlier text wrong, add a dated note at the top
   of that file. The note says what is no longer true and where the
   correction is. Keep the original measurements; do not silently rewrite
   them.

### 3. Pivot

When a change replaces the approach of an entry instead of extending it, open
a new entry, link the two entries in both directions, and set the old status
to `Superseded by [NNN-new-slug](../NNN-new-slug/000-plan.md)`.

## Templates

### 000-plan.md

```markdown
# NNN — <Title>: Plan

| | |
| --- | --- |
| **Status** | Planned \| In progress \| Implemented \| Superseded by <link> |
| **Anchor date** | YYYY-MM-DD |
| **Primary PRs** | #a, #b (fill in as they merge) |
| **Related** | issue #n, [NNN-other](../NNN-other/000-plan.md) |

## Background
The problem and its context. For a fix: the observed symptom and the environment
(Xcode, iOS or Android version, Device Hub open or closed).

## Goals
Bullets. Add **Non-goals** when the scope exclusion is a real decision.

## Design
The approach. Name the types and files that it touches.

## Alternatives & decisions
| Decision | Options considered | Chosen because |
| --- | --- | --- |

## Verification plan
Which `make test`, E2E suites, matrix legs, live checks or evals prove it.

## Amendments
```

### 000-investigation.md

Use the plan template, but replace **Design** with these sections:
**Reproduction** (exact commands), **Evidence** (measurements, logs, with the
command that produced each one), **Hypotheses** (each one confirmed or ruled
out, and how), and **Root cause**. End with **Decision**.

### 001-action.md

```markdown
# NNN — <Title>: Action log

## Timeline
| Date | Change | Ref |
| --- | --- | --- |

## Outcome (as of YYYY-MM-DD)
What exists in the code now. Key files and types, with repo-relative paths.

## Verification
What was run and what it showed. Only results that you produced.

## Deviations from plan
Where the work diverged from 000-plan.md, or "None."

## Open questions
Claims not verified, follow-ups, related issues, or "None."
```

### Amendment (002 and later)

```markdown
# NNN.00M — <Topic>

## Context
Why this follow-up happened.

## Change
What was decided or done, and why. Refs: PR #x.
```

## Writing rules

- Write in English that follows ASD-STE100. Be factual. Prefer tables for
  timelines, options and measurements. A plan is usually 40–150 lines; an
  investigation can be longer when the evidence needs it.
- Every repo-relative path, type and symbol that you name must exist. Check
  with a search before you write it. Put claims that you cannot verify under
  **Open questions**.
- Give evidence that can be reproduced: the command, the environment, and the
  measured number. Do not state build, test or eval results that you did not
  produce.
- The repository is public (github.com/lycorp-jp/sim-use). Do not add internal
  hostnames, internal ticket links, credentials or customer data. Refer to
  pull requests as `#123` and to upstream idb pull requests as `facebook/idb#123`.
- Link sibling entries with relative links. When code is shaped by a
  non-obvious decision, point to the record from the code comment, for example
  `/// Work record: docs/ai/009-resizable-app-session/000-investigation.md`.
- A file without a number in an entry folder is a living document (a guide, a
  runbook, a contract), for example `008-linux-android-build/linux-guide.md`.
  Update it in place when the behavior changes, and link to it instead of
  copying its content.
- Current behavior for users and agents goes in `README.md`, `AGENTS.md` and
  `skills/sim-use/`. User-facing release notes go in `CHANGELOG.md`. The reasons
  go in `docs/ai/`. These may link to an entry, but they must not depend on it
  for current behavior.
- After you add, rename or supersede an entry, update its row in the
  `docs/ai/README.md` index.
