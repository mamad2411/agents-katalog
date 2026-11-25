---
name: long-form
description: Produces a LONG-FORM.md (a blog/article/landing/case-study/tutorial declaring content type, audience, goal, hook, outline, CTA) written outline-first with no padding and substantiated claims; primes the editorial + accessibility gates. Use to write a long-form piece from the brief.
---

# long-form

The long-form producer of the content domain — it writes a `LONG-FORM.md`: a blog post, article, landing
page, case study, or tutorial, declaring its **content type**, **audience**, **goal**, the **hook**, the
**outline**, and the **CTA**. The bar is the three ways long-form fails: **padding** (a section with no
nameable purpose), **unsubstantiated claims**, and **AI-isms**. So it is written outline-first, every section
earns its place, every claim is cited or flagged, and the prose carries the anti-slop discipline. It binds the
pack's `long-form` sub_target and verifies by **Review** (judged against the brief) plus **Audit** for any
factual claim. It writes the piece; it does not set the brand voice (`content-brief`).

## What this does / does not do

Does: resolve the `long-form` sub_target, write a `LONG-FORM.md` (content type + audience + goal + hook +
outline + CTA + the prose, claims sourced), grounded in the brief, and a receipt. Does not: set the brand
voice/audience/structure (that is `content-brief`), write UI microcopy (`copy`), write campaign/positioning
copy (`marketing-copy`), write reference docs (`documentation`), or issue the gate verdict (the
editorial/accessibility/compliance gates do — this primes them).

## When NOT to use

- The work is deciding the brand voice / audience / structure — that is `content-brief` (this consumes it).
- The work is short in-product UI text — that is `copy` (microcopy), not a long-form piece.
- The work is campaign/positioning copy — that is `marketing-copy`; long-form is the article, not the ad.
- The work is task-oriented reference documentation (diataxis) — that is `documentation`.
- A current `LONG-FORM.md` still fits and nothing changed — edit it; do not rewrite a published piece.

## Reference Routing

| Situation | Reference |
|---|---|
| The LONG-FORM.md contract template | `references/long-form-template.md` |
| Per-sub_target must-declares · overlay · vocabulary | `../acceptance/sub-targets.md` · `../acceptance/overlay.md` · `../vocabulary.md` |
| The upstream content contract (voice / audience / structure) | `BRIEF.md` / `STYLE-GUIDE.md` / `VOICE.md` |

## Inputs

- The content type (blog/article/landing/case-study/tutorial) + the topic, and the goal the piece serves.
- `BRIEF.md` / `STYLE-GUIDE.md` / `VOICE.md` if present — the audience, voice, and structure.
- The sources for any factual/market claim the piece will make.
- The content domain pack (`../vocabulary.md`, `../acceptance/`) + `state/intake.json`.

## How to do it

1. **Declare the frame**: content type, audience, goal, and the CTA the piece drives toward. The goal is the
   one thing the reader should do or believe after reading.
2. **Write the hook**: the opening that earns the next paragraph — a tension, a question, concrete stakes. A
   hook that could open any article is not a hook.
3. **Outline before prose**: the section structure, each section with a nameable purpose tied to the goal.
   Outline-first is the content ordering rule; a section you cannot name the purpose of is cut.
4. **Draft to the outline**: write each section to its stated purpose, leading with the point. Key message
   before supporting detail; facts and sources before claims.
5. **Substantiate claims**: every factual or market claim is cited or sourced; an unsourced claim is flagged
   as opinion/assumption, not stated as fact. A regulated claim routes through the compliance gate + Audit.
6. **Strip the AI-isms**: no "delve / tapestry / robust / leverage / comprehensive", no hedging preambles, no
   "not X but Y" reversal padding, no em-dash as a tic. Say it once, plainly (the editorial gate).
7. **Write `LONG-FORM.md`** from `references/long-form-template.md`; verify reading level + structure
   (accessibility).

### Gate (before marking complete)

- [ ] Content type + audience + goal + hook + outline + CTA are declared (outline before prose).
- [ ] Every section has a nameable purpose tied to the goal; no padding.
- [ ] Every claim is cited/sourced or flagged as opinion; regulated claims routed to compliance + Audit.
- [ ] The anti-AI-slop pass is applied (no buzzwords, no hedging, no reversal padding).
- [ ] Plain language at the audience's reading level; scannable structure; inclusive language (accessibility).

A gate failure is fixed before lock, not waived — these mirror the editorial/accessibility/compliance gates.

## Output

- **LONG-FORM.md** at the product root (or `content/LONG-FORM.md`; rename to the piece) — persistence:
  **Spec-Anchored**. Frontmatter (content type · audience · goal · hook · CTA) · the outline (nameable
  purposes) · the prose · sources for claims.
- **receipt** (`<workspace>/receipts/long-form-receipt-<ts>.json`): base schema + `sub_target`,
  `content_type`, `audience`, `goal`, `sections`, `claims_sourced`, `long_form_path`, `gate_checks`.
  persistence: Spec-Anchored.

## Proactive Triggers

- **A section with no nameable purpose**: cut it or give it one — padding is the long-form failure mode the
  editorial gate catches.
- **An unsourced factual claim**: cite it or flag it as opinion; a stated-as-fact claim with no source fails
  the Audit.
- **AI-isms in the draft** ("delve", "tapestry", "it's not just X, it's Y"): rewrite plainly; the anti-slop
  pass is part of the editorial bar, not optional.
- **A generic hook**: replace it with one specific to this piece's tension — a hook that fits any article
  earns nothing.

## Completion Criteria

**Done when:** a `LONG-FORM.md` exists with its frame declared (type/audience/goal/hook/outline/CTA), every
section purposeful, every claim sourced or flagged, the anti-slop pass applied, at the audience's reading
level; a long-form receipt records the gate checks. Verified by Review (+ Audit for claims).

**Not done if:** the outline came after the prose; a section has no purpose; a claim is stated as fact
unsourced; AI-isms remain; or the reading level/structure misses the audience.

**Next step:** the editorial + accessibility gates judge the piece (Review); claims are Audited; the piece
ships / localizes (`localization`); `content-brief` is the upstream voice contract.

## Related Skills

- **content-brief**: sets the audience, goal, voice, and structure the piece is written to. content-brief
  decides; long-form writes the piece. Run content-brief first when the frame is the gap.
- **copy**: short in-product UI microcopy. long-form is the article; copy is the button label — different
  lengths, different jobs.
- **marketing-copy**: campaign/positioning copy. long-form is editorial (the article); marketing-copy is the
  funnel — route the ad there.
