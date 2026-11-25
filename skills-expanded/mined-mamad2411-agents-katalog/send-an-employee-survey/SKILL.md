---
name: send-an-employee-survey
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 30min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Send an employee survey with the correct audience, questions, anonymity settings, and response deadline.

## Preconditions

- Survey purpose, questions, audience, and timeline are approved.
- You have access to the survey tool and employee list.
- Privacy and reporting thresholds are defined.

## Steps

1. **Create the survey draft.** Add title, introduction, questions, response scale, and estimated completion time. → *Expect:* the survey content is visible in draft mode.
2. **Set privacy options.** Configure anonymous or confidential settings, reporting thresholds, and data access permissions. → *Expect:* privacy settings match the approved plan.
3. **Upload the audience.** Select employees by department, location, tenure, or other approved filters. → *Expect:* recipient count matches the target population.
4. **Preview the survey.** Test the employee view, mobile layout, branching, and required questions. → *Expect:* the survey can be completed without errors.
5. **Schedule communications.** Add launch message, deadline, reminders, and support contact. → *Expect:* communications are queued with correct dates.
6. **Send the survey.** Release the survey to the selected audience. → *Expect:* the survey tool shows sent or active status.
7. **Monitor response rate.** Track responses without identifying individuals beyond approved reporting rules. → *Expect:* aggregate participation is visible.

## Decision points

- If anonymity cannot be guaranteed → state the actual privacy model clearly before sending.
- If a small group would reveal identities → suppress or combine reporting groups.
- If survey questions involve protected traits or sensitive topics → get HR or legal review before launch.

## Failure modes & recovery

- **F1 Wrong audience:** detect recipients outside the approved group → close the survey if needed and notify HR about correction.
- **F2 Privacy mismatch:** detect settings that expose individual responses → pause reporting and restrict access.
- **F3 Broken question logic:** detect incomplete or contradictory branching → fix the survey and decide whether to relaunch.

## Verification

The survey is active for the approved audience, privacy settings match the communication, and response reporting follows the defined threshold.

## Variations

- US: demographic questions should be optional, job-related, and separated from individual employment decisions.
- Other countries: works council review, consent, data transfer, and employee monitoring rules may apply.
- Pulse survey: use fewer questions, shorter response window, and faster aggregate reporting.

## Safety & privacy

Medium risk because surveys may collect sensitive employee sentiment or demographic data. Be honest about anonymity, limit raw data access, suppress small groups, and never retaliate based on responses.
