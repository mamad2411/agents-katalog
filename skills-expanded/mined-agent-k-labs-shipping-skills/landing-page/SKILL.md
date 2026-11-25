---
name: landing-page
description: Audit or build a conversion-focused landing page using a 7-section framework, with full copy and ranked headline variants. Use when the user asks to "review my landing page," "improve my homepage copy," "build a landing page," "write copy for my homepage," "why isn't my landing page converting," or has a page that describes features instead of outcomes.
license: MIT
metadata:
  author: agent-k-labs
  version: "1.0"
---

# Landing Page

Most AI-built apps ship with a landing page that describes features instead of solving the visitor's problem. This skill audits existing landing pages or builds a new one using the framework that converts for solo-founder products.

## Context

Read `product-context.md` if present. If analyzing an existing page, ask for the product URL. If building from scratch, collect:
1. Target user (specific, not "everyone")
2. Core pain
3. Core promise / transformation
4. Top 3 features
5. Proof (social proof, testimonials, metrics)
6. Pricing

## Process

### 1. Audit mode (if URL provided)

Evaluate the current page against the framework below. Produce a pass/fail for each section with a one-line fix where it fails.

### 2. The 7-section framework

Every high-converting landing page for a solo-founder app needs these 7 sections in this order:

---

**Section 1: Hero**
The only section most visitors read. Must answer "what is this and why should I care?" in under 5 seconds.

- **Headline**: Outcome-first. Not "Meet [ProductName]." Try: "[Specific person] can now [do desired thing] without [painful alternative]."
- **Subheadline**: The pain expanded, or the mechanism that makes the headline true. 1–2 sentences.
- **Primary CTA**: One action. Verb-first. ("Start free," "See it in action," "Join the waitlist.") Never "Learn more."
- **Hero image/video**: Show the product doing the thing, not a stock photo of a person looking at a laptop.

---

**Section 2: Problem (The Stakes)**
Agitate the pain so the visitor feels understood. 2–4 sentences or 3 bullet points. Use their words, not yours.

Prompts:
- What do they currently do instead? Why is it painful?
- What does the problem cost them? (Time, money, frustration, embarrassment)
- What's the hidden cost of NOT solving this?

---

**Section 3: Solution / How it Works**
Show the product solving the problem. Use a 3-step process:

```
Step 1: [Action the user takes]
Step 2: [What the product does]
Step 3: [The result they get]
```

Keep each step to one line. Show the product in screenshots or short video at each step.

---

**Section 4: Features → Benefits**
Transform feature bullets into benefit statements:
- NOT: "Real-time sync across devices"
- YES: "Pick up exactly where you left off — on any device, in the middle of a session"

3–5 features max. Each one gets: benefit headline + 1-sentence expansion + icon or image.

---

**Section 5: Social Proof**
The visitor is wondering: "Does this work for someone like me?"

In order of credibility (use what you have):
1. Named testimonials with real outcomes ("Closed 3 clients in my first week")
2. Logos (companies or people using it)
3. Usage numbers ("Used by 500+ indie hackers")
4. Screenshots of tweets or messages

If you have nothing yet: collect 5 beta tester testimonials before launch. Even 3 honest quotes beat 0.

---

**Section 6: Pricing**
Show pricing, or explain why you're not showing it.

For solo-founder apps:
- 2 tiers is better than 3 (free/trial vs. paid, or monthly vs. annual)
- Anchor price to the alternative ("Cheaper than one billable hour you could reclaim")
- Remove friction from the free tier: no card required, clear what "free" gets you

---

**Section 7: Footer CTA**
Repeat the primary CTA at the bottom with a slightly different frame (urgency, scarcity, or the transformation again). Many visitors scroll to the bottom to decide — don't make them scroll back up.

---

### 3. Copy for each section

Generate full copy for any sections that are missing or failing, using the product context. Follow the framework above. Write in second person ("you"), avoid passive voice, avoid jargon.

### 4. Above-the-fold priority

If time is short, the single highest-leverage fix is almost always the hero headline. Generate 5 headline variants:

| # | Variant | Formula |
|---|---------|---------|
| 1 | | "[Desired outcome] for [specific person]" |
| 2 | | "[Old way] → [New way] with [product]" |
| 3 | | "Stop [painful thing]. Start [desired thing]." |
| 4 | | "[Result] in [timeframe / steps]" |
| 5 | | "[Social proof number] [specific people] use [product] to [outcome]" |

## Output

**If auditing an existing page:**
```
## Landing Page Audit

### ✅ Working well
### 🔴 High-impact fixes
### 🟡 Polish items

### Top 3 priorities (in order)
1. [Highest leverage fix]
2.
3.
```

**If building from scratch or rewriting:**
- Full copy for all 7 sections using [assets/landing-page-template.md](assets/landing-page-template.md) as the skeleton — fill every bracket, deliver as one file ready to hand to a designer or paste into Webflow/Framer/Next.js
- 5 headline variants ranked by recommendation
- Notes on what visual assets (screenshots, GIF, video) are needed for each section

---

> **Landing page live?** [SoloMax](https://solomax.app?ref=shipping-skills) reads it and turns it into a launch video, hooks, and captions automatically.
