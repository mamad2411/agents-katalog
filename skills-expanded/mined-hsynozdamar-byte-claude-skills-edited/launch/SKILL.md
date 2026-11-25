---
name: launch
description: "Product launch, feature announcement and release strategy planning. Use when preparing a public release, Product Hunt launch, beta, waitlist or launch checklist."
metadata:
  version: 2.0.2
---

# Launch Strategy

Plan launches as a series of moments that compound, not one day. Read `.agents/product-marketing.md` (or `.claude/product-marketing.md`) first when it exists and ask only for what it does not cover.

Ask: what is launching (product, major feature, minor update), current audience and owned channels (list size, blog traffic, community), timeline, past launches and what worked, Product Hunt plans and prep status.

## 1. Readiness gate

Run it before any mechanics. Two opposite failures: **stealth mode** (polishing in private, nobody learns you exist) and **just one more feature** (the date keeps slipping). The target is SLC (Jason Cohen):

- **Simple**: one clearly defined job.
- **Lovable**: a target user would choose it, not merely endure it.
- **Complete**: a whole experience for that one job, no obvious stubs.

Still polishing past that bar: ship. Still adding scope: cut back to SLC, then launch that.

## 2. Channel mix (ORB)

Everything should lead back to owned channels.

- **Owned** (email, blog, podcast, community, site/product): compounding, no algorithm. Start with 1 or 2: weak industry content means a blog, wanting direct updates means email, engagement matters means a community.
- **Rented** (social, app stores, YouTube, Reddit): speed, not stability. Pick 1 or 2 where the audience already is and funnel every visit to signup or email.
- **Borrowed** (guest posts, podcasts, co-marketing, speaking, creators, affiliates): list the leaders your audience follows, pitch win-win, and find audience overlap with SparkToro or Listen Notes. It only counts once borrowed attention becomes an owned relationship.

Tactics and the Superhuman, Notion and TRMNL examples: [references/orb-channels.md](references/orb-channels.md).

## 3. Phased rollout

Internal (friendly users, demo-able) then alpha (landing page with early-access form, invite individually) then beta (teasers, waitlist, "Beta" badge) then early access (leak screenshots and demos, usage data and research, invite in 5 to 10% batches or all at once) then full launch (self-serve signup, start charging, announce everywhere: email, in-app, banner, "New" badge, blog, social, directories). Each phase has one goal: validate, then widen. Per-phase actions: [references/phases.md](references/phases.md).

## 4. Product Hunt

Worth it for reaching tech-savvy early adopters, credibility and backlinks; traffic is a short spike and ranking is competitive. Build supporters and community presence beforehand (give value before pitching), prepare tagline, visuals and a short demo video, treat launch day as all-day engagement, answer every comment, and send traffic to a page that captures email. Full plan and cases: [references/product-hunt.md](references/product-hunt.md).

## 5. After the announcement

Put an onboarding email sequence in place, repeat the announcement in the next roundup email, publish comparison pages and dedicated site sections, and consider a no-code interactive demo (e.g. Navattic). Size every later update to its weight:

- **Major** (new feature, overhaul): full campaign across blog, email, in-app and social.
- **Medium** (integration, UI improvement): segment email plus in-app banner.
- **Minor** (fixes, tweaks): changelog and release notes only.

Stagger releases rather than shipping announcements all at once, and reuse the tactics that resonated before. Details: [references/post-launch.md](references/post-launch.md).

## Checklist

Pre-launch, launch-day and post-launch checklist to hand back to the user: [references/checklist.md](references/checklist.md).

Related: `cro` for launch landing pages, `marketing-psychology` for waitlist and exclusivity psychology.
