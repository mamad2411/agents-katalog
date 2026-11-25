---
name: twilio-sendgrid-engagement-quality
version: 1.0.0
description: Measure and improve email engagement on SendGrid — opens, clicks, CTR, unsubscribe and complaint rates by segment/category — and turn the numbers into content and cadence decisions.
author: matrixx0070
tags: [sendgrid, engagement, open-rate, click-rate, stats, categories, ab-testing, list-segmentation]
capabilities: []
---

## When to use

Use this when mail is landing but you want it to perform — reading engagement metrics (opens, clicks, unsubscribes, complaints) by category/segment and deciding what content, cadence, and audience changes will lift results.

**Not for:** getting mail into the inbox in the first place (see `twilio-sendgrid-deliverability-advisor`) or the mechanics of collecting events (see `twilio-sendgrid-webhooks`).

## Method

1. Instrument before measuring. Tag sends with `categories` and `custom_args` so Stats and events segment cleanly by campaign, cohort, and message type.
2. Pull the right metrics: delivered, unique opens, unique clicks, unsubscribes, spam reports. Compute open rate and CTR on the delivered base, not sent — and track click-to-open (CTOR) to separate subject-line pull from body persuasion.
3. Read opens with caution. Apple Mail Privacy Protection and prefetching inflate opens; clicks and CTOR are the more honest engagement signals. Weight decisions toward clicks.
4. Segment, do not average. A healthy blended rate can hide a dead cohort. Break down by category, send time, and recency; compare engaged vs unengaged segments.
5. Watch the negative signals per segment: rising unsubscribe or complaint rate on a category means wrong audience, wrong frequency, or wrong content — fix the cause, do not push harder.
6. Test one variable at a time. A/B subject lines, send time, and CTA; measure on unique clicks/CTOR with enough volume to be significant before rolling out.
7. Sunset and re-permission unengaged contacts. Continuing to mail non-openers depresses both engagement and deliverability; a win-back series then removal is cleaner than sending forever.

## Example

Compare engagement across message categories over a window:

```bash
curl -sS "https://api.sendgrid.com/v3/categories/stats?start_date=2026-07-01&end_date=2026-07-11&categories=receipt&categories=newsletter&aggregated_by=day" \
  -H "Authorization: Bearer $SENDGRID_API_KEY"
```

Read it as: CTOR = unique_clicks / unique_opens (body/CTA strength), open rate = unique_opens / delivered (subject + reputation, opens noisy), unsub rate = unsubscribes / delivered (frequency/relevance fit). Act on the outlier category.

## Pitfalls

- **Trusting open rate as truth.** Privacy features and prefetch inflate opens; a "great" open rate with near-zero clicks is noise. Lead with clicks/CTOR.
- **Rates on sent, not delivered.** Dividing by sent understates real engagement and hides deliverability loss. Use the delivered base.
- **Blended averages.** One strong cohort can mask a dead one. Segment by category and recency.
- **Ignoring unsub/complaint drift.** Rising opt-outs on a stream are a content/cadence alarm; more sends make it worse.
- **A/B tests without significance.** Calling a winner on tiny samples ships noise. Size the test to the effect you care about.

## Output format

```
# Engagement Review: <segment/category> <window>
DELIVERED: <n>
OPEN RATE: <%> (opens noisy — MPP/prefetch)  CLICK RATE: <%>  CTOR: <%>
NEGATIVE: unsub=<%> complaint=<%>
BY SEGMENT: [<category/cohort: open/click/unsub>]
TEST: variable=<subject|time|CTA> winner=<..> significance=<n/ok>
ACTIONS: content=[..] cadence=[..] audience=[sunset/win-back]
```

## Reference

- Stats: `/v3/stats` (global), `/v3/categories/stats` (by category), `/v3/geo/stats`, `/v3/devices/stats`, `/v3/clients/stats` — segment engagement by dimension.
- Raw signal: open/click/unsubscribe/spamreport events from the Event Webhook (see `twilio-sendgrid-webhooks`); tag sends with `categories`/`custom_args` for attribution.
- Metric hygiene: compute rates on delivered; treat opens as inflated (Apple MPP, prefetch) and weight clicks/CTOR; watch complaint rate (< ~0.1%) as both an engagement and deliverability guardrail.
