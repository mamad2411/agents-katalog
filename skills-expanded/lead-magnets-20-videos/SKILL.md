---
name: lead-magnets-20-videos
description: Builds B2B lead magnets and inbound lead generation plans using rules weighted by how many of the 20 most-watched videos on the topic repeat each one, and flags where the experts disagree so you A/B test instead of guessing. Use when the user says "create a lead magnet", "B2B lead magnet ideas", "get more inbound leads", "build a quiz funnel", "lead magnet follow-up emails", or "where should my leads come from".
author: Yonathan Cohen (Tool Monsters)
version: 1.0.0
updated: 2026-09-14
license: MIT
---

# /lead-magnets

This skill is built from the transcripts of the 20 most-watched videos on B2B lead magnets and inbound lead generation from the last 6 months (since 2026-03-14), totaling 252,811 views and 70,868 words. From them, 446 pieces of advice were extracted and 417 were kept because their verbatim quote was found, grouped into 275 distinct themes. The number next to each rule below is how many of the 20 videos say it, and the sources are in sources.md.

The most repeated rule reached 5 of 20. Treat the weights as odds, not laws.

## Inputs
1. The paid offer the lead magnet should lead to, including its price and the result it promises.
2. The customer's real problems, in their own words (from calls, emails, reviews or support tickets).
3. Where current leads come from, by channel, with numbers if the user has them.
4. The CRM and email tool in use (for example HubSpot or Salesforce).

Refuse to invent customer problems, lead source numbers or conversion rates the user has not given.

## The rules, by weight
### Strong (5 of 20)
- **Base lead magnets on customer problems and needs.** (5/20) If the offer is "save $5,000/month on software bills", the lead magnet is "how to save $5,000 a month on your software bills". Inputs like "low response rate, getting emails to inbox" can produce ideas such as an email deliverability checker or a lead list quality auditor.
- **Include CTA links to your offer within lead magnets.** (5/20) Put a direct link to the paid offer inside the asset itself.

### Solid (4 of 20)
- **Use free or low-cost entry offers, then upsell.** (4/20) Keep the entry offer free or under $100. Examples cited ranged from $49 to $200.
- **Automatically sync lead form data into your CRM.** (4/20) Connect the form to HubSpot or Salesforce so no lead is copied by hand.
- **Diversify lead sources across multiple channels.** (4/20) Cited reasons: a 60% no-click search rate, and roughly 30 to 40% of leads coming from LLMs for one speaker.

### Mentioned (3 of 20)
Use multi-email follow-up and nurture sequences, not one email (for example 3 to 4 touches before a lead is considered dead, or 4 emails plus 1 LinkedIn connection over 14 days) · Offer a diagnostic quiz with personalized results · Build lead magnets quickly with AI, don't overthink · Repurpose one content asset across all channels

## Where the experts disagree: do not pick, test
| Choice | Side A | Side B |
|---|---|---|
| Channel strategy | Focus on one avatar, problem, channel and platform at a time (2/20) | Diversify lead sources across multiple channels (4/20) |

## Steps
1. List the customer's top problems using only what the user provided, and pick the one most directly solved by the paid offer.
2. Turn that problem into a lead magnet idea that mirrors the offer's promise. Consider a checker, auditor, checklist or diagnostic quiz, and draft it quickly with AI from a template plus the user's own points.
3. Add CTA links to the paid offer inside the lead magnet, and decide on a free or under $100 entry step before the main offer.
4. Connect the opt-in form to the user's CRM so lead data syncs automatically.
5. Write a follow-up sequence of at least 3 to 4 touches (for example an immediate welcome, then a follow-up around day 7, then further touches) instead of a single email.
6. Plan distribution by repurposing the lead magnet into content for each channel the user already uses, such as LinkedIn, YouTube, email and community platforms.
7. Set up the channel A/B test: run a focused single-channel push against a multi-channel push for the same lead magnet, and compare leads per channel using the user's own tracking.
8. Close by listing which rules were applied with their weight (for example "Base lead magnets on customer problems and needs, 5/20"), and state that the channel strategy choice (focus on one channel vs diversify) is being A/B tested.

## Never
- Never claim results, conversion rates or lead volumes the user has not measured.
- Never invent facts about the prospect or customer, including their problems, quotes or company details.
- Never build a lead magnet that does not connect to the paid offer or leaves out a link to it.
