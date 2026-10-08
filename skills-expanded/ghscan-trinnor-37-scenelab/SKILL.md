# one-take-ugc

Generates a single-shot, continuity-locked UGC-realism video prompt: one unbroken phone-camera take with locked verbatim dialogue, fixed camera geometry, and second-by-second choreography binding speech to physical action.

Use this skill when the brief calls for authentic, handheld, "she's talking straight to camera while doing something" content — product demos, testimonials, routine videos, unboxings — where the goal is to read as a real phone recording, not an AI-generated clip.

This skill produces ONE camera movement style: locked-off after an initial handheld placement. It is not a general camera-movement skill — for pans, dollies, tracking shots, or other movement, use Cinema Gear 2.0 instead. In SceneBloc, this skill should be exposed as a single option inside Cinema Gear 2.0's movement picker ("One-Take Locked (UGC realism)"), not as a separate mode fork. Selecting any other movement in that picker means this skill's rules do not apply.

## Why this structure works

Real phone-recorded UGC content has specific tells that AI video generation gets wrong by default: models cut between angles like edited video, insert idle "waiting for the line" stillness, and let identity/skin details drift during action. Each section below exists to suppress one specific failure mode. Do not remove or weaken any FIXED clause — they are the mechanism, not decoration.

## Mandatory Prompt Structure

Every generated prompt must contain these eight sections, in this order:

### 1. Continuity Lock (FIXED — insert verbatim, do not paraphrase)

```
ONE UNBROKEN TAKE. {{DURATION}} of continuous recording from a single camera
that never stops rolling. There are no cuts, no edits, no transitions, no
jumps, no angle changes, no reframing, no shot changes. Time never skips.
This is one single continuous recording from beginning to end.

ABOUT THE TIMESTAMPS BELOW. The timestamps mark when things occur inside the
one continuous take. They are not shot boundaries, not clip divisions, and
not edit points. Nothing changes at a timestamp except what she is doing.
The camera keeps rolling straight through every one of them.

NO DEAD AIR. She never stops, stares, or holds a blank expression between
actions. Every movement overlaps the next — she is already beginning the
following action before the current one finishes, and she talks through
her movements rather than pausing to speak. There is no moment where she
sits motionless waiting for a line, and no moment after a line where she
holds a still expression. Speech, gesture and activity run continuously
and overlap throughout.
```

### 2. Device Realism Clause (FIXED — insert verbatim)

```
NO VISIBLE PHONE OR DEVICE. The camera is her phone. No phone, screen,
handheld device or recording equipment appears anywhere in frame at any
point. During the opening she is carrying the camera — her {{CARRY_ARM}}
arm is extended toward the lens and heavily foreshortened at the frame
edge, and her hand is out of frame. Her other hand is empty. She is never
seen holding a phone while a phone films her.

FORMAT. {{ASPECT_RATIO}}. Front-facing phone camera. Mild wide-angle
distortion.
```

### 3. Camera Geometry (fill per brief)

Establish: reflective surface (mirror/window/none) and its position; camera rest position and offset angle from her facing direction; her resting body position (e.g. three-quarter); which side is nearer the lens; where her natural gaze exits frame vs. where she turns to address the viewer; what's visible at the extreme frame edges; what fills the open side of frame (background elements); where any hero prop container sits at frame start.

### 4. Lighting (fill per brief)

Establish: light quality and source direction; diffuser if any; color temperature; which practical lights are off; how the light rakes across her face given her body position — name which side falls into shadow and which is lit.

### 5. Delivery (fill per brief)

Accent, pace (default: 3.4 words/second unless brief specifies otherwise), tone quality. Lines run into one another without gaps.

### 6. Dialogue — Locked Verbatim (FIXED instruction, fill lines)

```
She speaks exactly these words, in exactly this order. No improvisation,
no rewording, no reordering, no additions, no omissions. This is the
complete and only dialogue in the video.
```

Generate exactly 6 lines, timestamped, sized to fill the target duration at the delivery pace, with ~0.5–1s natural gaps between lines:
- LINE 1: Hook
- LINE 2: Setup / relatable framing
- LINE 3: Context / what this is
- LINE 4: Differentiator / what makes this different
- LINE 5: Value / detail
- LINE 6: CTA

### 7. Continuous Behaviour (FIXED skeleton — adapt specifics to the scene)

```
She is never still or neutral. Across the full {{DURATION}}: eyebrows move
constantly with her speech, lifting on emphasis and drawing in slightly on
key words. She blinks at irregular intervals, sometimes twice in quick
succession. Her mouth stays active between words — small lip presses, a
slight purse while thinking, tongue against the inside of her cheek. Her
head makes small tilts and nods tracking her own sentences. Shoulders shift
and settle. She adjusts her seated weight two or three times. Her hands are
almost never at rest; when not gesturing they touch the desk edge, her own
forearm, a strand of hair. Her eyeline moves continuously between three
places — the lens, {{REFLECTIVE_SURFACE_OR_OMIT}}, and whatever her hands
are doing. She takes audible breaths between lines. She never freezes to
deliver a line.
```

### 8. The Recording, In Order (the engine — generate in ~5s blocks)

Choreograph the full duration in sequential timestamped blocks. Each block must:
- Bind physical action to a dialogue line's exact timestamp range
- Have the *next* action begin before the current line/action finishes (overlap, never sequence)
- Include one camera/lighting/skin-realism micro-detail per block, placed at whichever moment brings her physically closest to the lens (this is when phone cameras actually resolve fine detail — see realism-details.md for the tag vocabulary)
- Note a gaze-target shift where relevant (lens / reflective surface / hands)

Standard beat shape for a 30s duration (scale proportionally for other durations):
1. **Entry (0–4s):** camera already recording, carried into frame, hands/gaze established, Line 1 delivered
2. **Camera Placement (4–4.8s):** camera set down and locked — note this is the ONLY camera movement in the whole take; after this point every image change comes from her, never the camera
3. **Settle + Line 2 (4.8–8s):** sit/turn/speak happen together, not in sequence; first realism-detail peak here (closest proximity moment)
4. **Prop 1 Retrieval (8–13.6s):** first object retrieved and handled while talking, Line 3
5. **Prop 2 Reveal (13.6–18.3s):** second object introduced, not presented to camera — handled naturally, Line 4
6. **Prop 2 Use (18.3–24.5s):** object opened/activated, Line 5, gestures stay low and close to body
7. **Prop 3 / Payoff (24.5–29.4s):** final object/application, Line 6 runs underneath
8. **Return / Close (28.9–29.5s):** she returns to lens, closing the same turn used at the settle beat — this creates a loop
9. **Out (29.5s–end):** reaches forward, camera lifted, recording stops mid-motion

Adjust the number and nature of prop beats to match the brief — not every video needs 3 props. The proportions (roughly: entry 13%, placement 3%, settle 10%, then even splits across remaining action beats, close 2%, out 2%) scale to any duration.

## Realism Details

This skill does NOT own its own realism vocabulary. Realism tags, the
mandatory skin-tone-accuracy clause, and peak-intensity placement logic all
come from the shared `human-realism-system` skill, imported via
`lib/realism.ts`'s `buildRealismContext()`. See
`lib/prompt-skills/human-realism-system/SKILL.md` for the full system.
Do not invent realism tags locally or re-add a local realism-details.md —
add new tags to `lib/realism.ts`'s `REALISM_TAGS` instead, so every skill
benefits from the addition.

## What NOT to do

- Do not add camera movement, cuts, or angle changes anywhere after the initial placement beat (4.8s onward is fixed-position for the rest of the take)
- Do not let the dialogue and choreography run as separate tracks — every line must be anchored to a specific physical action happening at the same timestamp
- Do not front-load realism detail evenly across the timeline — concentrate it at proximity-peak moments, matching how a real phone camera actually resolves detail
- Do not omit the skin-tone-accuracy clause when any realism tag is used
