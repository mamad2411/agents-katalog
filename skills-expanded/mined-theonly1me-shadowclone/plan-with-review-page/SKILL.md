---
name: plan-with-review-page
description: 'Use before a change that touches many files, needs many steps, or has open design choices. Also use it when the user says "plan this first", "make a plan", "think this through", or "do not code yet". Explores the code read-only, finds the cause, asks the open decisions with the recommended option first, and writes one plan. The plan explains the problem, the evidence, the cause, the fix and why it works, the alternatives, the risks, and the decisions. Builds a self-contained HTML review page from a template, and checks the page with a validator. Not for checking finished work (use `verify-and-review`).'
metadata:
  shadowclone-category: workflow
  shadowclone-section: workflow
  shadowclone-applies-when: before a change that has many steps or open design choices
---
# Plan With a Review Page

## Use when

A change touches many files, needs many steps, or has a design choice that belongs to the user. An approved plan stops work in the wrong direction. A small and clear change does not need this skill.

The plan is the reference for the person who approves the work. That person may not have read the conversation, so the plan alone must let them judge the change.

## Gates

1. Are you read-only until the user approves? Before approval, write only the plan file and the review page.
2. Did you read the code, the documents, and the history before you asked? Never ask what the code can answer.
3. Did you ask in rounds until no decision was open? Each risky choice, such as a skip, a block, a fallback, or a default, belongs in a round. Each round has at most 4 questions, each with 2 to 4 options and the recommended option first.
4. Can a reader who missed the conversation judge the change from the plan alone? The plan gives the problem, the evidence, the cause, the fix, why it works, and the alternatives.
5. Does each cause have a change that removes it and a check that proves the fix?
6. Is there one plan file for this conversation, and does its page pass `scripts/validate-page.mjs` with 0 errors?

## Process

### Explore

1. Read the code that the request touches, and the instructions of the repository for that code.
2. Reproduce or observe the problem. Record each fact with its source: a `path:line`, a command and its output, or a URL. Label each fact as measured, read, inferred, or reported.
3. Find each cause: the first place where the behavior goes wrong, with its `path:line`. For a new feature, a cause is a limit of the current design that blocks the feature.
4. Record each cause that you tested and rejected, with the observation that ruled it out.
5. Find the functions and patterns that the change can use again. For a broad search, use a read-only subagent if the host has one.
6. Stop when you can name the causes, the change, its tests, and what users would see break. Write each follow-up as one line in the plan. Do not research a follow-up first.

### Ask

1. List each open decision about scope, behavior, edge cases, data, release, and tests.
2. Ask at most 4 questions in each round. Put the recommended option first, with one reason.
3. Use the question tool of the host if it has one. If not, use a numbered list in the chat.
4. If an answer is not clear or opens a new decision, ask another round. Do not guess.

### Write

1. Put the plan at `/tmp/agent-artifacts/<repo>/<date>-<slug>/plan.md`. If the sandbox blocks `/tmp`, use the temporary folder of the agent. If the host gives a plan file path, use it for the plan and keep the review page in `/tmp/agent-artifacts/`.
2. Write for a reader who was not in the conversation. Define each project term the first time you use it. Use these sections in this order, in the plan file and on the page:
   - **Summary and status:** what changes, why, and the result, in two or three sentences. The status is draft, approved, in progress, or done.
   - **The problem:** what is wrong or missing as the user sees it. Give its impact: who it affects, how often, and the cost.
   - **What happened:** the facts, each with its source and its label.
   - **Why it happened:** each cause with an id such as `C1` and its origin. Add each cause that you ruled out, with the reason.
   - **The fix:** the approach, then each change with an id such as `F1`, its files, and the causes or risks that it addresses. Say why each change works. For a change that repeats across many files, describe the pattern once and list a few example paths.
   - **Why the fix works:** the page builds this table from the causes, the changes, and the checks.
   - **Alternatives considered:** each other option, including no change. Say what it gives, what it costs, and why the plan does not use it.
   - **Risks:** each risk with an id such as `R1`. Say what can go wrong after the change, and how the plan prevents it or finds it early. A change can exist only to limit a risk.
   - **Decisions:** each question, its answer, its reason, and its source. The source is user, repository, or agent. An agent decision is a default that the user can change.
   - **Open questions:** each question, and the step that waits for its answer.
   - **Steps, verification, and follow-ups:** the steps in order, and each check with the result that proves the fix and the causes that it proves. Then write one line for each follow-up.
3. Copy `assets/review-page.html` to the same folder as `index.html`. Edit only the JSON block with the id `plan`, and replace each value that starts with `TEMPLATE:`.
4. Add Mermaid source in `diagram` when the change has more than two parts. The page shows the source as text, and draws it when the pinned Mermaid file loads.
5. Run `node scripts/validate-page.mjs <page>`. If Node is not available, run the script with `bun`. Fix each error.
6. Give the user both paths, the summary, the main risk, and the open questions. If the host has a plan approval step, use it. If not, ask "Do you approve this plan?" Wait for approval in this conversation.

### Execute

1. Do the steps in order. After each step, update its status in the page and in the plan.
2. If a fact changes a decision or a cause, stop. Update the plan, and ask again.
3. Keep a step that you skip in the list, with the status `skipped` and the reason in its note.

## Example

**Situation:** The user asks for a fix to a sync command. Sync replaced installed skills, and some installed copies contained edits that the user made.
**Easy route:** Write four steps: read the sync code, add a check, add a test, and open a pull request.
**Hidden cost:** The reviewer cannot tell why sync replaced the edits, or whether the check removes that cause. The plan also hides a choice that deletes the work of the user. The reviewer approves a guess.
**Best route:** Write the cause `C1` with its `path:line`: sync compares the file name and not the fingerprint. Link the change `F1` to `C1`, and name the test that proves it. List the rejected alternative "always save a backup" with its trade-off. Ask whether to keep and list edited copies (recommended) or to replace them and save a backup.
**Evidence:** The "Why the fix works" table shows `C1`, the change `F1`, and the test that proves the fix. The decision table shows "Edited copies: keep and list" with the source "user". The validator printed "validate-page: 0 errors in 1 file".

## Guardrails

- Approval covers only the steps in the plan. Ask before a step that the plan does not list.
- Never commit the plan or the review page to a repository.
- Keep the review page self-contained. Do not add scripts, styles, or fonts from the network.
- Do not open a decision again unless a new fact changes it.
- Make the plan complete first. Keep it easy to scan with tables, short sentences, and one idea in each sentence.
- Keep the label of each fact true. Do not present an inference as a measurement.

## Completion

- The plan path and the review page path.
- The validator command and its result line.
- Each question round, with the recommended option first in each question.
- Each cause, the change that addresses it, and the check that proves the fix.
- Each step with its status, and each skipped step with its reason.
