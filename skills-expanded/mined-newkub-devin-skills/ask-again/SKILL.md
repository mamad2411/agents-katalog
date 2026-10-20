---
name: ask-again
description: Re-ask with a shorter, plainer question and examples when the user is confused
argument-hint: "[scope]"
related:
  - ask-me
  - dont-ask-me
  - follow-my-persona
  - continue
  - ask-project-requirement

---

## Goal

Re-ask the user when the original question was not understood: rephrase it shorter, cut jargon, add context or examples, or break it into smaller points

## Scope

Use when the user replies "don't understand", "ask again", "repeat", "explain", or picks `Suggest another` a second time in `/ask-me`

Do not use for gathering requirements (use `/ask-project-requirement`) or interviewing preferences (use `/follow-my-persona`)

## Execute

### 1. Detect Confusion

> Goal: Recognize that the user does not understand the question

1. Watch for confusion signals: "don't understand", "ask again", "repeat", "explain", "confused", "can't follow"
2. Look at the context of the most recent question asked
3. If there is no prior question → stop and report that there is no question to re-ask

### 2. Analyze Why Unclear

> Goal: Find out why the question was not understood

1. Assess whether the question is too long or too complex
2. Assess whether it contains jargon or terminology the user may not know
3. Assess whether context or background is missing
4. Assess whether there are too many options or unclear labels
5. Pick the appropriate rephrasing strategy

### 3. Rephrase

> Goal: Make the question easier to understand

1. Shorten the `question` to 1-2 brief sentences
2. Remove or replace jargon with plain words
3. Add brief context explaining why the question is being asked, e.g. "to pick the runtime that fits the project"
4. Give a short example or comparison in `description`
5. If there are too many options, cut down to the 2-3 most important
6. If it is complex, split into 2 sub-questions instead of asking everything at once

### 4. Ask With `ask_user_question`

> Goal: Send the new question to the user

1. Use the `ask_user_question` tool only
2. Keep the original `options` as much as possible, but reword `label` and `description`
3. Preserve the recommended option
4. Set `multi_select` to match the original question
5. Tell the user this is a re-ask, e.g. "Let me ask that again — ..."

### 5. Handle Re-Ask Loop

> Goal: Never loop the question more than 2 times

1. Count how many times the question has been re-asked
2. On the 2nd re-ask → ask open-ended or reduce to the 2 clearest options
3. On the 3rd or later → use `/dont-ask-me` or a default without asking further
4. If the user says they don't want more questions → use `/dont-ask-me`

### 6. Process Response

> Goal: Process the answer

1. Pair each question with its answer from the mapping `ask_user_question` returns
2. If the user answered in their own words (custom_text), analyze it and adjust the plan
3. If the user still doesn't understand → go back to Step 2, counting the re-ask
4. Once the user answers → continue based on the answer

## Rules

### 1. No Exact Repeat

- Never repeat the question verbatim; rephrase it or add context
- Change at least one of `question`, `label`, or `description`

### 2. Preserve Intent

- Keep the original ask and the intended answer intact
- Don't change `single` to `multiselect` without a reason
- Don't add irrelevant options

### 3. Loop Limit

- Re-ask at most 2 times
- On the 3rd time, use `/dont-ask-me` or go open-ended
- If the user says to stop asking → stop immediately

### 4. Tool Discipline

- Use the `ask_user_question` tool only
- Don't ask through plain chat text

### 5. Escalation

- If the user is confused because information is missing → use `/ask-project-requirement`
- If the user wants to explain their preferences → use `/follow-my-persona`
- If the user says they don't want questions → use `/dont-ask-me`

- Use /continue if needed
## Expected Outcome

- The user understands the rephrased question and can answer
- Fewer repeated question loops
- The conversation flow is preserved
- If it is still unclear after 2 rounds, there is a clear fallback (default / open-ended / hand off to another skill)
