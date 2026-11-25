---
name: landing-md
description: >
  Use when paid traffic needs somewhere to land and there is no page yet, or the existing
  page does not match the ad. Also when a landing must be one self-contained file that can be
  hosted anywhere, and must pass a pre-launch check before any money is spent on it.
  Triggers on: "build my landing page", "landing for my campaign", "página de captación",
  "landing de captación", "necesito una landing", "landing that matches my ad".
  Self-contained: no other skills required.
version: 0.2.0
author: GrowthLab (growthlab.mx)
license: MIT
---

# landing-md

> GrowthLab-original content. MIT licensed (see repo `LICENSE`).

> **Purpose:** Produce the page your ad clicks deserve to land on. `product-marketing.md`
> gives the words, `design.md` gives the look — this skill turns both into one
> `index.html` you can host anywhere — a marketing platform, a CMS, a static host, a plain
> server — with the
> lead form where it converts and a QA gate before any paid traffic touches it.

**No skill dependencies.** This skill never calls another skill. It *reads* two optional context
files, `product-marketing.md` and `design.md`, and works without them — see Step 0. It pairs with
`content-humanize` as the copy gate; if you do not have it, the embedded checklist in Step 2 covers
the essentials.

---

## The set

This skill is one of five in the same repo. Two of them write a context file; three read it.

`product-marketing-md` writes `product-marketing.md` (what you sell, to whom, why they buy).
`design-md` writes `design.md` (how you look and how you sound). Those two files are read by
`landing-md`, `social-calendar` and `content-humanize`.

**You need none of them to run this one.** They are separate downloads from
[github.com/jeremidelacruz/growthlab-skills](https://github.com/jeremidelacruz/growthlab-skills),
and if this file is all you have, everything below still works.

---

## Why this works

Most landing pages fail before the visitor reads a word, for one of two reasons:

1. **The page doesn't match the ad.** Someone clicked a promise; the page greets them with a
   different one. They leave in seconds and the ad platform charges you anyway.
2. **The form is buried.** Real session recordings show scroll dying at 30–40% of page depth.
   A form parked at the bottom is invisible to most visitors even when everything else is right.

This skill builds against both failures by default: the H1 mirrors the ad, and the form lives
in the first viewport. Not as an A/B test idea — as the starting point.

### The two files this page is built from

| File | Answers | Written by |
|---|---|---|
| `product-marketing.md` | What you sell, to whom, why they buy, how they talk | `product-marketing-md` |
| `design.md` | How you look and how you sound | `design-md` |

Without them this skill still builds a page — it just has to interview you first, and the page
is only as good as the answers you improvise. With them, Step 0 is a file read and every later
step inherits decisions you already made once.

---

## The source rule

Everything you write about the business, its customers or its competitors has to trace back to
something you were given. **Not just numbers. Claims too.**

A claim is anything a reader could check and find false:

- how the service works, or what is included in it
- a security, safety or privacy property ("the connection is read-only")
- a turnaround time, a guarantee, a policy
- what a competitor believes, charges or is bad at
- what the customer feels, fears or wants

Three moves, in this order:

1. **Cite it.** It came from a context file or the person told you. Use it.
2. **Cut it.** No source? Delete the sentence. Replacing it with a vaguer sentence is not a fix.
3. **Mark it.** If the piece structurally needs something you were not given, write it and mark
   that line `[ASSUMED — confirm before publishing]`.

**Nothing unsourced and unmarked ships.** A marked guess is a question for the owner. An unmarked
guess is a promise they get held to.

> This rule is wider than it used to be for a reason. In testing, a run of this skill published
> "the connection is read-only" about a fintech product, and another asserted that a mechanic
> keeps every removed part on a labeled tray. Neither is a number, so a numbers-only rule waved
> both through. Both are promises somebody would have been held to.

### When you cannot ask

If you are running unattended, or inside someone else's workflow, and the questions below cannot
be answered: **do not stop, and do not assume silently.** State the questions, answer each with
the most defensible assumption you can support, mark them, and put them in an `## Assumptions`
block at the top of what you deliver. The reader needs to see the guesses before they see the work.

---

## Process

### Step 0 — Read the two files

Read `product-marketing.md` and `design.md` from the working folder. Extract: ICP, offer,
differentiator, customer language, tone rules, palette (exact hex), fonts, logo rules.

- Missing `product-marketing.md` → stop, run the `product-marketing-md` skill first.
- Missing `design.md` → stop, run the `design-md` skill first.
- Never invent what the files don't say. See "The source rule" above.

**Validate before you trust.** A file that exists is not a file that is correct. Check every
value you pulled:

- **Every hex matches `^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$`.** A value that fails
  is corrupt, not missing — CSS drops an invalid custom property silently and you ship a page
  with an unstyled CTA and no error anywhere.
- **Every font has a name you can look up**, and you know whether it is free, licensed, or
  neither.
- **Every referenced asset path exists.** A logo rule pointing at a file that isn't there is a
  rule you cannot follow.

Anything that fails: **stop and surface it.** Say which value, in which file, and what is wrong
with it. Do not repair it by guessing the intended value, and do not pass it through.

### Step 1 — Capture the campaign inputs

Three questions before writing anything:

1. **What is the offer on THIS page?** (one offer per page — a page that sells two things sells none)
2. **Where does the traffic come from?** (Meta ad, Google ad, organic, QR at an event)
3. **What does the ad say?** Paste the actual headline/primary text. The page must repeat its
   promise — this is *message match*, and it is the single highest-leverage decision on the page.

### Step 2 — Write the copy (before any HTML)

**Above the fold:**
- **H1** — max 12 words, mirrors the ad promise. Formulas: outcome-first
  ("[Result] sin [pain]"), audience-first ("Para [ICP]: [benefit]"), problem-first
  (the question that names the pain).
- **Subheadline** — one or two sentences, adds one proof element (a number you can back, a
  timeframe, a credential). No adjectives doing the work facts should do.
- **CTA button** — `[Action verb] + [what they get]`: "Descargar la guía", "Agendar mi
  diagnóstico". Banned: "Enviar", "Registrarse", "Comenzar", "Submit".
- **The form itself renders here**, in the hero, when traffic is paid and cold. 3 fields
  maximum for a top-of-funnel offer.

**Section order:** hero → problem in the customer's own words → solution as benefits →
how it works → proof → FAQ → final CTA. Adjust to the offer, keep the logic.

**Microcopy:** visible label on every field, errors that say the cause and the fix, and a
thank-you message that says what happens next and when.

**Humanization gate.** If `content-humanize` (this repo) is installed, run the full rubric
(threshold 42/60).
If not, the minimum embedded pass: no em dashes in the copy, no "no es X, es Y" constructions,
no sentence openers like "En un mundo donde", vary sentence length, cut every adverb that
survives a second read, and read the hero out loud — if it sounds like a press release,
rewrite it.

**Language rule:** the page's copy is written in the language of the ICP as documented in
`product-marketing.md` (for GrowthLab-method users in México that's Spanish, es-MX — no
Spain-isms, no unadapted anglicisms).

### Step 3 — Hero image

- **Default: a free stock library** that permits commercial use without attribution. Search in
  English; pick an image that matches the ad creative so the visual promise carries through.
  Check the licence before you ship — "free" and "free for commercial use" are not the same thing.
- **Better than stock:** a real photo of you, your product, or your work. Real beats pretty.
- **Specs:** WebP (or AVIF), hero ≤200KB, explicit `width`/`height` attributes,
  `loading="eager"` on the hero, `loading="lazy"` on everything below the fold.
- If you hold a paid stock subscription, its assets are licensed to YOUR account — fine on your
  own pages, never redistributed as raw files or handed to a third party.

### Step 4 — Build one `index.html`

Build rules, in order of importance:

1. **Single self-contained file** — CSS inline in `<style>`, no external frameworks, no CDN
   dependencies. It must open from a double-click and survive being pasted into any host.
2. **Brand tokens once** — declare the palette from `design.md` as CSS custom properties in
   `:root`; no raw hex below that line.
3. **Mobile-first** — base styles at 375px, one breakpoint at 768px. CTA full-width on mobile,
   ≥48px tall. Form inputs `font-size: 16px` minimum (stops iOS zoom). No horizontal scroll.
4. **Form in the first viewport** (paid cold traffic default) with hidden UTM fields
   (`utm_source/medium/campaign/content/term`) populated by a small JS snippet from the URL —
   plus `fbclid`/`gclid` capture if present.
5. **The form has to go somewhere.** A page that cannot capture a lead is not a landing page,
   and this is the step most often left half-done. Ask for the destination before you build; if
   you cannot ask, pick one, implement it, and mark it `[ASSUMED]`:
   - a form endpoint URL (`<form action="…" method="post">`), or
   - an embed/script the platform provides, or
   - `mailto:` as an explicit stopgap, labelled as one.

   **Never invent a plausible endpoint.** A made-up URL on a domain you did not verify is worse
   than an obvious stopgap: it looks wired, so nobody checks it, and the page captures zero while
   appearing to work. If you were not given a destination, use `mailto:` — it is unmistakably
   provisional, and it still delivers the lead.

   Whichever it is, say it out loud in your handoff. A `TODO` buried in the HTML is not a handoff.
6. **Name the conversion event.** Declare it once and use it in both the page and the handoff —
   default `dataLayer.push({event: 'lead_submit'})`. If you invent a different name and never say
   so, the tag manager trigger in Step 6 will not match and the page will look like it converts
   zero.
7. **Performance** — target LCP under 2.5s: one optimized image above the fold, reserve space for
   anything that loads late (CLS <0.1).
8. **Fonts: pick one and say which.** Rule 1 forbids CDN dependencies and `design.md` may specify
   a web font. Those conflict, so decide explicitly rather than silently dropping the brand:
   - **System stack** — fastest, no dependency, and the page does *not* render in the brand
     typeface. Say so in the handoff.
   - **Embed as base64** in the `<style>` block — keeps rule 1 and keeps the brand, costs weight.
   - **Link the font CDN** — breaks rule 1 knowingly. Acceptable if the page will always be
     online; never for a file meant to open from a double-click.

   `font-display: swap` only means something if a web font actually loads. Do not write it into
   a page that has none.
9. **A thank-you state** — either a `gracias.html` or an inline confirmation block, saying what
   happens next. The conversion event from rule 6 fires here.

### Step 5 — QA gate (do not send traffic without it)

- [ ] H1 repeats the ad's promise — read them side by side
- [ ] Offer and form visible without scrolling on a 375px screen
- [ ] ONE call to action (repeated is fine; competing is not)
- [ ] Form ≤3 fields, visible labels, keyboard types match inputs
- [ ] Text contrast ≥4.5:1, tap targets ≥48px, no horizontal scroll
- [ ] Every number on the page is one you can defend. No invented stats, ever.
- [ ] **Every claim on the page is one you can defend.** Walk the FAQ, the how-it-works steps and
      the thank-you copy line by line: turnaround times, "read-only", "secure", "cancel anytime",
      what is included. If a line is not in the context files and nobody told you, cut it or mark
      it. The FAQ is where invented claims collect, because the section demands answers the
      context files rarely contain.
- [ ] Every hex and font from `design.md` passed the Step 0 validation
- [ ] The form posts somewhere real, and you said where in the handoff

**Write the filled gate into the output folder** as `qa-gate.md`, with the date and who ran it.
A checklist that lives only in a chat reply is not evidence — the next person to open the folder
has no way to know it was ever run.

**Assumptions have to be visible in the page, not only in a sidecar file.** An HTML comment is
invisible to whoever opens the page, and a separate `assumptions.md` is invisible to whoever does
not. While any assumption is unresolved, render a plain banner at the top of `index.html` saying
what is unconfirmed and that the page is not ready for paid traffic. Deleting that banner is the
last step before launch, and someone does it on purpose.

**An unrun check is a failure, not a warning.** If you could not measure contrast, or could not
open the page at 375px, the box does not get a partial mark — it gets a fail with the reason.
"Verified by construction" is a calculation, and this gate exists because calculations about
rendered pages are wrong often enough to matter.

### Step 6 — Publish and wire

Host the file anywhere that serves static HTML. Then wire the
conversion: one well-built form-submit trigger in Google Tag Manager can feed Meta and Google
at the same time — set it up once, verify it in both platforms, and only then activate spend.

---

## Output

- `index.html` — the complete landing page, self-contained
- `gracias.html` (or inline thank-you state) — with the conversion event
- A filled QA gate (Step 5) — the page ships only when every box is checked

---

## What this skill does not do

It builds **one page for one offer**. Deliberately, it stops there:

- No aesthetic direction system — it follows `design.md` and applies sane defaults where that
  file is silent. Art direction is a judgment call, not a table.
- No A/B testing, no variant generation, no experiment design
- No analytics wiring beyond "put a form-submit trigger in your tag manager and verify it fires"
- No multi-step forms, no quizzes, no calculators, no dynamic personalization
- No page speed budget beyond keeping the hero image small
- No iteration loop: it does not read session recordings, heatmaps or form-abandonment data and
  tell you what to change next

A page that converts is the start of the work, not the end of it. If the page is live and the
numbers are not moving, the answer is in the data, and reading that data is a different job
than writing HTML. It happens to be ours: [growthlab.mx](https://growthlab.mx).

---

## Credits and inspiration

GrowthLab-original text. While writing our internal landing tooling we studied and admired
(without re-hosting): **UI/UX Pro Max** by Next Level Builder (MIT) for its style/palette/
typography decision databases, **impeccable** (Apache 2.0) for its anti-slop HTML production
standards, and **huashu-design** by alchaincyf (MIT) for its self-contained HTML craft.
The copy gate pairs with **`content-humanize`** (this repo), whose scored audit loop is itself
adapted from **humanizalo** by Hainrixz (github.com/Hainrixz/humanizalo, MIT).

### About GrowthLab

These skills are the free half of a working method. [GrowthLab](https://growthlab.mx) is a
paid-media agency in México that runs its delivery on Claude Code — the context files, the
gates and the QA you just used are how our own client work ships. If you would rather have
the campaigns, the pages and the content *run for you* on top of this method, that is the
paid half: [growthlab.mx](https://growthlab.mx) · hola@growthlab.mx.
