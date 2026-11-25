---
name: ultrareal-prompt-architect
description: Transforms simple image ideas into production-ready photorealistic image-generation prompts written as photography briefs, not keyword dumps. Use when the user wants a realistic, cinematic, DSLR, documentary, product, food, portrait, landscape, architecture, fashion, or street-photography prompt; when they mention Midjourney, Flux, Stable Diffusion, SDXL, GPT Image, DALL-E, Gemini, Nano Banana, Ideogram, or Imagen; or when they ask to make an image less AI-looking, more realistic, more cinematic, more documentary, video-ready, or to refine lighting, camera, skin, or aspect ratio.
license: MIT
metadata:
  author: UltraReal
  version: "1.0.0"
  skill: UltraReal Prompt Architect
---

# UltraReal Prompt Architect

Turn a short image idea into a physically believable photograph brief.

**Core principle:** Do not describe "AI realism." Describe reality.

Wrong: `ultra realistic skin, cinematic lighting, highly detailed, 8K, masterpiece`

Right: `soft late-afternoon sun from camera left, warm highlights on the near cheek, cooler ambient shade behind, visible pores and faint stubble, cotton shirt creased at the elbow`

## When this skill is active

- User wants an image prompt, photo prompt, or generation brief
- User wants photorealism, cinematic realism, documentary, product, food, fashion, architecture, wildlife, travel, or religious/devotional photography
- User names an image model and wants the prompt adapted
- User refines an existing prompt (`more realistic`, `make it night`, `9:16`, `less AI`, `video-ready`)

Do **not** generate the image unless the user also asked you to. This skill writes prompts.

Do **not** interrogate short requests. Infer sensible photographic details. Never overwrite identity, clothing, location, action, mood, culture, or objects the user already specified.

## Workflow

Follow this sequence internally. Do not dump the checklist into the user-facing prompt.

1. **Lock the brief**
   - Preserve: subject, clothing, location, action, mood, culture, named objects
   - Infer only supporting photographic facts (time of day, weather, lens, light direction, surface wear)
   - If the user named a style (`documentary + cinematic`, `luxury fashion`), honour the combination
   - If no style is given, default to **professional observed photography** — believable, not movie-poster, not beauty-filtered

2. **Classify the shot**
   - Genre: portrait / environmental portrait / street / travel / landscape / architecture / product / food / vehicle / wildlife / action / interior / still life / religious-devotional / historical / editorial / fashion
   - Human present? product-critical materials? motion? text-in-image?
   - Target model, if any
   - Delivery: still / later video / vertical social / print / e-commerce

3. **Load only the references you need**
   - Humans → [references/human-realism.md](references/human-realism.md)
   - Camera/lens choice → [references/cameras-lenses.md](references/cameras-lenses.md)
   - Lighting design → [references/lighting.md](references/lighting.md)
   - Framing → [references/composition.md](references/composition.md)
   - Surfaces, fabrics, metal, food, weather → [references/materials.md](references/materials.md)
   - Genre recipes → [references/subject-playbooks.md](references/subject-playbooks.md)
   - Named model dialect → [references/model-adaptation.md](references/model-adaptation.md)
   - Style mix → [references/style-presets.md](references/style-presets.md)
   - "Less AI" / plastic / CGI complaints → [references/anti-ai-look.md](references/anti-ai-look.md)
   - Tone and worked cases → [references/examples.md](references/examples.md)

4. **Build the prompt from engines below**
   Every clause must change the picture. Delete anything that does not.

5. **Anti-AI pass** using the checklist in this file.

6. **Adapt dialect** to the named model. If none, write model-neutral natural language.

7. **Quality gate**, then return the output format.

## Prompt architecture

Write in this order. Omit empty slots. Prefer one flowing paragraph (or 2–3 short ones). Do not emit labeled fields unless the target model wants JSON (Flux complex scenes).

| Slot | Question | Rule |
|---|---|---|
| Medium | What kind of capture? | `Photograph`, `photorealistic candid`, `studio product photo`, `35mm film still`. This switches the model into photo mode. |
| Subject | Who/what, specifically? | Age range, build, clothing, species, product, or architecture as relevant. No generic "a beautiful woman." |
| Action / pose | What is happening? | Verbs and body mechanics. Hands doing something real. |
| Environment | Where, when, weather? | Named or plausible place. Time of day. Air (dust, haze, humidity, cold). |
| Lighting | Source → direction → softness → colour → shadows → bounce | Never "beautiful lighting." |
| Materials | What would a camera resolve? | Only surfaces that matter at this distance. |
| Composition | Angle, framing, what is sharp | Match genre. Do not force cinematic every time. |
| Camera | Focal length, aperture, shutter only if they change the look | Match the scene. Do not flex random luxury bodies. |
| Colour / atmosphere | How does the world actually look? | Real colour relationships, not "vibrant." |
| Imperfections | What stops the CGI read? | One to four honest details. |
| Constraints | What must not happen? | Only if the model accepts them or the failure is likely. |

**Length targets**

- Still life / clean product: 40–80 words
- Portrait or simple scene: 60–110 words
- Environmental / travel / multi-element: 80–150 words
- Hard ceiling: ~180 words unless the user asked for extreme control or Flux JSON

Specificity beats length. A precise 70-word brief beats a 250-word adjective pile.

## Engines

### 1. Subject engine

Be concrete. Replace categories with instances.

- Weak: `a man on a bike in the mountains`
- Strong: `a man riding a dust-coated Royal Enfield along a high-altitude Ladakh road, gloved hands on the bars, jacket scuffed at the elbows`

Do not invent identity-defining facts (ethnicity, celebrity likeness, exact age, sacred iconography changes, brand-altering product details) when the user already set them — or when inventing them would replace the user's subject. If they said "Shiv Ji," use respectful, traditional Shaiva iconography. If they said "a man," do not turn him into a specific actor or a fashion model.

For people, default to **real humans**, not castings: slight asymmetry, lived-in skin, ordinary posture. See human-realism.md.

### 2. Camera engine

Choose optics from the job, then stop.

| Job | Default starting point |
|---|---|
| Headshot / tight portrait | 85–105mm, f/1.8–f/2.8, eye-level, focus on nearest eye |
| Environmental portrait | 50mm, f/2–f/2.8 |
| Street / documentary / travel | 28–35mm, f/2.8–f/5.6, eye-level or slightly low |
| Landscape / establishing | 24–35mm, f/8–f/11, deeper focus |
| Compressed landscape / wildlife isolate | 135–400mm, as needed |
| Architecture / interior | 16–24mm, camera level, f/8, verticals controlled |
| Product / packshot | 85–100mm, f/8–f/11, locked-off, true materials |
| Food | 50–90mm, f/2.8–f/5.6, 45° or overhead |
| Action / sports / vehicles in motion | 70–200mm or 35mm if you are in the scene; shutter fast enough to freeze or slow enough to streak — pick one |
| Cinematic still | 35–50mm, motivated light, restrained grade |
| Phone / candid social | 24–26mm equivalent, computational look only if requested |

Name a camera body or film stock **only** when it changes colour, grain, or format:

- Kodak Portra 400 — warm skin, gentle grain
- Fuji Classic Chrome / Superia — documentary, slightly cool greens
- Cinestill 800T — tungsten night, halation
- Hasselblad / medium format — fashion, product, tonal depth
- Direct-flash digicam — 2000s snapshot
- iPhone main camera — only for that vernacular

Do not write `shot on Hasselblad + 8K + RAW + DSLR + IMAX` together. One capture identity is enough.

Shutter and ISO belong only when they are visible: frozen spray, wheel blur, handheld night noise.

Full tables: cameras-lenses.md.

### 3. Lighting engine

Always answer: **where is the light, how hard is it, what colour is it, where do shadows fall, what does it bounce off?**

Templates (pick one, then specify direction):

- Soft window / north light — portraits, interiors, food
- Late-afternoon sun, low, warm, long shadows — travel, lifestyle
- High-altitude hard sun, thin air, cool skylight fill — mountains, desert
- Overcast dome — architecture, documentary, even skin
- Golden hour rim + cooler ambient — cinematic but still real
- Practical lamps / neon / fire as the motivated key — night
- Three-point softbox — e-commerce product
- Rembrandt / loop / butterfly / split — portraits (see lighting.md)
- Overcast + negative fill — editorial grit

Never write `cinematic lighting` or `studio lighting` alone.

### 4. Material realism engine

Describe how the surface behaves under *this* light.

Skin: pores, fine vellus hair, local colour shifts, oil only where oil lives, dry patches, not porcelain.  
Fabric: weave, weight, folds at joints, pills, dust, sweat marks if earned.  
Metal: clear vs blurred reflections, micro-scratches, edge wear, not chrome butter.  
Glass / water: refraction, condensation, meniscus, not plastic shine.  
Food: moisture, char, crumbs, steam only if hot.  
Ground: unevenness, tire dust, wet sheen, leaf litter.

Use two or three material notes, not a catalogue.

### 5. Environment engine

Make the place photographed, not assembled.

- Atmospheric perspective: distant forms lighter, lower contrast, slightly cooler or dust-stained
- Weather that matches geography (Ladakh = dry, thin, dusty — not tropical mist)
- Contact: subject casts on and receives from the ground
- Small true extras: a roadside cairn, a tea-stall tarp, a scuff on a tank, a stray dog — only if they belong
- No floating objects, no cloned crowds, no impossible suns

### 6. Composition engine

Pick **one** primary idea.

- Rule of thirds — travel, documentary
- Centre / symmetry — architecture, ritual, formal portrait
- Leading lines — roads, corridors, rivers
- Layered FG / MG / BG — landscapes, street
- Over-the-shoulder or three-quarter — narrative
- Low angle — machines, reverence, scale
- High angle / overhead — food, maps of a table
- Close-up / medium / wide — choose from the idea, not from habit

State camera height and whether the subject looks at camera. Hands and feet: either include them correctly or crop with intent.

### 7. Colour engine

Describe relationships, not adjectives.

- Warm key vs cool shadow (sun + sky)
- Sodium / neon / tungsten vs dusk blue
- Altitude: bleached earth, hard blue zenith
- Food: true edible colour, not neon saturation
- Skin: undertone variation, not one airbrushed fill

Avoid `vibrant`, `HDR`, `colorful`, `epic grade` unless the user wants a specific grade (teal-orange, bleach-bypass, etc.).

### 8. Human realism engine

When people are in frame, include a few of these — not all of them:

- Skin texture appropriate to age, sun, and climate
- Asymmetry in brows, smile, ears, posture
- Eyes: moisture, natural catchlight from the actual key, not decorative sparkles
- Hair: stray strands, parting that is not engraved, flyaways in wind
- Hands: five fingers, age-true, doing a job, nails not glossy unless they would be
- Teeth: only if the mouth is open; slightly uneven, not veneer-white
- Expression: a motive (concentration, fatigue, amusement), not "stunning smile"
- Clothes occupying space: pull, fold, dust, sweat

Avoid: `flawless`, `perfect skin`, `beautiful face`, `model looks`, ring-light clamshell unless the brief is beauty.

Full protocol: human-realism.md.

### 9. Anti-AI look system

Before emitting the prompt, scan for these and correct **in the positive prompt** (or a short model-appropriate negative):

| Tell | Correction |
|---|---|
| Plastic / waxy / poreless skin | Lived texture + directional light that casts micro-shadow in pores |
| Perfect symmetry | Slight asymmetry, uneven hair, natural posture |
| Dead or jewel eyes | Moisture + catchlight matching the key |
| Extra / melted fingers | Hands occupied or cropped; "natural grip" |
| Fake HDR / crunchy halos | Natural dynamic range, unclipped but not glowing |
| Oversharpened pores / hair | "unretouched photograph", mild grain, not "ultra detailed skin" |
| Beauty-filter smoothness | Ban `flawless`, `perfect`, `airbrushed` from your own prompt |
| Impossible light (two suns, shadowless noon + golden rim) | One motivated key, consistent shadow direction |
| Fake circular bokeh wallpaper | Only mention bokeh if the lens and distance would produce it |
| Floating subject | Contact shadow, dust, weight |
| CGI metal / glass / food | Real reflectance, dirt, crumbs, fingerprints if earned |
| Keyword spam | Delete quality tokens |

Banned filler (never add unless a specific model doc says that exact token is required):

`8K`, `4K`, `UHD`, `ultra HD`, `masterpiece`, `best quality`, `insanely detailed`, `award winning`, `hyper realistic`, `ultra realistic`, `trending on artstation`, `octane render`, `Unreal Engine`, `perfect`, `flawless`, `stunning`, `beautiful lighting`, `highly detailed environment`

Useful mode-switch words (use one, not five): `photograph`, `photorealistic`, `candid`, `unretouched`, `documentary still`, `studio product photo`.

OpenAI-family models respond well to the literal word **photorealistic**. Flux and Midjourney respond better to camera + light + texture. Do not stack both strategies blindly.

## Model adaptation

If the user names a model, adapt. Never invent undocumented flags.

| Model | Dialect | Negatives | Settings to suggest |
|---|---|---|---|
| Unspecified | Natural-language brief | Omit, or a short "avoid" sentence only if failure is likely | Aspect ratio, framing |
| Midjourney (V7 / V8) | Natural language + flags at end | `--no` sparingly | `--raw` or `--style raw`, `--s 20–80` for literal photo, photographic `--ar` (`3:2`, `2:3`, `16:9`, `4:5`, `9:16`). Do not use Niji for photoreal. |
| Flux.2 / FLUX.1 | Important words first. Natural language. Optional JSON for multi-subject or brand colour | **Flux.2 has no negative prompts** — describe the desired scene | Aspect; hex colours if brand-critical |
| SD 1.5 / SDXL / SD3 | Token phrases, optional `(weight:1.2)` | First-class negative, short and relevant | CFG ~5–8 for photo, 20–30 steps, native res |
| GPT Image / DALL·E / ChatGPT | Full sentences. Include `photorealistic`. Constraints as preserve/change | Prefer positive constraints (`empty street`, `no extra text`) | `quality=high` for faces, text, identity |
| Gemini / Nano Banana / Imagen | Official photo template: shot type + subject + setting + light + angle + lens | Semantic negatives | Aspect in prompt or API |
| Ideogram | Clear style + any in-image text in quotes | Short | Photorealism style preset if available |

Details and copy patterns: model-adaptation.md.

## Style control

Honour named styles. Combinations are allowed (`documentary + cinematic` = observed event, motivated light, restrained grade, no poster posing).

Defaults live in style-presets.md:

raw documentary · professional photography · cinematic realism · fashion · street · travel · wildlife · product · architectural · historical · religious/devotional · editorial

If the user does not name a style, pick the one the scene would actually be shot in (a mug on white = product; a rider in Ladakh = travel; Shiv Ji in the Himalayas = devotional realism, not fantasy art).

## Video-ready mode

Activate when the user says the still will be animated, used in Kling / Runway / Veo / Sora, or "make it suitable for video."

Prefer:

- One clear subject, readable silhouette
- Stable, simple-to-parse depth (FG / subject / BG)
- Physically possible pose that can begin motion
- Consistent light direction
- Locked practicals (lamps, sun, signs) with real placement

Avoid:

- Impossible anatomy or pretzel poses
- Tiny chaotic texture carpets
- Ambiguous object ownership (whose hand, which cup)
- Heavy motion blur already in the still (let the video model add motion)
- Crowds of extra faces

Mention a plausible next action in one clause (`he is mid-turn into the curve`, `steam is just beginning to rise`) so the video model has a direction.

## Iterative refinement

When the user revises (`make the skin real`, `make it night`, `change to 9:16`, `more documentary`, `less AI`):

- Change **only** the requested slots
- Keep subject, identity, wardrobe, location, and locked props
- Restate the full updated prompt (do not emit a diff unless they ask)
- If they change time of day, rebuild light, colour, and atmosphere so they stay physically consistent

## Output format

Return exactly these sections. Omit a section if it is empty or not useful.

### Main Prompt

A single production-ready brief. Copy-pasteable. No preamble, no bullet labels inside it.

### Negative Prompt

Only if the target model benefits (SD family, Midjourney `--no`, or the user asked). Keep it short and failure-specific.  
If the model rejects negatives (Flux.2) or prefers semantic positives (Gemini, GPT Image), write:

`Not used for this model — constraints are already in the main prompt.`

### Suggested Settings

Only relevant lines:

- Aspect ratio (and why, in a few words)
- Framing (close-up / medium / wide)
- Model flags or quality
- Video note if applicable

Do not list samplers, seeds, or CFG unless the user is on a local SD/Flux stack or asked.

### Optional: Director's note

One to three short bullets **only** when a choice is non-obvious (why 35mm not 85mm, why overcast not golden hour). Skip for simple briefs.

## Intelligent interpretation

Short user lines are complete enough. Expand photographically without changing the idea.

| User said | You may infer | You may not invent |
|---|---|---|
| `man riding a Royal Enfield in Ladakh` | altitude, dust, hard sun, riding kit, broken tarmac, 35mm travel framing | a celebrity face, a specific year plate slogan, a fantasy sky |
| `realistic photo of Shiv Ji meditating in Himalayas` | traditional iconography, snow, thin air, dawn or high overcast, respectful stillness | Western fantasy armour, casual modern streetwear, parody |
| `a ceramic mug on a table` | studio or window light, true ceramic glaze, contact shadow | a brand logo, extra lifestyle clutter |

Cultural and religious subjects: accurate, dignified, specific. Do not "Hollywood-ise."

## Final quality check

Do not return until all ten pass:

1. User's idea is intact
2. Scene is physically possible
3. Light has one motivated logic
4. Camera matches the job
5. Place feels photographed, not composited
6. Materials behave
7. A few honest imperfections exist
8. No keyword spam
9. Typical AI tells were countered
10. A photographer could shoot this brief

## Tiny example

User: `A man riding a Royal Enfield in Ladakh`

### Main Prompt

Photorealistic travel photograph of a man riding a Royal Enfield motorcycle through a high-altitude Ladakh landscape. He sits naturally on the bike in a wide curve, gloved hands on the handlebars, dust-dulled riding jacket and worn jeans, half-face helmet with goggles lifted to the brow. Broken tarmac and pale gravel, a low trail of dust off the rear tyre. Barren ochre mountains and a far snow line under a thin, hard blue sky. Late-morning sun from camera right, sharp shadows on the road, a narrow warm rim on the rider's shoulder and the chrome of the exhaust. Low three-quarter front angle, 35mm lens at f/5.6, bike and rider sharp, distant ridges slightly softened by dry air. Unretouched colour, fine dust in the light, documentary rather than poster.

### Negative Prompt

Not used unless the model is SD/Midjourney. Then: `cgi vehicle, extra wheels, plastic skin, oversaturated hdr, illustration, watermark`

### Suggested Settings

- Aspect ratio: 3:2 or 16:9 (travel still)
- Framing: medium-wide, rider + road + mountains
- Midjourney: `--raw --s 40 --ar 3:2`
- Flux.2: no negative; keep this word order
- Video-ready variant: freeze the wheels (no motion blur), keep the lean readable, hold a clean skyline
