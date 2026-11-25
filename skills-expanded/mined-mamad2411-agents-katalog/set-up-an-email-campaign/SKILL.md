---
name: set-up-an-email-campaign
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

Prepare a compliant marketing email campaign for an approved audience.

## Preconditions

- You have approved email copy, subject line, sender, links, and audience definition.
- Recipients have given appropriate marketing consent or otherwise qualify under applicable rules.
- You have access to the email marketing platform.

## Steps

1. **Choose the campaign type.** [BRANCH: Mailchimp | generic] create a regular email campaign in Mailchimp, or create a standard marketing email in the platform. → *Expect:* a draft campaign exists.
2. **Select the audience.** Choose the approved list or segment and exclude unsubscribed, suppressed, or ineligible contacts. → *Expect:* the recipient count matches the campaign plan.
3. **Set sender details.** Enter the from name, reply-to address, and subject line. → *Expect:* inbox preview shows the intended sender and subject.
4. **Build the email.** Add approved copy, images, buttons, footer, and required unsubscribe link. → *Expect:* the email preview matches the approved creative.
5. **Check links and tracking.** Test each link and confirm tracking parameters if required. → *Expect:* every link opens the intended destination.
6. **Send a test email.** Send to internal reviewers and check desktop, mobile, and plain-text rendering if available. → *Expect:* reviewers receive a usable test.
7. **Schedule or prepare send.** Choose send time and time zone, or leave as draft for final approval. → *Expect:* the campaign is ready for approval or scheduled send.
8. **Send or schedule the campaign.** ⚠️ *Irreversible:* before sending or scheduling, confirm audience consent, unsubscribe link, sender, subject, and recipient count because mass email cannot be recalled reliably. → *Expect:* the platform shows sent, scheduled, or queued status.

## Decision points

- If consent is unclear → do not send; verify the source of the list first.
- If the recipient count is unexpectedly high → stop and inspect segment rules.
- If the campaign promotes a regulated offer → obtain required legal or compliance approval.

## Failure modes & recovery

- **F1 Missing unsubscribe:** detect the footer or compliance check fails → add the required unsubscribe link and retest.
- **F2 Wrong segment:** detect audience count or sample contacts are wrong → rebuild the segment before sending.
- **F3 Test rendering issue:** detect broken layout or clipped content → fix the template and resend a test.

## Verification

The campaign has the approved audience, sender, subject, content, working links, unsubscribe mechanism, and sent or scheduled status.

## Variations

- Newsletter: use a recurring template and update only the dated content.
- Product launch: coordinate timing with site availability and social posts.
- Internal announcement: use company distribution lists and internal policy instead of marketing consent rules.

## Safety & privacy

Medium risk because mass email can expose recipients and trigger compliance obligations. Follow CAN-SPAM and applicable consent rules, include a physical mailing address where required, honor unsubscribes, and avoid purchased or scraped lists.
