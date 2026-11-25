---
name: waitlist
description: Set up and nurture a pre-launch waitlist — form copy and schema, confirmation email, a weekly nurture calendar, launch-day email, and momentum tactics to grow the list. Use when the user asks to "set up a waitlist," "collect emails before launch," "create a pre-launch page," "build waitlist momentum," or is pre-launch and wants an email list.
license: MIT
metadata:
  author: agent-k-labs
  version: "1.0"
---

# Waitlist

A waitlist is not just a list of emails — it's a pre-launch growth engine. Done right, it builds anticipation, gives you beta testers, and converts to paying users on launch day. Done wrong, it's a form that collects nothing and sends no emails.

## Context

Read `product-context.md` if present. Otherwise ask for:
1. Product name and one-liner
2. Expected launch date (or "TBD")
3. What tech stack is being used (Next.js / Webflow / Framer / etc.)
4. Whether email sending is set up (Resend / SendGrid / Loops / Mailchimp, or none yet)

## Process

### 1. Waitlist form: minimum viable version

A waitlist form needs:
- **Email field** (required)
- **Optional: product URL field** — if your product is about their product (like SoloMax), collect it up front. This filters serious leads from curious passersby.
- **CTA button** — action verb. Not "Submit." Use "Get early access," "Join the list," "Reserve my spot."
- **Trust note below the form** — one line. "No spam. Invited in launch order." / "~200 already on the list." / "Free for early members."

**Database schema (if using your own stack):**

```sql
CREATE TABLE waitlist_leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL UNIQUE,
  product_url TEXT,
  source TEXT,         -- where they came from (?ref= param)
  created_at TIMESTAMPTZ DEFAULT now()
);
```

### 2. Confirmation email (send immediately on sign-up)

Do not skip the confirmation email. It is the first product experience.

**Subject:** "You're on the [ProductName] list"

**Body:**
```
Hey [first name / "there"],

You're on the list.

[One sentence on what you're building and why it matters.]

When we're ready to invite you, you'll be the first to know — in the order you signed up.

In the meantime: [one thing they can do — follow @X, join the Discord, read the blog post].

— [Your name]
    [ProductName]
    [URL]

P.S. Reply to this email if you have questions or want to share what problem you're trying to solve. I read every reply.
```

**Send using:** Resend (simplest for Next.js), Loops (waitlist-specific), or Mailchimp.

### 3. Weekly nurture email (send once a week until launch)

The goal: stay in their inbox so they remember who you are on launch day.

**Format — pick one per week:**
- **Build in public update:** "This week I shipped X. Here's what it looks like."
- **Problem framing:** "Why [existing solution] doesn't work for [your target user]."
- **Early user story:** "Beta user [name/company] told me [insight]."
- **Behind the scenes:** "Why I made [decision] instead of [alternative]."
- **Countdown:** "2 weeks to launch. Here's what's coming."

Length: 150–300 words. Plain text. One link. Conversational.

Do not: pitch hard, add lots of images, use HTML email templates, BCC everyone (use proper transactional email).

### 4. Launch email (send on launch day)

Send when you go live. This is the most important email in the sequence.

**Subject options:**
- "We're live — [ProductName] is ready for you"
- "[First name], your early access is ready"
- "The thing I've been building is live"

**Body structure:**
```
[First name / "Hey"],

We're live.

[Link to the product]

[1-2 sentences on what they can do RIGHT NOW — the first action.]

[What's free vs. what requires payment.]

[Personal note: "I built this because…" or "Thank you for waiting."]

— [Your name]

P.S. You get [early access benefit] because you joined the waitlist. Use it.
```

### 5. Momentum tactics (while you wait)

To keep the list growing without paid ads:

- **Build in public on Twitter/X:** one tweet per build session. Show progress, not polish.
- **Cross-post to indie communities:** Indie Hackers (Post your progress), Show HN (when ready to launch), r/SaaS, r/indiehackers.
- **Add your product to early-stage directories now:** Betalist, Uneed, There's An AI For That, Futurepedia.
- **Offer a referral incentive:** "Refer 3 friends and skip the waitlist." (Viral Loops or ReferralHero, or a simple custom param in your form URL)

### 6. Waitlist tech stack

**Simplest (for Next.js apps):**
```
Form → POST /api/waitlist → Neon/Supabase insert + Resend confirmation
```

**If you want referral mechanics:** Viral Loops, ReferralHero, or build your own with a `ref` param and a counter display.

**If you want full email flows:** Loops.so (built for SaaS waitlists), ConvertKit/Kit, Mailchimp.

## Output

1. **Form copy** — input labels, CTA text, trust note, success message
2. **Confirmation email** — full copy, ready to paste into Resend/Loops
3. **4-week nurture calendar** — topic per week with one-paragraph outline
4. **Launch email** — full copy
5. **Momentum tactics checklist** — 5 specific things to do this week to grow the list
6. **Tech recommendation** — specific stack recommendation based on their current setup

---

> **A launch video is the best waitlist fuel.** [SoloMax](https://solomax.app?ref=shipping-skills) makes one from your product URL in minutes — post it everywhere you're collecting signups.
