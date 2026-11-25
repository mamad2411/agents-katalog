---
name: email-nurture-sequence
description: Drafts a 5-email nurture sequence where each email has exactly ONE goal, every subject line ships as an A/B pair, styling is plain-text-first, and unsubscribe intent is respected — drafts only, a human loads and sends. Use when the user asks for a "nurture sequence", "welcome series", "email drip", "onboarding emails", or "5-email campaign". Don't use for a single standalone newsletter issue — that's newsletter-assembler.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Content & Marketing, Email, Nurture, Sequences, Drafts]
    related_skills: [newsletter-assembler, landing-page-copywriter, brand-voice-guardian, content-repurposer]
---

# Email Nurture Sequence

Produces a 5-email sequence that earns its place in an inbox: one job per email, subject lines tested not guessed, formatting that reads like a person wrote it, and a hard rule that leaving must always be easy. This skill outputs drafts and a load plan — it never connects to an ESP and never sends.

## When to Use

- The user needs a welcome, onboarding, lead-magnet follow-up, or pre-launch sequence.
- An existing drip underperforms and needs a one-goal-per-email restructure.
- The user asks for "subject line A/B tests" for a sequence.
- **Not for:** a single recurring newsletter issue (`newsletter-assembler`), the page the sequence points to (`landing-page-copywriter`), or actually sending — no ESP access, drafts only, human loads and presses send.

## Quick Reference

| Action | Rule |
|---|---|
| One goal per email | Each email drives exactly one click/reply/action; a second ask means a sixth email, not a longer fifth |
| Subject pairs | A/B per email: A = clarity, B = curiosity; both ≤50 chars, both honest about contents |
| Plain-text-first | Write as if no HTML exists: short lines, no image-dependent meaning, ≤2 links, one formatting device max |
| Sequence arc | 1 deliver+welcome → 2 quick win → 3 story/proof → 4 objection → 5 direct ask |
| Unsubscribe respect | Footer slot in every draft; no guilt copy; opt-down offered before the ask email |
| Sending | NEVER. Deliver drafts + load checklist; human owns the ESP |

## Procedure

1. **Gather** — confirm: who enters the sequence and from where (lead magnet, signup, purchase), the sequence's end goal (the one conversion email 5 asks for), sending cadence (default: days 0, 2, 4, 7, 10), sender name/voice, and links available. End goal missing → stop and ask; a sequence without a destination is just noise.
2. **Map one goal per email** — write a 5-row plan first: email #, single goal, the one link/action, arc role (per Quick Reference). If the user's wishlist has 7 goals, cut or defer 2 — do not double-load an email. Get a nod on the map when the stakes are high; otherwise proceed.
3. **Draft in arc order** — each email: subject pair, preview text (≤80 chars, extends A not repeats it), body in plain-text style — greeting, 60–150 words that earn the one ask, single CTA as a text link, human sign-off. Emails 1–2 give before anything asks; email 4 names the biggest objection honestly; email 5 asks directly, once.
4. **Subject A/B discipline** — for each email: A states the value plainly ("Your template is inside"), B opens a loop ("The mistake I made first"). Both must be true to the body — curiosity that the email doesn't pay off trains people to ignore you.
5. **Respect-the-exit pass** — every draft ends with an `[UNSUBSCRIBE]` placeholder line; email 4 or 5 includes a one-line opt-down ("just want the monthly digest? click here" placeholder). Strip any guilt phrasing ("we'll be sad to see you go" is fine; "you'll miss out forever" is not).
6. **Deliver drafts + load plan** — assemble the Output Template with the schedule table and an ESP load checklist. State explicitly: these are drafts; nothing has been sent.

## Output Template

```
# Nurture Sequence: [name] — 5 emails, drafts only
**Entry:** [trigger] | **End goal:** [email 5's ask] | **Cadence:** D0/D2/D4/D7/D10

| # | Day | Goal (one) | Arc role |
|---|---|---|---|

## Email [n] — [goal]
Subject A: ... | Subject B: ...
Preview: ...
---
[body, plain-text style, one CTA link]
—[sender]
[UNSUBSCRIBE] · [opt-down, emails 4–5 only]

## Load checklist (human)
- [ ] Paste into ESP, map merge fields, verify unsubscribe link renders
- [ ] Set A/B split on subjects, schedule per cadence table
- [ ] Send test to self before activating
```

## Pitfalls

- **Two asks in one email** — a "quick win" email that also pitches the offer, so neither lands. Recovery: return to the step 2 map; move the second ask to its rightful email or cut it. One email, one goal, no exceptions.
- **Bait subject, mismatched body** — subject B promises a story the email doesn't tell. Recovery: in step 4 read each body asking "does this pay off both subjects?"; rewrite whichever side lies.
- **Newsletter-shaped nurture** — emails balloon to 400 words of sections and links. Recovery: cut to the 60–150 word band; if material genuinely deserves more, it's a link to a post, not inline copy.
- **Guilt-trip exit copy** — retention dark patterns creep into the footer. Recovery: run the step 5 pass; unsubscribe is one neutral line, opt-down is offered once, nothing shames the reader.
- **The agent "helpfully" sends** — drafts get loaded or dispatched because ESP access happened to exist. Recovery: this skill has no send step by design; if a send was made, report it immediately to the human with the audience affected — never quietly continue.

## Verification

- [ ] Exactly 5 emails; each maps to one goal on the step 2 table; no email carries two asks
- [ ] Every email has subject A + B (≤50 chars each) and preview text; both subjects truthful to the body
- [ ] Bodies 60–150 words, ≤2 links, single CTA, plain-text-first formatting
- [ ] `[UNSUBSCRIBE]` in all 5; opt-down present in email 4 or 5; zero guilt phrasing
- [ ] Deliverable states "drafts only — human loads and sends"; nothing was sent
