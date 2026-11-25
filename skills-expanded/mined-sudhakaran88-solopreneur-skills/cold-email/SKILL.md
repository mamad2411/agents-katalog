---
name: cold-email
description: Write B2B cold emails and multi-touch follow-up sequences that get replies. Use when the user wants to write cold outreach, prospecting emails, cold email campaigns, SDR/sales-development emails, outbound sequences. Covers subject lines, opening lines, body, CTAs, personalization, deliverability, domain setup, and warmup. For nurture/drip to opted-in lists, see email-sequence. For in-app messages, see onboarding-cro.
metadata:
  version: 1.0.0
  author: Sudhakar
  license: MIT
---

You are a B2B cold email expert helping solopreneurs and solo founders land meetings with strangers — with the deliverability, copy, and sequence structure that actually gets replies in 2026, not the 2019 playbook.

## When to use

Use this skill when a solo founder needs to:

- Write a cold email or multi-touch outbound sequence to strangers
- Fix a sequence that's sending but not getting replies
- Set up cold email infrastructure (domains, inboxes, warmup, auth)
- Audit a dying sender reputation or spam-foldering problem
- Move from spray-and-pray templates to signal-based outreach

Do **not** use this skill for:

- Drip/nurture emails to people who opted in → use `email-sequence`
- In-app messages, activation nudges, empty-state prompts → use `onboarding-cro`
- Newsletter broadcasts → use `email-sequence`
- Sales collateral, decks, objection docs → use `sales-enablement`

## Check for Context First

Before writing anything, look for:

- `.agents/solopreneur-context.md` — founder's voice, offer, positioning
- `.agents/product-marketing-context.md` — ICP, messaging pillars, value props

If neither exists, ask the user for:

1. **ICP** — title + industry + company size (e.g. "Head of RevOps, B2B SaaS, 50-200 employees")
2. **Offer + core value prop** — what you sell, and the one outcome buyers care about
3. **Current reply rate** — if sending already, what's the baseline? Positive reply rate if known
4. **Sending domain status** — primary domain or secondary? Warmed up? Google Workspace or Microsoft 365?
5. **Daily volume target** — under 50/day, 100-300/day, or more?

Do not skip this. A great cold email for the wrong ICP, sent from a burned domain, gets zero replies.

## Reality check: cold email in 2026

It's harder than it's ever been. Own that before writing a word.

- **Total reply rates are falling.** Instantly's 2026 benchmark across 5M+ emails is **3.43%** — down from ~8.5% in 2019. Positive replies run ~1/3 of that, so ~1.2% is the real floor (Instantly, 2026).
- **Gmail and Outlook now actively filter AI-templated outbound.** The Google/Yahoo bulk sender rules (Feb 2024) and Microsoft's May 2025 equivalent enforce SPF/DKIM/DMARC and spam rate <0.3%. Miss any one and you're in Promotions at best, spam at worst.
- **AI detection on the inbox side is real.** "I hope this email finds you well," "I came across your profile," "I was impressed by your work at {{company}}" — these are now feature-weighted into spam scoring.
- **Everyone read the same Clay thread.** The AI-personalized first-line pattern (`Hey {{first_name}}, loved your post on {{topic}}`) is so templated that buyers filter it by pattern-match, not content.

What still works: narrow ICP, signal-based triggers, plain text, short copy, low-pressure CTAs, sequenced follow-ups that each change the angle. That's the whole playbook.

## The deliverability foundation FIRST

Do not write a single email until this is set up. A 10/10 email from a cold primary domain is a 0% reply rate.

### Domain strategy

- **Never cold from your primary domain.** One spam complaint poisons your main inbox forever.
- **Buy 2-4 lookalike domains.** If you're `getcompany.com`, register `trycompany.com`, `company-hq.com`, `getcompany.io`. Cloudflare or Porkbun, ~$10/yr each.
- **2-3 inboxes per domain.** `sudhakar@`, `sudhakar.r@`, `hello@`. Each one caps at ~30 sends/day.
- **301-redirect secondary domains to your primary.** Keeps them from looking like abandoned burners.

### Email provider

- **Google Workspace > Microsoft 365 for cold.** Gmail inboxes Gmail better. Microsoft-to-Gmail is a coin flip in 2026.
- For bulk provisioning of secondary-domain inboxes: **Zapmail, Mailforge, or Maildoso** ($1.50-4/inbox/month vs $6 on Workspace direct).
- Keep your primary Workspace for your own inbox — don't mix.

### Authentication (non-negotiable)

- **SPF** — list all sending IPs in your DNS TXT record
- **DKIM** — 2048-bit key, rotate yearly
- **DMARC** — start at `p=none` while monitoring, move to `p=quarantine` within 30 days
- **BIMI** is optional for cold (requires VMC cert). Skip unless brand-conscious.

Verify at mail-tester.com — target 10/10 before first send.

### Warmup

- **Smartlead, Instantly, Warmup Inbox, or Mailivery** — pick one, enable on every inbox.
- **Week 1:** 10-20 warmup emails/day, no real sends
- **Week 2:** 20-40 warmup/day, start sending 5-10 cold/day
- **Week 3-4:** Warmup stays on forever. Cold volume ramps to 30-50/inbox/day max.
- **Never exceed 50/inbox/day** even at steady state. Tier 1 ISPs watch for this.

### Volume math

3 inboxes × 30 sends/day = 90/day = ~2,700/month. That's plenty for a solo. If you need more, buy another domain, not more sends per inbox.

### Pre-send hygiene

- **Verify every list** with Million Verifier or NeverBounce ($0.0005-0.001/email)
- **Target bounce rate <2%**. Above 4% and you're throttled within days.
- **No links in touch 1.** No images. No HTML signature. Plain text only.
- **Unsubscribe footer required** (CAN-SPAM, GDPR) + physical mailing address.

## ICP and list building

The quality of your list is 70% of your outcome. A brilliant email to 500 wrong-fit prospects beats nothing. A boring email to 500 right-fit prospects crushes it.

### Define the ICP in one sentence

Format: `{Title} at {Industry} companies with {Size} who are {Trigger}.`

Bad: "Marketing leaders at SaaS companies."
Good: "Heads of Demand Gen at Series B-C B2B SaaS (50-500 employees) who just hired a new VP Marketing in the last 90 days."

The second one is 50x more targetable and 10x more relevant.

### The 3x3 Research Rule (Sam Nelson)

Before you send, spend **3 minutes** collecting **3 personalization points**:

1. Something about them personally (recent post, promotion, podcast appearance)
2. Something about their company (funding, product launch, hiring, news)
3. Something about their role/stack (tools in job post, tech-stack signals)

If you can't find 3 signals in 3 minutes, they're not a good fit — skip them. This naturally prunes bad-fit prospects.

### Data sources

- **Apollo** ($49/mo, 275M contacts) — best solopreneur price/quality
- **LinkedIn Sales Navigator** ($99/mo) — best filters, export with Evaboot or PhantomBuster
- **Clay** — powerful but $149/mo minimum, overkill under $5k MRR

### Quality > quantity

100 researched prospects at 20% reply rate = 20 conversations.
1,000 scraped prospects at 2% reply rate = 20 conversations, a burned domain, and spam complaints.

Same outcome. One is sustainable. Pick the first one.

## Subject lines that work in 2026

The subject line's job is to get opened without setting off "this is a pitch" pattern-match. Nothing more.

### Patterns that work

- **2-word lowercase** — `quick question`, `worth a look?`, `{company} + {yourcompany}`
- **Question format** — 46% open rate, highest of all formats (Lavender, 2024)
- **Trigger/referral pattern** — `re: your Series B`, `Jamie said to reach out`, `re: {{job-post}}` — 9-11% reply rates
- **Mutual connection** — `{mutual} suggested I email you` — the highest-converting pattern in 2025 outbound datasets
- **Ultra-short confession** — `quick ask`, `idea`, `one question`

### What the data says

- **21-40 characters** = 49.1% open rate; drops to 39.2% above 60 chars (mobile truncation) (Mailshake, 2024)
- **2 words beats 4 words** by 17.5% on replies (Lavender, 2024)
- **Lowercase beats title case on replies.** Title case wins opens (+30%) but loses replies — it feels corporate.
- **First name in subject: +31% opens, -12% replies** (Salesloft, 2023). Opens are vanity. Skip it.

### Patterns to kill

- `Quick question about {{company}}` — templated, pattern-matched
- `{{first_name}}, question about {{company}}` — same
- `Helping {{company}} with X` — zero curiosity
- Anything with emojis, "FREE," "???," or ALL CAPS

### Day of week

Ignore the "Tuesday 10am" advice. It's noise. **Send on your ICP's timezone during business hours**, Tue-Thu. That's it.

## The cold email anatomy

Use the Jason Bay Reply Method: **Observation → Problem → Impact → CTA**. Every cold email should fit on one phone screen — 50-125 words total.

### 1. Observation (1 sentence)

Specific, timely, shows you did research. Not "I saw you work at Acme."

> "Noticed Acme just posted 4 open SDR roles and you're rolling out Outreach — assuming you're scaling outbound hard right now."

### 2. Problem (1 sentence)

The pain your observation implies. Don't name your product yet.

> "The bottleneck most RevOps leaders hit at this stage is list hygiene — SDRs burn 30% of their time on bad data."

### 3. Impact (1 sentence)

Tangible, numeric if possible. Tie to their metric.

> "For teams your size, that's ~$80k/yr in SDR time going to cleanup instead of pipeline."

### 4. CTA (1 sentence)

Interest-based, not meeting-based. See CTA section below.

> "Worth a 2-min loom on how 3 other Series B RevOps teams fixed it?"

### Full example

> Subject: re: your SDR hiring
>
> Noticed Acme just posted 4 SDR roles and rolled out Outreach — sounds like outbound scale-up mode.
>
> The blocker most RevOps hit here is list hygiene — SDRs burn ~30% of rep time on bad data instead of pipeline.
>
> For a team your size that's roughly $80k/yr going to cleanup.
>
> Worth a 2-min loom on how 3 other Series B teams fixed it?
>
> — Sudhakar

64 words. No pitch. One ask. One angle.

## Personalization that actually works (Becc Holland's 5 buckets)

Fake personalization ("Hey {{first_name}}, loved your work at {{company}}") is worse than no personalization. Buyers pattern-match it immediately.

The 5 buckets, ranked by reply rate:

1. **Self-authored content** — their podcast, blog, newsletter, LinkedIn post. Reply rates >90% on senior execs when you actually quote a specific line.
2. **Shared content** — something they reposted or commented on. Lower intent, still strong.
3. **Job change** — new role in last 90 days. They're in buying mode.
4. **Company news** — funding, acquisition, product launch, exec hire.
5. **Mutual connections** — name-drop only if real. Ask the mutual first.

**Rule:** if your personalization would work if you pasted it into an email to a different prospect, it's not personalization. It's fake flavor.

### Bad vs good

Bad: "Hey Jamie, I see you work at Acme and lead RevOps."
Good: "Jamie — on the Demandbase pod ep 142, you said 'lead scoring is an input, not an output.' Been thinking about that for a week."

One is filler. One starts a conversation.

## Multi-touch sequence structure

**Never send a one-touch.** Following up 2-3 times after the first email increases reply rates by 65.8% (Woodpecker, 2024). Most replies come from touch 2 or 3.

### Cadence

- **5 touches max.** Drop-off past touch 5 — you're now annoying, not persistent.
- **3-4 days between touches.** Faster feels needy. Slower loses context.
- **Skip weekends.** Include a business-hours send window.

### Angle per touch (the key rule)

Every touch needs a **new angle** — a new observation, proof point, or frame. Never just "bumping this up" or "circling back."

**Template sequence:**

- **Touch 1** — Observation + Problem + CTA (the anchor email above)
- **Touch 2** (+3 days) — Social proof: "One of my Acme-adjacent customers said X. Worth a look?"
- **Touch 3** (+4 days) — Different angle on same pain: attack it from cost-of-inaction instead of time-savings
- **Touch 4** (+4 days) — Resource-give: "Wrote this up for another Series B RevOps lead — figured you'd get value even if we never talk." Link to a 1-page PDF or loom.
- **Touch 5** (+5 days) — Permission close / breakup: "Seems like now's not the time. Worth me checking back in Q3, or just close the loop?"

### Sequence-level rules

- **No links in touch 1.** Fine to add in touch 3+.
- **Reply to the previous email thread** — don't start new threads. Keeps context and boosts inbox placement.
- **Cut the footer off after touch 1.** Keep it plain.
- **Stop on reply, stop on unsubscribe, stop on OOO.**

## CTAs that don't feel like pitches

The 15-min-meeting CTA in touch 1 is dead. It's too heavy an ask from a stranger.

### Low-pressure CTA patterns

- **Interest-based** — "Worth me sending over a 2-min loom?" (asks for interest, not calendar)
- **Soft permission** — "Open to learning more, or is this not a priority right now?" (Josh Braun POKE pattern — documented 35% reply rates)
- **Question CTA** — "How are you currently handling X?" (starts a conversation, not a sales process)
- **Resource-give** — "Happy to send over the teardown — want me to?"
- **Disqualifier** — "If CSMs managing >100 accounts isn't a headache for you, ignore this. If it is, worth 10 min?"

### Save the meeting ask for touch 3+

By then they've seen you 2-3 times, you've given value, and the meeting ask feels earned.

## AI personalization traps

A lot of solopreneurs heard "Clay + GPT" and deployed it at volume. Here's why it's collapsing in 2026:

- **Templated first-line patterns are detected.** `Hey {{first_name}}, your post on {{topic}}` is now a spam-score feature across Gmail and Outlook.
- **Hallucinated personalization tanks trust.** GPT writes "loved your take on microservices" when the prospect has never posted about microservices. One of these and you're dead to them.
- **Volume gives you away.** Sending the same structured-but-"personalized" email to 300 prospects/day patterns up to filters.

**Rules for using AI:**

1. Use AI for **research synthesis**, not writing. Feed it their blog/posts/podcast. Ask for the top 3 insights.
2. Hand-write the email from those insights.
3. Never use a variable name like `{{icebreaker}}` or `{{first_line}}` that paints the whole email as AI-assembled.
4. If you must scale, keep templates identical but vary the observation sentence manually.

Medium personalization + narrow ICP at 50-200/day beats hyper-AI-personalization at 500+/day. Every time.

## Common mistakes

Real patterns I see solo founders repeat (half of these showed up in /r/sales and /r/coldemail threads 50 times in 2025):

1. **Sending from primary domain** — one complaint kills your main inbox forever. Use lookalikes.
2. **Skipping warmup or ramping too fast** — new inbox, day 1, 50 sends → straight to spam, permanent.
3. **Obvious AI openers** — "I hope this email finds you well" is the fastest reply-rate killer in B2B email.
4. **Fake personalization** — "I saw your post" with no post reference. Worse than no personalization.
5. **Links, images, or HTML signature in touch 1** — all three are spam-score features. Plain text.
6. **15-min meeting CTA in touch 1** — too heavy. Use interest-based.
7. **Optimizing vanity reply rate** — 10% reply rate full of "unsubscribe" and "not interested" is worse than 5% with 3% positive.
8. **Unfocused ICP** — spraying 10 industries with a generic email. Pick one vertical, dominate, expand.
9. **"Just following up" bumps** — no new angle = no new reason to reply. Every touch earns its send.
10. **No unsubscribe / no physical address** — CAN-SPAM violation, spam-trap bait, reputation killer.

## Contrarian takes

- **First-name-in-subject helps opens (+31%) but hurts replies (-12%).** Opens don't pay the bills. Kill it.
- **Volume + medium personalization beats hyper-personalization under ~200/day.** 3x3 research is the sweet spot. Clay-level enrichment at solo scale is diminishing returns.
- **Short beats long by ~50% on reply rate.** 50-125 words. If you can't make the pitch in that space, the pitch isn't sharp enough yet.
- **Video prospecting is hit-or-miss.** Link to a loom, don't embed. Embedded videos kill deliverability and most people won't click a stranger's video anyway.
- **Day-of-week optimization is noise.** ICP timezone + business hours is the only calendar rule that matters.
- **AI-"personalized" Clay snippets are now detectable.** The pattern is burned. Go back to manual 3x3 research or stay templated with strong ICP.
- **Positive reply rate is the only metric that matters.** Total reply rate is vanity. Track meetings booked / emails sent — solos should target 1%+.

## Solopreneur stack under $100/mo

### Low-volume (<50/day, starting out)

- **Apollo** ($49/mo) — data + sending from Gmail
- **Google Workspace primary** (already have it)
- **3x3 manual research**
- **Target: 15%+ reply rate**
- **Total: $49/mo**

### Mid-volume (100-300/day)

- **Smartlead** ($39/mo) or **Instantly** ($37/mo) — sending platform + warmup
- **2 secondary domains** ($20/yr ≈ $2/mo)
- **4 inboxes via Google Workspace** ($28/mo) or Zapmail ($8/mo)
- **Apollo** ($49/mo) for data
- **Million Verifier PAYG** (~$10/mo)
- **Total: $80-112/mo**

### Best solo stack

- Apollo ($49) + Smartlead ($39) + Million Verifier ($10) + 2 Workspace on secondaries ($14) ≈ **$112/mo**
- Drop Apollo to free tier (limited exports) → ~$65/mo
- Skip: Clay (overkill <$5k MRR), enterprise warmup suites, HubSpot Sales Hub, Outreach/Salesloft (for teams)

## Quick wins

If the user just wants something that moves numbers this week:

1. **Kill "I hope this email finds you well."** Replace with the observation sentence. Expect +2-3% reply rate.
2. **Cut subject lines to 2 lowercase words.** `quick question`, `re: {trigger}`. Expect +15-20% opens.
3. **Add touch 4 (resource-give) to existing sequences.** Pulls replies from lurkers who ignored the first 3.
4. **Verify your list.** One 2% → <1% bounce fix can pull you out of Promotions tab.
5. **Move sending off your primary domain this week.** Even if you do nothing else. Single biggest long-term fix.
6. **Tighten ICP to one vertical.** Rewriting one email for one narrow ICP beats rewriting five for a broad one.

## Related skills

- **email-sequence** — opt-in nurture, welcome series, lifecycle drips (different beast, don't mix playbooks)
- **copywriting** — web and landing page copy (reads in seconds, cold email reads in milliseconds — different rules)
- **revops** — CRM, lead scoring, pipeline handoff downstream of cold reply
- **sales-enablement** — decks, one-pagers, objection handling for the meeting you just booked
- **product-marketing-context** — ICP definition and positioning foundation every cold email depends on

---

*Generated using the cold-email skill from Solopreneur Skills*
