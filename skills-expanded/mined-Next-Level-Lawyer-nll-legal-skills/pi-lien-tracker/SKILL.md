---
name: pi-lien-tracker
description: Track medical liens, health insurance subrogation claims, and Medicare/Medicaid conditional payment amounts against a personal injury settlement, and show net proceeds after liens. Use whenever the user mentions medical liens, subrogation, ERISA plan reimbursement, Medicare/Medicaid liens, or wants to calculate net settlement proceeds to the client after liens and fees.
---

# PI Lien Tracker

Tracks every lienholder against a PI settlement and shows what the client actually nets, so nothing gets missed at disbursement.

## Workflow

1. **List every lien source** the user identifies: hospital/provider liens, health insurance subrogation (note if plan is ERISA — different reimbursement rules apply), Medicare conditional payments, Medicaid liens, workers' comp liens if applicable.
2. **Record for each**: lienholder, amount claimed, amount confirmed/finalized vs. still estimated, and status (asserted / negotiating / resolved).
3. **Flag reduction opportunities factually** (e.g., common fund doctrine, made-whole doctrine, statutory lien reduction caps) as things to raise with the lienholder — don't calculate a specific negotiated reduction yourself, that's attorney/lienholder negotiation.
4. **Calculate net proceeds** once settlement amount and attorney fee/costs are known: settlement − attorney fees − costs − total liens (using confirmed amounts; show estimated liens separately if not yet finalized) = net to client.
5. **Flag Medicare/Medicaid liens as highest priority** to resolve before disbursement — these carry federal reimbursement obligations and disbursing before resolution creates real risk.

## Output format

```
## Lien Summary — [Client name] | Settlement: $[amount]

| Lienholder | Type | Amount Claimed | Status | Notes |
|---|---|---|---|---|

**Total liens (confirmed):** $[sum]
**Total liens (estimated, unresolved):** $[sum]

### Net Proceeds Calculation
Settlement: $[amount]
– Attorney fees: $[amount]
– Costs: $[amount]
– Liens (confirmed): $[amount]
= **Net to client: $[amount]** (before resolving estimated liens: $[amount] still outstanding)

### Flags
- [Medicare/Medicaid liens unresolved — do not disburse until finalized]
- [Reduction arguments to raise: common fund / made whole / statutory cap, if applicable]
```

## Document Output Format

If this is being prepared as a settlement disbursement statement for the client's file (or the client's own records), use the `docx` skill:

- **Header:** firm name/logo placeholder, client name, case name, "Settlement Disbursement Summary" title, date.
- **Lien table and net proceeds calculation:** real Word tables, not markdown — the net proceeds section should read like a clean ledger (settlement amount, each deduction on its own line, bold total row at the bottom).
- **Unresolved-lien flags:** visually distinct (bordered/shaded callout), especially the Medicare/Medicaid do-not-disburse flag — this should be impossible to miss on the page.
- **Typography:** Calibri or Arial 11pt, 1" margins, page numbers.

## Notes

- Never disburse math should imply finality on Medicare/Medicaid amounts until the user confirms they're finalized — always show these as estimates until stated otherwise.
- Don't negotiate or assert a specific reduced lien amount — flag the applicable doctrine/argument and leave the number to attorney negotiation.
