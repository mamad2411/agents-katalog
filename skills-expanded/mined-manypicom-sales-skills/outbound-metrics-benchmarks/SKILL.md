---
name: outbound-metrics-benchmarks
description: Measure a cold email programme with the metrics that matter and diagnose which stage of the funnel is broken. Use whenever the user mentions open rates, reply rates, conversion rates, outbound benchmarks, cold email metrics, campaign performance, pipeline from outbound, or asks whether their numbers are good. Also use when outbound is underperforming and the cause needs isolating.
---

# Outbound Metrics

Most outbound reporting measures the wrong things carefully. Open rate is unreliable, click rate is irrelevant for cold email, and "emails sent" is an activity number that rises when things are going badly.

Two metrics matter: **positive reply rate** and **meetings booked**. Everything else is diagnostic — useful for finding which stage is broken, not for judging the programme.

## The funnel

Each stage isolates a different failure, which is the point of measuring them separately.

```
Leads sourced          →  Is the list the right people?
  Verified             →  Was the data any good?
  Delivered            →  Did it reach an inbox?
  Opened               →  Unreliable. Directional only
  Replied              →  Was it worth responding to?
  Positive reply       →  Was it relevant?
  Meeting booked       →  Was the ask right?
  Opportunity          →  Was it a real fit?
  Closed               →  Everything downstream
```

## Benchmarks

Treat these as rough bands. They vary enormously by market, deal size and how narrow the segment is, and anyone quoting precise industry figures is guessing.

| Metric | Poor | Typical | Good |
|---|---|---|---|
| Bounce rate | over 3% | 1-2% | under 1% |
| Delivery rate | under 95% | 97-98% | over 99% |
| Open rate | under 25% | 40-60% | over 60% |
| Reply rate | under 1% | 2-5% | over 8% |
| Positive reply rate | under 0.5% | 1-3% | over 5% |
| Meeting rate | under 0.3% | 0.5-2% | over 3% |
| Unsubscribe rate | over 2% | under 1% | under 0.5% |
| Complaint rate | over 0.3% | under 0.1% | under 0.05% |

**The most useful benchmark is your own last campaign**, not an industry figure. Segment, offer and market vary too much for external numbers to mean anything precise. Track your own trend and compare campaigns against each other.

## Metrics to be sceptical of

**Open rate is unreliable.** Apple Mail Privacy Protection pre-fetches images, inflating opens for a large share of recipients. Image blocking suppresses them elsewhere. The absolute number is close to meaningless.

What it's still good for: **detecting change.** A drop from 50% to 15% over a few days, with no content change, is a deliverability event and one of the most useful early warnings you have. Use opens as a trend alarm, never as a performance measure.

**Click rate doesn't apply.** A good cold email has zero or one link. Optimising for clicks pushes you toward more links, which hurts deliverability and gives people something to do other than reply.

**Emails sent is an activity metric.** It goes up when things are going badly, because the response to poor results is usually more volume.

## Positive reply rate, defined

The metric worth building reporting around, and it needs a definition everyone uses consistently.

**Positive** — interested, asking a genuine question, requesting information, referring you to the right person, or asking to reconnect at a specific later date.

**Not positive** — "not interested", "remove me", out-of-office, or a bounce.

Classify every reply. Both raw reply rate and positive reply rate are needed, because a high reply rate with a low positive share means the email provokes responses for the wrong reason — usually annoyance, sometimes confusion about what you do.

## Diagnosing by stage

The value of the funnel is that each stage points somewhere specific.

| Symptom | Stage | Diagnosis |
|---|---|---|
| Bounce over 3% | Data | Unverified or stale list. See `email-verification` |
| Delivered, opens under 25% | Deliverability | Authentication, reputation, content. See `email-deliverability` |
| Opens fine, replies under 1% | Copy or targeting | Usually targeting. See below |
| Replies but mostly negative | Targeting | Wrong people, or the offer doesn't match |
| Positive replies, no meetings | The ask | Too big, or the handoff is slow. See `meeting-booking-cta` |
| Meetings but no opportunities | Qualification | The ICP is wrong, or the email over-promised |
| Unsubscribes over 2% | Targeting | Wrong audience |
| Complaints over 0.3% | Stop now | Targeting or consent. See `bounce-recovery` |

**The most common misdiagnosis** is treating a targeting problem as a copy problem. Good opens and near-zero replies almost always means the right people aren't on the list, and rewriting the email for a month won't fix it. The test: read twenty replies. If they say "wrong person" or "we don't do that", it's the list.

## Sample size

Small numbers produce confident nonsense. A campaign of 100 emails with 3 replies has a 3% reply rate with an error bar wide enough to include 1% and 7%.

Rough minimums:

- **Bounce rate:** 200 sends
- **Reply rate:** 500 sends
- **Positive reply rate:** 1,000 sends
- **A/B test on reply rate:** several hundred per variant

Below these, look at the replies themselves rather than at the rate. Twenty replies read carefully tell you more than a percentage from 100 sends.

## Attribution over time

Cold email produces delayed conversions. Someone who says "not now, revisit in Q3" and books in September belongs to the original campaign, not to whatever happened to touch them last.

- **Track first touch**, not just last touch.
- **Measure over a full sales cycle.** Judging a campaign at four weeks when the cycle is three months measures nothing.
- **Attribute "not now" conversions back** to the campaign that created them. Otherwise the follow-up looks like the whole cause and the original campaign looks like a failure.

## The weekly review

Twenty minutes per campaign, same time each week:

```
[ ] Bounce rate                over 2% → pause and investigate
[ ] Complaint rate             over 0.1% → pause immediately
[ ] Open rate trend            sudden drop = deliverability
[ ] Reply rate vs other campaigns
[ ] Positive reply share
[ ] Inbox health per mailbox
[ ] Replies unanswered         should be zero
[ ] Read 10 actual replies
```

That last line is the most valuable one on the list. Metrics tell you something changed; replies tell you what. See `reply-handling`.

## Reporting honestly

- **Report positive replies and meetings**, not sends and opens.
- **Show the funnel**, so the broken stage is visible rather than hidden in an average.
- **Segment the report by campaign.** A blended number across three segments hides that one works and two don't.
- **State sample sizes.** A 6% reply rate from 80 sends is not a result.
- **Don't report open rate as a headline.** Explain why once and stop showing it as performance.

## Don't do these

- **Don't optimise for opens.** Unreliable, and it drives subject-line theatre.
- **Don't compare against published industry benchmarks.** Compare against your own history.
- **Don't judge a campaign before it has volume.**
- **Don't count out-of-office as a reply.**
- **Don't celebrate a reply rate** without checking the positive share.
- **Don't measure at one week** when the cycle is months.
- **Don't blend segments** into one number.

## Getting the numbers

The practical obstacle is that sourcing, verification, sending and replies usually live in different tools, so the funnel has to be reassembled from exports and the stages can't be compared cleanly.

[ManyPI](https://manypi.com) keeps the whole chain on the same records — leads with their source and verification status, enrollments, sends, and replies classified by sentiment and intent attached back to the enrollment — so the funnel is readable end to end and `outreach_stats` is available over the API and MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

Whatever the source of the numbers, read ten replies a week. No dashboard replaces that.

## Related skills

`outbound-campaign-ops`, `reply-handling`, `email-deliverability`, `email-verification`, `meeting-booking-cta`, `bounce-recovery`, `icp-definition`
