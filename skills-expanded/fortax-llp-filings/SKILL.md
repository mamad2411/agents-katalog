---
name: fortax-llp-filings
description: LLP work on MCA end to end — RUN-LLP and FiLLiP incorporation, drafting the LLP agreement and filing Form 3, Form 4 partner and designated-partner changes, DPIN KYC, and the annual Form 11 and Form 8 with the audit-threshold check — prepared up to the DSC and payment. Typical asks: "LLP banana hai", "LLP agreement draft karo", "partner add/remove karna hai", "Form 8 Form 11 pending hai".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# LLP filings

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## Do the work, then stop at the DSC

Every LLP form is signed with a designated partner's DSC, most are certified by a professional, and
all carry a fee. Those clicks are the CA's or the partner's. **Refusing the job because of them is a
failure.** Yours is the rest: intake, name search, agreement drafting, the figures, every field of the
form. Say where you will stop, then start.

**Looking rules up.** Due dates, filing periods, audit thresholds, stamp duty and additional fees are
never stated from memory. Run `python3 scripts/fortax.py kb "LLP Form 8 due date" --topics mca` and
quote its source and captured date; where the reply is `weak` or `none`, read the LLP Act, 2008, the
LLP Rules, 2009, the state stamp Act or the MCA portal and mark it "confirm on the portal". Record each
in **Rules used**.

## What is different about an LLP

Say this before planning any LLP work; it changes what is due and what is not.

| Company | LLP |
|---|---|
| Directors, with DINs | Designated partners, with DPINs — same number series, same KYC form |
| MoA and AoA, filed at incorporation | LLP agreement, filed separately after incorporation in Form 3 |
| AOC-4 with financial statements, and MGT-7 annual return | Form 8 (statement of account and solvency) and Form 11 (annual return) |
| Annual general meeting drives both due dates | No AGM; the due dates run from the financial year end |
| Board and general meetings, with statutory minutes | Only what the LLP agreement itself requires |
| Audit by threshold under the Companies Act | Audit by turnover or contribution thresholds under the LLP Act — look them up, never state them |
| Charges registered in CHG-1 | LLP charge registration follows its own route — confirm it on the portal |

An LLP with no activity still files Form 8 and Form 11. "There was no business" is the commonest
reason an LLP arrives with years of default and an additional fee behind it.

## Incorporation — FiLLiP

FiLLiP is the integrated form: name reservation, DPIN allotment for the proposed designated partners,
and incorporation. The name can also be reserved separately in **RUN-LLP** first. Name discipline is
the same as for a company (`fortax-mca-incorporation`): search the MCA company and LLP name database
for identical and resembling names, and the trademark register for the proposed word in the classes
matching the business. Never promise a name — the Registrar decides. Give the CA two or more options
with the evidence, say which are riskier, then prepare:

- Each partner's PAN, identity and address proof in the portal's accepted forms; passport with
  apostille or consularisation for a foreign national or body corporate partner.
- Registered office proof: ownership document or rent/lease deed, owner's NOC, and a recent utility
  bill. A rented office with no NOC stops the filing — flag it at intake.
- Subscribers' sheet, consents to act, business activities, contributions, professional's certificate.

DPIN is allotted through FiLLiP up to a capped number per application, confirmed on the portal and not
from memory; anyone already holding a DIN or DPIN uses it. On approval the certificate issues with
the LLPIN, and PAN and TAN follow.

## The LLP agreement and Form 3

This is where LLPs most often fall into default. The agreement is executed on stamp paper of the value
the state prescribes for the contribution — **stamp duty is a state subject and varies with
contribution: look it up for that state, never state a figure** — then filed in **Form 3** within the
period allowed after incorporation, which you look up too.

The drafting is yours. Cover at least: each partner's contribution and the form it takes, profit
sharing ratio, rights and duties, who is a designated partner and their powers, admission and
retirement, how accounts are kept and audited, dispute resolution, dissolution. Any later change is
filed in Form 3 again with the supplementary deed attached. Partner changes and agreement changes
usually come together — Form 4 and Form 3 go as a pair; one without the other leaves the record wrong.

## Partners — Form 4

Form 4 covers appointment, cessation, and any change in the name, address or designation of a partner
or designated partner. Prepare: the incoming partner's consent, the outgoing partner's resignation
letter, the supplementary agreement recording the change, the partners' resolution where the
agreement requires one, and a body corporate partner's nominee details.

An LLP must keep the minimum number of designated partners the LLP Act requires, with one of them
resident in India; a cessation that breaks either condition is a stop-and-escalate. Every designated
partner needs a DPIN, and DIR-3 KYC applies to a DPIN exactly as to a DIN — a deactivated DPIN blocks
every LLP filing that partner must sign (see `fortax-mca-director-changes`).

## Annual filings — Form 11 and Form 8

| Form | What it carries | Signed and certified by |
|---|---|---|
| Form 11 | Annual return: partner details, contribution, and the other entities the partners are in | Designated partners, certified by a professional in the cases the rules specify |
| Form 8 | Statement of account and solvency, with assets and liabilities and income and expenditure | Designated partners, with the auditor's or a professional's certificate |

Both have their own due dates running from the financial year end, and late filing carries an
additional fee. State no date and no amount from memory: look each up for that financial year and
record it in **Rules used**. Whether a statutory audit is required turns on turnover and contribution
thresholds under the LLP Act — look those up too, and where the figures sit close to a threshold show
the working, not the conclusion. Form 8 also carries the partners' declaration of solvency and
contingent liabilities: take the figures from the finalised accounts, cite file and line for each, and
recompute totals from the rows in a spreadsheet or script, not in your head.

## Filing on the portal, and what you hand over

Open the MCA V3 portal in your browser tool (Claude in Chrome, a Playwright or browser MCP, or the
Codex browser); if you have none, give the CA the click path. The CA signs in. Re-read the page before
each click. LLP forms have moved to the MCA V3 portal and are filed as web forms from a logged-in
account, not as downloaded eForms; if a form is not where you expect on the V3 menu, look for it
rather than giving the CA a path that may no longer exist. Save the draft, run check-form, fix what it
reports.

In the client's ROC folder, dated: the intake sheet with LLPIN and SRNs, the drafted agreement or deed,
the completed form with each field's source noted, the attachment list marked found or missing, and
**Rules used** with every date, threshold and fee looked up. Never rename or delete a raw file.

**Check before filing**: LLPIN and every DPIN against MCA master data, DPIN KYC current and DSC
registered and unexpired for each signing partner, the designated-partner minimum and the resident
condition still met, contribution figures agreeing between Form 11, the agreement and the accounts,
Form 8 figures traced to the finalised accounts, and each attachment within the portal's limits. The
fee is whatever the portal computes. The DSC and the payment are the CA's.
