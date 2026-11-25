---
name: copy-analyze
description: Deep analysis of the client's copy from a sales perspective in their niche. Finds strengths, weaknesses, and "magic words". Delivers a structural recommendation for the landing. Requires brief/01-business.md (niche) filled.
---

# /copy-analyze

Reads texts from `inbox/texts/`, analyzes through the lens of the client's niche, produces `brief/copy-analysis.md` with recommendations for design and structure.

## When to use

- After `/inbox` (texts validated).
- BEFORE `/design-lock` — copy analysis affects mood, density, section length.
- Re-run if the client updates the copy.

## Requirements

**Required:**
1. `brief/01-business.md` filled (especially the Niche section).
2. `brief/02-audience.md` filled (pain points, language).
3. At least one text file in `inbox/texts/`.

If anything is missing — **refuse to work**, ask to fill.

## Process

**Step 1. Load context**
Read:
- `brief/01-business.md` — niche, competitors, convention/subversion.
- `brief/02-audience.md` — persona, pain, tone, language, triggers.
- `brief/03-goals.md` — main CTA, metrics.
- All `inbox/texts/*`.

**Step 2. Clarify niche if needed**

If the niche is described too broadly ("beauty", "services", "marketing") — re-ask until you have a sub-niche like "men's Botox for CEOs in Barcelona" or "SEO for local dentists in Germany".

Also ask if needed:
- Average check (affects copy volume and depth).
- Sales cycle (minutes vs weeks — affects section list).
- Real client phrases (voice-of-customer — gold for copy).

**Step 3. Deep analysis**

Walk the copy and answer each point concretely (not "generally OK").

**A. What the client actually sells**
- Explicit offer: literal text.
- Implicit offer: implied (people buy transformation, not the product).
- Transformation: from state A → to state B.

**B. Strengths for this niche**
- Unique claims — what can't be said about competitors (check 01-business.md → competitors).
- Proof — numbers / cases / credentials.
- Emotional hooks (fear / status / curiosity / belonging).
- Rational hooks (savings / efficiency / safety).
- Magic words for this niche (found in the copy, resonating with audience maturity).

**C. Weaknesses**
- Generic / cliché ("individual approach", "best materials", "top quality").
- Feature-talk instead of benefit-talk ("we have 5 sessions" instead of "in 5 sessions the pain goes away").
- Missed audience pains (cross with 02-audience → pain points).
- Missed objections (cross with 02-audience → objections).
- Missing social proof / guarantees / urgency where appropriate.
- Passive voice, long sentences, bureaucratese.

**D. Niche specifics**
- Does the tone match the audience (formal/friendly/expert)?
- Does the copy length match maturity?
  - cold → long (explain the problem).
  - warm → medium (explain the solution).
  - hot → short (compare with competitors).
- Niche-required elements present (e.g. certifications for medical, portfolio for design, credentials for consulting)?
- Niche taboos ("cheap" for premium, "best in market" for B2B enterprise) — violated?

**E. Landing structure (recommendation)**

Section order + for each: which copy from the original is used, what to add, what to cut.

```
1. Hero
   Headline (A/B): ...
   Subheadline: ...
   CTA: ...
   Visual: (what to show — from inbox/media/ if available)

2. Proof (opt.)
   What: logos / numbers / credentials
   Source: ...

3. Offer
   ...

4. Process
   ...

5. Testimonials (opt., if in inbox)
   ...

6. FAQ (opt., if 5+ real questions)
   ...

7. CTA-form
   Text before the form: ...
   Argument to act: ...
```

**F. Open questions for the client**

5-10 questions that need answers before final copy. Format:
```
Q1: <question>
Why: <what the answer unlocks>
```

**Step 4. Save to `brief/copy-analysis.md`**

Everything above — into a structured markdown file.

**Step 5. Show summary to the user**

- Top 3 strengths.
- Top 3 weaknesses.
- Top 3 questions critical to clarify.

Ask: dig deeper on any point? Or move to `/refs`?

## Rules

- **No "generally good".** Every point is specific.
- **Ground in niche.** "Individual approach" may be OK in mass-market and a disaster in premium.
- **Show examples.** Not "sounds weak", but "sounds weak: [quote] → stronger: [rewrite]".
- **Do not rewrite the copy in full.** Task is analysis + recommendations, not final copy. Final copy is the client's job (with their copywriter), but they now have a clear brief.

## What NOT to do

- Do not invent "strengths" that aren't in the copy (may suggest as "add if true").
- Do not guess facts (numbers, cases, guarantees).
- Do not "improve" the tone to your taste — respect niche and audience from the brief.

## Next

- Show the user.
- If approved — continue via `/refs`, `/design-lock`, `/blocks`, `/tokens`, `/build`.
- New copy (after client answers open questions) goes back into `inbox/texts/` — rerun `/copy-analyze` for validation.
