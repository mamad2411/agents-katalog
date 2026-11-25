---
name: twilio-email-deliverability-advisor
version: 1.0.0
description: Improve SendGrid inbox placement with SPF/DKIM/DMARC, domain authentication, IP warmup, list hygiene, and 2024 bulk-sender rules.
author: matrixx0070
tags: [sendgrid, deliverability, dkim, dmarc, reputation, compliance]
capabilities: []
---

## When to use

Use this when SendGrid email is landing in spam, bouncing, or failing Gmail/Yahoo bulk-sender requirements. Use it to set up SPF/DKIM/DMARC and domain authentication, decide between shared and dedicated IPs, plan IP warmup, and keep sender reputation healthy through list hygiene and engagement. Use it before scaling volume so you don't torch a new domain/IP.

**Not for:** the mechanics of constructing and sending a message — use twilio-email-send. SMS/voice — use twilio-webhook-architecture / twilio-reliability-patterns.

## Method

1. Authenticate the sending domain first. In SendGrid Settings → Sender Authentication → Authenticate Your Domain, generate CNAME records and add them at your DNS host. This publishes DKIM keys and SPF alignment via SendGrid-managed subdomains. Nothing else matters until this passes.
2. Verify SPF. Ensure the return-path/envelope domain's SPF includes SendGrid (`include:sendgrid.net`) and that you have not exceeded the 10-DNS-lookup SPF limit. SPF must align with the from-domain for DMARC.
3. Confirm DKIM signing. Domain authentication installs DKIM CNAMEs; verify SendGrid shows the domain as "verified" and that outbound mail is DKIM-signed with an aligned `d=` domain.
4. Publish DMARC. Add a `_dmarc` TXT record starting at `p=none` with `rua=` reporting, monitor aggregate reports, then tighten to `p=quarantine` and `p=reject` once SPF/DKIM alignment is proven. Decision point: don't jump to `p=reject` before confirming all legitimate streams align.
5. Choose IP strategy. Low/irregular volume (under ~100k/month sustained) → shared IP pool (SendGrid manages reputation). High, steady volume → dedicated IP for control, but you now own its reputation and must warm it.
6. Warm up a dedicated IP. Ramp volume gradually over ~2–4+ weeks (e.g. hundreds → thousands → tens of thousands/day), sending to your most engaged recipients first so mailbox providers build positive reputation. Cold-blasting a new IP gets it throttled/blocklisted.
7. Enforce list hygiene. Send only to opted-in addresses; process bounces (suppress hard bounces immediately), honor unsubscribes and spam reports, and remove chronically unengaged recipients. SendGrid suppression lists (bounces, blocks, spam reports, unsubscribes, invalid) are authoritative — respect them.
8. Separate streams. Put transactional and marketing mail on different subusers/subdomains/IP pools so a marketing reputation hit doesn't sink password resets. Use distinct authenticated subdomains (e.g. `t.example.com` vs `mail.example.com`).
9. Meet Google/Yahoo 2024 bulk-sender rules (senders >~5000/day to Gmail/Yahoo): authenticate with SPF AND DKIM, publish DMARC (`p=none` minimum with aligned from), provide one-click unsubscribe (RFC 8058 `List-Unsubscribe`/`List-Unsubscribe-Post`) honored within 2 days, and keep the Postmaster Tools spam complaint rate under 0.3% (ideally <0.1%).

## Method (verification)

Monitor via the SendGrid Event Webhook and Stats (delivered/bounce/spamreport rates), Google Postmaster Tools (domain/IP reputation, spam rate, auth pass rates), and DMARC aggregate reports. Treat rising bounces/complaints as a stop-and-fix signal.

## Example

```dns
; SPF on the envelope/return-path domain
example.com.            TXT   "v=spf1 include:sendgrid.net -all"

; DKIM — installed as CNAMEs by SendGrid domain authentication
s1._domainkey.example.com.  CNAME  s1.domainkey.uXXXXXX.wlYYY.sendgrid.net.
s2._domainkey.example.com.  CNAME  s2.domainkey.uXXXXXX.wlYYY.sendgrid.net.

; DMARC — start at p=none with reporting, then tighten
_dmarc.example.com.     TXT   "v=DMARC1; p=none; rua=mailto:dmarc@example.com; adkim=s; aspf=s; pct=100"
```

```
Required List-Unsubscribe headers for one-click (Gmail/Yahoo 2024):
List-Unsubscribe: <https://u.example.com/unsub?id=..>, <mailto:unsub@example.com>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

## Pitfalls

- **Sending before domain authentication passes.** Without aligned DKIM/SPF you fail DMARC and the 2024 bulk rules outright — mail is spam-foldered or rejected. Authenticate the domain first.
- **SPF 10-lookup overflow.** Too many `include:` chains produce `permerror`, silently breaking SPF and DMARC alignment. Keep lookups ≤10; flatten if needed.
- **Jumping straight to DMARC p=reject.** A strict policy before all legitimate streams align will bounce your own mail. Ramp none → quarantine → reject while reading `rua` reports.
- **Cold-blasting a dedicated IP.** New IPs have no reputation; high initial volume triggers throttling and blocklisting. Warm up gradually to engaged users.
- **Mixing transactional and marketing.** A marketing complaint spike on a shared reputation can block password resets. Separate subusers/subdomains/IP pools.
- **Spam rate over 0.3%.** Gmail Postmaster complaint rate above 0.3% causes rate-limiting/blocking; ignoring unsubscribes compounds it. Suppress unengaged and honor opt-outs within 2 days.

## Output format

```
DOMAIN AUTH: <verified|pending>  SPF=<pass|fail>  DKIM=<pass|fail>  DMARC=<none|quarantine|reject, aligned?>
IP STRATEGY: <shared | dedicated>  warmup=<n/a | day X of ramp>
BULK RULES (Gmail/Yahoo): auth=<ok|gap> one-click-unsub=<yes|no> complaint-rate=<%>
LIST HEALTH: bounce=<%> spamreport=<%> suppressions-respected=<yes|no>
STREAM SEPARATION: transactional=<subdomain/IP> marketing=<subdomain/IP>
ACTIONS: <prioritized fixes>
```

## Reference

- **Domain authentication (SendGrid):** publishes DKIM CNAMEs on a SendGrid-managed subdomain and provides SPF alignment via the return-path; shown as "verified" in Sender Authentication. Preferred over single-sender verification for anything beyond testing.
- **SPF:** TXT `v=spf1 include:sendgrid.net -all`; hard 10-DNS-lookup limit; must align with the from/return-path for DMARC `aspf`.
- **DKIM:** cryptographic signature with aligned `d=` domain; installed via CNAMEs by domain authentication; satisfies DMARC `adkim`.
- **DMARC:** `_dmarc` TXT, `v=DMARC1; p=none|quarantine|reject; rua=mailto:...; adkim=s|r; aspf=s|r`. Requires at least one of SPF/DKIM to pass AND align. Start at `p=none`.
- **Shared vs dedicated IP:** shared = SendGrid-managed reputation, good for lower volume; dedicated = your reputation, needs warmup, justified at sustained high volume.
- **IP warmup:** gradual volume ramp (weeks) to engaged recipients to build mailbox-provider trust.
- **Suppression lists:** bounces (hard/soft), blocks, spam reports, unsubscribes, invalid emails — SendGrid auto-suppresses; do not resend.
- **Google/Yahoo Feb 2024 bulk-sender requirements (>5000/day):** SPF + DKIM, DMARC with aligned from, RFC 8058 one-click unsubscribe honored ≤2 days, spam complaint rate <0.3% (target <0.1%) in Postmaster Tools, valid forward/reverse DNS (PTR) on sending IPs, TLS for transmission.
- **Monitoring:** SendGrid Stats + Event Webhook (delivered/bounce/dropped/spamreport/open/click), Google Postmaster Tools, DMARC aggregate (`rua`) reports.
- **Compliance:** CAN-SPAM (physical address + unsubscribe for commercial mail), GDPR/consent for EU recipients, honor opt-outs promptly.
