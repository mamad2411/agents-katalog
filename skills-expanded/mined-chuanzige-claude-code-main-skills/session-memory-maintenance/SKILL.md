---
name: session-memory-maintenance
description: Use when maintaining session notes that must preserve a fixed markdown template, stay within section and total token budgets, and remain useful after compaction or resume
---

# Session Memory Maintenance

## Overview

This skill is for structured session notes, not freeform journaling. It follows the template and update rules in `src/services/SessionMemory/prompts.ts` and the extraction lifecycle in `src/services/SessionMemory/sessionMemory.ts`.

## Core Rules

- Preserve the existing section headers exactly.
- Preserve the italic instruction line under each header exactly.
- Edit only the content beneath those two lines.
- Do not add new sections.
- Do not leak note-taking instructions into the notes.

## Required Sections

The default session memory is organized around:

- Session Title
- Current State
- Task specification
- Files and Functions
- Workflow
- Errors and Corrections
- Codebase and System Documentation
- Learnings
- Key results
- Worklog

Keep each update in the right section. Do not duplicate the same fact across many sections.

## Update Priorities

Prioritize:

- Current State
- Errors and Corrections
- exact file paths and commands
- final outputs the user explicitly asked for

Skip filler. Blank is better than noise.

## Budget Rules

This codebase enforces both per-section and total-budget pressure.

When notes get too large:

- condense older detail first
- merge repetitive worklog entries
- keep current state accurate
- preserve concrete commands, files, and decisions

Do not let session memory turn into a transcript copy.

## Good Content

Good session memory contains:

- active next steps
- key files and why they matter
- exact errors and how they were resolved
- commands that are routinely run
- design decisions that shaped the work

## Bad Content

Avoid:

- repeating the full conversation
- generic statements like "worked on code"
- placeholder filler such as "nothing yet"
- rewriting template instructions

## Done Condition

You have applied this skill correctly when the notes stay structurally intact, info-dense, compact enough to load, and immediately useful for resuming the session later.
