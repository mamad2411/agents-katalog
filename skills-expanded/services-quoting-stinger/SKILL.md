---
name: "services-quoting-stinger"
description: "Prepare service quotes and agency SOW drafts from supplied scope/costs. Use for project pricing, acceptance criteria, maintenance, unknown integrations or scope changes."
license: AGPL-3.0-or-later
compatibility: Claude Code, Cursor, ChatGPT Codex, Claude Cowork. Python 3.9+ for optional offline calculation.
metadata:
  hive-drone: services-quoting-wasp-drone
  pair-drone: services-quoting-wasp-drone
  domain: software economics
---

# Services quotations

Prepare a reviewable proposed quote with acceptance scope, effort/cost evidence, uncertainty, pricing maths and separate maintenance coverage. Runtime is research/preparation (source-repository research, not shipped with the plugin); it does not send, accept or implement a contract.

## When to use

- How much should I quote for this website, app or integration?
- What is included, how many revisions, and how do I price maintenance?
- How does markup differ from margin or contingency?
- An unknown integration or new scope changed the original quote.
- Prepare an agency statement of work from deliverables, quote evidence and client dependencies.

## Procedure

1. Read [scope and quote](guides/01-scope-and-quote.md), [research distillation](references/research/distillation.md) and [model](references/model.md). Ask one compact batch for missing inputs, preserving uncertainty.
2. Resolve Estimation and its paired Stinger through selected-owner routing for effort and delivery scenarios. Do not invent rates, AI speed factors, certainty or acceptance.
3. Complete [scope worksheet](references/templates/scope.md). Unbounded integration discovery blocks a full fixed quote; prepare a bounded discovery proposal instead.
4. Use the [quote worksheet](references/templates/quote.md) and [optional calculator](scripts/README.md) to distinguish owner cost, cash, reserve, markup/margin and pass-through. Show proposed project/month units separately and retain price evidence.
5. Read [maintenance and change](guides/02-maintenance-and-change.md) for coverage caps, incident handling and separately proposed scope deltas. Preserve the accepted baseline.
6. For a statement of work, use [the SOW guide](guides/03-statement-of-work.md), [worksheet](references/templates/statement-of-work.md) and [fictional proposal](examples/statement-of-work.md); reuse the dated scope/quote/maintenance/change records. Keep test evidence, commercial acceptance, executed agreements and Accepted interface CTRs distinct; legal terms and rights stay with selected Legal Docs/counsel.
7. Check [worked examples](examples/quotes.md), run calculator tests when used, and deliver one proposed recommendation, evidence, exclusions and unresolved owner/legal decisions.

## Selected-owner routing

Load `pest-controller-suit` before dispatch. Source work uses `plugin-catalog.json` and its `source_root`; installed work uses trusted Core's `hooks/resolve-component.py` with the explicit selected-plugin registry. Resolve `estimation-stinger` for effort/date assumptions and `unit-economics-stinger` for business break-even. Resolve legal-documentation specialists for jurisdiction, warranty, IP, tax and enforceability decisions. Cached siblings do not prove availability; report missing owners and stop dependent conclusions.

## Boundaries and reporting

No market-hourly-rate guesses, public price changes, purchases, signatures, customer messages, charges, live configuration or application implementation. Output a local advisory worksheet in the owner's agreed destination, or `library/requirements/reports/services-quoting/` when Library exists. State proposal/acceptance status, costs counted once, period/currency, assumptions, evidence dates, checks and unanswered questions. Source code changes to this component require the parent construction gates.

## References

- [README](README.md): guide map.
- [Executable sample input](references/example-input.json): supplied hypothetical website quote for the offline calculator.
- Research archive, FAR context, source hashes: grounding and limitations.
- [Paired Drone](../../agents/services-quoting-wasp-drone.md): owning specialist.

<!-- Ship Gate removed: research-only runtime, produces no application implementation or provider writes. Component construction still requires parent Security then Quality and repository health before authorized commit/push. -->

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [paired specialist](../../agents/services-quoting-wasp-drone.md) - Owns this quotation domain and resolves related Estimation, Unit Economics and legal skills through selected-owner routing.
