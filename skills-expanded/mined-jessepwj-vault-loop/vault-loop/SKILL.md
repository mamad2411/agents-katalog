---
name: vault-loop
description: "Design recurring knowledge-base update loops for Obsidian-style vaults, project wikis, second-brain folders, and research notebooks. Use when setting up automated source ingestion, daily reflection, meeting-note processing, health checks, state cursors, runbooks, scheduler prompts, or validation gates for a maintained knowledge system."
---

# Vault Loop

Use this skill to create a recurring maintenance loop for a knowledge base.

The goal is not to copy a private automation setup. The goal is to create a small, durable loop with state, runbooks, validation, and recovery rules.

## Workflow

1. Restore context from the user's local agent instructions and shortest recent cache, if they exist.
2. Ask only for missing source scope, privacy boundary, runtime, and first lane.
3. Define a lane with `lane_id`, purpose, source, frequency, state file, run artifacts, writeback targets, validation gate, failure behavior, and notification behavior.
4. Create or update a runbook and state file.
5. Draft a self-contained scheduler prompt.
6. Verify that validation and state advancement rules are explicit.
7. Report active, paused, proposed, and blocked lanes.

## Required Rules

- Use compensation windows: `last_success_at - overlap_minutes -> trigger_start`.
- Do not advance `last_success_at` after partial coverage, missing validation, health errors, or unresolved pending queues.
- Keep raw sources immutable when the vault has a raw layer.
- Write durable knowledge to object pages, not only dated run logs.
- Separate knowledge update lanes from notifications and outbound actions.
- Ask before scanning broad personal files, chats, drives, browser history, or cloud accounts.
- Do not send private knowledge into public posts, messages, issues, or tasks without explicit permission.

## Artifact Shape

Every recurring lane should have:

- a state file with `last_success_at`, `overlap_minutes`, `pending`, `last_run`, and `known_blockers`;
- a runbook with workflow, recovery steps, and completion rules;
- dated plan/run/review artifacts;
- a validation checklist or deterministic validation script;
- a scheduler prompt that another agent can run without hidden context.

## Completion Gate

Only mark a lane setup complete when:

- source scope is explicit;
- privacy boundary is explicit;
- state cursor exists;
- runbook explains blocked recovery;
- scheduler prompt includes startup, source collection, writeback, validation, health, and state advancement rules;
- validation has been run or the remaining blocker is named.

