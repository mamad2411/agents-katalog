---
name: send-an-interview-invite
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Send a candidate a clear interview invitation with time, format, preparation details, and contact information.

## Preconditions

- The interview time, interviewer, format, and role are confirmed.
- Candidate contact information is available.
- Any accommodation or accessibility process is known.

## Steps

1. **Open the candidate record.** Confirm candidate name, email address, role, and interview stage. → *Expect:* the invite will go to the correct person.
2. **Select the invite template.** Use the approved interview invitation template for the stage and format. → *Expect:* the message includes standard recruiting language.
3. **Add schedule details.** Insert date, time zone, duration, interviewer names, meeting link or location, and check-in instructions. → *Expect:* the candidate can tell when and where to attend.
4. **Add preparation guidance.** Include agenda, materials to bring, portfolio expectations, or assessment instructions if applicable. → *Expect:* the candidate knows how to prepare.
5. **Include support contact.** Provide recruiter contact details and accommodation request language. → *Expect:* the candidate has a path for questions or access needs.
6. **Send the invitation.** Send the email or ATS message and attach the calendar invite if supported. → *Expect:* the message is marked sent.
7. **Record the communication.** Confirm the invite appears in the ATS activity log. → *Expect:* the recruiting record shows the invitation timestamp.

## Decision points

- If the candidate has not confirmed availability → send a scheduling request instead of a fixed invite.
- If the interview is onsite → include address, parking, reception, ID, and accessibility details.
- If the candidate requests accommodation → route through the approved process and share only need-to-know information.

## Failure modes & recovery

- **F1 Wrong time zone:** detect candidate confusion or mismatched calendar time → resend with explicit time zone and corrected calendar invite.
- **F2 Broken meeting link:** detect an invalid or missing link → create a new link and update the candidate and interviewers.
- **F3 Message not logged:** detect no ATS activity entry → manually log the communication or resend through the ATS.

## Verification

The candidate received an invitation with correct date, time zone, format, location or link, preparation notes, and recruiter contact information.

## Variations

- US: include equal opportunity and accommodation language consistent with company practice.
- Other countries: adjust privacy, identification, travel reimbursement, and accessibility language for local rules.
- Phone interview: include caller responsibility, phone number, backup number, and expected caller ID if available.

## Safety & privacy

Low risk, but candidate contact details and interview logistics are confidential. Do not expose other candidates, private interviewer notes, or unnecessary personal data in the invite.
