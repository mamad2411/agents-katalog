---
name: architecture-discovery
description: "Research before implementation. Use for questions starting with: исследуй, проанализируй, сравни, как лучше, перед, нужно выбрать / research, analyze, investigate, compare, before adding/refactoring, how does interact. The goal is understanding architecture, dependencies, options, or patterns before coding. Not for writing code, reviewing diffs, verifying tests, deploying, or basic explanations."
user-invocable: true
allowed-tools:
  - Read
  - Bash(git *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(cat *)
  - Bash(rg *)
  - Bash(jq *)
---

# Skill: Architecture Discovery

## Purpose

Use this skill to turn unclear technical direction into a concise Architecture Brief before normal SDD planning and coding.

This is optional research support for Control Tower / architect-like planning work. It is not a mandatory role, approval gate, or workflow stage.

## When to Use

- New projects or major modules
- Unclear technical direction
- Stack or library selection
- API contract design
- DB/schema/storage design
- Third-party integrations or unknown APIs
- Security-sensitive design
- Large refactors with architecture risk

## When to Skip

- Small bugfixes
- Text-only or doc-only edits
- Minor CSS/UI changes
- Tasks with an already approved implementation plan
- Local changes where repo conventions already make the design obvious

## Allowed Inputs

- Owner request, ticket, or Work Block
- Relevant `AGENTS.md`, memory bank, tasklist, spec, plan, and repo files
- Existing implementation, schemas, routes, tests, deploy docs, and operational constraints
- External documentation or references when needed for the decision

## Research Sources

Prefer official and primary sources.

Allowed sources:
- Repository files and current project docs
- Official vendor documentation
- GitHub repositories, issues, releases, and examples
- Available MCP tools
- Package/library documentation
- Public technical references

Record important links and source names in the Architecture Brief. If MCP, GitHub, web, or external docs are unavailable, continue with local repo analysis and state the limitation.

## Hard Limits

- Do not install packages without Owner approval.
- Do not use real credentials unless explicitly authorized.
- Do not call production APIs without Owner approval.
- Do not apply migrations or deploy.
- Do not run destructive git operations.
- Do not change production code as part of discovery.
- Do not expand scope beyond the approved research question.

## Workflow

1. State stage, objective, role, expected result, scope, and out of scope.
2. Read the canonical project context first: `AGENTS.md`, `.agent/workflows/sdd-protocol.md`, `.agent/ROSTER.md`, and relevant memory/task/spec files.
3. Inspect existing repo conventions before proposing new architecture.
4. Research only the uncertain areas needed for the decision.
   For broad research, use read-only scoped subagents for independent slices and
   consolidate their findings into one brief.
5. Compare practical options, including "keep current approach" when valid.
6. Recommend one approach with boundaries, risks, and verification needs.
7. Hand off to normal SDD planning with a proposed Work Block.

## Required Output

Produce an Architecture Brief using `docs/templates/architecture-brief-template.md`.

The brief must include:
- Problem statement and assumptions
- Existing system/repo findings
- Research sources used
- Options considered
- Recommended approach and stack
- Architecture boundaries
- Data model / storage model
- API / integration contracts
- Security, privacy, and operational constraints
- Risks, implementation plan, acceptance criteria, and open questions
- Recommended next SDD Work Block

## Handoff

- **Success condition**: Architecture Brief is complete enough for Control Tower to create a scoped SDD Work Block.
- **Next**: `task-decomposition` or Stage 0 · Plan & Discover in `.agent/workflows/sdd-protocol.md`.
- **Auto-proceed**: 🟢 YES for read-only discovery inside approved scope.
- **Hard stop**: 🔴 YES for package install, credentials, production API calls, migrations, deploys, destructive git operations, or production code changes.
