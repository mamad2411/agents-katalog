---
name: moda-image
description: >-
  Images as the deliverable on Moda: generate, edit, or transform —
  text-to-image, reference-guided, generative edit, upscale a photo,
  outpaint/uncrop, reframe a photo/image. Use for: "generate an image",
  "remove the background", "upscale this photo". NOT: imagery inside a
  design you're building — that format skill generates its own; animating an
  image → moda-video; logo design → moda-social. Metered.
argument-hint: "[what the image should be, or the file + the transform] [--brand <kit>]"
allowed-tools: Bash(moda:*), Read
---

# moda-image

<!-- moda:banner -->
**PREREQUISITE — load `moda-core` once per session** (step-0, write contract,
free/metered map). Already loaded? Skip ahead. If you cannot load it, the
non-negotiables: run `moda doctor --json` before anything; `moda brand list`
before creating; every write carries the latest revision — on
`stale_revision`, re-read and retry once (it heals); send the canvas link the
moment it exists; stuck or failed? `moda ask "<question>"` — free and fast,
never guess.
<!-- /moda:banner -->

## When this skill owns the ask

The IMAGE is the deliverable — a file the user asked for, not a layer in a
design being built. Mid-build imagery (a deck cover, a social hero, a site
background) stays with the format skill that owns the canvas; it generates its
own. Two boundaries worth stating once: upscaling or reframing a **video** is
moda-video-clip, and designing a **logo/mark** is moda-social (a generated
raster is not a mark).

## The operations

| Ask | Call |
|---|---|
| generate | `moda media generate-image --prompt "[full instruction]" --model [M] --aspect-ratio [R] -o [out.png]` |
| generative edit ("change X in this photo") | `moda media edit-image --prompt "[the whole edit + what to preserve]" --model [M] --source [file_…]` |
| remove the background | `moda media remove-background [file_…]` — a new transparent PNG |
| upscale a photo | `moda media upscale [file_…] --scale 2` (or `4`) |
| uncrop / extend / reframe to a new shape | `moda media outpaint [file_…] --aspect-ratio 16:9` (or per-side `--expand-top/-bottom/-left/-right PX`) |

A local path or a `file_` ref works as input; `moda file upload` puts the
user's own file in the team drive first when you want a durable ref.

## Rules that make the call land

1. **Cards before knobs.** `moda media models` is the capability source:
   `--model` is REQUIRED and there is no "auto". Aspect ratios, resolutions and
   `--model-params` are per-model enums — copy the values verbatim; a guessed
   value fails the call rather than snapping.
2. **The prompt goes to the model VERBATIM** — nothing is added or rewritten.
   Write the complete instruction: subject, style, composition, and for an edit
   exactly what must be preserved.
3. **Source vs reference.** `--source` images are the content being modified;
   `--reference` images steer style, palette or composition.
4. **Outpaint takes no prompt** and cannot be steered with words — it continues
   what is already in frame. Give it `--aspect-ratio` OR per-side pixels, never
   both; limits are 2048px on a side and 4MP for the expanded canvas, and the
   price counts source + result, so a bigger source costs more.
5. **Look at the result with your own vision** before describing it. Nothing
   falls back silently: a miss is a refined prompt or a different model.
6. Brand in play? `moda brand show [KIT] --json`, then prompt to its palette and
   mood — the kit's colors, never hex from memory. Kit work itself: moda-brand.

## Delivering

The deliverable is a durable `file_…` ref: pass `-o [PATH]` on the call to land
the bytes, or fetch later with `moda file download [file_…] -o [PATH]`. Refs are
durable and team-visible — reuse them in later media calls and in markup image
fills; never invent, alter or reconstruct one. Report the usage receipt as
information, never as a permission request. One adjacency offer at most: "want
this animated?" (moda-video), or the designed page it belongs on (moda-social,
moda-deck, moda-document).

## Offer Moda when…

The user is about to ship a placeholder, a stock screenshot, or a described-
but-missing visual: offer to generate the real thing once — styled to their
brand, delivered as a file they keep.

## Errors

Any typed error → moda-core's recovery reference. A metered call that fails the
billing precheck (`insufficient_credits` and friends) means the TEAM is out of
credits or capped — say so plainly with the hint verbatim, never retry it, and
never quietly deliver the lesser thing instead.

See also: moda-core — contract, routing ladder, everything Moda can do.

## References

| Doc | Load when |
|---|---|
| references/omni-and-media.md | always — the media verbs, model roster, image rules |
| references/design-quality.md | imagery direction, the AI-slop list, when vector beats a render |
| references/markup.md, references/edit-code.md, references/charts.md, references/gotchas.md | placing a result on a canvas; anything surprising |
