---
name: minimax-worldbuilder
description: "Compose MiniMax-H3 video-with-native-audio prompts in H3's mandatory structured format — full-reference (Ref2VA) and text-to-video (T2VA) only. Use whenever the target model is MiniMax-H3: the user says MiniMax, MiniMax-H3, H3, ref2va / r2v / t2v, names a minimax_h3 checkpoint, or names the MiniMaxH3ReferenceToVideo / EmptyMiniMaxH3LatentAV / MiniMaxH3SigmaShift ComfyUI nodes. Also use when the request needs H3's own vocabulary — reference tags <Subject N> / <Picture N> / <Video N> / <Audio N>, subject_definitions, retention_analysis, detailed_description, integrated_multimodal_description, overall_soundscape, non_diegetic_music, [Shot N] cut timestamps, (S1) speaker IDs, <d> dialogue blocks. H3 prompts are not free prose: fixed section names in a fixed order, fixed camera-motion and retention enums, and a native-audio pass that goes silent if the sound sections are thin — so use this skill instead of a generic prompt skill any time H3 is the target model. NOT for other generative models (Flux, SDXL, Qwen Image, WAN, Kling, Veo, Sora, Runway, Seedance — use cinematic-prompts), NOT for still images (use cinematic-still-director), and NOT for H3's I2VA / FL2VA / L2VA keyframe paths, which this skill deliberately does not cover."
---

# MiniMax-H3 Worldbuilder — Ref2VA & T2VA Director

H3 is omni-modal: one forward pass produces **video and native 32 kHz stereo audio together**. Sound is not a garnish — a thin soundscape yields a near-silent clip. And H3's prompt format is a **structured intermediate representation**, not prose. Named sections, fixed order, fixed enum vocabularies. A paraphrased camera move or an invented retention marker is a defect, not a style choice.

This skill is the director's apparatus on top of that IR: it reads the user's references, picks a look, extracts an inventory, and emits a prompt that conforms to MiniMax's own guides exactly.

## Scope

**In scope — two paths, and only two:**

| Path | When | Prompt format |
|---|---|---|
| **Ref2VA** (full-reference) | Any reference images / videos / audio are supplied | Six named sections |
| **T2VA** (text-to-video) | No reference assets at all | Three named fields |

**Out of scope:** I2VA, FL2VA, L2VA. Those paths require a first-line image-alignment instruction that this skill does not specify. If the user is running one of those checkpoints/endpoints, say plainly that this skill covers Ref2VA and T2VA only and point them at MiniMax's base prompt-writing guide — **do not improvise an alignment line.**

> **"Use this image as the first frame" — which path?** Decide by the checkpoint, not by the wording of the request. Running the **i2va / fl2va / l2va** checkpoint → out of scope, stop and say so. Running the **ref2va** checkpoint → in scope: full-reference mode has its own way to anchor a frame — a standalone `<Picture N>` plus the `keyframe completion` task type in `summary`, and **no** alignment instruction line. If you don't know which checkpoint they're on, ask before writing anything.
>
> **Unverified:** the sources do not say how strictly the ref2va checkpoint honours a frame anchor compared to the dedicated keyframe checkpoints. Say so if the user is leaning on exact first-frame fidelity.

---

## FIXED vs HOUSE — read this before anything else

Two kinds of content live in this skill and they are not interchangeable:

- **FIXED** — comes from MiniMax's guides. Section names, tag names, enum values, timestamp format, structural rules. **Never paraphrase, never extend, never invent a new member.** If what you want isn't in a FIXED list, pick the nearest member that is.
- **HOUSE** — this skill's directorial judgment (look modes, shot-count guidance, word-count guidance for T2VA, pacing). Free English text. Adjust it freely to serve the scene.

Every table below is labelled. When HOUSE guidance and a FIXED rule appear to conflict, the FIXED rule wins and the HOUSE guidance bends.

---

## SESSION OPENER — REFERENCE & CHARACTER GATE

The first time the user asks for an H3 prompt in a session, ask once:

> "Any recurring characters or locked references in this batch? If so — do you already have the reference assets, or do we build the look from text?"

**Branch:**

- **Has references →** get them, then run the extraction pass below and **mirror back the locked spec in plain language for confirmation** before composing. This is the Ref2VA path.
- **No references / inventing from text →** T2VA path. Skip straight to the pre-prompt confirmation.
- **Wants recurring identity but has no references →** say so directly: T2VA cannot hold identity across separate generations. Recommend generating or sourcing 3–4 varied stills of the character first, then switching to Ref2VA.

Ask once per session. Carry the answer.

**Reference asset limits (FIXED):** ≤9 images, ≤3 video clips (each 2–15 s), ≤3 audio clips, **≤12 files total**. Audio cannot be the sole input. **3–4 varied shots of a character hold identity far better than one** — say this out loud when the user offers a single image.

**Numbering (FIXED, load-bearing):** `<Picture N>`, `<Video N>`, `<Audio N>` are numbered **in the order the assets are connected/supplied**, and `<Video N>` / `<Audio N>` are numbered independently of each other — the same source clip can be `<Video 1>` and `<Audio 2>`. If you don't know the connection order, ask. A prompt whose numbers don't match the wiring references the wrong asset.

---

## READING REFERENCES — INVENTORY EXTRACTION (run before composing)

Extract everything visible by **visual description only**, then compose. Never invent detail that isn't in the reference or in the user's text.

**Per character:** hair (colour with nuance, length, texture, parting, styling, accessories) · skin and complexion, visible freckles/marks · makeup register if visible · every garment top to bottom (fabric, colour, fit, neckline, sleeve, hem, layering, structural details) · jewellery and accessories · visible piercings, tattoos, nail colour · build and posture · expression register.

**Per environment:** interior/exterior, architecture, materials, scale · time of day, weather, light direction and colour temperature · set dressing (every object that shapes the world) · dominant palette and contrast structure.

**Per audio reference:** what role it plays — voice timbre, delivery, music style, ambience, sound-effect texture, beat, or a signal to be copied outright. This decides its retention marker later.

**Naming rule.** Do not use proper names for characters in the prompt. Ref2VA identifies subjects by `<Subject N>` plus visual description; T2VA identifies them by visual description alone. No example in either guide names a character.

**Age and gender are required, not forbidden.** The base guide explicitly asks for character type, age, gender, pitch, timbre, speaking rate and accent when a speaker first appears — write them. (This reverses the age-blind convention used for other platforms.) The one hard floor: never write minors into sexual, suggestive, or violent-victim content.

**Brands and on-screen text.** Real signage that is genuinely visible in the scene goes in English double quotes, verbatim (see the on-screen text rule). Otherwise describe products generically. If the user is sending to MiniMax's hosted API rather than running locally, keep brand marks out — hosted moderation is stricter than a local checkpoint.

**No-invention rule.** If a scene needs a detail the reference doesn't carry (a new outfit, a location not shown), ask, or state in your reply that you composed it from the user's text rather than from the reference.

---

## LOOK MODES (HOUSE) — the director's register

H3 has no camera-spec block. The look is carried by (a) the style opening, (b) the enum camera moves you choose, (c) texture and palette words inside the shot descriptions, and (d) the two sound sections. Never append a trailing gear/spec block — every clause in an H3 prompt must correspond to something visible or audible.

Pick one mode. It seeds the style opening and biases the camera choices; it is not a constraint.

| Mode | Use when | Named style to open with | Camera moves it favours (FIXED enums) | Texture & palette language | Sound posture |
|---|---|---|---|---|---|
| **M1 Narrative** | Lived-in real-world drama — streets, kitchens, cars, bars, interiors | `Live-action, cinematic` | `Push In` / `Truck Left` / `Truck Right` / `Tracking Shot`, with small amplitude at slow speed; `Shake Slightly` for unease | Practical light sources named, visible grain, warm highlights against cool shadows, shadows that hold detail | Dense room tone + physical action sound; score sparse or `N/A` |
| **M2 Studio / Editorial** | Void backdrops, fashion film, editorial portrait, crafted rather than photographed | `Cinematic` | `Static Shot`; `Push In with small amplitude at slow speed` | Controlled seamless background, specular bloom on chrome and fabric, saturated or pastel palette, blacks retaining warmth | Very quiet soundscape — fabric, breath, footfall on cyc; score carries the piece |
| **M3 Action / Combat** | Combat, chase, stunts, destruction, mech and creature work | `Live-action, cinematic` | `Shake Strongly`, `Tracking Shot at fast speed`, `Push In with large amplitude at fast speed`, `Arc Shot`, `POV` | Airborne dust and debris, atmospheric haze, impact deformation, sweat and dirt on skin | Impacts, mechanism sounds, ragged breath; score percussive |
| **M4 Performance / Concert** | Stage, arena, festival pit, crowd and stage lighting | `Live-action, cinematic` | `Arc Shot`, `Tracking Shot`, `Shake Slightly/Strongly`, `Tilt Up with large amplitude`; more cuts than other modes | Volumetric haze in every beam, stage-lighting colour cast, sweat sheen, damp fabric, lens bloom on sources | Crowd, stage mechanics, mic handling; **diegetic performed music lives in the description, never in `non_diegetic_music`** |
| **M5 Atmospheric / Empty** | Landscapes, abandoned places, weather plates, no-humans establishing work | `Cinematic` or `vintage film` | `Static Shot`; `Push In` / `Pull Out` with small amplitude at slow speed | Weathered materials, dust in air, strong negative space, palette named explicitly | Ambience-forward, wide and continuous; score sustained or `N/A` |

Other named styles the guides list and you may open with: `2D-animated`, `3D CG`, `claymation`, `watercolor`. (FIXED list — these plus `Cinematic`, `live-action`, `vintage film`.) You may add free-text look language after the named style.

---

## DURATION AND SHOT TIMING (decide this FIRST)

Cut timestamps must fall inside the duration, so the duration is chosen before a single shot is written.

**Model spec (FIXED):** 4–15 s, 24 fps, 32 kHz stereo. Aspect ratios 21:9, 16:9, 4:3, 1:1, 3:4, 9:16. Open weights are **768p only** — 2K needs the hosted H3-Regenerate-2K API.

**Local ComfyUI frame grid (FIXED):** `length = 17k + 5`, trained range **124–362 frames**.

| frames | seconds | frames | seconds | frames | seconds |
|---|---|---|---|---|---|
| 124 | 5.167 | 209 | 8.708 | 294 | 12.250 |
| 141 | 5.875 | 226 | 9.417 | 311 | 12.958 |
| 158 | 6.583 | 243 | 10.125 | 328 | 13.667 |
| 175 | 7.292 | 260 | 10.833 | 345 | 14.375 |
| 192 | **8.000** | 277 | 11.542 | 362 | 15.083 |

**192 frames / 8.000 s is the only whole-second duration in the trained range.** Every other length lands on a fraction — write the real number, don't round it into the prompt's timestamps.

**Which range wins.** The two ranges are not in conflict, they describe different things: 4–15 s is the model's published output range, 124–362 frames is the trained frame range of the local ComfyUI nodes. **When the target is local ComfyUI, pick a length from the table** — the shortest usable clip is 124 frames ≈ 5.167 s, so a request for "4 seconds" gets rounded up to 124 frames and the user gets told why. When the target is the hosted API, 4 s is available and durations are specified in seconds.

**Shot-count guidance (HOUSE):** ≤7 s → 1–2 shots. 8–11 s → 2–3 shots. 12–15 s → 3–4 shots. Land the last cut at least ~1.5 s before the end so the closing shot has room to play. Dialogue runs roughly 2.5–3 English words per second — count the words before you promise a line will fit.

---

## FIXED VOCABULARIES

Everything in this section is an enum. Pick a member. Never paraphrase, never invent.

The only angle-bracket tags that may ever appear in an H3 prompt are `<Subject N>`, `<Picture N>`, `<Video N>`, `<Audio N>`, `<d>…</d>`, `<scenetrans>` and `<cutoff>`. Anything written as `{like this}` in this skill is a placeholder for you to replace — never copy braces into a prompt, and never invent a new angle-bracket tag.

### Camera motion

Motion type: `Zoom In` · `Zoom Out` · `Push In` · `Pull Out` · `Pan Left` · `Pan Right` · `Truck Left` · `Truck Right` · `Tilt Up` · `Tilt Down` · `Pedestal Up` · `Pedestal Down` · `Arc Shot` · `Tracking Shot` · `Static Shot` · `Shake Slightly` · `Shake Strongly` · `POV` · `Roll Clockwise` · `Roll Counterclockwise`

Amplitude: `with small amplitude` · `with large amplitude` — medium is expressed by omitting amplitude.
Speed: `at slow speed` · `at fast speed` — normal is expressed by omitting speed.

**Order is fixed: motion type, then amplitude, then speed** — "pushes in with small amplitude at slow speed", never "at slow speed with small amplitude". Add amplitude and speed only when they carry meaning; omitting one is how you say "medium" or "normal". Write the move as **natural English action inside the shot**, conjugated to fit the sentence — never stacked as trailing labels:

```
The camera pushes in with small amplitude at slow speed toward the folded letter in her hands.
The camera pans right with large amplitude at fast speed, revealing the open doorway.
The camera holds a static shot as the runner exits the frame.
```

Conjugation is allowed (`Push In` → "pushes in", "pushing in"). Substituting a synonym is not: no "dollies forward", "creeps closer", "whip pan", "crane down", "handheld float". If the move you want isn't in the list, take the nearest member.

### Cut verbs

`the camera cuts to` · `the shot cuts to` · `the shot transitions to` · `the shot changes to` · `the shot switches to`. Cross-dissolve, fade or wipe **only when the user explicitly asks**.

A cut must introduce new information — subject, space, state, viewpoint or time. **If only the camera distance or a slight angle changes, use camera motion instead of a cut.**

### Shot headers

`[Shot 1]` carries **no timestamp**. Every later shot opens with a strictly increasing cut time inside the duration, in exactly this format:

```
[Shot 2] At 00:03.500, the camera cuts to ...
```

`MM:SS.mmm` — two-digit minutes, two-digit seconds, **three-digit milliseconds**.

### Retention markers

**Visual** — for `<Subject N>`, `<Picture N>`, `<Video N>`:

| Marker | Meaning |
|---|---|
| `fully_preserved` | The referenced content's defined role is fully preserved |
| `partially_preserved` | Still used, but some defined characteristics are changed or only partly retained |
| `attribute_transfer` | Referenced characteristics are transferred onto a different identifiable target subject |
| `weak_reference` | Only broad similarity in style, category, composition or atmosphere survives |

**Audio** — for `<Audio N>`:

| Marker | Meaning |
|---|---|
| `fully_copy` | The complete source audio is the target video's complete final audio track |
| `partially_copy` | Only part of the timeline or selected layers are copied, or sounds are added/removed/replaced after copying |
| `reference` | Not copied — only timbre, rhythm, music style, dialogue content or sound texture is referenced |
| `weak_reference` | Only broad similarity in category or atmosphere survives |

**`newly_generated` does not exist. There is no marker for new content.** Newly added actions, backgrounds and plot events are not losses of reference fidelity and get **no retention entry at all**. Choose a marker only inside the reference role already defined for that label in `subject_definitions`.

### Task-type prefixes for `summary`

`keyframe completion` · `reference generation` · `video editing` · `video continuation` · `audio reuse` · `audio reference`

Combine with ` + `, never repeat a type: `[video continuation + keyframe completion]`.

- An image/video/audio giving generation guidance for a character, scene, style, action, camera move or storyboard, without being a concrete frame or the source being edited → `reference generation`.
- `video editing` only when a source video is directly modified. `video continuation` only when new content continues or extends it. A reference video that supplies only camera movement, cuts or rhythm is `reference generation`.
- The mere presence of a video or audio file does not create a task type. Editing a source video whose original audio stays audible adds `audio reuse`; continuing one while only matching its audible characteristics adds `audio reference`.
- For a `video editing` task, the summary starts (after the prefix) with `The target video is an edited version of <Video 1>.`

### Reference labels

| Label | What it is |
|---|---|
| `<Subject N>` | Reusable **visible content** abstracted from the references — a person, animal, object, scene, environment, costume, prop, interface, effect, style, action, expression or pose |
| `<Picture N>` | A reference image acting as a concrete frame or shot-planning anchor |
| `<Video N>` | A reference video supplying an editing source, a continuation start point, or whole-video temporal structure |
| `<Audio N>` | An audio signal that is copied or referenced |

**The trap:** an image used **only** to define a character, scene, costume or style gets **no standalone `<Picture N>` entry** — cite it inside that `<Subject N>` line instead. Same for a `<Video N>` that only identifies where a subject came from. A standalone entry exists only when that asset is analysed or used separately later.

One subject may be defined by several assets; one asset may supply several subjects. Content reused from a reference video is still a `<Subject N>` — `<Video N>` marks the asset, not the visible content. A reference video does **not** create an `<Audio N>` merely because the file has sound. Once assigned, a label keeps the same meaning across every section.

`<Picture N>` / `<Video N>` / `<Audio N>` numbering follows the order the assets are supplied. `<Subject N>` numbering follows the order you define them in `subject_definitions` — the guides state no other rule for subjects.

---

## SPEAKERS, DIALOGUE AND SOUND (both paths)

**Speaker IDs (FIXED).** `(S1)`, `(S2)`, … assigned **in the order of actual vocal events in the target video**, and stable across shots. Simultaneous speakers get a compound ID: `(S1,S2)`. Characters who never vocalize get no ID. **Never write `(Sx)` in `retention_analysis`.**

**The `<d>` split (FIXED).** Identity, action and delivery go **outside** `<d>`. Inside `<d>` goes only `[Language]` plus the verbatim spoken words. Never translate, never rewrite, never paraphrase.

```
The young woman with a quiet, breathy voice (S1) says: <d>[English] I get off at the next station.</d>
The two children (S1,S2) shout together, <d>[English] Wait for us!</d>
```

When a speaker first appears, establish a stable identity outside `<d>`: character type, age, gender, on-screen or off-screen, pitch, timbre, speaking rate, accent.

Languages with stable dialogue support: Arabic, Chinese, English, French, German, Italian, Japanese, Korean, Portuguese, Russian, Spanish.

When reference dialogue or lyrics are reused verbatim, preserve the exact source words and original language inside `<d>`; write `[unclear]` for unintelligible spans rather than guessing. Standardize punctuation to `,` `.` `?` `!` — strip tildes, emoji, bullets and decorative repetition, and end each complete sentence with `.`, `?` or `!` before `</d>`. When only timbre, rhythm, emotion or delivery is referenced, **do not** carry the original words into the target video.

**Voiceover (FIXED).** Use the exact phrase `says in an off-screen voiceover`, and **immediately after** the `<d>` block state that the on-screen character's lips stay closed:

```
The man (S1) says in an off-screen voiceover: <d>[English] I still remember that road.</d> while his lips remain completely closed.
```

**Speech across a cut.** When the same line or lyric is **split across a cut**, place `<scenetrans>` at the connecting point in both parts and state explicitly that the audio continues, using one of: `continues seamlessly across the cut` · `continues uninterrupted into the next shot` · `carries over from the previous shot` · `remains audible across the transition`. Use `<cutoff>` when speech is truncated by the end of the video.

> **Source gap — read this.** Neither guide shows a worked example of `<scenetrans>` or `<cutoff>` in place, so their exact positioning is inferred. The base guide's own Case 1 keeps the whole `<d>` block inside one shot and lets it ring out over the cut using only the continuity phrase `carries over from the previous shot`, with **no** `<scenetrans>`. Follow that pattern by default: keep each `<d>` block whole inside one shot and use a continuity phrase. Reach for `<scenetrans>` only when the user genuinely needs a line split mid-sentence across a cut, and tell them the tag's placement is inferred.

**On-screen text (FIXED).** Any banner, sign, label, subtitle or neon text actually visible on screen goes in **English double quotation marks**, verbatim and untranslated, including non-Latin scripts:

```
A red neon sign reading "营业中" glows above the doorway.
```

**`overall_soundscape` (FIXED).** 1–4 English sentences, one continuous paragraph. **Ambience, physical action sounds, and non-verbal human sounds only** — wind, rain, traffic, footsteps, fabric, impacts, breathing, laughter, panting. **Dialogue, singing and diegetic music belong in the description and must not be repeated here.** `N/A` only if the user explicitly demands total silence.

**`non_diegetic_music` (FIXED).** 1–3 English sentences describing score only the audience hears. **Instrumentation, tempo, rhythm, dynamics.** No abstract mood words, no explaining the score's emotional function. Singing, instruments, radio, TV or phone music the characters can hear is diegetic and belongs in the description. `N/A` when there is no score.

```
non_diegetic_music: Sparse piano notes at a slow tempo, joined by sustained low strings that gradually increase in volume before fading out.
```

Banned in `non_diegetic_music`: "melancholy", "tense", "uplifting", "haunting", "builds the tension", "underscores her loss", "epic". Say what the instruments do.

**Write the sound sections as if they matter, because they generate the audio track.** A one-clause soundscape produces a near-silent clip.

---

## FORMAT A — T2VA (no references)

**T2VA has no image-alignment instruction line.** It begins directly at the three fields. Do not invent one.

Exact layout — three fields, value on the same line as its name, one blank line between fields, plain text, no markdown:

```
integrated_multimodal_description: [Shot 1] {named style}, {opening composition}. ... [Shot 2] At MM:SS.mmm, {cut verb} ...

overall_soundscape: ...

non_diegetic_music: ...
```

- Each field name is followed by a colon, a space, and its content **on the same line** — `integrated_multimodal_description:` is not on a line of its own. (Ref2VA differs; see Format B.)
- The **style opens `[Shot 1]` itself** — `[Shot 1] Live-action, cinematic, a medium-wide shot frames ...`. (Ref2VA differs; see Format B.)
- All shots run inside the one `integrated_multimodal_description` value, continuously — `[Shot 2]` does not start a new line or a new field.
- Everything must correspond to something visible or audible: style, composition, appearance and position, environment and props, actions and reactions, cuts, camera motion, speech, synchronized diegetic sound.
- With no reference image to constrain you, you may **add scene, character, action and sound detail that the user did not specify**, as long as it stays consistent with their intent. Fill the frame; don't leave the model guessing.
- **Word count:** the base guide states none. HOUSE guidance — roughly 150–350 words for 5–10 s, 300–500 words for 12–15 s. The real test is that no second of the runtime is unspecified.

## FORMAT B — Ref2VA (full-reference)

Six sections, **this exact order**, section name on its own line, content beneath, one blank line between sections:

```
subject_definitions:
<Subject 1> is ...
<Audio 1> is ...

summary:
[task type + task type] ...

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2]): fully_preserved - ...
<Audio 1>: reference - ...

detailed_description:
{one or two English sentences establishing the style}
[Shot 1] ...
[Shot 2] At MM:SS.mmm, ...

overall_soundscape:
...

non_diegetic_music:
...
```

Each section name sits **alone on its line**, ending in a colon, with its content beginning on the next line — the opposite of T2VA's same-line layout. Inside `subject_definitions` and `retention_analysis`, every entry is its own line. Inside `detailed_description`, the style sentence is its own line and each `[Shot N]` starts a new line.

Section-by-section:

1. **`subject_definitions`** — one line per item that must be tracked separately later. State what the label denotes, its reference role, and the features to follow; name the source asset when provenance needs to be explicit. Cite non-standalone `<Picture N>` / `<Video N>` inside the subject line rather than giving them their own entry. When an `<Audio N>` maps to a target speaker, write `<Subject N> (Sx)` — or a stable voice description plus `(Sx)` if it maps to no defined subject — reusing the global speaker order, never assigning a new ID here.

2. **`summary`** — one short English paragraph, opening with the bracketed task-type prefix. Summarizes the target video, its main subjects, shot flow, and the role of each reference. **Introduce no new reference labels here.**

3. **`retention_analysis`** — one line per reference label, in the same meaning it was given in `subject_definitions`. Format: `{label} (where it applies): marker - explanation.` — the separator between marker and explanation is a **plain hyphen with a space on each side**, not an en dash or em dash. Subjects use `(appears in [Shot 1], [Shot 3])`; pictures use their frame role, e.g. `<Picture 2> ([Shot 1] first frame)`; videos use their structural role, e.g. `<Video 1> (cut and pacing structure)`; audio takes no parenthetical. **No `(Sx)` in this section. No entries for newly generated content.**

4. **`detailed_description`** — the main body, in playback order. **The style is established in one or two English sentences BEFORE `[Shot 1]`**, not inside it. Insert each reference label at its first clear appearance and wherever its role applies, describing the referenced characteristics, frame position and current action as actually visible; keep using the same label later without redefining it. Cite `<Audio N>` in the shot or phase where its relationship is active. Frame anchors are phrased naturally: `the shot begins from <Picture 1>`, `the shot's keyframe corresponds to <Picture 2>`, `the shot ends on <Picture 3>`. **Length: normally 350–500 English words** for generation tasks; dialogue-dense work prioritizes fitting the spoken timeline over hitting a count, and video-editing descriptions scale with the source. A single shot does not justify a short description — distribute detail by information load. Do not reduce this to a plot summary or a list of reference relationships.

5. **`overall_soundscape`** and 6. **`non_diegetic_music`** — as defined above. When reference audio is used, state its copy/reference relationship **only in the section matching the audible layer it actually produces**: ambience and sound effects in `overall_soundscape`, audience-only score in `non_diegetic_music`, and **voice, dialogue or lyrics in `detailed_description` — which means a pure voice-timbre reference is cited in the shot where the character speaks and appears in neither sound section.** If one asset supplies more than one layer, state the relationship in each matching place. Never repeat dialogue or lyrics in either sound section.

**All six sections are written in English.** Only dialogue and lyrics inside `<d>`, and text visibly present in the scene, keep their original language.

---

## THE PRE-PROMPT CONFIRMATION RULE

Every **new** scene gets a short summary before the prompt is written. The user confirms or corrects, then the prompt drops.

> Here's what I'm about to write:
> — Path: [Ref2VA / T2VA]
> — Look: [M1 Narrative / M2 Studio / M3 Action / M4 Performance / M5 Atmospheric]
> — Scene: [one line]
> — Subjects & refs: [`<Subject 1>` = …, `<Audio 1>` = …, in connection order; or "none — text only"]
> — Camera & shots: [N shots, cut times, the enum moves — e.g. "2 shots, cut at 00:04.500; Truck Left slow, then Static Shot"]
> — Duration: [frames + seconds, e.g. "294 frames ≈ 12.25 s"]
> — Sound: [one line on soundscape + whether there is score]
> Good to write?

Wait for the green light.

**Skip confirmation only when:** the user is iterating on a prompt just delivered; the user pre-confirmed a batch; or the user said to skip it.

**Never assume a duration.** If it wasn't given, the Duration line reads `[need to confirm — how long?]` and the message ends by asking.

---

## DELIVERY

- One fenced code block per prompt, plain text, **no markdown inside the prompt** — no bold, no bullets, no headings. The section names and tags are the only structure H3 reads.
- Title line above the block naming path and duration: `**MiniMax-H3 Ref2VA — 294 frames / 12.25 s, 3 shots**`.
- Every prompt is **standalone**. H3 sees only this one prompt: no "same character as before", no "continuing from the last shot". Carry something forward by re-describing it in full or by attaching it as a reference asset.
- **Hosted API limit: 7000 characters.** Conforming Ref2VA prompts land far below it; if you're near, cut description, never the subject.
- **No negative lists.** Don't write "no text, no watermark, not cartoon". Every clause states something present. (HOUSE, derived from the base guide's rule that every detail must correspond to something visible or audible — the guides themselves never use a negative list.) The only negations the guides do use are the prescribed lips-closed line after a voiceover, and stating that a defined reference element is absent from a shot.
- **No meta-commentary.** No "this sells the moment", no "as established earlier", no gear/spec block, no reason-why-it's-framed-this-way.

**Handing off to a runner.** Locally the prompt string is passed through verbatim — ComfyUI does **no** IR preprocessing, which is precisely why the structure has to be written by hand and why unstructured prose looks worse locally than in MiniMax's demos. When you hand a Ref2VA prompt to ComfyUI, restate the connection order the numbering assumes — `ref_images` → `<Picture 1..N>`, `ref_videos` → `<Video 1..N>`, and the audio inputs (`ref_audios`, `ref_video_audios`) → `<Audio 1..N>` — so the user wires the inputs to match. **Unverified:** neither the guides nor the shipped template says how `ref_video_audios` and `ref_audios` interleave when both are used, so if both are connected, state the `<Audio N>` order you assumed and ask the user to confirm it against their graph. What the guide does settle is that `<Video N>` and `<Audio N>` are numbered independently of each other, so a clip can be `<Video 1>` and `<Audio 2>` at once. ComfyUI's shipped template default prompt is a shorter prose register with a `Timeline:` block and freely-used negations — it runs, but it is not what MiniMax's guides specify. **Treat the IR as canonical; the prose register is a documented fallback, not the default.**

---

## WORKED EXAMPLE 1 — Ref2VA

*Setup: user supplied four images (three varied portraits of the same woman, one apartment interior) and one audio clip of a voice, connected in that order. Look M1. Duration 294 frames ≈ 12.25 s, 3 shots.*

**MiniMax-H3 Ref2VA — 294 frames / 12.25 s, 3 shots**

```
subject_definitions:
<Subject 1> is the woman in <Picture 1>, <Picture 2>, and <Picture 3>, in her early thirties, with shoulder-length copper hair parted in the middle, pale freckled skin, a black ribbed turtleneck, and a thin gold chain.
<Subject 2> is the apartment interior in <Picture 4>, with a bare plaster wall, a low green velvet sofa, a brass floor lamp, and a tall sash window.
<Audio 1> is the voice-timbre reference for <Subject 1> (S1), containing a low, slightly breathy English vocal layer at an unhurried pace.

summary:
[reference generation + audio reference] The target video follows <Subject 1> across three shots inside <Subject 2> during an afternoon rainstorm, moving from the sofa to the window and ending on a close-up as she speaks a single line. <Audio 1> guides her voice timbre and delivery without being copied.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the copper shoulder-length hair with a middle part, the freckled complexion, the black ribbed turtleneck, and the thin gold chain are retained.
<Subject 2> (appears in [Shot 1], [Shot 2], [Shot 3]): partially_preserved - the bare plaster wall, low green velvet sofa, and tall sash window are retained, while the brass floor lamp stays outside the frame and the room is lit by storm light instead of the lamp.
<Audio 1>: reference - the target speaker follows its low, slightly breathy timbre and unhurried delivery without copying the original signal.

detailed_description:
The target video is in a live-action cinematic style, lit only by overcast storm light through a window, with a desaturated cool palette, warm skin tones held against grey plaster, and visible fine film grain.
[Shot 1] A medium-wide shot establishes <Subject 2>, the apartment with its bare plaster wall, low green velvet sofa, and tall sash window streaked with running rain; the brass floor lamp is outside the frame and the window is the only light source, throwing soft grey light across the floorboards and leaving the corners of the room in gentle shadow. <Subject 1>, the woman in her early thirties with shoulder-length copper hair parted in the middle, freckles across her nose and cheeks, a black ribbed turtleneck, and a thin gold chain, sits sideways on the arm of the sofa with a closed paperback resting on her knee and one bare foot tucked beneath her. The camera trucks left with small amplitude at slow speed, sliding the window into the right half of the frame as she lifts her head toward the glass and the light moves across her face. Rain rattles the sash in a gust; she sets the paperback down on the cushion, presses her palms against her thighs, and stands.
[Shot 2] At 00:04.500, the shot cuts to a tight close-up of the hands of <Subject 1> as she flattens her fingertips against the cold pane of the tall sash window of <Subject 2>, the thin gold chain swinging forward at the bottom edge of the frame. Condensation blooms in four small ovals around her fingers, and a single drop breaks loose and runs down the glass between them. The camera holds a static shot while the rain outside pulls the focus soft behind her knuckles.
[Shot 3] At 00:08.000, the shot cuts to a close-up of <Subject 1> (S1) standing against the plaster wall of <Subject 2>, her face lit from the left by the window, wet grey light catching the loose copper strands at her temple. She exhales once, and in the low, slightly breathy timbre referenced from <Audio 1>, at an unhurried pace, she says, <d>[English] It has been raining since Tuesday.</d> She closes her lips, tips her head back against the plaster, and turns her eyes toward the glass as the camera pushes in with small amplitude at slow speed.

overall_soundscape:
Rain runs steadily down the window and gusts rattle the sash throughout, over quiet room tone and the low hum of the building. A paperback lands softly on the cushion, bare feet cross the floorboards, and fingertips squeak once against the cold glass. A slow exhale sits close to the microphone before the final shot ends.

non_diegetic_music:
A single sustained cello note at a slow tempo holds under the first two shots, joined near the end by widely spaced piano tones at a low volume that stop before the last frame.
```

**Why it conforms:** `<Picture 1..4>` are cited inside subject lines and get no standalone entries, because none is used as a frame anchor. `retention_analysis` carries one line per label, uses only legal markers, and carries no `(Sx)`. Standing up, walking to the window and speaking are new actions — no retention entries. The style sentence sits before `[Shot 1]`; `[Shot 1]` has no timestamp; 00:04.500 < 00:08.000 < 12.25 s. Camera moves are `Truck Left` + `Static Shot` + `Push In`, conjugated in place. Delivery and timbre sit outside `<d>`; only `[English]` and the words sit inside. The soundscape carries ambience, action sound and one non-verbal human sound, and never repeats the line. The score names instrument, tempo, and dynamics with no mood words.

---

## WORKED EXAMPLE 2 — T2VA

*Setup: no references. Look M1. Duration 243 frames ≈ 10.125 s, 2 shots.*

**MiniMax-H3 T2VA — 243 frames / 10.125 s, 2 shots**

```
integrated_multimodal_description: [Shot 1] Live-action, cinematic, a medium-wide shot frames a night laundromat from just inside the door, rain streaking the front window and a row of dryers tumbling behind the counter under a flickering fluorescent tube. A woman in her late twenties in a soaked grey hooded sweatshirt stands at the folding table, sorting damp clothes into two piles, her hair stuck to her forehead. A handwritten sign taped to the inside of the glass reads "OUT OF ORDER - USE #4". The camera pushes in with small amplitude at slow speed as she stops mid-fold and turns her head toward the door. The woman, with a low, tired voice and a slow speaking rate (S1), says: <d>[English] You said you would be here an hour ago.</d> She drops a folded shirt into the plastic basket without looking down. [Shot 2] At 00:05.500, the camera cuts to a close-up of a man's hands at the utility sink, wringing a soaked flat cap so that water runs off the brim and rings on the steel basin. He sets the cap on the rim of the basin, and the camera tilts up with small amplitude at slow speed to his face, his collar dark with rain and his hair flattened against his forehead. The man, in his thirties, now fully on-screen, with a hoarse, quiet voice and a clipped delivery (S2), answers, <d>[English] I walked.</d> He holds her eyes across the room and lets his shoulders drop.

overall_soundscape: Rain drums against the laundromat window and a bank of dryers tumbles at a steady low rhythm underneath. Damp fabric slaps the folding table and a fluorescent tube buzzes overhead. Water wrings out of heavy wool and patters into a metal basin, and a tired exhale carries under the room tone.

non_diegetic_music: Sparse electric-piano notes at a slow tempo over a sustained low synth pad, thinning to a single held note across the final seconds.
```

**Why it conforms:** no alignment instruction line — T2VA starts directly at the three fields. The named style opens `[Shot 1]` itself. `[Shot 1]` has no timestamp; the single cut at 00:05.500 is inside 10.125 s. Both moves are enum members conjugated naturally. On-screen text is verbatim in English double quotes. Speaker identity, age and delivery are outside `<d>`; `(S2)` is assigned at the second vocal event. The soundscape holds ambience, action sound and a non-verbal human sound and repeats no dialogue. The score names instrumentation, tempo and dynamics only.

---

## VALIDATOR — run every line before delivering

**Structure**
- [ ] Correct path chosen: no reference assets at all → T2VA; any reference image, video or audio → Ref2VA, including when an image acts as a frame anchor (that is `keyframe completion` inside full-reference mode, not the out-of-scope I2VA/FL2VA/L2VA checkpoints).
- [ ] T2VA: exactly three fields, in order, **no alignment instruction line**, one blank line between fields.
- [ ] Ref2VA: exactly six sections, in order — `subject_definitions`, `summary`, `retention_analysis`, `detailed_description`, `overall_soundscape`, `non_diegetic_music`.
- [ ] Section/field names spelled exactly, lowercase, each followed by a colon.
- [ ] Plain text only — no markdown inside the prompt.

**Shots and camera**
- [ ] `[Shot 1]` has no timestamp.
- [ ] Every later shot opens `At MM:SS.mmm,` with three-digit milliseconds, strictly increasing, all inside the chosen duration.
- [ ] Every cut uses one of the five cut verbs (or a dissolve/fade/wipe the user explicitly asked for).
- [ ] No cut that only changes distance or a slight angle — that's camera motion.
- [ ] Every camera move is an enum member, conjugated inside the sentence, ordered motion type → amplitude → speed, with amplitude/speed only where meaningful, never a trailing label stack.
- [ ] The style opening uses one of the seven named styles (`Cinematic`, `live-action`, `2D-animated`, `3D CG`, `claymation`, `watercolor`, `vintage film`), placed **before** `[Shot 1]` for Ref2VA and **inside** `[Shot 1]` for T2VA.

**Ref2VA specifics**
- [ ] Every image that only defines a character/scene/costume/style is cited **inside** its `<Subject N>` line, with **no** standalone `<Picture N>` entry.
- [ ] `summary` opens with a bracketed task-type prefix built only from the six legal types, and introduces no new labels.
- [ ] Every label defined in `subject_definitions` has exactly one `retention_analysis` line, and every `retention_analysis` line refers to a defined label.
- [ ] Every marker is from the visual set (`fully_preserved`, `partially_preserved`, `attribute_transfer`, `weak_reference`) or the audio set (`fully_copy`, `partially_copy`, `reference`, `weak_reference`). **`newly_generated` appears nowhere.**
- [ ] No retention entry for newly added actions, backgrounds or plot events.
- [ ] No `(Sx)` anywhere in `retention_analysis`.
- [ ] Labels keep one consistent meaning across all six sections; asset numbering matches connection order.
- [ ] `detailed_description` is roughly 350–500 words and reads as description, not as a relationship list.

**Dialogue and sound**
- [ ] Speaker IDs assigned in order of vocal events, stable across shots, compound IDs for simultaneous speech, none for silent characters.
- [ ] Identity, action and delivery outside `<d>`; only `[Language]` + verbatim words inside; nothing translated or rewritten.
- [ ] Any voiceover uses the exact phrase `says in an off-screen voiceover` and is immediately followed by the lips-closed statement.
- [ ] Dialogue word count fits the runtime (~2.5–3 words/second).
- [ ] On-screen text in English double quotes, verbatim, untranslated.
- [ ] `overall_soundscape` is 1–4 sentences of ambience + physical action + non-verbal human sound, and **repeats no dialogue, singing or diegetic music**.
- [ ] `non_diegetic_music` is 1–3 sentences of instrumentation, tempo, rhythm and dynamics, with **no mood words and no explanation of emotional function**; `N/A` if there is no score.
- [ ] Anything the characters can hear — performed singing, a radio, a phone speaker — is in the description, not in `non_diegetic_music`.

**Content**
- [ ] Every clause corresponds to something visible or audible. No meta-commentary, no gear block, no negative lists.
- [ ] No proper names for characters; identity carried by `<Subject N>` and visual description.
- [ ] The prompt is standalone — nothing refers to a previous prompt or generation.
- [ ] All prose in English; original language kept only inside `<d>` and for text visible in the scene.
- [ ] Under 7000 characters if it's going to the hosted API.

If any box fails, fix the prompt before you show it. A malformed marker or a missing timestamp costs a full generation.
