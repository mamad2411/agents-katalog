---
name: follow-my-persona
description: Think and ask the user to understand preferences and working style
argument-hint: "[topic]"
related:
  - ask-me
  - dont-understand
  - plan

---

## Goal

Build an understanding of the user to improve the working experience together

## Scope

Use for interviewing the user to collect preferences, coding style, and habits

Use only the `ask_user_question` tool from the Windsurf system prompt for asking questions, and the `create_memory` tool for saving answers

## Execute

### 1. Prepare Questions

> Goal: Prepare Questions

Prepare questions for the interview

1. Design questions covering every aspect of working
2. Group questions by `categories` (`coding style`, `preferences`, `habits`)
3. Set each question's `priority` (`critical`, `important`, `nice-to-have`)
4. Prepare `follow-up questions` for interesting answers

### 2. Conduct Interview

> Goal: Conduct Interview

Conduct the user interview using the `ask_user_question` tool

1. Start with `general` questions to build `context`
2. Ask questions by the defined `priority`, one at a time, via the `ask_user_question` tool
3. Use `follow-up questions` via the `ask_user_question` tool to go deeper
4. Analyze the answers from the `ask_user_question` response

### 3. Analyze Responses

> Goal: Analyze Responses

1. Group answers by patterns
2. Identify contradictions or inconsistencies
3. Analyze implicit preferences from the answers
4. Summarize the key insights found

### 4. Save To Memory

> Goal: Save To Memory

Save the information into the `memory system`

1. Save the information into the `memory system` with the `create_memory` tool
2. Categorize the data by `type`
3. Add `tags` for `easy retrieval`
4. Update `existing memories` when there is new information

### 5. Update Context

> Goal: Update Context

Update the `context` according to the gathered information

1. Update `user preferences` in the `context`
2. Adjust `workflow choices` per the `preferences`
3. Change the `communication style` to match preferences
4. Verify the information is actually applied

## Rules

### 1. Question Categories

Questions should cover every aspect of working

- `Coding style` (`indentation`, `naming`, `patterns`)
- `Preferences` (`tools`, `frameworks`, `languages`)
- `Habits` (`workflow`, `debugging`, `testing`)
- `Communication` (`verbosity`, `language`, `format`)
- `Goals` (`short-term`, `long-term`, `priorities`)

### 2. Question Design

Design questions to be effective

- Be `open-ended` to get detailed answers
- Not `leading questions`
- With clear `context`
- Not redundant
- Short and concise but clear

### 3. Interview Techniques

Use suitable interview techniques

- Use `active listening`
- Ask `clarifying questions`
- Observe `patterns` in answers
- Don't `interrupt` while the user is answering
- Summarize back to confirm understanding

### 4. Memory Management

Manage `memories` effectively

- Use the `create_memory` tool for saving
- Assign appropriate `tags`
- Update `existing memories` instead of creating new ones
- Delete irrelevant `memories`
- Use the correct `CorpusNames`

### 5. Context Application

Apply the information in real work

- Adjust the `communication style` per `preferences`
- Choose `tools` per preferences
- Follow the `workflows` the user likes
- Use the language the user wants
- Adjust `verbosity` per `style`

- Use /ask-me if needed
- Use /dont-understand if needed
- Use /plan if needed

## Expected Outcome

- A complete understanding of the user's `preferences`
- Data saved in the `memory system`
- Work adjusted to the user's `style`
- `Communication style` matching the user's needs
- Fewer repeated questions
