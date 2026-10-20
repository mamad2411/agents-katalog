---
name: a-b-test-an-email-subject-line
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

Run an A/B test comparing two email subject lines for the same campaign audience.

## Preconditions

- You have an approved email campaign and two approved subject lines.
- The audience is large enough for a meaningful split.
- Recipients are eligible to receive marketing email.

## Steps

1. **Open campaign testing.** [BRANCH: Mailchimp | generic] choose A/B Test or subject-line test in Mailchimp, or enable the platform's email experiment feature. → *Expect:* a test setup screen is open.
2. **Define variants.** Enter subject line A and subject line B while keeping sender, content, and audience unchanged. → *Expect:* only the subject line differs between variants.
3. **Choose audience split.** Set the test percentage or equal split according to campaign size. → *Expect:* each variant receives a comparable sample.
4. **Select winning metric.** Choose open rate, click rate, conversion, or manual review based on campaign goal. → *Expect:* the platform knows how to pick a winner.
5. **Set test duration.** Choose a duration long enough for recipients to open but short enough to send the winner on time. → *Expect:* test timing fits the campaign schedule.
6. **Check compliance and previews.** Confirm subject lines are truthful, not misleading, and render correctly. → *Expect:* both variants pass preview and compliance checks.
7. **Launch or schedule the test.** ⚠️ *Irreversible:* before launching, confirm audience consent, split, subject lines, and winner rules because test emails will send to real recipients. → *Expect:* the test shows scheduled, running, or sent status.
8. **Record the result.** After completion, note winner, metric, sample size, and learning. → *Expect:* future campaigns can use the result.

## Decision points

- If the list is small → run a full split and treat results as directional.
- If subject lines differ in offer or promise → revise so the test isolates subject wording.
- If timing is urgent → skip automated winner selection and send the approved best option.

## Failure modes & recovery

- **F1 Unequal content:** detect body or sender differs between variants → correct before launch.
- **F2 Inconclusive result:** detect tiny sample or close metric → avoid overclaiming and document as no clear winner.
- **F3 Misleading subject:** detect subject overstates the offer → replace it before sending.

## Verification

The test sends or schedules two approved subject variants to eligible recipients with a defined split, metric, duration, and recorded result.

## Variations

- Preheader test: vary only preheader text while keeping subject constant.
- Send-time test: isolate send time and keep subject identical.
- Lifecycle email: test on new entrants over time rather than a one-time batch.

## Safety & privacy

Medium risk because the test sends marketing email. Follow CAN-SPAM and applicable consent rules, include unsubscribe handling, and avoid deceptive subject lines.
