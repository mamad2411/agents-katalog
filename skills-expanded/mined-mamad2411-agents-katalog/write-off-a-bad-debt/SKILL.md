---
name: write-off-a-bad-debt
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 15min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Write off an uncollectible customer balance so accounts receivable and reports no longer show it as expected cash.

## Preconditions

- The invoice is unpaid and collection attempts are documented.
- You have authority to write off the balance.
- You know whether the business uses cash or accrual accounting and which bad-debt account to use.

## Steps

1. **Open the unpaid invoice.** Locate the customer invoice and confirm the open balance. → *Expect:* the receivable amount is visible.
2. **Review collection history.** Check reminders, disputes, payment plans, returned mail, bankruptcy notices, or collection notes. → *Expect:* the record supports treating the balance as uncollectible.
3. **Confirm approval.** Get owner, manager, or accountant approval for the write-off. → *Expect:* approval is documented in the customer or invoice notes.
4. **Create the write-off entry.** [BRANCH: credit memo | bad-debt expense | allowance] create a credit memo or journal entry using the approved bad-debt account. → *Expect:* the entry amount equals the balance being written off.
5. **Apply the entry to the invoice.** Apply the credit or write-off against the unpaid invoice. → *Expect:* the invoice open balance becomes zero.
6. **Save supporting notes.** Add the reason, approval, date, and whether collection may resume later. → *Expect:* a reviewer can understand why the receivable was removed.

## Decision points

- Customer may still pay → consider a payment plan instead of write-off.
- Invoice is disputed because work was not accepted → issue a credit or adjustment based on the dispute outcome.
- Cash-basis books show no income from the invoice → ask your accountant whether a bad-debt deduction applies.
- Sales tax was already remitted → check whether tax can be recovered with the write-off.

## Failure modes & recovery

- **F1 Written off without approval:** detect by missing approval note → recover by reversing or obtaining documented approval.
- **F2 Wrong account used:** detect by write-off appearing in the wrong report category → recover by editing the credit memo or journal account.
- **F3 Balance not cleared:** detect by invoice still showing amount due → recover by applying the credit or entry to the invoice.
- **F4 Customer later pays:** detect by receipt against a written-off invoice → recover by recording recovery of bad debt according to accountant guidance.

## Verification

The invoice has zero open balance, the write-off entry is linked to it, the approved reason is documented, and accounts receivable no longer includes the written-off amount.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks often uses a credit memo or journal entry; Xero uses credit notes or manual journals; generic tools may use adjustment or write-off actions.
- `us`: bad-debt tax treatment depends on accounting method and prior income recognition.

## Safety & privacy

Medium risk because write-offs affect revenue, tax, and customer records. Do not erase collection history, and avoid sharing customer debt details outside approved staff or advisors.
