---
name: contract-redline-scan
description: Scans a contract and flags risky clauses — IP assignment, indemnity, auto-renewal, exclusivity, payment terms — into a structured issue list for a human lawyer to review. Use when the user says "review this contract", "check this agreement", "any red flags in this NDA/MSA/SOW", or pastes/attaches a contract. Don't use for drafting the commercial offer itself — use proposal-builder — and never as a substitute for legal advice.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Business Ops, Legal, Contracts, Risk]
    related_skills: [proposal-builder, invoice-runner, pipeline-tracker]
---

# Contract Redline Scan

> **This is issue-spotting, not legal advice.** This skill helps a business owner walk into a lawyer conversation prepared — it does not replace the lawyer. Every scan output states this, and no contract gets signed on the strength of this scan alone. **A human lawyer signs off.**

Reads a contract end to end and produces a prioritized flag list across the five clause families that most often burn small operators: IP assignment, indemnity, auto-renewal, exclusivity, and payment terms. The standard: every flag quotes the exact clause text and page/section, so the lawyer's billable time goes to judgment, not hunting.

## When to Use

- User received a contract (NDA, MSA, SOW, partnership, platform ToS) and wants to know what to worry about before the lawyer call.
- User asks "anything scary in here?", "check the payment terms", "does this take my IP?".
- **Not for:** legal advice, negotiating on the user's behalf, or judging whether to sign — that is the lawyer's job. Not for writing the deal itself — use `proposal-builder`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Check the text is readable | `head -c 500 contract.txt` — real sentences, not binary garbage |
| Keyword sweep | `grep -n -i -E "assign|indemnif|renew|exclusiv|net [0-9]+|terminat|liabilit|perpetu|irrevocab" contract.txt` |
| Count sections found | `grep -c -i "indemnif" contract.txt` |
| Save the scan | write `redline-scan-<party>-<YYYY-MM-DD>.md` next to the contract |

## Procedure

1. **Precheck + rail** — confirm you have the contract as readable text (`read_file`; if it's a scanned PDF with no text layer, ask the user for a text export and stop). Open your reply with the issue-spotting-not-legal-advice rail verbatim before any analysis.
2. **Full read, then sweep** — read the whole document first; grep alone misses clauses written in plain words. Then run the keyword sweep from Quick Reference to catch anything you skimmed past. Note every hit's section number.
3. **Score the five families** — for each, extract the exact clause text and rate 🔴 / 🟡 / 🟢:
   - **IP assignment** — 🔴 if it assigns pre-existing IP, portfolio rights, or "all work product" with no carve-out for your tools/templates.
   - **Indemnity** — 🔴 if one-way against the user, uncapped, or covers the other party's own negligence.
   - **Auto-renewal** — 🔴 if renewal is automatic with a notice window under 30 days or buried terms changes on renewal.
   - **Exclusivity / non-compete** — 🔴 if it blocks the user from serving other clients in their actual niche or survives termination broadly.
   - **Payment terms** — 🔴 if net-60+, pay-when-paid, unilateral setoff rights, or no late-payment remedy.
4. **Catch-all pass** — flag anything else that limits liability asymmetrically, grants unilateral termination, or reads like it survives forever ("perpetual", "irrevocable"). One line each under "Other flags".
5. **Write lawyer questions** — turn every 🔴/🟡 into a specific question the user hands their lawyer ("Section 7.2 assigns 'all deliverables and related materials' — can we carve out pre-existing tools?"). Questions, not conclusions.
6. **Deliver** — fill the template, save the file, and close by repeating: nothing here is legal advice; the next step is a lawyer, not a signature.

## Output Template

```
# Redline Scan — {Contract name / counterparty}
{Date} · ⚠️ Issue-spotting only, NOT legal advice. A qualified lawyer must review before signing.

## Verdict at a glance
🔴 {n} high-attention · 🟡 {n} discuss · 🟢 {n} looks standard

## Flags
### 🔴 {Family} — §{X.X}
> "{exact clause text}"
Why it matters: {one sentence, business terms}.
Ask your lawyer: {specific question}

### 🟡 ...

## Other flags
- §{X} — {one-liner}

## Clean areas
{Families that came back 🟢, one line each — absence of a flag noted explicitly.}

## Next step
Send this scan + the contract to your lawyer. Do not sign before their review.
```

## Pitfalls

- **Grep-only scan misses plain-language traps** — "Client shall own everything Contractor creates" contains no keyword hit for "assign". Recovery: the full read in step 2 is mandatory; if you skipped it, go back before scoring.
- **Skill drifts into advice** ("this is fine to sign", "just strike section 7") — that's practicing law. Recovery: rewrite conclusions as lawyer questions; the verdict line counts flags, it never says "safe to sign".
- **Quote paraphrased instead of exact** — the lawyer can't find the clause and trust collapses. Recovery: every 🔴/🟡 must contain verbatim text in quotes with a section number; re-pull from the source if you summarized.
- **Missing text layer silently truncates the contract** — you scan 4 pages of a 12-page PDF and report it clean. Recovery: sanity-check length (page count vs. extracted text length); if they don't match, stop and ask for a full text export.

## Verification

- [ ] Output opens AND closes with the not-legal-advice / lawyer-signs-off rail
- [ ] All five clause families scored, each with verbatim quote + section number for 🔴/🟡
- [ ] Every 🔴/🟡 has a concrete lawyer question, no sign/don't-sign conclusions anywhere
- [ ] Extracted text length is plausible for the document's page count
- [ ] Scan saved as a file next to the contract
