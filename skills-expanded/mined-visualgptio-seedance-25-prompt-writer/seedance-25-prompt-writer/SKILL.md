---
name: seedance-25-prompt-writer
description: >-
  Write, optimize, or rewrite prompts for Dreamina Seedance 2.5 video generation — plain
  text-to-video, image/video/audio-referenced generation, 30-second timestamp storyboards,
  30–180s long video, video extension, local editing, transitions, white-model rendering, and
  multilingual output. Use this skill whenever the user mentions Seedance, Dreamina, Jimeng,
  即梦, AI video prompts, 视频提示词, storyboards, shot lists, camera-movement prompts, or asks
  why a generated clip drifted, changed the character's face, hard-cut badly, or came back with
  subtitles and BGM nobody asked for — even when they never name the model.
  当用户需要撰写、优化或改写 Seedance 2.5 的文生视频 / 图生视频 / 多模态参考提示词、时间戳分镜脚本、
  长视频脚本、视频延长与转场提示词，或想排查画面漂移、人物串脸、乱加字幕与 BGM 等问题时使用本 Skill。
---

# Seedance 2.5 Prompt Writer

All rules below are extracted from the official *【Dreamina】Seedance 2.5 User Guide*. Anything
not from that guide is tagged **[inferred]** or **[non-doc]**.

## Hard limits to respect

Do not write a prompt that violates these — the platform will reject or degrade it.

| Item | Limit |
|---|---|
| Standard single generation | 4–30 s (97–721 frames) |
| Long Video mode | 30–180 s in one pass |
| Video extension | source clip must be under 30 s; extend 4–30 s per pass; nest up to 60 s total |
| Output resolution | 480p / 720p |
| Reference images | up to 30 per request |
| Reference videos | up to 10, each 2–30 s, total ≤ 30 s |
| Reference audio | up to 10, each 2–30 s, total ≤ 30 s; audio-only input is supported |
| Stability sweet spots | 1–5 subjects (6–10 works but needs re-rolls); 1–8 subject images (9–12 shakier); 5–10 s reference clips; edit targets under 20 s; 1–5 reference images for edits |

When extending, the duration you request is the length of the **new segment only**, not the total.

## Core principles

1. **Not a sentence describing a moment — a production brief with a fixed running order.**
   The guide's formula is: asset declaration → one-line summary → plot in time order → global
   supplement. A beautiful flowing sentence has no scaffolding for 30 seconds.
2. **Not "hopefully it won't add junk" — forbid it in writing.** The guide states plainly that if
   you want clean footage you must write "pure video, no subtitles, no background music". Negative
   description is a first-class element, not an afterthought.
3. **Not sequence words — real timestamps.** Seedance 2.5 natively honors time intervals and frame
   numbers. "Then… after that… finally" gives the model permission to fast-forward; `[00:10 - 00:15]`
   does not.
4. **Not "copy the reference" — assign each asset a job and lock what must not move.** Number assets
   in upload order, say what each one is for, and re-`@` them throughout. The guide is explicit that
   mentioning an asset repeatedly makes the result more accurate.
5. **Not "a beautiful woman" — seven dimensions of physical detail.** Generic subjects are what
   produce the plastic-skin, twin-faced, AI-looking output the character formula exists to prevent.

## Writing workflow

Work these six steps in order. Do not skip step 1 — the mode determines which formula applies.

### Step 1 — Fix the intent and pick the mode

**Do:** Decide target duration, aspect ratio, and which generation mode the user is in, because each
mode has its own formula.

**How:**

| Situation | Mode | Formula to use |
|---|---|---|
| ≤ 30 s, simple single scene | Standard | Basic formula (below) |
| ≤ 30 s, multi-beat or one-shot showpiece | Standard | 30-second formula (below) |
| 30–180 s | Long Video | Super-long formula (below) |
| Continuing an existing clip | Extend Video | Extension formula (below) |
| Changing part of an existing clip | Smart Edit / Edit with marks | Edit formula (below) |
| Rendering a Maya/Blender white model | Clay Renderer | White-model formula (below) |

**Counter-example:** Writing a 30-second timestamp storyboard and then sending it to a 5-second
standard generation. The beats get crushed and the model drops most of them.

### Step 2 — Declare the assets

**Do:** If the user uploaded anything, open with an asset manifest.

**How:** Asset number (in upload order) + what it is for — character, timbre, action, or scene.
Then, for anything that must not drift, add the lock sentence:
*"Based on the uploaded [asset type], strictly keep [X] consistent, strictly lock [Y]."*
Re-`@` each asset inside the shot descriptions where it matters.

**Counter-example:** "Use the attached images." The model has to guess whether image 3 is a prop, a
location, or a second character.

*If there are no reference assets, skip this step entirely — the guide says it can be ignored.*

### Step 3 — Write the one-line summary

**Do:** One sentence that sets the whole tone before any detail.

**How:** Subject + location + event + theme/style + any special camera movement.

**Counter-example:** Opening with "cinematic, 8K, masterpiece, highly detailed" — a keyword pile with
no subject, location, or event tells the model nothing about what happens.

### Step 4 — Build the global settings block (30 s and above)

**Do:** For anything over about 10 seconds, lock the world before you direct the action. This block
is what stops the character's outfit and the room's architecture from mutating mid-clip.

**How:** `[Base environment & texture] + [Visual style] + [Camera language] + [Character styling] +
[Core performance] + [Negative prompts]`

- Base environment & texture = time + place + atmosphere + a texture demand such as "emphasize
  extreme realistic physical texture"
- Visual style = cinematic / photoreal / 2D-cel + depth-of-field control + lighting method
- Camera language = shot size / angle + a detailed description of how it moves
- Character styling = the seven-dimension character formula, or `@` the reference image *and*
  describe it. For an object subject instead: quantifier + colour + shape/design style + specific
  object noun + material detail / wear state + iconic feature
- Core performance = the one or two things the finished clip must actually sell
- Negative prompts = pull from four directions: sound, subtitles, behaviour, and whatever is most
  likely to collapse in this particular scene

**Counter-example:** Putting the character description inside shot 3 only. Shots 1 and 2 will invent
their own version of the character and the cut will not match.

### Step 5 — Write the timestamp storyboard

**Do:** Slice the runtime and give each slice explicit content.

**How:** Per slice —
1. `[start s – end s]` + a named core phase (e.g. *Resignation — Swallowing the Bitterness*)
2. Physical directives: scene + composition + specific character/subject action, expression, dialogue,
   sound effects
3. Emotional analysis or camera subtext — explain to the model *why* the physical directive exists
4. If this slice cuts, add the transition instruction (see the transition formula)

Frame numbers work as well as seconds (`Frames 0-90 (0s - 3s)`, `Frame 32`).

**Counter-example:** "She looks sad, then walks away, then it starts raining." No durations, so the
model compresses all three into the first four seconds and holds on an empty frame.

### Step 6 — Add the global supplement, then self-check

**Do:** Close by re-stating what must hold true across the entire clip, then run the checklist.

**How:** Camera position + environment/scene features + overall sound and atmosphere + lighting.
Repeat the global prohibitions here too — subtitles and BGM in particular are worth saying twice.

**Counter-example:** Ending on the last shot description. The model treats late instructions as
local to that shot, and global constraints stated only at the top get diluted over 30 seconds.

## Element quick reference

### Subject / character

| | |
|---|---|
| Writing points | Seven dimensions: age/ethnicity, skin tone & texture, facial detail, eyes/soul, hair, clothing & fabric, physique/emotion/aura. Works for animated characters too. |
| Recommended | "22-year-old East Asian woman with a classical, gentle cinematic face. Cool-toned fair skin retaining realistic fine pores and natural skin texture. Slender eyes, delicate straight nose bridge, full lips, soft jawline. Gaze gentle and focused, revealing deep attachment." |
| Counter-example | "A pretty Asian girl, very beautiful." |

The dimension detail that matters most: **skin** needs a fidelity suffix ("retaining realistic fine
pores and natural skin texture", optionally freckles or blemishes) to avoid flat plastic white;
**facial features** need at least 3–4 points combined to be recognisable; **hair** should never be
just "black hair" — give colour, condition, style noun, and how it interacts with wind or movement.

If the storyboard already specifies composition and character action, drop those two sub-items from
the physique dimension rather than contradicting yourself.

### Action

| | |
|---|---|
| Writing points | Concrete physical verbs plus the physics you expect back. Complex long-tail movement is supported — describe it rather than simplifying it. |
| Recommended | "The tyres grind against the road, sparking orange friction sparks, executing a tight S-curve through the burning debris." |
| Counter-example | "Make it dynamic and exciting." |

### Camera

| | |
|---|---|
| Writing points | Shot size or angle + how it moves + a speed qualifier. State whether it is one continuous shot or cuts. |
| Recommended | "The camera pushes in extremely slowly toward the coffee cup. No shake, no characters entering frame, hard cuts prohibited." |
| Counter-example | "Cinematic camera work." |

### Lighting

| | |
|---|---|
| Writing points | Name the source, the direction, and the physical effect you want. |
| Recommended | "Sunlight slants in from the horizon, piercing the mist to create a Tyndall effect (volumetric lighting)." |
| Counter-example | "Good lighting, well lit." |

### Style & texture

| | |
|---|---|
| Writing points | Style family + depth-of-field control + a texture demand. For realism, ask for native skin texture and distinct hair roots. |
| Recommended | "Classic BBC period-drama style, warm gold and ivory palette, high-contrast candlelight, film grain texture." |
| Counter-example | "Realistic, 4K, masterpiece." |

### Dialogue

| | |
|---|---|
| Writing points | Write the line verbatim in the target language, inside the time slice where it lands. Add tone direction. Say explicitly whether it should be voiced without subtitles. |
| Recommended | "She says in a barely audible but steadied voice: \"You can go.\" (Voiced only, no subtitles.)" |
| Counter-example | "She says goodbye sadly." |

### Sound & audio

| | |
|---|---|
| Writing points | Audio is not a separate block — it lives inside each time slice (SFX, dialogue) and in the global supplement (overall sound and atmosphere). For voice cloning, reference the audio asset and add an emotional instruction. |
| Recommended | "Reference @Audio 1 for timbre saying 'I found you', keep a low, suspenseful tone." Global: "Only real natural white noise — rain on glass, subtle ambience. No BGM globally, no subtitles globally." |
| Counter-example | "Add nice background music." (Then also complaining the model added BGM you didn't want elsewhere.) |

### Negative prompts

| | |
|---|---|
| Writing points | Cover four directions: sound, subtitles, behaviour, and the failure mode specific to this scene. Repeat globally at the end. |
| Recommended | "No exaggerated crying, no fast cuts, no large body movements, no extra dialogue, no BGM, no premature dropping of tears." |
| Counter-example | "Nothing weird." |

### Timing

| | |
|---|---|
| Writing points | Explicit intervals or frame numbers before each beat, in chronological order. Also use timing to gate effects that must not appear early. |
| Recommended | "The ink-wash effect must only appear after 25 seconds, triggered by the 'click' sound — absolutely no premature appearance." |
| Counter-example | "Later on, the scene turns into ink wash." |

### References

| | |
|---|---|
| Writing points | Number by upload order, state the role of each, `@` them repeatedly, and lock what must stay identical. Split multiple viewpoints into separate images rather than one image containing several views. |
| Recommended | "@Image 1 wind traveller (protagonist), @Image 11 moon lake (scene), @Audio 1 theme melody. Strictly keep the protagonist's face and outfit consistent with @Image 1 throughout." |
| Counter-example | Uploading one contact sheet containing six views of the same character and hoping the model separates them. |

## Camera vocabulary

Every term below appears in the official guide. Speed qualifiers are the single highest-leverage
words in a Seedance prompt — an unmodified "the camera moves in" produces a very different clip from
"the camera pushes in extremely slowly".

### Shot sizes

| Term | When to use |
|---|---|
| Extreme wide / establishing | Opening a world, showing scale contrast between subject and environment |
| Wide / full shot | Full-body action, group blocking, dance |
| Medium shot | Dialogue, character introduction with some environment |
| Medium close-up | Emotional turns where the shoulders still read |
| Close-up | Micro-expression, a single prop, the emotional core |
| Extreme close-up | Eyes, tears, the final beat of an emotional arc |
| Macro close-up | Texture, dew, product detail, microscopic openings |
| Two-shot | Two characters in one frame at a relationship beat |

### Angles and perspectives

| Term | When to use |
|---|---|
| High angle / tilt-down | Making the subject small, surveying a space |
| Low angle / tilt-up | Oppression, heroism, scale of a towering object |
| Eye level | Neutral, realistic dialogue |
| Top-down / overhead | Graphic composition, table-top, flat-lay product |
| Aerial / drone | Landscape, city, epic reveal |
| First-person POV | Immersion — parkour, driving, horror |
| Over-the-shoulder | Directing attention toward what the character sees |
| Subjective POV | Making the viewer stand in for an unseen character |

### Movements

| Term | When to use | Typical speed qualifier |
|---|---|---|
| Dolly in / push in | Tightening emotional focus, product reveal | slowly, extremely slowly, at a constant speed, rapidly |
| Pull back / pull out | Revealing scale or context at the end | slowly, rapidly, significantly |
| Pan | Scanning a room or a row of subjects | slowly, smoothly, quickly |
| Tilt up / down | Revealing height, or dropping from sky to ground | slightly, slowly |
| Crane down | Descending from high angle to eye level in one move | smoothly and rapidly |
| 360° orbit / tracking | Action climax, showing a subject in the round | smooth, slow |
| Spiral circling | Descending reveal around a group | downward, slow |
| Aerial dive | Entering a scene from above with force | rapid |
| Handheld | Documentary realism, "breathing" intimacy | subtle, slight |
| Fixed camera | Atmosphere pieces, product display, split-screen comparison | (state "no shake, no zoom") |
| Zoom | Fast emphasis, transition into a detail | at extreme speed, infinitely |
| Whip pan | Violent connection between two shots | violently |
| Rack focus | Shifting attention between foreground and background | extreme, instantly |

Observed speed qualifiers, weakest to strongest: *slightly · subtle · slowly · extremely slowly ·
gradually · smoothly · steadily · at a constant speed · continuously · quickly · rapidly · at
extreme speed · suddenly · instantly · violently*. "Freeze" ends a movement.

### Optics and lighting

Shallow depth of field · natural depth of field · focus shift · bokeh light spots · Tyndall effect /
volumetric lighting / God rays · backlighting · side-backlighting (rim lighting) · HDR lighting ·
volumetric fog · soft natural light · high-contrast candlelight · warm-cold contrast · film grain.

### Transitions

Formula: **cut setting = [transition type guide] + [basic constraint] + [cut logic]**

Every transition in the guide repeats two constraints — *prohibit rigid cutting* and *prohibit
objects appearing out of thin air*. Include both every time; they are the model's most common
failure mode at a cut.

| Transition | What it is | When to use |
|---|---|---|
| Natural shot switching | A to B with no effect, but with breathing room and coordinated duration | Most ordinary narrative cuts |
| Fade in / fade out | Through black or white | Opening, closing, "the next day" |
| Stacking (dissolve) | A goes transparent as B emerges, 1–2 s overlap | Memory, dream, slow time passing |
| White flash / black flash | Instantaneous flash then cut | Beat sync, impact, tension |
| Erase (wipe) | B pushes A off from one direction | Retro style, obvious location change |
| Mask transition | Camera is blocked by an object, screen blacks, pulls out elsewhere | Space crossing, portal moments |
| Similar object transition | Last frame and first frame match in shape, outline or colour | Montage — moon to coffee cup |
| Action transition | Camera whips in A, whips in the same direction into B | Action, parkour, travel vlogs |
| Dynamic relay | Character jumps out of frame in A, falls into frame in B | Outfit changes, location hopping |
| Zoom in / out transition | Zoom into a detail until it becomes the whole of the next scene | Sci-fi, micro-to-macro, nested worlds |
| Ink painting transition | Ink drops into water, bleeds out, next scene emerges | Eastern aesthetics, historical, memory |

You may also hand the model a shortlist and let it choose: *"Please choose the most suitable one for
this film's style from [natural shot switching / mask transition / ink transition / similar object
transition]."*

## Templates

### Template A — text-only (T2V)

```
[One-line summary: subject + location + event + theme/style + special camera movement]

[Global settings]
Base environment & texture: [time] + [place] + [atmosphere] + [texture demand]
Visual style: [style family] + [depth of field] + [lighting method]
Camera language: [shot size/angle] + [movement + speed qualifier] + [one-shot or cuts]
Subject styling: [seven-dimension character formula] OR [quantifier + colour + shape + object
  noun + material/wear + iconic feature]
Core performance: [what the clip must actually sell]
Negative prompts: [sound] + [subtitles] + [behaviour] + [scene-specific collapse risk]

[Timestamp storyboard]
[00:00 - 00:0X] [Phase name]
  Action / physics: [scene] + [composition] + [detailed action, expression, dialogue, SFX]
  Camera subtext: [why this shot exists]
  [Transition instruction, if this beat cuts]
… repeat per slice …

[Global supplement]
Camera position + environment features + overall sound and atmosphere + lighting.
Restate global prohibitions.
```

### Template B — with references (I2V / multimodal)

```
[Asset manifest]
@Image 1 = [role: character / scene / prop], @Image 2 = [role], @Video 1 = [role: camera
movement / action / creative form], @Audio 1 = [role: timbre / BGM]

[Lock statement]
Based on the uploaded [asset types], strictly keep [X] consistent, strictly lock [Y].

[One-line summary: subject + location + event + theme/style + special camera movement]

[Timestamp storyboard]
[00:00 - 00:0X] [Phase name]
  Action / physics: … re-@ the relevant asset inside the beat …
  Camera subtext: …
… repeat per slice …

[Global supplement]
Camera position + environment + overall sound and atmosphere + lighting.
Character identities must not mix; counts must be exact. Restate global prohibitions.
```

### Template C — video extension

```
Reference the content of @Video 1, extend the video by [N] s [backwards / to continue the story].
[Continuous:] Require natural extension, smooth action connection, hard cuts prohibited, objects
appearing out of thin air prohibited.
[With a cut:] Require a "[transition name]" at the cut (hard cuts prohibited, objects appearing out
of thin air prohibited). Shot A shows [X], then transitions naturally to Shot B where [Y]. Require
the scene to switch naturally, changing from [close-up] to [medium shot].
[New content for the extended segment only.]
```

Set the generation length to the **new segment's** duration, not the total.

### Template D — edit

```
[Annotation tool and orientation — Edit with marks only: "inside the red box", "the area the red
arrow points to", "left of the red line"]
+ [Specific object to modify] + [Action and change: replace with / add / remove]
+ [Effective time range: whole clip / seconds 5–8 / gradually from second 3]
```

### Template E — white model (Clay Renderer)

```
Coarse: [Reference statement: reference the {camera movement | action | movement line | lighting |
character positioning | SFX | rhythm} of @Video 1] + [Correspondence mapping: replace the
{colour/shape} model with {character} in @Image X] + [Plot details in chronological order]
+ [Scene processing] + [Overall conclusion: style, quality, consistency, audio]

Fine: [Render command] + [Segmented rendering description per time range] + [Scene processing]
+ [Overall convergence]
```

For coarse models with limbs or wings, write the complete limb action sequence or the result goes
stiff — the guide's own advice is to avoid uploading limbed or winged models at all. For fine models,
strip trajectory lines, coordinate lines and camera cones from the reference video first.

### Template F — seamless join of two clips

```
Seamlessly connect [@Video 1] and [@Video 2], but do not modify [@Video 1] and [@Video 2].
[Bridging object and how it carries across.] Keep [its position, size, direction] consistent at the
join. [How the environment morphs.] No black screens, frame skipping, hard cuts, flickering, text,
logos, or subtitles.
```

## Worked examples

All six are condensed from cases in the official guide. The breakdowns explain what makes each work,
so the pattern transfers.

### 1. Nature documentary / landscape (basic formula, references)

> Realistic nature documentary style, cinematic realistic lighting. In morning mist within a vast
> wetland reed bed @Image 1, an elegant red-crowned crane spreads its wings and dances. @Image 2 —
> snow-white feathers, bright red crown, slender upright posture. Low-angle medium shot, slight
> handheld feel, crane centred throughout.
> **0s-3s:** Standing in shallow water, it slowly unfolds its wings; the airflow ripples the surface;
> sunlight slants in from the horizon, piercing the mist into a Tyndall effect.
> **3s-8s:** It leaps, feet tapping the water, neck tilting back, then lands and calls out. Camera
> follows the jump. Natural depth of field, foreground reeds blurred, crane in sharp focus. Natural
> sound: water, wing beats, the call. Peaceful, ethereal.

**Why it works:** the style sentence lands before any detail, so everything after inherits it. Each
`@` asset gets an explicit job — scene versus subject. The closing paragraph re-states camera, depth
of field, sound and mood, which is exactly the global supplement the formula asks for.

### 2. Emotional character piece, 29 s one-shot (30-second formula)

> **[Global settings]** Early morning by the river, a blurred boat behind, quiet and restrained.
> Cinematic, shallow depth of field, soft natural light. Hold a close-up of the woman throughout,
> imitating the subjective POV of the man opposite her; subtle handheld breathing effect; one
> continuous shot, no fast cuts.
> **[Character styling]** All seven dimensions — 22-year-old East Asian woman with a classical
> cinematic face; cool-toned fair skin retaining realistic fine pores; slender slightly moist eyes,
> straight nose bridge, soft jawline; gaze gentle and focused, revealing deep attachment; jet-black
> hair in a classical low bun with loose strands in the breeze; minimalist white cross-collar silk
> dress; slender narrow shoulders, graceful classical aura.
> **[Core performance]** Restrained — shifting gaze, breathing, trembling lips, throat swallowing,
> one tear sliding naturally.
> **[Negative]** No exaggerated crying, no fast cuts, no large body movements, no extra dialogue,
> no BGM, no premature tears.
> **[Storyboard]** 0-3s Questioning · 3-10s Resignation · 11-17s Remembering · 18-23s Regret ·
> 24-29s Letting go — each with physical directives plus an emotional analysis line.

**Why it works:** the camera is locked once, globally, so 29 seconds cannot drift into coverage it
was never asked for. The negatives are scene-specific — "no premature tears" matters only because the
arc depends on tears arriving in stage four. Each beat carries an emotional analysis line, the
guide's mechanism for telling the model the intent behind a physical instruction.

### 3. Landscape one-shot with no character (30-second formula, subject-free)

> **[Global setting]** Polar glaciers and deep ocean; National Geographic level physical realism;
> meltwater refraction and underwater dappling must obey real optics. Epic landscape style, cool
> palette shifting icy blue to abyssal blue. Globally smooth, slow, epic one-shot forward drone push,
> absolutely no hard cuts. **Subject:** no specific character — the performance is the environment,
> the time-lapse light, and the seamless above-to-below-water transition.
> **[Negative]** No humans or vehicles except the shipwreck; no flickering or tearing at the water
> transition; strictly remove subtitles and default BGM.
> **[Storyboard]** 00:00-00:09 glacier cruise · 00:10-00:15 time-lapse sky · 00:16-00:21 dive through
> the surface · 00:22-00:30 underwater ruins, freeze on the figurehead.

**Why it works:** with no character, the "core performance" slot is reassigned to the environment
rather than left empty — the block keeps its shape. The riskiest moment, the water-penetration
transition, gets its own beat *and* its own negative clause. Protect the shot you already know is
the hard one.

### 4. Cut-driven narrative with transitions (30-second formula, montage)

> Late-night bamboo-forest tavern, top-tier cel-shaded wuxia anime, ink-wash rendered edges, cold
> moonlight against warm candlelight. Razor-sharp montage with multiple physical transitions.
> **[Negative]** No greasy 3D feel, no sluggish combat, no limb clipping, no subtitles. *Emphasis:
> the ink-wash effect must only appear after 25 seconds, triggered by the "click" of the sword
> sheathing — absolutely no premature appearance. The wine bowl must not appear until the full moon
> has completely faded out.*
> **[Storyboard]** 00:00-00:04 match cut, moon crossfades into an identically sized wine bowl ·
> 00:05-00:10 zoom into the pupil, scene expands from inside it · 00:11-00:18 pull out then whip pan
> into the clash · 00:19-00:24 a bamboo leaf masks the lens, revealing the aftermath · 00:25-00:30
> ink-wash bleed, freeze.

**Why it works:** every cut names its transition type instead of trusting the model to invent one.
The negative block does something worth copying — it gates two effects *in time*, which is the fix
for a signature visual firing in second three instead of second twenty-five.

### 5. Multilingual product ad (localisation)

> Reference @Image 1–@Image 6 to generate a vertical premium cocktail commercial. Spring-fresh,
> light-luxury, cream-green background, soft studio lighting, commercial ad texture. Six cocktails
> shown one by one: ice, condensation, salted rims, lime, mint — highlighting liquid layers and
> transparency. Cinematic camera: slow push-ins, macro close-ups, slight orbiting, silky transitions.
> **All text in the final film must be entirely in Korean** — main title, product names, per-product
> slogans, subtitles, ending copy, and all on-screen copy. Chinese, English, Spanish or any
> non-Korean text is prohibited. Names and slogans must be natural premium Korean suitable for
> fashion ad typography.

**Why it works:** the localisation instruction enumerates every place text can appear rather than
saying "in Korean", and pairs the requirement with an explicit prohibition on other scripts. It asks
for *natural* Korean copy rather than translated copy, which is what stops the output reading like a
subtitle track. Write dialogue lines verbatim in the target language for the same reason.

### 6. Chained video extension

> **Pass 1 (base):** The muscular warrior in @Image 1 walks alone through dense primeval forest,
> steady steps, alert expression, camera pans forward following him, sunlight mottled through leaves.
> **Pass 2 (+5 s, continuous):** Reference @Video 1, extend backwards by 5 s. Require natural
> extension, smooth action connection, hard cuts prohibited, objects appearing out of thin air
> prohibited. He notices something, stops, eyes sharpen, adopts a defensive posture.
> **Pass 3 (+10 s, with a cut):** Reference @Video 1, extend by 10 s. Require a "mask transition" at
> the cut (hard cuts prohibited, objects out of thin air prohibited). Shot A: the warrior defending
> in close-up; a leaf drifts toward the lens and covers it, screen goes dark; the camera pulls back
> through the leaf to reveal @Image 2, a young ranger raising his bow. Naturally switch from the
> warrior's close-up to the ranger's medium shot.

**Why it works:** each pass carries only the new content, which is what the extension feature
expects. Pass 2 uses the continuous constraint set; pass 3 switches to the transition formula and
names the shot-size change, so the cut has a stated logic. The character reference is re-`@`'d in
every pass so identity survives the chain.

## Common mistakes

### From the guide

- **Trusting the model to stay clean.** Subtitles and BGM appear unless you write "pure video, no
  subtitles, no background music". Say it globally and repeat it at the end.
- **Omitting the two cut constraints.** Every transition in the guide repeats *prohibit rigid
  cutting* and *prohibit objects appearing out of thin air*. Leaving them out is the top cause of
  jarring cuts and things materialising mid-frame.
- **A generic negative list.** Prohibitions should come from four directions — sound, subtitles,
  behaviour, and this scene's specific collapse risk. "No weird stuff" prevents nothing.
- **Vague subjects.** Flat white skin, twin faces, and plastic sheen are what the seven-dimension
  character formula exists to prevent.
- **Overloading references.** Past 5 subjects, or past 8 subject images, stability drops and you are
  re-rolling. Reference clips work best at 5–10 s; edits work best on footage under 20 s.
- **One image containing several viewpoints.** Split viewpoints across separate images — multi-image
  multi-view beats single-image multi-view.
- **Choosing the wrong extension length.** Request the new segment's duration, not the total.
- **Uploading limbed or winged white models** without writing the complete limb action sequence, or
  leaving trajectory lines, coordinate lines and camera cones in a fine-grained white-model reference.
- **Effects with no time gate.** If a signature visual must not appear early, say so with a timestamp
  and a trigger.

### Inferred [inferred]

- **Contradicting yourself across blocks.** If global settings say "one continuous shot" and a beat
  says "cut to", the model has to pick one. Resolve it before sending.
- **Stacking quality keywords instead of directing.** "8K masterpiece ultra detailed" occupies space
  the guide's formula would have filled with subject, location, and event.
- **Writing negatives for things you never established.** "No red car" only helps if a car could
  plausibly appear; noise dilutes the negatives that matter.
- **Reusing a 5-second prompt at 30 seconds.** Without a timestamp storyboard the model paces the
  whole idea into the opening seconds.
- **Describing a camera route no single camera could physically travel** in a shot declared as
  one-shot.

## Self-check

Run every line before sending.

- [ ] Mode and duration are inside the platform limits, and the formula matches the mode
- [ ] Every uploaded asset is numbered, given a role, and re-`@`'d where it matters
- [ ] Anything that must not drift has an explicit lock sentence
- [ ] There is a one-line summary containing subject + location + event + style + special camera move
- [ ] For 30 s or longer: a global settings block covering environment, style, camera, subject,
      core performance, and negatives
- [ ] Every beat carries a timestamp or frame range, in chronological order
- [ ] Every camera instruction has a shot size or angle **and** a speed qualifier
- [ ] Every cut names its transition type and repeats both cut constraints
- [ ] Negatives cover sound, subtitles, behaviour, and this scene's specific collapse risk
- [ ] Subtitles and BGM are addressed explicitly, globally, at least once
- [ ] Dialogue is written verbatim in the target language, with tone direction
- [ ] The prompt closes with a global supplement re-stating camera, environment, sound, and lighting
- [ ] No block contradicts another (one-shot versus cuts, character described two different ways)
- [ ] For extensions: the requested length is the new segment only

## Extended suggestions

The guide does not cover these. Everything here is **[non-doc]** — treat it as working practice, not
official rule.

- **Three points where common belief contradicts the guide.** The guide states output resolution is
  480p/720p; 4K appears only as an *input* reference-image spec. The guide has no "six elements"
  framework — its structure is the four-part formula. And the guide encourages restating what is
  already visible in a reference image and `@`-ing it repeatedly, which is the opposite of the usual
  "don't describe what's in the image" advice for image-to-video models.
- **Commercial intent stated up front.** Naming the deliverable ("a 15-second conversion-oriented
  in-feed ad") before the visual description is not in the guide, but it costs one line and gives the
  model a frame for pacing decisions.
- **No prompt length guidance exists.** The guide's own examples run from one sentence to well over a
  thousand words. Longer helps at 30 s and above; there is no stated ceiling.
- **No negative-prompt syntax.** No weights, no `--no` flags — plain natural language only.
- **No seed or reproducibility control.** The guide calls variance "drawing cards" / gacha and offers
  no way to pin a result. Plan on re-rolls for anything near a stability limit.
- **A/B variant workflow.** Keep the global settings block fixed and vary one element at a time; the
  guide's own diagnostic logic (each formula slot answers a different production question) makes this
  the natural way to isolate what went wrong.
