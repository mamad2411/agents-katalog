---
name: fortax-legal-response
description: Draft a reply to a routine legal inquiry for a client from a template — a DPDP data principal request (access, correction, erasure, grievance), a document preservation notice, a vendor's legal question, an NDA request, a privacy inquiry, an acknowledgement of a summons or legal notice, an insurance claim intimation — and stop with an escalation note when the matter should not get a template reply. Use for "is request ka jawab draft karo", "customer ne data delete karne bola hai", "legal notice ka acknowledgement bhejna hai", "litigation hold notice banao", "insurance company ko intimation".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "https://github.com/anthropics/knowledge-work-plugins/tree/main/legal/skills/legal-response (Apache-2.0)"
---

# Legal response from templates

Typical asks: "customer ne apna data maanga hai, reply draft karo", "vendor audit maang raha hai",
"cheque bounce ka notice aaya hai", "employees ko data preserve karne ka notice", "NDA bhejna hai".

You draft; the CA or the client reviews and sends from their own mail. This is not legal advice, and
regulated replies (data requests, anything to a court, police or department) are always reviewed before
they go. Tax notices (GST, income-tax, TDS) are not handled here: use `fortax-notice-reply`.

## Inquiry types

| Type | Covers |
|---|---|
| `dpr` / `dsr` | Data principal (or data subject) request: access, correction, completion, updating, erasure, grievance, nomination, withdrawal of consent |
| `hold` | Document preservation notice to staff, reminder, scope change, release |
| `vendor` | A vendor's legal question: contract status, amendment request, compliance certificate, audit request, insurance certificate |
| `nda` | Sending the client's NDA, accepting the counterparty's with markup, declining, renewal |
| `privacy` | Cookies and tracking, privacy notice questions, data sharing, children's data, transfers abroad |
| `legal-process` | Acknowledgement of a court summons, a notice to produce documents, a police or regulator notice, a lawyer's legal notice; request for time; cover letter for documents |
| `insurance` | Claim intimation, further information, reply to a reservation of rights |
| `custom` | A template the client or firm keeps |

If no type is given, show this table and ask.

## Step 1 — identify the inquiry

Read the inquiry itself (mail, letter, notice — read the file). Note who sent it, when it was received
(deadlines run from receipt), what exactly is asked, and any reference number.

## Step 2 — load the template

Look in the client folder for the firm's or client's approved templates (a `templates/` folder or a
`legal-templates.md`). If one fits, use it and name it. If none:

- say that no template was found for this type;
- use the default structure in `references/response-templates.md`;
- offer to turn the approved draft into a template (guide in the same reference).

## Step 3 — check escalation triggers first

Before drafting, check whether this matter should not get a templated reply.

**Any category:**
- Possible litigation, arbitration, or a regulator's or department's investigation
- The inquiry is from a regulator, government department, police or court
- The reply could create a binding commitment, an admission, or a waiver of rights
- Possible criminal liability (cheque dishonour, fraud allegation, data theft, anything under BNS)
- Media attention, actual or likely
- Unprecedented for the client (never handled before)
- More than one jurisdiction with conflicting rules
- Promoters, directors or senior management personally involved

**Data principal requests:**
- The data is a child's, or the request is by or for a child or a person with a disability through a guardian
- The request comes from the Data Protection Board or another authority, not the individual
- The data is under a preservation hold for a dispute
- The requester is a current or former employee in a dispute or HR matter
- The scope is unusually wide or looks like fishing for a dispute
- The data is processed abroad or also under GDPR/CCPA
- Health, biometric, financial, Aadhaar or other sensitive data

**Preservation (hold) notices:**
- Possible criminal liability
- Scope unclear, disputed or too wide
- Doubt whether certain data is within scope
- Earlier holds for the same or a related matter
- The hold would disrupt operations significantly
- The hold conflicts with a legal duty to erase (DPDP erasure, retention limits)
- A custodian objects

**Vendor questions:**
- A dispute or possible breach
- The vendor threatens litigation or termination
- Regulatory compliance, not just contract terms
- The reply could bind or waive
- The reply could affect a live negotiation

**NDA requests:**
- The counterparty is a competitor
- Government or defence information
- The context suggests an acquisition or investment
- Unusual subject matter (AI training data, biometric data, source code)

**Legal process (summons, notices, legal notices):**
- **Always needs an advocate's review.** Templates are only a starting frame.
- Any statutory period running (e.g. a demand notice for a dishonoured cheque, a notice before a suit)
- Privilege or confidentiality issues
- Third-party data in what is asked for
- Documents or people abroad
- An unreasonable time limit

**When a trigger fires:**
1. **Stop** — no templated reply.
2. **Alert** — tell the CA a trigger was found.
3. **Explain** — which trigger and why it matters.
4. **Recommend** — who should handle it: the CA personally, the client's advocate, a specialist.
5. **Offer** — a draft clearly headed `DRAFT — FOR ADVOCATE REVIEW ONLY — NOT TO BE SENT`, not a final reply.

## Step 4 — gather the details

**Data principal request:** requester's name and contact; request type; what data and in which systems;
the law that applies (DPDP Act, 2023 and DPDP Rules; GDPR/CCPA only if applicable); date received and the
response deadline — look the period up in the current Rules (see `fortax-india-dpdp-act`) or mark
"confirm"; the client's grievance officer or DPO contact.

**Preservation notice:** matter name and reference; custodians; scope (date range, data types, systems —
mail, WhatsApp and other chats, Tally/ERP, laptops, phones, paper files); the advocate's contact; effective date.

**Vendor question:** vendor; the agreement and clause; the exact question.

**NDA request:** who in the client asked; counterparty; purpose; mutual or one-way; special needs.

**Legal process:** issuing court or authority, case or notice number, provision cited, date of receipt,
date for reply or appearance, what is demanded.

**Insurance:** policy number and period, insurer, what happened and when, notice clause in the policy.

## Step 5 — draft the reply

Fill the template with the details. The reply:
- uses the right tone for the audience (plain for a customer or business team, formal for an authority),
  and for the relationship (new, existing, adversarial) and urgency;
- has every element required for the type (reference, the right the person is exercising, deadline, contact,
  complaint route where the law requires it);
- states specific dates, deadlines and obligations — each deadline computed from the receipt date in a
  sheet or script, not in your head;
- gives clear next steps;
- admits nothing and waives nothing unless the CA says so.

Must be customised every time: correct names, dates, reference numbers; the facts of this matter; the law
and jurisdiction that apply (check a cited provision is right for the requester's location); the correct
deadline; the signature block and contact of the person who will send it.

Present the draft to the CA. Never send it.

## Output

```
Draft response — <type> — <client>

To: <recipient>
Subject: <subject line>

---
<reply body>
---

Escalation check
<"No trigger found" with the list checked, OR the triggers found and the recommendation>

Deadline
<received on <date>; reply due by <date> under <law / rule / clause>, or "confirm the period">

Follow-up
1. <after sending: log the request, file the reply in the client folder>
2. <calendar reminders to set>
3. <record keeping: request log entry, hold acknowledgement tracking>
```

Save as `YYYY-MM-DD_<type>_<counterparty>_draft.md` next to the inquiry in the client folder. When the CA
edits a templated draft before sending, suggest updating the template so the next one starts better.

## Rules

- **Draft only.** The CA or client sends from their own mail. No auto-reply, no mail sent from here.
- **No periods, penalties or provisions from memory.** Look them up or write "confirm" with the law named.
- **No case law from memory.**
- **Legal process always goes to an advocate** before anything is sent.
- **Examples use made-up names** (Sharma Traders, Riya Mehta).

---

Credits: the workflow, escalation triggers, response categories and template method are adapted from
`legal-response` in [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins/tree/main/legal/skills/legal-response),
© Anthropic, Apache License 2.0 (`LICENSE-THIRD-PARTY-knowledge-work-plugins.txt`).

Changes by Fortax: adapted for Indian law and CA practice, not merged with another source; data subject
requests reworked around the DPDP Act, 2023; US discovery holds and subpoenas reworked as preservation
notices and Indian summons and legal notices; tax notices routed to fortax-notice-reply; mail-connector
sending removed (drafts only); templates moved to `references/response-templates.md`.
