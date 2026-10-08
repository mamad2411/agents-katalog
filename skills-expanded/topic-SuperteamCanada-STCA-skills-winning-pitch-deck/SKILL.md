---
name: winning-pitch-deck
description: Craft or review a 3-minute Colosseum Frontier pitch deck using the DePitch framework. Triggers on "pitch deck", "pitch my project", "Colosseum submission", "review my deck", "roast my pitch".
---

# Winning Pitch Deck (DePitch framework)

This skill helps a founder build or review a 3-minute pitch deck that wins hackathon / startup-competition judges and, downstream, investors. The framework is by Sofian (DePitch Academy / Legends.fun) and has shipped 16 Colosseum wins, 3 accelerator entries, and $2.5M+ raised across teams that used it.

## The core insight

> "Interest is earned every 30 seconds. Your slides are support for *your* message — you are the spotlight. One slide = one message. If you sell the problem, you don't need to sell the solution."

Most founders lose the pitch before they start because they pitch a **concept** instead of a **scalable business**, rush to show everything instead of leaving the judge wanting more, and forget that the judge is watching hundreds of pitches in a row with a thumb hovering over "next".

## When to use this skill

**Use it proactively** any time the user signals they're preparing a pitch. Phrases that should trigger:

- "help me build a pitch deck" / "craft my pitch" / "write my pitch script"
- "Colosseum Frontier", "Solana hackathon", "Colosseum submission", "frontier pitch"
- "review / roast / critique my deck", "what's wrong with my pitch"
- "I have 3 minutes to pitch", "demo day", "startup competition", "YC-style pitch"
- "how do I pitch [my project]" — even without the word "deck"
- Submitting a founder pitch *video* (script + slides are the same problem)

Don't wait for the user to say "pitch deck" literally. If they're preparing to pitch, use the skill.

## Two modes — detect which one first

**Ask the user once, if it's not obvious:** "Do you want me to help you *build* this from scratch, or *review* a deck/script you already have?"

### Build mode
The user has a product/idea but no deck yet. Workflow:
1. Run the founder interview (see `references/founder-interview.md`) — ask **all** the questions up-front in one batched message so they can answer asynchronously, then wait for answers before drafting.
2. Draft a slide-by-slide outline applying `references/slide-by-slide.md`.
3. Write a speaker script with timing marks (see "Output format" below).
4. Self-check the draft against `references/failure-patterns.md` and `references/review-rubric.md` before showing the user. Fix anything that fails the check.
5. Deliver outline + script + a delivery-rehearsal checklist from `references/delivery-10-techniques.md`.

### Review mode
The user has a deck, script, or video/transcript. Workflow:
1. Read what they have.
2. Score against `references/review-rubric.md` and tag which of the 5 `failure-patterns.md` they're hitting.
3. Return **top 3–5 prioritized fixes**, not a full rewrite. Rewriting everything burns trust and buries the high-impact changes. Only rewrite sections the user asks you to.
4. For each fix: name the slide, quote the current version, write the suggested version, explain the why in one sentence.

## The framework (four movements, ~15 slide types)

The pitch moves through four beats. Slide *count* is flexible — one slide one message, so splitting is fine — but the **order** is load-bearing.

| Beat | Slides | Purpose |
|---|---|---|
| **Concept** | Intro → Problem → Value Proposition → Features → Demo | Make the judge feel the pain, then show the product working |
| **Business** | Market → (Trends) → (Competition) → Business Model → Traction → (Partners) | Prove this is a scalable business, not a concept |
| **Growth** | Growth Strategy → Roadmap | Show the engine to reach users + what ships next |
| **Close** | Team → Conclusion + CTA | Prove you'll deliver, leave them something to do |

Slides in parentheses are optional — include only if they add signal.

Details, winning examples, and per-slide "what to avoid": **`references/slide-by-slide.md`**.

## Hard rules (non-negotiable)

These come directly from the framework. Violating them is the single biggest predictor of a losing pitch.

1. **One slide = one message.** Titles 3–4 words. Words are the killer of your deck.
2. **Tense discipline.** Present or past tense everywhere. Future tense is allowed **only** on the roadmap slide. Ban all conditionals: *"trying to"*, *"hope to"*, *"aim to"*, *"would"*, *"should"*, *"could"*. These halve the trust signal instantly.
3. **Ban "obviously" and "of course."** They kill the surprise for the listener — and surprise is how you hook attention.
4. **Demo appears before 2:00.** A demo at 2:10 or 2:20 in a 3-minute pitch is too late — the judge is already leaving. 20–30 seconds, no background music, live through one main feature.
5. **Business model slide is non-negotiable.** Skip it and you're pitching a concept, not a business.
6. **Traction = 3 real metrics.** Prefer revenue > growth % > users > waitlist. **Do not use X/Twitter followers as traction** — judges and VCs read that as a red flag.
7. **Team slide = one outstanding achievement, not bios.** Highlight the thing that proves "we can deliver this again." Listing "CEO / CTO / Head of BD" is the default and costs you the slide.
8. **Every transition between slides is scripted.** "And that's exactly what we're solving." "So how do we make money?" The pitch is one continuous funnel, not a slide deck read aloud.
9. **End with a CTA, not "thank you."** Give the judge a next step: watch longer demo, book a call, try the product, scan the QR to our Legends.fund / product page.
10. **Embed something memorable.** One quotable line the judge can repeat to another judge in the hallway. Without it you're forgettable.

## Output format

When building, return three artifacts in one response, in this order:

### 1. Slide-by-slide outline

Markdown with one heading per slide. Under each slide:
- **On-slide content** — exactly what appears on the slide (title, sub-items, image notes)
- **What the judge should feel** — one line, why this slide exists
- **Transition into the next slide** — the sentence the founder says as they click

### 2. Speaker script with timing marks

A single script block with `[0:00]`, `[0:20]`, `[0:45]`, etc. timing marks. Target total runtime at bottom. Use the founder's actual voice from the interview answers — write how *they* talk, not corporate-speak. Mark transition sentences explicitly so the founder can rehearse the glue.

Aim for **~150 words per minute** spoken (so ~450 words for a 3-min pitch). Err on the shorter side — Sofian's advice: pitch a teaser, not a full movie.

### 3. Delivery rehearsal checklist

Pull from `references/delivery-10-techniques.md`. Tailor it to this deck specifically (e.g., flag tense violations in the draft so the founder can catch them when they rehearse, note which slide carries the hook, etc.).

## Colosseum Frontier specifics

If the user mentions Colosseum Frontier, the Solana hackathon, or the accelerator, layer these on:

- **Submission = 3-min pitch video + 3-min demo video.** Two separate videos. This skill handles the pitch video; the demo video is a longer walkthrough of the product.
- **Judges are busy VCs/founders/ecosystem partners** watching hundreds of pitches. They have a bias: they fund startups that can raise multiple rounds and reach high valuations. Pitch fundability, not just product.
- **Acceptance rate into the accelerator is reportedly lower than Y Combinator.** ~10 teams out of thousands make it to the accelerator with $250k pre-seed.
- **Legends.fun QR trick:** the user can put a QR code on the closing slide linking to their Legends.fund page, so judges reviewing weeks later see *current* traction, not submission-day traction. Strong signal of "still building".
- **Previous winners are public on the Colosseum site.** Recommend the founder watch 2–3 winning pitches in their category before finalizing.
- **Interview follow-up.** If they pass the video filter, the interview tests solidity of business model, moat ("why can't anyone copy you tomorrow?"), and grit ("is this a company or a hackathon project?"). Flag this to the founder so they start preparing now, not later.

## Turning the outline into slides

The skill outputs a markdown outline — the founder still needs to build the actual deck. Recommend one of these tools based on the founder's design skill and timeline:

| Tool | Best for | Notes |
|---|---|---|
| [Gamma](https://gamma.app) | Fastest path from outline to polished deck | Paste the outline and Gamma generates branded slides. Best for founders with no design skills or <24h to submission. |
| [Canva](https://canva.com) | Founders who want visual control without learning design software | Startup pitch templates available. Drag-and-drop. Good for custom imagery and brand consistency. |
| [Google Slides](https://slides.google.com) | Teams collaborating in real-time | Free, familiar, easy to share. Use a clean template — don't use the defaults. |
| [Pitch](https://pitch.com) | Design-forward teams who want presentation analytics | Built for startup decks. Has collaboration + analytics (see which slides investors spend time on). |
| [Figma](https://figma.com) | Founders who already use Figma | Figma Slides or community deck templates. Best if you're already in the Figma ecosystem. |

**Key advice regardless of tool:**
- Keep slides minimal — the outline says "one slide = one message" and that applies visually too
- Pick two fonts, three colors, and use them consistently
- Use high-quality images (Unsplash, Pexels) over clip art or stock illustrations
- Export as PDF for backup, but present from the native tool for animations

## Reference files

Load these as needed — don't front-load all of them.

- `references/slide-by-slide.md` — per-slide guidance with winning-deck examples (Surf Cache, Nomu, Spend, CFL, Loot Go). Load this when drafting or reviewing specific slides.
- `references/delivery-10-techniques.md` — the 10 delivery techniques (hook, teaser, tenses, rehearsal, stage, etc.). Load at the end of build mode and always in review mode.
- `references/failure-patterns.md` — the 5 reasons pitches fail. Use as a self-check before showing the user anything.
- `references/founder-interview.md` — structured interview questions for build mode. Load at start of build mode.
- `references/review-rubric.md` — scoring checklist for review mode. Load at start of review mode.
- `assets/deck-outline-template.md` — fillable outline the user can copy into their slide tool. Offer this at the end.

## A note on tone

Sofian's framework is direct and a little tough — he'll tell a founder their team slide is boring, their demo is too late, their tense is wrong. Mirror that. Founders reviewing a pitch are in the last week before a deadline; they need honest feedback, not compliment-sandwich feedback. Be specific, quote their words, give the fix.

The goal isn't to make the founder feel good about their draft. It's to get them into the top 10% of submissions.
