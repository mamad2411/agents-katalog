---
name: harness-scope
description: >-
  One feature at a time with clear done criteria — less half-finished work.
  Use when the agent does too much at once, rewrites the task list, or leaves
  features stuck in progress.
---

# Harness Scope

## What this does for you

- **One thing at a time** — only one feature `in_progress`
- **Done means observable** — verification steps a human can follow
- **Stable task list** — the agent follows priorities, not rewrites the plan

Agents over-scope and under-finish (Lesson 07). Feature lists are harness primitives (Lesson 08): machine-readable boundaries the agent cannot ignore.

## Scope rules

1. **One active feature** — only one with `status: "in_progress"`
2. **Explicit priority** — lower number = more urgent
3. **Observable behavior** — `user_visible_behavior` describes what the user sees
4. **Verification as contract** — concrete steps, not vague claims
5. **Do not rewrite the list** — adding features requires documented justification

## Feature anatomy

```json
{
  "id": "auth-001",
  "priority": 1,
  "area": "auth",
  "title": "Login with email and password",
  "user_visible_behavior": "User enters credentials and reaches the dashboard.",
  "status": "not_started",
  "verification": [
    "Open /login",
    "Enter valid credentials",
    "Verify redirect to /dashboard",
    "Verify error message with invalid credentials"
  ],
  "evidence": [],
  "notes": ""
}
```

## Feature selection

At session start:

```
1. Filter status != "passing"
2. Sort by priority ASC
3. Pick the first
4. Set its status to "in_progress"
5. Work ONLY on that feature
```

## Handling blockers

If a feature is blocked:

```json
{
  "status": "blocked",
  "notes": "Requires Stripe API key — see issue #42"
}
```

Do not jump to another feature without documenting the blocker. Do not mark partial work as `passing`.

## Support fixes

Changes outside the active feature scope only if:

- They unblock the current feature (narrow fix)
- They repair a broken verification baseline
- They are documented in `notes` or `progress.md`

## Create feature_list from scratch

1. List user-visible features (not internal tasks)
2. Order by dependency → priority
3. Write verification[] as steps a human can follow
4. Set global rules in the JSON

## Update workflow

```
Finish work on feature X:
  → Run verification[] for X
  → If pass: status="passing", evidence=[...]
  → If fail: fix or status="blocked"
  → Never: status="passing" without evidence
```

## Anti-patterns

- Three features `in_progress` at once
- Vague verification: "works correctly"
- Deleting incomplete features from the list
- Implementing priority 5 while priority 1 is still pending

## Templates

- [templates/feature-list.json](../../templates/feature-list.json)
- Schema: [templates/feature-list.schema.json](../../templates/feature-list.schema.json)

## Course reference

- Lesson 07: Why agents over-scope and under-finish
- Lesson 08: Why feature lists are harness primitives
- Project 04: Runtime feedback and scope control
