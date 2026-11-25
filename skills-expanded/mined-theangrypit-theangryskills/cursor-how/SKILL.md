---
name: cursor-how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
disable-model-invocation: true
---

## Runtime selection

Before runtime-dependent work, read [execution selection](references/runtime/selection.md). In a verified T3 host follow [the T3 contract](references/runtime/t3.md) and its method reference; the inline section below is the native Codex branch, not literal T3 dispatch. Outside T3, native Codex follows that inline branch unchanged. If the host is ambiguous or a required capability is unavailable, report the gap; a permission refusal never authorizes switching branches.

## Native Codex branch

# How

Explore the codebase to answer "how does X work?" questions. If scope is ambiguous, state your interpretation and explore; the user can redirect.

## 1. Explain

Use one authorized native read-only delegate that explores and explains in one pass. Give it the user's question and this brief:

> You are writing an architectural explanation for a senior engineer. Explore the codebase and write an explanation that a senior engineer unfamiliar with this area could read and walk away with a solid mental model. They should understand the architecture well enough to start working in it confidently. You have read-only access to the codebase.

Use the actual native delegation interface and the operator's model selection. If read-only delegation is unavailable, report that capability gap; do not replace this with an explorer panel or a separate synthesis stage.

## 2. Present

Present the delegate's output. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.
