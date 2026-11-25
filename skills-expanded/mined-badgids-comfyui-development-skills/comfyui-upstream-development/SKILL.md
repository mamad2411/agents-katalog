---
name: comfyui-upstream-development
description: Use when preparing changes intended for Comfy-Org repositories, aligning with current upstream architecture, reviewing RFC-related work, writing upstream-facing tests/docs, or preparing a PR-quality change for ComfyUI or related official repositories.
metadata:
  version: "00.01.11"
---
# ComfyUI Upstream Development

## Repository-local agent guidance

Before changing an official repository, inspect its current repository-local instructions when present: `AGENTS.md`, `CLAUDE.md`, `.claude/skills/`, `.claude/commands/`, `.cursor/skills/`, CONTRIBUTING files, and developer READMEs. Treat those as process guidance for that repository. Do not import the global `comfy-claude-prompt-library` wholesale, and do not let prompt guidance override the repository's implementation or version-matched API contract.

## Procedure

1. Refresh the relevant official repository and inspect current contribution guidance without modifying the user's checkout unexpectedly.
2. Search open/current architecture and tests before designing a new abstraction.
3. Search RFCs for related proposals, but confirm shipped implementation separately.
4. Keep scope narrow enough to review.
5. Add or update tests that demonstrate the intended contract.
6. Update docs when public behavior changes.
7. Run the repository's current required checks.
8. Review the diff for accidental generated/vendor changes.
9. Do not push, open a PR, or rewrite history unless explicitly requested.

## Upstream compatibility

Avoid solving a local extension problem by adding a core API unless the change is broadly justified. Conversely, do not build fragile monkey patches when an upstream extension point already exists.

## RFC use

When a change is substantial enough to intersect an RFC area, determine whether the current project expects an RFC before implementation. Do not invent process requirements; inspect current repository guidance.

## Acceptance gate

Before calling an upstream change PR-ready:

- verify current contribution guidance for the owning Comfy-Org repository;
- keep the diff scoped to the intended contract;
- add or update tests and public docs when required;
- run the repository's relevant current checks;
- inspect the final diff for accidental generated or vendor changes;
- do not push, rewrite history, or open a PR unless the user explicitly asks.

