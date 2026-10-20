---
name: llm-context-builder
description: Reconstruct trustworthy working context from recent Codex sessions, Claude Code sessions, Claude Cowork traces, memories, rollout summaries, repository history, and connected source systems. Use when asked to look across prior sessions, recover earlier decisions, build a handoff prompt, trace how a feature evolved, or assemble an evidence-backed brief from scattered history.
---

# Build Cross-Session Context

Recover only the context needed for the user's current decision or task. Prefer an evidence trail over a large undifferentiated dump.

## Scope

1. Define the target question, project, and lookback window. Default to 30 days; honor a requested window.
2. Search sources in this order:
   - Recent Codex session summaries or local rollout files
   - Claude Code project sessions and project memories
   - Claude Cowork local-agent session traces
   - Chronicle, when enabled, for discovery only
   - Repository history, issues, pull requests, documents, email, or other source systems for confirmation
3. Inspect existing briefs, memories, skills, agents, and automations before creating a new artifact.

Typical local roots include:

- `~/.codex/sessions/` and `~/.codex/archived_sessions/`
- `~/.claude/projects/` and project `memory/` folders
- `~/Library/Application Support/Claude/local-agent-mode-sessions/`

Treat paths as hints, not guarantees. Search narrowly by date, project, and distinctive terms before opening large files.

## Evidence Rules

- Separate direct evidence from inference.
- Attach a date and source type to every important claim.
- Prefer the original task, commit, PR, document, or message over a later summary.
- Use memories and Chronicle to locate evidence, not as sole proof for consequential details.
- De-duplicate repeated prompts, injected skill text, scheduled-task boilerplate, tool output, and copied context.
- Do not expose credentials, tokens, client secrets, private keys, or unrelated personal data found in histories.
- State when a source was unavailable or when evidence is incomplete.

## Workflow

1. Build a compact event index: date, source, project, user intent, output, and unresolved state.
2. Cluster events by repeated workflow or decision thread.
3. Confirm high-impact details in the relevant source system when possible.
4. Extract:
   - stable facts and constraints
   - decisions and their rationale
   - artifacts already created
   - open questions and contradictions
   - next action or stopping condition
5. Produce the smallest useful output:
   - a concise context brief for human use
   - a copy-paste handoff prompt for another agent
   - a dated decision timeline
   - a shortlist of recurring workflows worth packaging
6. Save a file only when the user asks or when the artifact is clearly intended for reuse.

## Output Format

Lead with a short synthesis, then use:

- **Confirmed context** — claim, date, and source
- **Decisions and rationale** — what changed and why
- **Existing artifacts** — reusable files, branches, PRs, decks, or notes
- **Open questions** — missing or conflicting evidence
- **Recommended next step** — one bounded action or stopping condition

For workflow-packaging audits, add frequency/confidence, existing coverage, and a recommendation of extend, skill, subagent, automation, or skip.

