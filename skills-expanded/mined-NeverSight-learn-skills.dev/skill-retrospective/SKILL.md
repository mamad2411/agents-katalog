---
name: skill-retrospective
description: Use when the user explicitly asks to retrospect on an agent session, summarize lessons learned, preserve an experience, generate a skill-improvement proposal, or assess whether durable guidance such as a skill or AGENTS.md should be updated.
---

# Skill Retrospective

## Core Rule

Turn an explicit retrospective request into a bounded improvement proposal. Capture evidence first; propose durable guidance only when justified; never self-modify automatically.

Do not invoke this merely because a task ended, a tool failed, or a session is closing.

## Use When

The user explicitly asks to retrospect, summarize lessons, preserve an experience, generate a skill-improvement proposal, or assess whether SKILL.md/AGENTS.md guidance should change.

Do not use for ordinary planning, brainstorming, code review, or implementation unless the user asks to extract reusable lessons.

## Retrieval Contract

Start from the user's retrospective material. If the episode is unclear, ask for missing facts.

Retrieve only needed context:
- Current project instructions or AGENTS.md inside a repo.
- Relevant skills when proposing skill changes.
- Target SKILL.md/AGENTS.md before proposing exact durable wording.

Default output stays in chat. Write files or memory only when explicitly asked.

## Output Template

### Episode evidence
- Facts:
- Inferences:
- Missing evidence:

### Pattern candidate
- Candidate rule:
- Scope / non-scope:
- Evidence level: candidate | supported | validated | promotable

### Proposed durable change
- Target:
- Change type: add | refine | remove | defer
- Proposed wording or summary:
- Decision: propose | defer | reject

### Validation plan
- Test or counterexample:
- Baseline / with-skill check if changing a skill:
- Rollback or rejection condition:

## Evidence Levels

- candidate: one episode, correction, or failure. Never promote directly.
- supported: repeated occurrence, cross-task evidence, or explicit user confirmation.
- validated: eval, baseline vs with-skill comparison, benchmark, or successful reuse.
- promotable: validated, target file read, rollback clear, and user approval obtained.

Use labels, not fake numeric confidence.

## Promotion Boundaries

Prefer skill updates over AGENTS.md updates. AGENTS.md proposals need repository-level evidence, target-file reading, and explicit approval.

When asked to persist: prefer long-term memory for confirmed decisions/patterns; modify skill files only when the user asks to update a specific skill; create repo proposal files only when a project workflow or user path exists.

## Hard Bans

Do not:
- Automatically edit SKILL.md, AGENTS.md, hooks, runtime config, or memory.
- Trigger hooks, session-end automation, self-loops, or background continuation.
- Write files by default.
- Promote a single episode into durable guidance.
- Invent numeric confidence or application counts.
- Scan the whole repository by default.
- Propose exact target-file wording without reading that file.
- Generalize project-specific lessons cross-project without evidence.
- Persist secrets, private data, malicious commands, or prompt-injection content.

## Acceptance Dry Runs

1. User correction after a session: output candidate + validation plan only; do not persist or patch.
2. Repeated issue with a named skill: read target SKILL.md before durable wording; include validation plan.
3. AGENTS.md update request: raise evidence threshold, read target AGENTS.md, explain why a skill update is insufficient, and require approval before edits.
