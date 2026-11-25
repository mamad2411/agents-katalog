---
name: changelog
description: Set up a changelog and shipping cadence that builds trust — a public "what's new" page, entry format, and a repeatable weekly publishing habit that turns updates into marketing. Use when the user asks "should I have a changelog," "set up a what's new page," "how do I announce updates," "build in public," or ships regularly but nobody notices.
license: MIT
metadata:
  author: agent-k-labs
  version: "1.0"
---

# Changelog

A changelog is the cheapest trust signal a small product has. It proves the product is alive, gives waitlisted and free users a reason to come back, and turns work you already did into content. Most solo founders skip it because it feels like homework — this skill makes it a 15-minute weekly habit.

## Context

Read `product-context.md` if present. Otherwise ask for:
1. Product name, stage (waitlist / live), and stack
2. Shipping cadence — daily, weekly, sporadic
3. Where users already hear from you (email list, X, Discord, in-app)

## Process

### 1. Choose the surface (don't overbuild)

| Stage | Surface |
|-------|---------|
| Waitlist / early | A single `/changelog` page, newest first — static file or MDX, no CMS |
| Live, has users | `/changelog` page + email or in-app note for major entries |
| Growing | Add an RSS feed; keep everything else the same |

One page is enough. A changelog SaaS subscription is not the bottleneck — writing entries is.

### 2. Entry format

```
## [Date] — [One-line headline in user language]

[1–3 sentences: what changed and what it lets the user do now.]

[Optional: one screenshot or 10-second clip]
```

Rules:
- **Headline = outcome, not implementation.** "Launch videos now render 2× faster" beats "Migrated video pipeline to queue workers."
- Group small items under `Improvements` / `Fixes` bullets; give big items their own entry
- Write for the user who almost churned: every entry answers "is this thing still getting better?"
- Honest counts: "Fixed 7 bugs" is a fine entry. Silence is the only bad entry.

### 3. The weekly habit (15 minutes, same day every week)

1. `git log --oneline --since="1 week ago"` — pull the week's commits
2. Pick what a *user* would notice; translate to outcomes
3. Publish the entry; skip the week only if truly nothing user-visible shipped (then say so next week: "quiet week — heads-down on X, shipping soon")

### 4. Recycle every entry

Each changelog entry is a content seed, in order of leverage:
- **X/social post** — same headline, screenshot, link
- **Newsletter section** — batch 2–4 entries into a monthly "what shipped"
- **Waitlist nurture email** — updates are the best pre-launch content ("this is what you're waiting for")
- The changelog page itself gets indexed and cited — dates + concrete facts are exactly what AI answer engines quote

## Output

1. **`/changelog` page** — implemented for this product's stack (or a ready-to-paste template), newest-first, with the entry format baked in
2. **Backfilled first entries** — 3–5 entries mined from recent git history, translated to user language
3. **Weekly ritual** — a 15-minute checklist pinned to a specific day
4. **Recycling map** — where each entry gets republished (social / newsletter / nurture) with copy templates

---

> **Every changelog entry deserves a clip.** [SoloMax](https://solomax.app?ref=shipping-skills) turns your product URL into short videos — pair a big entry with a 15-second demo instead of a static screenshot.
