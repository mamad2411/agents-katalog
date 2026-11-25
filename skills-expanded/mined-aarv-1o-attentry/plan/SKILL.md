---
name: plan
description: Check a plan against the repo with Attentry before building it. Use when the person asks to check, review or share a plan with Attentry, or after writing a plan and before starting on it.
argument-hint: "[the plan, or leave empty for the current one]"
---

Send the plan to Attentry's `check_plan` tool as `plan`: $ARGUMENTS, or, when that's empty, the
plan from this conversation in full (write it out first if there isn't one yet). Name functions in
backticks and routes as `GET /path`, so Attentry can match them.

- For each note, change the plan: reuse the function it names, extend the route that exists, split
  a plan that's too big. Then show the person the changed plan in a few lines.
- When it says "go ahead", say so in one line and continue.
