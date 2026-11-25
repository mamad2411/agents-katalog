---
name: agent-instruction-pairing
description: Set up and maintain paired CLAUDE.md and AGENTS.md files for cross-runner agent-instruction parity across repo roots and nested packages. Use when users ask about CLAUDE.md, AGENTS.md, agent instructions, repo guidance, nested package instructions, or syncing agent policy files.
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---


# Agent Instruction Pairing

Use this skill when the user wants to create, repair, or reason about repo instruction files for Claude Code, Codex, PI, or other agent runners that look for `CLAUDE.md` and/or `AGENTS.md`.

This skill is operational, not theoretical. Default to making the filesystem safer for cross-runner behavior.

## Primary Rule

If a directory needs agent instructions, prefer a paired-file layout:

- `CLAUDE.md`
- `AGENTS.md`

Do this at:

- the repo root
- any nested package, app, or work area that needs local overrides

Keep the pair aligned within each directory unless the user explicitly wants divergence.

## Why This Rule Exists

The saved eval at `docs/research/agent-instruction-eval/README.md` on 2026-07-30 showed:

- `claude` strongly honored paired setups and preferred `CLAUDE.md` in same-directory conflicts
- `codex` behaved better with paired layouts than mixed parent/child filename layouts and preferred `AGENTS.md` in the direct conflict probe
- `pi` also preferred `AGENTS.md` in the direct conflict probe

The portable conclusion is simple: a single-file or mixed-file strategy is weaker than keeping both files present and aligned.

## When To Apply This Skill

Use this skill when prompts include things like:

- "set up CLAUDE.md"
- "set up AGENTS.md"
- "add repo agent instructions"
- "make package instructions work for Claude and Codex"
- "sync agent policy files"
- "nested package guidance"
- "why is one runner ignoring CLAUDE.md"

## Default Operating Policy

### Root Policy

At the repo root, create both `CLAUDE.md` and `AGENTS.md` when the user asks for instruction setup or repair.

If only one exists, create the missing peer file and align it with the existing one unless the user wants a deliberate split.

### Child Policy

If a child directory needs different instructions from the root, create or maintain both files in that child directory as well.

Do not rely on:

- root-only `CLAUDE.md` plus child-only `AGENTS.md`
- root-only `AGENTS.md` plus child-only `CLAUDE.md`
- any other mixed-file parent/child arrangement when parity matters

### Override Policy

If a child directory intentionally differs from the root:

- mirror that child-local override into both `CLAUDE.md` and `AGENTS.md` in the child directory
- keep the two child files semantically equivalent
- document the override briefly so later edits do not accidentally collapse it back to root behavior

### Maintenance Policy

When editing one file in a pair, update its sibling in the same change unless the user explicitly wants a one-runner experiment.

If the pair drifts, repair the drift instead of adding more runner-specific branching.

## Recommended Workflow

1. Inspect the root for existing `CLAUDE.md` and `AGENTS.md`.
2. Inspect nested packages or apps that the user expects agents to work inside.
3. If a directory has one file but not the other, create the missing peer.
4. If a directory has both but they differ accidentally, sync them.
5. If a directory needs a local override, apply the override to both filenames in that directory.
6. Summarize which directories now own local instruction scope.

## Decision Rules

- If the user asks for maximum portability, choose the paired-file layout.
- If the user asks which single file to prefer, explain that single-file preference is runner-dependent and recommend both instead.
- If the user asks whether to add child-local instructions, do it only where behavior truly differs from the parent.
- If the user asks whether an agent working from the root can still operate inside a child package, treat paired root plus paired child files as the safest layout.

## Anti-Patterns

- Do not recommend a root-only `CLAUDE.md` as universally sufficient.
- Do not recommend a root-only `AGENTS.md` as universally sufficient.
- Do not leave a directory with only one file when parity matters.
- Do not keep conflicting sibling files in the same directory unless the user is explicitly running an experiment.
- Do not assume mixed parent/child filename layouts will behave consistently across runners.

## Response Pattern

When advising or editing, be explicit:

- say which directories should own instruction files
- say whether the root and child directories should inherit or override
- say that both filenames should be kept aligned

If asked for rationale, cite the saved eval in `docs/research/agent-instruction-eval/README.md`.
