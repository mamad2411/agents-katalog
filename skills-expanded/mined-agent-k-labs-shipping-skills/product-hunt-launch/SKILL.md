---
name: product-hunt-launch
description: Plan and execute a Product Hunt launch — timing strategy, 5 tagline options, product description, gallery brief, maker comment, and an hour-by-hour day-of timeline. Use when the user asks to "launch on Product Hunt," "plan my PH launch," "write my PH description," "what's the best day to launch," or mentions Product Hunt at all.
license: MIT
metadata:
  author: agent-k-labs
  version: "1.0"
---

# Product Hunt Launch

A Product Hunt launch done right is still the best single-day distribution moment for a vibe-coded app. Done wrong, it's a wasted day. This skill builds the full playbook: tagline, description, gallery, maker comment, voting strategy, and day-of timeline.

## Context

Read `product-context.md` if present. Otherwise ask for:
1. Product URL
2. Target launch date (or "not set yet")
3. Current community size (Twitter followers, Discord members, email list, etc.)

## Process

### 1. Timing strategy

**Best days to launch** (ranked): Tuesday, Wednesday, Thursday.
- Monday: high competition, community slow to engage
- Friday–Sunday: lower traffic, weekend slump

**Best time to submit:** 12:01 AM Pacific Time on launch day (you get the full 24-hour window).

**How far in advance to prep:** at minimum, 1 week before launch day.

### 2. Tagline (the most important copy you'll write for PH)

Rules for a PH tagline:
- Under 60 characters
- No jargon, no buzzwords ("revolutionary," "AI-powered," "seamless")
- Says what it does, not what it is
- Works without seeing the product name
- Passes the "tell a friend" test: can you say it out loud without sounding weird?

Generate **5 tagline options** in this format:

| # | Tagline | Style | Char count |
|---|---------|-------|-----------|
| 1 | | Pain-led | |
| 2 | | Outcome-led | |
| 3 | | Comparison ("X without Y") | |
| 4 | | Audience-first | |
| 5 | | Provocative / counter-intuitive | |

Recommend one and explain why.

### 3. Product description

PH description: 200–260 words, markdown-supported.

Structure:
```
**[Opening line — lead with the pain, not a greeting]**

[2-3 sentences on the problem. Use "you" language.]

**[Product name]** [does the thing in one line].

[How it works in 3 bullet points. Each one is a step or a key feature.]
• 
•
•

[Social proof if you have it: "X founders have used it to…" / "Built after seeing…"]

[CTA: "Try it free at [URL]"]
```

### 4. Gallery (5 images / 1 video)

Order and content for the PH media gallery:

1. **Hero image** — product name + tagline on a clean background (matches OG image style)
2. **Problem frame** — the pain state, in 1 line + a screenshot showing the "before"
3. **Product in action** — a GIF or screenshot of the core feature working
4. **Result / "after"** — what the user sees when the product delivers
5. **Pricing or CTA** — free trial terms or pricing, with the URL

**Video** (optional but high-impact): 30–60 second demo. See `/launch-video` skill.

### 5. Maker comment (first comment = the highest-read thing on your launch)

Write a maker comment that follows this structure:
```
Hey PH 👋

[One sentence on who you are and why you built this.]

[2-3 sentences on the core problem and your "aha" moment.]

[What makes this different from X / Y.]

[What you're giving PH hunters specifically: free trial / extended access / code "PH24"]

I'm here all day — ask me anything. Would love your feedback on [specific thing you want feedback on].

— [Your name]
```

### 6. Day-of timeline

```
12:01 AM PT — Submit the product (do not wait until morning)
12:15 AM PT — Post maker comment
12:30 AM PT — Personal message / tweet: "Just launched on PH, would mean a lot if you upvoted"
08:00 AM PT — Post in relevant communities (Discord, Slack, Reddit) with the PH link
09:00 AM PT — Check and respond to every comment on PH. Respond within 1 hour all day.
12:00 PM PT — Midday status update tweet: screenshot of rank, thank early supporters
03:00 PM PT — Second community post wave
06:00 PM PT — Final push: email your list (if any) with 6 hours left
11:00 PM PT — Final response sweep. Thank top commenters individually.
```

### 7. Pre-launch checklist (run 48 hours before)

- [ ] Product page is live and passes `/pre-launch-checklist`
- [ ] PH listing preview looks correct (no broken images, tagline fits)
- [ ] All 5 gallery images are ready (1080×1080 or 1270×760)
- [ ] Maker comment is drafted and ready to paste
- [ ] Personal outreach list: 20–50 people who will genuinely support your launch (warm contacts only, not cold asks)
- [ ] Launch tweet is drafted and scheduled for 12:15 AM PT
- [ ] If you have an email list: launch-day email is ready to send at 8 AM PT
- [ ] Slack / Discord / Reddit posts are drafted
- [ ] Your calendar is blocked for the entire day

## Gotchas

- **Never buy upvotes or join upvote-exchange pods.** PH's fraud detection penalizes or delists launches for this — it can kill the launch mid-day. Warm personal outreach only.
- **Create the PH "upcoming" (teaser) page as soon as the date is set.** It gives you a shareable link for the waitlist/countdown emails before launch, and people can subscribe to be notified at launch.
- **Calibrate expectations to audience size.** With <1k followers and a small list, a healthy outcome is 100–250 upvotes and a strong sub-category ranking — not #1 Product of the Day, which typically requires a much larger pre-existing audience. Say this to the user so launch day isn't read as a failure.
- **Early velocity matters most.** Upvotes and substantive comments in the first 1–2 hours drive ranking more than totals — front-load the warmest asks to right after 12:01 AM PT, not the morning.

## Output

Deliver in order:
1. **Timing recommendation** — best launch date given current date and context
2. **5 tagline options** with recommendation
3. **Product description** — ready to paste into PH
4. **Gallery brief** — what to put in each of the 5 image slots
5. **Maker comment** — ready to paste
6. **Day-of timeline** — hour-by-hour
7. **Pre-launch checklist status** — pass/fail based on current product state

---

> **Need your launch video?** [SoloMax](https://solomax.app?ref=shipping-skills) creates a Product Hunt–ready launch video from your product URL in minutes.
