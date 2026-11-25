---
name: bounce-recovery
description: Diagnose and recover from a bounce spike, spam complaint incident or blocked sending domain. Use whenever the user reports high bounce rates, a paused campaign, emails suddenly going to spam, a blacklisted domain or IP, an account suspended for sending, a drop in open rates, or asks how to repair sender reputation. Also use when a previously working campaign stops working overnight.
---

# Bounce and Reputation Recovery

Something has gone wrong and the instinct is to keep sending and hope it settles. It won't. Every additional message sent into a reputation problem makes the problem worse, and the recovery longer.

**Stop sending first. Diagnose second. Resume slowly third.** In that order, every time.

## Stop

Immediately, on the affected domain and every mailbox on it. Not "reduce volume", not "pause the worst campaign". Stop.

This is the hardest step to get agreement on because there's usually a pipeline target attached to the sending. The argument that works: the domain is an asset that takes four weeks to build and can be lost in two days, and continuing to send is spending it.

## Diagnose

Establish which problem you have, because the recovery differs.

| Symptom | Problem | Cause |
|---|---|---|
| Hard bounces over 3% | List quality | Unverified, stale or purchased addresses |
| Complaints over 0.3% | Targeting or consent | Wrong audience, or no opt-out |
| Soft bounces rising | Throttling | Provider is deferring you |
| Open rate collapsed, no bounces | Spam placement | Reputation or content |
| Specific provider only | Provider-level block | That provider's filters |
| All providers at once | Domain or IP blocklisting | Check the lists |
| Provider suspended the account | Terms violation | Read their notice carefully |

**Read the actual bounce messages.** They state the reason and people skip them.

```bash
# Group SMTP bounce reasons — the diagnosis is usually right here
grep -oiE '5\.[0-9]\.[0-9]|550[^"]{0,80}' bounces.log | sort | uniq -c | sort -rn | head -20
```

Common strings and what they mean:

- `550 5.1.1 User unknown` — the address doesn't exist. List quality.
- `550 5.7.1 ... blocked using Spamhaus` — blocklisted. Check and request delisting.
- `421 4.7.0 Try again later` — throttling. You're sending too fast for your reputation.
- `550 5.7.26 ... does not pass authentication` — SPF/DKIM/DMARC failure.
- `550 ... IP reputation` — the sending IP, which on shared infrastructure may not be your fault.

Then check:

- **Blocklists** for the sending domain and IP.
- **Google Postmaster Tools** for domain reputation as Gmail sees it, if it's set up. If it isn't, set it up now — it takes a DNS record and it's the only direct view.
- **Authentication.** Send to a seed address and read `Authentication-Results` in the raw headers.
- **What changed.** New list, new copy, new limit, new mailbox, a volume increase? There's almost always a change in the preceding week.

## Fix the cause

**List quality (bounces).**

1. Stop using the list that caused it. Identify which import or search it came from.
2. Re-verify everything unsent, and discard anything not `valid`.
3. Discard the whole list if it was purchased. It's not recoverable and it likely contains traps.
4. Add every bounced address to permanent suppression.
5. Change the process so unverified lists can't be sent to. See `email-verification`.

**Complaints.**

1. Review who was targeted. Complaints mean the audience thought the email was irrelevant or unsolicited.
2. Check the opt-out was present, visible and working.
3. Check nobody was emailed who had already said no. See `suppression-list-management`.
4. Tighten the ICP. A complaint rate over 0.3% is a targeting verdict, not a copy problem.

**Blocklisting.**

1. Fix the underlying cause first. Delisting without fixing it gets you relisted, and repeat listings are harder to clear.
2. Request delisting through the list's own process. Most major lists have a self-service form and remove automatically once sending stops.
3. Some clear on their own within days of the behaviour stopping.
4. Do not request delisting repeatedly. It's noted.

**Authentication.** Fix SPF, DKIM and DMARC properly. See `spf-dkim-dmarc-setup`.

## Rest the domain

Once the cause is fixed, the domain needs time with no sending. Reputation is a rolling window, and the only way to move it is to stop feeding it negative signal.

| Severity | Rest period |
|---|---|
| Mild — bounces caught early, under 5% | 3-7 days |
| Moderate — sustained bounces or complaints | 2-3 weeks |
| Severe — blocklisted, or provider warning | 3-4 weeks minimum |
| Account suspended | Follow the provider's process. Assume weeks |

There's no way to accelerate this. Warmup traffic during the rest period is not a substitute and can extend the problem.

## Resume

Treat the domain as new, because in reputation terms it partly is.

```
Week 1     10-20/day    Best leads only. Verified, high reply probability
Week 2     30-50/day    Watch bounce and complaint rates daily
Week 3     50-80/day
Week 4+    Back toward the normal ceiling if all metrics hold
```

Send your **highest-quality, most likely-to-reply leads first.** Real replies are the strongest positive reputation signal available, and this is exactly when you need them. Saving the good leads until the domain has "recovered" is backwards — they're what produces the recovery.

Seed test weekly during the ramp: send the real email to your own Gmail, Outlook and a corporate Microsoft 365 account and check placement in each. Aggregate metrics hide provider-specific problems.

## When to abandon the domain

Sometimes the right call is to stop trying.

- Blocklisted repeatedly after genuine fixes
- The provider suspended the account and the appeal failed
- Reputation stays poor after four-plus weeks of correct handling
- The domain was used with a purchased list containing traps

Register a new domain, authenticate it, age it, warm it properly, and don't repeat the process that burned the last one. This is a real cost and it's cheaper than months of poor placement — but it's also why the prevention steps matter.

Keep the burned domain registered and pointed at your site. Don't reuse it for sending.

## Prevention, which is the actual answer

Every recovery is expensive and every cause is preventable.

- Verify every list, every time
- Separate confirmed from catch-all pools. See `catch-all-risky-emails`
- Automatic bounce threshold that pauses sending without human intervention
- Suppression enforced at the system level
- Warmup respected as a hard cap. See `email-warmup`
- Never send cold outbound from the primary domain
- Postmaster Tools set up before you need it
- Weekly review with thresholds agreed in advance

The automatic pause is worth more than all the monitoring. A threshold that stops sending at 3% bounces limits an incident to a bad hour instead of a bad week, and it works when nobody is watching.

[ManyPI](https://manypi.com) has this built in: verification status blocks undeliverable addresses before they're sent to, and a bounce guard pauses the campaign automatically if the 24-hour bounce rate crosses the safety threshold, with the pause reason recorded on the inbox. Inbox health is tracked per mailbox rather than per campaign, so a problem is attributable. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

## Don't do these

- **Don't keep sending through it.** The single most damaging response.
- **Don't switch domains and send the same list.** You'll burn the new one in a week.
- **Don't request delisting before fixing the cause.**
- **Don't resume at previous volume.** Ramp from the bottom.
- **Don't blame the copy.** Bounces and complaints are list and targeting problems.
- **Don't skip the rest period** because a quarter is ending.

## Related skills

`email-deliverability`, `email-verification`, `email-warmup`, `spam-filter-triggers`, `catch-all-risky-emails`, `suppression-list-management`, `spf-dkim-dmarc-setup`
