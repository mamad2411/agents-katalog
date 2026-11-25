---
name: story-production-pipeline
description: >
  Reusable end-to-end pipeline that turns any story premise into a finished AI video via
  Higgsfield. Runs eight stages: Intake → Concept Lock → Beat Sheet → Script → Shot List →
  Cast & Look Lock → Generation → Assembly. Weighted heavily toward concept and beat work,
  because a weak beat sheet cannot be rescued by good renders. Genre-agnostic and
  runtime-adaptive (15s micro to 12min standard to episodic series). Every project persists
  as a single STORY.md so any later session can resume mid-pipeline instead of restarting.
  Use this skill whenever the user wants to build a story, write a narrative script, break a
  story into beats, build a shot list, turn a script into video, or produce narrative video
  content in Higgsfield — including phrases like 'help me write this story', 'break this into
  beats', 'turn this script into a video', 'make a story video', 'I have an idea for a short
  film', 'build the shot list', 'resume my story project', or any request that starts from a
  premise and needs to end as moving picture.
---

# Story Production Pipeline

Eight stages, one persistent file, resumable at any point.

```
0 INTAKE        →  constraints, runtime, audience
1 CONCEPT LOCK  →  logline, dramatic question, want vs need
2 BEAT SHEET    →  the spine — most of the work happens here
3 SCRIPT        →  timed narration + dialogue
4 SHOT LIST     →  beats become shots with camera language
5 CAST & LOOK   →  continuity locked before a single render
6 GENERATION    →  keyframes → video → audio
7 ASSEMBLY      →  edit order, timings, delivery manifest
```

**The controlling principle:** every stage downstream of the beat sheet is execution. If the
beats are flat, the renders will be beautiful and the video will still be boring. So resist
the pull toward generation — the user will feel it too, because generating is the fun part.
Hold the line at Stage 2 until the beat sheet passes its quality gates.

**Never skip forward on assumption.** If the user says "just make the video," run the earlier
stages fast and compressed rather than skipping them. A 90-second concept pass still beats
none.

---

## The persistent artifact: STORY.md

Everything lives in one file per project. This is what makes the pipeline reusable rather
than a one-time conversation — a session three weeks later can read `STORY.md` and know
exactly where things stand.

Create it at Stage 0 from `assets/STORY-template.md`. Update it at the end of every stage.
Never keep pipeline state only in conversation.

Structure:

```
STORY.md
├── 00 META          project name, runtime target, status, last stage completed
├── 01 CONCEPT       logline, dramatic question, want/need, stakes, ending type
├── 02 BEATS         numbered beat table
├── 03 SCRIPT        timed script
├── 04 SHOTS         numbered shot table with prompt seeds
├── 05 CAST & LOOK   character sheets, palette, lens grammar, Higgsfield element IDs
├── 06 RENDERS       job IDs, URLs, accept/reject status per shot
└── 07 ASSEMBLY      edit order, audio map, deliverables
```

If the user already has a script or partial material, parse it into the relevant sections and
enter the pipeline at the matching stage. Tell them which stage you're entering and what's
missing.

---

## Stage 0 — Intake

Ask via `ask_user_input_v0` with tappable options. Keep it to one round. Infer everything you
can from what they've already said rather than asking again.

Four things you actually need:

➠ **Runtime tier** — Micro (15–60s) · Short (1–4min) · Standard (5–12min) · Episodic
➠ **Story shape** — Single protagonist arc · Two-hander · Ensemble · Voice-over essay
➠ **Delivery format** — 9:16 vertical · 16:9 horizontal · 1:1 square
➠ **Register** — where on the scale from grounded realism to full stylization

Everything else (genre, setting, character names) either comes from the premise or gets
proposed by you and confirmed. Don't interrogate. A user with a half-formed idea needs you to
make concrete proposals they can react to, not a form to fill out.

Write META into STORY.md, then move.

---

## Stage 1 — Concept Lock

The purpose here is to find out whether there is a story at all, before spending effort on
structure. Most premises are situations, not stories. A situation is "a man discovers his
neighbor is a thief." A story is "a man discovers his neighbor is a thief, and reporting him
means losing the only person who checks on his mother."

Produce these six, in this order:

**1. Logline** — one sentence, under 30 words, containing protagonist, want, obstacle, stakes.
No adjectives doing the work. If the logline needs a second sentence to make sense, the
concept isn't locked.

**2. Dramatic question** — the yes/no question the audience carries. "Will she get the
package to the border before dawn?" The whole video is the delay of this answer.

**3. Want vs Need** — what the protagonist is chasing versus what the story will teach them
they actually required. These must be in tension. If want and need point the same direction,
there's no arc, only errands.

**4. Stakes ladder** — three rungs: what's lost at minimum, what's lost at worst, what's lost
that can never be recovered. The third rung is what makes an ending land.

**5. Central image** — one visual that could carry the entire story on a thumbnail. This
serves double duty later as your key art and your first Higgsfield keyframe.

**6. Ending type** — chosen deliberately from: earned win · costly win · meaningful loss ·
ironic reversal · open question. Choose now, because every beat is engineered backward from
this. Changing it at Stage 5 means rebuilding the beat sheet.

### Concept gate

Before proceeding, check honestly:

➠ Can the dramatic question be answered no? If not, there's no tension.
➠ Does the protagonist make the decisive choice, or does the world resolve it for them?
  Protagonist agency is non-negotiable — audiences forgive plot holes, not passivity.
➠ Is there a version of this premise 30% stranger? Propose it. Users often anchor on their
  first idea and are glad to be pushed.

Present the six items and the gate findings, get confirmation, write to STORY.md.

---

## Stage 2 — Beat Sheet

This is the stage that matters. Everything else is craft; this is architecture.

Load `references/beat-templates.md` and select the template matching the runtime tier from
Stage 0. Do not use a 12-beat structure on a 45-second video — the beats will be four seconds
each and nothing will breathe.

### Beat fields

Every beat carries all six. A beat missing any of these is not finished:

| Field | What it captures |
|---|---|
| **Event** | What physically happens on screen. Concrete, filmable, no interiority. |
| **Function** | Why this beat exists structurally. If you can't name it, cut the beat. |
| **Charge** | Value state at beat's end: + (better) or − (worse) for the protagonist. |
| **Delta** | Emotional shift the audience makes: *curious → uneasy*, *hopeful → gutted*. |
| **Duration** | Seconds. Must sum to the runtime target ±10%. |
| **Shots** | Rough count, ~1 shot per 4–8s. Feeds Stage 4 directly. |

### The four gates

Run every beat sheet through these before showing it. Fix failures rather than reporting
them — the user wants a working spine, not a critique.

**Alternation gate.** No three consecutive beats share the same charge. Continuous + reads as
smug, continuous − reads as misery, and both flatten. If beats 4, 5, 6 are all −, one of them
is doing nothing and should either be cut or inverted.

**Change gate.** Every beat ends with the situation materially different than it started. Ask
of each: what is now true that wasn't true 20 seconds ago? "They talk about the plan" fails.
"They agree on the plan and burn the map" passes.

**Agency gate.** The protagonist makes an active choice in at least a third of beats, and
always in the climax beat. Count them. If the count is low, find the beats where the world
acts on the protagonist and rewrite them so the protagonist acts first.

**Removal gate.** For each beat, ask whether the next beat still makes sense if this one is
deleted. If yes, the beat is decoration. Cut it and give the seconds to the climax — short-form
video almost always underweights the climax and overweights setup.

### Output format

Present as a table, then the gate report:

```
| # | Beat | Event | Fn | Chg | Delta | Sec | Shots |
```

Follow with two or three lines on what the gates changed. Then ask one question: whether any
beat feels wrong. Beat sheets are cheap to revise and expensive to regret.

Write to STORY.md section 02.

---

## Stage 3 — Script

Convert beats to timed script. Load the `anti-ai-slop-writing` skill before writing any
narration or dialogue — story voice is exactly where generated text betrays itself, and the
user's standing writing bans apply here.

Format per beat:

```
[BEAT 3 — 0:24–0:41 — "The offer"]

VO:      (or) CHARACTER:
         Line.

ON SCREEN:   what we see while that line runs
SOUND:       key effect or score cue
```

Rules that matter for AI-generated video specifically:

➠ **Read it aloud and time it.** ~150 words per minute for narration, faster for dialogue.
  If the script overruns the beat duration, cut words, don't stretch shots — pacing problems
  are almost never solved by longer shots.
➠ **Dialogue does not explain the plot.** Characters want things from each other. If a line
  exists to inform the audience, either cut it or bury it under conflict.
➠ **Leave silence.** Generated video reads as artificial partly because everything is filled.
  Mark at least two deliberate silent stretches.
➠ **Write for the voice you'll actually use.** Check `list_voices` before finalizing narration
  register — writing a gravelly world-weary VO and then discovering the voice bank is all
  bright and clean wastes a pass.

Write to STORY.md section 03.

---

## Stage 4 — Shot List

Load `references/prompt-grammar.md`. Break each beat into its shot count from Stage 2.

Every shot row:

```
| Shot | Beat | Dur | Size | Move | Subject/Action | Light | Continuity tags |
```

**Size** — from extreme wide to extreme close. **Move** — static, push, pull, pan, handheld,
crane. Vary deliberately; a sequence of all-static shots reads as a slideshow and a sequence
of all-moving shots reads as chaos.

Two structural habits that carry a story:

➠ **Coverage rhythm.** Establish wide, play the scene in mediums, punch to close on the
  emotional turn. When you break this pattern, break it because the beat earns it.
➠ **Reserve your closest shot.** Whatever your tightest framing is, use it once, at the
  climax. Spending it in beat 2 costs you the ending.

The continuity tags column is what makes Stage 5 work — tag every shot with the characters,
locations, and props it contains, so recurring elements get registered before generation.

Write to STORY.md section 04.

---

## Stage 5 — Cast & Look Lock

**Do this before generating a single final shot.** The single largest failure mode in AI story
video is a protagonist whose face changes between shots. It is unfixable in post and it
destroys the story's credibility instantly.

Load `references/higgsfield-ops.md` for exact call sequences.

The sequence:

1. Pull the unique entities from your continuity tags — every recurring character, location,
   and hero prop.
2. Check what already exists via `show_reference_elements` and `show_characters`. Reuse
   before creating.
3. For each recurring character, generate a clean reference frame, then register it as a
   reusable element or Soul Character. Characters appearing in more than three shots always
   get registered.
4. Lock the look sheet: palette (3–5 colors), lens grammar, lighting logic, grain/texture,
   and one "never" rule that keeps the style honest.
5. Run a two-shot consistency test before committing to the full batch. Generate the same
   character in two different framings. If the face drifts, fix it here — regenerating 40
   shots later is expensive in credits and time.

Write element IDs into STORY.md section 05. These IDs are the reusability payload — the next
project in the same world reuses them directly.

---

## Stage 6 — Generation

Check `balance` first and estimate cost before firing. Report the estimate to the user and
get a go-ahead. Never surprise someone with a credit burn.

Order of operations:

**Keyframes first.** Generate a still for each shot via `generate_image_batch`. Stills are
cheaper and faster than video, so this is where you catch composition and continuity problems.
Present the keyframe contact sheet for approval before any video generation.

**Then image-to-video.** Approved keyframes drive `generate_video_batch`. Batch by scene, not
by whole film — the user should be able to stop after any batch. Use `jobs_wait` to poll
without opening widgets.

**Then audio.** Narration via `generate_audio` with the voice chosen at Stage 3. Keep one
voice per character across the whole project; note the voice ID in STORY.md.

Log every job ID and output URL into STORY.md section 06 with accept/reject status as you go.
This is the difference between a resumable project and a lost one.

Regeneration policy: give any failed shot two attempts with prompt adjustments. On the third
failure, the shot is fighting the model — change the shot rather than the prompt. Reframe it,
cut it, or replace it with a different angle on the same beat.

---

## Stage 7 — Assembly

Produce the handoff, not the edit:

➠ **Edit order** — numbered shot sequence with in/out timings against the script
➠ **Audio map** — narration, dialogue, and sound cues placed against the timeline
➠ **Deliverables** — every asset URL grouped by shot, plus key art from the central image
➠ **Gap list** — anything unrendered or rejected, stated plainly

Then a short retro: which beats survived unchanged, which shots needed the most attempts,
what to carry into the next project. Write it into STORY.md — this is how the pipeline gets
better with each story rather than starting cold.

---

## Resuming a project

When the user returns with an existing STORY.md, or says "continue the story project":

1. Read STORY.md.
2. State the last completed stage and what's next in one line.
3. Resume. Don't re-confirm decisions already locked unless the user raises them.

If they want to change something upstream — a new ending at Stage 6, for instance — say
plainly what it invalidates downstream and let them decide. Changing the ending type
invalidates the beat sheet. Changing a character's look invalidates rendered shots.

---

## Reference files

➠ `references/beat-templates.md` — beat structures by runtime tier and story shape. Load at
  Stage 2, always.
➠ `references/prompt-grammar.md` — shot prompt construction, camera vocabulary, continuity
  syntax, negative constraints. Load at Stage 4 and keep for Stage 6.
➠ `references/higgsfield-ops.md` — exact MCP call sequences, element registration, batching,
  cost estimation, failure handling. Load at Stage 5.
➠ `assets/STORY-template.md` — copy at Stage 0 to start any new project.
