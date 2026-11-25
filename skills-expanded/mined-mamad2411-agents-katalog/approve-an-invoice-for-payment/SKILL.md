---
name: approve-an-invoice-for-payment
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 10min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Approve a vendor invoice for payment after confirming the charge is authorized, accurate, and ready to be paid.

## Preconditions

- The vendor invoice or bill is in the accounting, procurement, or approval system.
- Purchase order, receipt, contract, or service approval is available if required.
- You have approval authority for the amount and vendor.

## Steps

1. **Open the invoice awaiting approval.** Find the vendor bill in pending, awaiting approval, or inbox status. → *Expect:* invoice details and attachments are visible.
2. **Verify vendor identity.** Confirm vendor name, remittance details, invoice number, and tax ID if used. → *Expect:* the invoice belongs to an approved vendor.
3. **Match support.** Compare invoice lines to purchase order, receipt, contract, timesheet, or service acceptance. → *Expect:* quantity, price, and work received match support.
4. **Check coding and due date.** Review expense category, project, department, tax, payment terms, and due date. → *Expect:* the bill will post to the correct accounts and payment cycle.
5. **Resolve exceptions.** Hold the invoice if there are price differences, duplicate invoice numbers, missing receipt, or suspicious bank changes. → *Expect:* only valid invoices continue to approval.
6. **Approve for payment.** ⚠️ *Irreversible:* approval may release payment in automated workflows, so confirm vendor, amount, and bank details before approving. → *Expect:* the invoice status changes to approved or ready to pay.
7. **Add approval note.** Record any exception resolution, partial approval, or payment instruction. → *Expect:* the audit trail shows why the invoice was approved.

## Decision points

- Invoice exceeds your authority → route to the proper approver.
- Vendor bank details changed → verify through a trusted channel before approval.
- Goods were not received → hold until receiving confirms delivery.
- Invoice is a duplicate → reject or mark duplicate instead of approving.

## Failure modes & recovery

- **F1 Duplicate invoice:** detect by same vendor invoice number, amount, and date → recover by rejecting the duplicate and notifying accounts payable.
- **F2 PO mismatch:** detect by price or quantity variance → recover by requesting credit, revised invoice, or approval for variance.
- **F3 Fraudulent bank change:** detect by new payment details or urgent request → recover by stopping approval and verifying with known vendor contact.
- **F4 Wrong accounting code:** detect by category or project mismatch → recover by editing coding before approval.

## Verification

The invoice status is approved or ready to pay, with matched support, correct coding, verified vendor details, and an approval note or audit trail.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks may use bills and approval apps; Xero has bill approval workflows in supported plans; generic tools may use AP approval queues.
- `us`: collect W-9 or vendor tax details where required before paying reportable vendors.

## Safety & privacy

Medium risk because approval can trigger cash outflow and fraud exposure. Verify bank changes independently and limit invoice attachments to authorized reviewers.
