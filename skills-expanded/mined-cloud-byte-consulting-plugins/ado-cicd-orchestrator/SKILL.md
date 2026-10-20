---
name: ado-cicd-orchestrator
description: >-
  Primary entry for Azure DevOps CI/CD work across Claude, Copilot, Codex,
  Cursor, OpenCode, and Gemini: discover live org state, verify Microsoft
  guidance, assess SDLC maturity, produce Wiki-ready Mermaid diagrams, and
  deliver a governed architecture with a 30/60/90 roadmap. Read-only by
  default. Use for brownfield ADO assessments and modernization planning.
---

# Azure DevOps CI/CD Orchestrator

## Purpose

Coordinate the full azure-devops-cicd assessment pipeline on any Agent
Skills-compatible host. This skill is the portable equivalent of the Claude
`ado-cicd-orchestrator` agent. Prefer this skill when Claude-only `agents/*.md`
are not available.

## Pipeline (mandatory order)

1. Confirm org, project scope, Services vs Server version, and assessment window.
2. Run `ado-sdlc-discovery` (Azure CLI + `azure-devops` first; Azure DevOps MCP for gaps only).
3. Verify material recommendations with Microsoft Learn MCP (or current Learn docs if MCP is unavailable; disclose the gap).
4. Run `ado-cicd-architect` for scorecard, findings, target architecture, and 30/60/90 roadmap.
5. Produce current-state and target-state diagrams with `ado-wiki-mermaid` using `::: mermaid` fences.
6. Consult `domain-context` (and its domain checklists) only when language or platform specifics are material.
7. Deliver one Wiki-ready Markdown document. Publish only after explicit approval.

## Host behavior

On hosts that can spawn independent subagents (Claude Code, Cursor Agent, similar):

- You may delegate discovery, architecture, Mermaid, and domain checklists to focused subagents, each following the matching skill.
- Keep orchestration ownership here: sequencing, evidence handoff, final deliverable assembly.

On hosts without subagents (typical Copilot / Codex / Gemini / OpenCode skill runs):

- Execute the same pipeline sequentially in one session.
- Still keep role separation for PR reviews by following `ado-pr-review-gang` (independent Advocate, Skeptic, then Judge passes).

## Rules

- Discover before prescribing. Never invent live configuration.
- Discovery and assessment are read-only. No queues, policy edits, work-item edits, or Wiki publishes without explicit approval.
- No em dashes in ADO-facing output.
- Distinguish observed facts, access gaps, Microsoft guidance, book patterns, and judgment.
- For PR reviews, redirect to `ado-pr-review-gang` instead of doing a solo review here.
- Never print PATs, tokens, variable-group secrets, or secret-bearing logs.

## Starting prompt

> Use ado-cicd-orchestrator for org https://dev.azure.com/<org> project <project>. Read-only discovery via az devops. Produce a Wiki-ready assessment with ::: mermaid diagrams and a 30/60/90 roadmap. Do not queue pipelines or publish Wiki pages.
