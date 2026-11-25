---
name: pci-dss-scoping
description: PCI DSS v4.0.1 scope determination and control assessment for the payment paths — Stripe, Moyasar, KuickPay, Authorize.net/Chase and Apple — including which SAQ applies and how to keep scope minimal. Use for any question about card data, payment pages, refunds, webhooks or PCI.
---

# PCI DSS scoping and assessment

Registry: `PCI-DSS`, plus `VENDOR-STRIPE`, `VENDOR-MOYASAR`, `VENDOR-APPLE-IAP`.

**v4.0.1 is the only active version.** All 51 previously future-dated requirements have been
mandatory since **31 March 2025** — there is no best-practice carve-out and no grace period left.
Anyone still describing requirements as "future-dated" is working from stale material.

## Scope first, controls second

PCI DSS applies to entities that **store, process or transmit cardholder data, or can affect the
security of the cardholder data environment**. That second clause is the one that catches people:
a page that merely *loads* a script onto a payment page is in scope even if no PAN touches your
server.

Determine, per gateway, and write it down:

1. Does a PAN, expiry, CVV or track data ever reach our process memory, logs, database, error
   tracker or backups?
2. Do we render card input fields ourselves, or does the gateway (hosted page, redirect, iframe, or
   gateway-hosted fields)?
3. Do we control any script that executes on a page where card data is entered?
4. Do we store a token, a last-4, or a card fingerprint — and is that treated as cardholder data?
5. Who is the merchant of record — us, or the hotel?

This codebase has five payment paths (`Services/Integrations/Payments/implementations/` plus the
Moyasar webhook route). **Answer these per gateway.** They will not all be the same, and the
weakest one sets your SAQ.

## SAQ selection

| Integration shape | Typical SAQ | Note |
|---|---|---|
| Full redirect to gateway-hosted page | SAQ A | Smallest scope |
| Gateway iframe / hosted fields on our page | SAQ A (with 6.4.3 and 11.6.1 still applying) | Script and change-detection controls apply |
| Our page posts card data through our server | SAQ A-EP or D | Large scope — avoid |
| Any storage of PAN | SAQ D | Do not do this |

The direction of travel is clear: **keep card data out of our systems entirely.** Every design
decision that moves a card field onto our page multiplies the assessment burden.

## Controls that apply even at minimal scope

| ID | Requirement | Surface |
|---|---|---|
| PCI-01 | Payment page script inventory, integrity and authorisation (Req 6.4.3) | frontend |
| PCI-02 | Change- and tamper-detection on the payment page (Req 11.6.1) | frontend, cicd |
| PCI-03 | No PAN/CVV in logs, error reports, analytics or support exports | backend, frontend |
| PCI-04 | Strong cryptography for transmission over public networks (Req 4) | backend |
| PCI-05 | Webhook authenticity — signature verification and replay protection on every gateway callback | backend |
| PCI-06 | Access control and MFA for administrative access to payment functions (Req 7, 8) | backend |
| PCI-07 | Logging of payment and refund actions with actor attribution, retained (Req 10) | backend |
| PCI-08 | Vulnerability management and secure development for in-scope components (Req 6, 11) | cicd |
| PCI-09 | Third-party service provider management — PCI status of each gateway tracked (Req 12.8) | organisational |
| PCI-10 | Refund and adjustment authorisation controls | backend |

## Hospitality-specific traps

- **Card on file for incidentals.** The moment a PMS stores a card for a no-show or damage charge,
  scope expands unless it is a gateway token. Verify what is actually stored.
- **Written card details.** Phone and email reservations where staff key a card into a form —
  including screenshots and email attachments landing in `Uploads/`.
- **POS and channel manager** interfaces that pass card data through the PMS.
- **Refunds and chargebacks** as privileged flows needing authorisation and audit.

## Grid guidance

PCI rows exist on all three surfaces with different content — script controls on frontend, data and
webhook handling on backend, vulnerability management and change control on CI/CD. Where the answer
is "no cardholder data reaches us", record `n/a` *with the evidence that established it*, because
that finding is the most valuable one in this section and it must be re-verified whenever a payment
integration changes.
