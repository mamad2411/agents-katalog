---
name: openspec-bugfix
description: Start a new bugfix using the OpenSpec artifact workflow. Use when the user describes a bug, defect, or unexpected behavior and wants to fix it using a structured approach.
metadata:
  author: CosticaPuntaru
  version: '1.0'
---

# OpenSpec Bugfix Skill

This skill implements a structured workflow for identifying, reporting, and fixing bugs using OpenSpec artifacts.

## When to use

- When the user reports a bug or technical issue.
- When you need to troubleshoot and fix a defect in the codebase.
- Specifically triggers when the user says something like "fix this bug", "there is an issue with X", or "I found a defect".

## Prerequisites

This skill requires the `bugfix` OpenSpec schema. 
- You can find the bundled schema files in the `resources/bugfix-schema` directory of this skill.
- If the project does not have `openspec/schemas/bugfix` established, you MUST offer to set it up by copying the files from the skill's resources.

## Steps

### 1. Information Gathering (Proactive)

To ensure a high-quality fix, gather details from the user one by one using the **AskUserQuestion tool**. For EACH question, attempt to provide a **"Best Guess"** based on the user's initial description to reduce their effort:

A. **Reproduction Steps**: Present your best guess of the steps.
   Ask: > "Based on your description, here are the **reproduction steps** I've gathered. Is this correct or would you like to adjust them? [List steps]"

B. **Expected Behavior**: Present your best guess.
   Ask: > "For the **expected behavior**, I assume it should [Guess]. Does that sound right?"

C. **Actual Behavior**: Present your best guess.
   Ask: > "And the **actual behavior** is [Guess]? (Please correct me if I missed a detail)."

D. **Environment**: If the bug appears to be **environment-dependent** (e.g., UI issues, browser-specific crashes, OS-level failures), ask:
   Ask: > "Are there any specific **environment details** (OS, browser, etc.) that are relevant, or should I proceed with standard defaults?"
   Otherwise, skip this question and proceed to Step 2.

**Wait for each response before moving to the next.** Allow the user to "Skip" or "Confirm" if your guess is correct.

### 2. Initialize the Change

Derive a kebab-case name prefixed with `fix-` (e.g., `fix-login-failure`).

Run the initialization command:
```bash
openspec new change "<name>" --schema bugfix
```

### 3. Draft the Proposal

Create the `proposal.md` in the new change directory (`openspec/changes/<name>/proposal.md`). Use the information gathered in Step 1 to populate the bug-specific sections.

### 4. Planning and Tasking

Run the OpenSpec status check to confirm the proposal is ready:
```bash
openspec status --change "<name>"
```

Generate sub-artifacts and tasks:
```bash
openspec ff change "<name>"
```

### 5. Summary and Next Steps

Summarize the change location and the tasks generated. Prompt the user to start implementation:
> "Bugfix change `<name>` initialized using the native `bugfix` schema. I've drafted the proposal and spawned the implementation tasks. Ready to start implementation? Run `/opsx-apply` or let me know if you want to refine the plan first."

## Guardrails

- **CRITICAL**: You MUST ask the Information Gathering questions **one by one**. Do NOT combine them into a single message. Pause and wait for the user to respond after EACH question.
- ALWAYS gather reproduction steps before initializing the change.
- Prefix all bugfix changes with `fix-`.
- Pass `--schema bugfix` when creating the change.
- Do NOT skip the proposal phase; it's critical for documenting WHY a fix was made for future reference.
