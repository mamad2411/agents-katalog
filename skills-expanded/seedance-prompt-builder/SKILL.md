---
name: seedance-prompt-builder
description: Write production-ready Seedance 2.0 prompts (image, video, and motion/edit) for Higgsfield. Use this skill whenever the user wants a single Seedance prompt rather than a full shotlist — e.g. "make a Seedance prompt for X", "write me a video prompt", "restyle this clip", "turn my photo into a character sheet", "transformer video of my car", "bullet-time freeze", "sticker peel", "swap the character in my video". Covers the recurring prompt recipes (text-to-video, POV action, character/storyboard image sheets, timed-beat edits, JSON prompts, transformer template, freeze-frame, sticker peel, environment/object restyle) and the exact media-placeholder syntax Seedance expects. If the user instead wants a whole script broken into many numbered 15-second shots, use the seedance-shotlist-director skill instead. This skill produces one copy-ready prompt block (plus any required reference-image prompt) directly in chat.
---

# Seedance 2.0 Prompt Builder

You write single, copy-ready Seedance 2.0 prompts for Higgsfield. One request → one prompt the user can paste straight into Seedance. When a job needs a reference image first, you write the image prompt too, in order.

This is **not** the shotlist skill. No HTML, no checkboxes, no breaking a whole script into dozens of shots. One focused prompt (occasionally a short chain: image → video).

---

## First, pick the recipe

Read what the user wants and match it to one of the recipes below. When unsure, ask one short question. The recipes are patterns, not rigid templates — adapt them.

| User wants… | Recipe |
|---|---|
| A quick clip from a text idea | **A. Text-to-video** |
| First-person action (hands in frame, powers) | **B. POV action** |
| A character to reuse across shots | **C. Character sheet** (image) |
| A blocked-out fight/scene plan as one image | **D. Storyboard sheet** (image) |
| Precise timing / dialogue beats in one clip | **E. Timed-beat** |
| Maximum structure / machine-readable | **F. JSON prompt** |
| A vehicle/object becoming a giant robot | **G. Transformer template** |
| Frozen moment, camera orbits | **H. Bullet-time freeze** (image ×2 → video) |
| Peel a subject out as a paper sticker | **I. Sticker peel** |
| Keep a clip's motion but change look/world/object | **J. Restyle / swap / replace** (edit) |

---

## Media placeholders (this is the law)

Seedance references uploaded media by placeholder, kept **verbatim** in the prompt text. The user uploads the actual files in Higgsfield; you just write the placeholder.

- `<<<video_1>>>`, `<<<video_2>>>` — uploaded videos
- `<<<image_1>>>`, `<<<image_2>>>` — uploaded images (e.g. start frame / end frame)
- `@img`, `@video1`, `@` — alternate shorthand seen in some edit prompts; use the triple-angle form by default unless the user is copying an existing pattern

Rule of thumb for **edits**: name the source clip, state the single change, then **lock everything else**: "keep the exact same camera motion, framing, composition and performance from `<<<video_1>>>`." That lock line is what makes edits hold together.

Whenever a prompt relies on uploads, end your chat message with a one-line note telling the user which files to upload (e.g. "Upload your clip as video_1 and your character still as image_1").

---

## Core building blocks (used across recipes)

- **Realism tags**: "ultra-realistic live-action", "hyper-realistic", "cinematic realism", "real movie style", "photorealistic textures".
- **Camera language**: lens (14mm/24mm/35mm/50mm/85mm), angle (low/eye-level/Dutch), move (dolly-in, orbit, whip-pan, crash-zoom, handheld, crane). Motivate the move.
- **Speed-ramp / bullet-time**: "speed ramp", "ultra slow motion", "bullet-time", "the world frozen while only X moves at full speed".
- **Trailing tag cloud**: many strong prompts end with a comma-separated list of style/effect keywords. It reinforces the look. Use it for action and stylized pieces.
- **Negative prompt**: end with "Negative: No cartoon look. No anime. No glitch. No morphing…" or inline "no text, no watermark". Add whenever a clean result matters.
- **Diegetic sound**: SFX/music cues can be embedded inline per beat ("SFX: soft flare hiss, low bass pulse"). Seedance honors them.

---

## The recipes

### A. Text-to-video (quick)
One to three sentences, declarative, front-load the subject, add a couple of realism tags. Optionally one camera instruction.
> `Woman playing cello, ultra detailed, start close to her hands and then go wide`

For bigger action, expand into a short paragraph of beats, then a trailing tag cloud (see B).

### B. POV action
First-person framing, hands/body part in the foreground, escalating beats in prose, then a dense tag cloud. Pattern: establish POV → beat 1 → beat 2 → escalating climax → tag cloud listing every effect and the realism keywords. Reference the Colosseum POV example as the gold standard for density.

### C. Character sheet (image, then reuse)
Image prompt to lock a character you'll reference later:
> `create a character sheet of [subject] with close-up and full-body shots from different angles in [style] style`
Then the generated sheet becomes `<<<image_1>>>` in a follow-up video prompt. Tell the user this is a two-step chain.

### D. Storyboard sheet (image)
For a whole sequence planned in one frame. Use bracketed sections: `[PROJECT CARD]` (title, meta, brief), `[SCENE]`, `[REFERENCE RULE]` (which uploaded image is the authority for each character's likeness), `[VISUAL RULES]` (clean low-detail blocking, what to avoid), `[CONTINUITY]`, optional `[DIRECTOR STRIP]` (rhythm/escalation track), `[SEQUENCE]` (numbered panels in a grid, each with lens + beat name). Keep panel interiors sparse; put labels in header strips. This produces a previs board, not finished art.

### E. Timed-beat
One clip with explicit timecodes. Pick one notation and stay consistent: `[00:00–00:02]`, `00-02s:`, or `0:00–0:02`. Each beat = shot description + action + (optional) dialogue + (optional) SFX. Good for dialogue scenes and tightly choreographed action. End with a tag cloud / negative if stylized.

### F. JSON prompt
Maximum structure. A JSON object with keys like `title`, `style`, `camera` (perspective, shot_type, lens, focal_length, motion[]), `scene` (environment, details[]), `action` (movement[], events[]). Paste as-is into Seedance. Use when the user wants precision or to template many variations.

### G. Transformer template (reusable)
Vehicle/object → Cybertronian giant. Five timed beats, swap the nouns:
1. **00-02s Setup** — wide, eye-level, the object moving normally, "grounded and realistic".
2. **02-05s Transformation begins** — it violently bursts open; head pushes out (color + glowing eyes); parts fold/spin/reconfigure into limbs.
3. **05-08s Ejection** — the driver/operator is thrown clear as it finishes forming.
4. **08-11s Mount** — they fearlessly charge, grab shifting plating, vault up onto the shoulder/back.
5. **11-14s Hero pose** — low-angle epic; figure stands gripping armor; titan aggressive, fists crackling; cinematic lens flare.
Fill in: object, city/setting, robot archetype (titan/eagle/sentinel), color palette, weather/light.

### H. Bullet-time freeze (image ×2 → video)
1. **Image prompt** — a cinematic freeze-frame mid-action, shallow DOF, debris/particles bursting toward the lens and hanging frozen.
2. **Image prompt** — "keep this photo the same, but add a perfect plain-white border ~10% of the size, as a 3D effect where the bursting elements spill into the white box. Change nothing else."
3. **Video prompt** — "Bullet-time freeze frame: everything frozen; the camera rotates around the floating frozen object; keep the white border."

### I. Sticker peel (locked-off or living photo)
A manicured hand peels the subject out as one flat die-cut paper sticker along a single continuous path from one lifted edge. Specify: background stays still like a printed photo; white border/backing appears only where already peeled; realistic paper bend + thickness + contact shadows; final beat brings the sticker to camera. **Living-photo variant**: the printed subject keeps moving (from `<<<video_1>>>`) the whole time and never freezes. Always add the negative: no extra fingers, no morphing, no early white outline.

### J. Restyle / swap / replace / extend (edit)
The workhorse. Name the source, make one change, lock the rest.
- **Environment restyle**: "change the environment in `<<<video_1>>>` so it looks like [world], change the lighting to [look], [optional new action]; keep the exact same camera motion, framing, composition and performance."
- **Character swap**: "turn the characters in `<<<video_1>>>` into the characters in `<<<image_1>>>`, keep the exact composition and motion from `<<<video_1>>>`."
- **Object replace**: "Replace the [object] in `<<<video_1>>>` with [new object]."
- **Add element**: "after 0.2s metal armour magnetically attaches to the arm in `<<<video_1>>>`" / "a huge energy beam fires from the device in `<<<image_1>>>`".
- **Start→end frame**: "start frame is `<<<image_1>>>`, end frame is `<<<image_2>>>`".
- **Keep lip-sync**: when speech matters, add "use the same motion and lip sync from `<<<video_1>>>`".

---

## Output format

- Put the final prompt in its own fenced code block so the user can copy it cleanly. Keep placeholders (`<<<video_1>>>`, `@img`) exactly as written.
- If the recipe needs a reference image first, give the **image prompt block**, a one-line "→ generate this, then use it as image_1", then the **video prompt block**.
- Below the block(s), add one short line listing what to upload, if anything. Nothing else — no long explanation unless asked.
- English prompt text always, even if the user writes in another language (Seedance expects English).
- Default to a trailing tag cloud and a Negative line for stylized/action work; keep simple test clips clean and short.
