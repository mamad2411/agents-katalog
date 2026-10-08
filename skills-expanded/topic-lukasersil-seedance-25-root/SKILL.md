---
name: seedance-25
description: "Writes production-ready Seedance 2.5 prompts for any surface (Dreamina web, CapCut Desktop, Jimeng, Doubao, ModelArk API): 30-second clips staged with explicit end states, integer-second timestamps, editing and extending finished footage, keyframes, storyboards, 3D clay-model references, and reference binding with roles and exclusions across up to 50 inputs. Use when someone wants a clip longer than 15s, more than 9 references, a prompt for Dreamina or CapCut, or wants to change something inside an already-generated shot. Triggers: 'seedance 2.5', 'thirty second clip', 'one-take', 'prompt for Dreamina', 'prompt for CapCut', 'omni reference', 'keyframes', 'extend this video'. Note on resolution: 2.5 runs at 480p and 720p only, never 1080p or 4K; that is Seedance 2.0 at 15s. It writes the prompt and the settings block; it does not generate, and it is not for timeline editing, captions, or export."
license: MIT
user-invocable: true
tags: [seedance, video, prompting, dreamina, capcut]
---

# seedance-25

`v2.0.0` · 2026-08-09 · MIT · see `ATTRIBUTION.md`

Prompt engineering for **Seedance 2.5 on any surface**. The deliverable is always a copy-paste prompt
plus the settings block the operator sets, whether that surface is a web UI, a desktop app, or an agent.
This skill writes prompts. It does not generate, upload, or send anything.

## What this skill is

Seedance 2.5 doubled the clip length and more than tripled the reference budget. Both changes reward
people who write like a director and punish people who write like they are filling in a search box.
More room does not mean you can be vaguer. It means there are more places to go wrong before you find
out, and you only find out after the render finishes.

This skill is the discipline that keeps that from happening.

| File | What it holds |
|---|---|
| `SKILL.md` (this one) | step 0, beat architecture, reference binding, output contract, checklist |
| `references/official-spec.md` | **the official contract: locked/unlocked tasks, `content.role`, trigger words, timestamps, task catalogue, reference budgets** |
| `references/craft-essentials.md` | the prompt spine, camera and light vocabulary, audio budget, anti-slop, IP gate |
| `references/surface-profiles.md` | what each surface supports, settings blocks, evidence grades |
| `references/beat-templates.md` | four ready skeletons for common jobs |
| `references/modes-and-workflows.md` | Extension, Smart Edit, First & Last Frame, keyframes, storyboards, clay models, building reference images |
| `references/proven-fixes.md` | verbatim repair lines, audio tag syntax, languages, reference sweet spots |

This skill is **self-contained**. It does not depend on any other skill being installed.

**Precedence when files disagree:** `official-spec.md` → `surface-profiles.md` → everything else.
The first stands on ByteDance documentation published 2026-08-07; several other files were originally
written from practitioner reports. Where they conflict, the documentation wins, and the other file
should already say so. If you find a contradiction that has not been reconciled, say so out loud
rather than picking one.

## Evidence grading, and why it exists

Seedance 2.5 was announced **2026-07-31** and documented **2026-08-07**. A lot of what is written
about it online is still launch-window reporting or vendor marketing. Every factual claim in this
skill carries a label:

| Label | Meaning |
|---|---|
| `[official]` | BytePlus/Volcengine documentation or a ByteDance product page |
| `[press]` | trade reporting |
| `[community]` | a practitioner who actually shipped with it, named and dated |
| `[verified-live]` | checked directly against a running surface on the date given |
| `[unverified]` | waiting on a first real run |

**Never state an unlabeled number as fact.** If a value is not confirmed for the surface in play,
write it into the settings block with `(verify in UI)` next to it. Guessing a resolution or a
reference ceiling is how a client gets promised something the tool cannot do.

`[community]` is usable as a working method. It is not usable as a claim in a client deck or a
sponsored post.

## Step 0: identify the surface. Always.

**Without a surface there is no settings block and half the limits are invented.** 2.5 runs on
several products. Each has a different UI, different tag syntax, different resolutions, and different
feature availability. Before writing a single sentence:

1. Ask where the prompt is going. Do not default.
2. Load that surface's profile from `references/surface-profiles.md`.
3. If the surface is not in the profiles, use the **conservative profile** (also in that file), mark
   unverified values as unverified, and say out loud that the profile is conservative. Never carry a
   limit from one surface to another, not even between two ByteDance products.

**Hard dividing line:** 30 seconds in one generation and 50 references is **Seedance 2.5**. Seedance
2.0 is still 4-15 seconds and 9 images / 3 videos / 3 audio. Never write "Seedance 2.0 now does 30
seconds." It is wrong and it is the single most common mistake made about this model.

**Second hard line, and it is new:** `[official 2026-08-09]` **Seedance 2.5 runs at 480p and 720p
only. It does not do 1080p and it does not do 4K. Anywhere.** Not on Magnific, not on Higgsfield, not
in CapCut, not in Dreamina, not through the API. This is a property of the model, not a limitation of
a surface. **Only Seedance 2.0 reaches 4K**, and it does so at 15 seconds. Earlier versions of this
skill said the opposite and told people to go to CapCut for higher resolution. There is nothing there
either.

The model ID is public: **`dreamina-seedance-2-5-260628`** (480p/720p, 4-30s, 24 fps, mp4 and mov).
The API is not enterprise-only; the individual tier allows 180 RPM and a concurrency of 3. Full model
card, rate limits, and pricing are in `references/surface-profiles.md`.

**Thirty seconds is the documented ceiling for one generation.** Video Extension is real and
documented, but the official docs give **no ceiling for the final cut**, and the 60s figure is
community-reported. Ultra-Long mode does not appear in the documentation at all, and the model card
says 4-30s. When someone asks for longer than thirty seconds, load
`references/modes-and-workflows.md` and offer Extension, and **when quoting any number above 30
seconds, say that it is a community claim the official model card contradicts.**

**The trade is length against resolution.** A client master at 1080p or 4K is Seedance 2.0 at 15
seconds, with no exceptions. Length, a large reference budget, timestamps, or editing finished
footage is 2.5 at 720p. Say which one you are on before you hand over the prompt, not after the
render.

## Model invariants

Do not take these from a UI. They are properties of the model:

- **Prompt spine:** subject → action → camera → light and setting → style → sound. The official
  macro-structure wraps it in four blocks (asset referencing → one-sentence summary → detailed plot →
  additional notes), see `official-spec.md` section 4.
- **At 30 seconds only one slot changes:** the action holds a short arc, not a single motion.
- **Write in stages, not one paragraph.** One primary change per stage and an explicit `End state:`
  for each. That end state is the anchor the next stage attaches to.
- **Timestamps work, but only on 2.5.** Integer seconds, no gaps in the timeline, never for
  high-frequency actions. Seedance 2.0 ignores them entirely and understands only shot numbers. `[official]`
- **Locked tasks set their own aspect ratio and duration.** Editing, first/last frame, and extension
  inherit those from the input asset, so there is nothing to ask the operator about. `[official]`
- **Time windows are budgets, not frame-exact cuts.** Underfeeding a beat does not trim it, it rushes it.
- **Pin the constants once at the top** and **restate them once at the bottom** as a consistency line.
- **The audio budget does not scale with duration.** The limit is per line and per breath, not per clip.
  A 30-second clip is room for more lines, not permission for longer ones.
- **An unbound reference blurs the result.** One dimension, one owner, exclusions written out.
- **Positive description is preferred.** Negatives are officially supported only for subtitles and
  audio, not for visuals. `[official]`
- **Emotion is described through visible signals**, never named. Never "she is sad."
- **Anti-slop applies everywhere.** A specific lens, a specific movement, a specific light source.

Always surface-specific and resolved from the profile: tag syntax, reference ceiling, available
resolutions, aspect ratios, whether duration is continuous or a fixed set, whether audio references
exist, whether Extension and region-level editing are present, and what any of it is called in the UI.

## Beat architecture for 30 seconds

ByteDance's own guidance splits 30 seconds into four beats. Treat it as the default skeleton, not
dogma. It holds on every surface because it is a property of the model, not the UI:

| Beat | Window | Function | Typical shot |
|---|---|---|---|
| 1 | 00-06s | exposition, establishing the world | wide establishing |
| 2 | 06-14s | development, the action enters | medium to detail in action |
| 3 | 14-24s | escalation | moving shot or insert |
| 4 | 24-30s | resolution, callback | detail that returns to beat 1 |

The rules that hold it together:

1. **One arc, not four ideas.** Beats are phases of a single thought. If every beat introduces a new
   subject, the model glues them into a trailer collage.
2. **The callback in beat four is not decoration.** Returning to an object or gesture from beat 1 is
   what gives a 30-second clip closure instead of an ending that just stops.
3. **Roughly 4-6 seconds per beat is comfort, not a ceiling.** Four beats sit well in 30 seconds.
   **So do eight and nine.** The official 30-second examples in ByteDance's own documentation run 8
   and 9 shots at 2-4 seconds each `[official 2026-08-07]`. The earlier "seven is the ceiling, eight
   compresses" line in this skill was a guess and is withdrawn. What breaks a beat is **too much plot
   inside its window**, not the number of windows. When in doubt, add a window and take something out
   of each, rather than forcing two changes into one.
4. **Pin the constants once, at the top.** Subject description, wardrobe, props, lighting mode, and
   grade get stated once and declared to hold for the whole clip. Repeating them in every beat is
   filler, but never stating them at all is the most common cause of drift at 30 seconds.
5. **The end of a beat is a completed action.** A beat's sentence lands on impact and the next beat
   opens something new. Otherwise the cut falls in the middle of a movement.
6. **Every beat gets an `End state:`.** The beat describes what happens, the end state says where it
   should land. Without it, stages blur and the model invents the join. This is the cheapest edit
   with the largest effect on a 30-second clip.

Both at once, the beat as dramaturgy and the end state as a machine anchor:

```
[0-8s] A florist trims stems behind a workbench.
End state: she holds the finished bouquet in her left hand.

[8-16s] She wraps it in kraft paper and ties a green ribbon.
End state: the wrapped bouquet lies centered on the workbench.

Keep her identity, clothing, and the workbench layout consistent throughout.
No subtitles, no background music.
```

Skeletons and worked examples: `references/beat-templates.md`. Longer formats, extension, and editing
finished footage: `references/modes-and-workflows.md`.

## Reference binding

An unbound reference is a reference that blurs. Every asset gets one primary role and an explicit
exclusion. **Tag syntax is surface-specific** (`@Image1` in most UIs, a `references[]` array in an
API), the rules are the same everywhere:

```
@Image1 defines the main character's identity: face, hair, wardrobe. Do not take background or composition.
@Image2 defines the location and colour palette. Do not take any person.
@Video1 defines camera motion and pacing only. Do not take appearance, wardrobe, or location.
@Audio1 is the music bed. Beat 3 lands on the drop.
```

Hard rules:

- **One dimension, one owner.** Identity, motion, camera, environment, timing, style. If two assets
  control the same dimension, the model averages them and you get neither.
- **Exclusions are written, not assumed.** "Motion only, no appearance" is a functional part of the
  prompt, not a comment.
- **50 slots is a trap as much as a feature.** Thirty unlabeled images are thirty ways to average your
  subject into mush. More slots raise the ceiling on *role separation*, not on dumping.
- **The quality band sits far below the ceiling.** `[official]` 1-8 distinct subjects from images
  (stretch 9-12), 1-5 from video (stretch 6-10), donor clips 5-10 seconds, edit sources ≤20 seconds,
  1-5 reference images for an edit. Past those numbers it turns into a slot machine. Full table in
  `references/official-spec.md` section 8.
- **Multi-view inputs are allowed on 2.5** `[official]` and not on 2.0. Up to 5 subjects, multi-view
  is fine. Above 5, prefer one view per subject and split extra angles into **separate images**. One
  image holding several viewpoints is wrong in every case; the model reads it as one composition.
- **A tag's number is its upload order** `[official]`, not the order it appears in the prompt.
- **Mapping does not go inside the picture.** `[official]` Writing a character's name onto their
  reference image and then using that name in the prompt is a documented route to character confusion
  and duplication. Bind in the text.
- **When a reference is accurate, do not describe the scene again.** `[official]` "Strictly refer to
  the actions and camera movements in Video 1" is enough; spelling out its contents makes it worse.
- **Tags are never translated or renumbered.** Preserve exactly the shape the surface or the operator
  supplies. **But there is no single shape:** the official documentation uses `@Image 1` with a space,
  `[Video 1]`, `<video1>`, and `Images 1-2`. The earlier "no spaces" rule in this skill was invented
  and is withdrawn.
- **An asset that owns nothing gets dropped.**
- **The ceiling is surface-specific.** The model does 50: 30 images (up to 4K each), 10 videos
  **≤30s combined**, and 10 audio clips **≤30s combined** `[official]`. A given UI may allow fewer.

**Group ranges are official** `[official]`: `Use Images 1 to 7 in order as keyframes.` and
`Images 1-2 are Character 1 and correspond to Audio 1; Images 3-4 are Character 2 and correspond to
Audio 2.` A group still needs one role and one exclusion, stated once for the group.

**The tag `@ClayRender1` does not exist and never did.** It was invented in an earlier version of this
skill. 3D clay-model reference is a real, documented task, but it binds with an ordinary `[Video 1]`
plus a sentence naming what is taken from it: *"Refer to the camera movement and motion in [Video 1]."*
See `references/official-spec.md` section 10.

## Output contract

Deliver the same shape every time so the operator can paste and go:

1. **The final prompt, in English.**
2. **A settings block**, because the prompt alone does not determine the clip. Fields come from the
   surface profile and the heading carries the surface name:
   ```
   --- SETTINGS: {surface} ---
   Mode: {from profile}
   Model: Seedance 2.5
   Duration: 30s        (locked tasks: inherited from the source)
   Aspect: 16:9         (locked tasks: adaptive, inherited from the source)
   Resolution: 720p     (2.5 does not go higher)
   Format: mp4          (editing and extension: mov)
   References: @Image 1 = ..., @Video 1 = ...
   ```
   Any value the profile has not confirmed goes in with `(verify in UI)`. Do not invent it. On the API,
   add `content.role` per asset plus `ratio` and `duration` according to the task type.
3. **State the resolution before anyone asks.** 2.5 is 480p or 720p, full stop. If the prompt is aimed
   at a 1080p or 4K master, say so and let the operator choose: **2.5 for length, references, and
   timestamps at 720p, or 2.0 for 15 seconds at 4K.** Never hand over a 720p render as if it were what
   was ordered.
4. **Do not silently run it.** Magnific and Higgsfield can generate 2.5 through an agent
   `[verified-live 2026-08-07]`, but generation costs credits and is the operator's decision. On
   Higgsfield, 2.5 also has no keyframes, so anything built on a start/end frame stays on 2.0 or goes
   manual.

## Procedure

1. **Identify the surface.** Step 0. Load the profile, resolve limits and syntax.
2. **Pick the task and establish whether it is locked.** `[official]` This comes **before** asking
   about aspect ratio and duration, because on a locked task there is nothing to ask:

   | Situation | Task | Locked? |
   |---|---|---|
   | no assets | text to video | no |
   | one starting image | image to video / first frame | **yes**, ratio from the frame |
   | locked opening and closing image | First & Last Frame | **yes**, ratio from the first frame |
   | several assets with roles | Omni Reference / reference-to-video | no |
   | output must match a board shot for shot | **Keyframe reference** | no |
   | loose guide, rough plot only | **Storyboard reference** (≤15 panels, line art) | no |
   | a coarse 3D blockout carries motion and camera | **3D clay-model reference** | no |
   | changing something inside finished footage | **Editing** (Smart Edit) | **yes**, ratio **and** duration |
   | extending existing material | **Extension** | **yes**, ratio from the source |
   | joining two finished clips | **Seamless transition** | from the sources |

   **Keyframes versus storyboard is the choice people get wrong most often.** A storyboard is loose
   and the output will not follow it panel for panel. Keyframes are strict. When a client wants their
   board reproduced exactly, that is keyframes. Full catalogue: `references/official-spec.md` section 7.
3. **Establish intent and format.** What the clip is for and where it is going. **On unlocked tasks,
   always ask for aspect ratio and duration** and never default them; the ratio can be anything
   between 0.4 and 2.5 `[official]`, so you are not stuck with 2.0's six fixed values. **On locked
   tasks, do not ask.** Just state what is inherited from the input.
4. **On locked tasks, set the parameters and put a trigger word in the prompt.** `[official]`
   `ratio = adaptive` on all three, plus `duration = -1` for editing, plus `output_format = mov` for
   editing and extension. Editing needs `add` / `remove` / `replace` / `change to` / `modify` in the
   prompt; extension needs `continue` / `extend forward` / `extend backward`. **Without that word the
   model cannot tell which task you mean.** With more than one input video, name the specific one or
   the model chooses for you. For extension and editing, load `references/modes-and-workflows.md`.
5. **Safety gate.** A real face, a third-party brand, a public figure, a protected character: resolve
   it through the IP gate in `references/craft-essentials.md` before writing the first sentence.
6. **Build the beats.** One arc, callback at the end, `End state:` on each. Four windows is a
   comfortable default; eight or nine is equally fine. On 2.5, write **integer-second timestamps with
   no gaps in the timeline**.
7. **Pin the constants.** Subject, wardrobe, light, grade, ambience. Once at the top, restated once
   at the bottom.
8. **Bind the references.** A role and an exclusion for every tag, numbered by upload order. If the
   references do not exist yet, **build them before writing the prompt**
   (`modes-and-workflows.md` section 6): lock one look, generate by category, build reference sheets
   for anything recurring, then leave them alone.
9. **Run anti-slop.** `references/craft-essentials.md`. No "cinematic", "stunning", "breathtaking",
   "ethereal", "glow", "majestic".
10. **Deliver per the output contract.** Prompt, then settings block with the surface named.
11. **Say draft-first out loud.** At 30 seconds a bad take costs double. Test the look on a short
    clip, then commit the length.

## Pre-flight checklist

- [ ] Surface identified, profile loaded, unconfirmed values marked `(verify in UI)`
- [ ] **Resolution matches the model: 2.5 is 480p or 720p. If the client wants 1080p or 4K, that is 2.0 at 15s**
- [ ] Established whether the task is locked or unlocked
- [ ] Unlocked: aspect ratio and duration confirmed by the operator, not guessed (ratio 0.4 to 2.5)
- [ ] Locked: `ratio = adaptive`, plus `duration = -1` for editing, plus `output_format = mov` for editing and extension
- [ ] Editing or extension carries a **trigger word**, and the specific video is named when there is more than one
- [ ] Mode matches the assets and is named the way that surface names it
- [ ] Strictness matches the brief: keyframes when the output must match exactly, storyboard when a loose guide will do
- [ ] Reference ceiling matches the surface, not the model maximum
- [ ] Videos total ≤30s and audio totals ≤30s, not merely each clip under the limit
- [ ] Every tag has a role **and** an exclusion, numbered by upload order
- [ ] Mapping lives in the text, not written inside the images
- [ ] No dimension has two owners
- [ ] References inside the quality band (1-8 image subjects, 1-5 from video, clips 5-10s), not merely under the ceiling
- [ ] Subject and main action stated plainly, without ornament
- [ ] Constants stated once at the top **and restated at the bottom**
- [ ] Every stage has one primary change and an explicit `End state:`
- [ ] The timeline is continuous, with no gaps between windows
- [ ] Character count, wardrobe, and prop ownership consistent across stages
- [ ] The final beat contains a callback
- [ ] Lines are short, one thought per breath
- [ ] Emotion written as visible signals, not named
- [ ] Actions described generally, only a few detailed, none repeated
- [ ] Negatives limited to subtitles and audio; visuals described positively
- [ ] Forbidden items listed at the end (subtitles, background music, morphing, extra characters)
- [ ] If the track must be clean: a `[SOUND]` directive, not just "no music"
- [ ] On-screen text carries a language directive wherever text appears
- [ ] Prompt passed anti-slop
- [ ] IP and likenesses clean or authorized
- [ ] Settings block attached

The exact wording of the repair lines referenced above lives in `references/proven-fixes.md`. Paste
them as written. A reworded line is a different prompt.

## Two notes on talking about this model publicly

**Do not oversell it on the vendor's behalf.** ByteDance's own documentation states that 2.5 is *not*
a generational leap over 2.0 in the way 2.0 was over 1.5, and describes it as a systematic hardening
for production work. When the vendor is that measured, inflating it in a post is a risk with no upside
and it is trivially checkable. If you are writing sponsored or ambassador content, that applies twice,
alongside the usual disclosure and verifiable-claims discipline.

**ByteDance publishes its own prompting skill for 2.5** (`/sd25-pe`, installed via `npx skills`, see
`references/official-spec.md` section 12). This skill is not the only option and should not be
presented as one. Installing theirs is the operator's call.
