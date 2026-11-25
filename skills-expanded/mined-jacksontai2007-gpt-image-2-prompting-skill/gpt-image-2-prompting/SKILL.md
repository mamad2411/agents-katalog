---
name: gpt-image-2-prompting
version: 0.1.0
description: >-
  Write, refine, and debug production-grade prompts for GPT Image 2 (OpenAI's
  text-to-image / image-to-image model; also covers gpt-image-1, ChatGPT image
  generation, and DALL·E-style prompting). Use WHENEVER the user wants to create
  or improve an AI image prompt — posters, UI/app mockups & screenshots,
  infographics, product/e-commerce shots, logos, character/concept sheets,
  photoreal portraits, game screenshots, illustration, or any image that must
  contain readable text or keep a consistent character. Trigger even when "GPT
  Image 2" isn't said but the user asks to "make a prompt for an image", "design
  a poster/app screen with AI", "fix the text in my AI image", "keep the same
  face across images", "generate a whole set/series of images", or "turn this
  idea into an image prompt". Also use to structure a vague idea, build a
  reusable template, edit an image with a reference (image-to-image), or diagnose
  a bad generation (gibberish text, messy layout, plastic-looking people, wrong
  style, identity drift).
---

# GPT Image 2 Prompting

Distilled best practices for getting reliable, professional output from GPT Image 2. The core shift this model rewards: **stop writing prose wishes, start writing structured specifications.** GPT Image 2 follows long, layered instructions, so the bottleneck is no longer "can it make an image" but "can you specify the image precisely enough to be reproducible."

## What this model is unusually good at (the leverage points)

Aim prompts at these strengths — they are where specificity pays off most:

1. **Typography / text-in-image** — renders exact text, including Latin, Cyrillic, and CJK scripts, with high accuracy. → *Hardcode the literal strings you want.*
2. **Identity retention** — keeps the same character, product, or IP consistent across panels, angles, and scenes. → *State the consistency contract up front; use grids or a reference image for series.*
3. **Structured design** — infographics, exploded/cutaway diagrams, multi-panel and grid layouts. → *Specify exact module/panel counts and the layout skeleton.*
4. **Style induction** — captures the "soul" of an art movement or aesthetic, not just surface colors. → *Name the style precisely, or describe its signature mechanics.*
5. **World knowledge** — accurate real places, named games, apps, brands, and scenes. → *Reference real-world context by name to replicate a look (e.g. "GTA 6 in-game footage", "TikTok live UI").*
6. **Prompt adherence** — honors long, constraint-heavy instructions; it handles detailed prompts *better* than short ones. → *Be detailed and demanding; layer the specifics.*
7. **Photorealism** — output can be indistinguishable from a photo or screenshot. → *Use camera/film vocabulary and add imperfections.*

## The 6-block prompt protocol

Every strong prompt — prose or JSON — is built from these atomic blocks. Compose only the blocks the task needs, but always order them intent → structure → style → constraints. Filling blocks 1, 3, 4, 6 is what separates a reproducible spec from a lucky roll.

1. **Intent** — what artifact this is and what it's for ("an iOS app screen for a fitness feed", "a museum-grade event poster"). State this *first* so the model builds the right global context before any detail.
2. **Subject** — the hero element, *decomposed into concrete attributes* (not "a beautiful woman" but "almond eyes, high nose bridge, natural full brows; silk blouse"). Vague adjectives are where quality leaks out. For people, appearance is an explicit variable — see *Depicting people* below.
3. **Composition** — aspect ratio, layout pattern, module/panel count, camera angle + lens, perspective, and the focal hierarchy (what dominates, what supports).
4. **Text** — the *exact* strings, each with a role (headline / subhead / label / body), plus a readability + spelling + language lock. The model invents nonsense copy if you leave this open.
5. **Style** — art style or medium, brushstroke/render technique, materials and textures, color system, and lighting. The "soul" layer — worthless without blocks 3 and 4 holding the structure.
6. **Constraints** — explicit negatives and forbidden elements ("no gibberish text", "no modern objects", "no cluttered collage", "single poster only — no moodboard", "no plastic skin, no watermark"). Negatives prevent the model's most common failure modes and matter as much as the positives.

## Authoring workflow

When a user gives you an image idea, don't just polish their words — run it through the protocol:

1. **Classify the task** → use `references/categories.md` to route the request to its artifact archetype, then pull the matching template from `references/templates.md` (13 categories) and/or a specific recipe from `references/scene-cookbook.md`.
2. **Lock structure before style.** Pin aspect ratio, layout/grid, module count, and camera *before* reaching for adjectives. Structure-first is the single biggest defense against "messy AI collage."
3. **Hardcode every piece of text** that must appear, verbatim, with its role and a readability demand.
4. **Layer style and material** — pull concrete components from `references/style-library.md` (lighting, lens, film stocks, materials, palettes, named styles) rather than generic words like "high quality."
5. **Add the negative constraints** for that artifact type (each template/recipe lists its top traps).
6. **Pick the form & mode**: prose vs JSON (see below); text-to-image vs image-to-image (see below).
7. For open-ended briefs, **offer a primary plus one alternate**; for a *set/series*, deliver one batch-orchestrated prompt (see *Consistency & series*).

## Universal principles (distilled from hundreds of reverse-engineered prompts)

These hold across every category — the difference between hobby rolls and production assets:

- **Declare intent + use-case first.** Global context up front makes every later instruction land better.
- **Hardcode exact text; never let the model write copy.** Specify the literal headline/subhead and demand "spelled exactly, clearly readable." Open-ended text → gibberish.
- **Structure before style.** Aspect ratio, layout pattern, and module/panel count first. A precise skeleton beats a pile of style words.
- **Decompose the subject.** Replace every vague adjective with concrete, observable features. The model can't read your taste; it can read "freckles, wind-swept hair, weathered denim."
- **Layer detail — longer is better here.** Unlike older models, GPT Image 2 rewards dense, specific prompts. Don't strip detail to "keep it clean"; add the right specifics.
- **Materials + lighting are the soul of realism.** Stack material keywords (matte, brushed metal, woven) and a named lighting setup (softbox, rim light, golden hour). Cool-exterior / warm-interior contrast instantly reads "high-end."
- **Speak in camera/optics for photoreal work.** `f/1.4` beats "shallow depth of field"; `50mm` beats "half-body"; name a film stock or camera type (35mm, CCD, "RAW iPhone") for color and texture. Then *add imperfections* — pores, film grain, slight asymmetry, motion blur — to kill the plastic "AI mannequin" look.
- **Reference real-world context to replicate a look.** Naming a specific game, app, brand, or place ("Black Myth: Wukong scene", "Spotify-style player", "Apple Park") activates the model's world knowledge far better than describing the look generically.
- **Ration information density.** Short phrases, capped module counts. Don't pour body text into an image. For long copy use "simulated text blocks" and hardcode only the headlines.
- **Always write the negatives.** Forbid the specific failure for that artifact ("no modern elements", "no extra text", "single poster only", "no plastic skin/watermark/text"). Load-bearing, not polish.
- **Extract a master's mechanics, not their name.** "Van Gogh's swirling impasto starscape" induces the technique; "by Van Gogh" tends to clone one famous canvas.
- **Make elements interact, not decorate.** Text should overlap, frame, or emerge from the subject; props should be compositional anchors with a specified angle and scale — not background clutter.
- **For series/consistency, state the contract before the sequence** — and prefer a reference image for a strict identity lock (see below).
- **Don't silently choose who appears.** When people are depicted and appearance is unspecified, treat it as an explicit, swappable variable — see *Depicting people*.

## Depicting people (internationalization)

This skill is meant to be culture-neutral and reusable worldwide, so **never hard-code a single demographic default.** When a prompt involves people and the user hasn't specified appearance:

- **Let scene context win first.** If the request itself implies a culture or place ("Hanfu garden portrait", "Parisian café", "Lagos street style", "Diwali family photo"), depict people consistent with that context.
- **Otherwise, match the user's language/locale as a sensible default.** A request written in Japanese implies Japanese subjects; Hindi → South Asian; Arabic → Middle Eastern; Korean → Korean; and so on. This respects the user's likely context without you imposing one.
- **Always expose appearance as a variable.** Put ethnicity/age/features in a clearly editable slot (e.g. `subject.ethnicity_age`) so the user can override in one edit, and mention it's adjustable.
- **When it's genuinely ambiguous** (neutral English, no cultural cue), either ask, or vary it / state the assumption you made so the user can change it — don't default unawarely to one group.

The goal: the depicted person should plausibly fit the user's context, and the user should always be able to change it trivially.

## Text rendering — the #1 differentiator, so get it right

Because text is this model's signature strength and most common failure point:

- Put the exact copy in quotes and label its role: `headline: "BEYOND STARS"`, `subhead: "A New Era Begins"`.
- Add an explicit lock: *"Render this text exactly as written, correctly spelled, fully legible. Do not translate, shorten, paraphrase, or add other large text."*
- Keep on-image text short. Long paragraphs degrade; if body copy is unavoidable, request "simulated text blocks" and only hardcode the few strings that must be correct.
- Name the script/language when it isn't English (e.g. "Simplified Chinese, correct characters").
- For typography-led posters, declare that the title *is* the primary visual structure (huge, exact) and that no other large readable text competes with it.

## Consistency & series

- **One character across scenes:** lock identity attributes (face shape, hair, build, signature clothing/colors) and repeat them verbatim each time; add "maintain the same character identity, do not change face or outfit."
- **Strict identity lock → use a reference image (image-to-image).** Text alone yields *similar*, not *identical*, faces across separate generations. For a true lock, generate or pick one hero image, then feed it back as a reference: "using this exact face/person, generate [new scene]." This is the ceiling for consistency.
- **A whole set in one go:** the model makes one image per generation, but in a chat app you can issue **one message that orchestrates N sequential generations.** Open with an explicit instruction — "Generate these as N SEPARATE standalone images, one per scene, one after another in this response; do NOT merge into a grid/collage" — then a shared base block + a list of per-scene deltas. Warn the user a single turn may cap the count (continue with "next scenes, same spec") and that consistency will be close but not identical without a reference image.
- **Multi-panel sheets** (turnarounds, expression grids, card sets): specify an N×M grid, equal-size panels, per-panel numbering, and a per-panel structure (title / figure / caption), with the consistency contract written *above* the panel list.
- **Exploded / cutaway / technical diagrams:** state the number of numbered callouts and that labels must be short and readable.

## Image-to-image / editing mode

GPT Image 2 is strong at transforming or extending an existing image, not just generating from scratch. Reach for this mode when the user uploads an image or wants consistency with one:

- **Style transfer:** "Turn this photo into a watercolor / anime snapshot / 3D render," keeping composition. Name the target style precisely.
- **Reference-locked generation:** "Using this exact character/face/product, create [new pose/scene]." The single best consistency technique.
- **Character reference sheets from one drawing:** "Based on this character, produce a three-view + expression variations + equipment breakdown + color palette + worldview note, official-concept-art layout."
- **Inpainting / local edits:** change one region (the API `images.edit` endpoint takes the image + a mask). Describe only what changes; state that everything else stays identical.
- **Restyle + translate:** "Colorize this comic page and translate the speech bubbles to English, keeping bubble positions and composition."

In every case: tell the model explicitly what to keep vs change, or it may redraw the whole frame.

## Prose vs JSON form

Same *content* either way — both obey the 6-block protocol; JSON just makes the blocks explicit keys.

- **Prose** — best for one-off, human-driven generation in a chat UI. Natural, readable, easy to hand-tweak.
- **JSON** — best for automation, batch jobs, Agent/tool pipelines, and template systems. The atomic schema (type, subject, layout, style, content, constraints) is machine-fillable and diff-able. Use `{placeholder}` variables for anything swappable across runs. `references/templates.md` gives a JSON form for every category.
- **Note:** JSON doesn't make output "better" per se — a fully-specified prose prompt and a fully-specified JSON prompt converge. JSON's wins are completeness (no forgotten block), reuse, and batching. One caveat unique to this model: because it renders text so eagerly, it occasionally paints JSON key names into the image — always keep a `no text/watermark/labels` constraint, and if you see stray keys rendered, switch that one to prose.

## Runtime knobs (when generating via API/app)

- **Aspect ratio / size:** state it in the prompt ("aspect ratio 3:4", "9:16", or `--ar 9:16`). API `size` accepts `1024x1024`, `1536x1024`, `1024x1536`, or `auto`.
- **Quality:** API `quality` is `standard` or `high`.
- **Count:** `n` returns variations of *one* prompt — not different scenes. For different scenes, issue separate generations (or orchestrate them in one chat message; see *Consistency & series*).
- **Editing:** image-to-image uses the `images.edit` endpoint (image + optional mask) instead of `images.generate`.

## Generating the image (only if the host can)

Your job is to produce the *prompt*. Only offer to generate the image itself when the runtime actually exposes an image tool (e.g. an `image_generate` / images API tool in this session):

- **Check first, never assume.** If no image-generation tool is available, hand over the finished prompt and tell the user where to paste it (ChatGPT, the OpenAI API, etc.). Do **not** pretend you rendered anything.
- **Offer, don't auto-fire.** When a tool *is* available, deliver the prompt first, then ask if they want you to run it — generating can cost money and they may want to tweak the prompt first.
- **One prompt → one image.** For a set, generate separate calls (see *Consistency & series*), never a merged grid.

## Reference files

Load these as needed; don't dump them into context preemptively.

- **`references/categories.md`** — A router: maps each request to its artifact archetype, the matching template, and the recipe(s) that apply. Read this *first* to classify a request before drafting.
- **`references/templates.md`** — Copy-paste prose **and** JSON templates for all 13 artifact categories (UI, infographic, poster, e-commerce, brand, architecture, photography, illustration, character, narrative, historical, document, general), each with its pitfall guide. Read this when the task maps to a broad artifact type.
- **`references/scene-cookbook.md`** — 29 optimized, ready-to-run recipes for specific high-value scenes (film-stock portrait, authentic amateur snapshot, consistency grid, city-silhouette poster, surface-integrated typography, named-game screenshot, full app screenshot, live-stream UI, social-feed mockup, character reference sheet, expression grid, museum-catalog infographic, exploded breakdown, process journey, text-hierarchy product poster, brand-mascot collab, ancient scroll, hand-drawn map, labeled grid, and more). Each entry names *the one trick* that makes it work. Read this when the user's request matches a specific scene rather than a generic category.
- **`references/style-library.md`** — Composable component menus: aspect ratios, camera & lens, film stocks & camera types, lighting setups, color systems, materials & textures, art/illustration styles, composition patterns, realism boosters, render-quality tags, and reusable text directives. Read this when layering blocks 3 and 5, or offering look/feel options.
- **`references/troubleshooting.md`** — Symptom → cause → fix table for failed generations (gibberish text, messy layout, plastic faces, wrong era, ignored text, washed-out product, identity drift, screenshot looking like concept art, rendered key names). Read this when a generation came out wrong and the prompt needs a fix.
