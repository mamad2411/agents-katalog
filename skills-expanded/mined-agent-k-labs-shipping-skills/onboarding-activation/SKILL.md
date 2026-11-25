---
name: onboarding-activation
description: Define the activation moment, audit the onboarding flow, and rebuild it so new users reach first value in under 3 minutes — includes welcome and day-3 emails, empty-state copy, and activation tracking. Use when the user says "users drop off after signup," "high sign-up low activation," "nobody's using the core feature," "users aren't converting," or wants to improve onboarding.
license: MIT
metadata:
  author: agent-k-labs
  version: "1.0"
---

# Onboarding & Activation

Most vibe-coded apps get signups but lose them in the first session. The user lands, doesn't immediately understand what to do, and leaves. Activation — getting a user to experience the core value at least once — is the most important metric in your first 30 days. This skill audits and rebuilds your onboarding.

## Context

Read `product-context.md` if present. Otherwise ask for:
1. What is the single core action that defines an "activated" user? (The thing that, if they do it once, they're likely to come back.)
2. How many steps are currently between sign-up and the first time they do that core action?
3. What does your current sign-up flow look like? (email/password, SSO, magic link, etc.)
4. Do you have any data on where users drop off? (even anecdotal is fine)

## Process

### 1. Define the activation moment

**The "aha" moment:** The first time a user feels the product's core value. Not signing up. Not looking around. The moment they think "oh, this actually works."

Examples:
- Slack: the first time a message they send gets a reply
- Dropbox: the first file they sync successfully
- A launch video tool: the first video that comes back looking like a real launch asset

**Your activation event:** Based on the product context, define the exact user action that constitutes activation. This is the north star metric for onboarding.

Checklist for a good activation definition:
- [ ] It's a single, specific action (not "uses the product")
- [ ] It correlates with retention (users who do this come back)
- [ ] You can track it with a single database query or analytics event
- [ ] A user can reach it in under 5 minutes from sign-up

### 2. Onboarding audit

Map the current user journey from landing to activation. For each step:

```
Step 1: [What user sees/does]
Step 2: [What happens next]
...
Step N: [Activation event]
```

Then evaluate each step against:
- **Time to complete:** More than 30 seconds = friction. Can this be skipped or automated?
- **Required vs. optional:** Is each piece of information actually needed before the user can try the product? If not, defer it.
- **Cognitive load:** Does the user have to make a decision here? Every decision is a drop-off point.
- **Clarity:** If a user lands on this step cold, do they know what to do?

Common onboarding anti-patterns in vibe-coded apps:
- Asking for company size, job title, or team size before the user has seen the product work
- Long email confirmation flows that delay getting to the product
- A dashboard full of features with no clear "start here"
- Empty states with no guidance ("Your projects will appear here")
- Requiring setup (API keys, integrations) before showing any value

### 3. The minimum viable onboarding

For a solo-founder app, target:
- **Time to first value:** < 3 minutes from sign-up
- **Steps to activation:** ≤ 3 decisions before the user can do the core action
- **Zero required setup:** The product should work out of the box with example data if needed

**The simplest effective onboarding:**

```
Sign-up (30 seconds)
  ↓
One-sentence welcome (5 seconds, in-app or email)
  ↓
The one thing to do right now (big button, no other options)
  ↓
[Activation event — user experiences the value]
  ↓
"Now here's what else you can do…" (only shown after activation)
```

### 4. The welcome email (day 0)

Sent immediately on sign-up. This is your best engagement window.

**Subject:** "Here's where to start with [ProductName]"

**Body:**
```
Hey [name / there],

Welcome to [ProductName].

The one thing to do right now: [exact action with link directly to it — not to the dashboard].

It takes [time estimate]. Here's what happens: [one line on what they'll experience].

If anything's confusing, just reply to this email. I read every reply.

— [Your name]

---
P.S. You signed up to [benefit they were seeking]. This is exactly how to get there: [direct link].
```

Keep it under 150 words. One CTA only.

### 5. Day 3 follow-up (if they haven't activated)

Check if the user completed the activation event. If not, trigger a follow-up:

**Subject:** "Did [ProductName] actually help?"

**Body:**
```
Hey [name],

You signed up [3 days ago] but haven't [done the core action] yet.

Totally normal — [ProductName] can feel [thing it might feel confusing] at first.

The fastest way to see if it works for you: [one-sentence instruction] → [direct link to the exact step].

Takes 2 minutes. Worth it if you're trying to [benefit they came for].

— [Your name]

P.S. If you ran into a problem or it's not what you expected, reply and tell me. I want to know.
```

### 6. Empty states (the moment most apps lose users)

Every empty state in your UI should have:
1. An illustration or icon (so it doesn't look broken)
2. A one-sentence explanation of what goes here
3. A CTA to fill it ("Create your first [X]" or "Try an example")
4. An example of what it looks like when full (screenshot or demo data option)

Never: a blank page, "No data yet," or "Coming soon" without context.

### 7. Activation tracking

Set up tracking for the activation event so you can measure your onboarding:

**Metric 1 — Activation rate:** % of signups who complete the activation event within 7 days. Target: >40%.
**Metric 2 — Time to activation:** Median time from sign-up to first activation event. Target: <15 minutes.
**Metric 3 — Day-7 retention:** % of activated users who return within 7 days. Target: >30%.

If activation rate is below 20%: your onboarding flow has a serious friction point.
If time to activation is >30 minutes: users are being asked to do too much before experiencing value.

## Output

1. **Activation event definition** — the single event, with the database query or analytics event name to track it
2. **Onboarding flow map** — current flow with friction points marked
3. **Recommended flow** — simplified version: ≤ 3 steps, < 3 minutes
4. **Welcome email** — ready to send via Resend/Loops
5. **Day-3 follow-up email** — ready to trigger
6. **Empty state copy** — for every major empty state in the product
7. **Activation tracking setup** — what to add to analytics / the events table

---

> **Activation fixed? Keep the top of the funnel full.** [SoloMax](https://solomax.app?ref=shipping-skills) turns your product URL into launch videos for TikTok, Reels, and Shorts.
