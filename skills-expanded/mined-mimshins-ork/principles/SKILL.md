---
name: principles
description: Use when deciding how to split work into an Ork workflow - which steps are programs, which are Claude sessions, where a person decides - so it costs less than doing it by hand and can't go wrong quietly.
---

# How Ork splits work

Ork exists to do long jobs for less than doing them by hand, and safely. Four
rules decide the shape of a workflow.

## 1. A program for what a program can do

A model turn is for judgment. Anything a program can decide, it should: run the
tests, read a pull request's state, count what changed, wait for CI.

- **A tool node** (`tool.shell`, `tool.git`, `tool.gh`, `tool.aws`) or an
  **`mcp.call`** does it with no session. With `output: { format: json }`, its
  answer routes the run: `when: "json.state == 'OPEN'"`.
- **`verify:`** on a session runs a check before its report counts, so a session
  can't claim success past failing tests. **`before:`** hands it what a program
  found, so it doesn't spend turns finding it.
- **`watch:`** waits on CI or a review with a program that looks every few
  seconds; hours of waiting cost nothing.
- **`notify:`** lets a program tell a running session what it found, with no
  model turn to carry the news.

## 2. Spend where it pays

- A small model and low effort for a narrow task (`model: claude-code.haiku`,
  `effort: low`); the large ones where thinking pays.
- `budgetUsd` on each session and on the run (`limits.budgetUsd`). A loop of
  sessions without a budget or `limits.timeout` gets a warning, for good reason.
- Give a session what it needs in its `prompt` and `before:`, rather than
  letting it search; and `isolation: readonly` for a reviewer that only reads.

## 3. Make a mistake impossible before checking for it

- Declare what a node says: `output.schema` lists on tool JSON and Claude
  reports (`verdict: [approve, escalate]`). Conditions then compare against a
  closed list, and a run fails a value off it rather than matching nothing.
- A verdict is a declared field, never words to search a summary for.
- Give each condition its opposite, and each failure a handler (`when: "!ok"`).
- Check every draft with Ork's `check` tool until it's clean.

## 4. A person decides what can't be undone

Merging, deploying, publishing, spending a lot: put a `human.gate` before it,
with the safe option `recommended`. For a run nobody watches, give it a
`timeout` and the safe `default`. You never answer a gate yourself.

## An example

A review that a program checks first, and a person signs off:

```yaml
schemaVersion: 1
name: careful-review
description: Lint with a program, review with a small model, and ask before merging.
inputs:
  pr:
    type: string
    required: true
limits:
  budgetUsd: 3
nodes:
  lint:
    type: tool.shell
    command: pnpm lint
    allow: [pnpm lint]
  review:
    type: agent.worker
    prompt: "Review pull request {{inputs.pr}}. The linter passed."
    model: claude-code.haiku
    effort: low
    isolation: readonly
    budgetUsd: 1
    output:
      schema:
        verdict: [approve, escalate]
  ask:
    type: human.gate
    question: "Merge pull request {{inputs.pr}}? The review says {{nodes.review.output.verdict}}."
    options: [merge, wait]
    recommended: wait
  merge:
    type: tool.gh
    command: pr merge {{inputs.pr}} --squash
    allow: [pr merge]
edges:
  - lint -> review
  - review -> ask
  - from: ask
    to: merge
    when: "choice == 'merge'"
```

`lint` costs nothing, `review` is a small model with a cap, and nothing merges
without a person.
