---
name: cursor-poteto-help
description: Guides users through pstack setup, /poteto-mode, and picking the skill, playbook, or principle for a task. Type /poteto-help with a question.
disable-model-invocation: true
---

## Runtime selection

Before runtime-dependent work, read [execution selection](references/runtime/selection.md). In a verified T3 host follow [the T3 contract](references/runtime/t3.md) and its method reference; the inline section below is the native Codex branch, not literal T3 dispatch. Outside T3, native Codex follows that inline branch unchanged. If the host is ambiguous or a required capability is unavailable, report the gap; a permission refusal never authorizes switching branches.

## Native Codex branch

# Poteto help

Answer the user's Pstack question, give them a usable prompt, and link the current skill or guide that owns the answer. A help question does not start the workflow. An action request does: read `cursor-poteto-mode` and the relevant playbook, then carry out the authorized work.

Infer the need from the conversation: setup, starting a task, choosing a skill, repairing a run, or adapting Pstack. Ask one focused question only when it changes the answer. Read the destination before explaining it.

- Setup: `cursor-setup-pstack` maps current roles and three budgets through `model-capability-router`; native inventory and operator bindings govern. Source distribution does not install skills or enable Cursor Custom Modes, automation or `/loop`.
- Design: `cursor-architect` traces touched systems, sketches two shapes and chooses ownership and simple caller contracts. It uses `cursor-arena` for large or contested designs.
- Explanation: `cursor-how` uses one read-only explainer, then presents its output with light edits. `cursor-why` reads commits and PR discussions, cites authors and labels inference and gaps.
- Learning: `cursor-reflect` mines this conversation for durable improvements to existing skills, presents Accepted, Rejected and Backlog, and waits for approval before source edits.
- Execution: pick among the current 22 Poteto playbooks. Read `cursor-poteto-mode` for the list. Opening a PR does not start Babysit; Babysit stops at merge-ready, and Shipping requires the operator's merge grant.
- Proof: when the project lacks a way to drive the real artifact, mention `cursor-create-verification-skill`. For an invariant, race or property beyond example tests, mention `cursor-create-formal-verification-skill`. Generate either only if requested.

The bundled upstream guide pages document Cursor and are reference material. Use the actual native skill contracts for execution; an unavailable capability remains a disclosed gap, not a silently waived step. A new task needs explicit skill selection where the host requires it. Do not promise sticky modes, installed roles or runtime certification from source files.
