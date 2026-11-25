---
name: motion-dictionary
description: >-
  Named vocabulary for motion - 25 effects (entrances, impact, easing curves,
  text, shapes, scene transitions, and the animation principles: anticipation,
  squash & stretch, follow-through, echo trail, count-up, iris) with default
  duration, easing and parameters; fx.js, a dependency-free deterministic
  implementation; and 5 fill-in prompt templates (app launch, showreel,
  product spot, personal intro, App Store style promo); plus web.md, scroll
  choreography for landing pages (line mask reveals, picture unveils, one
  pinned scrub section, smooth scroll, reduced-motion levels) with the
  patterns owners rejected as amateur; timing.md (duration by element,
  distance scaling, easing direction, emotion-to-motion, choreography and
  stagger budgets); styles.md (15 named styles with checkable signatures,
  from flat vector to HUD and pixel art, plus a juror review loop); and
  review.md (what reads as AI slop in a promo film, craft laws, render
  gates). Use whenever writing or reviewing a
  motion spec, a beat table, a prompt asking an AI for an animated video,
  animation code (HTML-to-video, GSAP, Remotion, CSS, Framer Motion), or the
  motion of a web page, and when the user says an animation looks generic,
  "AI-made", "junior", or asks "how do I ask for this motion".
---

# motion-dictionary

"Make a nice video" fails because nothing in it can be checked. A motion spec names the effect, the
element, the time and the curve, so the result can be compared against it frame by frame.

## The spec grammar

One line per element, in this order:

```
<element> <effect> [direction/amount] em <duration> com <easing> [, stagger <gap>] [, no beat <n> / em <t> ms]
```

Example (the "peça assim" pattern):

> Title enters with **slide in** from the left in **0.4 s**, **ease out**. Benefits revealed with
> **stagger 0.15 s**. Ends with a **punch zoom** on the product.

Rules when writing a spec or a beat table:
- Every animated element gets a dictionary name. If no name fits, describe start state, end state,
  duration and curve explicitly, never "smooth" or "dynamic".
- One focus per beat. Three new effects on the same beat is a crowded beat.
- Vary the curve. One easing and one speed for the whole piece is the most common "AI video" tell.
- Fade in alone is the default of every generator. Pair it (fade + slide, fade + blur) or replace it.

## The dictionary

Defaults are starting values, not measurements. `fx.js` uses the same names and defaults.

### Entradas suaves (soft entrances)
| Effect | What happens | Default | Use / avoid |
|---|---|---|---|
| **Fade in** | opacity 0 to 1 | 0.4 s, outCubic | secondary text, backgrounds. Never alone on the hero |
| **Slide in** | travels from an offset to rest | 0.4 s, outExpo, 80 to 160 px | titles, cards, list items. State the direction |
| **Blur in** | blurry to sharp, with opacity | 0.5 s, 24 px blur | calm reveals, numbers. Expensive on large layers in live UI |

### Entradas com impacto (impact entrances)
| Effect | What happens | Default | Use / avoid |
|---|---|---|---|
| **Pop in** | small scale jump past 1 and back | 0.45 s, from 0.6, outBack s=1.7 | one hero element, icons, badges. Not for whole lists |
| **Scale up** | grows to final size, no overshoot | 0.6 s, from 0.2, outExpo | logos, charts, containers |
| **Stagger** | same entrance, items start one after another | gap 0.08 to 0.2 s (0.15 default) | lists, grids, words. Over ~8 items, shrink the gap or group them |

### O ritmo do movimento (curves)
| Effect | What happens | Default | Use / avoid |
|---|---|---|---|
| **Ease in-out** | slow start, accelerates, brakes | inOutCubic | moves between two on-screen positions, camera pans |
| **Overshoot** | passes the target and returns | outBack s=1.70158 (~10 %) | landings with character. One overshoot, small |
| **Bounce** | bounces before resting | outBounce, 0.9 s | playful drops. Rarely fits tech/serious content |

Entrances generally want ease **out** (fast start, soft landing). Ease **in** is for exits. Linear is
only for continuous motion (scroll, rotation, progress) that never starts or stops on screen.

### Texto em movimento (text)
| Effect | What happens | Default | Use / avoid |
|---|---|---|---|
| **Typewriter** | letters appear one by one with a caret | 18 chars/s | commands, code, short prompts. Long text: too slow to read |
| **Word reveal** | words appear in sequence | 0.18 s between words, 0.3 s each | headlines, captions synced to speech |
| **Text swap** | one word replaced by another in the same slot | 0.35 s, old leaves up, new enters from below | "X becomes Y", rotating keywords. Slot needs overflow hidden |

### Formas que mudam (shapes)
| Effect | What happens | Default | Use / avoid |
|---|---|---|---|
| **Draw-on** | a stroke draws itself | 0.8 s, inOutCubic, stroke-dashoffset | arrows, underlines, paths, diagrams |
| **Morph** | one shape becomes another | 0.6 s, inOutCubic | circle to rounded square, button to panel. Paths need equal point counts |
| **Bar grow** | a bar fills to its value | 0.8 s, outExpo | real numbers only. Bar and label from the same curve |

### Transicoes de cena (scene transitions)
| Effect | What happens | Default | Use / avoid |
|---|---|---|---|
| **Mask reveal** | a mask opens to show the content | 0.6 s, inOutExpo, letterbox from the middle | scene openings, image reveals |
| **Wipe** | a moving edge replaces scene A with B | 0.5 s, inOutCubic, accent bar on the seam | before/after, A vs B |
| **Punch zoom** | very fast push-in on the subject | 0.18 s to 1.35x, outExpo, hit sound on the same frame | emphasis on a product, a number, a punchline. Max once per 5 to 10 s |

### Principios de animacao (extension)
| Effect | What happens | Default | Use / avoid |
|---|---|---|---|
| **Anticipation** | pulls back before the move | 15 % of the move, first 35 % of 0.6 s | buttons, jumps, a dial before it fills. Makes the move readable |
| **Squash & stretch** | stretches falling, squashes on contact, keeps volume | 30 %, 0.25 s damped | anything that hits a surface. Origin at the contact point |
| **Follow-through** | secondary parts arrive after the lead, overshooting more | lag 0.05 s per part | grids of dots, hair, cables, a group settling |
| **Echo trail** | fading ghost copies behind a fast move | 4 copies, 0.04 s apart | fast transitions instead of a hard cut. Not on text that must be read |
| **Motion blur** | blur along the movement direction | renderer subframes, or 4 to 12 px directional blur | fast pushes and whips. Frame renderers: average subframes, do not fake with CSS blur |
| **Count-up** | number rolls to its value | 1.2 s, outExpo, locale-formatted | metrics, stars, money. Real numbers only, same source as the voice-over |
| **Iris** | circular mask opens or closes on a point | 0.6 s inOutCubic | photo reveals, scene ends on the subject |

## Prompt templates

[prompts.md](prompts.md) has 5 fill-in templates (app presentation, motion showreel, App Store style launch,
product spot, personal intro), rewritten with dictionary names, durations and a beat order. Start from
one when the user wants a whole video, then adjust the beats; never send a template with the
placeholders still in it.

## Sizing, styles and review

- [timing.md](timing.md): how long, which curve, in what order. Read when choosing numbers for several elements.
- [styles.md](styles.md): 15 styles with the techniques that make each recognisable. Read when the brief names a look.
- [review.md](review.md): "never ship" list, craft laws and render gates. Read before planning a promo or ad, and on the first render.

## Motion on a web page

For a landing page or any scroll-driven page, read [web.md](web.md) before writing code. It covers
the accepted choreography: smooth scroll, line mask reveals, picture unveils, one pinned scrub
section, and a header that hides on scroll. It also lists what owners rejected as amateur: cursor
followers, magnetic buttons, mouse tilt, velocity skew, rainbow accents and glow. Finally, it explains
why motion can look absent on a machine with reduced motion turned on. fx.js is for clock-driven
video; on a page, use GSAP ScrollTrigger as described there.

## fx.js

`fx.js` (next to this file) implements every entry as a pure function of time, no dependencies:

```html
<script src="fx.js"></script>
<script>
  window.__seek = (ms) => {
    const t = ms / 1000;
    FX.apply(title, FX.slideIn(t, 0.2, { from: [-140, 0] }));
    items.forEach((el, i) => FX.apply(el, FX.slideIn(t, FX.stagger(0.8, i, 0.15), { from: [0, 60] })));
    FX.apply(product, FX.punchZoom(t, 2.4));
  };
</script>
```

Contract: `effect(t, t0, opts)` with `t`, `t0` in seconds returns numbers (`x`, `y`, `scale`, `opacity`,
`blur`, `clipPath`, `scaleX`/`scaleY`...). `FX.apply(el, ...parts)` writes them, multiplying opacities. Because nothing
reads a clock, any single frame renders alone and identically, which is what a frame-by-frame
renderer needs and what makes a frame checkable.

Other stacks: the defaults translate one to one. CSS: `cubic-bezier(0.16, 1, 0.3, 1)` for outExpo,
`cubic-bezier(0.34, 1.56, 0.64, 1)` for outBack. Framer Motion: `transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}`,
`staggerChildren: 0.15`. Remotion: call the fx.js functions with `frame / fps`.

## Reviewing motion against the dictionary

For a rendered piece, sample frames at each beat (a contact sheet) and check:
- Can every movement be named? Unnamed motion is usually drift without intent.
- Does each entrance have a direction and a curve with character, or is everything fading in together?
- Do overshoots land once, small? Bounce on serious content?
- Is text readable at phone size at the moment it is still (blur and swaps finish before the read)?
- Does every punch zoom and hard cut have a sound on the same frame?

## Source

Vocabulary organised from the carousel "Dicionario de efeitos Motion" by @omatheusdaia (Instagram).
Prompt templates adapted from the carousel "Prompts para criar motion graphics com o Claude"
(Instagram; author handle not visible in the copy reviewed). Defaults, the spec grammar, the
rewritten templates and fx.js are this skill's own. The block structure
(inputs/direction/structure/build/gotchas/start) and the banned list in prompts.md follow the
patterns collected on prompt-motion.com (gallery of Claude motion prompts curated by @p4nthera_), read
2026-11-05. Easing formulas are the standard Penner curves.
timing.md condenses LottieFiles/motion-design-skill (MIT); styles.md condenses Vincentwei1021/mg-styles-15 (MIT);
review.md rewrites the rules of Tejashmakwana/motionmaxxing (Apache-2.0) in our words. All read 2026-11-20,
adopted because the owner's video pipelines (news Shorts, stream cuts, product spots) render motion every day (Path 2).
