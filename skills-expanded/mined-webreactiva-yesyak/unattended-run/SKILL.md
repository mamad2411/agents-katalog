---
name: unattended-run
description: Lets the feature-delivery-pipeline and its phase skills run from start to end without the user. The agent answers every checkpoint, interview round and "which option?" question with the recommended option and logs it with its reason. The run only stops for actions the user did not authorize. yak-pilot loads it for every run to answer the questions that are not gates, and the observer preset uses it for a run without questions. Use it directly when the user says "do not ask me", "answer the questions yourself", "run it to the end without me" and yak-pilot is not installed.
---

# Unattended run

## What the user authorized

Read the request once and write down, in the first lines of `.scratchpad/<slug>/unattended-decisions.md`:

- **Start point**: the base branch and the branch you must work on.
- **End point**: for example "open the PR, do not approve, do not merge". It includes every phase of the pipeline still to run, up to the retrospective; a project step such as a merge comes after it. A phase you skip is a `Q-` entry.
- **Outward actions allowed**: push, PR, issues, comments. Only what the request names or clearly implies.
- **Skills allowed**: for example "only the YesYak skills".
- **Skill feedback wanted**: should you note problems in the skills while you use them?

Anything that is not on this list stays forbidden: merge, approve, force-push, delete branches, deploy, post in other repositories, write files outside the repository.

## How to answer a question

Every time a skill says "ask the user", "wait for the user" or "checkpoint":

1. Write the question as you would ask it, with its options and the recommended option first.
2. Choose. Prefer the recommended option. Choose another option when the code, the request or a previous answer gives a reason.
3. Append one entry to `unattended-decisions.md`:

   ```markdown
   ### Q-07 Phase 2 · write-acceptance-spec · What happens when a paid order is cancelled?
   - Options: refund at once (recommended) / refund after a review / store credit
   - Chosen: refund at once
   - Why: the payment provider supports it; the spec has no reviewer role
   - Reversible: yes
   ```

4. Continue in the same message. Do not stop at the checkpoint, and never end your turn to wait for a test run, a build or a subagent: nobody sends the next message. Wait for it in the same turn.

Give every entry a stable id (`Q-01`, `Q-02`…). Decisions that a reviewer could question also get an ADR (`decision-record-log`). The ADR source field names the `Q-` id.

## Optional steps

The pipeline marks some steps as optional (devil's advocate, work items, browser testing). An unattended run has no one to offer them to. Run an optional step when the request says "the full process" or when the feature needs it. Browser testing is needed when the change has a user interface that the acceptance criteria describe: run `browser-acceptance-testing`, which accepts this decision in place of the user's request. Record the choice as a `Q-` entry either way.

## Checkpoints become progress entries

At each phase end, do not send a question to the user. Update `progress.md` with the phase, the artifacts and the commits, and send one short status line in the chat, so the user can follow and interrupt. Name the skill that runs next; the user cannot see skill calls otherwise.

## When to stop anyway

Stop and wait only when:

- Something the user named is missing (a branch, a file, an issue). Say what is missing and wait. Do not search other repositories or all of GitHub for it.
- The next action is outside what the user authorized.
- The action cannot be undone and the request does not cover it.
- Two sources the user gave contradict each other and each choice loses something the user asked for.
- The point is a gate of the `yak-pilot` plan, planned or dynamic.

## Skill feedback

When the user wants skill feedback, keep `.scratchpad/<slug>/skill-feedback.md`: the skill, the problem you met, the change you propose. Do not edit an installed skill. It can be a symlink to the shared skills repository. A change for this project only goes to `customize-yak`.

## At the end

- Tell the user the number of decisions you took alone and where the log is.
- In the pull request, add a short "Decisions taken without the user" section with the most important `Q-` entries, because `.scratchpad/` is not in the repository, and a cloud session loses it with the container.
