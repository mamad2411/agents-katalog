---
description: Scaffold and author an ad's files from a brief — stops before rendering
argument-hint: [a campaign brief path, and/or overrides e.g. "ratios 9x16 and 1x1"]
---

Build the ad files. **Stop before rendering** — `/render` and `/verify` own that.

Arguments — a brief path, overrides, or both (may be empty): **$ARGUMENTS**
Overrides win over the brief. Say which fields they changed.

## 1. Get the brief

A `campaigns/*/briefs/` path in the arguments, merged over that campaign's
`campaign.md`; otherwise the request and this conversation. Validate it as
`/brief` does — required fields, contradictions, the claim boundary.

**A missing required field is a question, not an assumption.** Ask for Format,
Angle, Pain point, Hook or Script if the conversation hasn't settled them.
Everything else you may infer from the brand profile and the request, saying
what you assumed — don't turn a one-line request into a questionnaire.

A campaign brief carries a `Persona` and a `Pain point`. They aren't decoration:
they decide the vocabulary and which objection the copy clears. Read the
concept's row in the campaign's `strategy.md` before writing.

## 2. Settle angle and format before markup

The **angle** is the argument (problem-solution, testimonial, educational…) and
it decides structure. The **format** is the artefact. They're independent.

Read `references/angles.md` for what this angle requires, then the file for this
format — `image.md`, `carousel.md`, `video.md` or `ugc.md`. The structure is
most of the quality.

Some angles can't be built from a thin brief: `social-proof` with no real
numbers, `demo` with no assets. Say so and propose another rather than filling
the gap with placeholders.

## 3. Scaffold

```bash
pnpm new <format> <name> --brand <brand> --formats <ratios>
```

This fails if `ads/<slug>` already exists — pick another slug or clear the old
one deliberately. It sets only name, type, brand and formats.

**Duration is not applied by scaffolding.** If the brief gives one, edit
`duration` in `ad.config.json` and match the timeline to it, or the ad renders
at the template's default length.

If the brand doesn't exist yet, run `/brand` first, or omit `--brand` for
neutral tokens.

## 3a. Assets

An ad's own files live in `ads/<slug>/assets/`, created empty by the scaffold and
referenced as `assets/hero.jpg`. The brand's logo and fonts are shared and
referenced where they sit — `../../brands/assets/<brand>/logo.svg`.

**Most ads are generated before their imagery exists.** `Assets: none` is normal;
build the placeholder treatment and say so. Real files are added afterwards with
`/adjust`, which drops them into that ad's `assets/` and re-renders.

**Check every file the brief names actually exists before you write the markup.**
A missing or misspelled path still exports — a 404 image can't stop a screenshot
— so the ad renders with a hole in it. `pnpm render` names the offending source
(`⚠ n asset(s) failed to load`), but that's a warning in a log, not a failure,
and it's easy to scroll past. If a named file isn't there, say so and build the
placeholder treatment rather than pointing at nothing.

`<video>` needs `ctx.video(el, { start })` as well as a `src`, or it exports as
a frozen first frame.

## 4. Write it

Invoke the **`create-ad`** skill and follow it — it owns the craft. Read
`references/copywriting.md` before the copy and `references/visual-design.md`
before the layout.

The template is a starting structure, not a constraint. Replace the markup
freely; keep the invariants:

- Size in `--u`, never `px`
- Content inside `.ad-safe`
- Animation on the paused GSAP timeline — no CSS transitions or `@keyframes`
- Nothing non-deterministic in a timeline
- Text over imagery sits on a scrim
- No CDNs — assets local, `brand.css` generated

The Script is the source for on-screen copy — tighten it to ad length, keep its
substance and its specifics. Don't replace the user's Hook with your own; build
it as written and say why you'd change it.

A layout tuned at one ratio does not scale to another. Do the per-ratio work now
with attribute selectors, not a second file — you'll confirm it at `/verify`.

## 5. Hand off

Report where the ad is, what you assumed, and any placeholder standing in for
proof you weren't given. If this came from a campaign brief, set that concept's
`Status` to `built` in the campaign's `strategy.md` production map.

Then say what's next: `/render` to export, or `/verify` to export and check the
pixels. **You have not looked at this ad yet** — say that plainly rather than
implying it's finished.
