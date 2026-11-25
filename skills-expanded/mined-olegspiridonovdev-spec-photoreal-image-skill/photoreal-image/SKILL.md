---
name: photoreal-image
description: Use when the user asks to generate or create a photorealistic photo or a photorealistic image, or any image that must look like a real camera captured it. Triggers include "photorealistic photo", "photorealistic image", "photo-realistic", "realistic photo", "generate a photo of", "make a photo", "hyperrealistic", "lifelike", "true to life", "cinematic still", "movie-style frame", "documentary shot", "product photo", "make it look real", "not AI-looking", "shot on", "film still". For illustrations, logos, diagrams, charts, or social media graphics, use the image skill instead.
---

# Photoreal Image

## Overview

A short request ("AC repair scene, symmetrical, from inside the unit") produces a generic image. The same request expanded into the physical facts a camera would have recorded produces a photograph. Expanded into the *decisions a photographer would have made* — it produces a good one.

**Two axes, not one.**

- **Truth** — would a camera have recorded this? Served by blocks 3, 4, 7, 8.
- **Merit** — is this frame worth looking at? Served by blocks 2, 5, 9, 10.

A prompt that only serves truth produces a convincing stock photo: real, and boring. Realism comes from constraint, not adjectives — "photorealistic, 8k, ultra detailed" is noise, while a named lens, a named source, a named flaw and a named material are signal. But merit comes from **commitment**: one moment, one light idea, one detail that could not be anywhere else.

**Never ship a prompt without blocks 2 (Moment), 8 (Imperfections) and 9 (Punctum).** Imperfection is what stops it reading as CGI. Moment and punctum are what stop it reading as stock.

**Commit to one idea.** Dramatic *and* soft, wide *and* intimate, moody *and* bright — the model averages conflicting instructions into mush. Pick the idea, then make every block serve it.

## Workflow

1. **Infer, don't interrogate.** Fill every unstated detail with the most plausible concrete choice. Ask only if the *subject itself* is ambiguous (which product, whose brand). One clarifying question maximum.
2. **Choose a look** before writing prose — a preset or a reference from `references/looks.md`. It decides blocks 3, 4 and 10 in one move and keeps them consistent with each other.
3. **Write the prompt** to the contract below. Prose, not `key: value`. Save it to a file in the scratchpad — never inline a 400-word prompt into a shell argument. Target **250–400 words**; past ~400 the later blocks get diluted. Over budget? Cut the least load-bearing sentence — never blocks 2, 8 or 9.
4. **Draft two on the model you will finish with** — never on a cheaper one:
   ```bash
   ~/.agents/skills/photoreal-image/generate.sh \
     --prompt-file /path/to/prompt.txt --slug ac-repair-interior \
     --aspect 16:9 --n 2 --model pro --size 2K
   ```
   Realism is a property of the model, not just the prompt. A flash draft tells you about *composition* and nothing about *skin* — judge one and you will "fix" a prompt that was never the problem.
5. **Look at what came back.** Read each PNG and score it against `references/critique.md`. This step is not optional — a photographer shoots, then edits. Skipping it is why prompt-only workflows plateau.
6. **Make one targeted fix.** Change the single worst failure. Do not rewrite the prompt; a rewrite trades a known problem for three unknown ones.
7. **Final render** of the winner: `--model pro --size 2K --n 1`, or `--size 4K` if it will be printed or cropped into. Switch to `--model gpt` only if the frame carries legible text or the composition must follow the prompt literally.
8. **Report the saved path only**, plus one line of assumptions ("assumed late-summer morning, 35mm, unbranded uniform"). Do not paste the prompt into the reply — `generate.sh` writes it beside the image as `.prompt.txt`. If the script exits 3 (`NO_PROVIDER`), print the full prompt in a code block instead; that is the deliverable when no key is available.

## The Prompt Contract

One paragraph per block, in this order. All 10 are REQUIRED.

| # | Block | Must contain |
|---|-------|--------------|
| 1 | **Frame** | Medium + subject + action + where the camera is standing. Then one clause on what the eye does: where it enters the frame and what it lands on. |
| 2 | **Moment** | The *instant*, not the activity. Name what just happened and what is about to. Prefer the beat before or after peak action — that is where photographs live. "He has just stopped turning the wrench and tilted his head toward the compressor; his hand is still on the tool." |
| 3 | **Light** | Hour, season and weather as one physical fact. Then every source and its quality (key, fill, practicals, bounce), the **key-to-fill ratio in stops**, and the *light idea* in one clause — what light is doing in this frame. Mixed color temperatures read as real. |
| 4 | **Camera** | Height, distance, angle. Body class + focal length + aperture. **Rendering character** — diffusion, flare, bokeh shape, grain, vignetting. Exactly which plane is sharp and how fast it falls off. Shutter if anything moves. |
| 5 | **Composition** | Layering across foreground / midground / background. How the subject separates from the ground — by tone, by color, or by focus; name which. Subject scale ("the figure fills about a third of the frame height"), negative space, lookroom. **Edge discipline: nothing tangent to the frame edge or to a background line.** |
| 6 | **Environment** | Specific objects that belong in that real location, distributed across the three planes. Clutter and utility, never staging. Include at least one thing that does not serve the picture — real photographs contain irrelevant objects. |
| 7 | **Subject truth** | Exact garments, fit, condition, drape. Then the human physics: an asymmetrical micro-expression, where the gaze is aimed *and at what*, what the hands are doing, where the weight sits. If no person is in frame, replace with **Materials & surfaces** — substrate, finish, age, and how light behaves on each. |
| 8 | **Imperfections** | **5+ concrete flaws**, drawn from at least three of: skin, fabric, air, surfaces, optics, environment. Never skip this block. |
| 9 | **Punctum** | Exactly **one** small, specific, faintly irrational detail that makes this frame this frame and no other — a child's drawing taped inside the equipment door, one mismatched sock, a wedding ring over a work glove. Not a flaw; a fact with a story behind it. |
| 10 | **Palette, grade & reference** | A color *relationship* — complementary, analogous, near-monochrome with one saturated break, or split-tone — expressed in 4–6 real tones. A named film stock or grade. What tradition the frame belongs to. Then the negative list, last: no CGI look, no plastic or waxy skin, no beauty retouching, no over-sharpening, no HDR halos, no artificial symmetry beyond the intended composition, no malformed hands, no watermark or text unless requested. |

Vocabulary banks and a full worked example: `references/craft.md`.
Presets, photographer/DP references, film stocks, clichés to avoid: `references/looks.md`.
The scoring rubric for step 5: `references/critique.md`.

## Quick Reference

**Lens by intent**

| Shot | Lens | Look |
|---|---|---|
| Interior/POV, environment around subject | 24mm | Wide, immersive, mild edge stretch |
| Documentary / reportage | 35mm | Close to human vision |
| Standard portrait, natural | 50mm | No distortion |
| Flattering portrait, compressed | 85mm f/1.4 | Creamy falloff, isolated subject |
| Product / detail | 100mm macro | Flat field, texture detail |
| Distant subject, compressed layers | 200mm | Stacked planes, thin focus |

**Key-to-fill ratio** — the fastest way to set drama. `1:1` flat, overcast, honest · `2:1` gentle modeling, editorial · `4:1` dramatic, shadow side still reads · `8:1+` low-key, shadows fall to black.

**Depth of field:** `f/1.4` face isolated, background dissolved · `f/2.8` subject sharp, environment legible · `f/5.6` group in focus · `f/11` near-to-far sharp · macro `f/8` with a 2cm plane.

**Rendering character** — what makes digital look photographed: Black Pro-Mist ¼ (halation, lifted blacks) · anamorphic (oval bokeh, horizontal blue flare) · vintage uncoated glass (veiling flare, low contrast) · 7-blade aperture (heptagonal specular highlights, not perfect circles) · cat's-eye bokeh at the edges · 1/48s at 24fps for correct motion blur.

**Resolution:** `--size 1K|2K|4K`, default `2K`. Resolution *is* realism here — pore, weave and grain detail only exist if there are pixels to hold it. 1K is for layout tests. 4K for print or when you will crop in; it costs more and very small in-frame text degrades slightly versus 2K.

**Aspect ratio:** cinematic/landscape `16:9` (default) · social vertical `9:16` · print portrait `2:3` · square `1:1` · ultrawide `21:9`.

## Choosing the Model

`--model auto` (default) tries best-photoreal first and falls back only when a model errors. Override deliberately:

| Flag | Model | Use it when | ~Cost/image |
|---|---|---|---|
| `pro` | `gemini-3-pro-image` (Nano Banana Pro) | **Default for anything with skin, fabric or aged material.** Best pore-level texture, subsurface scattering and natural falloff of anything currently available on these keys. | $0.134 (2K) · $0.24 (4K) |
| `gpt` | `gpt-image-2` | The frame carries legible text, or the composition must follow the prompt literally. Denser environments, slightly smoother faces. | ~$0.19 (high) |
| `draft` | `gemini-3.1-flash-image` → `-lite` | Blocking out composition only. Visibly waxier skin and garbled small text — never judge realism from it. | $0.03–0.10 |
| `flux` | `flux-2-pro` (Black Forest Labs) | Optional. Independently rated a 2026 photorealism leader; needs `BFL_API_KEY`. **Untested here** — no key on this machine. | ~$0.03/MP |
| `legacy` | `gpt-image-1`, `dall-e-3` | Comparison only. Both render flat, waxy, illustration-like faces — this is what "cartoonish" output looks like. | — |

Verified on 2026-07-23 by rendering one identical 400-word prompt through all four available models; Nano Banana Pro at 2K won on skin, hands, mixed-temperature light and in-frame text. `imagen-*` models still answer on the API but Google has deprecated them (shutdown 2026-08-17) — do not use them.

Other flags: `--n 1-4` variations · `--quality low|medium|high` (OpenAI only, default high) · `--out-dir DIR` (default `~/Downloads`) · `--dry-run` to check availability without spending.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Aiming for *competent* | "Honest, not glamorous" is a real style, but it is a choice — not the default. Decide what this frame is *for*, then aim there deliberately. |
| Stacking quality adjectives ("8k, ultra HD, masterpiece") | Delete them. Spend the tokens on light, moment, and flaws. |
| Skipping block 8 | Guaranteed plastic, CGI-looking output. Always name 5+ imperfections. |
| Skipping blocks 2 and 9 | Technically perfect, completely forgettable. This is the stock-photo failure. |
| Describing an activity instead of an instant | "Repairing an AC unit" averages every moment into none. Name the half-second. |
| Listing colors instead of a relationship | Six unrelated tones average into mud. Name the relationship first, then the tones. |
| Inventorying light sources without a light idea | A list of lamps is not lighting. State what light *does* here. |
| Contradicting yourself | "Golden hour" + "overcast" + "harsh shadows" averages into mush. Keep the light physically consistent. |
| Vague camera position | "Nice angle" means nothing. State height, distance, and what the camera sees. |
| AI-beautiful clichés | Teal-and-orange grade, dual unmotivated rim lights, wet ground everywhere, dust motes in every beam, flare with no source in frame. See `references/looks.md`. |
| Naming real people or trademarked brands | Describe the type: "a service uniform with an unbranded logo patch". |
| Generating once and reporting | Draft 2 on the finishing model, look at them, fix one thing, then render the winner. |
| **Output looks cartoonish / illustrated** | Almost always the model, not the prompt. Check the `Model:` line the script prints. If it says `gemini-3.1-flash*`, `gpt-image-1` or `dall-e-3`, re-render with `--model pro`. Only then start editing blocks 8 and 3. |
| Drafting on `flash`, then judging skin from it | Flash renders waxy faces however good the prompt is. You will rewrite a prompt that was already fine. Draft on the model you will ship. |
| Rendering at 1K and wondering where the texture went | Pores and fabric weave need pixels. `--size 2K` minimum for anything with a face in it. |
| Passing the prompt as a shell argument | Quoting breaks on apostrophes and newlines. Always `--prompt-file`. |
| Asking the user for details it could infer | Choose plausibly, generate, note the assumptions in one line afterward. |
