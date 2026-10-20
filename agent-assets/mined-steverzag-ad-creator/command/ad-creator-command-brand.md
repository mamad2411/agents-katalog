---
description: Create or edit a client profile — colours, fonts, voice, product lines — then recompile brand.css into every ad using it
argument-hint: [brand and what to change, or "create <name> from <url>"]
---

Work on a client profile: **$ARGUMENTS**

If that's empty, ask which brand and what should change. List what's in
`brands/` so the answer is easy.

A profile is more than styling: `colors`, `fonts` and `radius` compile into
`brand.css`, while `business`, `logo` and `voice` are read by the skills that
plan campaigns and write copy. Both halves live in `brands/<name>.json`.

## 0. Given a URL, extract — don't interview

If the arguments name the client's website, read it and fill in as much of the
profile as it supports. **One fetch here is what stops `/campaign` asking later
for things the project has already seen.**

Take both halves in the same pass:

- **Styling** — the palette and font stacks. Fetch the *stylesheet*, not the
  rendered page: a markdown conversion strips the CSS, and modern sites declare
  the whole palette as `--color-*` custom properties that can be read exactly.
- **Business** — what they are, where they trade and any licensing limit, the
  languages they publish in, their socials, and **every product or service line
  with its URL**. That line list is what a campaign gets scoped to.

Then say what you couldn't find and ask only for that. Fonts are the usual gap:
identify the families from the CSS, confirm the licence permits embedding, and
download real `woff2` files into `brands/assets/<brand>/`.

**Stable facts only in `business`.** Prices, offers, response times, savings
figures and testimonials are *not* profile data — they go stale silently and
every future campaign would inherit the stale copy. `/campaign` fetches those
fresh from the line's URL, dated to that run. See the skill.

## 1. Edit the JSON, never the CSS

Brands live in `brands/<name>.json`. `ads/<slug>/brand.css` is **generated** —
hand edits there are silently reverted by the next `pnpm brand`, which is a
confusing way to lose work.

For a new brand, or for structural changes to colours, fonts, logo, voice or
the business block, invoke the **`brand-setup`** skill; it owns the
field-by-field guidance.

Compiled tokens are a fixed set — `bg`, `fg`, `muted`, `accent`, `onAccent`,
`surface`, the two font stacks, two radii. A brand with more colours than that
has to map them onto those roles; extra shades belong in an ad's own `ad.css`
or in an asset, not invented as new tokens.

Fonts listed under `fonts.faces` must exist in `brands/assets/<brand>/`. A
variable font can declare a range (`"weight": "400 700"`). No CDNs — download
the file into the repo.

## 2. Recompile into every ad that uses it

**Only if you touched `colors`, `fonts` or `radius`.** Those are the fields that
compile. An edit confined to `business`, `voice` or `logo` leaves every
`brand.css` correct — skip to step 4 and say you skipped it.

For the compiled fields, **this is the step that gets missed.** `pnpm render`
does not recompile `brand.css`, so an edited brand JSON changes nothing on
screen until you do this — the ad exports with the old tokens and looks fine
while being wrong.

Recompile the whole fleet, not just the ad in front of you — a brand edit that
lands in one ad and not its siblings is worse than not making it:

```bash
pnpm brand --all <name>     # every ad using this brand
pnpm brand --all            # every ad, each from its own brand
pnpm brand ads/<slug> <name>  # one ad, or to move it onto a different brand
```

`pnpm render` and `pnpm dev` both warn when an ad's `brand.css` is stale, so you
don't have to track this by hand — but they won't fix it, by design.

## 3. Re-render and look

A styling change is visual, so it isn't done until you've seen it. Follow
`/render`, then `Read` at least one exported PNG per affected ad.

Colour changes are where this matters most: a `muted` tone tuned for a light
ground goes illegible on a dark one, and an `accent` with poor contrast against
`onAccent` fails on the CTA — the one element that must stay readable. Check
those in the render, not in the hex values.

**No ads use this brand yet?** Then there's nothing to recompile and nothing to
re-render — but a profile that has never been rendered is unverified, and the
things that break are invisible in the JSON: a font that silently falls back,
or a subset missing the accented characters the copy needs. Scaffold one
throwaway ad, put representative copy in it, render, look, and remove it. Say
that you did.

## 4. Report

- What changed in the JSON, split into what compiles and what doesn't
- Which ads were recompiled, and which you re-rendered — or that there were
  none, and how you verified instead
- Anything that now fails contrast, with the format it fails in
- Any ad using this brand you did **not** recompile, and why
- For a profile built from a URL: what you extracted, what the site didn't
  give up, and anything you deliberately left out of `business` as too
  volatile to cache
