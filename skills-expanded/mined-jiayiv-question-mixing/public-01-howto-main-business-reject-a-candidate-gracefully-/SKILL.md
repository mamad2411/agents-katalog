---
name: reject-a-candidate-gracefully
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Send a respectful candidate rejection and update the recruiting record with an appropriate status.

## Preconditions

- The hiring team has made a documented decision not to move forward.
- Any required disposition reason is known.
- You have access to the applicant tracking system or recruiting email.

## Steps

1. **Open the candidate record.** Confirm candidate name, role, stage, email, and decision status. → *Expect:* the correct candidate and requisition are visible.
2. **Confirm disposition reason.** Select the approved job-related reason or category in the ATS. → *Expect:* the record has a compliant disposition.
3. **Choose the rejection template.** Use the appropriate template for application, post-screen, post-interview, or final-stage rejection. → *Expect:* the message tone matches the candidate stage.
4. **Personalize carefully.** Add a brief thank-you or role reference without giving unsupported feedback or promises. → *Expect:* the message is respectful and accurate.
5. **Send the rejection.** Send the message through the ATS or approved recruiting channel. → *Expect:* the communication is marked sent.
6. **Update candidate status.** Move the candidate to rejected, archived, or talent pool status as appropriate. → *Expect:* the workflow no longer shows the candidate as active.
7. **Log follow-up limits.** Record any referral, reapply timing, or talent community note if approved. → *Expect:* future recruiters can see the intended next step.

## Decision points

- If the candidate is final-stage or internal → consider a phone call or manager-aligned message before email.
- If rejection reasons involve legal sensitivity → use approved language and consult HR or legal.
- If the candidate requests feedback → provide only approved, job-related feedback if company policy allows.

## Failure modes & recovery

- **F1 Wrong candidate:** detect a rejection sent to the wrong person → notify recruiting leadership and follow data incident or correction process.
- **F2 Discriminatory rationale:** detect notes tied to protected traits → escalate to HR and correct disposition documentation.
- **F3 Candidate still active:** detect the candidate remains in the workflow → update status and cancel pending interviews.

## Verification

The ATS shows the candidate rejected or archived with an approved disposition reason, sent communication, and no remaining active interviews.

## Variations

- US: disposition records may support EEO and OFCCP compliance for some employers.
- Other countries: candidate access, deletion, and feedback rights may differ.
- High-volume hiring: batch rejections may be appropriate after confirming status and template accuracy.

## Safety & privacy

Medium risk because rejection affects employment opportunity and creates discoverable records. Use fair-hiring criteria, avoid protected-class references, limit candidate PII, and keep communication respectful and truthful.
