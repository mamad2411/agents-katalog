---
name: grimoire-init
description: Initialize the .grimoire project knowledge directory and register it with the agent configuration.
disable-model-invocation: true
---

# Purpose

Bootstrap the `.grimoire` directory in a project to store persistent knowledge across grimoire skills.

# Workflow

## 1. Explore

Discover:

- Does `.grimoire` already exist? If yes, list every existing file and directory inside it.
- Which injection targets are present? (AGENTS.md, CLAUDE.md, CURSOR.md, etc.)
- If a target already contains a grimoire block, capture its current content.
- What is the project type and structure?

Completion: All relevant project state is known.

---

## 2. Plan

Present the user with:

- The canonical directory structure (see [directory-structure](./references/directory-structure.md))
- What already exists vs. what will be created — show a diff
- Which injection targets will be modified and what will be injected (see [injection-targets](./references/injection-targets.md))
- If a target already has a grimoire block, show the existing block alongside the proposed replacement

Do not write anything yet.

Completion: A setup plan is presented and waiting for approval.

---

## 3. Confirm

Wait for explicit user approval.

The user may adjust the plan. Loop back to Plan if changes are requested.

Completion: User approves the plan.

---

## 4. Execute

Create the directory structure. Inject configuration into every target.

Verify every planned file exists and every injection target contains the registration block.

Completion: Every planned file exists. Every injection target contains the grimoire registration.

---

# Rules

- Never write before user approval.
- Never remove existing content from injection targets. Append only.
- If `.grimoire` already exists, present a modification plan showing what will be added alongside what already exists. Do not treat existing content as an error.
- Use the directory structure defined in references. Do not improvise.
