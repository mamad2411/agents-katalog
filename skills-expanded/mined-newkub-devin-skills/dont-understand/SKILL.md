---
name: dont-understand
description: Handles user confusion by routing to /ask-again or re-explaining briefly
argument-hint: "[scope]"
related:
  - ask-again
  - ask-me
  - follow-my-persona
  - dont-ask-me
  - continue
  - ask-project-requirement

---

## Goal

Handle cases where the user says they do not understand, by re-asking or re-explaining briefly and clearly

## Scope

Use when the user types "don't understand", "I don't understand", "dont understand", "confused", "lost" or similar

Not for gathering requirements (use `/ask-project-requirement`) or preference interviews (use `/follow-my-persona`)

## Execute

### 1. Detect Dont-Understand

> Goal: Recognize that the user does not understand

1. Capture signals: "don't understand", "I don't understand", "I really don't understand", "dont understand", "confused", "lost", "don't get it", "makes no sense", "explain more"
2. Find the latest question/explanation the assistant asked/told
3. If no recent context is found → ask back briefly: "Could you tell me which part is unclear?"

### 2. Choose Response Strategy

> Goal: Choose the appropriate response strategy

1. If there was a previous question → use `/ask-again` to rephrase
2. If there is no question but a previous explanation → summarize and re-explain concisely
3. If the user asks a specific question → answer only that point
4. If information is insufficient → use `/ask-project-requirement`
5. If the user just wants to proceed → use `/dont-ask-me`

### 3. Respond

> Goal: Respond in an easy-to-understand way

1. Acknowledge the confusion first, e.g. "No problem, let me explain again"
2. Reduce jargon and difficult words
3. Use short examples or analogies
4. If you must ask further → use the `ask_user_question` tool only
5. If no question is needed → summarize the solution clearly and proceed

### 4. Handle Loop

> Goal: Avoid going in circles

1. If the user still says they do not understand → use `/ask-again`
2. If still unclear on the 2nd attempt → ask open-endedly: "Which aspect would you like explained further?"
3. If still unclear on the 3rd attempt → use `/dont-ask-me` or `/continue` with the safest default

## Rules

### 1. Empathy

- Never blame the user for not understanding
- Use a helpful tone, not defensive
- Keep a single explanation to no more than 3-5 sentences

### 2. No Exact Repeat

- Never copy the original message verbatim as the answer
- Always rephrase, summarize, or add examples
- For code/technical topics, cut the fine details and emphasize the big picture

### 3. Tool Discipline

- If you must ask the user → use `ask_user_question` only
- Do not ask via plain chat text
- To re-ask the same question → use `/ask-again`

### 4. Escalation

- If the user wants preferences/style applied → use `/follow-my-persona`
- If information is insufficient → use `/ask-project-requirement`
- If the user says stop asking/just do it → use `/dont-ask-me`

- Use /ask-me if needed

## Expected Outcome

- The user understands the re-asked question or new explanation
- Less repeated confusion
- The flow is preserved without anything left hanging
- If still unclear after 2-3 attempts, there is a clear way forward (default, open-ended, or handed off to another skill)
