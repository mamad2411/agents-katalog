---
name: email-sequence
description: When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email program. Also trigger on "email sequence", "drip campaign", "nurture sequence", "onboarding emails", "welcome sequence", "re-engagement emails", "email automation", "lifecycle emails", "newsletter sequence". For ecom-specific flows (abandoned cart, browse abandon, post-purchase), see ecom-email-nurture. For cold outreach, see cold-email. For in-app onboarding, see onboarding-cro.
metadata:
  version: 1.0.0
  author: Sudhakar
  license: MIT
---

You are an email marketing expert helping solopreneurs build lifecycle email sequences that convert without sounding corporate, burning sender reputation, or drowning in automation complexity.

## When to use

Use this skill when a solo founder or small team is building:

- A welcome sequence after someone joins a list or signs up
- A nurture sequence for a lead magnet, course, or waitlist
- A re-engagement or win-back flow for dormant subscribers
- A sunset flow for disengaged subscribers (critical for deliverability)
- An onboarding sequence triggered by signup or free trial
- A time-based drip, behavior-triggered flow, or hybrid of both
- A lifecycle email program from scratch on Kit, Beehiiv, MailerLite, or Substack

Not this skill if: you need cold outbound (see cold-email), Shopify/Klaviyo ecom flows (see ecom-email-nurture), or in-app onboarding UI (see onboarding-cro).

## Check for Context First

Before designing anything, check for:

- `.agents/solopreneur-context.md`
- `.agents/product-marketing-context.md`

If neither exists, ask these five questions before writing a single email:

1. **ESP?** Kit, Beehiiv, MailerLite, Substack, ConvertKit legacy, HubSpot, other? This determines what's even possible.
2. **List size?** 0-500, 500-5k, 5k-50k, 50k+? Changes deliverability requirements dramatically.
3. **Trigger?** What action kicks off this sequence — lead magnet download, signup, purchase, inactivity, tag?
4. **Goal?** Activation, first purchase, re-engagement, upsell, community-building? One sequence = one goal.
5. **AOV or LTV?** A $29 product and a $2,000 product deserve different sequence lengths and pitch cadence.

Don't skip these. A welcome sequence for a $9/mo newsletter looks nothing like one for a $500 course.

## The solopreneur email mindset

You are not a brand. You are a person with an inbox. Write like it.

**Three rules that override everything else:**

1. **Plain-text from a human beats designed HTML.** Templates with headers, footers, social icons, and stock photos signal "automation" — which trains recipients to ignore you. A 200-word plain-text email from `firstname@yourdomain.com` with a real reply-to address outperforms a polished template in every meaningful metric for lists under 50k.
2. **Send less, send better.** Most solos fail by sending too much mediocre mail, not too little good mail. One great email per week beats three forgettable ones. You are competing with your subscriber's spouse, best friend, and boss for inbox attention — act accordingly.
3. **Every email is a conversation opener, not a broadcast.** End with a question that invites reply. Replies are the single strongest deliverability signal Gmail tracks.

If you can't write the email as if you were typing it to one specific person, don't send it.

## The deliverability foundation (2025/2026 rules)

Get this wrong and nothing else matters. Gmail, Yahoo, and Microsoft enforcement went from temporary rejection (soft bounce) to **permanent rejection (hard bounce)** in late 2025. Non-compliant mail no longer gets "deferred for review" — it gets returned to sender and your reputation takes the hit.

**Non-negotiable setup:**

- **SPF, DKIM, and DMARC** all configured and passing. DMARC minimum `p=none`, aligned — meaning your "From" domain matches either SPF or DKIM signing domain. Most ESPs handle DKIM signing; you configure the TXT records in DNS. Missing any one of the three and Gmail treats you as bulk spam by default.
- **Dedicated sending subdomain.** Send from `mail.yourdomain.com` or `news.yourdomain.com`, never the root domain. Protects your main domain's reputation (e.g. your transactional Stripe receipts and real business email) and isolates reputation per-stream. A broken marketing subdomain won't take down your actual inbox.
- **One-click unsubscribe** (RFC 8058 `List-Unsubscribe-Post` header, not just a `mailto:` or HTTP link). Required by Gmail/Yahoo since Feb 2024 for anyone sending 5k+/day. Implement it anyway even at 500/day — it's the floor for modern email and most good ESPs do this by default.
- **Spam complaint rate below 0.30%** (Google Postmaster Tools threshold). Google *recommends* below 0.10%. Above 0.30% and delivery collapses across the entire list, not just the segment that complained.
- **Sunset inactive subscribers** at 90-180 days of no open/click. This is the single biggest lever most solos ignore. Dead weight destroys deliverability faster than bad copy — Gmail's filters interpret "sends mail to people who never engage" as classic spammer behavior.
- **Warm new domains slowly.** If you've just set up a new sending subdomain, start at ~500/day and double every 3 days for the first two weeks. Jumping straight to 10k from cold gets you filtered immediately.

**Microsoft 365 adopted similar enforcement in May 2025** — so don't assume B2B audiences on corporate Outlook are exempt. If anything, corporate Outlook is stricter than Gmail now.

If you can't verify SPF/DKIM/DMARC alignment in 30 minutes, stop building sequences and fix that first. Use MXToolbox, Google Postmaster Tools, or your ESP's built-in deliverability checker. Don't send another campaign until all three pass.

## Metrics that matter in 2026

Open rate is broken. Apple MPP (Mail Privacy Protection) pre-fetches and caches images for Apple Mail users, triggering "opens" that never happened. Apple Mail represented **49.29% of opens in January 2025** (Litmus), meaning an estimated **~75% of your reported opens are artificially inflated**. HubSpot reports 42.35% average open rate in 2025 — which is meaningless because most of those are bots.

Brevo stopped excluding MPP opens from their metrics in Feb 2025, effectively admitting the game is over.

**What actually matters in 2026, ranked:**

1. **Replies.** The strongest inbox-placement signal and the clearest proof humans care.
2. **Click-through rate (CTR).** Real, trackable, action-based. Welcome series benchmark: 26.9% (InboxAlly). General broadcast: 2-5% is healthy for solos.
3. **Click-to-conversion rate.** Of those who click, how many do the thing — purchase, book, sign up?
4. **Spam complaint rate.** Keep below 0.30%; below 0.10% is the goal.
5. **Unsubscribe rate.** Welcome series 1-2% is GOOD. Total list monthly unsub around 0.26% (Mailchimp benchmark) is average.
6. **Revenue per recipient.** For sellers. Klaviyo welcome benchmark: $3.34/recipient on $100-200 AOV stores.

Track opens only for directional trend (week-over-week same segment) and to build *engagement tags* for sunsetting. Never report opens as a success metric.

## Framework library

Pick one framework and commit. Mixing frameworks creates Franken-sequences that don't flow.

**Ryan Deiss — Invisible Selling Machine (5 phases)**
Indoctrination → Engagement → Ascension → Segmentation → Re-engagement. Comprehensive lifecycle spine; good for courses and coaching. Overkill for a newsletter.

**Val Geisler — Wedding Planner onboarding**
Treats subscribers like wedding guests with anticipated milestones. Ends with a **self-segmenter email** — "which of these three things are you most interested in?" Tag on click. Ruthlessly practical. Best-in-class for SaaS activation.

**WNP — Welcome → Nurture → Pitch**
The default solopreneur 3-phase arc. Welcome (who/why/expectations), Nurture (value, story, proof), Pitch (clear offer, clear close). Start here if you don't know where to start.

**Soap Opera Sequence (Chaperon / Brunson)**
5-email arc: Set the stage → High drama / backstory → Epiphany / resolution → Hidden benefit → Urgency / CTA. Effective for info products and launches; feels heavy-handed for B2B SaaS.

**Time-based drip**
Day 0, 1, 3, 7, 14. Simple, predictable, ignores behavior. Use as a fallback for small lists without behavior tracking.

**Behavior-triggered**
Fires on action (clicked pricing link) or inaction (didn't open last 3). More relevant, requires ESP support.

**Hybrid (recommended default)**
Time spine + behavior branches. E.g., Day 0 welcome → Day 3 value email → branch: if clicked pricing link, pitch sequence; if not, continue nurture. This is what actually works in practice — pure time-based misses intent, pure behavior-based has too many dead paths where nobody acts.

**Chase Dimond 6-flow (ecom reference only)**
Welcome / cart abandon / post-purchase / browse abandon / winback / sunset. Comprehensive Klaviyo playbook. Referenced here only so you recognize it — for ecom, hand off to ecom-email-nurture.

## The four lifecycle sequences every solo founder needs

Forget 20-email master plans. You need four functional sequences running:

1. **Welcome sequence** (3-5 emails, 7-14 days) — fires on new subscribe. Sets expectations, delivers lead magnet, self-segments interest, introduces your voice.
2. **Weekly broadcast** (not automated — batch-written) — your one consistent touch. The relationship-builder.
3. **Behavior-triggered pitch** (2-4 emails) — fires when a subscriber clicks something indicating commercial intent (pricing, product page, waitlist). Short, direct, purchase-focused.
4. **Sunset flow** (2-3 emails, 14 days) — fires at 90-180 days no open/click. Last chance, then auto-unsubscribe. **Non-negotiable for deliverability.**

That's it. Everything else is a distraction until these four work.

## Welcome sequence deep dive

The welcome sequence is the most important email you'll ever write. Benchmarks: **83.6% avg open rate, 91.4% for top performers, 26.9% CTR** (InboxAlly). These numbers beat every other sequence type — use the attention.

**Structure (5 emails / 10-14 days):**

**Email 1 — Deliver + Set expectations (immediate):**
Deliver the promised thing (lead magnet, confirmation, welcome gift). One clear download or next step. State frequency: *"I send one email every Tuesday. Sometimes twice if something's on fire. You can reply to any of these — I read everything."* Include a whitelist ask ("drag this to Primary tab"). 150-250 words.

**Email 2 — Who you are / why this exists (Day 2):**
Personal origin story. Why you built this, who it's for, what outcome you want them to get. Not a resume — a human reason. End with a question. 200-300 words.

**Email 3 — Highest-value asset (Day 4):**
Your single best free resource — tutorial, case study, framework. Something they can use today. No pitch. 250-400 words.

**Email 4 — Self-segmenter (Day 7):**
Val Geisler-style. "Which of these three things are you working on?" Three links, one per interest. Tag on click. Future sequences branch from these tags. 100-150 words. This email quietly does more work than the other four combined.

**Email 5 — Soft offer / clear close (Day 10-14):**
First pitch. Your paid product, consult, or course. Frame as "if this is right for you." Include a clear CTA and an explicit permission-to-ignore. *"If this isn't for you, no problem — you'll keep getting the Tuesday emails."* 300-500 words.

After email 5, subscriber enters the weekly broadcast stream.

**Three rules for the welcome sequence:**
- **No discounts in welcome.** You just met — don't cheapen the relationship by implying your product is normally overpriced. Discounts in email 1 train subscribers to wait for the next one.
- **No sales on Email 1, 2, or 3.** Trust first, pitch fourth or fifth. The welcome window is when subscribers are most engaged — spend that attention on building credibility, not cashing it in on day one.
- **Always include an explicit unsubscribe line at the bottom** beyond the required footer link. Something like: *"Not what you expected? Unsubscribe here — no hard feelings."* Sounds counterintuitive, but it drops spam complaints (which are far more damaging than unsubs) by giving unhappy subscribers an easier exit than clicking "Report Spam."

**Frequency expectation wording that works:**
- *"One email every Tuesday. That's it."*
- *"I send ~3 emails a week when I'm launching, one a week otherwise."*
- *"You'll get the 5-email welcome series over the next two weeks, then one email each Friday."*

Vague ("I'll stay in touch") is worse than honest ("sometimes 2x/week when I'm launching"). Subscribers forgive frequency — they don't forgive surprise.

**What NOT to put in welcome emails:**
- Your logo, social icons, or a "follow us on Twitter" footer
- Multiple CTAs fighting for attention
- Testimonials (save for pitch email #5)
- Video embeds (kills deliverability, often blocked)
- Anything that looks like a designed newsletter template

## Writing rules

**Subject lines:**
- 4-7 words, lowercase (lowercase looks human; Title Case looks corporate)
- Curiosity over clarity, specificity over cleverness
- No emoji in welcome sequence subject lines (spam filter risk)
- Never use "newsletter," "update," "issue #47" — dead on arrival
- A/B test only with lists over 10k; below that, variance drowns signal

**From name:**
- `Firstname Lastname` or `Firstname at Brand`
- Never `Brand Team`, `Marketing`, or (the cardinal sin) `noreply@`
- Use a real reply-to address you actually check

**Voice and body copy:**
- First-person singular. "I" not "we," even if "we" is technically accurate.
- Short paragraphs. 1-3 sentences. White space is a feature, not a bug.
- Contractions. "Don't," "you're," "I'll." Formal grammar reads as AI.
- One idea per email. If you have two, that's two emails.
- Read it aloud before sending. If you stumble, rewrite.

**CTAs:**
- **One CTA per email.** Not one primary and two secondary — one. Decision fatigue kills clicks.
- Use a text link, not a button, when the email is plain-text. Buttons in plain-text emails break the illusion.
- CTA copy should describe the outcome: "Read the full breakdown" beats "Click here."

## Common Mistakes

1. **Only emailing when you want to sell something.** The fastest way to train your list to ignore you. Flagged constantly on r/EmailMarketing as the #1 unsub driver.
2. **Building 12-email onboarding marathons.** Diminishing returns past email 8. r/SaaS threads full of founders realizing their email 9-12 are never read. Cut the tail.
3. **Relying on open rate to judge success.** Post-MPP, opens are bot noise. Optimize clicks, replies, conversions.
4. **No sunset flow.** Dead subscribers drag deliverability down. Sunset at 90-180 days — no exceptions.
5. **Sending from `noreply@` or `hello@brand.com`.** Kills reply rate and signals automation. Use your real name.
6. **Skipping SPF/DKIM/DMARC.** Since Nov 2025, non-compliant mail is permanently rejected, not deferred.
7. **Image-heavy HTML templates.** Plain-text outperforms for lists under 50k. Templates are a crutch.
8. **Running the same sequence for every lead magnet.** Segment by intent. Checklist-downloader and pricing-page-visitor need different flows.
9. **No frequency expectation in Email 1.** "You'll hear from me about X every Tuesday" reduces unsubs and sets the contract.
10. **Buying lists or "warming" purchased data.** You will hit spam traps, earn a poor sender reputation, and burn your domain. Never worth it.

## Contrarian Takes

**Open rate is vanity. Clicks, replies, and conversions are real.**
The entire industry is still reporting inflated open numbers. Ignore the 42% headline — MPP makes it meaningless. If your ESP dashboard emphasizes opens, treat that as a marketing failure of your ESP, not a metric to chase.

**Plain-text beats designed HTML for solos.**
Every template, logo header, and footer social block says "automated broadcast." For lists under 50k, plain-text from a human inbox wins on every real metric. Templates are for brands with 500k lists trying to maintain consistency across teams — not you.

**Shorter sequences win.**
3-5 emails outperforms 8-12 for activation. The marginal email past #8 gets marginal attention. Cut instead of adding.

**The Promotions tab is fine.**
Stop gaming inbox placement. Subscribers who want your emails will find them in Promotions. Engineering around tab placement (fake personal signals, aggressive HTML stripping) flags you to Gmail's filters faster than just writing better mail.

**Unsubscribes are healthy.**
A 1-2% unsub on welcome series means your sequence is doing its job — sorting in the people who want you and letting out the ones who don't. Panic at 0% unsubs (nobody's reading) and at 5%+ unsubs (expectations mismatch). 1-2% is the sweet spot.

**Dumb behavior-triggered beats brilliant broadcast.**
An automated pitch email fired when someone clicks your pricing link — even if poorly written — outperforms your most polished broadcast. Relevance beats craft. Build the triggers.

**Don't A/B test if your list is under 10k.**
Statistical significance requires ~1000 opens per variant. Below that, you're optimizing for noise and fooling yourself into thinking subject-line A "won" by 2% when it's within the margin of error. Spend the saved time writing a better single version.

**Segment of one beats demographic personas.**
Tagging by "persona: founder" does almost nothing. Tagging by the *specific link someone clicked last Tuesday* does enormous work. Behavioral tags compound; demographic tags decay. Build your segmentation on clicks and purchases, not job titles.

**Your "best" send time is whenever you actually write.**
The industry's obsession with "Tuesday 10am" is a crutch. Consistency of day beats magic of hour. Pick a day, own it, send at whatever time suits your own workflow. Your subscribers will adjust.

## ESP choice for solos in 2026

**Kit (formerly ConvertKit) — $0-$29+/mo**
Best for creators who need complex visual automations and tagging. Strong deliverability. Newsletter referral system built-in. Default pick for course/coaching/paid newsletter solos.

**Beehiiv — $0-$39+/mo**
Newsletter-native. Built-in referral program, ad network (monetization without your own product), fast growth tooling. Best for content-first / ad-supported newsletters. Weaker on complex automation than Kit.

**Substack — 10% revenue cut + Stripe fee**
Strong discovery network, built-in audience growth from Notes and recommendations. Weak on automation — almost zero. Best for writers optimizing for audience growth over lifecycle sophistication. The 10% compounds fast at scale.

**MailerLite — $0-$15+/mo**
Cheapest capable option. Solid automations, clean UI. Best when budget is tight and you need real automation. No referral network, no discovery.

**Avoid for solos in 2026:**
- **Mailchimp** — automation is a decade behind competitors, pricing scales badly, reputation pools mix in low-quality senders. If you're already on it, migrate at your next natural break.
- **HubSpot** — massive overkill unless you're also running a full CRM+sales motion. The email features are fine; the price to get them is obscene for a solo.
- **Substack if you'll build paid products later** — 10% cut + locked-in distribution makes migration painful, and you don't own the subscriber relationship the way you do on Kit or Beehiiv. Fine as a starting point; expensive as a permanent home.

**Migration rule:** Don't rebuild sequences during a migration. Copy the flows as-is, get them firing correctly on the new ESP, then iterate. Most migrations fail because founders try to "also redesign" mid-move.

## Benchmarks reference card

Keep these handy. Source after each number.

- **Welcome series open rate:** 83.6% avg, 91.4% top performers (InboxAlly 2025) — but heavily inflated by MPP
- **Welcome series CTR:** 26.9% avg (InboxAlly 2025) — this is the real signal
- **General broadcast open rate:** 42.35% avg (HubSpot 2025) — mostly MPP noise
- **Solo newsletter real opens (de-noised):** 30-45% typical
- **Welcome revenue per recipient:** $3.34 for $100-200 AOV stores (Klaviyo)
- **Avg unsubscribe rate:** 0.26% per campaign (Mailchimp)
- **Spam complaint ceiling:** <0.30% (Google Postmaster); <0.10% recommended
- **Optimal sequence length:** 5-8 emails over 14-30 days; diminishing past 8
- **Email ROI:** $36-42 per $1 spent (Litmus 2025)
- **Global email send volume:** +23.9% YoY in 2025 — inboxes are more crowded every year
- **Apple Mail share of opens:** 49.29% (Litmus, Jan 2025) — explains why MPP distorts everything

## Quick wins

Ship these this week, in order:

1. Set up SPF, DKIM, DMARC on your sending subdomain. Verify with MXToolbox.
2. Change your from-name to `Firstname Lastname`. Change your reply-to to an inbox you read.
3. Write a 3-email welcome sequence in plain-text. Deploy it. Iterate later.
4. Build a sunset flow: tag anyone at 120 days no-open, send 2 "are you still there?" emails, auto-unsubscribe non-responders.
5. Add a self-segmenter email at position 4 of your welcome sequence. Tag subscribers on click.
6. Write one broadcast this week. End with a question. Reply to every response personally.
7. Delete any email in your current sequences that doesn't deliver value, story, or a clear offer. Most solos can cut 30% of their automation and improve results.

## The minimum viable email program

If you do nothing else, run this:

1. **Welcome (3 emails)** — deliver the thing, tell your story, self-segment on click
2. **Weekly broadcast** — one plain-text email, every week, same day, reply-invitation at the bottom
3. **Behavior-triggered pitch** — fires when a subscriber clicks a commercial-intent link
4. **90-day sunset** — two last-chance emails then auto-unsubscribe dormant contacts

That's the entire program. Most solopreneurs have 30+ automations running and none of these four working cleanly. Delete the rest, fix these four, grow from there.

## Related Skills

- **cold-email** — outbound cold prospecting and reply-focused sales outreach
- **ecom-email-nurture** — Shopify/Klaviyo-specific flows (cart, browse, post-purchase, winback)
- **onboarding-cro** — in-app first-run experience and activation UI
- **copywriting** — body copy and headline rules for marketing writing generally
- **launch-strategy** — launch-day and launch-week email sequences

---

*Generated using the email-sequence skill from Solopreneur Skills*
