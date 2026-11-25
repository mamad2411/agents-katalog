---
name: vox-style-collage-video
description: >-
  Turn a script or fact list into a finished Vox-style paper-collage explainer
  video: flat torn-edge photographic cut-outs, off-white newsprint ground with ONE
  bold accent color, big kinetic typography synced to the voiceover, infographic
  motifs (maps, arrows, redlines, timelines, charts), limited low-frame-rate cutout
  motion, narration-first pacing. ALL image/video/music generation runs on Unsora
  (create_image nano-banana-pro, create_video seedance-2.0, create_music
  mureka-7.5); the VOICEOVER is the one thing Unsora cannot make, so it comes from a
  supplied file or the session's own TTS tool, then timed and mixed with ffmpeg. Use
  whenever the user wants a Vox-style or editorial/news/journalism explainer collage
  video from text, says "make a Vox-style video/explainer", "paper collage
  explainer", "turn this script into a Vox video", wants one Vox-collage shot's
  prompts, or asks to write, voice, or time narration onto a Vox-style animation.
  Default to this for any Vox paper-collage explainer built on Unsora.
---

# Vox Collage Video

Script in, finished Vox-style explainer MP4 out — or a single shot's prompts, if
that's all that's asked. Self-contained: the visual style system, the prompt
templates, and the production pipeline all live in this folder.

**Runtime target:** this skill is written for Claude, OpenClaw, and Hermes Agent
style skill runtimes.

**Hard precondition:** Unsora MCP must be connected and authenticated before
running any image, video, music, or optional posting step. If the Unsora MCP tools
are missing, stop before the approval gate and tell the user to connect Unsora MCP
first. Do not replace Unsora with another generator unless the user explicitly
asks for a port of the skill.

**The style, in one line:** flat photographic cut-outs with torn edges, layered
photomontage-style over an off-white newsprint ground, ONE bold accent color, big
kinetic typography that lands the point, infographic marks (maps / arrows /
circles / redlines / timelines), limited low-frame-rate cutout motion, and a
voiceover the whole cut is timed to.

**What makes it *Vox*, not a generic paper cutout:** the subjects are **cut-out
photographs** (archival, editorial, magazine — not engravings or storybook
shapes); the on-screen **typography carries the argument** and moves in sync with
the narration; the vocabulary is **journalistic infographics** (a red line on a
map, a circled face, a rising bar); and the whole thing is **narration-first** —
the VO is written and voiced *before* the shots are sized, and every shot is cut
to its line.

**The tool split (read this — it is the point of this skill):**

- **Everything visual + the music runs on Unsora.** `create_image`
  (`nano-banana-pro`) for hero frames and reference sheets → `create_video`
  (`seedance-2.0`) to animate each frame → `create_music` (`mureka-7.5`) for the
  underscore. Each `create_*` is async; poll its `wait_for_*`.
- **The voiceover never comes from Unsora — it has no TTS.** It comes from
  **outside this skill**: either the user **supplies a VO audio file**, or it is
  synthesized on **whatever TTS tool happens to be connected in the session** (see
  `references/pipeline.md` §VO for how to find one and what to do if none exists).
  The user decides at the front door. Never quietly substitute a connector, and
  never claim Unsora voiced it.
- **Assembly, timing, and the mix are ffmpeg**, locally.

**The pipeline, in one line:**

```
elicit params → read script → beat map (flag recurring assets) → shot list + VO draft
  → [APPROVAL GATE] →
  VO FIRST: obtain each line's audio (supplied file, or the session's TTS tool) →
    measure real durations → size each shot to its line →
  reference sheets (Unsora create_image, only for assets recurring across shots) →
  per shot: Unsora create_image (hero frame) → create_video (animate) →
  [music: Unsora create_music] → ffmpeg concat → time VO to cut, duck + mix → final.mp4
```

If the user wants only prompts for one or a few shots — no generation — run
**Part 1** and output shots in the per-shot format. If they want the film, run
everything.

---

# PART 0 — THE FRONT DOOR (resolve before spending anything)

Infer what you can from the request; ask only what is genuinely missing. On a
chat client with tappable inputs, ask with those; otherwise ask in one short
message. Never call a generation tool before these are fixed and the shot list is
approved.

1. **The script / idea.** Paste a script, VO copy, or beat list (`.docx`, `.txt`,
   `.md`, `.pdf`, fountain, or typed). If it's just an idea or a feature brief,
   say so and offer to write a beat list first for approval.
2. **Orientation.** `16:9` (YouTube / the native Vox format — default for
   explainers), `9:16` (Shorts / Reels / TikTok), or `1:1`. Infer from platform
   mentions.
3. **Voiceover source** — the one deliberate cross-tool choice. Vox style is
   narrated, so a VO is the default, and Unsora can't make it. Offer:
   **(a) I'll write the script and you supply the voiced audio file**, **(b) write
   it and voice it on a TTS tool connected in this session** (name whichever ones
   you actually find — never promise one that isn't there), or **(c) silent**
   (type-only — rare for this style; the kinetic cards must then carry everything).
   If the user already named a tool, that's answered. See `references/pipeline.md`
   §VO for how to locate a TTS tool and what the call needs to produce.
4. **Music.** None, a track the user supplies, or a generated **instrumental bed
   via Unsora `create_music`** (`mureka-7.5`). Vox typically runs a restrained
   editorial underscore under the VO; default to a light generated bed unless the
   user says otherwise.
5. **Accent color.** The palette is one editorial base + **one** bold accent held
   across the whole film (Vox's signature is a warm yellow, but ask/confirm — red,
   cobalt, and teal all read as Vox). Locked at the gate, never drifts.
6. **Length / shape.** Infer from the script; for a bare idea, ask for a target
   runtime or shot count, or offer a beat list first.
7. **Unsora MCP availability.** Confirm the session exposes Unsora MCP tools for
   `create_image`, `wait_for_image`, `create_video`, `wait_for_video`,
   `create_music`, and `wait_for_music`. If not, stop and ask the user to connect
   Unsora MCP before generation planning continues.

---

# PART 1 — THE STYLE SYSTEM

## Rule 0 — one shot delivers one point, and the type lands it

Each shot answers *"what does the viewer now understand that they didn't a second
ago?"* — a claim, a number, a contrast, a location, a single turn in the story.
The collage shows it; the **kinetic type states it**, and the **VO explains the
why**. The three tracks complement each other — they never all say the same thing.

- *"The border moved 200 miles west"* → a torn map with a red line sliding west, a big **200 MILES** card snapping in, VO gives the year and the reason.
- *"Nobody noticed for a decade"* → a circled newspaper clipping with a magnifier, card reads **10 YEARS**, VO delivers the irony.
- *"Three companies control it all"* → three cut-out logos/buildings layering over a pie wedge, card reads **3 FIRMS · 90%**.

**Test every shot:** name the point in one clause. If you can't — if it's "a nice
photo drifting" with no claim, number, or turn — it's filler. Give it a card that
carries information, or fold it into a neighbour. A Vox explainer that shows
without telling is just B-roll.

The full visual system (medium, ground, palette, typography, motion grammar,
infographic-mark vocabulary, camera, foley, style lineage, and the AI-default
negative) is in **`references/style-dna.md`** — read it before writing a single
prompt.

## The two-prompt structure (every shot)

Each shot is two prompts, built from the `style-dna.md` templates:

- **Hero-frame prompt** (Unsora `create_image`, `nano-banana-pro`): the single
  strongest frame of the shot — its *resolved* state, with the kinetic-type card
  already set. Ordered Subject → Action → Setting → Style → Camera → Lighting →
  Text → Constraints. Full sentences, art-director voice, and it MUST carry the
  Vox medium sentence **and** the AI-default negative (flat scanned-paper
  photomontage, torn cut edges, printed halftone/newsprint grain — no gloss, no
  3D bevel, no smooth vector look).
- **Animation prompt** (Unsora `create_video`, `seedance-2.0`): animates that
  frame. Names the frame by role ("the start frame is the target composition —
  the shot resolves to it"), never re-describes its design, uses only the style's
  limited-frame motion verbs, states the cadence, and closes with the audio line
  (`No voice.` — the VO is a separate track — plus paper foley, plus `No music.`).

**Frame-zero rule:** the hero frame is usually the *end* state, so the animation
prompt must say the shot **resolves to** it (elements slide in, snap, settle,
hold), not that it "starts" there — or the motion has already happened. If a clip
opens finished, fall back to plate mode (a second, emptier hero frame as the true
first frame). Mechanics in `references/pipeline.md`.

---

# PART 2 — THE PRODUCTION PIPELINE

Never skip the approval gate. Read `references/pipeline.md` for exact Unsora
parameters and the VO handling before Phase 4.

## Phase 1 — Read the script

Accept `.docx`, `.txt`, `.md`, `.pdf`, fountain, or pasted text; read in full,
then classify: **narration script** (prose to be heard — the VO is the timing
spine), **beat list** (one point per line — one shot each), or **hybrid** (VO with
bracketed visual directions — honour the directions, time to the VO). If it's a
product/feature brief, not a script, say so and offer to write one first.

## Phase 2 — Beat map + asset tally

Apply Rule 0. Tally every recurring **character, place, and significant object**
against the shots it appears in — this feeds the reference-sheet plan (3+ shots →
sheet; the film's hero subject → sheet even at 2; recurring place → sheet;
everything else per-shot). Assign each shot a **VO line** and a provisional
duration. Segmentation rules, the narrative-arc model, the split rule, and the VO
timing table are in `references/beat-mapping.md`.

## Phase 3 — Shot list + VO draft, then stop

Present the shot list as a table and **wait for a yes**:

| # | Point / beat | Kinetic-type card | Setting / accent use | Sec | Assets | VO line |

Below the table: the **VO script** (all lines, read start to finish — this is what
gets voiced), the **asset/sheet plan** (one line each: name, type, shots, one
sentence of the locked design), then total runtime, shot count, sheet count,
orientation, accent color, VO source, and — plainly — that generating spends
**Unsora** credits for images/clips/music (plus whatever the VO tool costs, if one
is being used), and takes roughly `clips × ~7 min` (Seedance) plus a bit per sheet,
per VO line, and for the music. Do not call a single generation tool before the user says
go. If the `anti-slop` skill is available, run the VO draft through it — VO is
public-facing copy and must not read as generic AI narration.

## Phase 4 — Voiceover first (the timing spine)

Vox is narration-driven, so the VO exists **before** shots are sized. Per the
source chosen at the front door (mechanics in `references/pipeline.md` §VO):

- **Supplied file** → ask for it now, split it per beat (or read the whole file's
  duration and lay lines out against the beats).
- **Session TTS tool** → find the TTS tool actually available, audition/pick one
  voice, synthesize **one call per VO line**, hold that same voice across every
  line, and download each result to `vo/vo_NN.<ext>`.
- **No TTS available and no file** → say so before the gate, and offer the silent
  type-only cut or a picture-lock the user can narrate themselves.

Then `ffprobe` each line's real duration and **set each shot's `duration` to fit
its line** (word budget ≈ 2.4 words/sec; give ~0.3s of air at each end). One VO
segment per shot keeps timing trivial. This measured `(shot n → seconds)` table is
what Phase 6 generates against.

## Phase 5 — Write the prompts

For each approved shot, write both prompts with the `style-dna.md` templates and
show them in the per-shot format below before generating. Shots that use a sheet
get the sheet-binding lines and describe only pose/arrangement for that element —
the design lives in the sheet. Cheap to fix on the page, expensive after. Run the
`style-dna.md` checklist per shot.

**Per-shot output format:**

1. `### SHOT N — [TITLE]` + one line: the point and how this shot lands it. If it
   uses sheets, a second line: `Assets: [name → role]`.
2. **Breakdown** — duration & pacing; subject(s); action & blocking; setting &
   accent use; framing & composition; camera & movement; lighting; the
   kinetic-type card; audio; THE HERO FRAME.
3. **Hero-frame prompt** — one fenced code block.
4. **Animation prompt** — one fenced code block.

## Phase 6 — Generate (Unsora)

Read `references/pipeline.md` first. Reference sheets once each (before any shot),
then per shot: `create_image` → `wait_for_image` → `create_video` (hero URL as
`image`) → `wait_for_video`. `aspectRatio` **identical** in both calls (a ratio
mismatch crops the type card — the most common silent failure). `generateAudio:
true` for the foley bed. Pass a shot's sheet URLs in `referenceImages` of **both**
calls (slot math: in the video call `image` = @Image1, first reference = @Image2).
Do **not** chain last-frame → next-first-frame — each shot is a discrete card and
the hard cut is the edit; for a seamless join use a flood/accent-wipe transition
(see `style-dna.md`), not chaining. Keep the manifest updated so a failed shot
regenerates alone. Never re-roll a `done` shot "for consistency."

## Phase 7 — Music (optional, Unsora)

If a bed was requested: `create_music(model="mureka-7.5", prompt=<editorial
underscore, restrained, no vocals>)` → `wait_for_music` → download. `mureka-7.5`
is the instrumental model — omit lyrics. Match the brief to the film's tone
(driving for investigative, warm for human-interest). The bed rarely matches the
runtime — loop or trim it in the mix.

## Phase 8 — Assemble, time the VO, mix, deliver

ffmpeg. Concat clips in manifest order (zero-pad shot numbers). The VO is already
per-shot and each shot was sized to its line, so placement is near-trivial: lay
each `vo_NN` at its shot's start offset, mix over the clips' foley (kept low so the
paper snaps read) with the **music bed ducked under the VO** (sidechain). Verify
the final duration against the picture cut — a dropped clip yields a valid file
that's simply short. Exact ffmpeg commands, ducking, optional brand-bug overlay,
verification, and resume-after-failure are in `references/pipeline.md`. Present
the completed `final.mp4` using the host agent's native file-delivery mechanism.
Offer, but never perform unprompted, any social post — that needs its own
explicit yes (Unsora `create_post`).

## Failure handling (universal; `style-dna.md` adds style-specific rows)

| Symptom | Cause | Fix |
|---|---|---|
| Clip opens on the finished collage, nothing assembles | Prompt said "first frame" | Reword to "target composition — the shot resolves to this frame"; if persistent, plate mode |
| Look turns glossy 3D / clean flat-vector motion-graphics | The Vox AI-default leaked | Add the medium sentence + AI-default negative (scanned torn paper, halftone grain, no gloss, no vector tween) to every prompt |
| Elements glide/tween smoothly | Smooth-motion verb slipped in | Purge morph/glide/ease; state "limited frame rate, snaps between poses, no smooth interpolation" |
| Type card cropped or reflowed | Aspect ratio mismatch image↔video | Regenerate the hero frame at the video's ratio; keep `aspectRatio` identical |
| A recurring face/place looks different between shots | No sheet, or sheet not passed/bound | Generate the sheet once; pass its URL in `referenceImages` of both calls, bind it by slot in both prompts |
| Seedance invents a voice | VO leaked into the video prompt | Keep the VO out of every video prompt; restore `No voice.` — the VO is a separate track |
| Second color creeps in | Accent not held | Force the palette: editorial base + monochrome photo cut-outs + the ONE locked accent |
| "Unsora voiced it" | Unsora has no TTS | State the real source (the session's TTS tool, or the user's supplied file); never attribute the VO to Unsora |
| Assembled film is short | A clip failed and got skipped | Check the manifest, regenerate the missing shot |
| VO drifts out of sync | Shots not sized to the lines | Re-measure each `vo_NN` with `ffprobe`, set each shot's duration to its line, regenerate the mismatched clips |

## Reference files

- `references/style-dna.md` — the full Vox collage visual system: medium, ground,
  the editorial-base-plus-one-accent palette, kinetic-typography rules, the
  infographic-mark vocabulary (maps / arrows / circles / redlines / timelines /
  charts), limited-frame motion grammar, camera, foley, the accurate style
  lineage, the AI-default betrayal + its negative, both prompt templates, the
  reference-sheet formats, and the per-shot checklist. **Read before writing any
  prompt.**
- `references/pipeline.md` — exact Unsora parameters and polling (sheets, hero
  frames, clips, `create_music`, reference-slot ordering); **the VO paths**
  (supplied file, or a session TTS tool — how to find one, what to ask it for, and
  how to retrieve and download the audio); the manifest schema; every ffmpeg
  command (concat, VO timing + normalise
  + duck/mix, brand-bug overlay, verification); resume-after-failure; and the
  optional Unsora posting flow.
- `references/beat-mapping.md` — segmentation rules, the asset tally, the
  narrative-arc model, the split rule, the VO-first timing table, and a worked
  narration → shot map.
