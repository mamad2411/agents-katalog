---
name: send-a-customer-satisfaction-survey
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 15min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Send a customer satisfaction survey to an appropriate customer group and collect responses.

## Preconditions

- You have approved survey questions, audience, sender, and timing.
- Customers are eligible to receive the survey under communication and consent rules.
- You have access to a survey or email platform.

## Steps

1. **Open the survey tool.** Create a new survey or open the approved survey template. → *Expect:* survey questions are editable or ready.
2. **Confirm questions.** Check rating scales, required fields, free-text prompts, and thank-you page. → *Expect:* the survey asks only necessary questions.
3. **Set audience.** Upload or select the approved customer segment and suppress unsubscribed or ineligible contacts where required. → *Expect:* recipient count matches the plan.
4. **Write the invitation.** Add clear purpose, estimated completion time, privacy note, and survey link. → *Expect:* customers know what they are being asked to do.
5. **Test the survey.** Submit a test response and verify routing, scoring, and confirmation. → *Expect:* the response appears in results.
6. **Send or schedule.** ⚠️ *Irreversible:* before sending, confirm audience, consent basis, survey link, and privacy language because customer messages cannot be recalled reliably. → *Expect:* the survey invitation is sent or scheduled.
7. **Monitor responses.** Check delivery, bounce, response count, and any urgent negative feedback. → *Expect:* responses are being collected and routed.

## Decision points

- If the audience includes recent support cases → coordinate with support before sending.
- If the survey collects sensitive data → add a privacy review and limit free-text prompts.
- If incentives are offered → state terms clearly and follow promotion rules.

## Failure modes & recovery

- **F1 Broken survey link:** detect test or customer reports failure → pause sends and replace the link.
- **F2 Wrong audience:** detect unintended recipients in the sample → stop the campaign and correct the segment.
- **F3 Response not saved:** detect test submission missing from results → fix survey routing before launch.

## Verification

The approved survey invitation is sent or scheduled to the intended eligible audience, and a test response appears in the results.

## Variations

- Post-purchase survey: trigger after delivery or service completion.
- NPS survey: use the standard 0-10 scale and route detractors for follow-up.
- In-app survey: use product targeting and frequency caps instead of email lists.

## Safety & privacy

Medium risk because surveys contact customers and may collect personal feedback. Follow CAN-SPAM and applicable consent rules for email invitations, disclose data use, and avoid requesting unnecessary sensitive information.
