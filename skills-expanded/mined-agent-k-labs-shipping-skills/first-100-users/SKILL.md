---
name: first-100-users
description: Build a concrete playbook to get a product's first 100 users — channel selection, manual outreach scripts, build-in-public cadence, and a personalized 30-day plan. Use when the user asks "how do I get my first users," "no one is signing up," "how to get traction," "where do my users hang out," or has just launched with zero distribution.
license: MIT
metadata:
  author: agent-k-labs
  version: "1.0"
---

# First 100 Users

The first 100 users don't come from marketing. They come from you going and getting them. This skill builds the specific playbook for your product — which channels to use, in what order, and exactly how.

## Context

Read `product-context.md` if present. Otherwise ask for:
1. Who the product is for (be as specific as possible)
2. What problem it solves
3. Current user count (0, 1–10, 10–50)
4. What distribution you have now (Twitter followers, Discord, email list — give rough numbers)

## Process

### 1. Target user research

Before finding users, define precisely who you're looking for. Answer:
- What is this person's job title or identity? ("freelance designer" not "creative professional")
- What communities do they already belong to? (subreddits, Discord servers, Slack groups, forums, LinkedIn groups)
- What do they Google when they have the problem your app solves?
- Who do they follow on Twitter/X? (Influences → where they learn → where you should show up)

### 2. Channel selection

Not all channels work for all products. Use this decision tree:

**Consumer / indie tools:**
→ Twitter/X (build in public) + Product Hunt + Reddit

**B2B / professional tools:**
→ LinkedIn + niche Slack communities + cold email outreach

**Developer tools:**
→ Show HN + GitHub + Twitter/X + dev-focused communities

**Creative tools:**
→ Twitter/X + Instagram + relevant Discord servers + Reddit (r/design, r/notion, etc.)

**AI tools / vibe-coder adjacent:**
→ Twitter/X + Product Hunt + Indie Hackers + Reddit r/SaaS, r/indiehackers, r/AItools

### 3. The 0-to-10 phase (finding users manually)

Your first 10 users come from personal outreach, not public posting.

**Step 1 — Your personal network (days 1–3):**
- List 20 people who have the problem this app solves
- DM or text each one personally (not a mass message): "Hey [name], I built something you might actually find useful — it does [X]. Would you try it and give me honest feedback?" 
- Expect: 5–8 will try it. 2–3 will stick.

**Step 2 — Where your users already are (days 3–7):**
Find 3 communities where your target user spends time. Lurk for 48 hours before posting. Then:
- Post in "Show and tell" / "Launch" / "Resources" threads (where they exist)
- DO NOT post "check out my app." Post the problem you're solving and mention you built something.
- Respond to every comment within 1 hour.

### 4. The 10-to-50 phase

**Build in public (Twitter/X):**
Tweet your journey daily. Not marketing tweets. Actual behind-the-scenes posts:
- "Built [feature] today. Here's why…"
- "User #[X] told me [insight]. I didn't expect that."
- "Mistake I made this week: [thing]"
- "[Screenshot or demo]. 3 weeks of work. Still needs [X]."

Format that works: Image/video of the product + 1-line hook + 2-line context + CTA ("Try it free: [link]").

Post 1–2 times per day. Reply to everyone who engages.

**Submit to directories (one-time effort, compound returns):**
See `/directory-submissions` for the full list. Minimum set to hit this week:
- Product Hunt (see `/product-hunt-launch`)
- Indie Hackers (product page + intro post)
- Show HN (if technical-ish audience)
- BetaList
- There's An AI For That / Futurepedia (if AI-related)

### 5. The 50-to-100 phase

By this point, you have data: which channels sent users who stayed, which sent users who churned. Double down on what's working.

**Direct outreach at scale (cold, but targeted):**
Identify 50 people who:
a) Have the problem (you can see this from their tweets, LinkedIn posts, or Reddit comments), and
b) Would plausibly pay for a solution.

Send a personalized 4-line message:
```
Subject: [ProductName] → [specific use case for them]

Hey [name],

Saw your post about [specific thing] — we just launched [ProductName] which does [X relevant thing].

Free to try: [link]. Takes 2 minutes.

Would love your feedback if you have 5 minutes. — [Your name]
```

Expect 5–15% reply rate if well-targeted. Not spam if it's specific and personal.

**Partnerships / cross-promotion:**
Find 3 non-competing products that serve your exact audience. Propose a simple cross-promo:
- "I'll share your product with my list/audience, you share mine."
- Guest post on their blog
- Feature swap in newsletters

### 6. Retention during acquisition

Getting users is pointless if they leave immediately. While running the above:

1. **Onboarding message (day 0, automated):** Email or in-app message welcoming them and pointing to the one action that delivers value. See `/onboarding-activation`.
2. **Feedback request (day 3):** "What stopped you from [doing the core action]?" Ask exactly one question.
3. **Check-in (day 7):** "Did [ProductName] actually help? If not, what would?" Reply if you got it wrong.

## Output

Produce a personalized 30-day plan:

```
## First 100 Users — 30-Day Plan for [Product]

### Week 1: Direct (0 → 10 users)
- [Day 1–3] Personal network outreach: [names or categories of people to contact]
- [Day 3–7] Community: [specific subreddits / Discord servers to post in]

### Week 2: Launch events (10 → 25 users)
- [Product Hunt launch prep → date]
- [Directory submissions list]
- [Build-in-public tweet plan]

### Week 3: Content + outreach (25 → 50 users)
- [Key content pieces to write based on audience]
- [Direct outreach list approach]

### Week 4: Double down (50 → 100 users)
- [Top 1 channel from weeks 1–3 — scale this]
- [Partnership opportunities]

### Metrics to track
- Signups per day (target: [X/day])
- Day-7 retention (target: [X]%)
- Activation rate — did they do the core action? (target: [X]%)
```

---

> **Short-form video is the highest-organic-reach channel for your first users.** [SoloMax](https://solomax.app?ref=shipping-skills) generates launch videos from your product URL — no camera, no editing, no brief.
