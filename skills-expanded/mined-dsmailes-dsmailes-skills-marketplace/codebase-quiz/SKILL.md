---
name: codebase-quiz
description: Use when the user wants to learn, rehearse, or maintain awareness of a software codebase through a short interactive quiz. Applies when the user asks to be quizzed on a repo, test their understanding, onboard to unfamiliar code, check codebase knowledge, avoid letting the agent do all the work, or practice explaining architecture, data flow, tests, risks, or implementation details.
---

# Codebase Quiz

## Mission

Help the user actively learn the current codebase. Inspect the repository, ask three evidence-based questions one at a time, score the user's answers, and give feedback that improves awareness without turning into a solution dump.

## Default Invocation

When invoked with no extra instructions:

1. Perform a read-only orientation pass.
2. Prepare exactly three adaptive questions.
3. Ask only Question 1 and wait for the user's answer.
4. After each answer, score and give brief feedback, then ask the next question.
5. After Question 3 feedback, give the total score and study targets.

Do not ask the user what to quiz them on unless the repository cannot be inspected or multiple unrelated repos are present.

## Orientation Pass

Before asking questions, inspect enough local evidence to make the quiz real:

- `README*`, docs, task notes, or architecture notes
- package/build manifests and dependency files
- tests, fixtures, and examples
- likely entry points and core modules
- recent diffs when the user asks about current work

Limit the orientation pass to the most relevant 8-12 files unless the user asks for a deeper quiz.

Keep the visible orientation summary short: 3-5 bullets naming the major areas found. Do not explain the answers to the quiz during orientation.

## Question Design

Create three questions with adaptive difficulty:

1. **Map**: structure, entry points, responsibilities, or where to find behavior.
2. **Flow**: data flow, control flow, lifecycle, state, API boundaries, or feature behavior.
3. **Risk**: tests, edge cases, invariants, failure modes, hidden coupling, or architecture tradeoffs.

Good questions require the user to reason from code, not recall trivia. Prefer "where and why" questions over naming facts.

Use this shape:

```text
Question 1/3 - Map
[one focused question]

Answer in a few sentences. I will score it before moving on.
```

## Scoring And Feedback

Score each answer out of 3:

- **3**: correct, grounded in code, explains why it matters
- **2**: mostly correct, missing one important detail or consequence
- **1**: partly correct, vague, or only names files without reasoning
- **0**: incorrect, unsupported, or no answer

After each answer, respond with:

- **Score**: `N/3`
- **What you saw**: one concise strength
- **Gap**: one concrete missing or mistaken point
- **Next place to inspect**: a file, test, symbol, or concept

Then ask the next question immediately, except after Question 3.

## Final Result

After the third answer, give:

- total score out of 9
- strongest area
- weakest area
- 2-3 study targets grounded in repository files or concepts

Do not include a full answer key by default. If the user asks for the answers after scoring, provide concise model answers with file references.

## Guardrails

- Do not edit files, implement features, or fix bugs while quizzing.
- Do not answer the quiz before the user attempts it.
- Do not ask all three questions at once.
- Do not use vague prompts like "explain this repo"; tie every question to inspected evidence.
- If the user tries to hand the work back to the agent, redirect with a smaller hint or narrower question.
- If repository evidence is thin, quiz on the available structure and say what could not be determined.
