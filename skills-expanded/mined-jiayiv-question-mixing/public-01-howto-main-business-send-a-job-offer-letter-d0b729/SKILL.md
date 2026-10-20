---
name: send-a-job-offer-letter
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 30min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Send an approved job offer letter to the selected candidate with accurate terms and acceptance instructions.

## Preconditions

- Final candidate selection and compensation are approved.
- Offer terms, start date, manager, location, and contingencies are confirmed.
- You have the approved offer template and candidate contact information.

## Steps

1. **Open the candidate record.** Confirm candidate identity, role, requisition, and offer approval status. → *Expect:* the offer workflow is ready for drafting.
2. **Enter offer terms.** Add title, salary or hourly rate, bonus or equity if applicable, benefits summary, location, start date, reporting manager, and employment status. → *Expect:* the offer fields match approvals.
3. **Add contingencies.** Include background check, work authorization, reference, drug screen, or credential requirements only if approved and lawful. → *Expect:* contingencies are visible in the letter.
4. **Review legal language.** Confirm at-will or local employment terms, expiration date, confidentiality, and signature requirements. → *Expect:* the letter uses the current approved template.
5. **Get final approval.** Route the offer for recruiter, compensation, HR, finance, or legal approval as required. → *Expect:* all required approvals show complete.
6. **Send the offer.** ⚠️ *Irreversible:* confirm recipient, terms, and approvals before sending because the candidate may rely on the written offer. → *Expect:* the offer is sent to the candidate.
7. **Log the deadline.** Record the response deadline and follow-up task in the ATS. → *Expect:* the recruiting team can track acceptance status.

## Decision points

- If terms differ from approval → stop and obtain corrected approval before sending.
- If the candidate negotiated verbally → update the written offer only after approved changes.
- If the offer is contingent → make the contingency clear without implying final employment before completion.

## Failure modes & recovery

- **F1 Wrong compensation:** detect mismatch with approved pay → void or correct the offer according to legal guidance and notify approvers.
- **F2 Wrong recipient:** detect delivery to the wrong email → escalate immediately, revoke access if possible, and follow data incident procedure.
- **F3 Missing approval:** detect incomplete routing → hold the offer until approvals are complete.

## Verification

The candidate record shows an offer sent to the correct candidate, with approved terms, required contingencies, expiration date, and a follow-up task.

## Variations

- US: include at-will language where applicable and comply with pay transparency and authorization rules.
- Other countries: employment contracts may require statutory terms, probation clauses, notice periods, or local-language versions.
- Executive offer: involve legal, compensation, equity, and board approval before sending.

## Safety & privacy

Medium risk because compensation, identity, and employment terms are sensitive. Verify recipient and approvals, protect PII, document decisions consistently, and avoid terms that could create unfair or discriminatory treatment.
