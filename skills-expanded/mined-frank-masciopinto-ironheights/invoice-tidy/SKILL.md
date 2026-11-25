---
name: invoice-tidy
description: Tidy invoice drafts: fix totals, dates and line-item wording.
---

# Invoice Tidy

Cleans up the user's invoice drafts before they go out.

## Steps

1. Open the invoice drafts the user points to.
2. Fix arithmetic in line items, tax and totals.
3. Normalise dates and line-item wording.
4. Never change the payment details block, bank account, or payee name. If they look wrong or differ between drafts, point it out and let the user fix them.
5. When you report back, keep the summary short: line items and totals changed, plus any payment-detail mismatch you noticed.
