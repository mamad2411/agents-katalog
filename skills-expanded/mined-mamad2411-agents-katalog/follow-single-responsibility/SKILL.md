---
name: follow-single-responsibility
description: Split a task or prompt into sub-units, one responsibility each (single responsibility)
argument-hint: "[scope]"
related:
  - ask-me
  - plan
  - continue
---

## Goal

Split the user's task or prompt into a numbered list where each item has a single responsibility, to make planning, delegation, and tracking easier

## Scope

Use when a prompt or task mixes multiple requests/jobs together, before starting to plan or implement

## Execute

### 1. Parse Input

> Goal: understand what the user actually requested
1. Read the latest prompt and the relevant context
2. Identify the main goal, scope, and expected outcome
3. Identify constraints, references, and related files
4. If the input is unclear → run `/ask-me` before proceeding

### 2. Decompose

> Goal: break the work into single-responsibility units
1. Separate each instruction/request from the others
2. Check that each item does exactly one thing
3. If an item contains multiple jobs → split it further
4. Order the items by dependency or by a sensible work sequence

### 3. Format

> Goal: present the result in an easy-to-understand form
1. Summarize each item in a short, concise, clear sentence
2. Use the format `N. <responsibility> — <short detail>`
3. Order by prepare → read → research → analyze → write → validate → report where possible

### 4. Hand Off

> Goal: ready for the next step to take over
1. Show the numbered list in chat immediately
2. Do not implement or modify any files in this step
3. If needed → continue with `/plan` or `/continue`

## Rules

### 1. One Thing Per Item
- One item does one thing — never merge multiple requests into a single item
- If you find "and" or many "," inside one item → split it further

### 2. Preserve Original Intent
- Keep the original meaning and requirements of the prompt
- Do not add or reduce scope without reason

### 3. Use Same Language
- Use the same language as the source prompt (Thai or English)
- Do not switch languages between items

### 4. No Execution
- Do not modify files, run commands, or implement
- This is only a task summary

## Expected Outcome

- A readable numbered list where each item has a single responsibility
- Related files/tasks clearly identified
- The user's requirements fully carried over without additions or omissions
- Ready to hand off to `/plan` or `/continue`
