---
name: cursor-setup-pstack
description: Configure which models pstack uses per role and at what reasoning budget. Detects your available models and writes an always-applied rule that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
disable-model-invocation: true
---

## Runtime selection

Before runtime-dependent work, read [execution selection](references/runtime/selection.md). In a verified T3 host follow [the T3 contract](references/runtime/t3.md) and its method reference; the inline section below is the native Codex branch, not literal T3 dispatch. Outside T3, native Codex follows that inline branch unchanged. If the host is ambiguous or a required capability is unavailable, report the gap; a permission refusal never authorizes switching branches.

## Native Codex branch

# Setup pstack for Codex

Configure the requested Pstack role mapping through the standing `model-capability-router` and actual native model inventory. Preserve the operator's explicit selections and native named-role bindings. Do not write a Cursor rule or introduce another model policy.

1. Detect the models and efforts accepted by the execution channel that will run each role. Treat `auto` and `inherit-parent` as inheritance, not invented model identities.
2. Load existing choices. Current Pstack roles are `feature, refactoring`, `bug-fix`, `perf-issue`, `hillclimb`, `judgment and prose`, `arena runners`, `arena cross-judge pool`, `swarm workers`, and `interrogate reviewers`. Retire obsolete Pstack proposal rows; this does not authorize deleting native specialist bindings or unrelated operator configuration. Preserve explicit user choices for the current roles.
3. Choose one setup mode. Preserve an explicitly selected role-aware preset from `model-capability-router` and its `references/pstack-role-presets.json`; recommend its classes only for unbound roles, preserving explicit overrides. Do not combine a preset with an upstream global budget. Otherwise offer `large — xhigh reasoning`, `medium — high reasoning`, or `small — medium reasoning`. Large keeps each role's starting effort, medium lowers it one step, and small lowers it two, on `xhigh > high > medium > low`, stopping at low. These labels describe the common starting level, not a command to raise every role to it. Do not propose an effort above xhigh for this Pstack setup. Existing native policies and explicit selections still govern actual execution. Leave inheritance aliases unchanged.
4. Show and validate the resulting mapping against detected capabilities. A runner or reviewer list has one seat per entry. The Arena judge tries eligible entries in pool order from a different vendor than the parent; Fable and Opus share a vendor. Inheriting aliases cannot supply an independent judge. Report an unavailable entry instead of substituting an unsupported model.
5. Apply only the requested scope through the existing native/project configuration or the canonical router source. Task-local choices stay in the task brief. Read back any authorized write. A fixture or accepted request does not prove effective future-session selection.
6. Report what changed, retired proposal rows and any unresolved capability. Offer `cursor-create-verification-skill` and `cursor-create-formal-verification-skill` once each when the project lacks the corresponding proof path; invoke either only if requested.
