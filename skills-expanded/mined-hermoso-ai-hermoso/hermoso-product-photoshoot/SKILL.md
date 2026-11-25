---
name: hermoso-product-photoshoot
description: >-
  Brand-quality product photography with Hermoso: drop a real product photo into studio, lifestyle, or hero-banner
  scenes via reference-image compositing, so the packaging/label stays accurate. Use when the user wants
  "product shots", "a photoshoot for my product", "lifestyle images of <product>", "hero banner", "a Pinterest
  pin", "a model wearing my product", "a levitating / splash product shot", "restyle this image", "Amazon listing
  images", or "a pack of ad images" from a real product image. NOT for: video (use hermoso-generate) or research (use hermoso-research).
argument-hint: "[product image + scene, e.g. './bag.png as a sunlit kitchen hero shot']"
allowed-tools: Bash
---

# Hermoso: product photoshoot

Use Hermoso's reference-image compositing so the real product (label, colours, shape) is preserved while the
scene around it is generated. Drive the **Hermoso CLI**.

## Setup (once)
- Install the CLI once: `npm install -g hermoso`, then run every command as `hermoso …`, as written below. If you cannot install packages, prefix the commands with `npx -y`, but know that npx asks the npm registry on every single call, so an agent making many calls can be rate-limited by npm (an HTTP 429 from npm, before Hermoso is ever reached). No MCP server is needed.
- Sign in once: `npx -y hermoso auth login` (opens a browser; nothing to paste). On a machine with no browser (a server, chatted over Telegram, Discord or WhatsApp): run `npx -y hermoso auth login --device --no-wait`, send the user the link and short code it prints, and once they approve run `npx -y hermoso auth login --device --resume`. No key needed. Only if nobody can open a link: `npx -y hermoso auth login --token <your key>`, using a key from app.hermoso.ai under **MCP & CLI**. No account at all? An agent can sign itself up on a paid plan with `POST /v1/signup` at app.hermoso.ai; see the Hermoso README.
- Run `hermoso capabilities` once to see image model ids and recipes. For anything these steps do not cover: `hermoso tools --search <what you want>` finds the tool, `hermoso tools <name>` prints its arguments, `hermoso call <name> --json '{...}'` runs it.

## Procedure
1. Get the **product image** path/URL from the user. This is the `--ref`, it forces product-accurate compositing. No photo? Ask for one first (it is much more faithful); only if there is none, ask for the product's category, packaging, colour and distinctive features and write them into the prompt.
2. **Ask at most four short questions, each with labelled options, never open-ended**, and skip any the brief, the photo or an earlier turn already answers:
   - "make me images of this": how many `[1 / 3 / 5]`, which style `[Clean studio / Lifestyle / Conceptual / With a model]`, where they will run `[Shop / Instagram / Pinterest / Paid ads / Website hero]`, brand colours to match.
   - a use case is named ("ads for my product", "a Pinterest pin"): the mode is obvious, so ask only how many, the offer or hook, and what to emphasise.
   - "redo this image / change the vibe": `restyle`, then which aesthetic and season, and what must stay.
   - a model wearing the product: which model archetype (suggest two or three for the audience), environment `[Studio / Outdoor / Street / Editorial / Home]`, framing `[Full body / Three-quarter / Waist up / Close on the product]`.
   - vague ("something cool for my brand"): which product, which goal `[Sell on a marketplace / Awareness / Paid ads / Website]`, then continue as above.
3. Pick **one mode by intent, not by keyword** (when two fit, the more specific wins):
   - `product_shot`: the product on a clean studio, neutral or catalog backdrop (white, seamless, shop listing). 1:1 or 4:5.
   - `lifestyle_scene`: the product in a real place in use (kitchen, desk, cafe, gym, outdoors), hands and atmosphere. 4:5.
   - `closeup_product_with_person`: a tight crop with hands or part of a face (applying, holding, demonstrating). 4:5.
   - `moodboard_pin`: a vertical Pinterest-native pin with a moodboard feel. 2:3 (3:4 if the model has no 2:3).
   - `hero_banner`: a wide website, email or campaign header with room for a headline. 16:9.
   - `social_carousel`: 3 to 10 connected slides of one product. 4:5 or 1:1.
   - `ad_creative_pack`: a coordinated set of static ad variants for paid social or search. Run each at the placement's ratio.
   - `virtual_model_tryout`: the product worn or used by a generated model (fashion, accessories, lookbook).
   - `conceptual_product`: surreal or CGI-style: levitating, floating, splash, frozen motion, sculptural.
   - `restyle`: change an EXISTING image's aesthetic, mood or season without changing its subject. Pass that image as the `--ref` and describe only what changes, never the whole picture again.
   Most modes are also a recipe for `plan_ad` (pass `recipe`, it brings the art direction and the canvas): `studio_product`, `lifestyle`, `hands_closeup`, `pinterest_pin` (2:3), `hero_banner` (16:9), `tryon_photo`, `levitating_product`, `restyle`. A recipe is a shortcut, never a limit: any scene the user describes can be written straight into the prompt.
   Tie-breakers: a Pinterest pin of the product on a counter is `moodboard_pin` (the platform wins); a hero banner showing it in use is `hero_banner` (the format wins); a carousel of different scenes is `social_carousel` (multi-slide wins); a close-up of someone applying a serum is `closeup_product_with_person` (the specific genre wins).
4. Render: `hermoso generate image --prompt "<scene + composition + any on-image text>" --ref <product image> [--model <id>] [--aspect <ratio from step 3>]`
   - Prefer the `★best` image model for hero work; a faster model is fine for bulk variations.
5. **Variants are distinct, never paraphrases.** Each variant is its own call and changes the setting, the lighting, the angle and the palette. For `social_carousel` and `ad_creative_pack`, lock ONE visual system across the set (palette, type, lighting family, product scale) and vary only the scene, angle and message, so the set reads as one campaign.
6. **A marketplace listing set** (Amazon-style) is its own job: a main image (the product alone on a pure white background, filling most of the frame, no props, text or badges, the marketplace's own main-image rule), then the secondary images: an infographic of benefit callouts, a multi-angle view, a detail or macro shot, a lifestyle shot and a "what's in the box" layout; and, when asked, A+ modules: a hero banner, pain points, features, ingredients or materials, results, how to use, and an endorsement. The main image renders FIRST and every other image is drawn from it (each waits for it, so the whole set shows the same product, scale and light); pass an approved main as `mainImage` to redo the rest from it. `aplus:true` adds Amazon's 7 A+ modules: a 21:9 brand hero and brand promise and 3:2 modules 2-6 (key benefits, how to use, materials and details, lifestyle, what you get), each also delivered at its Amazon module's exact pixels (Premium 1464x600 + mobile 600x450, or 800x600; the Basic size beside it), with its text fields suggested only from the product's own data (`copy` for the seller's words; `copyIn:"image"` paints them on). The set is ONE call: `hermoso call make_listing_set --json '{"image":"<product photo>","dryRun":true}'` returns the plan and its exact price (main, lifestyle, detail, scale, in use by default; `shots` takes multi_angle, whats_in_box, back_of_pack or the user's own words), then the same call with `plan` set to that plan renders it, one image job per shot.
7. Report each served image URL as a short labelled list (e.g. "lifestyle / kitchen counter"); never paste the prompt back. Offer to `hermoso fetch` them to disk or to tweak a scene.

## Notes
- Keep the product as the hero; never let generated text garble the real label, describe the product as "the exact product in the reference, label unchanged."
- `--ref` takes a local path (read + sent) or a URL.
