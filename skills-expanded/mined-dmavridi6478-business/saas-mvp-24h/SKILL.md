---
name: saas-mvp-24h
description: A 4-phase procedure for building and launching a SaaS MVP within 24 hours using AI-assisted tooling — from planning scope through design, development, and deployment. Use when the user wants to go from idea to live product as fast as possible, or asks "how do I build this quickly," "what's the fastest way to launch," or "help me ship an MVP today." Pairs with saas-idea-validator (run that first to confirm the idea is worth building) and saas-mvp-builder procedure. Source: @vibe_codez TikTok series "How I'd Build a SaaS MVP in 24 Hours."
---

# SaaS MVP in 24 Hours

Source: @vibe_codez TikTok series "How I'd Build a SaaS MVP in 24 Hours."

> Run `saas-idea-validator` first. Building fast on a bad idea is just failing faster — confirm there's a real problem and a real customer before sprinting.

## The 4 phases

### Phase 1 — Plan (0–2 h): MVP scope, user flow, launch checklist
**Tools:** Claude + GPT-5 + valycode.com

What to produce:
- Problem statement in one sentence
- Target user (specific role/context, not "businesses")
- 3–5 core features only (cut everything else)
- User flow: entry point → core action → value delivered → return path
- Launch checklist: what must be true before you show this to anyone

**Claude prompt to use:**
```
I want to build [PRODUCT IDEA] for [TARGET USER]. 

Give me:
1. A one-sentence problem statement
2. The 3 features that are truly MVP (cut everything else — be brutal)
3. The user flow from first click to first value delivered
4. A launch checklist of 10 things that must be true before showing this to users

Be direct. Tell me what I'm overcomplicating.
```

---

### Phase 2 — Design (2–6 h): Landing page + product UI
**Tools:** Figma + valycode.com + Lovable

What to produce:
- Landing page: headline, sub-headline, 3 feature bullets, CTA, social proof placeholder
- Product UI: auth screens, dashboard skeleton, core feature screen(s)
- Design principle: ship a working skeleton, not a polished product

**Claude/Lovable prompt to use:**
```
Design a landing page and product UI for a SaaS that [WHAT IT DOES] for [WHO].

Landing page needs:
- One headline that names the benefit, not the feature
- Sub-headline that names the target user and the pain it removes
- 3 feature bullets (outcome-focused, not tech-focused)
- One CTA button
- Placeholder for social proof (testimonials / logos)

Product UI needs:
- Login/signup screen
- Dashboard showing [CORE METRIC OR ACTION]
- [CORE FEATURE] screen

Keep it functional, not beautiful. Ship, then polish.
```

---

### Phase 3 — Build (6–20 h): Auth, dashboard, core features
**Tools:** Cursor + Next.js + Supabase

Stack:
- **Next.js** (App Router) — frontend + API routes
- **Supabase** — auth, Postgres DB, storage, realtime
- **Cursor** — AI-assisted coding in the IDE

**Cursor system prompt to use:**
```
We are building [PRODUCT NAME]: [ONE-SENTENCE DESCRIPTION].

Stack: Next.js 14 App Router, TypeScript, Tailwind CSS, Supabase (auth + Postgres), Shadcn/ui components.

Current phase: [auth setup / dashboard / core feature].

Rules:
- Write production-quality code, not tutorial code
- Use Supabase Auth for all authentication — no custom auth
- All database operations go through Supabase client
- Components go in /components, pages in /app, utilities in /lib
- No unnecessary abstractions — only what the current feature needs

Next task: [SPECIFIC FEATURE TO BUILD]
```

Order of build:
1. Supabase project setup + schema
2. Auth (sign-up, login, protected routes)
3. Dashboard skeleton
4. Core feature #1 (the one thing that delivers value)
5. Core features #2–#3 only if time allows

---

### Phase 4 — Deploy + distribution (20–24 h): Live and getting users
**Tools:** Vercel + Supabase + TikTok

Deployment:
- Push to GitHub
- Connect to Vercel (auto-deploys on push)
- Set Supabase env vars in Vercel dashboard
- Run one end-to-end test on the live URL

First users (same day):
- TikTok/Instagram: show the product working, not a pitch. "I built X in 24 hours, here's how it works" performs better than ads
- Post in 2–3 relevant communities (Reddit, Discord, Slack groups) with the problem framing, not the product pitch
- DM 5 people who match the target user profile with a direct ask to try it

**Post-launch Claude prompt to use:**
```
My SaaS [PRODUCT NAME] is now live at [URL]. 

It does: [WHAT IT DOES]
For: [TARGET USER]

Give me:
1. A TikTok/Reels script (60 seconds) that shows the product working — not a pitch, a demo
2. A Reddit post for [RELEVANT SUBREDDIT] that leads with the problem, not the product
3. A DM template to send to 5 potential users asking them to try it
4. The 3 things I should measure in week 1 to know if this has legs
```

---

## Critical constraints

- **Never skip Phase 1.** Jumping straight to code without a written user flow is why MVPs get abandoned mid-build.
- **Never skip the idea validator.** A 24-hour sprint on the wrong problem is 24 wasted hours.
- **Cut features ruthlessly.** An MVP that does one thing well beats a half-built product that does five things.
- **Deploy at hour 20, not hour 24.** The last 4 hours are for distribution, not polish.

## Related skills and commands

- **saas-idea-validator**: Run this before this skill — confirms whether the idea is worth building
- **open-source-devtools-2026**: Free alternatives for the build stack if you want zero tool cost
- **lean-software-stack**: Free alternatives for the ops layer around the product
- **content-repurposing-service**: Turn the TikTok launch content into a broader distribution campaign
- **growth-operating-framework**: After launch, use this for week-2+ growth structure
