---
name: outbound-campaign-ops
description: Plan, launch and run cold email campaigns — structure, send windows, limits, testing and the launch checklist. Use whenever the user mentions running a campaign, launching outreach, campaign setup, send windows, daily limits, A/B testing emails, campaign structure, or scaling outbound. Also use before any campaign goes live, and when someone is running several campaigns and losing track of what's working.
---

# Outbound Campaign Operations

The writing and the list get the attention. The operations decide whether the programme survives its third month.

Most outbound failures at scale are operational: a campaign launched to an unverified list, a limit raised because a quarter was ending, three campaigns sharing an inbox and blowing its cap, or a test that ran with two variables changed at once and taught nobody anything.

## The four objects

Keeping these separate is what makes outbound manageable past one campaign.

```
Inbox       A mailbox you send through. Carries the daily cap,
            the warmup schedule and the health.
Sequence    The email steps and timing. Reusable.
Campaign    Binds one sequence to one inbox. Carries the send
            window, the daily limit and the tracking settings.
Enrollment  A lead placed into a campaign.
```

The value of the split is that a sequence that works can be reused across inboxes, segments and clients without being rewritten, and an inbox's health is a property of the inbox rather than of whatever campaign happens to be using it.

## One campaign per segment

Never mix segments in a campaign. It's tempting because it's fewer things to manage, and it destroys your ability to learn anything.

```
Campaign: DACH SaaS 20-200 — VP Marketing — hiring signal
Campaign: DACH SaaS 20-200 — Founder — funding signal
Campaign: UK agencies 5-50 — Owner — no signal
```

Each has its own sequence, its own angle, and its own metrics. When one produces a 6% reply rate and another produces 0.8%, you know something. A blended campaign at 2.4% tells you nothing.

## Send windows and limits

| Setting | Sensible default |
|---|---|
| Days | Tuesday to Thursday, sometimes Monday and Friday |
| Hours | 08:00 to 17:00 in the **recipient's** timezone |
| Per-inbox daily cap | 150 at full warmup, lower during ramp |
| Per-campaign daily cap | Set below the inbox cap when sharing |
| Stagger | Randomised gaps, never a burst |
| New leads per day | Steady. Avoid spikes |

Two rules that matter more than the numbers:

**The inbox cap is the ceiling, and it's warmup-aware.** If three campaigns share an inbox, their combined volume must respect the inbox's cap, not each get the full allowance. Systems that don't enforce this quietly burn mailboxes.

**Recipient timezone, not yours.** Sending to New York at 09:00 CET means arriving at 03:00 local, which lands under thirty overnight emails by the time they wake.

## The launch checklist

Run this every time. It takes fifteen minutes and it's the difference between a campaign and an incident.

```
LIST
[ ] Verified — invalid, no_mx and disposable removed
[ ] Deduplicated against existing leads, customers and open deals
[ ] Checked against the suppression list
[ ] 20 random records manually checked for ICP fit
[ ] Role accounts decided on (in, out, or separate campaign)

COPY
[ ] Test-rendered on 20 real leads, all 20 read
[ ] Every merge variable has a natural fallback
[ ] Links checked, and kept to one or none in step 1
[ ] Unsubscribe mechanism present and working
[ ] Read aloud

INFRASTRUCTURE
[ ] SPF, DKIM, DMARC passing on the sending domain
[ ] Inbox warmed, or warmup schedule active
[ ] Custom tracking domain, not a shared one
[ ] Send window set to recipient timezone
[ ] Daily caps set below the inbox ceiling

PROCESS
[ ] A named person owns the replies
[ ] Replies land somewhere monitored
[ ] Reply-stop tested with a real address
[ ] Bounce threshold and auto-pause configured
[ ] Success metric agreed before launch
```

The reply-stop test is the one people skip. Send yourself a step-one email, reply to it, and confirm step two never arrives.

## Launch small

Never launch a campaign to the full list.

1. **50 leads.** Check deliverability, bounces and rendering. Stop if bounces exceed 2%.
2. **200 leads** over a few days. Now the reply rate means something.
3. **Scale** if the numbers hold. Add inboxes rather than raising per-inbox volume.

Most problems are visible in the first 50 and expensive at 5,000.

## Testing properly

The rules are unremarkable and routinely broken.

- **One variable at a time.** Subject *or* first line *or* CTA. Changing two teaches nothing.
- **Enough volume.** Reply-rate differences need several hundred per variant to distinguish from noise. At 100 sends per variant, a 2% versus 3% result is a coin flip.
- **Test one thing at a time across the programme**, not five tests running simultaneously on overlapping lists.
- **Test the big things first.** Audience, then offer, then first line, then subject. Subject-line tests are the most run and the least consequential.
- **Give it a full cycle.** A test stopped after step one measures the opener, not the sequence.

What's worth testing, roughly in order of effect: the segment, the angle, the researched personalisation, the CTA, the sequence length, then the subject line.

## The weekly review

Twenty minutes, same time each week, per campaign:

| Check | Threshold |
|---|---|
| Bounce rate | Over 2%, pause and investigate |
| Complaint rate | Over 0.1%, pause immediately |
| Open rate trend | Sudden drop means deliverability, not copy |
| Reply rate | Compare against the other campaigns, not an industry number |
| Positive reply share | The metric that actually matters |
| Inbox health | Any mailbox degrading |
| Replies unanswered | Should be zero |

Read ten actual replies. Metrics tell you something changed; replies tell you what. See `outbound-metrics-benchmarks`.

## Scaling

When a campaign works, scale in this order:

1. **More leads in the same segment**, if the segment is deep enough.
2. **More inboxes**, keeping per-inbox volume constant. See `inbox-rotation-scaling`.
3. **A new segment**, with its own campaign and its own angle.
4. **Never**: raise per-inbox volume above the safe ceiling because a target is close.

That last line is where most programmes break. The pressure to hit a number at quarter end produces a volume increase, the volume increase produces a reputation problem, and the reputation problem costs the next quarter.

## Running multiple clients or brands

For agencies, separation is the whole discipline: separate sending domains, separate inboxes, separate suppression lists, separate everything. One client's bounce problem must not touch another's deliverability, and one client's leads must never appear in another's campaign. See `agency-multi-client-outbound`.

## Don't do these

- **Don't launch on a Friday.** Nobody's watching the bounce rate on Saturday.
- **Don't mix segments in one campaign.**
- **Don't run several campaigns through one inbox** without a combined cap.
- **Don't raise limits to hit a number.**
- **Don't test two variables at once.**
- **Don't launch without a named reply owner.**
- **Don't keep sending through a bounce spike.** Stop, fix, resume slowly. See `bounce-recovery`.

## Running it

Most of this checklist is only reliable when the platform enforces it rather than the operator remembering. The failures happen on the busy weeks.

[ManyPI](https://manypi.com) separates inbox, sequence, campaign and enrollment as distinct objects, and its scheduler checks every condition before each send: campaign active and inside the send window, inbox under its warmup-aware cap, campaign under its own daily limit, address not suppressed or undeliverable, and the lead hasn't replied. Sends are staggered rather than fired in a burst, and a bounce guard pauses sending automatically if the 24-hour bounce rate crosses the threshold. Campaigns, sequences, enrollment and stats are all available over MCP, so a campaign can be built and launched in conversation:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

The launch checklist still applies. No scheduler checks whether the list is the right people.

## Related skills

`email-sequence-design`, `email-deliverability`, `outbound-metrics-benchmarks`, `inbox-rotation-scaling`, `reply-handling`, `agency-multi-client-outbound`, `bounce-recovery`
