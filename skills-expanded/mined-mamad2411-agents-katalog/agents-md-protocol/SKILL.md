---
name: agents-md-protocol
description: >
  Create or review an AGENTS.md file so coding agents get stable repo-local
  instructions: environment setup, testing, style, security boundaries, PR
  policy, and handoff rules. Use when a repo lacks durable agent guidance or
  when a custom harness needs a predictable context file.
---

# AGENTS.md Protocol

## Purpose

Create or tighten a repository-level `AGENTS.md` contract for coding agents.
Treat it as durable operating context, not a chat prompt.

## When to Use

- Repo has no `AGENTS.md`, `CLAUDE.md`, or equivalent agent instructions.
- Existing instructions are stale, vague, or missing test commands.
- A custom/API/local harness needs stable context it can load every run.
- A multi-agent workflow needs explicit handoff and review rules.

## Procedure

1. Inspect repo layout, package managers, CI files, and test commands.
2. Capture only durable facts and team rules.
3. Keep commands exact and runnable from the documented directory.
4. Add security and destructive-operation boundaries.
5. Add PR/review expectations and required verification.
6. Keep the file short enough to load every session.

## Recommended Sections

- `Dev environment tips`
- `Testing instructions`
- `Build and lint`
- `Code style`
- `Security boundaries`
- `PR instructions`
- `Agent handoff notes`

## Quality Bar

- Every command has a working directory or clear scope.
- No secrets, tokens, or private URLs.
- No vague rules such as "be careful" without a concrete check.
- No roadmap or marketing text.
- Instructions match current CI and package metadata.

## Harness Attachment

For non-Claude-Code harnesses, load `AGENTS.md` as outer-loop project context.
The harness should also keep explicit task state outside conversation history.
