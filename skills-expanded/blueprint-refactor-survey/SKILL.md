---
name: blueprint-refactor-survey
description: "Find what is worth tidying in this repository, measure each candidate's value and risk, and write a plan the person approves — including what to leave alone and why."
---

# Choose what to touch

A campaign spends most of its risk here. A target chosen wrongly is a pull request, a CI run and a merge
spent on something that did not need doing — and a change nobody asked for is a change that can break
something. Read `.blueprint/answers.json` for the goals, the limit on changes, and what to avoid.

## What to optimise for

In order, because they conflict:

> **a decision made testable** > a block moved with its behaviour **proved** > a block moved with its
> behaviour **argued** > **a costed no**

The last beats the third. "A lint bound cleared" is not on the list: a bound tells you where to look,
never what good looks like. Readable beats short.

## Finding candidates

Use what the repository already measures, then read the code yourself:

- **Its own tools.** Run the lint (`max-lines-per-function`, `complexity` and friends), and any `knip` /
  `duplication` / `jscpd` script it has. They point; they do not decide.
- **Untested exports.** For each exported symbol, does any test name it?
  `grep -oE "^export (const|function|class) [A-Za-z0-9_]+" f.ts` then `grep -rlw <name> test/ src/`.
  A file with tests can still have untested exports — often the cheapest wins.
- **Pure logic trapped behind a heavy import** — a database client, an SDK that initialises on import, a
  DOM API. The logic is untestable for a reason unrelated to the logic; the fix is a move, not a rewrite.
  This is the highest-value shape there is.
- **What breaks if it is wrong**: money, a permission boundary, one user's data reaching another,
  anything printed on a receipt. Rank by this, not by line count.
- **One question answered in several places** — grep for the concept, not the symbol. Unifying them
  (one module, one test asserting they agree) is a correctness change, not a size change.

Skip what is easy to test but worth nothing: style constants, presentation values, a comparator's exact
magnitude. Pinning those buys a test that goes red when someone adjusts a layout.

## Measuring each candidate

- **Reachable?** Find the caller or renderer, not just an import (a type-only import or a test-only reader
  keeps a file "used"). For a branch that cannot fire today, `git log -S "<symbol>" -- <file that would
  supply it>` tells *dead since birth* (delete) from *broken later* (fix) — opposite changes.
- **Cost of a move = the mutable cells it writes that are read afterwards**, not its length. A region that
  writes none lifts as-is; one that writes four needs four write-backs, and dropping one still type-checks.
- **Adjacency invariants.** What holds only because two pieces of code sit next to each other — an order, a
  shared answer, no `await` between a write and its reader? Those have no home after a move.
- **Someone else in the file?** `gh pr list --state open` and `git log --oneline -20 -- <file>`.

## Writing the plan

1. `.blueprint/spec.md`, for the person, in the language the build's prompt says they read (without one, in Japanese). It opens with what approving it means:
   this build will create a branch, commit, push and open a pull request per target, and — if
   `merge` in the answers says so — merge each one once CI is green. Then, per target: what it is, why it is
   worth doing, how the change will be proved to behave the same, and what could go wrong. Then **what you
   chose not to do and why** (a costed no each), and what you did not look at.
2. `.blueprint/open-questions.md`: anything you could not decide. Empty is fine.
3. `.blueprint/targets.json`, the machine's copy, in the order they will be done:
   ```json
   { "targets": [
     { "id": "split-parse-order", "kind": "decompose", "title": "注文の解析を関数に分ける",
       "files": ["src/order.ts"], "why": "...", "proof": "replica differential over generated orders",
       "status": "todo" }
   ] }
   ```
   `kind` is one of `ci`, `decompose`, `dedupe`, `test`, `dead-code`, `types`, `other`. Every target starts
   `todo`. No more targets than `maxChanges`.
   - If `.blueprint/ci.json` lists gaps, the **first** target is a `ci` one that closes them: every later
     change is merged on CI's word, so CI has to be checking the gates before anything else moves.
   - Put a `test` target before a later target that needs a guard the code does not have yet.

One target is **one region and one pull request** — anything that could be reverted on its own is a
separate target.

Change nothing in the repository in this step.

Done when the check passes: the plan parses, every target is still to do, and there are no more than
the agreed number.

## Always

- Read `.blueprint/answers.json`. Do not plan anything in the places it says to avoid.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
