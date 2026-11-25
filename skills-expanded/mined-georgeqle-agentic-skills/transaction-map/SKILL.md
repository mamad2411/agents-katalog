---
name: transaction-map
description: Plan purchase, checkout, payment, fulfillment, receipt, refund, dispute, and trust-state flows
type: analysis
version: v0.4
argument-hint: "[optional: app, transaction type, or payment scenario]"
interview_depth: full
visual_tier: visual
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `$pack install <pack>` inside Codex, or `npx skillpacks install <pack>` from the project shell, instead of the target skill.

# Transaction Map

Invoke as `$transaction-map`.

Map the operational transaction flow after a customer decides to buy or upgrade.

## Process

### 0. Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

When product path `{slug}` is active, read and write research under `research/{slug}/`, specs under `specs/{slug}/`, and treat top-level `research/*.md` files as flat-mode documents or cross-path summaries.

1. Resolve product-path scope using `research/{slug}/` when applicable.
2. Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Scope the transaction map to the active product path by default.
3. Require `research/journey-map.md`; recommend `$conversion-map` first when conversion decision logic is missing.
4. Load journey map, conversion map, monetization docs, specs, codebase payment routes/providers, support/refund policy docs, and customer feedback when present.
5. Interview and recommend around: checkout entry, plan/quantity selection, payment states, tax/invoice needs, account provisioning, fulfillment, receipts, failed payment recovery, refunds, cancellations, disputes, trust/safety messages, and support handoff.
6. Present transaction states and failure modes before writing.
7. Write `research/transaction-map.md` and `research/transaction-map-interview.md` in flat mode, or `research/{slug}/transaction-map.md` and `research/{slug}/transaction-map-interview.md` when product-path scope is active, after validation.

## Output Shape

```markdown
# Transaction Map

> Based on: research/journey-map.md[, research/conversion-map.md]
> Date: YYYY-MM-DD

## Summary
## Transaction Types
## Checkout And Payment Flow
## Provisioning And Fulfillment
## Receipts, Invoices, And Records
## Failure, Refund, And Dispute States
## Trust And Support Touchpoints
## Product Gaps
## Next Steps
```

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/transaction-map-{topic}.html`.

## Constraints

- Keep the map provider-agnostic unless the codebase or specs already choose a payment provider.
- Identify compliance, tax, or legal questions as gaps; do not invent policy.
- End with `## Next Steps`, preferring `$retention-map`, `$guide`, or `$lifecycle-metrics` as context dictates.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
