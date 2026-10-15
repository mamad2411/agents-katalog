---
name: cr-coding-style-core
description: Core coding style for application and feature work. Use when implementing features, refactoring app code, naming files/functions, or deciding whether to extract helpers/components.
---

# Coding Style Core

Use these defaults unless the user or project conventions say otherwise.

## Principles

- Prefer existing project patterns over introducing new ones.
- Prefer straightforward, readable code over cleverness.
- Keep feature code boring and easy to scan.
- Keep code easy to scan top-to-bottom.
- Optimize for local clarity first.
- Use descriptive, literal names for files, functions, variables, and components.
- Use explicit names and unsurprising APIs.
- Keep folder structure shallow and obvious.
- Keep code close to the feature unless it is clearly shared.

## Structure

- Put feature-specific code near the route or feature that owns it.
- Promote code to shared locations only when it is genuinely reusable.
- Prefer clear top-level buckets such as `components`, `helpers`, `server`, `lib`, or route-local files.
- Do not create extra files or layers unless separation improves comprehension.

## Abstraction Rules

- Avoid speculative abstractions.
- Do not introduce helpers, hooks, wrappers, or config layers just because code looks slightly repetitive.
- When duplication is real, refactor early if the resulting abstraction makes the code easier to skim.
- Prefer partial abstraction over forcing unrelated cases through one generic helper.
- If the abstraction makes the code harder to scan, keep the logic local even if that means some duplication.
- Extract only when one of these is true:
  - the logic is reused,
  - the concept is clearly distinct,
  - the main flow becomes easier to understand.
- Prefer a little duplication over indirection that hurts readability.
- Do not hide simple business logic behind generic utilities.

## Helper and Component Style

- Helpers should be small and single-purpose.
- Prefer inline logic over a tiny helper when the helper does not improve readability.
- Components should have clear responsibilities.
- Prefer sensible defaults and explicit props.
- Avoid giant catch-all utility files unless the functions are truly generic.
- Keep simple component logic local; extract only when complexity or reuse justifies it.
- Do not create custom hooks only as a cosmetic reorganization. Keep local component state in place unless the logic is truly reusable or the component has become large and logic-heavy.
- For large or complicated React logic, extracting a hook or using context is good when it meaningfully simplifies the component.

## Refactoring Boundaries

- Default to touching the requested area and closely adjacent code only.
- Clean nearby code when it materially improves readability or correctness.
- Do not perform broad renames, architecture changes, or cross-project cleanup unless asked.
- Preserve existing public APIs unless there is a clear reason to change them.

## Examples

### Prefer direct feature code

```ts
export const InvoiceRow = ({ invoice }: { invoice: Invoice }) => {
  const isPaid = invoice.receipts.length > 0;

  return <span>{isPaid ? 'Paid' : 'Pending'}</span>;
};
```

### Avoid unnecessary helper extraction

```ts
const getInvoicePaymentStatus = (invoice: Invoice) =>
  invoice.receipts.length > 0 ? 'Paid' : 'Pending';

export const InvoiceRow = ({ invoice }: { invoice: Invoice }) => {
  return <span>{getInvoicePaymentStatus(invoice)}</span>;
};
```

### Prefer meaningful abstraction when duplication is real

```ts
const hasExpiredState = (status: string, deletedAt: Date | null) =>
  status === 'inactive' || deletedAt != null;

const isExpiredUser = hasExpiredState(user.status, user.deletedAt);
const isExpiredAdmin = hasExpiredState(admin.status, admin.deletedAt);
```

### Avoid generic abstraction that hurts skimming

```ts
const isExpired = (entity: { status: string; deletedAt: Date | null }) =>
  entity.status === 'inactive' || entity.deletedAt != null;
```

Use this only if it really reads better in context.

## Output Checklist

Before finishing, check:

- Is the code easy to follow top-to-bottom?
- Are names literal and unsurprising?
- Did I avoid unnecessary abstractions while still refactoring meaningful duplication?
- Is feature code kept near its owner?
- Did I avoid creating extra files or layers without a strong reason?
