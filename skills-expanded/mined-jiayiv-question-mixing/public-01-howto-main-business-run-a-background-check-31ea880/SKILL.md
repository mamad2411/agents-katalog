---
name: run-a-background-check
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

Initiate an authorized background check for a candidate or employee and track it through compliant completion.

## Preconditions

- The check is required for the role and allowed by policy and law.
- The person has received required disclosures and given required authorization.
- You have access to the approved background check vendor or HR system.

## Steps

1. **Confirm eligibility.** Verify role, jurisdiction, timing, and check package are appropriate. → *Expect:* the check type matches the role and location.
2. **Confirm authorization.** Check that required consent, disclosure, and identity information are complete. → *Expect:* the record shows authorization before ordering.
3. **Open the vendor workflow.** Select the candidate or employee and the approved background package. → *Expect:* the vendor form displays the correct person and package.
4. **Review submitted data.** Confirm legal name, email, location, and required identifiers are correct. → *Expect:* the order data has no obvious mismatch.
5. **Submit the order.** ⚠️ *Irreversible:* confirm consent and package before submission because the vendor may begin processing immediately. → *Expect:* the vendor shows the check as ordered or in progress.
6. **Monitor status.** Track pending items, candidate action requests, and estimated completion. → *Expect:* blockers are visible.
7. **Record completion.** Save pass, review, or adjudication-needed status according to policy without copying unnecessary report details. → *Expect:* the HR or ATS record reflects the outcome.

## Decision points

- If consent is missing → do not order the check until authorization is complete.
- If the report has adverse information → follow the legally required pre-adverse and adverse action process before final action.
- If identity data conflicts → pause and ask the candidate or vendor to correct it.

## Failure modes & recovery

- **F1 Unauthorized order:** detect missing consent after submission → escalate to HR or legal and follow incident procedure.
- **F2 Candidate does not respond:** detect pending candidate action past deadline → send a reminder with vendor support details.
- **F3 Adverse result mishandled:** detect rejection without required notice → stop the decision and start the required adverse action process.

## Verification

The vendor shows the check ordered with valid authorization, current status is tracked, and the HR or ATS record contains only the necessary outcome.

## Variations

- US: comply with FCRA, ban-the-box, state timing rules, and adverse action notices.
- Other countries: background checks may require stricter consent, narrower scope, local vendor handling, or may be prohibited for some data.
- Regulated roles: package may include licenses, sanctions, education, or criminal checks required by law.

## Safety & privacy

Medium risk because background reports contain highly sensitive PII and can affect employment. Use the minimum lawful package, verify consent, restrict report access, and avoid discriminatory or inconsistent adjudication.
