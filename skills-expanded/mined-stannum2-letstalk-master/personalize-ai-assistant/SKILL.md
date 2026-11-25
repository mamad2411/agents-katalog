---
name: personalize-ai-assistant
description: Build or update privacy-first AI-assistant configuration and reusable preference skills for Codex, Claude Code, Cursor, Gemini CLI, and similar tools. Use when the user provides explicit preferences, existing config files, example rules, or asks to optimize AGENTS.md, CLAUDE.md, assistant rules, memory files, or package a repeated workflow into a durable custom skill/config.
---

# Personalize AI Assistant

## Overview

Use this skill to turn explicit, user-approved preferences into durable, auditable assistant behavior: configuration rules, project/user instruction files, or a new custom skill. The goal is not to flatter the user; it is to make future assistants behave consistently with clear, reviewable instructions.

## Core Workflow

1. **Scope the target.** Identify whether the user wants global personalization, project-local behavior, a new skill, or a specific assistant config such as `AGENTS.md` or `CLAUDE.md`. If unspecified, default to a global user-level config plus a short evidence summary.
2. **Audit available surfaces.** Run `scripts/detect_personalization_context.py` when local files are relevant. Inspect existing config files before editing and preserve their intent.
3. **Collect approved evidence.** Use only explicit user instructions, user-provided examples/files, current task constraints, local project conventions, and existing skills/configs. Do not inspect private logs, transcripts, shell data, mail, browser data, credential stores, or unrelated personal files unless the user provides the exact artifact and asks.
4. **Build an evidence ledger.** For each candidate preference, record the observed behavior, source, confidence, proposed rule, destination config, and risk. Read `references/personalization-model.md` for scoring and rule-writing patterns.
5. **Choose the packaging layer.** Read `references/config-targets.md` before editing assistant config files. Use a config rule for broad behavior, a project file for repository-specific norms, and a new skill only when the workflow is reusable and specialized.
6. **Patch safely.** Make small, reviewable edits. Prefer appending or replacing a clearly named personalization section over rewriting unrelated config. Back up only when the file is large, fragile, or not version controlled.
7. **Validate and report.** Read the final file, run skill validation when a skill is created or changed, and summarize what changed, why, and what approved evidence supported it.

## Evidence Rules

- Treat explicit user instructions as highest priority.
- Treat explicit standing instructions as stronger than one-off task constraints.
- Separate stable preferences from one-off task constraints.
- Mark inferred preferences as inferred; do not present them as user-stated facts.
- Exclude secrets, credentials, private identities, and unnecessary personal data from config files.
- Do not encode brittle rules such as exact wording quirks unless the user repeatedly asks for them.

## Packaging Decision

Use this priority order:

1. **Existing config edit** for broad communication, safety, workflow, or tool-use preferences.
2. **Project-local instruction file** when behavior applies only to one repository, document set, or product.
3. **Reference file** when the content is useful but too detailed for the main config.
4. **New custom skill** when the user repeatedly asks for the same domain workflow, with reusable scripts, references, or templates.
5. **No persistent change** when evidence is weak, sensitive, temporary, or likely to cause future overfitting.

## Output Shape

When finishing a personalization task, include:

- The file(s) changed, with absolute links when local.
- The top 3-7 preferences or workflows addressed.
- Any rules intentionally not added because confidence was low or the content was sensitive.
- Validation performed, such as reading the final config or running `quick_validate.py` for a skill.

## Resource Guide

- `scripts/detect_personalization_context.py`: list candidate assistant config files and skill directories without reading file contents.
- `references/personalization-model.md`: evidence taxonomy, confidence scoring, and instruction-writing templates.
- `references/config-targets.md`: common configuration targets and safe editing guidance across assistants.
