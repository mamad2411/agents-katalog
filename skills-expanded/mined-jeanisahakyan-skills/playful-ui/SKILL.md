---
name: playful-ui
description: >-
  Design philosophy and concrete interaction recipes for making an interface feel
  like a playful, tactile, alive TOY instead of a sterile tool — bright committed
  palettes, generous rounding, oversized rounded type, springy/liquid motion,
  felt presence, point-of-touch reactions, ephemerality, haptic+sound feedback,
  and delightful discovery. Use this whenever the user wants UI/UX that feels
  playful, delightful, tactile, "alive", bouncy, toy-like, organic, or
  characterful — when they say things like "make it feel fun / less corporate /
  more alive / more delightful", "add personality", "it looks too templated /
  flat / generic", or when designing onboarding, empty states, reactions,
  presence, loading, transitions, or any moment that could carry delight. Not
  limited to chat — applies to any product surface, in any UI framework
  (SwiftUI, React/React Native, Flutter, web/CSS). Reach for it even if the user
  doesn't say "playful" but is clearly chasing a joyful, characterful feel.
---

# Playful UI — designing interfaces that feel like toys, not tools

Most software follows a predictable, safe rhythm: neutral grays, tight radii,
restrained fades, everything optimized to get out of the way. It's effective and
forgettable. This skill is the other path: interfaces that are **playful,
tactile, and alive** — where the product has a body, interactions have weight,
and small moments carry delight.

The thesis in one line: **a product can be a toy.** When an interface is fun to
touch, people touch it more. The craft is making digital things feel physical,
responsive, and a little mischievous — without tipping into noise.

This is a stack-agnostic design philosophy. The recipes below name *what* to do
and *why*; translate the mechanics into whatever framework you're in (SwiftUI
springs, RN Reanimated, Flutter implicit animations, CSS transitions + Web
Animations). Code snippets are illustrative, not prescriptive.

## When this applies (and when it doesn't)

Reach for this when the goal is **feel**: onboarding, empty states, reactions,
presence, celebration moments, loading/discovery, transitions, a brand's
personality surface. It shines on consumer, social, creative, and "delight-led"
products.

Be deliberate where **density, speed, or trust** dominate — dashboards, data
tables, settings, financial/medical flows, dense enterprise tools. There, borrow
only the *restrained* moves (a soft spring on a toggle, a rounded empty state)
and skip the maximalist ones. Playfulness is a seasoning; a whole meal of it is
exhausting. The skill is knowing *where* to spend delight.

## The two layers

1. **Aesthetic foundations** — the visual system that makes everything read as
   one playful world (palette, shape, type, depth, motion). Read
   `references/aesthetic-foundations.md`.
2. **Interaction patterns** — the named, reusable recipes that give the product a
   body: presence, point-of-touch reactions, ephemerality, physical feedback,
   delight triggers, playful discovery, ritual gates, fluid morphs, a
   sound+haptic bus. Read `references/interaction-patterns.md`.

Pull the foundations first (they're cheap and set the whole tone), then layer in
one or two interaction patterns where they earn their keep. **Don't ship all the
patterns at once** — pick the moments that matter and make those unforgettable.

## The core moves (summary — details in the references)

**Commit to a mood.** The deadliest default is hedged neutrality. Pick a strong,
coherent world — bright and sunny, or deep and neon, or warm and papery — and go
*all in* on it. A committed palette of a few saturated hues plus one near-black
and two grays beats fifteen timid tints. Light-mode-only, done with conviction,
reads as more intentional than a wishy-washy adaptive theme.

**Round everything, generously.** Big corner radii (cards ~24–32, bubbles ~30+,
pills fully round), squircle avatars. Sharp corners read as "serious software";
round reads as "friendly object you can hold."

**Make type a voice.** Oversized, bold, *rounded* typefaces for the things that
matter (headlines, chat text at 28–34pt). Type that's big and round feels spoken,
not printed.

**Depth should be soft.** Low, soft shadows (black ~8–12% opacity, large blur,
small y-offset) — things float a little, nothing is heavy or hard-edged.

**Organic shapes beat rectangles.** A blobby "drip" tail on a bubble, a jiggling
mascot, a liquid morph — one signature organic detail gives the whole UI a
personality fingerprint. Find yours.

**Motion is springy, never stiff.** Spring everything (`response ~0.3–0.4`,
`damping ~0.7`); things overshoot slightly and settle, breathe when idle, react
to touch. Linear/easeInOut is the sound of a tool; springs are the sound of a
toy. This is the single highest-leverage change — if you do one thing, replace
your easing curves with springs.

**Give interactions a body.** The best moments are *felt*: a haptic tap, a tiny
sound, an object that physically fills/shakes/drains in response to what you do.
Wire a feedback bus early so every interaction can buzz and chirp.

**Spend delight at the edges.** Empty states, first-run, success moments, the
"nothing here yet" screens — these are where a playful product wins, because
they're where tools are most boring. A delightful empty state is worth ten
polished data tables.

**Never trade away contrast.** Playful ≠ low-contrast. A committed pastel/jelly
palette tempts you into faint text on faint fills — body copy, captions and
comments then wash out and the whole thing reads amateur, not warm. Keep real
text contrast (aim WCAG AA: ~4.5:1 body, ~3:1 large) even in the sunniest world:
near-black ink on paper, or committed light on a committed dark. Delight lives in
the motion and the accents, never at readability's expense. (This is the single
most common way a playful build goes wrong — watch for it.)

## The delight dial (choosing tone)

"Playful" is not one look — it's a **dial**, and the first design decision is
*where to set it*. The same foundations and patterns produce wildly different
products depending on how much delight you spend and *where* it lives. Pick the
tone from the product's job before anything else:

- **Toy / maximal** — delight in *everything*: saturated color, gradients, blobs,
  big rounded type, jelly springs, confetti, idle motion, sound+haptic on every
  touch. For consumer/social/kids/creative/celebratory products and **games/
  virtual pets**, where character *is* the point. (e.g. a Tamagotchi, a reactions-
  heavy chat.)
- **Playful-minimal** — minimal in *form*, playful in *feel*: lots of calm
  whitespace, one friendly accent, clean shapes, restrained type. The delight
  lives almost entirely in **motion, micro-interactions, and a warm human voice**
  (copy) — not in visual density. Nothing moves until you act, apart from maybe
  one tiny breathing element. Reads warm but grown-up. For everyday tools that
  still want a soul.
- **Refined / editorial** — sophistication first: a disciplined ink/paper (or
  premium dark) palette with ONE accent, tighter radii, a real typographic
  hierarchy (often serif + sans), hairlines and whitespace, **precise springs with
  little or no overshoot**, quiet optional feedback, at most one understated
  signature. For premium, trust-led, content-/audio-curation products. Playfulness
  is a whisper, not a circus.

What you turn as you move toy → refined: palette (rainbow+gradients → one accent),
density (packed+decorated → airy), type (heavy-rounded-900 → sans/serif hierarchy),
motion (jelly+overshoot+confetti+idle → short, crisp, on-action-only), signature
detail (loud+everywhere → subtle+once), feedback (loud default → quiet opt-in).
The *restraint* guidance in "When this applies" is really just the refined end of
this same dial. State the chosen tone up front, then keep every decision on it —
mixing toy chrome into a refined layout (or vice-versa) is what reads unfinished.

## How to work

1. **Set the tone dial first** (toy / playful-minimal / refined) from the product's
   job, and say it out loud — every later choice hangs off this.
2. Establish or restyle the **foundations** (palette, radii, type, shadow, motion
   tokens) *at that tone* so the surface already reads right before any special
   interaction. Lock in readable contrast while you set the palette.
3. Identify the **2–3 moments** that deserve a signature interaction (often:
   first-run, the core action, and a celebration/empty state). Pick matching
   patterns from the reference.
4. Build a tiny **feedback bus** (haptics + optional sound) so patterns can tap
   into it uniformly.
5. Prototype the motion first and tune the spring until it feels *alive* — this is
   iterative and tactile; numbers in docs are starting points, your thumb is the
   judge.
6. Pull back anywhere it fights clarity or speed. Delight that gets in the way
   stops being delight.

## Retrofitting an existing UI

Most real work isn't greenfield — it's making a UI that already exists *feel*
alive. The same foundations and patterns apply, but the job is a **restyle in
place, not a rewrite**, and that changes how you move:

- **Re-tune tokens; don't redraw.** Swap the palette, radii, type, shadow and —
  above all — the motion curves (easing → springs) at the component/token level.
  Most of the lift comes from changing *values*, not markup. Resist the urge to
  rebuild the screen; the structure is usually fine.
- **Preserve what the thing IS.** Keep the information architecture, content, copy
  semantics, routes, and — critically — **every working behavior**. Restyling the
  DOM must not break the handlers, state, or data flow. A user who knew the old
  screen should recognize it instantly, just delighted.
- **Keep accessibility and contrast intact or better.** Don't trade legibility for
  a pastel mood (see core moves); preserve focus states, labels, roles, hit-areas.
- **Work *inside* the existing system.** On a real codebase you're within a
  component library / design tokens / CSS architecture. Retrofit by editing shared
  tokens and the handful of base components (button, card, input, list row) so the
  change propagates — not by forking one screen. Find the existing theme layer and
  bend it; add a feedback bus as a small shared util.
- **Inject patterns only at the moments that matter.** Pick 2–3 high-value beats
  (the core action's completion, first-run/empty state, a celebration) and add the
  matching interaction pattern there. Don't sprinkle delight on every element.
- **Migrate incrementally and verify.** Restyle foundations first (instant
  global warmth), then one component family at a time, checking function after
  each. On a large app, land it as reviewable slices, not one big-bang re-skin.

Reality check: a throwaway single-file prototype lets you rewrite freely; a
production codebase does not. The constraint there is *faithfulness* — the art is
maximum new life for minimum structural disturbance.

Read both reference files before proposing a concrete design — they carry the
specifics (exact token ranges, per-pattern anatomy, motion/feedback/failure
notes) that make the difference between "cartoonish" and "alive".
