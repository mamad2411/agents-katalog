---
name: seedance-prompting
description: "Seedance 2 Prompt Generator: Transform any creative brief into perfect Seedance 2.0 prompts following the official 6-layer architecture (Subject → Action → Environment → Camera → Style → Constraints). Supports multi-shot generation with brackets, character lock via reference, native audio cues, and positive constraints. Use this skill whenever Tim needs Seedance 2 prompts — for hooks, walkthroughs, action shots, product shots, character scenes, or multi-shot sequences. Triggers on: 'seedance prompt', 'prompt seedance', 'video prompt', 'seedance 2', 'multi shot prompt', 'fais un prompt video', 'genere un prompt seedance', 'cinematic video prompt', 'prompt pour seedance', 'openart video prompt'."
---

# Seedance 2 Prompting — Multi-Shot AI Director Prompt Generator

Transform vague video ideas into precise, structured Seedance 2 prompts that produce cinema-quality multi-shot scenes. This skill exists because plain prompts make Seedance generate chaos — the 6-layer architecture below makes it generate films.

## Context

Read CLAUDE.md for Tim's brand DNA and API keys. Tim's aesthetic is **cinema-quality, editorial, hyperrealistic** — every Seedance prompt should default to this unless he specifies otherwise.

For deeper reference, see `references/seedance-rules.md` for the full ByteDance prompting specification, pitfalls, audio cue dictionary, and tested examples.

---

## Tim's Visual DNA (baked into every Seedance prompt)

These defaults apply unless Tim overrides them. They encode Tim's cinematic creative-director aesthetic:

| Element | Tim's Default | Why |
|---|---|---|
| **Style** | Editorial fashion + action sport, cinematic 35mm film look | Tim's brand = cinema-quality AI |
| **Lighting** | Golden hour rim light, dramatic directional, motivated | Lighting is the #1 Seedance quality lever |
| **Color grading** | Warm golden grading or teal/orange Hollywood | Consistent across reels |
| **Camera** | ONE primary instruction per shot (handheld, tracking, dolly in, locked-off, aerial) | Multiple = jitter |
| **Format** | 9:16 vertical for reels | Instagram |
| **Constraints** | Sharp focus throughout, natural anatomy, identity locked | Quality lock |
| **Length** | 60-100 words optimal (max 200) | Sweet spot |

---

## The 6-Layer Seedance Architecture (Official ByteDance)

Every prompt MUST follow this order. Skip a layer and Seedance fills the gap with chaos.

### Layer 1 — Subject
Specific visual features. Age, build, outfit, distinguishing details.
- ❌ "a man" → ✅ "a young athletic male traceur in beige cargo pants and white oversized t-shirt, sharp jawline, dark messy hair"

### Layer 2 — Action
Concrete verbs with physics awareness.
- ❌ "running" → ✅ "sprints across a Parisian zinc rooftop, then leaps over a gap between two Haussmann buildings in dramatic slow motion, body fully extended, arms stretched forward"

### Layer 3 — Environment
Location plus lighting mood. Lighting = #1 quality lever.
- ❌ "city" → ✅ "golden hour late afternoon Paris rooftops, distant Eiffel Tower glowing in warm haze, sun creating sharp rim light through his silhouette"

### Layer 4 — Camera (ONE instruction)
Pick ONE primary movement. Mixing causes jitter.
- Options: `dolly in`, `dolly out`, `tracking shot`, `handheld`, `locked-off`, `aerial drone`, `orbit`, `pan left/right`
- Always at a specific level: "at chest level", "at waist level", "low angle", "bird's eye"

### Layer 5 — Style
Visual references with film vocabulary.
- ❌ "cinematic" alone → ✅ "editorial fashion action sport, cinematic 35mm film look, warm golden grading"

### Layer 6 — Constraints (positive only)
Seedance does NOT accept negative prompts. Replace negatives with positives:
- ❌ "no blur" → ✅ "sharp focus throughout"
- ❌ "no morphing" → ✅ "identity stays locked across the entire shot"
- ❌ "no distortion" → ✅ "natural anatomy with properly formed limbs"

---

## Master Template

```
[SUBJECT with specific visual features]. [ACTION with concrete verbs and physics]. [ENVIRONMENT with location and lighting mood]. [CAMERA — ONE primary instruction at specific level]. [VOICE or audio cue if speaking]. [STYLE with visual references]. [CONSTRAINTS as positive statements].
```

---

## Audio Prompting (Killer Feature)

Seedance 2 has a native audio engine. Drop these directly in the prompt:

| Type | Examples |
|---|---|
| **Voice emotion** | "speaks with explosive enthusiastic attitude", "voice is loud, charged, electric, like she just discovered something insane", "calm grounded voice" |
| **Sound effects** | "wind whistling loudly past the camera", "footsteps echoing on metal", "waves crashing violently" |
| **Music mood** | "tense orchestral score", "upbeat electronic beat", "somber piano notes" |
| **Acoustics** | "reverb in large space", "muffled underwater", "crisp close-mic", "echo in cathedral" |

---

## Multi-Shot Generation (Killer Feature #2)

Seedance 2 is the ONLY AI video model that generates multiple cut shots in a single prompt. Use brackets with shot timing:

```
[Shot 1, 3 seconds: Wide tracking shot of the same male traceur sprinting across a Parisian zinc rooftop toward the camera, golden hour rim light, handheld camera at chest level following him from behind.]

[Shot 2, 3 seconds: Slow motion mid-air shot of him leaping between two Haussmann buildings, body fully extended, sun behind him creating a sharp silhouette, locked-off side angle camera.]

[Shot 3, 2 seconds: Tight close-up of him landing on the opposite rooftop, hands gripping the zinc edge, intense fast dolly in pushing toward his determined eyes, says "And here's everything you need to master it" with explosive charged voice.]

Editorial action sport, cinematic 35mm film, warm golden grading. Identity stays locked on reference face across all three shots, character consistency maintained, sharp focus throughout.
```

**Multi-shot rules:**
- Define the camera move INSIDE each bracket (each shot has its own grammar)
- Always end with a global STYLE line and a global CONSTRAINTS line OUTSIDE the brackets
- Reference the character with "the same [SUBJECT]" or "Same traceur" in shots 2+
- Keep shot timing realistic: 1.5s-3s per shot, max 5 shots per generation
- Total length ~6-15 seconds across all shots

---

## Reference System (Character Lock)

Seedance 2 on OpenArt accepts:
- **Up to 9 reference images** (character, mood, location, palette, lighting)
- **Up to 3 reference videos** (camera moves, energy, pacing)
- **Up to 3 audio files** (voice tone, music, sound design)

When the user uploads a face reference, ALWAYS add to the prompt:
- "identity stays locked on reference face"
- "character consistency maintained on the reference face"
- Use "the same [subject description]" in subsequent shots

---

## Pitfalls — Words to AVOID

| ❌ DON'T | ✅ DO |
|---|---|
| "fast" alone | "fast but controlled", "rapid with smooth easing" |
| "cinematic" alone | "cinematic 35mm film look with warm golden grading" |
| "epic", "amazing", "beautiful" | concrete visual descriptors |
| "lots of movement" | one specific motion |
| Negative prompts | positive constraints |
| Mixed camera moves | ONE primary camera instruction |
| Vague subject | specific outfit, age, features |

---

## Workflow

### Step 1 — Understand the brief

Tim gives you either:
- A **vague idea**: "un prompt pour le mec qui court sur les toits"
- A **shot deck entry**: "Shot 3 (3s): close-up vault over chimney"
- A **multi-shot scene**: "le hook avec sprint + jump + catch"

Extract: subject, action sequence, environment, mood, audio cues if any, single shot or multi-shot.

### Step 2 — Apply the 6-layer architecture

Build the prompt in the exact order: Subject → Action → Environment → Camera → Style → Constraints.

### Step 3 — Add audio if speaking

If the subject talks, add the voice emotion line + a sound effect (wind, footsteps, ambient).

### Step 4 — Multi-shot or single shot?

- Single action moment → one prompt
- Sequence of actions (3+ different camera moves or scene beats) → multi-shot brackets

### Step 5 — Lock the character

If a reference face is uploaded, add "identity stays locked on reference face" as the final constraint.

### Step 6 — Length check

- Single shot: 60-100 words optimal
- Multi-shot (3 shots): 150-200 words OK (each shot ~50-70 words)
- NEVER exceed 250 words total

---

## Tested Examples

### Single shot — Hook with voice + dolly in
```
A young athletic male traceur in beige cargo pants and white oversized t-shirt lands hard on a Parisian zinc rooftop, hands violently gripping the edge, dust scattering, looks straight into the camera with intense determined eyes and says "And here's everything you need to master it" with an explosive charged voice like he just discovered something insane. Golden hour sun creates a sharp rim light on his face. Distant Eiffel Tower silhouette glows in golden hour haze. Intense fast dolly in pushing aggressively toward his face during the line, ending on a tight close-up of his eyes. Wind whistles loudly past the camera. Editorial action sport, cinematic 35mm film, warm golden grading. Sharp focus throughout, identity stays locked on reference face.
```

### Multi-shot — Full hook scene
```
[Shot 1, 3 seconds: A young athletic male traceur in cargo pants and white tee sprints across a Parisian zinc rooftop toward the camera, intense focused expression. Handheld camera tracking him at chest level. Wind whistles past.]

[Shot 2, 3 seconds: Same traceur leaps between two Haussmann buildings in dramatic slow motion, body fully extended, golden hour sun behind him creating sharp silhouette. Locked-off side angle camera.]

[Shot 3, 2 seconds: Tight close-up, he lands and grips the zinc edge of the opposite rooftop, looks into the camera and says "And here's everything you need to master it" with explosive charged voice. Intense fast dolly in pushing toward his determined eyes.]

Editorial fashion action sport, cinematic 35mm film, warm golden grading. Distant Eiffel Tower in haze. Identity stays locked on reference face across all shots, sharp focus throughout, natural anatomy.
```

### Single shot — Action close-up
```
Tight close-up of a young male traceur placing both hands firmly on top of an old Parisian brick chimney, muscles tensing in his forearms, fingers gripping the bricks as he launches his legs sideways over the top in one fluid motion. Dust and loose mortar scatter in the air. Golden hour warm light on his knuckles and face. Handheld camera moving with him at hand level. Grunt of effort audible. Editorial action sport, cinematic 35mm, warm golden grading. Sharp focus throughout, natural anatomy, identity locked on reference face.
```

---

## Output Format

When generating prompts, ALWAYS return:

1. **The prompt itself** in a code block (plain text, no markdown formatting inside)
2. **Word count** at the bottom
3. **Camera instruction** flagged (so Tim can see the single instruction)
4. **Audio cues** flagged if any
5. **Reference recommendation** (which images/videos/audio to upload alongside)

Example output:
```
PROMPT (94 words):

[the actual prompt here]

Camera: handheld tracking at chest level
Audio: wind whistles past, voice with explosive charged attitude
Recommended references:
- 1 face image (close-up portrait, character lock)
- 1 environment image (Paris rooftop golden hour)
- 1 audio file (Tim's voiceover from voiceover-final.wav)
```

---

## Self-Improving Loop

Before generating Seedance prompts, check `logs/last-run.md` for known issues from the previous session.
After generating, overwrite `logs/last-run.md` with:
- Date, task, result
- What worked / what didn't
- Tim's feedback if any
- Known issues discovered

NEVER accumulate history — overwrite each time.
