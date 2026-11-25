---
name: skillforge-generator
description: Design, refine, and package Codex skills from a user goal, an existing workflow, or a source repository. Use when Codex needs to create a new skill, improve an existing skill, turn repeated work into a reusable process, or adapt an external skill idea into a Codex-native format.
---

# Skillforge Generator

Use a simple staged workflow to create skills that are actually reusable, instead of dumping notes into a folder.

## Core Rule

Start from the user's real repeated need, not from folder structure or documentation templates.

A good skill should help future work become:

- easier to trigger
- more consistent
- less dependent on long explanations

## Workflow

### 1. Define the job

Write the skill in one sentence:

- what it helps do
- when it should be used
- what kind of user request should trigger it

If that sentence is vague, the skill is not ready.

### 2. Collect real examples

Ask or infer a few realistic requests the user would actually make.

Prefer examples like:

- "帮我把一个外部 skill 改造成 Codex 版"
- "把重复的发布流程做成一个技能"
- "以后遇到这种文档整理任务，按固定步骤处理"

Use the examples to decide what belongs in the skill and what does not.

### 3. Separate reusable parts

Split the future skill into only the pieces that will save time repeatedly:

- `SKILL.md` for the working method
- `scripts/` for deterministic helper code
- `references/` for detailed docs only loaded when needed
- `assets/` for templates or starter files

Do not create extra files just to look complete.

### 4. Keep the trigger strong

The frontmatter `description` is the trigger. Make it explicit:

- what the skill does
- when to use it
- what kinds of tasks or files should activate it

Do not hide trigger logic in the body.

### 5. Write for execution

The body should tell another Codex instance how to succeed:

- what to inspect first
- what order to work in
- what to avoid
- what to validate before finishing

Prefer short commands, decision rules, and practical defaults over theory.

### 6. Validate the shape

Check that the skill is:

- small enough to read quickly
- specific enough to trigger reliably
- practical enough to use on the next real task

If a section would not change future execution, remove it.

### 7. Improve after use

After using the skill on a real task, tighten it based on friction:

- add missing steps
- move bulky details into `references/`
- add scripts only when repeated handwork appears
- delete vague guidance that did not help

## Default Build Pattern

When creating a skill, prefer this order:

1. decide the job
2. collect concrete examples
3. identify reusable resources
4. create the folder
5. write a concise `SKILL.md`
6. validate
7. refine after real use

For a fuller checklist and prompt pattern, read [skillforge-method.md](./references/skillforge-method.md).

## Codex Adaptation Notes

When adapting ideas from non-Codex systems:

- keep the method, not the branding
- remove tool assumptions that do not exist locally
- rewrite paths, commands, and user prompts for Codex
- prefer one focused skill over importing a giant external system

## Output Standard

A finished skill should leave behind:

- a clear `SKILL.md`
- only the resource folders that are truly needed
- a usable trigger description
- a short explanation of how it helps future work

## Language Rule

Show user-facing explanations in Chinese by default.

English may still appear in technical identifiers such as skill names, folder names, and frontmatter fields, but the explanation given to the user should be Chinese unless the user explicitly requests another language.
