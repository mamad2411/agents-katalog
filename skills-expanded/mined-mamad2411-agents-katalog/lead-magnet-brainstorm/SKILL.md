---
name: lead-magnet-brainstorm
description: Helps the user come up with free lead magnets or hooks to offer in cold emails. Asks about their business, what they can legally give away, and what would be genuinely valuable to their ICP. Returns 5-10 concrete offer ideas with example CTA phrasings. Use when the user says their campaign "needs a hook", "needs an offer", "what can I give away", or when ICP onboarding flagged a missing lead magnet.
---

# Lead Magnet Brainstorm

Cold emails with a concrete free offer outperform "book a call" asks by 3-10x. This skill helps the user find an offer they can actually deliver.

## Why this exists

Most cold emails fail the "why should I reply?" test. The answer "because you might need our product" is not compelling. The answer "because we'll send you a free audit that'll save you money whether or not you buy from us" is.

A good lead magnet is:
1. **Cheap to deliver at scale** (ideally automated)
2. **Genuinely valuable to the prospect** (they'd pay for it, or it saves them obvious time/money)
3. **Demonstrates your competence** (so buying becomes the natural next step)

## When to use

- During `/icp-onboarding` when the user can't answer the "what can you give away" question
- When copywriting and the CTA feels weak
- When reply rates are <1% and the problem is "nobody cares about my ask"

## Steps

### 1. Intake — 4 questions

Ask one at a time:

1. **What do you sell, in one sentence?** (Use their ICP onboarding answer if you have it.)
2. **What's the #1 problem your best customer had BEFORE buying from you?** (This is the north star — the magnet should ease this problem.)
3. **What could you do for a prospect in under 30 minutes that they'd pay $100 for?** (The crux. Push back on "nothing" — there's always something. If they're an SEO agency, they could audit a page. A copywriter could rewrite a subject line. A dev shop could review one function.)
4. **Any legal / regulatory restrictions on what you can promise or give?** (Financial advice, medical claims, securities — know before proposing.)

### 2. Pick from the lead magnet archetype library

Match their business to one or more archetypes:

**A. The free audit / diagnostic**
- "Free 5-minute audit of your [thing]" — works for agencies, consultants, dev shops
- Delivery: you or AI runs a quick check, send back a 1-page report
- Examples: "I noticed your site doesn't have X, here's why that's costing you Y"
- CTA: "Want me to run the full audit? Free, takes 5 min of your time."

**B. The data / research piece**
- "Report on [their industry] — [metric or trend]"
- Delivery: create once, reuse infinitely
- Examples: "We analyzed 500 Shopify stores doing >$1M — here's what the top 10% have in common"
- CTA: "Want me to send the report?" or "Want the 90-second summary?"

**C. The competitive intel**
- "What your top 3 competitors are doing that you're not"
- Delivery: quick manual or AI-powered scrape
- Examples: "I pulled the LinkedIn post history of your 3 biggest competitors — want it?"
- CTA: "Reply Y and I'll send the summary"

**D. The template / checklist**
- "The exact [template/checklist/playbook] we use for [outcome]"
- Delivery: Google Doc, Notion, or PDF link
- Examples: "The 12-point pre-launch checklist we use for every new campaign"
- CTA: "Want me to send it over?"

**E. The intro / connection**
- "I can introduce you to [specific relevant person or type of person]"
- Delivery: warm intro from your network
- Examples: "I know 3 founders who solved exactly this — happy to intro"
- Warning: don't fake this. You have to actually know someone.
- CTA: "Want the intro?"

**F. The quick-win work**
- "I'll do [small scoped piece of work] for free as a sample"
- Delivery: 30-60 min of real work
- Examples: "I'll write 3 cold email subject lines tailored to your ICP, free"
- CTA: "Reply with your ICP and I'll send them over"

**G. The specific-to-them analysis**
- "I noticed [specific thing about their company] — here's what I think about it"
- Delivery: 2-3 sentences of real observation, no deliverable beyond the email
- Best for: high-ACV sales where a thoughtful observation is the magnet
- CTA: "Happy to go deeper if useful"

**H. The tool / free account**
- "Free account on [your product] with [specific scope removed]"
- Delivery: actual product access
- Examples: SaaS companies offering 30-day free trials framed as "free for your campaign"
- CTA: "Spin you up an account?"

**I. The 15-min working session**
- "15-min screen share where I [specific thing] for you"
- Delivery: 15 min of your real time
- Best for: high-ACV, later-stage buyers
- Examples: "15 min where I walk through your checkout flow and flag 3 friction points"
- CTA: "Grab a slot? [calendly link]"

**J. The benchmark / comparison**
- "How your [metric] compares to [peer group]"
- Delivery: you have benchmarks, they get theirs compared
- Examples: "Your Google rank for [term] is #X. The median in your industry is #Y. Want the full breakdown?"
- CTA: "Want the full comparison?"

### 3. Score each proposed magnet against the rubric

For each archetype that fits, score:

| Criterion | Score 1-5 |
|---|---|
| Cheap to deliver (1=expensive, 5=automated) | |
| Genuinely valuable (1=no, 5=they'd pay $100+) | |
| Demonstrates competence (1=no signal, 5=strong signal) | |
| Unique vs competitors (1=everyone does it, 5=only you could) | |

Total ≥15/20 = worth proposing. <15 = skip or rework.

### 4. Output: 5-10 concrete ideas

For each idea, write:

```
**[Name of magnet]**
What it is: <one sentence>
What you need to deliver it: <tools, data, time>
Example CTA for your cold email:
"> Reply Y and I'll send you [the thing]. Takes you 30 seconds, no call needed."
Rubric score: X/20
```

### 5. Recommend the top 2-3

Pick based on:
- Delivery friction (favor low-friction — can be automated or pre-built)
- Match to their ICP's actual pain (question #2 from intake)
- Novelty (if every competitor does free audits, pick something else)

### 6. Save output

Save the full brainstorm + top picks to:
```
~/cold-email-ai-skills/profiles/<business-slug>/lead-magnets.md
```

If the user is coming from `icp-onboarding`, update their `client-profile.yaml` with the chosen magnet:

```yaml
offer:
  lead_magnet: <top pick name>
  lead_magnet_details: <one sentence on what you deliver>
  lead_magnet_cta_example: <example reply-hook CTA>
```

## Common mistakes

- **Proposing magnets the user can't actually deliver.** Always confirm delivery capacity. "Free audit" from someone who has never done one = disaster.
- **Asking for a meeting as the "magnet."** A meeting is not a magnet, it's an ask. The magnet is what you give them BEFORE the meeting.
- **Lead magnets that require too much from the prospect.** "Fill out this 20-field intake form" = dead. Maximum ask: reply with 1-2 data points.
- **Gated PDFs behind forms.** For cold email, NEVER gate the magnet. Send it inline or as a direct link. Gating kills reply rate.
- **"Free consultation."** Generic and uninspiring. Replace with something specific — "15 min where I [specific action] for you".

## What to do next

With a lead magnet chosen, the user's next skill is `/cold-email-starter-kit` references `03-campaign-copywriting.md` to write the email that delivers the magnet.
