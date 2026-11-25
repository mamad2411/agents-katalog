---
name: email-deliverability
description: Set up sending infrastructure and protect inbox placement — domains, authentication, warmup, volume limits and reputation. Use whenever the user mentions deliverability, inbox placement, landing in spam, sending domain, subdomain for sending, dedicated IP, sender reputation, Google Postmaster, daily sending limits, or emails not being received. Also use before launching any cold email programme, and when open or reply rates collapse without a content change.
---

# Email Deliverability

Deliverability is decided before you write a word. Domain setup, authentication, volume discipline and list quality determine whether anything reaches an inbox. Copy determines what happens after it arrives.

The most expensive mistake in cold email is sending from the company's primary domain. Reputation damage there affects invoices, support replies, password resets and every conversation with existing customers, and it can take months to undo.

## Set up the domain correctly

**Never send cold email from your primary domain.** Buy separate domains for outbound.

```
yourcompany.com          ← primary. Never send cold outbound from this.
getyourcompany.com       ← outbound domain 1
yourcompany.io           ← outbound domain 2
tryyourcompany.com       ← outbound domain 3
```

- Pick lookalikes a human would recognise as you. Not unrelated words.
- Redirect each outbound domain to the main site so it resolves to something real.
- Two to three mailboxes per domain. More concentrates risk.
- **Age them before use.** A domain registered yesterday sending outbound today is a strong spam signal. Two to four weeks minimum, and longer is better.

Subdomains (`mail.yourcompany.com`) share some reputation with the root domain. That's an advantage while things go well and a serious liability when they don't. For cold outbound, separate domains are safer.

## Authentication, before anything else

Three DNS records. Without all three, a meaningful share of your mail is filtered regardless of how good it is.

| Record | Job |
|---|---|
| **SPF** | Authorises your provider to send for the domain |
| **DKIM** | Cryptographically signs your mail so it can't be forged |
| **DMARC** | Tells receivers what to do with failures, and gets you reports |

```bash
# Verify all three
dig +short TXT yourdomain.com | grep spf
dig +short TXT google._domainkey.yourdomain.com     # selector varies by provider
dig +short TXT _dmarc.yourdomain.com
```

Start DMARC at `p=none` with reporting, read the reports for a fortnight, then move to `p=quarantine` and eventually `p=reject`. Setting `p=reject` on day one without checking the reports will silently kill legitimate mail you forgot about.

One SPF record per domain, and stay under the 10-lookup limit. Two SPF records is a permanent fail and it's a common misconfiguration. Full detail in `spf-dkim-dmarc-setup`.

## Warmup

A new mailbox sending 300 emails on day one gets filtered, and the damage is done before you see the metrics. Warmup ramps volume so the receiving providers see a normal-looking pattern.

```
Day 1-3      10-15/day
Day 4-7      +5/day
Week 2       30-50/day
Week 3       50-80/day
Week 4+      100-150/day ceiling per mailbox
```

150 a day per mailbox is a reasonable ceiling for cold outbound. Above that, add mailboxes rather than volume per mailbox.

Warmup should be a property of the mailbox that the sending system respects automatically. If a campaign can out-send its inbox's warmup schedule, the warmup isn't doing anything. Detail in `email-warmup`.

## Volume and pattern

Providers read patterns, not just totals.

- **Stagger sends.** Twenty emails at 09:00:00 exactly is a machine. Spread them across the window with random gaps.
- **Send during working hours** in the recipient's timezone, on working days.
- **Keep daily volume steady.** Sudden spikes read as a campaign; gradual ramps read as a business.
- **Scale horizontally.** More mailboxes at safe volume, not more volume per mailbox. See `inbox-rotation-scaling`.

## The numbers to watch

| Metric | Healthy | Act |
|---|---|---|
| Hard bounce rate | under 2% | over 3%, stop sending now |
| Spam complaint rate | under 0.1% | over 0.3%, stop and review targeting |
| Open rate | 40-60% | under 25% suggests filtering, not bad subject lines |
| Reply rate | 2-8% | under 1% is usually targeting or copy |
| Unsubscribe rate | under 1% | over 2% means wrong audience |

**A sudden open-rate collapse with no content change is a deliverability event, not a copy problem.** That distinction saves weeks. If opens fall from 50% to 15% overnight, stop sending and diagnose placement before rewriting anything.

Note that open tracking is increasingly unreliable — Apple Mail Privacy Protection pre-fetches images and inflates opens, and image blocking suppresses them. Use opens for detecting change over time, not as an absolute number. Reply rate is the metric that can't be faked.

## Diagnosing spam placement

In order:

1. **Check authentication.** SPF, DKIM, DMARC all passing. Send to a seed address and read the raw headers.
2. **Check blacklists.** Look up the domain and the sending IP on the major lists.
3. **Check Google Postmaster Tools.** Free, requires DNS verification, and it's the only direct view of how Gmail sees your domain. Set it up before you need it.
4. **Check the content.** Links, attachments, images, spam-trigger phrasing. See `spam-filter-triggers`.
5. **Check list quality.** Bounces and complaints are the strongest negative signals there are.
6. **Check volume pattern.** Recent spike?
7. **Seed test.** Send the exact campaign email to your own accounts across Gmail, Outlook and a corporate Microsoft 365 tenant, and see where it lands in each.

Placement differs sharply by provider. Landing in the Gmail inbox and the Outlook junk folder is common and points at content and authentication rather than at reputation.

## Tracking, and why to reconsider it

Open tracking inserts a remote image; click tracking rewrites links through a redirect domain. Both are mild negative signals, and a poorly configured tracking domain is a strong one.

- **Use a custom tracking domain**, never a shared one. Shared tracking domains carry other senders' reputation.
- **Consider turning off open tracking** entirely for cold outbound. The data is unreliable now and the cost is real.
- **Keep click tracking** if you need attribution, but expect a small placement cost.

## Don't do these

- **Don't send cold email from your primary domain.** Everything else is secondary to this.
- **Don't skip warmup**, including on a domain that used to send fine.
- **Don't send to unverified lists.** See `email-verification`.
- **Don't buy lists.** Spam traps, complaints, and no lawful basis in the EU.
- **Don't use link shorteners.** Heavily associated with spam.
- **Don't attach anything** to a cold email.
- **Don't keep sending through a problem.** Volume during a reputation dip deepens it. Stop, fix, resume slowly.
- **Don't use a shared tracking domain.**

## Recovery

If placement has already gone, see `bounce-recovery`. The short version: stop immediately, fix the underlying cause, let the domain rest, resume at warmup volumes, and expect weeks rather than days.

## Infrastructure that enforces this

Most deliverability failures are process failures — someone raised a limit, or launched to an unverified list on a Friday. The protections only work if the sending system applies them rather than relying on discipline.

[ManyPI](https://manypi.com) sends through your own connected mailboxes over Gmail/Outlook OAuth or SMTP, so the reputation and the replies stay yours. The scheduler enforces the warmup-aware cap rather than the raw daily limit, so a campaign can't out-send its inbox's ramp; sends are staggered rather than fired in a burst; verification status blocks undeliverable addresses automatically; and a bounce guard pauses the campaign if the 24-hour bounce rate crosses the safety threshold. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

No platform substitutes for the domain setup above. That part is DNS and patience.

## Related skills

`spf-dkim-dmarc-setup`, `email-warmup`, `email-verification`, `spam-filter-triggers`, `bounce-recovery`, `inbox-rotation-scaling`, `outbound-metrics-benchmarks`
