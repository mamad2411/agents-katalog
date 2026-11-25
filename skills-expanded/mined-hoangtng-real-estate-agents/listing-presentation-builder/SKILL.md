---
name: listing-presentation-builder
description: Build a complete, customized listing presentation for a seller meeting. Use this skill whenever a user asks to prepare for a listing presentation, write a pitch to a seller, create a pre-listing package, handle seller objections, or "what do I say when I meet with the seller." Also use when competing against other agents for the same listing. Produces a full presentation script with market section, pricing walk-through, marketing plan summary, objection handlers, and a strong close.
---

# Listing Presentation Builder

Builds a complete, personalized listing presentation — not a slide deck to read from, but a conversation guide that wins listings. This is Leo's work: the listing presentation is a conversation, not a monologue.

## What You Need From the User

- **Property:** address, beds/baths/SF, neighborhood, estimated value range
- **Seller intel:** names, motivation for selling, timeline, any known concerns
- **Competition:** are other agents presenting? How many? Any known competitors?
- **Agent background:** years in market, recent relevant sales, any specific credentials
- **Market context:** current conditions in this neighborhood (or generate from defaults)

The more seller intel provided, the stronger the presentation. If sparse, generate with `[PERSONALIZE: ...]` callouts.

## Output Format

```markdown
# Listing Presentation
**Property:** [Address]
**Sellers:** [Name(s)]
**Presenting Agent:** [Name] | [Agency]
**Date:** [Date]

---

## BEFORE YOU ARRIVE

**Research completed:**
- [ ] CMA run — recommended price range: $[X]–$[X]
- [ ] Last 5 sales in neighborhood memorized (not on paper — in your head)
- [ ] Active competition identified: [X] listings at [price range]
- [ ] Seller's name, motivation, and timeline confirmed
- [ ] Any prior listing history on this property checked
- [ ] Marketing plan customized for this specific property

**Your mindset:** You are not here to sell yourself. You are here to solve their problem. Listen more than you talk in the first 10 minutes.

---

## OPENING — Earn the Right to Present (5–8 min)

**Do not start with your slides or your stats. Start with their situation.**

> "Before I show you anything, I want to make sure I actually understand what matters most to you. Mind if I ask a few questions?"

**Ask (and genuinely listen):**
1. "What does a successful sale look like for you — beyond just getting a good price?"
2. "Is there anything about this process that you're worried about or want to make sure goes right?"
3. "Have you sold a home before? What was that experience like?"
4. "What's your ideal timeline?"

**[PERSONALIZE: Note their answers here. Reference them throughout the presentation. This is what makes you different from the three other agents who came in and talked about themselves for 45 minutes.]**

---

## THE MARKET (10–12 min)

**Transition:**
> "Let me show you exactly what's happening in [neighborhood] right now — because this is going to shape everything about our strategy."

**Deliver the market section verbally — not from a printed sheet:**
- "[X] homes are active in your price range right now. Those are your competitors."
- "The last [X] homes that sold here took [X] days and closed at [X]% of list price."
- "The absorption rate right now is [X] months — [plain language interpretation]."
- "[If seller's market]: Correctly priced homes are moving fast. Your window to capture peak demand is in the first two weeks."
- "[If buyer's market]: Buyers have more options than they did 12 months ago. The homes selling are the ones priced right and presented well. The ones sitting are overpriced."

> "I want you to feel like you understand this market deeply before we talk price — because I'm going to show you a number and I want you to trust it."

---

## PRICING STRATEGY (10–12 min)

**Transition:**
> "Let's talk about price. I'm going to walk you through exactly how I got to my recommendation — not because I want you to take my word for it, but because I want you to be able to explain this number to your neighbor."

**Walk through the CMA — see CMA Generator skill for full template**

**Key points to hit:**
- Show the 3 most similar recent sales — adjust for differences verbally
- Name the active competition and what makes their property different
- Show all three tiers (conservative / market / aggressive) — let them see the tradeoff
- Recommend the market price with confidence

**Handling the overpricing instinct:**
> "I know [X] feels right — and I want to get you there too. Here's the challenge: the first two weeks on market are your best window. After 21 days, buyers start wondering what's wrong. The data from this area shows that correctly priced homes average [X] days and [X]% of list price. Overpriced-then-reduced homes average [Y] days and [Y]% of their original list. The market price I'm recommending actually puts more money in your pocket."

---

## MARKETING PLAN (8–10 min)

**Transition:**
> "Most agents will put your home on the MLS and hold an open house. Here's what we do differently."

**Walk through the property-specific marketing plan — see Property Marketing Plan skill:**
- The property story: "Here's how I'd describe your home to a buyer..."
- Photography: "We use [photographer] and I brief every shoot personally..."
- Digital reach: "Your home will be seen by [X] targeted buyers in the first week..."
- Social: "Here's the content plan for the first two weeks..."
- Open house + broker preview strategy
- Your agent network: "I'm going to email [X] agents who have active buyers in this price range before it even hits the MLS..."

**[PERSONALIZE: Reference one specific feature of THIS property and how you'd market it. Don't be generic here. "That kitchen island is the hero shot — it's going on everything."]**

---

## PROCESS & WHAT TO EXPECT (5 min)

> "Let me walk you through what happens between now and closing — and what I promise you along the way."

- From sign to market: [X] days (what needs to happen, what they need to do)
- Communication: "You'll hear from me every week with a written update — showings, feedback, market changes. You'll never have to wonder what's happening."
- Transaction coordination: "Once we're under contract, [TC name] handles all the paperwork and deadlines so you can focus on your move."
- Your job: [Keep the home showing-ready / make it available for showings / small prep list]

---

## OBJECTION HANDLERS

### "Another agent said they could get me more"
> "I'd genuinely love to see that CMA — if there's data I missed, I want to know. What I've found is that higher list prices feel good on paper, but the question is what you net. Overpriced homes sit. Sitting homes get low-ball offers. The number I'm recommending is where qualified buyers write offers quickly — and that's where you net the most."

### "Your commission is too high"
> "That's a fair thing to raise. Let me show you what goes into it — and then let's look at what you'd actually take home in both scenarios. Because the question isn't what the commission is. It's what your check looks like at closing."

[Show net proceeds comparison: lower commission / less service / longer DOM vs. recommended commission / full service / faster close]

### "We want to try $[higher price] for a few weeks"
> "I understand — it's your home and your decision. I want to make sure you have the full picture before we decide. Here's specifically what happens when a listing sits in this market: [days on market data, price reduction pattern, buyer perception]. I'm not trying to talk you out of your number. I'm trying to protect your outcome."

### "We're thinking of doing it ourselves"
> "That's worth considering seriously. Here's the data on FSBO outcomes in this market, and here's where the process tends to get difficult: [pricing, negotiations, disclosure liability, transaction coordination]. If you decide to go that route, I'll share our disclosure checklist — no charge. And if it doesn't go as planned, I'm here."

### "We already have an agent in mind"
> "Completely understand. All I'd ask is: if they're not giving you a current CMA, a specific marketing plan for your property, and a clear process — push them on it. You deserve that from whoever you choose. And if at any point you want a second opinion on anything, I'm available."

---

## THE CLOSE (3–5 min)

**Transition:**
> "Based on everything we've talked about, here's what I'd recommend as your next step."

**Read the room:**
- Ready to sign → "I have the listing agreement here. If you're comfortable, we can take care of it now and I can start the photography prep this week."
- Needs time → "I completely understand — this is a big decision. How about I follow up [Tuesday/specific day]? I'll also send you a written summary of what we discussed so you have it in writing."
- Comparing agents → "That makes total sense. What's your timeline for deciding? I want to make sure you have everything you need from me to make that comparison."

**Never pressure. Never create false urgency. If the market is hot, that's real urgency — say so. If it isn't, don't manufacture it.**

---

## POST-PRESENTATION FOLLOW-UP

**Same day:** Handwritten thank you note (or personal email if out of market)
**48 hours:** "Just wanted to follow up — any questions after you've had a chance to think it over?"
**1 week (if no decision):** Brief check-in, offer to answer any new questions
**2 weeks:** Final follow-up — respect the decision if they've gone elsewhere

---

## COMPETING AGAINST OTHER AGENTS

**Your edge is always:**
1. Market knowledge (you know the last 5 sales cold)
2. Specific marketing plan for THIS property (not a generic pitch)
3. Honest pricing (you'll tell them what they need to hear, not what they want to hear)
4. Communication commitment (weekly updates, no going dark)

**What you should never do:**
- Criticize competitors by name
- Promise a price you can't support with data to win the listing
- Over-promise on timeline or outcome
- Bring a generic presentation that could have been for any house
```

## Behavior Notes

- Always generate the opening questions section — most agents skip this and it's where the listing is actually won.
- If seller intel is thin, add `[PERSONALIZE]` callouts throughout — the agent should never walk in and read generic copy.
- The objection handlers should feel conversational, not scripted. If the user wants to rehearse them, offer to do a mock Q&A.
- If user asks "how do I compete against a discount broker": add a specific section on net proceeds comparison — show the math, not just the argument.
- Always include the post-presentation follow-up sequence — Leo knows that 80% of listings are won by the third or fourth touchpoint, not the first.
