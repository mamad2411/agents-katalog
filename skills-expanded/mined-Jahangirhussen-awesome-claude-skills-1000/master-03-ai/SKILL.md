---
name: master-03-ai
description: 03-AI domain of the master skills library (LLM apps, agents, MCP, RAG, prompt/context engineering, ML and evaluation). Use when the task needs AI/ML application design, evaluation or tooling and no more specific installed skill matches. Not when a specific installed ML/LLM skill matches.
---

# 03-AI

## Purpose
Index for LLM apps, agents, MCP, RAG, prompt/context engineering, ML and evaluation: imported skills (read in place) and a pointer to the installed skills in this domain.

## When to use
The task needs AI/ML application design, evaluation or tooling.

## When NOT to use
- A specific installed ML/LLM skill matches.
- Another domain fits better (see `../ROUTER.md`).

## Inputs
The task, project context, and constraints; domain is inferred by the orchestrator.

## Core workflow
1. Check the imported skills below; if one fits, open its `SKILL.md` and follow it.
2. Otherwise open `INSTALLED.md` in this folder (installed skills per subdomain) and invoke the matching skill with the Skill tool.
3. For cross-domain needs follow `../DEPENDENCIES.md` instead of duplicating instructions.
4. Execute, verify, report.

## Decision rules
- Prefer the most specific skill; prefer installed canonical skills over imported generic ones.
- Open one skill at a time; do not read the whole folder.

## Edge cases and failure handling
- No fitting skill -> use general capability and say no adequate skill exists; do not invent one.
- Imported skill depends on an unavailable external service -> use the nearest installed alternative.

## Validation
Check the chosen skill's instructions match the task and that its output is verified with the matching testing/validation approach.

## Output requirements
The task result as a short `DONE`; no routing narration.

## Example
Request in this domain -> orchestrator selects the skill from the list below or `INSTALLED.md` -> follow its steps -> verify -> report.

## Imported skills (read the SKILL.md at the path when relevant)
- `agents/agents-in-the-team/SKILL.md` - Run delivery when AI coding and ops agents take tickets. Use when setting agent delegation policy, writing agent-ready tickets, planning rev
- `ai-development/ai-prototyping/SKILL.md` - Idea to AI-generated prototype to customer validation to engineering handoff. Use when deciding prototype vs spec, choosing fidelity, briefi
- `ai-evaluation/langsmith-fetch/SKILL.md` - Debug LangChain and LangGraph agents by fetching execution traces from LangSmith Studio. Use when debugging agent behavior, investigating er

## Related skills
`../ROUTER.md`, `../DEPENDENCIES.md`, `../RULES.md`, `INSTALLED.md`.
