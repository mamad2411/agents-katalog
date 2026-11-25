---
name: inbox-rotation-scaling
description: Scale cold email volume safely by adding mailboxes and domains rather than raising per-inbox limits. Use whenever the user mentions inbox rotation, multiple mailboxes, sending accounts, scaling outbound volume, how many emails per day, mailbox pools, secondary domains, or wants to increase sending capacity. Also use when a team wants to send thousands of emails a day.
---

# Inbox Rotation and Scaling

There's one rule for scaling cold email volume: **add mailboxes, never raise per-mailbox volume.**

A mailbox has a safe ceiling of roughly 150 emails a day at full warmup. That number comes from what a busy human plausibly sends, and exceeding it is the pattern providers are built to detect. Capacity comes from having more mailboxes at safe volume, not from pushing any one of them harder.

## The maths

```
Target: 1,000 cold emails per day

1,000 ÷ 150 per mailbox = 7 mailboxes minimum
7 mailboxes ÷ 3 per domain = 3 domains

Realistically:  4 domains × 3 mailboxes = 12 mailboxes
                12 × 120/day (below ceiling) = 1,440/day capacity
                Run at ~70% for headroom = ~1,000/day
```

Always build in headroom. Running every mailbox at its maximum leaves no room for a warmup pause, a mailbox going unhealthy, or a volume spike, and it means any incident immediately becomes a capacity problem.

## Two to three mailboxes per domain

More concentrates risk. If a domain gets flagged, every mailbox on it goes down together, so spreading across domains is what limits the blast radius.

```
outbound-a.com    sarah@ , tom@ , priya@
outbound-b.com    sarah@ , tom@ , priya@
outbound-c.com    sarah@ , tom@ , priya@
```

Use real names of real people who work there. `sales@`, `outreach@` and `noreply@` are recognisable as bulk-sending addresses and they're also harder for a recipient to answer, because nobody replies to a role account.

Each mailbox needs a display name, a signature, and ideally a profile photo. A mailbox with no identity sending to strangers is a pattern.

## Domain setup

Every sending domain, without exception:

- [ ] Registered and aged two to four weeks before sending
- [ ] Redirected to the main website, so it resolves to something real
- [ ] SPF, DKIM and DMARC configured and passing. See `spf-dkim-dmarc-setup`
- [ ] Its own custom tracking domain if tracking at all
- [ ] Warmed from zero. See `email-warmup`

**Never send cold outbound from the primary company domain.** Reputation damage there affects invoices, support and every customer conversation.

## How rotation should work

Distributing sends across mailboxes is not just round-robin. A correct implementation checks, per send:

1. Which mailboxes are **healthy** — not paused, not in a bounce incident
2. Which are **under today's warmup-aware cap**, not their raw limit
3. Which are **inside their send window** for the recipient's timezone
4. Whether this **lead has been contacted from another mailbox** already

Then it picks one and staggers the send with a randomised gap.

**The one-thread-one-mailbox rule matters.** Once a lead has been emailed from `sarah@outbound-a.com`, every subsequent step in that sequence must come from the same mailbox. A follow-up arriving from a different address breaks the thread, confuses the recipient, and looks exactly like what it is.

## Volume ceilings

| Scope | Safe ceiling |
|---|---|
| Per mailbox, per day | 150 at full warmup |
| Per mailbox, during warmup | Whatever the ramp allows today |
| Per domain, per day | ~450 across 3 mailboxes |
| Per campaign | Set below the combined inbox capacity |
| New mailbox, day one | 10-15 |

**Combined campaign volume must respect inbox capacity, not the other way round.** If three campaigns share a mailbox pool, their total has to fit inside the pool's warmup-aware capacity. Systems where each campaign gets its own limit independently will quietly burn mailboxes, and the failure isn't visible until placement drops.

## Cost, honestly

Scaling this way isn't free and the cost should be stated before someone commits to a volume target.

Per 1,000 emails a day, roughly: 4 domains, 12 mailboxes on a business email provider, warmup tooling, and the sending platform. Mailbox licensing is usually the largest line and it's per seat, per month, indefinitely.

Google Workspace and Microsoft 365 mailboxes have better deliverability than cheap SMTP providers and cost considerably more. That trade is usually worth taking — placement is the entire point — but it's a real number and it scales linearly with volume.

The question worth asking before scaling: **is the reply rate good enough to justify more volume?** Scaling a 0.5% positive reply rate to 1,000 a day produces five conversations and a lot of infrastructure. Fixing targeting first is almost always the better spend. See `outbound-metrics-benchmarks`.

## Monitoring a pool

Per mailbox, not just in aggregate. An aggregate bounce rate of 1.8% can hide one mailbox at 9%.

| Signal | Check |
|---|---|
| Bounce rate per mailbox | Weekly. Pause any over 3% |
| Complaint rate per mailbox | Weekly. Pause any over 0.3% |
| Open rate per mailbox | Weekly. An outlier low is a deliverability problem on that mailbox |
| Seed placement | Weekly, rotating across mailboxes |
| Warmup status | Any mailbox behind its ramp |
| Domain reputation | Postmaster Tools per domain |

**Rest a mailbox at the first sign of trouble.** Pausing one mailbox costs a twelfth of capacity for a week. Pushing through costs the mailbox and possibly the domain.

## Adding capacity ahead of need

Domains need two to four weeks of ageing plus four weeks of warmup before they're at full capacity. That's a six to eight week lead time.

So capacity has to be built before it's needed. A team that decides in March to triple volume for Q2 is already too late, and the usual response — raising limits on existing mailboxes — is exactly the thing that burns them.

Keep one or two spare warmed domains in reserve. They cost very little and they're the difference between a bounce incident being an inconvenience and being a shutdown.

## Don't do these

- **Don't raise per-mailbox volume above ~150.**
- **Don't put more than three mailboxes on a domain.**
- **Don't send from the primary domain.**
- **Don't switch mailboxes mid-sequence** for the same lead.
- **Don't let campaign limits exceed inbox capacity.**
- **Don't scale before the reply rate justifies it.**
- **Don't run every mailbox at maximum.** No headroom means no resilience.
- **Don't buy pre-warmed domains** from resellers. You don't know what they were used for.

## Implementation

The rotation logic is where this either works or quietly doesn't, because the failure mode — a campaign out-sending its inbox pool — isn't visible in any metric until placement drops weeks later.

[ManyPI](https://manypi.com) models the inbox as the object that carries the daily cap, the warmup schedule and the health score, with campaigns binding to inboxes rather than owning their own sending capacity. The scheduler checks the warmup-aware effective cap per inbox before each send, staggers rather than bursting, and pauses an inbox automatically when its 24-hour bounce rate crosses the threshold, recording the reason. Inboxes connect over Gmail/Outlook OAuth or SMTP, so the reputation and the replies stay on your own domains. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

The domain purchasing, ageing and DNS setup is still yours, and it's still the six-week lead time.

## Related skills

`email-warmup`, `email-deliverability`, `spf-dkim-dmarc-setup`, `bounce-recovery`, `outbound-campaign-ops`, `outbound-metrics-benchmarks`, `agency-multi-client-outbound`
