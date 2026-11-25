---
name: higgsfield-studio-product-photoshoot
description: "Make brand-quality product photos with Higgsfield: studio, lifestyle, Pinterest pins, hero banners, carousels, ad packs and try-ons. Triggers: 'product photo', 'studio shot of my product', 'lifestyle image of this bottle', 'make a Pinterest pin', 'hero banner for my site', 'ad creative pack', 'model wearing my product', 'restyle this photo for Christmas'. Part of Higgsfield Studio: each shoot is planned and priced for free before any image is made, never paid for twice, and written to a ledger. Needs Node 18+ and the higgsfield command line tool."
license: MIT
compatibility: "Requires Node 18 or newer and the Higgsfield command line tool, through the higgsfield-studio skill in the same plugin. Needs network access and a Higgsfield account. Generating spends its credits."
metadata:
  author: itqanlab
  version: 1.1.0
  category: media
  display: "Higgsfield Product Photoshoot"
  short: "Product photos priced before they are made"
  starter: "make three lifestyle shots of this bottle for Instagram"
---

# Higgsfield Product Photoshoot

Higgsfield writes the final image prompt from a mode and a short intent, then renders each image. The guard plans the shoot first with Higgsfield's free `--enhance-only` step and prices every planned image, so the user sees the full price before anything is made.

## What it costs

Each image is a `gpt_image_2` render at 2k, quoted at 6.5 credits on 2026-10-12. A `--count 2` shoot was quoted at 13. `--count 5` is about 33 credits. Start with `--count 1`, show it, then make more.

```
node ../higgsfield-studio/scripts/hf.mjs photoshoot --mode lifestyle_scene --prompt "cold-brew bottle on a sunlit kitchen counter" --image bottle.jpg --count 1 --dry
node ../higgsfield-studio/scripts/hf.mjs photoshoot --mode lifestyle_scene --prompt "cold-brew bottle on a sunlit kitchen counter" --image bottle.jpg --count 1 --max 8 --out shoot/ --tag launch --why "first lifestyle shot"
```

## Before anything else

```
sh ../higgsfield-studio/scripts/setup-deps.sh --check
node ../higgsfield-studio/scripts/hf.mjs check
```

The first checks Node and the `higgsfield` tool, and `sh ../higgsfield-studio/scripts/setup-deps.sh` installs what is missing after asking. The second checks the sign-in. If Higgsfield is not signed in, the user signs in once with `higgsfield auth login`, which opens the browser. Never print the sign-in token or open the CLI's credential file.

## Spending credits

This skill is part of the Higgsfield Studio plugin. Every paid command runs through the main skill's guard, `node ../higgsfield-studio/scripts/hf.mjs`. It asks Higgsfield for the price before running, refuses above `--max` or below the reserve, never pays twice for the same request, and writes what each job really cost to `.higgsfield/ledger.jsonl` in the project. The full rules are in `../higgsfield-studio/SKILL.md`. The short form:

- Price first with `--dry`, using every parameter the real job will use. Tell the user the total for anything over about 5 credits.
- Put `--max N` (a little above the price), `--tag` and `--why "..."` on every paid job.
- Ask before spending more than about 10 credits, or 10% of what is left. `node ../higgsfield-studio/scripts/hf.mjs account` shows the balance.
- Anything outward or not undoable goes through `act` and needs `--yes`. Say what will happen and wait for the user's yes before adding it.
- Report in plain words, in the user's language: where the file is, what it cost, what is left. No JSON or job ids unless asked.

Free commands, such as lists, `model get`, presets and uploads, can run as `node ../higgsfield-studio/scripts/hf.mjs run <command>` or as `higgsfield <command>` directly.

## Updates

This skill is versioned with its plugin. Its version is `metadata.version` in the header of this file. The plugin's history, for every skill in it, is in `../higgsfield-studio/CHANGELOG.md`. To check for a newer version, open the address on its `Latest:` line and compare the top version with this one. Read every entry in between and tell the user what changed before anything is updated.

## Higgsfield's guide

Everything below is Higgsfield's official guide for this task, with its paid and outward commands already pointed at `node ../higgsfield-studio/scripts/hf.mjs`. The rules above win where the two differ.

# Product Photoshoot

Brand-image generation via the `node ../higgsfield-studio/scripts/hf.mjs photoshoot` command. The CLI calls a backend prompt enhancer that holds mode-specific photography vocabulary and structural templates, then submits to `gpt_image_2` and returns image URLs.

## Step 0 — Bootstrap

Before any other command:

1. If `higgsfield` is not on `$PATH`, install it:
   ```bash
   sh ../higgsfield-studio/scripts/setup-deps.sh
   ```
2. If `higgsfield account status` fails with `Session expired` / `Not authenticated`, ask the user to run `higgsfield auth login` (interactive) and wait for confirmation.

## UX Rules

1. Be concise. Print only image URLs in the final reply.
2. Detect language, respond in it. Mode names and CLI flags stay English.
3. Ask at most 4 short questions before submitting. Use labeled options, never open-ended.
4. Skip questions whose answer is obvious from context (uploaded image, prior turn, brand memory).
5. Never write the gpt_image_2 prompt yourself — backend assembles it.
6. Polling is silent. Wait until URLs are ready, then deliver.

## Modes

| Mode | When user wants… |
|---|---|
| `product_shot` | Product on neutral / studio / catalog background |
| `lifestyle_scene` | Product in real-world environment, hands, action, atmosphere |
| `closeup_product_with_person` | Tight crop with hands / partial face — beauty application, holding, demonstrating |
| `moodboard_pin` | Vertical 2:3 Pinterest-native aesthetic, moodboard feel |
| `hero_banner` | Wide-format website / email / campaign header |
| `social_carousel` | 3–10 connected slides for IG / LinkedIn / Facebook |
| `ad_creative_pack` | Coordinated pack of static ad variants for Meta / TikTok / Pinterest / Google Ads |
| `virtual_model_tryout` | Product worn or used by an AI-rendered model |
| `conceptual_product` | Surreal / CGI-style / levitating / splash / sculptural product |
| `restyle` | Transform an existing image's aesthetic, mood, or seasonal context |

## Mode selection

Pick by intent, not surface keyword. When two modes could apply, prefer the more specific one.

- product + neutral / clean / white / studio / catalog / Shopify → `product_shot`
- product + scene / in use / kitchen / outdoor / cafe / gym → `lifestyle_scene`
- hands holding / face with product / beauty application / demonstrating → `closeup_product_with_person`
- Pinterest, pin, vertical pin → `moodboard_pin`
- hero, banner, website header, landing page, email header, wide format → `hero_banner`
- carousel, slide post, multi-slide, swipeable → `social_carousel`
- ads, ad pack, paid social, Meta / TikTok / Pinterest ads → `ad_creative_pack`
- model wearing, virtual try-on, on body, fashion shoot, lookbook → `virtual_model_tryout`
- levitating, floating, splash, frozen motion, surreal, CGI, sculptural → `conceptual_product`
- modify EXISTING image's aesthetic, mood, season — without changing subject → `restyle`

Tie-breakers:
- "Pinterest pin of my product on a kitchen counter" → `moodboard_pin` (Pinterest is the platform)
- "Hero banner showing my product in use" → `hero_banner` (banner format wins)
- "Carousel of my product in different scenes" → `social_carousel` (multi-slide wins)
- "Closeup of person applying my serum" → `closeup_product_with_person` (specific genre wins)

## Pre-generation interview

Ask 3–4 short questions before submitting. Always labeled options, never open-ended. Skip a question whose answer is obvious from context.

### Type A — uploaded a product photo, "make me images / photoshoots"

1. How many? `[1 / 3 / 5]`
2. What style/mood? `[Clean studio / Lifestyle / Conceptual / With a model / Other]`
3. Where will you use them? `[Shopify / Instagram / Pinterest / Paid ads / Website hero]`
4. Brand colors to match? (skip if obvious)

### Type B — uploaded a product photo, named a use case

E.g. "make ads for my product", "make a Pinterest pin", "make a hero banner". Mode is obvious. Ask only the gaps:

1. How many? (if multi-output mode)
2. What's the offer / mood / hook?
3. Anything in particular to emphasize?

### Type C — text only, no product photo

1. Can you upload a product photo? (preferred — much higher fidelity)
2. If not, describe the product — category, packaging, color, distinctive features.
3. What style? (same options as Type A)
4. Where will you use it?

### Type D — uploaded existing image, "redo / change vibe / different version"

→ `restyle`

1. What aesthetic? `[Clean girl / Cottagecore / Quiet luxury / Dark academia / Y2K / Other]`
2. Seasonal context? `[Christmas / Valentine's / Halloween / Black Friday / None]`
3. What to preserve, what to change? (only if ambiguous)

### Type E — model wearing a product (fashion, accessories)

→ `virtual_model_tryout`

1. Model archetype? (suggest 2–3 based on brand audience)
2. Environment? `[Studio clean / Outdoor natural / Street style / Editorial / Home cozy]`
3. Framing? `[Full body / Three-quarter / Waist up / Closeup on product area]`

### Type F — vague request, unclear subject

E.g. "make me something cool for my brand".

1. What product or topic?
2. Goal? `[Sell on a marketplace / Build awareness / Run paid ads / Update website]`
3. Upload a reference image?

After answers → return to the relevant Type A–E.

## Generation

Single command. Backend assembles the final prompt and submits to `gpt_image_2`. URLs print on stdout.

```bash
node ../higgsfield-studio/scripts/hf.mjs photoshoot \
  --mode <mode> \
  --prompt "<short user-intent description from interview answers>" \
  [--image <path-or-upload-id>]... \
  [--count <1-10>] \
  [--aspect_ratio <override>]
```

Examples:

```bash
node ../higgsfield-studio/scripts/hf.mjs photoshoot \
  --mode lifestyle_scene \
  --prompt "bottle of cold-brew on a sunlit kitchen counter, IG feed" \
  --image bottle.jpg \
  --count 3
```

```bash
node ../higgsfield-studio/scripts/hf.mjs photoshoot \
  --mode moodboard_pin \
  --prompt "vertical pin for my candle brand, cottagecore mood" \
  --image candle.jpg
```

```bash
node ../higgsfield-studio/scripts/hf.mjs photoshoot \
  --mode restyle \
  --prompt "Christmas version, quiet-luxury aesthetic" \
  --image existing-shot.jpg
```

## Image inputs

`--image` accepts a local file path (auto-uploaded) OR an existing upload UUID. Repeat the flag for multiple references.

## Multi-variant

`--count 3` returns 3 distinct image URLs. Backend asks the enhancer to vary preset, lighting, angle, and palette across variants — they will not be paraphrased copies of one another.

For `social_carousel` and `ad_creative_pack`, count = number of slides / variants in the pack. Backend locks the visual system across all slides automatically.

## Aspect ratio

Backend picks a sensible default per mode. Override with `--aspect_ratio` only if the user explicitly asks for a different one. Allowed values: `1:1`, `4:5`, `5:4`, `3:4`, `4:3`, `2:3`, `3:2`, `9:16`, `16:9`.

## Resolution

Use `2k` for every product-photoshoot job.

## Delivering results

Print the image URLs as a short bulleted list. No JSON, no IDs, no internal model names, no enhanced prompt text. If a job failed, mention it briefly with the failure status.

```
3 lifestyle shots ready:
- https://cdn.higgsfield.ai/.../job_abc.jpg
- https://cdn.higgsfield.ai/.../job_def.jpg
- https://cdn.higgsfield.ai/.../job_ghi.jpg
```

## What this skill does NOT do

- Does not write gpt_image_2 prompts directly. Backend owns prompt assembly.
- Does not auto-pick a different image-gen model. Always `gpt_image_2`.
- Does not replace `higgsfield-generate` Marketing Studio for branded video / avatar workflows.
- Does not replace `higgsfield-generate` for raw text-to-image without a product or brand context.

## Common mistakes to avoid

- Asking more than 4 interview questions in a single message.
- Picking the wrong mode (e.g. `product_shot` when the user wants a Pinterest pin).
- Calling `node ../higgsfield-studio/scripts/hf.mjs create gpt_image_2 --prompt ...` directly instead of `node ../higgsfield-studio/scripts/hf.mjs photoshoot` — bypasses the prompt enhancer and produces noticeably worse output.
- Pasting the assembled prompt back to the user — they want the URLs.
- Using a `--mode` value not in the table above.
