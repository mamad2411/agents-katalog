---
name: "operating-cost-stinger"
description: "Estimate low/base/high monthly operating costs from supplied workload and dated rates, separating allowances, shared credits, fees, floors and labor. Use for infrastructure operating budgets."
license: AGPL-3.0-or-later
compatibility: Claude Code, Cursor, ChatGPT Codex, Claude Cowork. Python 3.9+ for the offline calculator.
metadata:
  hive-drone: operating-cost-wasp-drone
  pair-drone: operating-cost-wasp-drone
  domain: software economics
---

# Operating cost

## Purpose

Produce a reviewable low/base/high monthly cost worksheet from the user's supplied architecture, workloads and dated rates. Report provider cash, paid operator labor and separate unpaid time valuation. Read [README.md](README.md) for the guide map.

## When to use

- "How much will this app cost to run each month?"
- "Estimate operating costs at low, expected and high usage."
- "Check whether the estimate double-counts included usage, a plan floor or shared credits."
- "Show provider bills separately from the value of my operating time."

## Boundaries

Architecture/provider choice belongs to platform owners. Commercial price-setting belongs to its owner. This component supplies arithmetic and evidence, not deployment, billing changes or tax/accounting assurance. Linear monthly meters only: disclose tiering, proration, per-line rounding, tax, FX, contracts and invoice timing as extensions or exclusions.

## Procedure

1. Read [intake](guides/01-intake.md) and gather missing workload, unit, region, plan and dated evidence in one compact question. Unknown costs remain gaps, never invented zeros.
2. Read [the model](references/model.md) and verify fee/credit ordering against the actual provider agreement. Classify allowances, monetary credit scopes, additive fees and minimum usage floors separately.
3. Fill [complete low/base/high input](references/templates/input.json) and the [worksheet](references/templates/worksheet.md), replacing every fictional value with supplied assumptions or evidence.
4. Follow [calculation and reporting](guides/02-calculate-and-report.md), run the bounded [offline calculator](scripts/README.md), and reconcile every shared credit budget and eligible charge.
5. Deliver inputs/output, provider cash, paid labor, unpaid time valuation, sensitivity, evidence gaps and one recommendation. Do not change provider settings or make live rate claims from the fictional example.

## Source and installed routing

Source work resolves this owner's `source_root` through `plugin-catalog.json`. Installed work uses trusted Core's `hooks/resolve-component.py operating-cost-stinger --kind skill` against the explicit selected-plugin registry. Resolve each optional platform owner by name before loading its skill. A cache is not selection. Use Unit Economics for contribution/margin feasibility once operating costs are supplied; it evaluates a supplied commercial price.

## Evidence and reporting

Ground claims in [the distillation](references/research/distilled-operating-cost.md), source ledger and its raw archive. Rates in official pages are never defaults; capture current region/plan/contract evidence for each actual estimate. Write runtime reports under `library/requirements/reports/operating-cost/<date>-<topic>.md`, or an agreed local destination when Library is absent. Retain assumptions and computed JSON with the worksheet. Calculator construction requires parent Security then Quality review; runtime remains advisory.

<!-- Ship Gate removed: research-only runtime produces no implementation code or provider writes. The bundled calculator construction requires the parent Ship Gate. -->

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [unit-economics-stinger](../unit-economics-stinger/SKILL.md) - Supplied-price margin and break-even modeling; resolve this selected owner before installed dispatch.
  - Platform specialists and pest-controller-suit - Resolve catalog names through trusted Core's selected-plugin resolver before optional dispatch.
