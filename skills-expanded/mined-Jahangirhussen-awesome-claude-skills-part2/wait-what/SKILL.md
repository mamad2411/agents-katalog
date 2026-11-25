---
name: wait-what
description: Re-pitch the previous message when the user did not understand it. Use when the user says they are lost or asks for a simpler restatement. Not for new work; only rephrases what was already said, in ASD-STE100 Simplified Technical English.
disable-model-invocation: true
---
Wait, I don't understand where you've got to here. Re-pitch that: give me a little bit of context, talk in ASD-STE100 Simplified Technical English, and use the ubiquitous language from `CONTEXT.md` (follow `CONTEXT-MAP.md` to the right one if the repo has more than one).

## Purpose
Recover from an unclear previous message by re-explaining it simply, with context, in the project's ubiquitous language.

## When to use
The user says "wait, what?", "I don't follow", or asks to re-pitch the last message.

## When NOT to use
- The user asks a brand-new question.
- The previous message was clear and the user disagrees (answer the disagreement instead).

## Core workflow
1. Re-read your last message and what you were trying to achieve.
2. Give a short context paragraph (where we are and why).
3. Restate the point in ASD-STE100 Simplified Technical English: short sentences, active voice, one idea per sentence.
4. Use the terms from `CONTEXT.md` (follow `CONTEXT-MAP.md` if the repo has several contexts).

## Edge cases and failure handling
- No CONTEXT.md in the repo -> use the plain project terms already used in the conversation.
- The user's confusion is about a term -> define it once, then continue.

## Validation
- Check every sentence is short and uses one defined term per concept; confirm the key decision or action is stated in the first lines.

## Output requirements
A short re-pitch: context, the point, and the next action or question.

## Example
```text
Previous: dense explanation of a migration. Re-pitch: "We are moving data to a new table. Step 1 copies data. Step 2 switches the app. Do you approve step 1?"
```

## Related skills
domain-modeling, grilling
