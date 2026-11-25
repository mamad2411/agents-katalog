---
name: email-warmup
description: Ramp a new sending domain or mailbox safely so it can reach inboxes at volume. Use whenever the user mentions email warmup, warming up a domain, warming an inbox, new sending domain, ramp schedule, warmup tools, warmup pools, or is about to start sending from a mailbox that hasn't sent before. Also use when a previously healthy mailbox needs re-warming after a pause or an incident.
---

# Email Warmup

A new mailbox has no reputation. Mailbox providers treat unknown senders with suspicion, and a new address sending 300 emails on day one confirms that suspicion. Warmup builds a track record by ramping volume slowly enough to look like a person who started using a new work address.

The cost of skipping it is not a slow start. It's a domain that never reaches inboxes and has to be replaced.

## The schedule

```
Day 1-3       10-15/day        Ramp begins
Day 4-7       +5/day           ~20-30 by end of week 1
Week 2        30-50/day
Week 3        50-80/day
Week 4        80-120/day
Week 5+       120-150/day      Ceiling for cold outbound
```

The three parameters that define it:

| Setting | Typical | What it does |
|---|---|---|
| Start volume | 10 | Emails allowed on day one |
| Daily increment | 5 | How much the cap grows each day |
| Ceiling | 150 | The number the ramp climbs toward |

For a fresh Google Workspace mailbox, start 10, increment 5, ceiling 150 is a reasonable and safe ramp. Faster than that is where people get burned, and the damage isn't visible for a week or two — by which point you've sent several thousand emails into spam folders.

**The effective cap is always `min(warmup cap for today, daily limit)`.** This has to be enforced by the sending system. If a campaign's daily limit can exceed the inbox's warmup cap, the warmup is decorative.

## Before day one

Warmup on an unauthenticated domain is wasted effort.

- [ ] Domain registered at least two to four weeks ago
- [ ] SPF, DKIM and DMARC all passing. See `spf-dkim-dmarc-setup`
- [ ] Domain redirects to a real website
- [ ] Mailbox has a real display name, a signature and a profile photo
- [ ] Custom tracking domain configured, if tracking at all
- [ ] MX records correct

An empty domain that resolves to nothing, sending mail from `sales@`, is a pattern filters recognise immediately.

## Warmup pools, honestly

Warmup tools work by putting your mailbox into a network of other mailboxes that email each other, open, reply and mark messages as important. It simulates engagement.

What's true about them:

- They do produce measurable early improvement in placement, and most cold email operations use one.
- Providers are increasingly good at recognising the pattern. The mail is formulaic, the network is closed, and the engagement is unnaturally uniform.
- A pool full of burned domains is worse than no pool. You're building an association with the other participants.
- Running warmup traffic forever, at a high ratio to real mail, is itself a signal.

A defensible position: use a reputable pool during the ramp, keep it at a modest ongoing level once real volume is flowing, and don't treat it as a substitute for the fundamentals. The strongest warmup signal available is real people replying to real email, which is what the actual campaign should produce.

## Manual warmup

Slower, free, and the signals are genuine. Worth doing alongside a pool, particularly in the first fortnight.

- Email colleagues, friends and existing contacts from the new address, and ask them to reply.
- Reply to those replies. Threaded conversation is a strong positive signal.
- Have recipients move the message out of spam and mark it as important where relevant.
- Subscribe to a few legitimate newsletters so the mailbox receives as well as sends. A send-only mailbox is an unusual pattern.
- Send at human times, in small numbers, with varied content.

## Mixing warmup with real sending

Start real campaign sends around day 8 to 14, at low volume, alongside continued warmup. The two together are better than either alone, because real recipients produce genuine engagement.

The order that works:

1. **Days 1-7:** warmup traffic only.
2. **Days 8-14:** warmup plus 10 to 20 real sends a day, to your *best* leads. Well-researched, high reply probability. Real replies at this stage are worth more than anything a pool produces.
3. **Week 3 onward:** real volume increasing along the ramp, warmup continuing at a reduced level.

Send your best-quality, highest-reply-probability leads first. It's counterintuitive — people save their best leads for when the domain is "ready" — but early engagement is exactly what makes the domain ready.

## Re-warming

A mailbox needs re-warming after:

- **Any pause over two weeks.** Reputation decays with inactivity.
- **A bounce or complaint incident.** See `bounce-recovery`.
- **A significant volume drop** followed by a planned increase.
- **Provider migration**, since the sending infrastructure changed.

Re-warming is faster than initial warmup on a domain with history — usually one to two weeks rather than four — unless the pause was caused by an incident, in which case treat it as a fresh start.

## Monitoring

Watch these during the ramp, and stop rather than push through a problem:

| Signal | Healthy | Stop and diagnose |
|---|---|---|
| Bounce rate | under 2% | over 3% |
| Complaint rate | under 0.1% | over 0.3% |
| Open rate | rising or steady | sudden drop |
| Spam placement in seed tests | inbox | junk on any major provider |
| Provider warnings | none | any |

**Seed test weekly.** Send the real campaign email to your own accounts on Gmail, Outlook and a corporate Microsoft 365 tenant, and check where it lands in each. Placement differs sharply by provider and the aggregate metrics hide it.

Set up Google Postmaster Tools before you start. It's free, requires a DNS record, and it's the only direct view of how Gmail sees the domain.

## Don't do these

- **Don't skip it** because the domain "seems fine". The damage isn't visible until it's done.
- **Don't ramp faster to hit a deadline.** The deadline gets missed either way, and you lose the domain too.
- **Don't warm up an unauthenticated domain.**
- **Don't run several campaigns through a warming inbox** with a combined volume above its cap.
- **Don't rely on a warmup pool alone.** Real engagement is what actually works.
- **Don't warm to 400 a day.** 150 per mailbox is the sensible ceiling for cold outbound. Add mailboxes instead. See `inbox-rotation-scaling`.
- **Don't warm and then sit idle.** Consistent volume maintains reputation; sporadic bursts damage it.

## Enforcement

Warmup only works if the sending system respects it under pressure, and pressure is exactly when someone raises a limit.

[ManyPI](https://manypi.com) makes warmup a property of the inbox — `warmup_enabled`, `warmup_start`, `warmup_increment` and `daily_limit` — and the scheduler uses the warmup-aware effective cap rather than the raw limit, so no campaign can out-send its inbox's ramp regardless of how its own limits are set. Inbox health is tracked per mailbox, and a bounce guard pauses sending if the 24-hour bounce rate crosses the threshold. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

## Related skills

`email-deliverability`, `spf-dkim-dmarc-setup`, `inbox-rotation-scaling`, `bounce-recovery`, `spam-filter-triggers`, `outbound-campaign-ops`
