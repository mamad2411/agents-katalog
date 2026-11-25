---
name: competitive-intelligence-brief
description: "Produce a structured competitive intelligence brief covering recent competitor moves, pricing changes, product launches, funding, hiring signals, and strategic implications. Use when someone asks for a CI brief, competitive update, what competitors are doing, competitive landscape update, monitor competitors, or track competitor changes. Different from competitor-analysis (which is a one-time deep-dive on a landscape) — this skill is designed for ongoing, recurring CI briefs that track movement over time. Supports weekly, monthly, and ad-hoc formats. Commands: /ci-brief, /competitive-brief, /competitor-update"
---

# Competitive Intelligence Brief

This skill produces a structured, recurring CI brief. It tracks competitor
movement — product, pricing, GTM, hiring, funding — and translates signals
into strategic implications for your product decisions.

The key distinction: `competitor-analysis` is a one-time landscape snapshot.
This skill is a recurring radar sweep.

Read the full file before producing anything.

---

## Step 1 — Brief Configuration

On first use, gather:

1. **Who are the 2–5 competitors to track?** (Primary and secondary)
2. **What's your product / company context?** (So implications are relevant)
3. **What cadence?** Weekly, monthly, or ad-hoc
4. **What signals matter most?** (Pricing, product launches, hiring, funding,
   GTM moves, regulatory actions, or all of the above)
5. **What's the output for?** (Internal team, leadership, board, or personal
   reference)

Store these as the brief's standing configuration. On subsequent uses,
reference them — don't re-ask.

---

## Brief Structure

Produce the following sections in every CI brief. Sections with no new signals
should say "No material changes this period" — never pad.

---

### Section 1 — Period Snapshot

**Brief period:** [Start date] — [End date]
**Competitors tracked:** [List]
**Signal sources:** [Product pages, app stores, job boards, press, LinkedIn,
earnings calls, pricing pages, social listening — note which were checked]

**Period in one line:** [The single most strategically important thing that
happened in the competitive landscape this period]

---

### Section 2 — Product and Feature Moves

For each competitor with new product activity:

**[Competitor name]**

What launched / changed: [Specific feature, product, or UX change]
Where observed: [App store release notes / product blog / user reports]
Target segment: [Who this appears aimed at]
Strategic read: [What problem are they solving? What does this signal about
their roadmap direction?]
Our response: [Ignore / Monitor / Accelerate our equivalent / Reframe our
positioning]

If no product changes: "No new product activity observed."

---

### Section 3 — Pricing and Packaging Changes

For each competitor with pricing activity:

**[Competitor name]**

Change: [Specific pricing or packaging change — be precise, not vague]
Direction: [Price increase / decrease / new tier / removed tier / bundle]
Effective date: [If known]
Strategic read: [Are they monetising more aggressively? Protecting market
share? Expanding into a new segment?]
Impact on us: [Does this create an opening, close one, or require us to
re-evaluate our own pricing?]

If no pricing changes: "No pricing changes observed."

---

### Section 4 — GTM and Marketing Moves

New campaigns, messaging shifts, channel expansions, partnership announcements,
or geographic moves.

**[Competitor name]**

Move: [Specific GTM action]
Channel: [Where observed — LinkedIn ads, TV, influencer, PR, events]
Message shift: [If positioning changed — quote or paraphrase their new framing]
Target: [New segment, geography, or use case they appear to be chasing]
Strategic read: [What does this signal?]

---

### Section 5 — Hiring Signals

Job postings are the most reliable forward indicator of competitor strategy.
Scan for roles that signal strategic intent.

**[Competitor name]**

Roles posted: [Job titles, volume, location]
Signal: [What does this hiring pattern indicate about their 6–12 month
roadmap? E.g., 5 ML engineer roles → AI feature investment;
3 enterprise sales roles → upmarket move]
Confidence: [High / Medium / Low based on volume and consistency]

---

### Section 6 — Funding and Corporate Activity

New funding rounds, acquisitions, leadership changes, or restructures.

**[Competitor name]**

Event: [Funding round / acquisition / IPO filing / leadership change /
restructure]
Amount / details: [Specific if known]
Strategic read: [What does this capital or change enable? What does it signal
about their trajectory?]
Timeline implication: [Does this accelerate their threat to us, or distract
them?]

---

### Section 7 — Customer Sentiment Signals

App store reviews, social media, community forums, and support tickets from
competitor users that surface unmet needs or satisfaction drops.

**[Competitor name]**

Signal: [Theme from customer feedback — e.g., "Multiple G2 reviews cite
poor mobile UX as a churn reason in last 30 days"]
Volume: [How many data points, from where]
Opportunity: [Does this signal a gap we can exploit in our positioning or
roadmap?]

---

### Section 8 — Strategic Implications

This is the highest-value section. Synthesise everything above into 3–5
actionable implications. Each must connect to a specific signal.

Format:

**Implication [N]: [Short label]**
Signal: [Which competitor move triggers this]
Strategic read: [What it means for your market position]
Recommended action: [Specific — not "monitor" but "accelerate X by [date]"
or "brief the sales team on Y counter-narrative by [date]"]
Priority: High / Medium / Low
Owner: [Role, if you want to assign — or leave blank]

---

### Section 9 — Watch List for Next Period

What to track in the next brief that isn't ready to call yet.

| Signal | Competitor | Why watching | Trigger to escalate |
|---|---|---|---|
| [Unconfirmed pricing change] | [Name] | [Rumoured in press] | [If confirmed] |

---

## Brief Format Options

Ask if not specified:

1. **Full brief** — all sections, suitable for leadership sharing
2. **Quick scan** — Sections 1, 2, 3, and 8 only — under 1 page
3. **Slide outline** — structured for a 5-minute competitive update in a
   leadership meeting
4. **Slack-ready summary** — 200 words max, top 3 moves and top implication

---

## Frequency Guidance

| Cadence | Best for | Focus |
|---|---|---|
| Weekly | Fast-moving markets (fintech, AI, consumer) | Product and pricing moves, hiring |
| Monthly | Stable markets or leadership updates | Strategic shifts, funding, GTM |
| Ad-hoc | Triggered by a specific event | Deep-dive on one competitor or one move |

---

## Quality Rules

**Signal over noise.** Not every competitor tweet is a strategic signal.
Apply a filter: does this change what we build, price, sell, or say?
If not, don't include it.

**Primary sources over secondary.** App store release notes, pricing pages,
job boards, and earnings transcripts beat press coverage. Use web search
where available.

**Separate fact from inference.** "Competitor X launched Feature Y" is a
fact. "This signals they're going upmarket" is an inference — label it as
such.

**Implications must be actionable.** "Competitor is growing" is not an
implication. "Competitor's new enterprise tier undercuts our mid-market
pricing by 30% — we should brief sales with a counter-narrative before
their next outreach cycle" is.

**Never pad.** A "No material changes" section is more credible than
a padded one. The reader notices.

---

## Suggest Next Commands

After producing the brief:
- `/competitive-battlecard` — to turn a key competitor insight into a sales
  battlecard
- `/positioning-ideas` — if competitor moves suggest a re-positioning
  opportunity
- `/stakeholder-update` — to communicate the most important CI signals to
  leadership
- `/pricing` — if competitor pricing changes warrant a pricing review

---

## Examples

**Setup trigger:**
"Can you help me set up a monthly CI brief? I want to track Razorpay, PhonePe,
and Paytm. I'm at a neobank and care most about product and pricing moves."

**Recurring trigger:**
"Time for our weekly CI sweep — same competitors as last time."

**Ad-hoc trigger:**
"Stripe just announced a new embedded finance product. Can you do a quick CI
brief on what this means for us?"

**Ambiguous trigger:**
"What are our competitors doing?"
→ Respond: "Happy to put together a CI brief. Which competitors should I
focus on, and do you want a quick scan or a full brief? Also, what's your
product context so I can frame the strategic implications correctly?"
