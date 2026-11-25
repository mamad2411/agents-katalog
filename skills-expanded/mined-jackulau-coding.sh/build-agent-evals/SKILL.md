---
name: build-agent-evals
description: "Builds eval suites with coding.sh from failed agent sessions, a skill's trigger prompts or cases you write, and reads paired comparisons of two runs. Use when the user wants an eval or regression test for their agent, wants to turn a failed session into a test, wants to check that a skill loads when it should, or asks which of two prompts, harnesses or models did better."
license: MIT
---

# Build evals for an agent

Uses the coding.sh MCP server's eval tools. `eval_init` writes files under `evals/` in the repo and
`eval_from_session` writes to the local coding.sh store. Ask the user before either, then pass
`confirm: true`.

## Pick the source

| The user wants | Call |
|---|---|
| Tests from runs that went wrong | `eval_candidates`, then `eval_init` (`source: "sessions"`) |
| One session as a task | `eval_from_session` |
| To check that a skill loads when it should | `eval_init` (`source: "skill"`) |
| Cases for an app or a prompt | `eval_init` (`source: "cases"`) |

Every `eval_init` call needs `name` (the suite's folder under `evals/`), `source` and
`confirm: true`.

## From failed sessions

1. Call `eval_candidates`. It ranks this repo's recent sessions by how good a task each would make
   and rejects the ones that cannot be replayed; `rejectedBy` counts them by reason.
2. Show the user the top candidates and the verifier you propose. A verifier is a shell command
   that exits 0 only when the task is solved, such as `npm test`.
3. After the user agrees, call `eval_init` with `name`, `source: "sessions"`, `sessionIds`,
   `verifier` and `confirm: true`.

## For a skill

1. Write prompts that should load the skill, 10 or more, and near misses that should not: requests
   that sound close but belong to another skill or to none.
2. After the user agrees, call `eval_init` with `name`, `source: "skill"`, `skill` (the skill's
   directory), `should`, `shouldNot` and `confirm: true`.

## From cases

1. Write the cases, each with an `input`. Give `expected` when a case has one exact answer.
   Otherwise write a `description`: it says what a good answer does and becomes the judge's rubric.
2. Find what answers a case: a `command` (it reads the input as JSON on stdin) or a `url`.
3. After the user agrees, call `eval_init` with `name`, `source: "cases"`, `cases`, the `command`
   or `url`, the `description` if you wrote one, and `confirm: true`.

## One session as a task

After the user agrees, call `eval_from_session` with `sessionId` and `confirm: true`. Pass
`verifier` when you know the command that proves the task is solved.

## After it is written

- Give the user the `run` command from the result. Do not run it yourself: it starts agent runs
  that take minutes and can cost money.
- When the result has `todo: true` or `notes`, tell the user what is left to fill in.
- When the result has `ci`, offer it: it is the workflow that runs the suite on pull requests.

## Compare two runs

1. Call `experiments_list` to find the two experiments.
2. Call `experiment_compare` with `baseline` and `candidate`.
3. Give the verdict with the pass-rate difference and its interval, then the regressed and
   improved cases. When it reports a power warning, say the result needs more cases or trials.
4. Do not call a difference real when its interval includes zero.
