---
name: cold-email-starter-kit
description: Complete beginner-friendly cold email toolkit. Walks from zero to launched campaign — domain purchase, inbox setup, list building, copywriting, enrichment, and sending via Smartlead or Instantly. Use when setting up cold email for the first time, launching a new campaign, teaching someone cold email, or when you need an end-to-end guide that bundles strategy, copy, infrastructure, and API references in one place.
---

# Cold Email Starter Kit

A complete system for running cold email. Follow it top-to-bottom and you will have purchased domains, created warmed inboxes, built a lead list, written a campaign, and sent your first emails. Designed for beginners — no prior cold email experience required.

---

## What you'll build

By the end of the flow you'll have:
- 10-20 throwaway sending domains purchased on Dynadot
- 20-40 warmed sending inboxes on Zapmail
- A 2,000-person lead list from Prospeo
- A 4-step email sequence with variants and personalization
- A live campaign in Smartlead or Instantly sending daily
- Analytics and reply handling set up

Total cost month 1: ~$186. Recurring: ~$126/mo. See `references/00-getting-started.md` for breakdown.

---

## The end-to-end flow

1. **Deliverability basics** → understand why we buy domains + inboxes (read once)
2. **Strategy** → pick your offer and ICP
3. **Copywriting** → write the sequence
4. **Infrastructure** → buy domains, create inboxes
5. **List building** → pull prospects from Prospeo
6. **Enrichment (optional)** → add personalization data
7. **Launch** → upload to Smartlead or Instantly
8. **Analyze + iterate** → pull metrics back, tweak

---

## Before you start: prerequisites

**Technical:**
- Node.js 20+ (`node --version` should print v20 or higher) → install from nodejs.org
- `tsx` (`npm install -g tsx`)
- Terminal comfort (you know what `cd` and `cp` do)
- A text editor (VS Code recommended)

**Accounts (sign up before continuing):**
- Dynadot (domain registrar)
- Zapmail (inbox provider)
- Prospeo (lead source)
- Smartlead OR Instantly (sending platform — pick one)

**Budget:** ~$200 for your first campaign.

If any of the above is missing, start at `references/00-getting-started.md`. It has exact signup links and API-key retrieval instructions.

---

## Recommended entry point: /cold-email-kickoff

Before reading this tutorial, invoke `/cold-email-kickoff` from Claude Code. It's a shorter, guided flow that orchestrates ICP onboarding + lead magnet + campaign strategy + a consolidated campaign plan — and hands you to the right next skill based on whether you have infrastructure already. Most users should start there.

This starter kit is the deeper manual tutorial for learning each step in detail. Use it if you want to understand what's happening under the hood, or if you want to wire up a specific step manually.

## One-hour quick start

If you just want to launch your first campaign in a single session, stop reading this file and open `references/14-60-minute-tutorial.md`. It's a step-by-step walkthrough that assumes zero context and gives you exact commands to run.

## Fast path — skip manual juggling once you've done it once

If you already have inboxes set up and just want a campaign to run automatically, invoke `/auto-research-public`. It does all of this in one flow: scrapes the target company → Claude generates an ICP → Prospeo pulls leads → emails are verified → Claude personalizes each lead via parallel Task sub-agents → Smartlead campaign launches. ~20 minutes end-to-end, no skill-juggling.

Prerequisites for the fast path:
- Ran `/icp-onboarding` once (produces `client-profile.yaml`)
- Ran `/zapmail-domain-setup-public` + `/smartlead-inbox-manager` to have active inboxes
- Have `SMARTLEAD_API_KEY`, `PROSPEO_API_KEY`, `MILLIONVERIFIER_API_KEY` in `.env`

The walkthrough below is for **manual** first-timer learning. If you've done a campaign once before, jump straight to `/auto-research-public`.

---

## Reading order (for understanding)

The references/ folder is numbered in the order to read them the first time:

| # | File | What it covers |
|---|---|---|
| 00 | `00-getting-started.md` | Accounts, API keys, `.env`, verify, cost breakdown |
| 01 | `01-deliverability-fundamentals.md` | SPF/DKIM/DMARC, warmup, domain strategy, volume math |
| 02 | `02-campaign-strategy.md` | Generate 15-20 campaign ideas from your website |
| 03 | `03-campaign-copywriting.md` | Stepwise copywriting: direction → subject → body → final |
| 04 | `04-sequence-structure.md` | Timing, follow-ups, threading, A/B testing, spintax |
| 05 | `05-domain-and-inbox-setup.md` | Dynadot purchase, Zapmail inboxes, export |
| 06 | `06-list-building-prospeo.md` | Prospeo filters, state-by-state crawling, full-export |
| 07 | `07-enrichment-library.md` | Optional enrichments + pricing |
| 08 | `08-smartlead-api.md` | Smartlead API reference |
| 09 | `09-instantly-api.md` | Instantly API reference |
| 10 | `10-reply-handling.md` | Positive/negative/OOO/bounce playbook |
| 11 | `11-legal-compliance.md` | CAN-SPAM, GDPR, unsubscribe requirements |
| 12 | `12-launch-checklist.md` | Pre-flight QA |
| 13 | `13-troubleshooting.md` | Error matrix |
| 14 | `14-60-minute-tutorial.md` | Literal step-by-step first campaign |

---

## Decision tree — where am I and what do I read?

| If you're at this point... | Read this |
|---|---|
| "I don't know what cold email even is" | `01-deliverability-fundamentals.md`, then `02-campaign-strategy.md` |
| "I have a product, need campaign ideas" | `02-campaign-strategy.md` |
| "I have a campaign, need to write emails" | `03-campaign-copywriting.md` + `04-sequence-structure.md` |
| "I need inboxes but don't have them" | `05-domain-and-inbox-setup.md` |
| "I need a lead list" | `06-list-building-prospeo.md` |
| "My emails need personalization" | `07-enrichment-library.md` |
| "Ready to upload to Smartlead" | `08-smartlead-api.md` |
| "Ready to upload to Instantly" | `09-instantly-api.md` |
| "Got my first replies, now what?" | `10-reply-handling.md` |
| "Am I legal? GDPR? CAN-SPAM?" | `11-legal-compliance.md` |
| "Something's broken" | `13-troubleshooting.md` |

---

## Choose your sending platform: Smartlead vs Instantly

| Criterion | Smartlead | Instantly |
|---|---|---|
| Entry price (2026) | ~$39/mo, 2K leads | ~$37/mo, 1K leads |
| Free trial | 14 days | 14 days |
| Inboxes | Unlimited on paid plans | Unlimited on paid plans |
| API auth | Query param (`?api_key=`) | Bearer token header |
| API endpoint count | ~50 | ~150+ |
| Master inbox | Yes (strong) | Yes (Unibox, strong) |
| Built-in warmup | Free | Included |
| AI reply categorization | Yes | Yes (lead-labels) |
| Branching follow-ups | Limited | Yes (Subsequences, first-class) |
| Inbox rotation | Yes | Yes |
| Deliverability testing | External tools | Built-in (inbox-placement-tests) |
| Done-for-you inboxes | No | Yes (DFY orders) |
| Built-in lead enrichment | No | Yes (SuperSearch) |
| Smartlead-exclusive | Simpler for beginners | — |
| Instantly-exclusive | — | Subsequences + Inbox Placement + SuperSearch |

**Default recommendation for first-time users: Smartlead.** Simpler mental model, cheaper at small scale, enough power for your first 6 months. Migrate to Instantly if you outgrow Smartlead's advanced features.

You only need one. Pick now so you know which API reference to read later.

---

## Eric-proven defaults for your first campaign

Use these unless you have a specific reason to deviate:

- **20 domains × 2 inboxes = 40 sending inboxes** — enough to warm 2 weeks then send ~1,200/day
- **30 emails/day/inbox** (post-warmup) — never exceed
- **2,000 leads per campaign** — good statistical size to learn from
- **4-step sequence** — Day 0, Day 3, Day 7, Day 11
- **2-week warmup minimum** before any real sending
- **`.com` domains** (~$10-14 each on Dynadot) — default choice. Fall back to `.co` if .com is taken. Avoid `.info`, `.xyz`, and other cheap TLDs — they hurt deliverability.
- **2 inboxes per domain max** (above that hurts reputation)
- **50-90 word emails** — extend to 125 only if AI personalization justifies it
- **Preview email to yourself first** before any real send
- **Reply within 30 seconds** when a positive reply comes in — this looks 10x more human than replying hours later

---

## Common beginner mistakes (avoid these)

1. **Sending from your main domain.** Instant risk of blacklisting your real business mail. Buy lookalike throwaway domains (e.g. `trygrowth.co` to send on behalf of `growth.com`).
2. **Skipping warmup.** New inboxes sending cold = instant spam folder. Minimum 2 weeks warmup.
3. **Buying one $30 domain.** Buy 10-20 `.com` / `.co` lookalike domains instead. Diversity = deliverability.
4. **Writing emails longer than 90 words.** Nobody reads long cold emails.
5. **Using em dashes (—).** Gmail spam filters flag these. Use periods or commas.
6. **Sending without SPF/DKIM/DMARC.** Zapmail sets these automatically if you connect domains through it. Verify with `dig`.
7. **Treating a 0% reply rate in week 1 as failure.** Expect 2-5% reply rate over the full sequence; wins compound over follow-ups 2-4.
8. **Buying a list from a random "lead seller."** Use Prospeo — verified, legal, clean data.
9. **Emailing EU consumers.** B2B to EU is generally fine under legitimate interest, but consumer addresses are off-limits. See `11-legal-compliance.md`.
10. **Not handling replies fast.** Replies that sit for hours go cold. Set up notifications.

---

## When something breaks

Open `references/13-troubleshooting.md`. It has an error matrix keyed by symptom → cause → fix, plus diagnostic `dig`/`curl` commands for verifying setup.

---

## Next steps after your first campaign

Once you've shipped and have ~2 weeks of data:
- Read `10-reply-handling.md` and set up unified inbox monitoring
- Run `scripts/smartlead-pull-analytics.ts` (or the Instantly equivalent) to get a CSV of daily stats
- Rewrite the worst-performing email variant
- Launch campaign #2 in parallel (different targeting, same infrastructure)
- Study what's working and compound it

---

## Scripts included

All in `scripts/`. Run with `npx tsx scripts/<name>.ts`.

| Script | Purpose |
|---|---|
| `setup-env.sh` | Interactive `.env` bootstrap |
| `verify-credentials.ts` | Ping all APIs, print ✅/❌ table |
| `dynadot-generate-domains.ts` | Generate + availability-check domain candidates |
| `dynadot-bulk-purchase.ts` | Purchase a batch of domains |
| `zapmail-full-setup.ts` | NS switch → connect → inboxes → export (4-phase) |
| `prospeo-full-export.ts` | Full paginated Prospeo search to CSV |
| `smartlead-create-campaign.ts` | End-to-end campaign creation |
| `smartlead-add-leads.ts` | Batch lead upload |
| `smartlead-pull-analytics.ts` | Daily stats to CSV |
| `instantly-create-campaign.ts` | Instantly campaign creation |
| `instantly-add-leads.ts` | Instantly batch lead upload |
| `instantly-pull-analytics.ts` | Instantly daily stats to CSV |
| `enrichments/company-phone.ts` | Blitz company phone enrichment |
| `enrichments/ai-company-analysis.ts` | OpenRouter GPT-4o-mini company analysis |
| `enrichments/company-news.ts` | OpenWebNinja recent-news enrichment |
| `enrichments/linkedin-profile.ts` | RapidAPI LinkedIn profile enrichment |

Every script:
- Reads `.env` from the skill root
- Is safe to re-run (idempotent where possible)
- Confirms before spending money (domain purchases)
- Writes structured output to CSV/JSON you can inspect
- Fails loudly on errors, never silently

---

## Getting help

- Check `13-troubleshooting.md` first — it covers 90% of issues
- Re-read the platform comparison if you're on the wrong tool
- For copy: run the QA checklist in `03-campaign-copywriting.md`
- For lists: re-read filter advice in `06-list-building-prospeo.md`
- Cold email subreddits (r/coldemail, r/salesdevelopment) are friendly if you post redacted details

---

## A note on ethics

Cold email works best when it's actually useful. Skip consumer addresses, honor unsubscribes promptly, include a real address in your footer, and write something the recipient is glad they got.

That's most of what compliance comes down to in practice.

---

## What to do next

**If you're new to cold email:** run `/cold-email-kickoff` instead of going through this tutorial manually. It orchestrates the entire setup (ICP + lead magnet + strategy + plan) in one flow.

**If you want to do it manually:** follow `references/00-getting-started.md` through `14-60-minute-tutorial.md` in order. Each document points at the next.

**Or wait:** this is a tutorial. Either you're ready to learn, or you're not — no waiting.
