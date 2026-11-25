---
name: file-a-new-hire-with-the-state
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 20min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Submit required new-hire reporting to the appropriate state or government agency by the deadline.

## Preconditions

- The new hire has started or is scheduled according to reporting rules.
- Required employee and employer identifiers are available.
- You know the filing jurisdiction and deadline.

## Steps

1. **Identify the jurisdiction.** Determine the state or agency based on work location, withholding setup, or reporting rule. → *Expect:* the correct filing destination is known.
2. **Gather required data.** Confirm employee legal name, address, start date, SSN or local identifier, employer name, address, and employer ID. → *Expect:* required fields are complete.
3. **Open the reporting portal.** Sign in to the state or agency new-hire reporting system. → *Expect:* the new-hire filing form or upload page is visible.
4. **Enter or upload the report.** Add the employee record manually or upload the approved file format. → *Expect:* the portal validates the submission fields.
5. **Review before submission.** Confirm employee identity, employer ID, work state, and start date. → *Expect:* the preview matches HR and payroll records.
6. **Submit the filing.** Send the report through the portal. → *Expect:* the portal displays a confirmation or receipt.
7. **Save confirmation.** Store confirmation number, filing date, and submitted record in the approved payroll or HR location. → *Expect:* the filing has an audit record.

## Decision points

- If the employee works in multiple states → ask payroll which jurisdiction to report.
- If required identifiers are missing → pause and collect them through secure onboarding or payroll channels.
- If the deadline has passed → file immediately and notify payroll or compliance owner.

## Failure modes & recovery

- **F1 Wrong state:** detect filing jurisdiction mismatch → submit to the correct state and document whether correction is needed.
- **F2 Identifier error:** detect SSN or employer ID rejection → verify source documents and resubmit securely.
- **F3 No confirmation:** detect submission without receipt → check portal history or contact agency support.

## Verification

The appropriate agency portal shows a submitted new-hire report with confirmation number, filing date, correct jurisdiction, and matching employee data.

## Variations

- US: most states require new-hire reporting within a short statutory deadline and specific identifiers.
- Other countries: equivalent starter, tax, social insurance, or labor agency registration rules vary widely.
- Payroll provider filing: verify provider submission status and save the provider confirmation.

## Safety & privacy

Medium risk because filings use SSNs or similar identifiers and legal employment data. Use secure portals, avoid emailing identifiers, verify jurisdiction, and retain only required proof.
