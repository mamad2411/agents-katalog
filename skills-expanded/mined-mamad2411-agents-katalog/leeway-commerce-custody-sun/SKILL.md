---
name: leeway-commerce-custody-sun
description: Evidence-bound financial/physical reconciliation evaluation for billing/AR and BOM/BOL/receiving/custody integrity.
license: MIT
---
# LeeWay Commerce & Custody Sun
Two primary rays: BILLING_REVENUE_CYCLE and ASSET_CUSTODY. Billing dimensions may include rated-vs-invoiced leakage, open-item reconciliation, unapplied cash, DSO deviation and dispute state. Asset dimensions may include BOM theoretical-vs-authorized actual consumption, PO-receipt-invoice match, lot/serial genealogy, custody events and count/mass variance.

For evidence-bound x_i,W_i,theta_i: r_i=sqrt(x_i^T W_i x_i); b_i=1 iff r_i<=theta_i; Omega=b1*2+b2, Omega_max=3, Phi=b1*b2.

Cash timing law: issued invoice balance need not equal cash received immediately; reconcile billed/credits/writeoffs/open AR/receipts/unapplied cash by accounting period and policy.
Three-way law: PO ↔ receiving/acceptance ↔ vendor invoice. BOL supports shipment/custody evidence but is not automatically accepted receipt.
Hard gates: ledger integrity, unauthorized write-off/credit, tax/legal-document requirement, broken lot/serial custody, material unapproved discrepancy and missing authority.
