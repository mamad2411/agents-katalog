---
name: twilio-sendgrid-deliverability-advisor
version: 1.0.0
description: Diagnose and improve inbox placement on SendGrid — authentication alignment, IP/domain reputation, warm-up, bounce/complaint thresholds, and content that trips filters.
author: matrixx0070
tags: [sendgrid, deliverability, inbox-placement, reputation, ip-warmup, dmarc-alignment, blocklist]
capabilities: []
---

## When to use

Use this when mail is being sent but under-performing — landing in spam, bouncing, or throttled — and you need a structured read on why and what to change to get into the inbox.

**Not for:** first-time account/domain setup (see `twilio-sendgrid-account-setup`) or interpreting engagement metrics for content quality (see `twilio-sendgrid-engagement-quality`).

## Method

1. Confirm authentication alignment first — it is the most common root cause. Verify SPF passes, DKIM signs with your domain, and DMARC aligns (the `From` domain matches the authenticated domain). Misalignment sends good mail to spam regardless of content.
2. Check DMARC posture. At `p=none` you only monitor; move toward `p=quarantine`/`p=reject` once aggregate reports confirm all legitimate sources align.
3. Read the numbers: pull Stats and reputation. Watch bounce rate (keep well under ~2%), spam-complaint rate (keep under ~0.1%), and the account/IP reputation score. These are the thresholds receivers punish.
4. Assess IP strategy. On shared IPs you inherit pool reputation; on a dedicated IP you own it and must warm up — ramp volume gradually over days/weeks so receivers build trust. A cold dedicated IP blasted at full volume gets throttled.
5. Segment by engagement. Sending to unengaged/old addresses drags reputation; send to recent openers/clickers first and sunset dead contacts.
6. Audit content: excessive links, image-only mail, spammy phrasing, URL shorteners, and unbranded (`sendgrid.net`) links depress placement. Use link branding and balanced text/HTML.
7. Check blocklists and seed-test. If reputation dropped suddenly, check major blocklists for your domain/IP and run inbox-placement seed tests across providers.

## Example

Pull the signals that most often explain spam-foldering:

```bash
# Global stats for the window (bounces, spam reports, delivered)
curl -sS "https://api.sendgrid.com/v3/stats?start_date=2026-07-01&aggregated_by=day" \
  -H "Authorization: Bearer $SENDGRID_API_KEY"
```

Then triage: DKIM/SPF/DMARC aligned? bounce < 2%? complaint < 0.1%? links branded? If all pass yet Gmail spam-folders, the cause is usually low engagement or a cold IP — segment to engaged recipients and slow the ramp.

## Pitfalls

- **Blaming content when auth is broken.** Rewriting copy will not fix DMARC misalignment. Verify SPF/DKIM/DMARC before touching the message.
- **Blasting a cold dedicated IP.** No warm-up means receivers see a sudden stranger at volume and throttle/block. Ramp gradually.
- **Ignoring the complaint rate.** Even ~0.1% spam complaints signals receivers to demote you. Prune and honor opt-outs aggressively.
- **Sending to stale lists.** Old, unengaged addresses generate bounces and spam-trap hits that tank reputation. Sunset non-openers.
- **Unbranded links.** `sendgrid.net` click links share pooled reputation; brand your link domain.

## Output format

```
# Deliverability Review: <domain/stream>
AUTH: SPF=pass DKIM=pass(domain) DMARC=aligned policy=<none/quarantine/reject>
REPUTATION: score=<n> bounce=<%> complaint=<%>  [thresholds: bounce<2%, complaint<0.1%]
IP: <shared|dedicated> warmup=<stage/NA>
LIST: engagement segmentation=<yes/no> stale sunset=<yes/no>
CONTENT: link-branding=<on/off> flags=[<image-only|shorteners|...>]
BLOCKLIST: <clear | listed on ...>
TOP FIXES: 1) ... 2) ... 3) ...
```

## Reference

- Stats/reputation: `/v3/stats`, `/v3/categories/stats`, and reputation surfaced in the console; suppression signals via `/v3/suppression/*`.
- Authentication: SPF + DKIM (from Domain Authentication) plus DMARC alignment (`From` domain = authenticated domain) is the deliverability foundation; DMARC aggregate reports (`rua`) reveal misaligned sources.
- Receiver thresholds to respect: bounce rate < ~2%, spam-complaint rate < ~0.1%; dedicated IPs require gradual warm-up.
- Event Webhook bounce/spamreport data (see `twilio-sendgrid-webhooks`) is the raw feed for these diagnostics.
