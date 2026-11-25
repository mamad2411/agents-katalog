---
name: design-quality
description: Project-aware design execution and quality gates for Codex, with optional Impeccable detector or live-mode integration and explicit local fallbacks.
---

# Design Quality

Use this skill when interface work needs a shared product context, deterministic design checks, browser evidence, critique persistence, or a final quality gate.

This skill adapts selected ideas from `pbakaus/impeccable` at commit `8259c28209b92792005cec14dad573df39f68eaf`. Impeccable is Apache-2.0 licensed. Its detector, hooks, browser server, and live-mode source rewriting remain external runtime capabilities.

## Load

1. Read `references/project-context.md`.
2. Read one representative UI source file and the existing tokens, theme, or component system.
3. Read `references/quality-gates.md`.
4. Read `references/impeccable-runtime.md` when deterministic scanning or live variants would help.
5. Read `references/critique-contract.md` for a critique or audit.

## Workflow

1. Resolve the target to a stable file, route, component, or URL.
2. Identify the product goal, user, design register, platform, and established system.
3. Choose the smallest applicable action:
   - direction through `design-consultation`
   - variants through `design-shotgun`
   - implementation through `design-html`
   - critique or polish through `design-review`
4. Use the external Impeccable runtime when it is already installed and materially improves evidence or iteration.
5. Apply the local quality gates and preserve explicit evidence limits.
6. Route material accessibility, human-impact, or organizational questions to `accessibility-review`, `responsible-design-review`, or `design-leadership-review`.

## Outputs

Always include:

- target and design context used
- evidence path
- highest-priority findings or changes
- external runtime status
- verification completed
- remaining uncertainty

## Guardrails

- Preserve established product and brand systems unless the user authorizes a redesign.
- Treat anti-pattern rules as evidence-informed defaults. Product context and accessibility can justify a documented exception.
- Never install or update Impeccable implicitly.
- Never claim detector, hook, browser, or live-mode coverage unless that path actually ran.
- Keep private Marlowe context outside public design artifacts and GStack commits.
