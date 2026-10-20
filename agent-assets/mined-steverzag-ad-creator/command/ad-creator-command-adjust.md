---
description: Apply a requested change to an existing ad — edit, re-render, and verify by looking at the output
argument-hint: [what to change, e.g. make the headline bigger at 9x16]
---

Apply this change: **$ARGUMENTS**

If that is empty, ask what to change. Don't guess a change nobody asked for.

## 1. Resolve the target

Which ad, in this order — stop at the first that answers it:

1. A slug named in the request (`elevia-seguro-resbalon: …`, `the ugc one`)
2. The ad this conversation has been working on
3. The only folder in `ads/`

Otherwise **ask**, listing what's in `ads/`. Guessing wrong here wastes a render
and edits the wrong files.

Read the ad's `ad.config.json`, `index.html`, `ad.css` and `ad.js` before
editing. If its source files are missing and only `out/` survives, say so — the
ad has to be rebuilt with `/build-ad`, not adjusted.

## 2. Decide where the change belongs

The most common mistake is fixing the right thing in the wrong file.

| The request is about | Edit | Then |
|---|---|---|
| This ad's copy, layout, timing | `ads/<slug>/` | — |
| Real imagery replacing a placeholder | `ads/<slug>/assets/` | swap the markup to point at it |
| Brand colour, font, logo, voice | `brands/<brand>.json` | `pnpm brand ads/<slug> <brand>` |
| Behaviour every ad shares | `runtime/ad.css` or `runtime/ad.js` | note the blast radius |
| Formats, duration, fps, audio | `ads/<slug>/ad.config.json` | — |

**Adding assets is an adjustment, and it's the normal path.** Ads are generated
against placeholder treatments, so the files arrive here. Put them in that ad's
`assets/`, reference them relatively (`assets/hero.jpg`), and replace the
placeholder element rather than layering over it. A `<video>` also needs
`ctx.video(el, { start })` or it exports as a frozen first frame. If a file the
request names isn't on disk, say so — a wrong path renders a hole and only warns
in the render log.

`brand.css` is generated. Hand edits there are silently reverted by the next
`pnpm brand` — change the brand JSON and recompile instead.

A change that only looks wrong at one ratio is per-ratio work: an attribute
selector (`.ad-stage[data-ratio='9x16'] …`), never a second file and never a
value that fixes 9:16 by breaking 1:1.

## 3. Ask only what actually changes the work

Ask when two readings would produce materially different ads — "make it punchier"
(copy, or type scale?), "use blue" (this ad, or the brand everywhere?), a new
claim with no source. Ask in one short block, then proceed.

Don't ask what you can infer, and don't ask permission to start. A concrete
change the user can react to beats a questionnaire.

## 4. Apply it — and only it

Change what was asked and what that change genuinely requires. Adjusting a
headline size is not licence to rewrite the copy, restyle the CTA, or "improve"
the layout on the way past. If you spot something else worth fixing, finish the
ask, then say what you noticed.

Hold the invariants — they are what make the ad renderable:

- Size in `--u`, never `px`
- Content inside `.ad-safe`
- Animation on the paused GSAP timeline; no CSS transitions or `@keyframes`
- Nothing non-deterministic in a timeline
- Text over imagery sits on a scrim
- No CDNs — assets and libraries stay local

**The claim boundary still applies.** New copy may not introduce a statistic,
price, rating, guarantee, award or testimonial the user hasn't supplied — not
even one that sounds safe. If the change needs proof you don't have, use a
visibly fake placeholder (`"[rating]"`) and name it in your report.

Honour the brand's `voice.avoid` and any **Do not say** list in the brief.

If the request is "make a version that…" rather than "change this", that's a
variant: a sibling folder with a shared prefix that differs in exactly one
element. See the `create-ad` skill.

## 5. Re-render and look

```bash
pnpm render ads/<slug>
```

Then `Read` the exported PNG — every format the change could touch, not just the
first. Layout bugs are routinely invisible in source and obvious in a render,
and exit code 0 says only that the encoder ran.

For motion, grab the affected beats instead of re-encoding repeatedly:

```bash
node .claude/skills/critique-ad/scripts/frames.mjs ads/<slug> --at 0,4,8 --thumb
```

Iterate until the change is actually there in the pixels. Skip rendering only if
the request said to.

## 6. Report

- What you changed, in which files, and why there
- What it looks like now — the honest read, not a restatement of the request
- Anything you deliberately left alone that the user might have expected to move
- Any placeholder, or any claim you declined to write

If the change made something else weak, say so and offer the fix. Don't apply it
uninvited.

---

Scope note: this command applies a change the user asked for. Grading an ad's
design against a rubric and fixing what's weak unprompted is the `critique-ad`
skill — reach for that when the request is "is this any good?" rather than
"change this".
