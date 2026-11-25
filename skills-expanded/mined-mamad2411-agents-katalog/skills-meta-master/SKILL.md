---
name: skills-meta-master
description: Master hub for Skill authoring & meta. Use to author, scan, and manage Cursor skills, rules, hooks, and subagents. Bundles 15 specialized skills (in skills/<name>/GUIDE.md). Use this for any skills meta task.
---

# Skill authoring & meta — Master Hub

Use to author, scan, and manage Cursor skills, rules, hooks, and subagents.

## How to use this hub

This single skill bundles **all 15 skills meta skills**. Each bundled skill's full instructions live in `skills/<name>/GUIDE.md` (plus any `scripts/`, `data/`, `references/` next to it).

**Workflow:**
1. Match the user's request to one or more skills in the list below.
2. Read that skill's `skills/<name>/GUIDE.md` for full instructions before acting.
3. Combine multiple bundled skills when a task spans several areas.

## Bundled skills

- **anthropic-skill-creator** — Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a sk...  
  → `skills/anthropic-skill-creator/GUIDE.md`
- **blastum-skill-authoring** — Write and refactor agent skills using published best practices (Anthropic and others), emphasizing token efficiency and progressive disclosure. Use when authoring new skills, merging learning from ...  
  → `skills/blastum-skill-authoring/GUIDE.md`
- **blastum-skill-catalog** — Generate skill catalog documentation files. Use when creating organized lists of available skills with descriptions.  
  → `skills/blastum-skill-catalog/GUIDE.md`
- **blastum-subagents** — Designs and optimizes Cursor subagents. Use when creating subagents, designing delegation patterns, optimizing performance, or choosing between subagents vs skills vs commands vs rules.  
  → `skills/blastum-subagents/GUIDE.md`
- **blastum-tips** — Documents the U.S. Treasury Fiscal Data TIPS/CPI API and inflation-adjusted coupon and principal math. Use when integrating summary or detail endpoints, computing TIPS cashflows, or building ladder...  
  → `skills/blastum-tips/GUIDE.md`
- **building-skills-from-patterns** — When the same multi-step workflow repeats in Cursor (user corrections or agent redos), capture it as a new SKILL.md under .cursor/skills/ so future sessions load it automatically.  
  → `skills/building-skills-from-patterns/GUIDE.md`
- **cursor-skills-general** — General Cursor IDE best practices — project structure, code quality, workflow, extensions, and universal development guidelines. Use for any Cursor project setup or cross-language conventions.  
  → `skills/cursor-skills-general/GUIDE.md`
- **mattpocock-scaffold-exercises** — Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course s...  
  → `skills/mattpocock-scaffold-exercises/GUIDE.md`
- **mattpocock-setup-matt-pocock-skills** — Sets up an `## Agent skills` block in AGENTS.md/CLAUDE.md and `docs/agents/` so the engineering skills know this repo's issue tracker (GitHub or local markdown), triage label vocabulary, and domain...  
  → `skills/mattpocock-setup-matt-pocock-skills/GUIDE.md`
- **mattpocock-write-a-skill** — Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill.  
  → `skills/mattpocock-write-a-skill/GUIDE.md`
- **sentry-skill-scanner** — Scan agent skills for security issues. Use when asked to "scan a skill",  
  → `skills/sentry-skill-scanner/GUIDE.md`
- **sentry-skill-writer** — Create, synthesize, and iteratively improve agent skills following the Agent Skills specification. Use when asked to "create a skill", "write a skill", "synthesize sources into a skill", "improve a...  
  → `skills/sentry-skill-writer/GUIDE.md`
- **suggesting-cursor-hooks** — When the user keeps asking for the same check to run (lint, tests, type-check), suggest a Cursor hook to automate it.  
  → `skills/suggesting-cursor-hooks/GUIDE.md`
- **suggesting-cursor-rules** — When the user repeats the same correction or convention multiple times, suggest a Cursor rule to encode it permanently.  
  → `skills/suggesting-cursor-rules/GUIDE.md`
- **suggesting-skills** — When the user struggles with a task that a known skill could handle, suggest installing it.  
  → `skills/suggesting-skills/GUIDE.md`

## Note

These bundled skills are intentionally not registered as separate Cursor skills (their files are `GUIDE.md`, not `SKILL.md`) so only this master appears in the skills list. Read the relevant `GUIDE.md` on demand.
