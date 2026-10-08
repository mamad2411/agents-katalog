---
name: task-spec
description: Turn a rough request into a spec with acceptance criteria that can actually be checked. Use when starting a task in the claude-god pipeline, or whenever a request needs a testable definition of done before anyone writes code.
---

# Writing a spec

You are writing the contract the whole pipeline is judged against. A critic will
later pass or fail the work against exactly what you write here, so vagueness now
becomes an infinite review loop later.

## Method

1. **Explore before you write.** Read the code that the request touches. Never
   describe behaviour you have not verified in a file.
2. **State the goal in one sentence.** If you cannot, the request is two tasks.
   Say so.
3. **Write criteria as observable outcomes**, not implementation steps.
   "The handler validates input" is a step. "POST /orders with a missing `sku`
   returns 422 and does not write to the DB" is an outcome.
4. **Attach a check to every criterion.** This is the part that matters most.

## Checks

Every criterion gets one of three:

- `check: cmd \`<command>\`` — a shell command that exits 0 when satisfied.
  Strongly preferred. Use commands that exist in this repo *today* — read
  package.json / Makefile / pyproject.toml to confirm. If the test does not exist
  yet, still write the command: the implementer must create the test to make it pass.
- `check: review` — a critic agent reads the diff and decides. Use only when no
  command can decide it (naming, structure, a design match).
- `check: human` — only a person can confirm (visual polish, product feel).
  Use sparingly; these never block the automated loop.

If a criterion cannot take any check, it is not a criterion. Move it to
`## Out of scope` or `## Open questions`.

## Required output format

Write exactly one file: `spec.md`. Nothing else, no source changes.

```markdown
# Spec: <short title>

## Goal

One paragraph. What changes for the user when this is done.

## Context

What exists today, with real paths. What this must not break.

## Approach

Two to five sentences of the intended shape. Not a full plan.

## Acceptance criteria

- [ ] AC-1: <observable outcome>
      check: cmd `pytest tests/test_orders.py -k bad_payload`
      lane: be
- [ ] AC-2: <observable outcome>
      check: review
- [ ] AC-3: <observable outcome>
      check: human

## Out of scope

Explicit list. This is what stops the pipeline gold-plating.

## Open questions

Only if the request is genuinely ambiguous. Answer them yourself with a stated
assumption where you can; leave a question only when a wrong guess would waste the
whole build.
```

## Rules

- The parser reads `- [ ] AC-N: text` items under the `## Acceptance criteria`
  heading, with indented `check:` and `lane:` attributes. Keep that shape exactly.
- 4–10 criteria. Fewer means the contract is too loose; more means the task is too big.
- `lane:` only when the repo actually has multiple lanes, and only one lane per criterion.
- Never invent file paths, scripts or test names you did not verify.
