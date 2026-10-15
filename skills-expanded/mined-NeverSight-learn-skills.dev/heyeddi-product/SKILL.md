---
name: heyeddi-product
description: "Product leadership: user stories, acceptance criteria, backlog, holistic reviews. Verifies the product works and is useful; delegates UX flow, design critique, visual contrast, and engineering audits; synthesizes plans and change recommendations. Use after @heyeddi-intake, before ship, or when the user asks for PM review, user stories, acceptance criteria, or \"is this feature good enough?\""
version: 1.0.0
---

# HeyEddi Product

**Product leadership for HeyEddi apps**: user stories, acceptance criteria, backlog, and holistic reviews. Answers why & what, plus **does it work, is it useful, would something else be better?**

You are the PM orchestrator. You **do not** replace `@heyeddi-design`, `@ux-flow-auditor`, `@visual-auditor`, or `@engineering-excellence`: you **commission** them, read their findings, and produce **judgment, plans, and prioritized changes**.

**All artifacts under `.heyeddi/docs/product/`**: never repo root.

## Cross-pillar sync (mandatory)

Read **`reference/cross-pillar-handoff.md`**. Use `@heyeddi-orchestrator`:

```
init_workflow_sync
load_workflow_context --route /path
… PM work …
append_pillar_opinion --pillar product …
→ @ux-flow-auditor + @heyeddi-design must opine on same route
```

## When to use

| Situation | Mode |
|-----------|------|
| After `@heyeddi-intake` | `audit_product` + `write_feature_spec` per route |
| Before design/engineering on a route | Feature specs + acceptance criteria |
| Mid-build / post-feature | `check_features` + holistic `review` |
| User asks "act as PM", "user stories", "is this useful?" | Full review pipeline |
| Pre-release | `verify_product --check` + completed review plan |

## Subagents (default)

See `reference/subagents.md`. **Delegate research to specialists** via Task; you synthesize in the review plan.

| Research question | Delegate |
|-------------------|----------|
| Can users finish the job? | `@ux-flow-auditor` `trace_flow` |
| Right UX for persona? | `@heyeddi-design` `critique` |
| Legible / contrast OK? | `@visual-auditor` `audit_contrast --check` |
| Code maintainable? | `@engineering-excellence` `audit_engineering` |
| UI sprawl? | `@no-duplicate-ui` |

## Mandatory pipeline: holistic review

Read **`reference/pm-review.md`** and **`reference/delegation.md`**.

```
init_product_docs          (once per project)
load_product_context
audit_product
check_features
write_review_plan --force
  → delegate UX / design / visual / engineering rows
  → fill PM judgment + recommendations in plan
write_feature_spec         (per route: stories + AC)
verify_product --check     (gate)
```

## Modes

| Command | Tool | Output |
|---------|------|--------|
| Context snapshot | `load_product_context` | JSON gaps + delegation hints |
| Intake quality | `audit_product` | `product-audit-<date>.md` |
| Spec vs code | `check_features` | `feature-status.json` + PM questions |
| Stories + AC | `write_feature_spec` | `features/<slug>.md` |
| Review scaffold | `write_review_plan` | `review-plan-<date>.md` |
| Gate | `verify_product --check` | exit 0/1 |

## PM judgment (you write: not scripts)

Scripts find **gaps**. You answer:

1. **Does it work?**: AC met? blockers from `check_features` and UX traces?
2. **Is it useful?**: persona `primary_job` satisfied vs competitors?
3. **Would something else be better?**: cut scope, merge routes, different IA: cite delegated evidence?

Update `backlog.md` when priorities change.

## Never

- Ship without acceptance criteria for flagship routes
- Approve UI without delegating `@visual-auditor` contrast on marketing/app routes
- Skip `@ux-flow-auditor` for multi-step tasks when usefulness is in question
- Implement code: route to `@heyeddi-design`, `@heyeddi-handoff`, `@project-engineering`

## Chain

- `@heyeddi-intake`: upstream author of `product.md`
- `@heyeddi-orchestrator`: discover skills; PM owns *product* routing judgment
- `@pre-merge-gate`: CI; PM review is advisory unless `verify_product` in workflow

## Artifacts

| Path | Purpose |
|------|---------|
| `.heyeddi/docs/product/backlog.md` | Prioritized features |
| `.heyeddi/docs/product/features/<slug>.md` | Stories + AC per route |
| `.heyeddi/docs/product/feature-status.json` | Spec vs code matrix |
| `.heyeddi/docs/product/review-plan-*.md` | Holistic review + synthesis |
| `.heyeddi/docs/product/product-audit-*.md` | Intake quality |
## When the task is complete: suggest next skills

When you have **finished the user's request** for this skill (not after every tool call or subagent phase), suggest what to run next:

1. Run:

   ```bash
   python .agents/skills/heyeddi-orchestrator/scripts/suggest_next_skill.py --current-skill heyeddi-product --project-root .
   ```

   Add `--route /path` if you worked a specific route.

2. Include the script's **`### Next step`** block in your **final** reply. The user copies the **Prompt** line into chat (e.g. `@heyeddi-design craft /settings`).

Pass `--mode shape` (or `craft`, `audit`, etc.) when you know which sub-command just finished.

See `@heyeddi-orchestrator` → `reference/next-skill-handoff.md`.

