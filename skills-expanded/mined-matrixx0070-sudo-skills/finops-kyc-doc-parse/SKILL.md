---
name: finops-kyc-doc-parse
version: 1.0.0
description: Extract and structure identity, entity, and ownership data from KYC/onboarding documents — IDs, proof of address, incorporation and ownership records — into verified fields, flagging quality, consistency, and expiry issues.
author: matrixx0070
tags: [kyc, onboarding, cdd, document-verification, identity, aml, operations]
capabilities: []
---

# KYC Document Parse

## When to use
Use this to turn a stack of onboarding documents into structured, checked KYC fields — reading a passport/ID, proof of address, certificate of incorporation, register of directors, or an ownership chart and emitting normalized data with per-field confidence and a list of quality/consistency exceptions. It prepares the evidence that risk rating and screening then act on.

**Not for:** deciding whether to accept the client or setting their risk rating (hand the structured output to finops-kyc-rules), or running sanctions/PEP screening. This *extracts and validates the documents*; it does not adjudicate the customer.

## Method
1. **Classify each document.** Identify type (passport, national ID, driving licence, utility bill, bank statement, certificate of incorporation, shareholder register, trust deed) and the party it belongs to.
2. **Determine required set.** Decision point: individual vs entity drives the checklist — an individual needs identity + address; an entity needs formation, directors, and beneficial-ownership evidence down to the UBO threshold.
3. **Extract fields per type** into normalized form: names, dates, document number, issuing authority, expiry, address, entity name/number, jurisdiction, directors, and ownership percentages.
4. **Validate each field.** Check format (date validity, ID checksum/MRZ where present), legibility, and internal consistency (name matches across documents, address matches the application).
5. **Check currency and authenticity signals.** Decision point: flag expired IDs, proof-of-address older than the accepted window (commonly 3 months), missing pages, or signs of alteration — these block acceptance until cured.
6. **Reconcile the ownership chain.** For entities, walk shareholders through intermediate holders to the ultimate beneficial owners; confirm percentages roll up and identify every UBO at/above the threshold.
7. **Emit structured output + exceptions.** Per-field value and confidence, per-document status, and a prioritized exception list (missing / expired / inconsistent / illegible / unverified UBO). Never invent a field the document doesn't support.

## Example
Corporate onboarding. Documents: certificate of incorporation (Delaware, entity #, formed 2019), register of members, two director IDs, one utility bill. Extraction: entity name, number, jurisdiction, two directors (passports, both valid), registered address (matches application). Ownership: HoldCo owns 100% of the applicant; HoldCo is owned 60% by Individual A and 40% by Individual B → both are UBOs above a 25% threshold. Exceptions: (1) Individual B's ID expired last month — BLOCK, request current ID; (2) utility bill is 5 months old — exceeds 3-month window, request recent proof of address; (3) name on register "Jon A. Smith" vs passport "Jonathan Alan Smith" — likely match, flag for review. Structured record emitted with these three items open.

## Pitfalls
- **Confabulating a missing field.** If a document doesn't state a value, emit "not present," never a guess — a fabricated KYC field is a control and regulatory failure.
- **Missing an indirect UBO.** Stopping at the direct shareholder hides beneficial owners behind holding companies, trusts, or nominees; walk the chain to the natural persons.
- **Accepting stale proof of address.** Utility bills/bank statements older than the accepted window (typically 3 months) don't evidence current residence.
- **Name/DOB near-matches waved through.** "J. Smith" vs "John Smith," transposed dates, or transliteration differences must be flagged for review, not silently accepted or rejected.
- **Ignoring expiry and document integrity.** An expired ID, missing MRZ, or altered field invalidates the evidence regardless of how clean the extracted data looks.

## Output format
```
Party: <individual / entity> | Applicant: <name/number>
Documents:
  | doc type | party | status (valid/expired/illegible/missing) | expiry | confidence |
Extracted fields:
  | field | value | source doc | confidence | consistency (matches app/other docs) |
Ownership chain (entities):
  <shareholder> → <intermediate> → <UBO> : <% roll-up>  | UBOs ≥ threshold: <list>
Exceptions (prioritized):
  | # | severity (block/review/info) | issue | field/doc | required action |
Record status: complete / incomplete (missing: <...>)
```

## Reference

### CDD document requirements
Customer Due Diligence requires evidence to (1) identify the customer and (2) verify that identity from reliable, independent sources.
- **Individuals:** full legal name, date of birth, residential address, and a government-issued photo ID (passport, national ID, driving licence) plus proof of address (utility bill, bank statement, government letter) usually dated within ~3 months.
- **Legal entities:** legal name, registered number and address, and formation evidence (certificate of incorporation, articles), plus the ownership and control structure — register of members/directors, and identification of beneficial owners.

### Beneficial ownership (UBO)
A **beneficial owner** is the natural person(s) who ultimately own or control the customer. The common threshold is **25% or more** of shares or voting rights (some regimes and higher-risk cases use lower thresholds, e.g., 10%). Where no owner meets the threshold, identify the natural person(s) exercising control by other means, and failing that the senior managing official. Chains through holding companies, partnerships, trusts (settlor, trustee, protector, beneficiaries), and nominees must be walked to the underlying natural persons — multiply percentages down the chain to compute effective ownership.

### Document validation signals
- **Passport MRZ:** two machine-readable lines encode name, document number, nationality, DOB, expiry, and check digits; the check digits validate the fields.
- **Date sanity:** issue < expiry; DOB consistent with a plausible age; expiry not in the past.
- **Consistency:** name, DOB, and address must agree across the ID, proof of address, and the application; discrepancies are review items.
- **Integrity:** legible, unaltered, all pages present, photo present where required.

### Individual vs entity checklists
| Requirement | Individual | Entity |
|---|---|---|
| Identity | Photo ID | Certificate of incorporation / registration |
| Verification | ID + proof of address | Registered details from an independent register |
| Address | Proof of address (≤3 mo) | Registered office evidence |
| Control | N/A | Directors / officers |
| Ownership | N/A | UBOs ≥ threshold, chain walked |
| Purpose | Nature/purpose of relationship | Nature/purpose + source of funds |

### Data quality and confidence
Emit a confidence per extracted field (high/medium/low or a score) reflecting legibility, source reliability, and cross-document agreement. Low-confidence or inconsistent fields become review exceptions; missing required fields make the record *incomplete* and block downstream acceptance. The extraction layer's job is fidelity — accurate values, honest gaps, and a clean exception list — not the accept/reject decision, which belongs to the rules layer.

### Reliance and record-keeping
Verification must use reliable, independent sources; where reliance is placed on a third party (introducer, another regulated firm), the underlying evidence must remain obtainable. KYC records — the documents and the extracted data — are typically retained for a defined period after the relationship ends (commonly 5 years) and must be reproducible for audit and regulatory request.
