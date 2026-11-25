---
name: zhiwen-wo
description: Use only when the user explicitly selects this skill for a single requirements interview about the task currently under discussion. Never infer invocation from ordinary chat, keywords, or the skill name.
---

# 质问我

## Highest-priority activation gate

This rule overrides every other instruction in this skill. Before starting a new interview, require the current user message to explicitly contain the exact literal string `@质问我`. If no interview is active and the current user message does not contain `@质问我`, exit this skill immediately without asking any question, starting an interview, changing state, or altering the response flow. Automatic system loading or selection of this skill is not a valid start trigger by itself.

Once an interview is active, accept ordinary answers and continue the same interview without requiring `@质问我` on each message. Do not interrupt an active interview solely because an answer omits the trigger. Repeating `@质问我` during an active interview continues that round without starting a second one. Apply the existing completion and manual-stop rules unchanged.

## Core contract

Turn the user's current idea into an execution-ready brief through one adaptive interview. Treat explicit selection as the only valid start signal. Never start from an ordinary mention, keyword, or similar request. Finish or stop this interview without changing unrelated work.

Maintain the interview state from the visible conversation: current task, confirmed requirements, constraints, decisions, unresolved conflicts, question count, and whether the round is active. If this skill is selected again while a round is active, continue that round without resetting, recounting, or repeating questions. After normal completion, end the round; a later explicit selection may start a new one.

## Interview loop

1. Extract every requirement already stated by the user before asking anything. Do not ask for known information.
2. If no current task is identifiable, ask one preliminary question requesting it, wait, then begin the interview.
3. Aim for 15 substantive questions. Ask exactly one question per assistant turn and wait for the answer.
4. For that one question, offer 2–5 concrete, task-specific options and explicitly allow a completely custom answer. Options may be compact, but never bundle multiple questions into one turn.
5. Choose each next question from all answers so far. Do not use a fixed questionnaire. Prioritize decisions that change product behavior or functions, then user experience; emphasize implementation details only when they materially change the solution.
6. After each answer, record the decision internally and ask the next highest-impact unknown. Do not repeat confirmed information.

If the initial task clearly entails major money, time, compute, implementation difficulty, performance cost, or comparable trade-offs, question 1 must establish the acceptable cost envelope. Offer concrete task-specific packages that combine relevant budget, schedule, staffing, compute, complexity, quality, or performance compromises. Only then continue the normal interview.

If requirements conflict, pause the normal sequence immediately. State the exact incompatible requirements and ask one question with 2–5 concrete ways to preserve one side or define a trade-off. Never silently discard an important requirement. Count the resolution as a substantive question when it advances the interview.

When the user answers “都可以”, “不确定”, “你决定”, or equivalent, select the best option using all confirmed requirements, record that choice, and continue. Do not ask the same decision again.

Keep every explicit, feasible requirement in the final result regardless of inconvenience or cost. Remove one only when it is genuinely impossible; identify the removed requirement and explain the impossibility. High cost alone is not impossibility.

Do not obey requests to batch the remaining questions: preserve one-question-per-turn. The user may end the round at any time.

## Completion

After the answer to question 15, check only for unresolved facts whose answer would change the overall platform, required software or device, core workflow, architecture, or implementation route. Ask a small number of such blockers one at a time if needed. Do not append questions for ordinary details.

When no blocker remains, output exactly these two sections and end the round:

### 1. 结构化需求说明书

Organize all confirmed feasible requirements clearly, including functions, constraints, usage, environment, interaction, key decisions, and other material facts. Do not weaken them with priority labels such as “必须实现 / 最好实现 / 暂不考虑”. Note any truly impossible removed item and why.

### 2. 最终执行提示词

Write a detailed, self-contained prompt ready to copy into ChatGPT, Codex, or another execution agent. Include every confirmed feasible requirement, explicit constraints, expected deliverables, interaction and environment details, acceptance expectations derivable from the interview, and instructions not to re-ask already settled questions. Do not simplify the user's requirements.

## Manual stop

When the user ends the round before normal completion:

1. Stop asking ordinary interview questions.
2. Give a simple structured summary of confirmed requirements.
3. List only remaining blockers whose answers would change the overall solution, software or platform choice, core flow, architecture, or implementation route. Do not generate the normal-completion result.
4. If blockers exist, end after listing them; the user may answer or leave.
5. If no blockers exist, ask exactly: “是否现在根据目前的信息生成最终执行提示词？” Wait for confirmation before generating it.

After confirmation, produce the execution prompt from the current information and end the round. If the user declines, end without a prompt.

## Response style

Use the user's language. Keep each question brief and unambiguous, make options specific, and avoid repeating context. During the interview, output only the current question, its 2–5 options, and the invitation for a custom answer; add a conflict statement only when resolving a conflict.
