---
name: evals
description: Prove that a skill, rule or prompt changes what the agent does - blind prompts, runs with and without it, graded on outcomes, never on the agent's own account. Use when writing or changing a skill, an AGENTS.md or CLAUDE.md rule, a system prompt or a plugin.
---

# Evals: prove an instruction works

A test proves code. An instruction (a skill, a rule in `AGENTS.md`, a prompt) is only a claim until you have watched the agent behave differently because of it. An eval is that proof: the same request, run with the instruction and without it, graded on what came out.

## 1. Frame

Name the change under test and what a user would notice if it worked. Write 3 to 6 criteria a stranger could check, outcome first: the file that exists, the number in the answer, the state the screen shows. Keep the criteria away from the agent being measured.

## 2. Pick the cases

- At least four requests where the instruction should change the result, in at least two different shapes. Real requests from your history beat invented ones.
- At least one where it should do nothing: a plain question it must not load, pitch or slow down.

## 3. Blind the agent

- The prompt reads like a real request. No "eval", "test", "judge", "rubric", "benchmark" or "score" in the prompt, folder names or file names.
- Never ask the agent which skills or rules it followed. It will say what you want to hear.
- Plant only what a real task would have: a small project, the bug, the files a person would mention.

## 4. Grade what it did, not what it says

In this order, using the first that can catch the failure:

1. Machine checks: a pattern in the answer, a file created, a tool used before another, the exit code of a command.
2. A judge model with concrete, checkable claims, given the transcript or the file, never the agent's summary. Use a different model from the one being measured.

"The agent said it reproduced the bug" is not evidence; a command in the transcript that printed the wrong total is.

## 5. Measure the difference

Run every case with the instruction and without it, at least three times each. The result is the difference between the two, reported with the run count and how much the runs disagreed (principle 2). A case that passes in both arms proves nothing about the instruction; it only proves the model already does it.

Pilot with one run first and read every output yourself. When you disagree with the judge, the criterion is ambiguous: rewrite it before the full run. A sudden jump in score is a gamed criterion until you have read the transcripts that earned it.

## 6. Keep it safe

Each run gets its own folder and a neutral config. No real accounts: use the one test account, stand-ins for external services, and nothing that sends, pays or publishes.

## In Claude Code

`claude plugin eval` runs this method: a case is a folder in `evals/` with a `case.yaml` (or `prompt.md` plus `graders/*.md`), and `--ablation with-without` runs each case with and without the plugin. CCM Stack's own suite is in its repository (`evals/`, run with `node scripts/evals.js`), one case per behavior worth protecting. Running a suite uses your Claude usage: start with `--runs 1`.

## In other tools

Run the same prompt in two fresh sessions, one with the rule removed, three times each, and grade the outputs with the criteria from step 1 before you read which session each came from.

**Reply:** the change under test, the criteria, the result of each case in each arm with run count, the difference, what you read by hand, and whether the instruction earns its place.
