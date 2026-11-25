---
name: authoring-skills
description: "Use when the user asks to create, write, compose, or design a new agent skill — turning an idea, notes, requirement, or repeated workflow into a SKILL.md with eval cases and a trigger set through an interview → draft → critique → refine loop."
version: 0.2.0
---

# authoring-skills

## Intent

Turn a human's idea into a finished Agent Skill through a structured loop:
interview the human for the raw material, draft against the anatomy contract,
critique with a rubric of qualities no linter can check, and refine until the
harness — not taste — says the skill works. The using-shakespii skill teaches
how to drive the CLI; this skill decides what the new skill should say.

## Inputs

- The idea: a problem statement, requirement, or repeated workflow the human
  wants captured as a skill.
- A writable parent directory for the new skill.
- Optional: raw material the human already has — notes, transcripts, a real
  worked example, memory excerpts.

## Preconditions

- The shakespii CLI resolves (`shakespii --version` succeeds); setup lives in
  the using-shakespii skill's Preconditions.
- The using-shakespii skill is available — every CLI mechanic here (fix loop,
  eval runs, trigger measurement) delegates to it.
- A human is reachable for the interview, or the task prompt already supplies
  and approves the interview's answers.

## Procedure

Phase 1 — Interview. Ask one question at a time, multiple-choice where the
options are enumerable, until every anatomy section has raw material:

1. Intent: what problem, for whom, and what does a successful use look like?
2. Triggers: at least five real requests that should fire the skill, and at
   least three lookalikes that must not.
3. Inputs and preconditions: what the skill consumes; binaries, paths, and
   environment it assumes.
4. Procedure: walk one real occurrence of the workflow end to end.
5. Example: one real input with its real output — not an invented pair.
6. Failure modes: what has gone wrong when this was done by hand.

The interview ends when you can state the kebab-case name, the purpose, and
the trigger list back and the human confirms them — or when the task prompt
already supplied and approved all three. In a non-interactive run where the
prompt leaves questions open, ask them all in one batch as your final output
instead of guessing.

Phase 2 — Draft. Scaffold, then fill from the interview:

```bash
shakespii init <name>
```

Fill every scaffold section, replacing each placeholder token. Craft rules
the linter cannot enforce:

- Freedom calibration: prescribe exactly where deviation breaks things (exact
  commands, exact formats); leave open where judgment beats prescription. A
  step that says "run these five commands in order" and a step that says
  "choose an appropriate threshold" should both survive the question "why
  this tight, why this loose?".
- Progressive disclosure: SKILL.md carries the loop; depth (rubrics, rule
  lists, long references) moves to `references/` files linked where used.
- The description leads with its trigger situations — the ones the interview
  named — not with the skill's implementation.
- The Examples section transcribes the interview's real input→output pair.
- Anti-patterns come from the interview's failure modes.

Phase 3 — Critique. Two layers, in order:

1. A fresh-eyes pass against [references/critique-rubric.md](references/critique-rubric.md),
   fixing what it catches.
2. The lint fix loop, delegated to using-shakespii: `shakespii lint <dir>
   --json`, apply remediations, re-lint until exit 0, handle warnings
   explicitly.

Phase 4 — Refine. Author the eval suite, then let the harness judge:

1. Write `evals/evals.json` (at least three cases, each an in-skill
   behavior branch — happy path, refusal or error branches, variants;
   scope negatives belong in `evals/triggers.json`) following
   [references/headless-eval-rules.md](references/headless-eval-rules.md).
2. Write `evals/triggers.json` (at least sixteen labeled queries, with
   near-miss negatives on the boundary of any neighboring skill).
3. Gate with the harness — token spend confirmed with the human, or already
   approved in the task prompt:

```bash
shakespii test <dir> --run --triggers
```

4. On trigger misses, reword the description and re-measure with `--fresh`;
   stop once accuracy holds at or above 0.8 without regressing queries that
   already passed. The using-shakespii skill documents the loop's CLI
   semantics.

Phase 5 — Present. Hand the human the skill directory, its lint output, and
its scenario and trigger results, plus any open questions. Do not install
the skill anywhere; installation is a separate, explicitly approved act.

## Output

- A new skill directory (`SKILL.md`, `README.md`, `evals/evals.json`,
  `evals/triggers.json`, optional `references/`) that lints clean, with
  recorded scenario and trigger results.
- A presentation of that evidence to the human. The skill is not installed.

## Examples

The human says: "I want a skill that helps agents write good commit
messages."

Interview (excerpt). Q: "What does a bad commit message look like in your
repos — what specifically goes wrong?" A: "They describe the diff instead of
the why; bodies restate the subject." Q: "Name three requests that should
trigger this skill." A: "Write the commit message for this change; clean up
my commit history wording; draft a PR-merge commit."

Draft (excerpt). The interview's answers become the description —

```yaml
description: "Use when the user asks to write or improve a commit message or
commit-history wording — leads with the change's why, keeps the subject
imperative and under fifty characters, and never restates the subject in the
body."
```

— and the bad-message example from the interview becomes the worked example:
input, a diff adding a retry wrapper around one HTTP call; output, subject
"retry transient checkout-service timeouts" with a body explaining the
incident that motivated it.

## Anti-patterns

- Inventing interview answers instead of asking the human — or instead of
  reading them from a task prompt that already supplies them.
- Pasting the raw idea into every section; each anatomy section answers its
  own question.
- Stopping at lint exit 0: lint checks the contract, while the rubric and
  the eval runs check whether the content is any good.
- Eval expectations that need a mid-run human reply — the headless rules
  file shows how to reword them.
- Re-teaching CLI mechanics inline instead of delegating to using-shakespii.
- Installing the finished skill without an explicit approval.
