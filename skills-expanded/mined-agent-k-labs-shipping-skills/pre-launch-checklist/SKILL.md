---
name: pre-launch-checklist
description: Audit a product before going live — core user flows, landing copy, trust signals, SEO basics, analytics, email deliverability, and stability — producing a launch readiness report with blockers ranked by impact. Use when the user asks to "review my app before launch," "do a pre-launch audit," "check if I'm ready to launch," or is about to announce publicly.
license: MIT
metadata:
  author: agent-k-labs
  version: "1.0"
---

# Pre-Launch Checklist

The checklist every vibe-coded app should run before announcing to the world. Catches the gotchas that kill first impressions: broken flows, missing trust signals, confusing copy, no analytics, no way to contact you.

## Context

Read `product-context.md` if present. If not, ask for the product URL and a one-line description before proceeding.

## Process

If a live URL is available, first run the automated checks — they cover HTTPS, meta/OG tags, favicon, robots.txt, sitemap, and 404 handling in one pass:

```bash
bash scripts/check_site.sh https://yourdomain.com
```

Merge its 🔴/🟡 results into the report, then work through the sections below that curl can't verify (flows, emails, copy, payments). Produce a pass/fail for each item with a one-line fix where it fails.

### 1. Core user flow (5 minutes)

Go through the app as a brand-new user with no prior knowledge:

- [ ] The sign-up or onboarding flow completes without errors
- [ ] The core value action (the one thing the app does) is reachable within 2 clicks of landing
- [ ] Error states show a human-readable message, not a stack trace or blank screen
- [ ] Mobile layout works — key actions are tap-accessible
- [ ] Slow 3G simulation: the page loads something meaningful in under 3 seconds
- [ ] Email confirmation, password reset, and magic links work and deliver within 60 seconds

### 2. Landing page copy

Read the hero section as if you've never heard of the product:

- [ ] The headline communicates what the product does, not what it is called
- [ ] There is a clear primary CTA above the fold (one action, not three)
- [ ] The subheadline addresses the pain or promise — not features
- [ ] There is at least one piece of social proof (testimonial, user count, logo, screenshot)
- [ ] The pricing is either shown or there is a clear path to find it
- [ ] The page has a contact method or a way to reach the founder (email, Twitter, etc.)

### 3. Trust signals

- [ ] The domain has HTTPS (no mixed-content warnings)
- [ ] A privacy policy page exists and is linked in the footer
- [ ] Terms of service exists if the product collects payments or user data
- [ ] If collecting payments: the checkout flow uses a recognized provider (Stripe, Paddle, Lemon Squeezy) and shows the product name, price, and billing period clearly
- [ ] The founder or company name is visible somewhere on the site
- [ ] Social links, if listed, are real and active accounts

### 4. SEO & discoverability basics

- [ ] The `<title>` tag includes the product name and a keyword phrase
- [ ] The meta description (under 160 chars) communicates the core value proposition
- [ ] The OG image (used when shared on X, LinkedIn, Slack) shows the product name and is not a blank box
- [ ] The page is not blocked by `robots.txt` or `noindex`
- [ ] A `sitemap.xml` exists and is accessible

### 5. Analytics

- [ ] At least one analytics tool is installed and receiving events (Vercel Analytics, Plausible, PostHog, Google Analytics)
- [ ] Signup / waitlist submission events are tracked
- [ ] The core conversion event (the action that means a user "got it") fires correctly

### 6. Communication

- [ ] Transactional emails (welcome, confirmation, password reset) send correctly and land in inbox, not spam
- [ ] The "from" name is the product name, not `noreply@vercel.app` or a generated domain
- [ ] There is at least one way to receive user feedback (email, in-app widget, Typeform, etc.)

### 7. Copy & content

- [ ] Zero lorem ipsum or placeholder text remains
- [ ] No "Coming soon" buttons that lead nowhere without a note
- [ ] Pricing page (if present) matches the actual Stripe products/prices
- [ ] No dead links in the footer or navigation

### 8. Performance & stability

- [ ] The app has been tested in Chrome, Safari, and Firefox
- [ ] Database connection limits won't be hit at 10 concurrent users (for Neon/Supabase free tiers: check the connection pool setting)
- [ ] Rate limiting exists on any endpoint a bot could spam (signup, email, etc.)
- [ ] Environment variables are set for production (not just `.env.local`)

## Output

Produce a **launch readiness report** with:

```
## Pre-Launch Checklist Results

### ✅ Ready
- [list of passing items]

### 🔴 Blockers (fix before launch)
- [item] → [one-line fix]

### 🟡 Nice to fix (won't kill launch, fix this week)
- [item] → [one-line fix]

### Launch verdict
Ready to launch / Launch after fixing blockers / Hold for a day
```

Prioritize blockers by impact on first impressions and payment trust. A broken payment flow is a blocker; a missing favicon is not.

---

> **Ready to make launch content?** Once this checklist passes, [SoloMax](https://solomax.app?ref=shipping-skills) turns your product URL into a launch video, hooks, and captions in minutes.
