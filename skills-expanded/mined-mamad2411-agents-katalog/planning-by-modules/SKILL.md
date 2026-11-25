---
name: planning-by-modules
description: Convert a SPEC, PRD, or feature request into a module-level implementation plan that names affected modules, designs their public interfaces, lists internal changes, identifies dependencies and risks, and specifies tests at each boundary. Save to PLAN.md. Use before any implementation that touches more than two modules. Works from a SPEC.md when one exists; otherwise plans directly from the user's stated request. Skip for single-file changes.
---

# Planning by Modules

Plan by module boundary, not by file. AI implementation goes wrong when it generates code one file at a time without a coherent picture of which modules own what behavior, what their public interfaces look like, and where the seams are. This skill produces that picture.

A good plan answers: which modules change, what their public interfaces look like after the change, what's internal versus exposed, and what tests live at each boundary. A bad plan is a step-by-step task list with no interface design.

## Process

1. **Read the input.** Look for `SPEC.md`, `docs/specs/<slug>.md`, or any similar specification document. If present, treat it as the canonical input. If absent, work from the user's stated request — but if the request is too vague to plan from (you'd be guessing at acceptance criteria, scope, or constraints), pause and ask the user clarifying questions before continuing. Running `clarifying-intent` first to produce a SPEC is one good option; a short inline Q&A is another.
2. **Anchor module names and existing patterns.** If `CONTEXT.md` (or similar architecture doc) exists, read it. If absent and the codebase is unfamiliar, briefly survey the relevant modules — entry points, the affected files, and adjacent tests — before planning. (If you find yourself doing extensive discovery, `mapping-codebase` is the dedicated skill for producing a reusable map.)
3. **Identify affected modules.** Group changes by module, not file. A module is a unit with a public interface and shared internal state — directories like `src/billing/` typically map to modules; loose utilities don't.
4. **For each affected module, design the interface change before the implementation.** What does the module expose after the change? What stays internal? An interface is the smallest possible surface that lets callers do what they need.
5. **Apply Ousterhout's red flags** (see Rules below). Stop and revise if you see them.
6. **Identify dependencies and ordering.** Which modules must change first because others depend on them? Where can work parallelize?
7. **Specify tests at each boundary.** What tests at the public interface prove the change works? Tests against internals are smells.
8. **Identify risks.** What could break? What existing behavior is at risk? What's the rollback?
9. **Write `PLAN.md`** at the project root using the format below.
10. **Confirm with user.** Ask: "Anything wrong, missing, or risky I haven't flagged?" Then recommend a fresh session for implementation.

## Rules

- **Design the interface first.** Do not list "implement X" as a step until X's public interface is on the page. The interface is the contract; everything else is fill.
- **Prefer deep modules.** A deep module hides a lot of complexity behind a simple interface. If the proposed interface has more methods than the module has real responsibilities, the module is shallow — redesign.
- **Watch for shallow modules.** Red flag: an interface where the method names mirror the implementation's internal steps (`parseInput`, `validateInput`, `transformInput`, `writeOutput`). That's a pass-through, not an abstraction.
- **Watch for information leakage.** Red flag: two modules both need to know the same fact (a file format, a magic constant, a data shape). Fold the shared knowledge into one module or extract it into a third.
- **Watch for pass-through methods.** Red flag: a method that does nothing but call another method with the same signature. That module is adding interface cost without functionality.
- **Watch for temporal decomposition.** Red flag: modules organized by *when* operations happen (`Step1`, `Step2`, `Step3`) rather than *what knowledge they own*. Reorganize by knowledge.
- **Pull complexity downwards.** If a choice can be made inside a module, make it there — don't push it to callers via configuration parameters they all have to set the same way.
- **Plan tests at module boundaries, not internals.** Tests that exercise the public interface survive refactors; tests that mock private methods break with every change.
- **If the interface design is non-trivial, consider `designing-it-twice` first.** Generating two or three radically different interface options before committing to one tends to pay off when the right shape isn't obvious.
- **Don't write code in this skill.** It produces a plan, not an implementation.

## Output Format

Write `PLAN.md` at the project root with this structure:

```
# PLAN: <one-line title>

**Source:** <SPEC.md path if one exists, otherwise short description of the user's request>
**Date:** YYYY-MM-DD
**Status:** Draft | Confirmed

## Summary

One paragraph. What's the change, which modules are affected at a high level, and what's the dominant risk?

## Affected modules

| Module | Path | Change type | New responsibility | Risk |
|---|---|---|---|---|
| Billing | `src/billing/` | Modified | Adds proration for mid-cycle plan changes | Medium — touches invoice generation |
| Domain | `src/domain/` | Modified | New `PlanChange` entity | Low |
| API | `src/app/api/billing/` | Modified | New `POST /plan-changes` endpoint | Low |
| (none) | — | New | — | — |

## Module: Billing (`src/billing/`)

### Current public interface

```typescript
generateInvoice(customerId: string, period: Period): Invoice
prorate(amount: Money, fraction: number): Money
```

### Proposed public interface

```typescript
generateInvoice(customerId: string, period: Period): Invoice
applyPlanChange(customerId: string, change: PlanChange): Invoice  // new
prorate(amount: Money, fraction: number): Money  // unchanged
```

### What stays internal

- The proration calculation strategy (linear, daily, custom) — selected inside the module based on plan settings, not exposed as a parameter.
- The order in which credits and charges are applied to the invoice.

### Tests at this boundary

- `applyPlanChange` produces an Invoice with the correct prorated line items for upgrades, downgrades, and same-tier plan changes.
- A `PlanChange` mid-period generates the credit and charge with the correct dates.
- Existing `generateInvoice` tests continue to pass without modification.

### Risks

- The current proration logic is used by ~5 grandfathered customers via `legacy_invoice.ts`. Verify their flow is unaffected before merging.

---

(Repeat the Module section for each affected module.)

## Dependencies and ordering

```
Domain (new entity) → Billing (consumes entity) → API (exposes endpoint)
```

What must change first: Domain. What can parallelize: API tests can be written while Billing is being implemented.

## Out of scope

- UI changes for displaying plan-change history (separate ticket).
- Migration of existing legacy invoice flow (see `legacy_invoice.ts` landmine in CONTEXT.md).

## Open questions

Things to resolve during implementation. Omit if none.

- Q: Should `PlanChange` records be immutable, or do we allow editing within a grace window?

## Rollback plan

If this change fails in production:

- The new endpoint is feature-flagged; disable the flag.
- The new entity has no destructive migration; rolling back the code is sufficient.
```

## Example interface red flag

> **Bad (shallow):**
> ```typescript
> billing.parseInput(raw)
> billing.validateInput(parsed)
> billing.calculateLineItems(validated)
> billing.applyTaxes(items)
> billing.formatOutput(taxed)
> ```
> Five methods, each doing one mechanical step. Callers must call all five in order. The module is a thin wrapper over the implementation steps.
>
> **Better (deep):**
> ```typescript
> billing.generateInvoice(customerId, period): Invoice
> ```
> One method, hides all the parsing/validation/calculation/tax/formatting internally. Callers don't know or care about the steps. The module owns the knowledge.

## Post-output instruction

After saving the plan, state:

> Plan saved at `<path>`. Start a fresh Claude Code session and ask it to implement the plan one module at a time using `tdd-with-feedback-loops`. The clean context will produce better implementation than continuing this thread.
