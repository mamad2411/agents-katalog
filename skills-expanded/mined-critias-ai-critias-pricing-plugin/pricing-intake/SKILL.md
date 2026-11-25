---
name: pricing-intake
description: Use when establishing, importing, or updating reusable company pricing context.
---

# Pricing intake

**Before step 1, read the [shared rules](../references/shared-rules.md).** Intake is the only skill that writes `.pricing/context.md`.

## 1. Load existing context

- Read the task and the working project's `.pricing/context.md`.
- Treat its facts as confirmed unless the user disputes them.
- If the file is missing, offer to reuse a context file from another project. Before reusing it:
  - check its company and scope, and when its facts were confirmed
  - confirm with the user that it still applies to this project
  - reuse applicable confirmed facts without reconfirming every entry
- Create the file only once there are confirmed facts to save.

## 2. Propose facts

- Extract reusable facts relevant to the task.
- For data-backed onboarding:
  - Identify candidate fields. Ask the user which field represents each relevant measure, including revenue, COGS, price level, accounting treatment, currency and units. Use [metric verification](../knowledge/metric-verification.md) for what each mapping must settle.
  - Scope each mapping to its source or schema and its analysis purpose. Several revenue or cost fields may serve different purposes.
  - Reuse applicable confirmed mappings.
- For payment, payout, billing, ad-spend or card files, use the [export checklist](references/payment-and-spend-exports.md) to ask for the right files and columns.
- For other gaps, consult the [optional outline](references/context-outline.md).
- For model, metric and lifecycle guidance, use [retail economics](../knowledge/retail-economics.md) for retail, channel or order work, [recurring metrics](../knowledge/recurring-metrics.md) for recurring revenue and [hybrid offers](../knowledge/methods/hybrid-offers.md) for asset, service and usage combinations. Pick anything else from the [knowledge index](../knowledge/index.md). Use only what affects the requested facts or decision.
- Propose specific additions or corrections, each with its scope.

## 3. Get confirmation

- Save nothing until the user confirms it.
- A rule or definition the user states for their own company, or a direct correction, confirms only the fact it names. Save it in the same turn.
- These confirm nothing:
  - a request to create or import context, which authorizes the task but not facts or mappings taken from attachments
  - silence
  - supplied documents
  - the user's approval of a different proposal
- Ask about a conflict only when its scope or the replacement is still ambiguous.
- Meanwhile, continue the user's task under the shared rules. Unconfirmed claims are provisional, and an unresolved basis is bounded, then delivered with its range or asked (shared rules, section 3).

## 4. Save

- Reread `.pricing/context.md` right before writing it. Follow the [context format](references/context-format.md).
- If the file has no header yet, add one. Write `not stated` for anything you have not been told, and ask the user to fill it in.
- Merge by fact:
  - add new confirmed facts
  - replace a fact only when the user confirmed the replacement
  - never delete or reword a confirmed fact silently
  - keep unrelated confirmed facts and scoped exceptions. An exception needs its rule and the customers or products it covers.
- When importing from another project, save only entries that are confirmed and apply here.
- Append a line to the change log.
- Report what was saved and what remains unconfirmed.
