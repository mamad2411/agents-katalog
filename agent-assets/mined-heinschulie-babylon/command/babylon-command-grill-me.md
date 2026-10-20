---
allowed-tools: Read, Grep, Glob, Agent
description: Stress-test a plan or design through relentless interviewing until reaching shared understanding
argument-hint: [plan or design topic]
model: opus
---

# Purpose

Interview the user relentlessly about every aspect of a plan or design until reaching shared understanding. Follow the `Instructions` to walk down each branch of the decision tree, resolving dependencies between decisions one-by-one.

## Variables

TOPIC: $ARGUMENTS

## Instructions

- Interview relentlessly — do not accept vague or hand-wavy answers. Push for specifics.
- Walk down each branch of the design/decision tree systematically.
- Resolve dependencies between decisions one-by-one before moving to the next branch.
- For each question, provide your own recommended answer so the user can accept, reject, or refine.
- If a question can be answered by exploring the codebase, explore the codebase instead of asking the user.
- Ask only one question at a time — do not overwhelm with a list of questions.
- Track which branches of the decision tree have been resolved and which remain open.
- Challenge assumptions — if something seems under-specified or risky, call it out.
- Once all branches are resolved, summarize the shared understanding reached.
- IMPORTANT: Once this prompt has been run, absolutely **NEVER** start implementing or actively editing code without EXPLICIT instructions from the user to do so.

## Workflow

1. Read and understand the TOPIC provided — if it references a file or plan, read it from the codebase
2. Identify the top-level decision branches of the plan or design
3. For each branch, drill down with targeted questions:
   a. State the question clearly
   b. Provide your recommended answer with reasoning
   c. Wait for the user's response before proceeding
   d. If the user's answer opens sub-branches, drill into those first
4. When a question can be answered from the codebase, explore the code and present findings instead of asking
5. After resolving all branches, proceed to the Report

## Report

Summarize the shared understanding as a structured decision log:

- List each decision branch and the resolution reached
- Note any open items or follow-ups that remain
- Highlight any risks or trade-offs that were explicitly accepted
