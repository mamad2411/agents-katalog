# dev/skill-creator — skill payload

> Machine-readable contract: [`../skill-creator.manifest.json`](../skill-creator.manifest.json).

## What this skill does

Walks a maker through the Register-gate workflow: prompts for the skill's
intent and IOPE (inputs, outputs, preconditions, effects), drafts a
schema-valid manifest, suggests canonical capability tags by inspecting
the existing registry for near-matches, and emits a starter SKILL.md.

This is **the** on-ramp into the graduation chassis. It's the difference
between "ten makers writing ten subtly-different invoice schemas" and "ten
makers all landing on `invoice.extract`".

## When to use it

- A user is describing a new repeatable process and you suspect it
  belongs in the registry.
- You're about to write a manifest by hand — let the skill do the
  schema-validation loop for you.

## When **not** to use it

- The capability already exists — call `find_skill_by_capability` first.
- The thing being described is a one-off task, not a *repeatable* skill.

## Determinism and risk

Determinism: **medium** — manifest values are schema-validated but copy
varies. Risk: **low** — only produces draft files; PR/Certify gate
intercepts before anything reaches the published catalog.

## How it composes

Pure upstream: feeds the Register gate. Output is consumed by
`submit_skill_draft` on the registry server (out-of-band in the Cowork
context — see the limitations doc).
