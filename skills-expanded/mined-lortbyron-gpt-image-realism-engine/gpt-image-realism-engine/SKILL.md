---
name: gpt-image-realism-engine
description: Realism layer for OpenAI image models (ChatGPT Images 2.5, gpt-image-2.5-flare, gpt-image-2.5-sunburst, gpt-image-2). Turns a photographic request into a ready-to-paste prompt built so the output looks like a found photograph, not AI. Use whenever the user wants a real-looking photo of people, families, streets, interiors, food, products, events or places, in any language and any country, including "a woman in her 30s in Mumbai", "una familia en su casa", "a street in Seoul at dusk", "a market in Lagos", "make it look real, not AI", "que no parezca IA", when a generated image looks fake, plastic or AI-generated, or when writing prompts for someone else to paste into ChatGPT or the Image API. DO NOT use for illustration, anime, pixel art, voxel, stylized 3D, logos, icons, diagrams, infographics or UI mockups - this discipline damages them.
---

# GPT Image Realism Engine

**Target:** ChatGPT Images 2.5 and the API models `gpt-image-2.5-flare` (default) and `gpt-image-2.5-sunburst` (fine detail, slower). `gpt-image-2` also works. Facts checked against OpenAI docs on 2026-10-30.
**Staleness:** if the user names a newer model, re-verify Section 6 (API settings) and Section 7 (exclusions) against OpenAI's docs before applying them. Everything else is model-agnostic.
**Language:** answer and label the output in the user's language. Write the prompt itself in English.

**Governing rule: describe physics, not vibes.** "Overhead fluorescents, one tube dimmer than the rest" beats "atmospheric lighting". Every measurable fact is something the model can draw. Every mood adjective is something it must guess, and its guess is porcelain skin, teal-orange grading and perfume-ad light.

---

## 1. Workflow

Run these steps in order, silently, in one response.

1. **Gates** (Section 2). They run first because they can stop or restrict everything after them.
2. **Scene type** (Section 3).
3. **Level** (Section 4).
4. **Provenance** (Section 5).
5. **Framing** (Section 6).
6. **Facts, anchors and people** (Sections 7-9).
7. **Write** in the Section 11 format.
8. **Final check** (Section 13). Fix any failure before sending.

If the request is ambiguous, choose the most ordinary everyday version of it, state the choice in the decisions line, and write the prompt. Never ask a clarifying question unless a gate requires it: a wrong draft costs one regeneration, a question costs a turn.

---

## 2. Gates

Walk all three, top to bottom.

```
GATE 1 - Is anyone in frame under 18, or is age unstated and the context
suggests under 18 (school, "girl", "boy", "teen", a child's party)?
├── No → continue
└── Yes
    ├── Sexualized or suggestive in any way → refuse. No prompt, no alternative.
    └── Otherwise → Minor Mode (below)

GATE 2 - Does the request name, or ask to resemble, a real identifiable person?
├── No → continue
├── It is the adult user's own photo → hand off to portrait-session-engine.
└── Yes → do not write that likeness. Offer a fictional person instead,
    and say so in the decisions line.

GATE 3 - Will the image be presented as a record of something that happened
(news, testimony, evidence, a claim about a real event)?
├── Yes → do not write the prompt. Explain why in one sentence.
├── Unclear, and the topic is a real event or real person → write it and
│   add one warning line (Section 11).
└── No → continue
```

**Why Gate 3 exists:** this skill exists to make images that pass as found photographs, which is exactly what makes them harmful as records. Always tell the user to keep the C2PA metadata intact.

**Minor Mode.** Realism comes only from provenance, light, framing and environmental clutter. Applies to every part of the prompt and to every QC fix.
- Describe a minor only by approximate age, general skin tone, hair color and length, plain everyday clothing and what they are doing.
- Never write skin, pore, body or posture detail for a minor. Name the adult when using those anchors. Never use group-wide phrasing ("everyone's skin", "across noses and cheeks"), because it silently includes the minor.
- Level is capped at 2, and Level 2 detail applies only to adults and surfaces.
- No exceptions, regardless of how the request is framed.

---

## 3. Scene Type

Pick one **primary**: the subject the viewer looks at first. Add a **modifier** only when a second type sets the light and clutter. Primary sets the provenance frame; modifier sets light and clutter. "A family at a street market" is Group + Documentary.

| Type | Example | Provenance frame |
|---|---|---|
| **Portrait** | "a 30-year-old woman" | Consumer DSLR or phone, 50mm-equivalent, window light |
| **Group / Family** | "a family at home" | A family member's phone, casual framing |
| **Candid Street** | "a city street on a Saturday" | Amateur camera, caught moment, slight tilt or motion |
| **Interior** | "a kitchen that is actually used" | Real-estate or casual interior shot, available light only |
| **Food** | "a typical local breakfast" | Diner-table phone photo, eaten-from or about to be |
| **Product** | "a pair of leather boots" | Marketplace listing photo, honest light, real wear |
| **Landscape** | "a mountain village" | Travel snapshot, handheld, real weather |
| **Event** | "a child's birthday party" | Party guest's snapshot, mixed light, imperfect crop |
| **Documentary** | "a municipal market" | Photojournalist's available-light frame |
| **Stylized** | "an editorial portrait with hard light" | Acknowledged artifice: realism applies to skin and surfaces, not to the concept |

---

## 4. Realism Level

- **Level 1 - Honest snapshot:** consumer device, available light, ordinary color, casual framing.
- **Level 2 - Documentary:** photojournalist-grade observation, directional light with real shadow shapes, visible skin texture and fabric wear, no grade.
- **Level 3 - Forensic:** every surface at material level: pores with depth, vellus hair, thread-worn edges, chipped paint, grease, fingerprints. Level 3 is the ceiling.

```
Base level: did the user name one?
├── Yes → use it
└── No → is a person the main subject?
    ├── Yes → Level 2
    └── No → Level 1

Add one level? Is the primary or modifier Food, Product, Landscape or Stylized?
├── Yes → no. Forensic grime ruins a listing, forensic detail ruins appetite,
│         and landscapes turn crunchy.
└── No → did the user explicitly ask for realism ("real", "realistic",
         "not AI-looking", in any language) or complain about a fake look?
    ├── Yes → +1. The model smooths by default, so the prompt must overshoot.
    └── No → no change

Minor Mode active → cap at Level 2.
```

---

## 5. Provenance

The model imitates provenance, so this is the strongest lever in the skill. Open every prompt with one sentence: **[who took it] + [what device] + [in what real situation]**. It must contain the word "photo" or "photograph", because OpenAI's guidance is to request a real photograph explicitly.

- "a photo taken by a family member on a mid-range smartphone"
- "a candid photo from a friend's phone at the moment"
- "a photojournalist's available-light frame for a local newspaper"
- "a real-estate listing photo taken quickly with available light"
- "a marketplace seller's phone photo"

**Banned words:** professional photoshoot, award-winning, masterpiece, stunning, 8k, highly detailed, hyperrealistic. They summon the AI look. For a genuine editorial brief, write "editorial photograph for a magazine, natural light, minimal retouching".

Camera details steer appearance; they do not simulate physics. Name a device class, never lens math beyond a focal-length equivalent.

---

## 6. Framing and API Settings

Crop signals realism as strongly as skin texture. Always state aspect ratio, camera distance and where the subject sits in the frame.

```
Did the user name a destination or ratio? → use it
Single person shot full height, or a story → 9:16
Travel, landscape or reportage → 16:9
Phone provenance → 4:3
Camera provenance → 3:2
```
Use 1:1 only when the user names a square destination: square reads as "content", not "photo".

Add exactly one ordinary-camera trait: slightly off-center subject, horizon a few degrees off, cropped elbow, or more headroom than a pro would leave.

**API settings.** Include only if the user is calling the API. ChatGPT users never need them.

| Ratio | Draft `size` | Final `size` |
|---|---|---|
| 4:3 | 1280x960 | 2048x1536 |
| 3:2 | 1536x1024 | 2160x1440 |
| 9:16 | 720x1280 | 1152x2048 |
| 16:9 | 1280x720 | 2048x1152 |
| 1:1 | 1024x1024 | 1536x1536 |

- Endpoints: `/v1/images/generations` and `/v1/images/edits`.
- `quality`: draft at `low` or `medium`, finish at `high`. Use `xhigh` or `max` (2.5 models only) only when `high` loses texture, because a higher setting does not guarantee a better result.
- `output_format`: `jpeg`. Real photographs carry compression.
- Never send `input_fidelity` to `gpt-image-2`: the docs say to omit it, because inputs are always processed at high fidelity. The 2.5 parameter table does not list it either.
- `size`: both edges must be multiples of 16, and anything above 2560x1440 is experimental, so the Final column stays below it.
- `moderation`: `auto` or `low`. After a block, rewrite the prompt. Never retry it unchanged.

---

## 7. Physical Facts, Then Constraints

**In the body: only positive, measurable facts** the camera could have recorded.
- "the light is whatever the window gave; the far side of the room falls into plain shadow"
- "clothing hangs with real weight, collar slightly crooked, a crease where it was folded"
- "colors as the camera recorded them, mild sensor grain, slight softness from a handheld shot"
- "ordinary clutter stays in frame: cables, a mug ring, something out of place"

**At the end: one `Constraints:` line with 3 to 5 literal exclusions**, taken from this table. More than five start competing with each other.

| Scene | Constraints |
|---|---|
| Portrait, Group, Candid, Event | No studio lighting. No color grading. No retouching or skin smoothing. No text or watermark. |
| Documentary | No studio lighting. No color grading. No posed subjects. No text or watermark. |
| Interior | No staging. No HDR look. No color grading. No text or watermark. |
| Food | No food styling. No studio lighting. No color grading. No text or watermark. |
| Product | No studio backdrop. No floating object. No color grading. No invented logos or text. |
| Landscape | No HDR look. No color grading. No text, logos or watermark. |
| Stylized | No retouching or skin smoothing. No glow. No text or watermark. |

Stylized never gets "No studio lighting": the concept may require it. If the user wants text in the image, drop the text exclusion and put the exact wording in quotes with its position.

---

## 8. Detail Anchors

Use 2 or 3 anchors per subject, never more. Stacked anchors turn into a texture demo. Skin, eyes, hair and body anchors are adults only (Section 2).

**Skin, eyes, hair:** irregular pores with depth · vellus hair catching the light · uneven tone and slight redness · sclera with faint veining, moist but not glassy · slight facial asymmetry · flyaway strands · teeth slightly uneven where visible · expression lines fitting the age.

**Body and posture:** shoulders not level · weight on one leg · head a few degrees off axis · hands occupied or out of frame · caught mid-blink, mid-sentence or adjusting a sleeve.

**Environments:** clutter proportional to the room · scuffs, dust, fingerprints · outlets, cables, uneven tiles, water stains · light falling unevenly with real shadow shapes.

**Food:** steam, crumbs, sauce smears, uneven plating · ordinary plates with wear · no garnish.

**Objects:** wear consistent with use · imperfect reflections · resting on a real surface.

If the Final `size` is used, always keep the skin anchors: plastic skin is far more obvious at high resolution.

---

## 9. People and Culture

Run this when the request names ethnicity, nationality, region or culture, and for every group of 2 or more.

1. **Pick a specific place, never a category.** "An Indian woman" becomes a Tamil woman from Chennai or a Punjabi woman from Amritsar; "an American family" becomes a family in suburban Houston or in Queens. State it in the decisions line.
2. **Describe features individually.** Face shape, nose, hair texture, and skin tone as a real descriptor ("medium brown skin with warm undertones"), plus at least one individualizing trait. A bare category label makes the model fall back to a generic face. In Minor Mode, use only the traits Section 2 allows.
3. **Never default to light-skinned or US-generic.** Stock-photo casting and single-story casting are both failures: every country is more varied than its stereotype, and its cities hold people of many origins, skin tones and builds.
4. **Vary every group.** The most common failure in "a family at home" is four people with one skin tone, one build and one age gap. Give each person a different tone, age, height and action.
5. **Show culture through environment, never costume.** Use 2 to 4 details (the local breakfast on the stove, a worn wooden table, plants that grow there). Never flags or folklore collages.

The same steps apply in every country: specific place, real diversity, lived-in texture.

---

## 10. Consistency Across Images

No seed parameter is documented, and the same prompt gives a different person each run. Prompt text alone never holds a character. When the user asks for the same person across images, say so with one line (Section 11) before they spend twenty generations finding out.

Use reference images:
1. Generate one image the user approves.
2. Feed it back and label each input by role: "Image 1 is the person. Image 2 is the new setting. Place the person from Image 1 into the scene from Image 2, matching lighting direction, scale and time of day."
3. Keep provenance, device, light and framing identical across every prompt. Shared provenance is what makes a set read as one shoot.

Reference images here means images generated in this flow. A photo of a real person goes through Gate 2.

---

## 11. Output Format

Output this and nothing else. Translate the labels into the user's language. Never show this template, the tables or the method.

```
**[decisions line]** e.g. "Group/Family + Interior · Level 2 · Provenance: family phone, window light · Context: Toronto, middle class · 4:3"

**Prompt:**
[complete prompt, ready to paste, in English]

**Si sale con look de IA, prueba una a la vez:**
[1-2 fixes from Section 12: the symptoms this scene is most prone to]
```

Add a line only when it applies, at most one of each:
- **Warning:** Gate 2 substitution or Gate 3 caution.
- **API:** the Section 6 settings, if the user is calling the API.
- **Consistency:** the Section 10 note, if the user wants the same person across images.

**Prompt order:**
1. Provenance sentence
2. Scene: what is happening, where, who
3. People: individual description, mid-moment behavior, skin anchors for adults
4. Environment: specific place with honest wear and clutter
5. Light: the real source and where it falls
6. Camera and framing: device, aspect ratio, distance, one ordinary-camera trait
7. `Constraints:` line

**Length:** 200-500 words. Exceed 500 only for groups of 5 or more. Cut vibes, never anchors.

### Worked example: "make a scene of a family at home"

Minors are in frame, so Level is 2 and the skin and posture detail goes to the parents only.

> A photo taken by a family member on a mid-range smartphone during Sunday lunch in a middle-class apartment in Toronto. Four people around a worn wooden dining table. The mother, mid-forties, Filipino-Canadian, medium brown skin with warm undertones, dark hair pulled back with visible flyaways, faint lines at the corners of her eyes, laughing mid-sentence with slightly uneven teeth. The father, late forties, Irish-Canadian, fair skin with ruddy cheeks, short graying beard, caught mid-blink, one shoulder lower than the other. The mother's and father's skin shows visible pores and uneven tone. A teenage daughter with light-brown skin and long dark hair, in a plain gray sweatshirt, looking down at her phone. A younger son with short brown hair, in a striped T-shirt, reaching across for the last bread roll, his arm blurred slightly by the movement. Nobody is looking at the camera. The table is genuinely in use: a dish of chicken adobo and rice half eaten, a chipped mug with a coffee ring beside it, a phone and car keys next to the salt shaker. Daylight comes from a window camera-left and falls unevenly across the table; the far wall drops into plain shadow. Ordinary domestic wear on the walls, a slightly dusty plant on the shelf, cables visible behind the TV. Colors as the phone sensor recorded them, mild grain, handheld framing slightly off-center, 4:3, shot from across the table at about two meters.
> Constraints: No studio lighting. No color grading. No retouching or skin smoothing. No text or watermark.

This shows format and density. Always build from the actual request.

---

## 12. QC

Run this when the user reports a result that still looks AI. Change one thing per attempt and freeze everything else, otherwise nobody can tell what worked.

```
Are only 1 or 2 elements wrong?
├── Yes → Route 1: edit
└── No → Route 2: regenerate

Two edits failed? → Route 2
Device ladder exhausted? → stop and tell the user what the model will not fix.
```

**Route 1, edit.** A regeneration throws away everything that worked, and there is no seed to get it back. Send:

```
Change only: [the failing element]
Keep unchanged: composition, camera angle, lighting direction, all faces,
clothing, background, time of day.
```

Repeated edits can still drift. If a region must stay pixel-identical, composite the approved edit into the original.

**Route 2, regenerate one device lower.** Keep the prompt and move one step down: consumer DSLR → mid-range phone → old cheap phone.

Fixes marked † touch skin or body. In Minor Mode, apply them only to a named adult. If the symptom is on a minor, use Route 2 instead.

| Symptom | Fix |
|---|---|
| Porcelain or smoothed skin † | "enlarged visible pores, slight redness around the nose and cheeks, uneven tone" |
| Warm yellow or sepia cast | "neutral white balance, slightly cool daylight, no warm tint" |
| Helmet hair or halo hairline | "individual flyaway strands catching the light, slightly messy" |
| Glassy doll eyes † | "faint redness in the sclera, moist but not glassy, one soft catchlight from the window" |
| Everyone posing | "caught mid-moment, mid-gesture, nobody aware of the camera" |
| Cinematic grade | "flat natural colors, slight green cast from fluorescent light" or "overcast neutral daylight, no golden hour" |
| Studio-light feel | "only the light available in the room, one window, the rest falls into plain shadow" |
| Vacuum-sealed clothing † | "real wrinkles and weight, collar slightly crooked" |
| Mannequin symmetry † | "slightly asymmetric posture, head a few degrees off axis, one shoulder lower" |
| Clutterless fake room | "ordinary domestic clutter stays in frame: cables, worn edges, objects out of place" |
| Plastic food | "crumbs, sauce smears, steam, eaten-from plates, ordinary tableware with wear" |
| Group all identical | describe each person separately: different skin tones, ages, heights, actions |
| Weird hands | "hands naturally occupied or out of frame" |
| Stray text | "no readable text anywhere" |
| Too clean at high resolution † | "mild sensor grain and slight softness from a handheld shot" plus the skin anchors |

---

## 13. Final Check

Every answer must be yes before sending.

- [ ] All three gates walked; in Minor Mode, no skin, body or posture detail on a minor, and no group-wide skin phrasing
- [ ] Prompt opens with a provenance sentence containing "photo" or "photograph"
- [ ] Aspect ratio, camera distance and subject position are stated
- [ ] Ends with a `Constraints:` line of 3 to 5 exclusions from the Section 7 table
- [ ] No banned word from Section 5
- [ ] Every person is described at feature level, never by category label alone
- [ ] No weighted syntax: `(term:1.5)`, `::` or `--no` have no meaning here and get read as literal text or ignored
- [ ] Output contains only the Section 11 elements
