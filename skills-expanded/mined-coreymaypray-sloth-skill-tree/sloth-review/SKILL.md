---
name: sloth-review
description: "Use when completing a task or major feature on a Maycrest build, or before merging — dispatch an independent reviewer subagent as the internal QA gate before the client sees the work."
---

# Sloth Review — The Internal QA Gate 🦥

## Overview

Before any Maycrest work reaches the client, an independent reviewer subagent catches issues
while they're cheap. The reviewer gets precisely crafted context for evaluation — never your
session's history. That keeps it focused on the work product, not your thought process, and
preserves your own context for continued work.

**Core principle:** Review early, review often. The client never sees an unreviewed build.

## When to Request Review

**Mandatory:**
- After each task in [sloth-build](../sloth-build/SKILL.md)
- After completing a major feature
- Before merging to main

**Optional but valuable:** when stuck (fresh perspective), before refactoring (baseline check),
after fixing a complex bug.

## How to Request

**1. Get the commit range:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)   # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch the reviewer subagent** (Task tool, `general-purpose`). Craft its context inline —
this skill is standalone, so give it exactly:

- **What you built** — one or two sentences of plain description.
- **What it should do** — the task spec or requirements it's measured against.
- **Commit range** — `BASE_SHA`..`HEAD_SHA` so it reviews only the relevant diff.
- **What to check** — correctness against the requirements; test quality (real assertions, tests
  that were watched failing, not theater); readability and naming; duplication; error handling;
  magic numbers; scope (nothing missing, nothing unrequested).
- **How to report** — strengths, then issues tagged **Critical / Important / Minor**, then a
  clear approve-or-iterate verdict.

Do NOT hand the reviewer your chat history or reasoning — only the work product and the bar.

**3. Act on feedback:**
- Fix **Critical** immediately.
- Fix **Important** before proceeding.
- Note **Minor** for later.
- Push back if the reviewer is wrong — with technical reasoning and code/tests that prove it.

## Example: Maycrest website contact form

```
[Just completed: server-side validation on the /contact route]

You: Review before this ships to the client.

BASE_SHA=$(git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch reviewer subagent]
  WHAT YOU BUILT: Server-side validation + rate limiting on the contact API route
  WHAT IT SHOULD DO: Reject empty/invalid email, cap submissions per IP, return field errors
  RANGE: a7981ec..3df7661
  CHECK: correctness, test quality, error handling, scope

[Reviewer returns]
  Strengths: Clean Zod schema, real failing-first tests
  Issues:
    Important: Rate limit resets on server restart (in-memory only)
    Minor: Magic number (5) for max attempts
  Verdict: Iterate on the rate-limit store, then ready

You: [Move rate limit to Upstash; extract MAX_ATTEMPTS]
[Re-review → approved → proceed]
```

## Integration with Workflows

- **[sloth-build](../sloth-build/SKILL.md):** review after EACH task — catch issues before they compound.
- **Executing plans:** review at each task or natural checkpoint; apply feedback, continue.
- **Ad-hoc work:** review before merge, and when stuck.

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If the reviewer is wrong:** push back with technical reasoning, show the code/tests that prove
it works, or request clarification — don't perform agreement and don't blindly comply.

## Integration with the Maycrest roster

- The receiving side of feedback is [sloth-receive-review](../sloth-receive-review/SKILL.md) —
  rigor, not performative agreement.
- This is the per-task gate inside [sloth-build](../sloth-build/SKILL.md).
- Confirm fixes hold with [sloth-verify](../sloth-verify/SKILL.md) before [sloth-ship](../sloth-ship/SKILL.md).
- For the final production sign-off, escalate to `maycrest-ops:reality-checker`.

---
*Adapted from the MIT-licensed [obra/superpowers](https://github.com/obra/superpowers) project (© 2025 Jesse Vincent). See [NOTICE](../../NOTICE).*
