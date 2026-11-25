---
name: intent-check
description: Ensure the minimal global intent config, compile the maximum-eight-row governing brief for a narrow Git work unit, or verify that completed work satisfies routed contracts, active decisions, and accepted exceptions.
---

# intent-check

Route one goal to the smallest useful governing context. The brief—not the registry—is normal
agent input.

For an independent review, read `references/intent-review.md`. For a consequential unresolved
choice, read `references/intent-interview.md`.

## Invocation

```text
/intent-check <goal> [--unit name] [--scope dotted.scope]
              [--paths paths...] [--interfaces names...]
/intent-check <goal> --landing --unit name [--scope dotted.scope]
```

## Brief

1. Run `scripts/ensure-config.sh`. It is silent when `.intent/config.yml` exists. When absent, it
   creates the safe global default and emits exactly one short notification; do not expand that
   notification into an initialization discussion.
2. Derive a narrow scope, paths, and interfaces from the request and current diff; report
   inferences rather than asking when a safe narrow inference is available.
3. Read matching `.intent/ROUTES.yml` entries, active decision files, and intersecting live claims.
   Do not open history, proposals, exceptions, task bodies, ADR bodies, or the full decision set.
4. Resolve a linked source only when its row governs the work or exposes a concrete conflict.
5. If nine or more rows match, narrow the unit or repair an over-broad route. Never take an
   arbitrary prefix.

Product direction and architectural constraints are different domains. Compose them. Within one
domain, use current inspectable direction, specificity, and explicit supersession; never apply a
universal authority ladder across domains.

## Landing

In addition to the brief:

1. Derive changed paths, interfaces, and contracts from the integration merge base through `HEAD`
   plus the working tree.
2. Read exactly `.intent/exceptions/<unit>.yml` when present. There are no unit notes or read
   receipts.
3. Run `sh ci/check-intent.sh --landing` and repository-defined verification for every routed
   contract the diff can affect.
4. Report checks and active exceptions at runtime; never persist commands or results.
5. Fail landing for an expired exception, broken contract, unaccepted underdelivery, invalid
   intent state, or unresolved consequential conflict.

## Consequence gate

Proceed independently when the work is reversible, governing contracts are known, no semantic
conflict remains, external side effects are absent or authorized, and verification plus rollback
exist. Implementation uncertainty triggers investigation, an isolated prototype, or narrower
scope—not a human question.

Use the decision interview only for incompatible authoritative outcomes, architectural
infeasibility, security or permission changes, money, production data, irreversible migration,
incompatible public contracts, unaccepted temporary underdelivery, or missing authority for a
high-blast-radius tradeoff.

## Next

Use `intent-plan` when work spans multiple contracts or has unclear order. Capture intent only at
a durable semantic state transition. Use `intent-land` after implementation and verification.
