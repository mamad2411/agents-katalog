---
name: cursor-continual-learning
description: Orchestrate continual learning by delegating transcript mining and AGENTS.md updates to `agents-memory-updater`.
disable-model-invocation: true
---

## Runtime selection

Before runtime-dependent work, read [execution selection](references/runtime/selection.md). In a verified T3 host follow [the T3 contract](references/runtime/t3.md) and its method reference; the inline section below is the native Codex branch, not literal T3 dispatch. Outside T3, native Codex follows that inline branch unchanged. If the host is ambiguous or a required capability is unavailable, report the gap; a permission refusal never authorizes switching branches.

## Native Codex branch

# Continual learning proposal for Codex

Use this only when the user explicitly asks to mine supplied task history or when an operator-enabled trusted project workflow invokes it.

## Workflow

1. Verify the transcript is explicitly authorized, belongs to the current workspace/task scope, and excludes secrets and unrelated private conversations.
2. Delegate the transcript review to one bounded native memory curator with an explicit proposal-only briefing. The coordinator supplies the exact input path and requests a proposal-only result.
3. Ask the curator to identify durable candidate rules, cite their source lines or hashes, deduplicate them against current instructions, and distinguish user authority from temporary task wording.
4. Return a reviewable proposal and receipt. Do not edit `AGENTS.md`, global memory, repository instructions, hooks, or runtime state unless the user separately authorizes that exact write.
5. If the transcript or native delegate is unavailable, return `not-run` and leave all outputs unchanged.

Automatic Stop-hook triggering remains unavailable. The observed native proof reviewed one explicitly authorized local transcript, produced a hashed proposal, and performed no repository, instruction, memory, hook, or global-state write.
