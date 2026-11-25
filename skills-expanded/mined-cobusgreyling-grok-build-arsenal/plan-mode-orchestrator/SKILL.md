---
name: plan-mode-orchestrator
description: For any non-trivial task, start in Plan Mode, produce a clear step-by-step plan with risks and verification method, and wait for explicit approval before any edits. Use when the user says "plan this", "use plan mode", "don't edit yet", or describes a complex feature/refactor/migration.
version: 1.0.0
author: Cobus Greyling
---

# Plan Mode Orchestrator

The single most important skill in this arsenal. Enforces disciplined agentic work.

## When to Use
- User asks for a plan or explicitly says "plan mode"
- Task is larger than a single obvious edit
- Risk of breaking changes, architecture impact, or many files
- User says "don't write code yet"

## Core Behavior

1. **Immediately enter or confirm Plan Mode mindset.**
   - Explicitly state: "Entering Plan Mode. I will not edit files until you approve a plan."

2. **Investigate first (read-only where possible).**
   - Use subagents for broad investigation if the scope is large.
   - Run `grok inspect` if configuration or skills may be relevant.
   - Gather evidence: relevant files, existing patterns, tests, risks.

3. **Produce a high-quality plan with these sections:**
   - Goal (one sentence)
   - Current state (what exists today)
   - Proposed changes (numbered, smallest possible steps)
   - Files likely to change
   - Risks and mitigations
   - Verification method (tests, manual steps, `grok inspect`, etc.)
   - Estimated diff size / complexity

4. **Present the plan and STOP.**
   - Do not proceed to implementation.
   - Ask for approval: "Does this plan look good? Any changes before I proceed?"

5. **After approval:**
   - Execute one step at a time where possible.
   - Re-verify after each meaningful chunk.
   - Use other skills (tdd-intelligence, git-discipline, etc.) as appropriate.

## Subagent Usage
For large investigations, spawn 2–4 subagents with clear charters (e.g., "backend impact", "frontend impact", "test surface", "security surface") then synthesize.

## Success Criteria
- User has explicitly approved the plan (or a revised version).
- All subsequent edits are traceable to the approved plan.
- Verification steps from the plan were actually performed.

## Anti-Patterns to Avoid
- Jumping into edits "just to explore".
- Vague plans ("I'll refactor the auth layer").
- Plans that are really just implementation notes.

## Example Trigger Phrases
- "Plan the migration to the new MCP protocol"
- "Use Plan Mode to add the arena runner feature"
- "Don't edit anything yet, just plan the security hardening"
