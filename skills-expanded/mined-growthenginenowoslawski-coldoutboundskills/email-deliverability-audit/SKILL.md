---
name: email-deliverability-audit
description: Diagnostic audit for a running cold email program. Checks domain authentication (SPF/DKIM/DMARC), inbox health/reputation from Smartlead, bounce rate by inbox type, and optionally runs a spam placement test via Smartlead's Smart Delivery API. Outputs markdown report + CSV with per-domain/per-inbox scores and concrete action items. Use when reply rates drop, when bounces spike, when onboarding someone else's account, or as a weekly/monthly health check.
---

# Email Deliverability Audit

**If your positive reply rate is dropping and you don't know why, start here.** Most of the time the problem is deliverability — your emails aren't reaching inboxes. This skill tells you what's broken.

## What it checks

| Layer | What | How |
|---|---|---|
| DNS auth | SPF, DKIM, DMARC present on each sending domain | `dig` commands |
| Inbox health | Warmup status, reputation, blocks, connection failures | Smartlead email-accounts API |
| Volume health | Daily sent trending, capacity utilization | Smartlead analytics |
| Send + reply rate per inbox | Sent count, reply count, reply rate % over lookback period | Smartlead campaign analytics |
| Bounce rate | Per-inbox and per-domain bounce rate over last 30 days | Smartlead campaign analytics |
| Spam placement | Real inbox-vs-spam test via Smartlead Smart Delivery | optional |

## The 1% rule — and the floors that gate it

**A healthy domain replies at 1% or better after 200 emails sent.** Below 1% on a fair sample,
something is broken, and if it stays broken the domain gets cancelled.

The 1% rule is **one number**: the same 1% that flags a domain here is the line that retires it in
`/inbox-lifecycle-manager`. What separates "flag" from "cancel" is not a softer second threshold —
it is the **floors**. Below a floor, the answer is "we don't know yet", which is a legitimate
output rather than a failure.

| Judgment | Floor before it counts |
|---|---|
| Reply rate | **200 sends** in the window |
| Bounce rate | **50 sends** |
| Bounce *composition* (which bucket) | **30 classified bounces for that domain** |
| Any cancel decision | **30 days of domain age**; unknown age counts as young |
| Placement test | 100-300 senders per test |

Reporting `0.00% reply` on 14 sends as a failure, or condemning a three-week-old domain that has
not finished ramping, is how healthy domains get killed.

| Reply rate (≥200 sends) | Reading |
|---|---|
| **≥ 1.5%** | Genuinely good. Leave it alone. |
| **1.0 - 1.5%** | Healthy. The rule passes. |
| **< 1.0%** | Burned. Hand to `/inbox-lifecycle-manager` — but only if it also clears the 200-send and 30-day floors. |
| **0 replies on ≥150 sends** | Decisive. A flat zero needs less sample than a low-but-nonzero rate. |

Possible causes when a domain is below the line (the audit's root-cause suggestions try to
pinpoint which):
- Emails landing in spam — run the spam placement test
- Domain reputation damaged — check DMARC reports and the bounce codes
- Copy is broken — re-run `/spam-word-checker`; confirm with a control-fleet placement test
- List is cold or wrong ICP — check bounce rate; if >3%, the list is the problem, not the domain
- Inbox hasn't warmed enough — check warmup status and domain age

### The domain-vs-copy isolation test

Low placement alone does not tell you whether the domain is burned or the copy is toxic. Run the
same copy from a known-good control fleet:

| Your fleet | Control fleet | Verdict |
|---|---|---|
| < 100% | ~100% | **Domain-side.** Your sending infrastructure is the problem. |
| < 100% | < 100% | **Copy.** Rewrite before you replace a single domain. |
| ≥ 85% | ≥ 85% | Neither. Infrastructure is fine — this is targeting or offer. |
| control untestable | — | Assume copy. It is cheaper to fix and reversible. |

## When to use

- Reply rate dropped by >30% week-over-week → run the full audit
- Bounces spiked above 2% → run auth + spam-placement checks
- Before scaling a campaign (make sure infrastructure is ready)
- Monthly as routine hygiene
- When taking over a Smartlead account you didn't set up

## Inputs

- `SMARTLEAD_API_KEY` (env)
- Optional: scope the audit
  - `--client-id=X` (for sub-clients)
  - `--campaign-id=X` (audit only one campaign's inboxes)
  - `--domain=example.com` (audit only one domain)
  - `--tag=active` (audit only inboxes tagged active)

## Steps

### 1. Pull the inbox inventory

```bash
npx tsx scripts/audit-inboxes.ts --all --out=/tmp/audit/inboxes.csv
```

Outputs per inbox: id, email, domain, warmup_status, reputation, max_warmup/day, sent_today, smtp_ok, imap_ok, is_blocked, tags.

### 2. Check domain authentication

```bash
npx tsx scripts/check-domain-auth.ts --from-csv=/tmp/audit/inboxes.csv --out=/tmp/audit/auth.csv
```

For each unique domain, runs:
```bash
dig TXT <domain> +short                             # SPF
dig TXT _dmarc.<domain> +short                      # DMARC

# DKIM has NO single selector. Present if ANY of these resolves:
dig TXT   google._domainkey.<domain>    +short      # Google / Gmail-backed — the common one
dig CNAME selector1._domainkey.<domain> +short      # Microsoft 365 — a CNAME, TXT returns nothing
dig CNAME selector2._domainkey.<domain> +short      # Microsoft 365, second key
dig TXT   default._domainkey.<domain>   +short      # generic fallback, frequently empty
```

⛔ **Never check `default._domainkey` alone.** It is empty on most real fleets, and a
`default`-only check reports every domain as "missing DKIM" — which routes genuinely burned
domains to "fix your DNS" and wastes a week republishing records that already exist. The script
tries all four and reports which one resolved.

Outputs: domain, spf_present, spf_strict, dkim_present, dmarc_present, dmarc_policy (none/quarantine/reject).

### 3. Pull sent + reply + bounce metrics per campaign/inbox

```bash
npx tsx scripts/audit-performance.ts --days=30 --out=/tmp/audit/performance.csv
```

Walks all active campaigns, pulls per-inbox analytics for the last 30 days. Output columns: `inbox_id, email, domain, type, tags, sent, replies, bounces, reply_rate_pct, bounce_rate_pct, flag_low_reply, flag_high_bounce`.

Flagged automatically:
- **`flag_low_reply = TRUE`** if sent ≥200 and reply_rate_pct < 1.0 (the 1% rule)
- **`flag_high_bounce = TRUE`** if sent ≥50 and bounce_rate_pct > 3.0

### 4. (Optional) Run a Smart Delivery spam placement test

```bash
npx tsx scripts/run-spam-test.ts --campaign-id=12345 --senders=100 --out=/tmp/audit/spam-test.json
```

This creates a real inbox-placement test via Smartlead's Smart Delivery API:
- Uses the only available provider pools: G Suite + Office365 (provider_ids 20, 21)
- Sends to ~200 seed mailboxes with 100 of your senders
- Waits for completion (5-20 min)
- Pulls: providerwise, spam-filter-details, dkim-details, spf-details, blacklist

Output shows: what % lands in Inbox vs Spam vs Promotions, broken down by your sender and the receiver provider. This is the ground truth.

### 5. Synthesize the report

Read the three CSVs (`inboxes.csv`, `auth.csv`, `performance.csv`) plus the spam-test JSON if you
ran one, and write the report by hand in this shape. There is no generator script; the synthesis
is the judgment call, and the template below is what it should look like:

```
# Deliverability Audit — 2026-04-17

## Summary

- 80 inboxes audited across 40 domains
- 3 inboxes blocked (4% of fleet)
- 5 domains missing DKIM
- 2 domains with DMARC policy=none (no enforcement)
- Fleet performance (last 30d):
    Sent:           42,384
    Replies:          523
    Overall reply rate: 1.23% (PASS — above 1% threshold)
    Bounces:           382
    Bounce rate:      0.90% (PASS — below 2%)
- 4 inboxes failed the 1% rule (sent ≥200, reply rate <1%)
- Spam placement (test run): 83% inbox / 14% spam / 3% tabs (ACCEPTABLE but not great)

## Critical issues (fix within 24h)

1. Domain trygrowth.co has no DMARC record. Add: v=DMARC1; p=none; rua=mailto:dmarc@trygrowth.co
2. Inbox sales@trygrowth.co blocked in warmup — likely flagged by warmup network. Rotate out of campaigns.
3. 12 inboxes have 0 daily sent today despite being in active campaigns. Check campaign schedule.
4. Inbox marketing@other.co failed the 1% rule: 347 sent, 1 reply (0.29% reply rate). Investigate:
   - Check spam placement for this inbox
   - Compare copy vs. a sibling inbox that's passing
   - Rotate inbox out if bad reputation is confirmed

## Warnings (fix within 1 week)

- 5 domains missing DKIM record at default._domainkey
- 3 inboxes reputation dropped "fair" → "bad"
- Spam filter trigger DKIM_INVALID firing 8% of the time — likely for a subset of domains

## Action items (prioritized)

1. [HIGH] Add missing DKIM records to: trygrowth.co, othergrow.co, ...
2. [HIGH] Rotate out blocked inboxes: sales@trygrowth.co, marketing@other.co, ...
3. [MED] Tighten DMARC to p=quarantine on all domains after 2 weeks of p=none observation
4. [MED] Replace 3 bad-reputation inboxes (tag them "retired", provision new)
5. [LOW] Re-run spam placement test after fixing DKIM issues
```

### 6. Act on the action items

Feed the action items into the right skills:
- Missing DKIM / SPF → `/zapmail-domain-setup-public` to reconnect domains through Zapmail
- Blocked inboxes → `/smartlead-inbox-manager` to tag "retired" and rotate in insurance
- Campaign schedule issues → Smartlead campaign schedule settings
- Bad copy flagged → `/spam-word-checker` on the campaign copy

## Interpreting the numbers

### Bounce rates
- **<1%** — Excellent. Healthy list.
- **1-2%** — Normal for cold. No action.
- **2-3%** — Yellow. Check list quality, might be old emails.
- **>3%** — Red. Verify the list (MillionVerifier), consider pausing.
- **>5%** — Stop immediately. You're damaging domain reputation.

### Spam placement
- **>90% inbox** — Great. Ship more.
- **85-90% inbox** — Healthy. This is the line a domain must clear to be considered good metal.
- **70-84% inbox** — Degraded. Look at spam-filter-details to see what's triggering.
- **<70% inbox** — Red, and a hard gate: do not attach this domain to a campaign. Pause and fix
  auth + copy before sending more.

Test with 100-300 senders. Smaller samples swing by double digits run to run.

### DMARC policies
- **None** — Acceptable for first 2 weeks of a domain's life. After that, tighten.
- **Quarantine** — Recommended long-term. Emails that fail auth land in spam.
- **Reject** — Strictest. Only use after 30+ days of clean `rua=` reports confirming all legitimate mail passes.

### Warmup reputation
- Smartlead reports reputation as 0-100. Higher is better.
- **≥98%** — required before promoting a reserve inbox into a live campaign.
- **80-98%** — sending is fine, but don't promote fresh reserves at this level.
- **50-80%** — keep warming, don't use for critical sends.
- **<50%** — don't send from this inbox; warmup peers aren't seeing it in their inboxes.

⚠️ **Warmup switched OFF is not a reputation of zero — it is no reading at all.** An inbox with
warmup off reports nothing, so it cannot be evaluated. Treat it as **held**: out of capacity, not
attached to campaigns, reported for a human. Do not silently turn warmup back on to make a number
appear — that rewrites the signal you are trying to measure.

## Common root causes

- **SPF too lax** — `v=spf1 +all` whitelists everyone. Use `v=spf1 include:zapmail.com ~all` or similar.
- **DKIM missing** — new domain, selector not published. Zapmail publishes at `default._domainkey` by default.
- **DMARC alignment failure** — From-domain doesn't match SPF/DKIM domain. Usually a misconfigured reply-to or a 3rd-party sender.
- **Too many inboxes per domain** — Gmail flags domains with >3-5 inboxes as suspicious. Keep it at 2/domain.
- **Judging a domain that is too young or too quiet** — under 30 days old or under 200 sends, the
  numbers cannot distinguish a burned domain from an unlucky week. This is not a root cause; it is
  the absence of evidence, and it is the single most common way a healthy domain gets killed.
- **Aggressive warmup ramp** — Jumping from 5 to 40/day in one week = flag. Ramp over 2-4 weeks.
- **Shared sending IP with spam traffic** — Zapmail/most providers use shared pools. If someone else on your IP spammed, you suffer. Not much to do except wait for pool rotation.

## What to do next

**If any flag fired:** `/deliverability-incident-response` → triage decision tree for whatever was flagged (low reply rate, high bounce, blocked inbox, etc).

**If a domain is confirmed burned:** `/inbox-lifecycle-manager` → the cancel/promote/buy decision, with the guards that stop you cancelling into a send shortfall.

**If all clean:** next Monday, run this again. This audit is the Monday task in `/cold-email-weekly-rhythm`.

**Or wait:** if you just applied fixes, wait 7 days then re-audit. Reputation changes propagate slowly.

## Related skills

- `/smartlead-inbox-manager` — execute the action items (rotate, retag, warmup settings)
- `/zapmail-domain-setup-public` — fix DNS/auth issues at the domain provider
- `/spam-word-checker` — check copy for spam-triggering phrases
- `/deliverability-test-public` — lighter-weight SMTP vs Gmail vs Outlook reply/bounce comparison
- `/inbox-lifecycle-manager` — acts on the verdict: cancel, promote reserves, plan the buy

## Scripts

- `scripts/audit-inboxes.ts` — pull + format inbox inventory
- `scripts/check-domain-auth.ts` — dig-based SPF/DKIM/DMARC checks
- `scripts/audit-performance.ts` — per-inbox sent / replies / bounces / rates from campaign analytics (applies the 1% rule)
- `scripts/run-spam-test.ts` — create + poll + pull Smart Delivery test

## References

- `references/dns-records.md` — SPF/DKIM/DMARC record templates + interpretation guide
