---
name: fortax-contract-review
description: Review a contract, agreement, NDA, rent/lease deed, vendor or service agreement, shareholders' agreement or engagement letter under Indian law, say what it binds the client to, rate each clause RED/AMBER/GREEN, draft the pushback, triage an incoming NDA, and run the pre-signature check and signing order. Use for "contract review karo", "is agreement me risk kya hai", "NDA theek hai kya", "rent agreement check karo GST registration ke liye", "sign karne se pehle dekh lo".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "https://github.com/anthropics/knowledge-work-plugins/tree/main/legal/skills/review-contract (Apache-2.0); https://github.com/anthropics/knowledge-work-plugins/tree/main/legal/skills/triage-nda (Apache-2.0); https://github.com/anthropics/knowledge-work-plugins/tree/main/legal/skills/signature-request (Apache-2.0); https://github.com/evolsb/claude-legal-skill (MIT, Copyright (c) 2026 Christopher Sheehan)"
---

# Contract review

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

Typical asks: "is contract me client kis cheez se bandh raha hai", "NDA triage karo", "liability cap theek hai?",
"rent agreement GST ke liye chalega?", "signing se pehle checklist bana do".

Three jobs, one procedure:

| Job | Use | Where |
|---|---|---|
| Full review | Any contract the client will sign or has signed | Steps 1-7 below |
| NDA triage | A quick GREEN / YELLOW / RED on an incoming NDA | Step 8 and `references/nda-triage.md` |
| Pre-signature | Final agreed draft, before anyone signs | Step 9 |

## What this is, and what it is not

A CA is handed contracts constantly: a client's vendor agreement, a rent agreement for GST
registration, a service contract whose payment clause decides the TDS, a shareholders' agreement
before an allotment. They need to know what the document actually says, what it costs the client,
and which clauses are dangerous.

You give them that. You do **not** give a legal opinion, and you never tell the client a clause is
"enforceable" or "safe" as a conclusion of law. Where the answer turns on how a court would read
something, say so and say the client should take an advocate's view. That line goes in the output
once, plainly, not as boilerplate at the bottom of every section.

## Step 1 — get the text, all of it

- A file in the client folder: read the file. PDF, Word, RTF and plain text all work.
- A page open in the browser: read it with your browser tool (Claude in Chrome, a Playwright/browser
  MCP, or the Codex browser). If you have none, ask the CA to save the page as PDF or paste the text.
- Pasted text: use it as given.

If pages come back with no text, the document is a scan. Say so, read those pages as images (see
`fortax-pdf-extraction`), and mark every figure from them as read from an image.

**Read the whole document before flagging anything.** Clauses interact: an uncapped indemnity may be
cut down by a liability cap three pages later, and a definition in Schedule 1 can change what a clause
in the body means.

## Step 2 — before the substance, check the paper

- **Blanks.** Any "₹____", "[amount]", "TBD", a blank date. List them at the top. A blank in a signed
  contract is a problem; in a draft it is a question for the client.
- **Schedules and annexures.** List every one the body refers to and say which are missing. A payment
  schedule that is "as per Annexure B" with no Annexure B means the price is unknown.
- **Parties.** Exact legal names. A proprietor contracting in a trade name, a company whose name does
  not match its CIN, or a signatory with no stated authority are all flags.
- **Executed or draft**, and the effective date against the signing date.
- **Stamping.** Whether the instrument appears stamped (e-stamp certificate, franking, stamp paper),
  and in which state. An insufficiently stamped instrument can be refused as evidence until duty and
  penalty are paid under the state's stamp law. Stamp duty is a state schedule that changes: look it
  up for the state and the instrument type, never state a rate from memory.
- **Registration.** A lease of immovable property for more than a year, and some other instruments,
  need registration under the Registration Act, 1908. Flag it; the CA confirms.

## Step 3 — whose side, and what kind of document

Ask if it is not obvious: which party is our client? Customer or vendor, landlord or tenant,
disclosing or receiving party, investor or promoter. Risk only exists relative to a side.

Then name the document type, because it decides which clauses are material. Leverage matters too:
a small client buying from a sole-source vendor will get fewer changes than a large customer in a
competitive market; terms required by a regulator (RBI, card networks, NPCI) are not negotiable.

## Step 4 — the clause map

Go through every clause that exists and every one that should but does not. For each, quote the
clause number so the CA can find it.

| Area | What to look for |
|---|---|
| **Scope and deliverables** | Is what is being bought actually defined? Acceptance criteria? |
| **Price and payment** | Amount, milestones, credit period, late-payment interest, price escalation, who can revise the price, auto-debit authority, holdback or reserve |
| **GST** | Price inclusive or exclusive of GST, who bears it, tax invoice and e-invoice obligations, cooperation on ITC and 2B mismatches, reverse charge where it applies |
| **TDS** | Whether payments will suffer TDS, whether the contract grosses up, whether it requires the payer to issue certificates. Name the section only after looking up which one applies to this payment type |
| **MSME** | If the supplier is Udyam-registered, whether the credit period is within the MSMED Act limit and what interest the Act imposes if it is not; also the income-tax disallowance for late MSME payment. Look the limits up |
| **Term and renewal** | Start, end, auto-renewal, and how much notice stops it (short notice windows are a trap) |
| **Termination** | For convenience (both sides or one?), for cause, cure period, suspension without notice, what survives, exit costs, data export on exit |
| **Limitation of liability** | Cap amount and basis, what is carved out of the cap, whether the exclusion of indirect loss is mutual |
| **Indemnity** | Mutual or one-way, triggers, whether capped, notice and defence control |
| **Warranties** | "As is" with no warranty, warranty period, exclusive-remedy clauses |
| **Confidentiality** | Definition, carve-outs, term, return or destruction on exit |
| **Data** | Whether personal data is handled; if so, obligations under the Digital Personal Data Protection Act, 2023 (processor contract, safeguards, breach notice, erasure on exit — see `fortax-india-dpdp-act`). Cross-border transfer if a party is abroad; RBI storage rules for payment data |
| **IP** | Who owns what is created, licences back, pre-existing IP protected, feedback ownership |
| **Non-compete and non-solicit** | Restraints of trade are void under section 27 of the Indian Contract Act, 1872 except in narrow cases; restraints during the contract are treated differently from those after it ends. Flag any; confirm the current judicial position from a cited source |
| **Liquidated damages and penalties** | Under sections 73-74 of the Contract Act a named sum is not automatically recoverable; reasonable compensation up to it is. Flag clauses that read as punishment |
| **Dispute resolution** | Courts or arbitration, **seat** versus venue, number of arbitrators, and **who appoints them**. Clauses letting one party alone appoint the sole arbitrator have been struck down by the Supreme Court; research and cite the current judgment before relying on it |
| **Governing law and jurisdiction** | Indian law? Which courts? A foreign law or offshore seat (Singapore, BVI, Cayman, London) for an Indian client is expensive to enforce |
| **Assignment and change of control** | Can they assign and we cannot? |
| **Amendment** | Can one side change the terms unilaterally ("as updated on our website")? |
| **"Sole discretion"** | Discretion given to the counterparty with no objective standard |
| **Force majeure** | Scope, notice, and whether it lets either side walk away |
| **Related parties** | If the counterparty is related to the client company, board or shareholder approval under section 188 of the Companies Act, 2013 may be needed before signing. Say so, do not decide it |
| **Foreign party** | FEMA reporting or approval may apply to the payment or the investment; equalisation levy or withholding on payments abroad. Flag it for the CA |
| **Rent / lease (GST registration)** | Lessor name matches the property owner or there is an NOC/consent, address matches the registration address exactly, period covers today, stamped; GST on commercial rent and reverse charge where the tenant is registered and the landlord is not |

For deal-specific checklists (NDA, SaaS/MSA, payment/merchant, M&A, finder/broker), the 41-category
CUAD risk list and the negotiability guide, read `references/clause-checklists.md`. They were written
for US practice: use them as a list of what to look at, not as the Indian market standard.

## Step 5 — red flags first

Before the deep pass, scan for these. Any one of them goes to the top of the findings.

| Red flag | Why it matters |
|---|---|
| Liability cap under six months' fees, or none | The client carries almost all the risk |
| Uncapped indemnity | Unlimited exposure |
| "As is" with no warranty | No recourse for defects |
| Suspension without notice | The service can vanish |
| Unilateral amendment right | Terms can change after signing |
| No termination for convenience | Locked in |
| Perpetual obligations (tails, non-competes) | Indefinite exposure |
| Offshore jurisdiction or foreign seat | Expensive to enforce |
| Pre-signed conflict waivers | No recourse for conflicts |
| "Sole discretion" for the counterparty | No objective standard |
| Unilateral arbitrator appointment | Challengeable, and slow when challenged |
| Asymmetric assignment | They can assign, you cannot |

## Step 6 — rate each finding

| Rating | Meaning |
|---|---|
| **RED** | Exposes the client to open-ended liability, loss of a core asset, a payment it cannot recover, or a statutory breach. Must change before signing |
| **AMBER** | Outside what is normal for this kind of deal but negotiable. Push back |
| **GREEN** | Normal and acceptable for our side. Note only |

Say *why* each RED is red in money or consequence, not in adjectives: "No liability cap, so a data
breach claim against the client has no ceiling" beats "this is a high-risk clause". For a scored
severity x likelihood view of a single risk, use `fortax-legal-compliance-check`.

## Step 7 — what to ask for

For every RED and AMBER, give:

```
Clause 11.2 — Limitation of liability
Says:     "The Service Provider's aggregate liability shall not exceed fees paid in the preceding
           one month."
Ask for:  "…shall not exceed the fees paid in the twelve months preceding the claim."
Why:      A one-month cap on an annual contract leaves the client carrying almost all the risk.
Priority: Must have
Fallback: Six months' fees.
```

Quote the contract exactly. Keep suggested language plain and usable; the CA may paste it into a mail.
Do not draft a whole replacement agreement unless asked.

### Output of a full review

```
Contract review — <document name>
Parties: <our client> (<side>) and <counterparty>
Type: <type>   Status: <draft / executed>   Read from: <file / page / pasted>, <N> pages

Before anything else
- <blanks, missing schedules, stamping, registration, authority — or "Nothing missing">

What it binds the client to
- <plain summary: pay what, when, for how long, and how to get out>

Money and dates
| Item | Value | Clause |

Findings
| # | Rating | Clause | Issue | Consequence |

What to ask for
<the Step 7 blocks, RED first>

Needs an advocate's view
- <only the points that turn on how a court would read them>

Tax points for the CA
- <GST, TDS, MSME, related-party, FEMA — flagged, not concluded>
```

Save it next to the contract in the client folder as `YYYY-MM-DD_<document>_review.md` and give the CA
the first two sections in chat.

## Step 8 — NDA triage

For an incoming NDA the CA wants sorted fast, screen it against the ten criteria in
`references/nda-triage.md` (structure, definition, obligations, carve-outs, permitted disclosures,
term, return/destruction, remedies, problem provisions, law and forum) and classify:

- **GREEN — standard.** Mutual (or one-way in the right direction), all five standard carve-outs
  (public, prior possession, independent development, third-party receipt, legal compulsion), term
  1-3 years with survival 2-5 years, no non-solicit / non-compete / exclusivity, no or narrow
  residuals, Indian law and a sensible forum, no liquidated damages, disclosure allowed to employees,
  contractors and advisers, retention exception for legal copies. Client can sign under its normal
  authority.
- **YELLOW — needs a look.** Broader definition, longer but market term, one carve-out missing,
  narrow residuals, non-preferred forum, minor asymmetry, workable marking rule, no explicit retention
  exception. One pass of redlines should fix it.
- **RED — full review, do not sign.** Wrong direction, missing independent-development or
  legal-compulsion carve-out, non-solicit or non-compete inside the NDA, exclusivity or standstill
  without an M&A reason, 10+ years or perpetual without a trade-secret reason, overbroad definition,
  broad residuals, hidden IP licence or assignment, liquidated damages, unscoped audit rights, foreign
  forum with mandatory arbitration, or a document that is not really an NDA (commercial terms inside).
  Counter with the client's own NDA or send for full review under Steps 1-7.

If the client or firm has its own NDA playbook (a file in the client folder), use it and say so;
otherwise say the defaults above were applied. Output format is in the reference.

## Step 9 — pre-signature check and signing order

Only on a final agreed draft. Nothing is sent or signed from here: you prepare the checklist and the
signing order; the client signs and the CA or client sends it.

```
Pre-signature check — <document>
[ ] Final agreed form, no open redlines or comments, blanks filled
[ ] All schedules, annexures and exhibits attached
[ ] Exact legal names, CIN/LLPIN/PAN/GSTIN where quoted, registered addresses
[ ] Signatory authority: board resolution / partner authority / POA for each signer
[ ] Internal approvals done: board, shareholders (s.180/s.188 where relevant), lender consent if a covenant needs it
[ ] Stamp duty paid before or at execution, in the right state and amount (confirm the state schedule); e-stamp certificate attached
[ ] Registration needed? (lease > 1 year, conveyance) — book the sub-registrar
[ ] E-signature allowed for this instrument? The IT Act, 2000 First Schedule excludes some documents (e.g. power of attorney, trust, will, sale/conveyance of immovable property) — confirm
[ ] Dates: execution date and effective date agreed, or left blank for the date of last signature
[ ] Witnesses where the instrument or state law needs them
[ ] Reviewed by an advocate where Step 7 said it needs one
```

Then the signing configuration:

```
| Order | Signer | Email / phone | Signs for | Mode (wet / Aadhaar eSign / DSC) |
| 1     |        |               | <client>  |                                   |
| 2     |        |               | <counterparty> |                              |
CC on the executed copy: <names>
Status: Ready for the client to send / Issues to resolve first: <list>
Next: expected turnaround, follow-up if not signed within <N> days, where the executed copy is filed
```

The most common signing errors are a wrong legal entity name and a signer with no authority. Once
executed, the copy goes into the client folder next to the review, stamp certificate with it.

## Rules that do not bend

- **Every finding points at a clause number.** A finding you cannot anchor to text is not a finding.
- **No rates, no limits, no due dates from memory.** Stamp duty, TDS rates, the MSME credit limit,
  interest rates: run `python3 scripts/fortax.py kb "<question>" --topics tds,gst` and quote the source
  and captured date. If the match is `weak` or `none`, write "confirm on the notification / state
  schedule" and name the law.
- **No case law from memory.** Research it (`fortax-deep-research`) and use only a judgment you can cite.
- **Never tell the CA to sign.** You say what the document does. They and the client decide.
- **Never send the document to the counterparty or a signing platform.** Draft; the CA sends.

---

Credits: the clause-by-clause workflow, the three-tier rating and the redline format are adapted from
`review-contract`; the NDA screen from `triage-nda`; the pre-signature checklist and signing
configuration from `signature-request` — all in
[anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins), © Anthropic,
Apache License 2.0 (`LICENSE-THIRD-PARTY-knowledge-work-plugins.txt`). The blanks-and-exhibits
pre-check, red-flag scan and the checklists in `references/clause-checklists.md` are from
[evolsb/claude-legal-skill](https://github.com/evolsb/claude-legal-skill), MIT, Copyright (c) 2026
Christopher Sheehan (`LICENSE-THIRD-PARTY-claude-legal-skill.txt`).

Changes by Fortax: adapted for Indian law and CA practice, merged with triage-nda and
signature-request (knowledge-work-plugins) and the checklists of claude-legal-skill; added Indian
stamping, registration, GST, TDS, MSME, DPDP, Contract Act, Companies Act and FEMA checks; removed
CLM / e-signature connector steps (nothing is sent or signed by the agent).
