---
name: character-continuity
description: Guides character and continuity consistency across the shots of an AI-generated film, so a character looks like the same person in every shot. Should be used when planning or producing a multi-shot film, series, ad or music video that features a recurring character, and when diagnosing a face that has drifted, wardrobe that changed between shots, blending between two characters in one frame, or deciding whether a damaged shot should be repaired or regenerated.
license: CC-BY-4.0
version: 0.2.0
---

# Character & Continuity Bible

## Two principles

**Consistency is a workflow.** No current tool guarantees frame-identical continuity; every model is probabilistic. What separates professional output from amateur output is whether the production locked its assets before generating, and changed one variable at a time afterwards.

**Invariance beats fidelity.** A slightly imperfect face that never changes will pass. A better face that shifts between shots will not. Cast something you can hold.

---

## 1. Cast before you shoot

Casting produces four assets per character, all created before a single shot exists.

### The canon frame

One approved master image. Once approved, **never regenerate it**. Everything else descends from it.

- Front-facing, neutral expression, mouth closed, eyes to camera
- Even, soft, neutral lighting. No dramatic key, no colour cast — dramatic light bakes shadow into the identity and poisons every downstream shot
- Clean background, minimum 1024px short side [PRACTITIONER: a working floor, not a documented threshold]
- Head and shoulders with headroom, not a tight crop. Models need the jaw-to-shoulder relationship

For an invented character, generate 10–20 candidates and cast deliberately [PRACTITIONER: the number is judgement, not measurement — cast until one is distinctive, however many that takes]. **Judge on distinctiveness, not beauty.** A face with a specific feature — a broken nose, heavy brows, deep-set eyes, a gap tooth — appears to hold better than a conventionally attractive average face, which regresses toward the model's mean face under pressure. [PRACTITIONER: consistent with how regression-to-mean works, but I know of no formal measurement. It costs nothing to test on your own material.]

### The turnaround set

One image per angle: front, 3/4 left, 3/4 right, profile left, profile right, back. Add a full-length T-pose for costume work.

**Never combine angles into one composite sheet.** Composite sheets cause bleed between panels. Every turnaround is generated *from* the canon frame, not prompted fresh.

### The detail plates

Close-ups of every small identity-bearing mark, because these get silently reinvented at full-body scale: scars, tattoos, birthmarks, freckle patterns, jewellery, hairline from two angles, signature costume details.

### The locked identity block

Text is the most portable asset — it travels between tools where images do not. See `references/prompt-blocks.md` for the template. This block is pasted **verbatim and unchanged** into every prompt for the rest of the production.

Critically, it ends by declaring what is locked and what is free. Telling the model where it may improvise and where it may not is a technique in itself.

### Sequence

1. Approve the canon frame
2. Generate the turnaround set from it
3. Generate the detail plates
4. Write the locked identity block
5. **Generate one test still in the film's actual lighting and lens**
6. Begin production

Step 5 gets skipped constantly and causes most disasters. A face that holds under neutral studio light can dissolve under a hard side key at 85mm.

---

## 2. Pick the right identity mechanism

Most professional pipelines combine two or three. Full per-tool detail, parameters and failure modes: `references/tool-matrix.md`.

Quick routing:

| Situation | Reach for |
|---|---|
| Character across many environments | Veo 3.1 ingredients, Runway Gen-4 references |
| Two characters physically interacting | Kling Elements |
| Dialogue performance, one character at a time | Runway Act-Two, Kling facial motion control |
| Stills and key art | Midjourney omni-reference, paired with a style reference |
| Likeness of a real person | Higgsfield Soul ID, Sora 2 Characters |
| Swapping identity onto an existing performance | Luma Ray3 character reference |
| Recurring IP needing text-only recall | Character LoRA |
| Facial lock inside an open pipeline | PuLID on Flux, InstantID on SDXL |

Before designing a sequence, check whether your tool lets you combine identity references with first/last-frame conditioning — several do not, and the workflow below is structured so you do not need them to.

### If your tool has no image input at all

Some pipelines are text-to-video only — no reference images, no first frame. Plenty of MCP servers and API wrappers expose only a text endpoint. **Say so up front rather than pretending the method still fully applies.**

What still works, and is worth doing:

- The **locked identity block**, pasted verbatim into every prompt. This is the single highest-value technique available to you
- **Distinctive casting**, expressed in text — specific, unusual features rather than attractive generic ones
- The **scene block** and **negative lists**
- **Fixed seed**, where the tool exposes one
- **One action per clip**, short durations
- The **continuity sheet** — it tracks your decisions, not the tool's capabilities
- The **audit script** — it samples finished output, so it works regardless of how that output was made

What is simply unavailable: the canon frame, turnarounds, detail plates, setup frames, and last-frame chaining. All of those require an image input.

**Be realistic about the ceiling.** Text conditioning alone is the weakest lever in this document, and the A/B test in the repo README demonstrates the failure directly: three text-only prompts describing the same woman produced three visibly different people. A disciplined identity block narrows that gap. It does not close it.

So, in order of preference:

1. **Get an image input.** Even a tool that only accepts a first frame changes the outcome more than any prompt engineering will. This is worth switching tools for
2. If you are stuck with text-only, **generate several candidates per shot and select** for identity, rather than accepting the first result. You are replacing conditioning with search
3. Keep the character in **fewer, longer shots** rather than many short ones. Every new generation is another roll of the dice, so take fewer rolls
4. Favour framings that hide the failure surface — wider shots, back-of-head, silhouette, obscured faces — and spend your close-ups where identity matters most dramatically

Point 4 is a real technique, not a consolation prize. Directors have always covered casting and continuity problems with staging. If the tool cannot hold a face in close-up, write fewer close-ups.

---

## 3. Diagnose drift

There is a real tension here: the features that preserve identity also encode motion. Force identity too hard and movement goes unnatural; leave it free and identity dissolves. Long sequences also decay — moles, tattoos and skin texture fade or flicker over time.

Seven named causes with mitigations: `references/drift.md`.

The master rule is the last one: **change one variable at a time.** If the character, camera and light all move at once, drift becomes undiagnosable.

### Chain continuity

The workflow I have found most reliable:

1. Approve a canonical keyframe in neutral light
2. Build each **setup frame from that approved image** — verify identity, wardrobe, screen direction and light *as a still*, before any motion exists
3. Animate only once the setup frame is locked. Two stages: construct the frame, then perform it
4. Chain the previous clip's **final frame** into the next clip's **starting reference**, where the tool supports frame conditioning
5. Hold seed, aspect ratio, duration and style constant
6. Keep clips **5–10 seconds** and stitch in the edit [PRACTITIONER]

Steps 2 and 3 are split for a practical reason: some tools will not accept identity references and a first frame in the same request. Constructing the frame first, then animating it, gets you both without needing a tool that does both at once. See "Choosing your conditioning mode" in `references/tool-matrix.md`.

**Chaining and the canon frame are different jobs.** Chaining forward keeps motion and composition continuous between adjacent clips. But because each link inherits the last one's error, chaining alone ratchets drift forward. That is why the QC gate in section 7 audits against the canon frame rather than the previous shot: **chain for continuity, audit against canon.** Doing only the first is how a face walks away from itself over forty shots.

---

## 4. Track continuity like a script supervisor

Live-action script supervisors track action, eyelines, hand occupancy, wardrobe, props, hair, makeup, injuries and story day. The generative equivalent is a per-shot sheet — template in `references/continuity-sheet.md`.

Two things people miss:

**Story-day progression.** Blood, dirt, sweat, bruising and costume damage advance across a film. Log the state *and its direction of travel*, or shots generated out of order will contradict each other.

**Marks need their own references.** Independent per-shot generation reinvents small marks. Note for each whether it is permanent, wardrobe-covered, makeup-altered, or revealed only in specific shots.

Continuity-checking tools exist, but they detect and flag rather than reliably fix. Human-approved metadata plus generation plus automated comparison is the defensible model.

---

## 5. Multi-character scenes

The dominant failure is **face blending** — two characters trading features or converging.

- **Cast for contrast.** Characters sharing hair colour, build and age will blend. Differentiate silhouette, hair, skin tone, wardrobe colour and height at the casting stage. This is a casting decision, not a prompting problem
- Address position explicitly: left, right, foreground, behind
- Avoid prompts where characters overlap heavily or exchange clothing
- Reject blended results immediately and regenerate; they do not repair well

### Eyelines and shot-reverse-shot

Establish the master angle first and lock, in that shot: both characters' screen positions, the action line, eyelines, lens, framing, lighting and location. Generate the reverse from the **same** references, explicitly keeping camera on the correct side of the line.

Specify eyelines numerically — "gaze 15 degrees camera-left, off-screen" — not "looking at the other person." Models default to the statistically likeliest framing regardless of geometry.

**The reverse-angle trap:** the reverse exposes set space that was never designed and never seen. Define that environment *before* attempting the reverse, or the two angles will describe two different rooms.

---

## 6. Repair or regenerate

**The rule:** repair when identity is coherent and the defect is local — blur, compression, mild warping. Regenerate when identity has collapsed. Restoration reconstructs a *plausible* face from degraded evidence; it cannot recover identity that is absent. Restoring a wrong face gives you a cleaner wrong face.

Decision tree, pipeline order, restoration settings and prompt patterns: `references/repair.md`.

---

## 7. QC gates

Before any shot enters the cut:

- [ ] Inspect at 100% for identity, mouth and eye geometry
- [ ] Inspect at playback speed for flicker and temporal seams
- [ ] Compare against the **canon frame**, not the previous shot — which may itself have drifted
- [ ] Check side turns, occlusions, glasses, smiles and motion blur separately; each is a distinct failure surface
- [ ] Verify wardrobe against the continuity sheet, including fastenings and damage state
- [ ] Verify marks are present, correctly placed and correctly sized
- [ ] Verify screen direction and eyeline against the blocking diagram
- [ ] **Reject any version that is sharper but less recognisably the same person**
- [ ] Keep a lossless intermediate so a bad pass can be replaced without re-running the chain

**The drift audit.** Every 8–10 shots, contact-sheet the accepted shots against the canon frame [PRACTITIONER: the interval is my habit, not a measured optimum — audit more often on long productions]. Slow drift is invisible shot-to-shot and obvious in aggregate. Catching it at shot 10 costs ten regenerations. Catching it at shot 60 costs the film.

---

## The ten rules

1. Cast before you shoot. Approve one canon frame and never regenerate it
2. Cast for distinctiveness, not beauty
3. One angle per reference image. Never composite turnaround sheets
4. Paste the identity block verbatim. Vary only action, camera and setting
5. Declare what is locked and what is free
6. Build the setup frame as a still and approve it before animating
7. Chain last frame to first frame
8. Change one variable at a time
9. Keep clips 5–10 seconds and stitch in the edit
10. Contact-sheet against the canon frame every ten shots

---

## Reference files

- `references/worked-example.md` — one character, one scene, three shots, end to end, including the failures
- `references/prompt-blocks.md` — turnaround, detail-plate and setup-frame prompts; identity block; scene block; negative lists
- `references/tool-matrix.md` — identity mechanisms per tool, and how to choose a conditioning mode
- `references/drift.md` — the seven causes of drift and their mitigations
- `references/continuity-sheet.md` — copy-paste continuity tracking template
- `references/repair.md` — repair-vs-regenerate, restoration settings
- `references/sources.md` — sources, graded by confidence
- `scripts/contact-sheet.sh` — builds the drift-audit contact sheet. Needs ffmpeg; uses ImageMagick if present

New to this? Read `worked-example.md` first — it shows the order of operations, which is most of the method.

Claims are labelled `[PRACTITIONER]` inline where they are reported experience rather than vendor-documented or research-backed. Tool capabilities change frequently; verify any specific parameter against current vendor documentation before building on it.
