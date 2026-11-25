---
name: using-superpowers
description: Use when the user asks to use Superpowers-style workflows, add external process skills, or enforce a structured skill-first workflow; adapts Superpowers principles to this research-agent system without replacing local source-first, quality-gate, and window-separation rules.
---

# Using Superpowers

Use this as a project-safe adapter for Superpowers-style workflows.

## Purpose

Bring the useful discipline from Superpowers into this research agent:

- check which skills apply before acting;
- use brainstorming before unclear design or workflow changes;
- use explicit plans before risky implementation;
- verify before claiming completion.

This skill does not replace `agent-orchestration`. In this project, `agent-orchestration` remains the primary router.

## Workflow

1. Classify the task with `agent-orchestration`.
2. Decide whether the task needs:
   - `brainstorming` for unclear ideas or workflow design;
   - `project-skill-creator-governance` plus system `skill-creator` for new or updated skills;
   - `playwright-dissertation-browser` plus global `playwright` for browser automation;
   - `markitdown` for file-to-Markdown conversion;
   - source-first and document-quality gates for formal outputs.
3. State the selected workflow briefly for substantial tasks.
4. Do not add heavy planning to simple chat answers.
5. Record rule or skill changes in `research-wiki/TASK_STATE.md`.

## Project Boundaries

- Do not install the full external Superpowers package unless the user explicitly requests that separate step.
- Do not let Superpowers-style rules override source-first checks.
- Do not force brainstorming for small, obvious, or sensitive single-document edits.
- Do not trigger code-development workflows for dissertation writing unless the task is actually technical.
- For Production Window work, still write a Production run receipt when the task is substantial.

## When To Skip

Skip this skill when:

- the task is a direct factual answer;
- the relevant dissertation skill is already obvious and sufficient;
- the user asks for a quick maintenance status;
- the task involves sensitive participant data and no workflow design is needed.

