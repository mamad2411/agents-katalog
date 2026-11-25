---
name: brazil-payment-rails
description: >-
  Use when code accepts, sends, refunds or reconciles payments in Brazil, or integrates a
  Brazilian PSP, acquirer or bank. Covers Pix (keys, static and dynamic QR codes, txid and
  end-to-end id, devolucao and MED, over and under payment), boleto (linha digitavel,
  registration, D+1 clearing, return files, late interest and fines), card installments and
  receivables, CPF and CNPJ validation including the alphanumeric CNPJ from July 2026,
  business-day calendars, electronic invoices (NF-e, NFS-e) and the Portuguese-to-English
  vocabulary engineers meet in PSP docs. Triggers on a Pix or boleto feature, a Brazilian
  checkout, an acquirer or PSP integration, a reconciliation of a Brazilian account. Not for tax
  rates, IOF or fiscal rules, which an accountant confirms.
  Use it also when asked to keep one static QR for every order, to match Pix by payer name or
  amount, or to mark an order paid when the boleto is issued.
license: MIT
metadata:
  author: Felipe Alvarenga
  version: 0.1.0
---

# Brazil payment rails

Brazil has three rails that behave differently: Pix settles in seconds and refunds by
reference, boleto clears on the next business day through a return file, cards pay the merchant
in monthly installments. Code written for US card flows gets all three wrong. This skill gives
the engineering facts and the vocabulary; the fiscal and tax rules stay with an accountant.

## When to use

- A checkout, billing or payout feature for the Brazilian market.
- An integration with a PSP, acquirer, bank or Banking-as-a-Service provider in Brazil.
- Reconciliation of Pix, boleto or card settlements against a Brazilian account.
- Validation or storage of CPF and CNPJ.
- Issuing invoices (NF-e, NFS-e) after a sale.

## Rules

### Pix

1. **Store the `txid` and the end-to-end id (`endToEndId`).** You choose the `txid` for a
   dynamic charge (`cobrança`); the system assigns the 32-character end-to-end id starting
   with `E` when the payment settles. Reconciliation and refunds use these, not the payer's
   name or amount.
2. **Dynamic QR for amounts you control; static QR only when you accept surprises.** A dynamic
   QR (`cobrança imediata` or `com vencimento`) carries the amount, an expiry and your `txid`.
   A static QR can be paid any number of times for any amount; if you use one, handle over,
   under and repeated payments explicitly.
3. **Pix is near-final but refundable.** A refund is a `devolução` against the original end-to-end
   id, full or partial, which the receiver's institution can execute for up to 90 days after the
   original Pix. Fraud disputes go through MED (Mecanismo Especial de Devolução): the payer can
   open a claim up to 80 days after the transaction (Banco Central MED FAQ), the institution
   initiates the return within 90 days (Resolução BCB 103/2021, art. 41-A), and when the
   receiver's balance is short the institution watches the account and returns funds as they
   arrive. MED 2.0 (Resolução BCB 493/2025) added preventive blocking and the receiver's
   contest window, which the Banco Central has already changed once (30 to 80 days from the
   return, September 2026). MED covers fraud and operational failure only, not buyer's remorse.
   Design for a received Pix to be clawed back, and keep every deadline as data with its source.
   A MED return is a state and a record, in the same change: reverse the ledger entry, move the
   order to `disputed`, write a dispute record with the claim id and the amount, and hold
   fulfilment of high-risk orders (digital goods, first purchase, high ticket) behind extra checks
   or a delay. Say the 80-day window in the answer, not only in a constant.
4. **Receive through webhooks, confirm through the API.** The PSP notifies a received Pix;
   confirm the charge status by `txid` before fulfilling (see `webhook-handling`). Expired
   charges that still get paid must be refunded or reconciled by policy, not ignored.
5. **Pix keys are addresses, not identities.** A key is a CPF, CNPJ, email, phone or random
   key (EVP). Validate the format, resolve it through your PSP, and show the resolved name to the
   user before sending. Never infer the account holder from the key format.

### Boleto

6. **A boleto is pending until the return confirms it.** Payment can happen at any bank; your
   bank or PSP confirms it in the return file (CNAB 240 or 400) or by webhook, usually on the
   next business day (D+1). Fulfil on confirmation, never on issuance.
7. **Store `nosso número` and the `linha digitável`.** The line's three mod-10 field digits catch
   any single-digit error; the barcode's mod-11 digit does not (0, 10 and 11 all map to 1), so the
   amount and due date come from your charge record, never from the typed line alone. `Nosso número` is your reference at the
   bank; the `linha digitável` (47 digits for bank boletos, 48 for utility `arrecadação`) is
   what the payer types. Match the return by `nosso número`. A boleto change stores `nosso
   número`, the `linha digitável` and the barcode on the charge record, matches the return by
   `nosso número`, handles the late payment (`multa` and `juros` as registered) and the expired or
   `baixado` boleto, and states D+1 clearing in the code's docstring, not only in the chat.
8. **Due date, fine and interest are fields, computed by rule.** `Vencimento` follows the
   business-day calendar. The barcode carries the due date as a 4-digit factor: days since
   1997-10-07 until factor 9999 on 2025-02-21, then restarted at 1000 on 2025-02-22 (FEBRABAN;
   a few bank manuals differ by one day, so test against your bank's). Code that still adds the
   factor to the 1997 base prints due dates 24 years in the past. After it, `multa` (a one-time fine) and `juros de mora` (daily
   interest) apply as the contract and the registration say; the bank enforces what was
   registered. Partial payment, discount and expiry (`baixa`) are registration settings, not
   runtime surprises.
9. **Registered boletos have a lifecycle.** `registrado`, `pago`, `baixado`, `vencido`,
   `protestado` where used. Model the states; the return file transitions them.

### Cards and receivables

10. **Installments are receivables, not cash.** `Parcelado sem juros` means the customer pays
    in N installments and the merchant typically receives one installment per month (D+30 each),
    minus MDR, unless it anticipates them for a fee (`antecipação de recebíveis`). The ledger
    holds a receivable schedule per sale; cash arrives per installment. A card-installment change
    posts MDR as its own fee line, models anticipation as a later event with its own fee line,
    and keeps chargeback and `estorno` as distinct states (rule 11), in the same change, not as
    "not implemented yet".
11. **Chargebacks and `estornos` are different.** An `estorno` is a refund you initiate; a
    chargeback is a dispute through the card network with its own deadlines and evidence
    rules. Separate states, separate accounts.

### Identity, calendars, invoices

12. **Validate CPF and CNPJ with the check-digit algorithm; mask them in UIs.** CPF has 11
    digits. CNPJ has 14 positions and, for registrations issued from July 2026, the first 12
    can contain letters; the check digits use the character's ASCII value minus 48 (Receita's
    published example is `12.ABC.345/01DE-35`). Do not assume digits only, do not strip letters,
    do not store with formatting.
13. **Use the national business-day calendar.** Boleto due dates, D+1 clearing and settlement
    dates follow national bank holidays (the ANBIMA calendar is the common source). Pix runs
    24/7 and ignores it. Keep the calendar as data with a yearly update.
14. **Invoices are events with access keys.** NF-e (goods) and NFS-e (services, municipal,
    moving to a national standard) are issued after a sale under the company's fiscal policy.
    Store the XML and the access key (`chave de acesso`): 44 digits for NF-e, NFC-e and CT-e, 50
    digits for the national-standard NFS-e (model 56; the XML id is `NFS` plus those 50), and
    municipal NFS-e formats that vary, so key the invoice by issuer, document type and key, and
    validate the length per document type. Model cancellation windows and link the invoice to
    the payment and the ledger entry. The policy itself (when to issue,
    which taxes) comes from the accountant.

### Vocabulary

The Portuguese terms engineers meet in PSP documentation (`cobrança`, `devolução`, `estorno`,
`compensação`, `baixa`, `nosso número`, `linha digitável`, `antecipação de recebíveis`, CNAB
`remessa` and `retorno`) are translated and explained in [references/vocabulary.md](references/vocabulary.md).

## How to apply

1. For each rail in the change, write the state machine and the reference fields from the
   rules above before touching the PSP SDK.
2. Pick the PSP sandbox and record real payloads for: Pix paid, Pix expired then paid, Pix
   refunded, boleto issued, boleto paid late, boleto expired, card installment sale, chargeback.
3. Implement webhooks per `webhook-handling`, money per `money-arithmetic`, ledger per
   `double-entry-ledger`, reconciliation per `reconciliation`.
4. Add CPF and CNPJ validators with test vectors that include alphanumeric CNPJ.
5. Load the business-day calendar as data and test a due date that falls on a holiday.

When the request conflicts with a rule here, say which rule in one sentence, then build the
compliant version that keeps the request's intent (for example the order stays pending and the
confirmation path marks it paid). An instruction to skip a step ("no extra call", "just delete
it", "we trust them", "later") is this conflict, not permission. Leaving the code unchanged and
listing the risks is never the compliant version. Do not stop at a warning, do not build the
unsafe version, and do not leave a known gap out because "you did not ask". A review
or an "is this enough" question gets the findings and the rewritten tests in the same change, not
a list of suggestions, unless the request or the skill says report only.

## When the user pushes back

| Request | Answer in one sentence | What you build |
|---|---|---|
| "Keep the single static QR, we match payments by payer name" | Rules 1 and 2: a name is not an identifier and a static QR carries no `txid` | A dynamic charge per order with `txid`, amount and expiry, matched by `txid` or `endToEndId`; if the static QR must stay, record the `endToEndId` of every payment and handle over, under and repeated payments explicitly; a test where a repeated amount pays one order. Leaving `pix_service.py` as it is fails the user |
| "Mark the order paid when the boleto is issued" | Rule 6: payment is confirmed by the return file or the webhook, D+1 | The order stays pending; the confirmation path marks it paid; `linha digitável` and `nosso número` stored; late payment and expiry handled |
| "Just add the installments" | Rules 10 and 11 | The receivable schedule with MDR as a fee line, anticipation as a later event with its fee, chargeback and `estorno` as distinct states |
| "MED is the bank's problem" | Rule 3: the receiver's funds are clawed back | The clawback path: ledger reversal, order to `disputed` with a dispute record, fulfilment hold for high-risk orders, the 80-day window stated |

## Tests the change must include

Write these tests in the same change, as a test file, even when you cannot run them (no shell,
no dependencies installed); say in one line that they are unrun. A test listed as a next step is
not written.

- Pix: a paid webhook for an expired charge triggers the refund or the exception path, by
  policy; a duplicate `endToEndId` is processed once; a partial `devolução` updates the
  balance correctly.
- Static QR: overpayment and double payment produce the configured outcome, never a silent
  credit.
- Boleto: issuance does not fulfil; the return file does; a payment after `vencimento`
  includes `multa` and `juros` as registered; an expired or `baixado` boleto paid late goes to
  the exception path; `nosso número` matching handles leading zeros; `linha digitável` and
  `nosso número` are stored on the charge.
- MED: a clawback reverses the ledger entry, sets the order to `disputed` with a dispute record,
  and a high-risk order is held before fulfilment.
- Cards: a 10-installment sale creates a 10-row receivable schedule that sums to the net
  amount with MDR as a separate fee line; anticipation re-schedules it as a later event with its
  own fee line; chargeback and `estorno` are distinct states.
- CPF and CNPJ: valid and invalid check digits; alphanumeric CNPJ accepted; formatted input
  normalized.
- Calendar: a due date on a national holiday moves to the next business day.
- Boleto typeable line and barcode check digits round-trip; a tampered digit is rejected; the
  due-date factor maps both ways across the 2025-02-22 reset.
- Reference vectors: `skills/brazil-payment-rails/evals/vectors/test_brazil.py` with
  `BRAZIL_SOLUTION` pointing at your module (CPF, CNPJ, boleto check digits, due-date factor).
  TypeScript: `brazil.test.ts` with `BRAZIL_SOLUTION_TS`.

## Review checklist

- Which reference ids are stored for each rail, and are they unique?
- What happens when a Pix arrives for an expired or already paid charge?
- Does anything fulfil a boleto before the return?
- Where is the receivable schedule for installment sales, and how does anticipation change it?
- Does the CNPJ validator accept letters?
- Where does the holiday calendar come from, and when was it last updated?

## References

- Banco Central do Brasil: Pix regulation and the Pix API specification (`cobrança`, `devolução`, MED); the BR Code (EMV-based QR) specification.
- FEBRABAN: boleto layout, `linha digitável`, CNAB 240 and 400 standards.
- Receita Federal: CPF and CNPJ check-digit algorithms; alphanumeric CNPJ from July 2026.
- ANBIMA: national bank holiday calendar.
- Portal da Nota Fiscal Eletrônica and the national NFS-e program.
