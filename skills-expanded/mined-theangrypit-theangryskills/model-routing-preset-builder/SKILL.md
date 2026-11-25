---
name: model-routing-preset-builder
description: "Use when the operator explicitly wants to customise the GPT-only or OpenClaw subscription model-capability-router policy."
---

# Native Routing Policy Builder

Read the installed `model-capability-router` as the single baseline. Select
its GPT-only or OpenClaw subscription edition before changing model choices.
The OpenClaw edition is defined in `references/openclaw-subscriptions.md`
inside that router; use its task table and subscription-route checks instead
of imposing the GPT-only palette. Preserve all existing explicit bindings.

Read the selected edition's task table for model versions and efforts; do not
copy one edition's defaults into the other. The general OpenClaw edition uses
Sol 6.2 medium for defined daily work, high for sustained coordination, Astra
6.2 medium for difficult judgment, and Fable 5.2 medium/high for technical
analysis/execution. Its pricing and benchmark rationale is in the router's
`references/gpt62-20261117.md`. These are recommendations, not proof of a live
subscription route or permission to change an explicit native selection.
Do not revive retired schema-3 presets, mandatory coordinator topology or
resolver scripts.

For GPT-only pstack role-aware choices, the router's
`references/pstack-role-presets.json` is the only preset mapping. Change that
source only when the operator asks for a durable shared-policy change. Keep a
selected role-aware preset separate from pstack's global budget options; do not
apply one global effort over its per-role recommendations. Equilibrado is the
default only for a new setup with no existing role choices.

1. Read the operator's requested changes and current native model/effort
   availability for each relevant channel. Preserve explicit selections.
2. Change only the requested profile choices or task boundaries. Keep task
   ownership, permissions, proof and compute selection separate.
3. For this operator, use the selected edition's palette when the exact native
   channel supports it. Luna Max is available when justified, not an Ultra mode
   or a new paid route. Terra capability and effort/cost/latency evidence is in
   the router's `references/gpt61-terra-20261028.md`; the OpenClaw Sol/Astra 6.2 and Fable comparison is in
   `references/gpt62-20261117.md`. Older launch notes are historical evidence.
   API token prices do not prove lower subscription consumption or cost per
   completed outcome.
4. Author changes in the normal TheAngrySkills source repository when requested
   as a durable shared policy. Do not create a competing Workbench install.
5. Validate identifiers and effort support against the current channel; check
   that the policy has no mandatory ladder, task creation or selected-main
   override, and adds no speculative cache retention, keepalive prompts or
   polling loops. Report unavailable options rather than inventing support.
6. Install published changes with `npx skills` from the normal source and verify
   canonical paths and lockfile provenance for each authorised host/profile.

Return the chosen profiles, actual source/version, validation evidence and
remaining gaps. Do not add topology machinery or modify native permissions.
