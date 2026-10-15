---
name: audio-album-creator
description: "Distill a pack of source material (audio / text / photos) into a complete, production-ready original emotional music album plan (a Markdown document). Use when the user wants to make an album for a person or a life experience, turn raw material into an album plan, create a life/memorial album, an Amber Ark-style custom album, or write an album following the creation guide. The user names which source files to use this time. For narrative, custom albums made for close family, a partner, a child, or a team/company. Not for plain lyric polishing, pure music-theory Q&A, or generic lyric-writing with no narrative material."
---

<!-- Ver 2026-07-02 01:14, by Claude Sonnet 5 -->

# Audio Album Creator

Read and understand a user-supplied pack of source material (audio, text, photos, or any mix), distill its essence, then run a **simple but effective** pipeline to produce a **complete, ready-to-produce original emotional album plan** (a Markdown document).

The engine behind this method is `references/album-creation-guide.md` (the Album Creation Guide — all `guide §N` citations in this document refer to it); the output structure follows `references/album-plan-template.md` (a pure skeleton template — section headings and placeholders only, with no story content or stylistic bias, so it can't contaminate the creation of different themes).

## Core principles (these drive every creative trade-off)

- **One lead + one second lead (two singles)**: a whole album (typically 6–8 tracks) carries **two singles** that bear the two different forces that "move the customer." The **lead single (主打)** — chosen by narrative, usually the throughline-resolving closer — is excellent in both lyrics and music, carries the emotional anchor, and is the breaking-point moment that "makes the customer cry" (QC ≥ 9/10, 85+). The **second lead (副主打)** — chosen by whichever track is most ear-catching in melody/style — aims first at "sounds great on the first listen," with lyrics that only need to clear the bar (80+, sound-first). The remaining "base tracks (底座)" hold the pass line (≥ 7/10, 60+). **Why two**: being catchy is what wins first impressions (the customer's gut reaction when choosing the album), and being moving is what drives retention (making the customer feel understood) — splitting these two peaks across two tracks is safer than betting everything on one.
- **Two-layer quality model (each track's pass line and ceiling)**: the **threshold layer** (every track must pass) = melodically pleasant, smooth, singable, easy to sing along to, no 倒字 (tonal mismatch — a character whose tone contour fights the melody so it's misheard as another word), **it reads through** (the plain-reading gate — every line and every adjacent pair reads in plain Chinese; see Prosody below), the story checks out, not maudlin. The **anchor layer** (required for the lead single — 1–2 spots; optional for the second lead) = the emotional moment that makes the customer feel "this is about me." **Metrical tidiness (工整) is a means in service of "catchy and pleasant," not an end — when over-tidiness hurts natural flow, pleasant wins.** **The three-pass lyric polish runs on every track**: lyrics are pure text, iteration is nearly free — the three-pass protocol applies to every track including base tracks (see Step 4); singles get additional forging beyond the three passes, base tracks accept once they pass the bar.
- **The 60-point commercial standard**: share-with-friends quality, not publication quality. Outside the two singles, don't chase artistic height — chase "the customer feels it was worth it."
- **Prosody (form matches meaning) is the first principle**: lyrics, music, voice, and production — all four layers serve one emotional intent. Paired with two underlying principles (guide §2): **signal over noise** (write only what the model can parse into sound, and put the strongest signal in the chorus) + **layered control** (put each intent on its most reliable layer: global sound → Style; section-level change → metatag; in-line breath points → punctuation and line breaks). The "hard writing discipline" below is mostly corollaries of these two. **There are no rules, only tools — when a discipline fights the emotion, return to Prosody rather than bolt on a new rule** (guide §2); abstract the underlying signifier instead of stacking "if X then Y" rules. **And meaning must hold before form can serve it** — Prosody makes form serve meaning, but only on a line that actually reads. So the first gate on every line is the **plain-reading (裸读)**: read it cold, as a native listener who doesn't know what you meant. Every word opens a semantic expectation — a question expects an answer on the *same axis*, a construction's first half expects its matching close, a word in a parallel slot locks to one sense — and the next line must honor it. One failure wears many faces: an answer off the question's axis (问"疼不疼"答"非常满意"), a construction opened but never closed ("先是凉的" with no "后"), one word forced into two clashing senses ("走" as *leave* beside "走" as *elapse*), a dangling fragment ("做到了的"). **Reads-through is a threshold, ahead of all form-work** — no tidiness, rhyme, real-quote authenticity, or negative space redeems a line that doesn't read. Corollary: **any form-fix is a re-write** — changing a rhyme or swapping a character can silently flip the sense ("过"→"走" locks the rhyme but changes the meaning), so re-run the plain-reading on whatever you touched, never assuming "I only moved the form."
- **Sense-bound sourcing**: an album's soul is the **personal anchors** caught from the source material (specific objects, smells, catchphrases, scenes, key events), not abstract sentiment. The more specific, the more the listener feels "this song is about me."
- **Track count is a beats budget, diagnosed from the story, not a slot count to fill**: 6–8 tracks is the recommended default (lean 6 for a short/single-facet story, 8 for a long/eventful one) — 5 or 9–10 stay acceptable when the material's own beat count clearly calls for it; don't drift further without a reason. What matters more than the number is the **arc's shape**, diagnosed from the material before anything is drafted (guide §5): a classic rising-action arc (clear external conflict/turning point) is only one shape among several — a spiral/introspective arc (every track circles the same core wound from a different facet), a gradual "no-climax" arc (an unremarkable, quietly-accumulating life — guide §5's example), and a fragmented/poetic collage are equally valid, each with its own track-count feel and its own curve (guide §34). **Never manufacture a climax the story doesn't have** — pick the shape the material actually has, then let the count and curve follow it.
- **A real person means ethics**: if the subject is a real person, handle them with dignity; abstract away or cut sensitive content (politics / illness / the deceased / privacy) per guide §27; before delivering the finished work, remind the family to confirm it.
- **The cover art is Prosody at the visual layer**: the CD cover shares a source with the lyric/music/voice/production work — subject imagery, color, typography, and composition all obey the same emotional intent, reusing the blueprint's throughline imagery + strongest personal anchor + emotional tone + style family + Persona character, so "the cover looks like the album sounds." Produce **3 genuinely divergent styles** in one pass (echoing the three-sketch spirit of Step 2); details in guide §36.
- **Delivery must be executable (Production Handoff)**: what the skill produces is a narrative "blueprint," but the **executable recipe** actually needed to roll songs / generate covers (each track's Style/Exclude/Sliders/full lyrics/roll SOP, the cover-gen command, the post-roll acceptance items) — if it stays scattered across a long document's track sections, the user still has to go back and re-extract it track by track. That "assembly grunt-work" is the skill's job to prepare once, at handoff. **Suno rolling stays manual** (a physical limit — no stable official API), and no tool can press "generate" for the user; but "prep it down to copy-paste / one-line image gen" is squarely the skill's job. So the tail converges into one **ready-to-execute "Production Handoff sheet"** (see Step 9 — **pure extraction and reordering, no new creation**).

## Workflow

This is a **human-run** skill, not an end-to-end fully automated one. It produces output in three escalating tiers: **Tier 1 pick the direction (Step 2) → Tier 2 lock the blueprint and contract (Step 3) → Tier 3 create track by track (Step 4 onward)**.

**Two run modes (confirm at Step 0)**:

- **Interactive mode (default)**: 1 mandatory gate (Step 2, creative direction) + 1 optional gate (Step 3, album name / lead + second lead / track order confirmation). **Track-by-track creation (Step 4) is not interrupted.**
- **Auto mode**: every gate auto-picks the "most recommended," runs straight through, and hands over a report at the end.

**Track-by-track creation uses subagent fan-out**: from Step 4 on, **dispatch one independent subagent per track** to focus on creation (this cures the attention dilution of "one long context carrying 8 songs"), relying on the "creative contract card" frozen in Step 3 to preserve album-level consistency. **Each track's "pick-best-from-multiple-lyric-versions" is done by the subagent's own self-evaluation; neither mode feeds it back to the user for a per-track choice** (avoiding choice explosion); if the user wants changes, they read the "candidates and polish" appendix and re-pick by hand.

The end produces standalone reports (a creation summary + a QA report) plus one **ready-to-execute "Production Handoff sheet"** (Suno roll recipes + cover-gen commands + post-roll acceptance, see Step 9). **Whether to rework is the user's call; the skill itself does no automatic rework.**

For non-trivial jobs (lots of material, unclear scope), first create `_album_plan.md` in the working directory to record task breakdown and progress, and clean it up when done.

### Step 0: Confirm input and working directory (before anything else)

1. **Confirm the material**: the user names which files to use this time. Confirm each path and type (audio / text / image / video) one by one.
2. **Determine the working directory (this is a fixed rule)**:
   - If all material is **inside one folder** → the working directory = that folder, and all intermediate results and final outputs are stored there.
   - If the material is **scattered across locations** → create a subfolder under the **current directory**, named by the **project name** (the project name is the subject's name or the album theme, e.g. `{subject}-album/`), and store all outputs there.
3. **Confirm the creative brief** (if missing, ask briefly — don't guess): who the subject is, what occasion, what core emotion is wanted, who's paying / who's listening, language (**Mandarin by default**; if the material's story has a strong modern/Western/English-language cultural background, 1–2 English-lyric or mixed-language tracks may be added, driven by the material not by the creator's preference — unless the user explicitly specifies an English-track count at input), **whether it's a real person** (this sets the strength of ethics and sensitive handling).
4. **Confirm the run mode**:
   - **Interactive mode (default)**: Step 2 must stop, Step 3 may stop, track-by-track is uninterrupted.
   - **Auto mode**: every gate auto-picks the most recommended and runs through continuously.
   - At the same time confirm the **production tier** (affects Step 4 cost): **standard tier** (base tracks also get 3 lyric versions) / **economy tier** (base tracks get only 1 lyric version × 3 passes; only the two singles get the full treatment). Interactive mode defaults to standard tier, auto mode defaults to economy tier; the user can override.

### Step 1: Ingest & distill the material

This skill runs on a **multimodal model** by default: it reads and understands text / image / audio / video material directly, with no transcoding or transcription pipeline.

- **Text / images**: read in full. For images, extract era, scene, relationships, mood, and any **objects** usable as personal anchors.
- **Audio / video**: hand directly to the model to understand — catch the spoken content, tone and mood, environmental cues.
- **If the current model or harness cannot ingest a material type** (e.g. audio isn't supported): **don't get stuck and don't fabricate content** — skip that material and, in the Step 8 creation summary, **explicitly record "such-and-such material was ignored because the model doesn't support it"** so the user knows.

After distilling, **write an intermediate file** `material-distillation-{subject}.md` into the working directory.

> **Extraction principle: exhaust, don't pre-filter.** Record every emotion, personality trait, scene, and story beat that exists in the material — this file is the complete "material archive," not a curated shortlist for this album. If there are 10 anchors, list all 10; Step 2/3 will select. **Step 1 is the only stage in the whole pipeline that reads the full input** — information lost here is lost permanently.

The file contains:

- Character bio / timeline (key life milestones)
- **The core story** (synthesized narrative, not a verbatim quote): 300–600 words, written from the perspective of a songwriter. Faithfully reflect the material — don't embellish or invent uncertain details. Focus on: what kind of person the subject is, what key turning points they experienced, what moments carry the most emotional weight. Capture personality traits (speech patterns, ways of handling things, recurrent behavioral patterns). Flag implied subtext (things the material doesn't state but can reasonably infer, e.g. "repeatedly mentions X but never says Y — this may mean…"). For multi-subject or relationship albums, describe the core tension of the relationship.
- **Personal-anchor & golden-line list** (the crux of guide §5: objects, smells, catchphrases, scenes, key events — list each, the more specific the better; **tag verbatim catchphrases as hook-candidate vs. texture**, so Step 4 can land the 1–2 that hit hardest per beat rather than stacking quotes to use them up)
- **The spine + emotional curve** (guide §5): the subject's *arc* — how they changed (wanted vs. needed, the turning point) as the album throughline — plus a **valence-over-time curve** of the key beats (this curve drives track order and tempo in Step 3, guide §34). List bitter→sweet / loss→gain / parting→return etc. as candidate shapes.
- Family members and relationships, important dates (seeding later family-memory and repeat-purchase hooks; also serving the perspective choice)
- **Sensitive-content flags and handling plan** (which to abstract, which are too dark and must be cut)
- **Ingestion status** (what was read, what was ignored as unsupported, any obvious gaps) — to be cited in the creation summary
- **Raw stock for the creative contract** (groundwork for freezing the contract card in Step 3): draft three-layer vocal descriptors for Persona candidates, throughline image candidates, recurring-motif-word candidates, an initial gathering of usable anchors per track. This is just prep; formal locking happens in Step 3.

### Step 2: [Tier 1 · mandatory gate] Propose 3 draft directions, ask the user to choose

Based on the Step 1 distillation, **offer 3 fundamentally different draft directions** for the user to decide. The three should **genuinely diverge** (determined by the material's content, not reskins) along these dimensions:

- **Stylistic leaning** (e.g. neo-folk vs. lyrical soul vs. synth-pop — whatever genuinely diverges for this material);
- **Emotional tone** (e.g. the warmth of bitterness-released vs. the restrained ache of holding back vs. the lightness of serene clarity);
- **Story core / throughline** (which single image threads the whole album — e.g. "a kept ticket" vs. "a single lamp" vs. "the road home").

Give each draft (**only at "sketch" granularity — don't expand a full blueprint**, which is Step 3's job, to avoid 3× blueprint cost with 2 discarded):

- A one-line concept + the emotional-arc trajectory + **the arc's shape** (classic rising-action / spiral-introspective / gradual no-climax / fragmented — guide §5; whichever the material actually has)
- **Throughline image** + the recurring motif word
- **Rough tracklist outline** (6–8 tracks as the default — lean 6 for a short/single-facet story, 8 for a long/eventful one; fewer or more only if the material's real beat count calls for it; one line of subject per track)
- The candidate lead single's angle + **one sample hook line** (so the user gets a taste first)
- An embryonic style family

**Mark the most recommended one and spell out why** (why it best fits this material and has the most "breaking-point" potential).

- **Interactive mode**: use `AskUserQuestion` to present the three sketches as options (the system auto-adds "Other" for custom directions). The user can: take the recommendation / pick another / customize / pick one and add notes.
- **Auto mode**: adopt the most recommended sketch directly, no interruption.

Record "three sketches + recommendation rationale + final choice and notes" into the intermediate file `creative-direction-{subject}.md`. **Once chosen, proceed to Step 3.**

### Step 3: [Tier 2 · optional gate] Album-level coordination (Album Blueprint) + freeze the creative contract card

Read §34 (album coordination), §24 (consistency), Part I §3 (emotion→lever) of `references/album-creation-guide.md`, and cross-reference template §0. **Expand along the direction the user chose** and write into the intermediate file `album-blueprint.md`:

1. **Concept and emotional arc**: state in one line what kind of album this is, **and confirm the arc's shape** (guide §5 — classic rising-action, spiral-introspective, gradual no-climax, fragmented, or another shape the material genuinely fits); the emotional arc — in that shape, not forced into another — is the track order.
2. **Persona lock**: describe the lead voice with the **three vocal layers** (timbre texture + delivery + production, guide §15.4), and set a backup voice if needed (e.g. a contrasting voice that enters on one track for a duet or a hand-off). **Artist names are for internal reference only and never enter a prompt** (translate them into the three-layer descriptors). You may set 1–2 **keys** for the whole album to rein in drift.
3. **Thematic motif**: one throughline image running through the whole album + one one-line subplot image + one melodic motif that recurs in the instrumental / at closings.
4. **Style family**: the sonic starting point and default baseline for the album — individual tracks may actively deviate per their narrative beat; this is design, not damage (§24/§34). The blueprint should assign each track its **actual genre slot** (the genre/era-color that track will actually use), not merely say "follows the family."
5. **Tracklist arrangement table** (6–8 tracks by default per the diagnosed arc shape — fewer/more if the material's real beat count calls for it; may include 1 instrumental as a "breath"): list # / title / subject / genre / mode / BPM·meter / role (lead / second lead / base / interlude) / Persona.
6. **Designate the lead + nominate the second lead**: place the **lead single** at the album's strongest emotional moment (center-back) — for a classic rising-action arc that's the climax with 1–2 tracks of descent/release after it; for a gradual/spiral/fragmented arc it's wherever the material's real peak of feeling falls, climax or not (guide §34) — chosen by narrative either way, usually the throughline-resolving track. **Nominate one candidate for the second lead** among the rest by "most ear-catching style/melody" — **don't lock it**: after the Step 4 roll-generations, if another track's melody is more stunning, it can change (catchiness is decided by the rolls, so it's locked late).
7. **3 album-name candidates**: mark the recommendation, with a one-line reason.

**Optional gate**: in interactive mode, you may here use `AskUserQuestion` to have the user confirm the album name / lead + second lead / track order (the user may also skip and wave it through); auto mode adopts the recommendations directly, no interruption.

#### Freeze the "creative contract card" (the crux that keeps fan-out from falling apart)

After the blueprint is finalized, **freeze a roughly 1–2KB creative contract card** at the end of `album-blueprint.md`. It is the "constitution" handed to each per-track subagent, and **replaces having the subagent re-read the whole guide** — this is the key to album-level consistency not splitting under fan-out. Template:

```
## Creative contract card (inviolable album-wide)
# An album reads as ONE album because the INVARIANT BINDER (Persona voice + throughline/motif + unified key) never moves — NOT because every track shares one genre. Genre / era-color / instrumentation are per-track variables, shifting by narrative beat (guide §24/§34).
- Persona "{name}" three vocal layers: {timbre texture + delivery + production — see §15.4}
- Backup voice (if any): {a second voice + where it is used}
- Unified key: main {key} / closing {key, if it resolves elsewhere}
- Style-family STARTING POINT (not a cage): {style family} + {core instrumentation} + {production} — **each track's genre/era-color is driven by its narrative beat, not forced into the family**; the album reads as one album because of the invariant binder (Persona voice + throughline + unified key), not genre uniformity. One genre end-to-end = monotonous; deliberate style variety = narrative energy (§24/§34). Heavy diversity → lean on Persona as the coherence anchor, not a Custom Model (§24)
- Throughline image: {throughline image}; recurring motif words: {2–3 motif words}
- Subplot image (if any): {subplot image} (recur the motif in {which tracks})
- Perspective baseline: {perspective}; breath points: {where the album shifts perspective to "breathe"}
- Tidy vs. free: tidy by default; free-verse latitude {0–N tracks, and which}
- Writing-discipline card: see the full "hard writing discipline" in this SKILL (punctuation controls breath / no bare spaces / write every chorus out in full / dense parallel couplets in chorus / metatags all in English / zero 倒字 on motif words …)

## Per-track dossiers (one per track, handed to the matching subagent)
- # / title / role (lead · second lead · base · interlude) / position in the emotional arc
- Narrative context for this track (1–3 sentences): which part of the source story this track corresponds to, what emotional moment it captures, what state the subject is in — not a list of anchors, but an explanation of why this track belongs here and what it's saying
- Subject and material anchors (from the distillation, the more specific the better)
- Most relevant golden lines / voice fragments for this track (selected from material-distillation, with source note)
- Emotion→lever suggestions (mode / BPM / meter / instrumentation / dynamics / vocals)
- This track's GENRE / era-color slot — driven by its narrative beat (the sound that fits this beat: its emotion, plus any era/place/event/cultural association the story carries; guide §15.1/§34)
- Throughline points that must be hit (e.g. the throughline image must appear in the chorus)
```

> A subagent has free rein within its own track, but **may not invent its own Persona / style family / throughline**. When it needs to dig deep into the engine, give it the path to `references/album-creation-guide.md` to read the relevant § on demand.

### Step 4: [Tier 3] Parallel per-track subagent lyric+music creation

The main context **no longer writes each track's lyrics itself**; instead it **dispatches one independent subagent per track** — giving each track back the full attention of "a single focused song" (this is exactly the mechanism by which "handing it off to a clean context gives higher quality"), while the creative contract card preserves album consistency. 8 tracks can run in parallel; wall-clock ≈ the slowest single track, not the sum of all 8.

**The brief handed to each subagent**:

- **Input** = the creative contract card (album-wide constitution) + this track's dossier (narrative context / anchors / golden lines / levers / throughline touchpoints) + **`references/lyric-craft.md`** (the per-track creation kit: seven dimensions / three-pass polish / lead-forging) + the path to `references/album-creation-guide.md` for reference. **The subagent doesn't read the full source material, but it must know the story behind this track** — the dossier's "narrative context" and "relevant golden lines" fields are its emotional anchor; the main context must fill them carefully, not just supply anchor symbols.
- **Task** = produce ① 3 candidate song titles; ② several complete lyric versions (each run through the "three-pass polish protocol" in `references/lyric-craft.md`; lyrics default to Mandarin — if this track's narrative beat has a strong English-language cultural flavor, the subagent may propose mixed-language or full-English lyrics with a reason, for the main context / user to confirm); ③ the Suno Style; ④ self-evaluate and pick the recommended version, with a brief pick-rationale + a short 倒字/QC note.
- **Constraints** = obey the contract card; don't invent Persona / style family / throughline; follow this SKILL's "hard writing discipline."

**Tiered investment (three tiers)**:

| Track role | Lyric versions | Three-pass polish | Style | Target | Production SOP |
|---|---|---|---|---|---|
| **Lead single** | **1 complete + dual-track killer line + 2 candidate choruses** | 3 passes on the complete version + killer-line forging | **3 (including vocal style)** | 85+ | N≥8, lock Persona, chorus Inpainting 2–5×, line-by-line 倒字 check (guide §31) |
| **Second lead** | 2 versions | 3 passes each + the three catchiness tests | **2–3 (favoring ear-catching melody/style)** | 80+ (sound-first) | **high-N rolls to land the melody**, Inpainting to tune the arrangement, lyrics clear the bar |
| **Base** | standard tier 3 versions / economy tier 1 | 3 passes each | **1 within the family** (may +1 backup) | 60+ | N=2–4, reuse Persona + style family, accept once it passes |
| **Instrumental interlude** | — | — | 1 (turn on Instrumental, leave Lyrics empty) + a structure note | — | roll several, take the warmest |

> **Base tracks don't do 3 styles**: a base track's style is already locked by the style family + Persona; forcing 3 styles either breaks album consistency or is a cosmetic tweak (wasteful). **Style is not the base track's variable — lyrics are.**

**The detailed creation kit** — the seven dimensions each lyric version must land, the three-pass polish protocol (run on every track, base included), and the extra forging for the lead / second lead (dual-track killer-line face-off + the three catchiness tests) — lives in **`references/lyric-craft.md`**, handed to each subagent alongside the contract card. Two cross-cutting reminders the main context keeps in view:

- The three-pass polish log travels with each lyric version into the Step 5 "candidates and polish" appendix (real iteration traces, not a one-shot draft with a label slapped on).
- **Restraint on the strongest material**: keep killer-line negative space to the lead's 1–2 anchor lines (full-song negative space thins the lyrics and hurts catchiness); and you needn't land every quotable source line — the 1–2 that hit hardest are usually enough (the rest stay as texture), so don't stack quotes just to use them up, though more may stay if they genuinely earn their place (guide §5).

### Step 5: Stitching and assembly (the consistency backstop after fan-out + assembly)

The subagents each write their own; cross-track consistency may crack. Return to the main context and do a **stitching check** (cheap but necessary), going through each item:

- **Motif/motif-word recurrence** actually landed (does the throughline image run through, does the subplot image recur in the designated tracks, does the melodic motif call back in the instrumental/finale);
- **Persona / key / style family** not drifting;
- **Perspective "breathes"** (not one person throughout, §6);
- Any **two choruses sharing a rhyme/hook**, any repeated imagery or self-plagiarism;
- **The lead / second lead are genuinely differentiated** (one goes for the emotional anchor, one for ear-catching melody — don't let them become two homogeneous songs);
- Real-person ethics and sensitive handling consistently in place.
- **Every selected lyric reads through** (the plain-reading gate, Core principles): re-read each final lyric **cold in the main context** — don't inherit the subagent's self-endorsement — line by line and against adjacent lines; **any rhyme/character fix you make here is itself a re-write** — re-check its meaning, never assume "form-only" (a 混辙 fix that swaps a character can flip its sense, e.g. "过"→"走").

When you find a crack, **feed it back to the matching subagent to revise, or fine-tune in the main context**, until stitching passes. Then assemble the outputs:

1. **The album-plan main document**: assembled from **each track's selected version**, clean and deliverable. Append a "how this album implements the Album Creation Guide" mapping table at the end (structure per the template's closing section).
2. **The candidates-and-polish document** (`candidates-and-polish-{album}-{model name}.md`): collect each track's **3 candidate titles / multiple lyric versions / three-pass polish logs / 3 album-name candidates**, mark the selected version and the reason, for the user to re-pick by hand.

### Step 6: CD cover design (produce 3 styles in one pass)

This goes after the stitched final draft — by now the album name, throughline, Persona, and style family are locked. The cover **doesn't start from scratch**: it draws directly from the blueprint — throughline image / strongest personal anchor / emotional tone / style family / Persona character — mapping each onto the four visual elements (subject imagery / color / typography / composition). Principles and specs in guide §36. **This step produces only the cover design and prompts (that's Design); actually generating the image is Production, on the same "to be executed" footing as Suno rolls — a pure-Design run goes only as far as the prompts and does not call an image API.**

- **Give 3 genuinely divergent styles in one pass** (not reskins, echoing the three sketches of Step 2): **photorealistic photography / hand-drawn illustration / abstract minimalism (or collage) are the default archetypes, swappable per the album's character**, or the same subject in different color and typography; only the three need to genuinely diverge. For each write: ① a one-line visual concept; ② the four-element values; ③ a prompt that can be fed straight to an image model. Fill in the template's "cover design (3 style candidates)" section.
- **Subject = the throughline image / strongest personal anchor** (prefer a concrete object, sense-bound), don't use a generic abstract image; **when the throughline can't be visualized, fall back to the anchor object**. Leave **negative space for overlaying the title** in the composition, and the thumbnail (the streaming first image is tiny) needs a strong focal point and little information.
- **Prompt-writing rules + output specs** (two prompt styles per image model, always add `no text`, AI text-rendering is unreliable so overlay the title in post, streaming master 3000×3000 + physical-CD specs): see **`references/cover-production.md`**.
- **Real / living subjects**: **don't rely on a recognizable face by default** — use the throughline object, a hand/back-of-figure or other crop, or illustration (this both sidesteps likeness rights and works because AI can't actually render a specific real person); a genuine portrait of the person requires family authorization. Abstract sensitive imagery per guide §27.
- **Interactive mode** may use `AskUserQuestion` to have the user pick 1 main cover (the rest kept as alternates); **auto mode** picks the one best fitting the album's character and explains why.

Write the 3 style designs and prompts into the cover section of the album-plan document (the template already includes it). **Actually generating the image is Production, not pure Design** — the helper script `scripts/gen_cover.py`, its zero-config UV env, flags, and API keys are documented in **`references/cover-production.md`**; the Step 9 handoff splices the chosen prompt into a ready-to-run command.

### Step 7: QA Report (a fresh-eyes subagent's adversarial re-check)

**Dispatch an independent subagent for a fresh-eyes re-check** — give it only the final album plan + the engine's QC chapters (§31/§32/§33), **without the "I just wrote this" self-endorsement bias**. Like the editor standing behind the author, it owns product quality with a critical eye and would rather over-report problems. Check each item and give a verdict (pass / needs fix / risk):

- **Plain-reading / reads through (a first-class item, ahead of catchiness)**: read each lyric **cold, as a native listener who doesn't know the intent** — does every line and every adjacent pair read in plain Chinese, with no answer-off-axis, no construction opened-but-never-closed, no one-word-two-senses, no dangling fragment; **the lead's killer line above all** (a question and its answer must sit on the same axis — 问"疼不疼"答"非常满意" fails this). Anything that doesn't read is a **must-fix regardless of how tidy or catchy it is**
- **Catchy / smooth (a first-class item, ahead of tidiness)**: is each track smooth, catchy, sing-along-able, with a melodic hook (can the hook be hummed); **the second lead is verified primarily by this**
- **Lead-single anchor**: are there 1–2 "this is about me" emotional moments; has the killer line been dulled by rhyme (self-check against the "minimalist held-back version")
- 倒字 / Chinese singability re-checked per track; does the hook hold up, short and repeatable
- **Parallel-couplet density**: is the chorus densely paved with parallel couplets, or has it degraded into "colloquial prose with line breaks"
- **Golden-line restraint**: does any track stack source quotes that dilute the memory point (quotes that don't earn their place) — restraint means you needn't use every quote, not a hard cap on how many (guide §5)
- **Rhyme-label cross-check**: per track, check the tracklist's chorus rhyme label against the lyrics' **actual end-rhyme**; if the lead / signature line takes the "legal exception" and drops the rhyme-lock for parallelism, the label must honestly say "parallelism / rhyme-break," not vaguely name a rhyme category (catches mislabels — see "legal rhyme-lock exception" in the hard writing discipline)
- **Were the three passes actually done**: does each lyric version have a polish log, are there real iteration traces (not a one-shot draft with a label slapped on)
- **Bare-space violations**: are in-line breath points done with punctuation/line breaks, any bare spaces used as pauses (never allowed)
- Is every chorus written out in full, any "(repeat)" violation; are metatags all in English, any Chinese parenthetical notes in the lyric body
- Is each Style 4–7 descriptors, **are the three vocal layers up front, is the key marked**, any mutually conflicting descriptors; any misuse of an artist name / reproduction of a famous song
- Prosody form-meaning match (does structure match emotion); **album consistency via the invariant binder** — does the Persona voice / unified key / thematic motif run through (the real source of coherence); where genre/era-color varies by beat, is it a deliberate narrative signifier rather than drift, and conversely not a monotone single-genre album (guide §24/§34)
- Does the emotional arc and track order hold up **for its diagnosed shape** (don't fault a gradual/spiral album for lacking a classic climax); is total runtime in proportion to track count (~2:30–3:30/track, so an 8-track album lands ≈ 26–30 min)
- Is the genre-confidence expectation noted (opera/folk-instrument and other low-confidence cases only promise "approximate flavor")
- **The 3 cover styles**: genuinely divergent (not reskins), subject anchored to the throughline image/personal anchor, color and typography matching the emotional tone and Persona character, negative space left for the overlaid title, specs met (3000×3000 1:1); any platform logo/artist name wrongly stuffed into the prompt
- Sensitive / ethical handling adequate (real person; including whether the cover used an unauthorized likeness of a real person)
- Word-level polish: rare characters, mixed CJK-and-alphanumeric, **breath points (punctuation/line breaks, not bare spaces)**, colloquial feel; **is the strongest anchor in the chorus**, any section over-filled by formula/over-written, are the lyrics on the long side

**Honestly mark the boundary**: the plan stage is pure text — **the actual sound of 倒字, AI artifacts, pitch, dynamics, etc. can only be settled after Suno rolls and a listen** — list these separately as "to be verified at the listening stage," and don't pretend to have verified them on text.

End with an **overall QA verdict** + a **prioritized list of suggested rework items**. Write into a standalone file `qa-report-{album}-{model name}.md`. **Report only, no automatic rework** — whether to rework is the user's call.

### Step 8: Creation Summary (a project-level retrospective)

Write an **overall project summary** (a separate thing from the QA report, its own file): review the whole creation process, list the key points of each step (ingestion status, the chosen direction and why, the album blueprint highlights, an overview of the lead/second lead and base tracks, **why each track's selected lyric version was picked**, **the 3 cover styles and the chosen direction**), and **come clean about the problems along the way** — which material was ignored, whether the selection had gaps or bias, how sensitive content was handled, where compromises were made. Write into `creation-summary-{album}-{model name}.md`.

### Step 9: Assemble the Production Handoff sheet (pure extraction and reordering, no new creation)

This goes after QA — by now the album plan, the cover's 3-style design, and the to-verify-at-listening items are all locked. **Converge in one pass** the executable recipes scattered across the long document into one ready-to-execute sheet `production-handoff-{album}-{model name}.md`, so the user can roll songs / generate covers straight from it without going back to re-extract. **All content comes from the already-produced album plan and QA report — no new creation.** Three sections:

1. **Suno roll section (one block per track, copy-paste ready)**: each track a delimited block — title + role (lead / second lead / base / interlude) + target score; `Style` (4–7 descriptors, three vocal layers first, key included) + `Exclude` (only if the album plan specified one — it's an optional negative field, guide §23) + `Sliders`, each on a copyable line; full lyrics (English metatags, every chorus written out) as one paste-into-Suno-Lyrics block; this track's roll SOP (N value, Inpainting count, what to listen for — lead: 倒字 on anchor lines / second lead: the melodic hook / base: accept once it passes). The instrumental interlude listed separately (turn on Instrumental, leave Lyrics empty, give Style + a structure note). **Sliders notation must be unified album-wide into one form** (pick qualitative Safe/Strong OR percentages, not mixed per track), killing the scatter.
2. **Cover-gen section (commands ready to run)**: splice the chosen main-cover prompt straight into the full command `cd {working dir} && uv run {skill}/scripts/gen_cover.py "<chosen prompt>" -o covers/{album}-{style}.png`, plus one line each for alternates B/C; note the key requirement (any of `GRSAI_API_KEY`/`GOOGLE_API_KEY`/`OPENAI_API_KEY`) and the output dir `covers/`.
3. **Post-roll acceptance checklist (checkbox list)**: distill QA's "to be verified at the listening stage" items into a checkable list (倒字 on a real listen, AI artifacts, pitch/dynamics, overall catchiness, whether a legal-exception parallelism/rhyme-break holds up); append the **post-roll delivery specs** (from template §0.6: WAV master + 320k MP3, unified **-14 LUFS**, verify volume and track order separately for the physical version) to give Production specs a landing spot.

### Step 10: Save and deliver

All final outputs are stored in the working directory, each with a version-header comment at the top `<!-- Ver YYYY-MM-DD HH:MM, by {model name} -->` (**time down to the minute** — use `date "+%Y-%m-%d %H:%M"` to fetch the current time; don't write date only):

- **The album plan** (the main output, each track's selected version, **including the cover's 3-style design and prompts section**): `album-plan-{album}-{subject}-{model name}.md`
- **Candidates and polish** (3 candidate titles / multiple lyric versions / three-pass polish logs / 3 album-name candidates): `candidates-and-polish-{album}-{model name}.md`
- **Production handoff** (Suno roll recipes + cover-gen commands + post-roll acceptance, ready to execute): `production-handoff-{album}-{model name}.md`
- **QA report**: `qa-report-{album}-{model name}.md`
- **Creation summary**: `creation-summary-{album}-{model name}.md`
- **Cover images** (if actually generated): **stored in the working directory's `covers/` subfolder** (in the same project directory as the rest of the outputs, don't scatter them); the chosen main cover + alternates, named `{album}-{style}.png`, streaming master 3000×3000.
- Keep the intermediate files too (material distillation, creative direction, album blueprint [including the creative contract card]).

## Hard writing discipline (violations will directly ruin the Suno output)

> The foundation is just two principles — **signal over noise + layered control** (guide §2): write only what Suno can parse into sound, put the strongest signal in the most prominent spot, and place each intent on its most reliable control layer. Everything below is a corollary; when unsure, return to the principles.

> **Two categories in this section:**
> - **★ Suno engineering rules** (marked ★): violating these causes Suno to generate incorrectly — non-negotiable, Prosody can't help here.
> - **Lyric-quality defaults** (unmarked): recommended practice based on Prosody; legal exceptions exist, but must be intentional and disciplined; when one fights the emotion, return to Prosody.

- **★ Write every chorus out in full**: write out every chorus where it appears, **never "(repeat)" or "same as above"** — Suno generates literally.
- **Chorus = the strongest signal spot**: the chorus repeats most, so **put the most anchored (personal image), most impactful words in the chorus**; the verse handles "why/setup," the chorus is responsible for "being remembered."
- **Lock the rhyme + dense parallel couplets (the #1 lever for Chinese sounding "like a song")**: each chorus **locks one rhyme category to the end** (the thirteen rhyme categories of New Chinese Rhyme — 中华新韵十三辙), the verse rhymes on even lines; **the chorus defaults to densely paved parallel couplets (对仗)** (paired lines with matching structure and opposed imagery, e.g. "一碗甜粥／一缕晨光," "风吹不熄／雨打不凉"), and verses bury couplets as needed. Even line length (≤ ~10–12 chars), cut colloquial prose phrases. **Better tidy and densely paralleled than "colloquial prose with line breaks"** (guide §9.1). But **tidiness serves "catchy and pleasant"**: when the rhyme-lock/couplets force something stiff and tongue-twisting, or say everything for the listener, return to Prosody — being pleasant is itself an emotional carrier, so loosen a notch and favor negative space (especially on the lead's anchor lines).
- **Legal rhyme-lock exception (lock by default; break with discipline)**: the lead's anchor lines / the signature hook's opening line may drop the end-rhyme and use **strong parallelism** or another binding device instead (e.g. "these hands cut grass / sewed clothes / carried the load" — parallelism is itself catchy, a legitimate strong binder in Chinese song). But a break must: ① **stay within 1–2 lines**, never spreading across the whole song (a fully rhyme-less song falls apart); ② be **labeled honestly as "parallelism / rhyme-break" in the tracklist rhyme label**, never vaguely tagged as some rhyme category (else it misleads, and QA checks it — see Step 7); ③ be **listed under "to be verified at the listening stage,"** confirmed by rolling and a listen. Every other line still locks one rhyme to the end.
- **★ Use punctuation and line breaks for in-line rhythm, not bare spaces**: Suno reads punctuation/line breaks as breath instructions (period = breath and reset, comma = short pause, … = lingering hold, hyphen = drawn-out, line break = a longer pause, blank line = instrument continues while vocals stop); **in-line bare spaces are unreliable and often swallowed in connected reading**. Lines should be ≤ ~10–12 chars, split long lines, don't cram.
- **★ All performance/arrangement cues go in English square-bracket metatags** (`[Verse: breathy, sparse]`, `[Chorus: full band, erhu accent]`), **the lyric body keeps only the words to be sung**; **strictly no Chinese parenthetical notes** (e.g. "(softly)") — Suno will sing them as lyrics.
- **★ Each Style is 4–7 descriptors, three vocal layers first**: timbre + delivery + production (guide §15.4) go at the start of Style; you may add the **key** (`in A minor`) to boost album consistency (guide §15.5); name core instruments (for Chinese folk instruments use specific names like erhu/guzheng/pipa/dizi). Fewer than 4 descriptors is too vague; more than 7 produces conflicting signals and a muddy output.
- **★ Don't write artist names** (filtered/banned by the platform, and a placebo anyway): treat the target singer as internal reference, **translate them into the three vocal-layer descriptors** before writing; don't reproduce famous songs — do "evocative likeness + original lyrics" only.
- **Add or cut sections by function, don't fill the whole formula, don't fill every section**: the classic template is a toolbox, not a fill-in-the-blank; if 3 sections say it clearly, don't write 5; **lyrics: simpler over fuller** (form follows emotion).
- **★ Don't write chord progressions into the lyric body** (they'd be sung as lyrics); to influence harmony use "mode + key + mood + genre," and put chord progressions only at the end of Style as a low-expectation supplement (guide §15.5).
- **★ Tag every section; `[End]` is mandatory**: add a bracket tag to every section (`[Verse 1]`, `[Chorus]`, `[Bridge]`, etc.); **`[End]` is an engineering rule — prevents Suno from trailing off endlessly**. Which sections to include is decided by narrative logic and genre, not by a fixed formula — a simple ballad may have no Bridge, a rap track may have no traditional chorus form (see guide §7). The tag names listed here are a toolbox, not a checklist.

## References (read on demand, progressive disclosure)

- `references/album-creation-guide.md`: the complete methodology engine (Album Creation Guide). **Read the relevant chapters before creating in Steps 3–4** (the two underlying principles §2, emotion→lever §3/§18, lyrics Part II [tidiness §9.1], music Part III, Suno practice Part IV [three vocal layers §15.4, key/chords §15.5, Style §21, punctuation-as-rhythm §22], the prompt framework Part V, QC Part VI, genre confidence §26). **Per-track subagents by default read only the Step 3 creative contract card and aren't forced to read the whole thing**; read a given § by path when a deep dive is needed; **for Step 6 cover design read §36 (the cover = Prosody at the visual layer)**. Suno and image-model capabilities change by version — verify against the current version before hands-on work.
- `references/album-plan-template.md`: the structural skeleton and placeholders for the final plan. **Fill in by this structure from Step 3 on**, replacing each `{…}` placeholder, deleting inapplicable optional sections (e.g. delete the "real-person note" if not a real person). The template gives only the form; content and style all come from the material distillation.
- `references/lyric-craft.md`: the per-track creation kit (seven dimensions / three-pass polish protocol / lead-forging) — **handed to each Step 4 subagent alongside the contract card**, so it doesn't have to read the whole engine guide.
- `references/cover-production.md`: Step 6 cover production detail (prompt-writing rules per image model, output specs, the `gen_cover.py` zero-config UV env + flags + API keys) — **read at Step 6 when writing prompts / generating the image**.

**Terminology cross-reference (this SKILL vs. the underlying engine)**: `album-creation-guide.md` is a general-purpose methodology engine written before this SKILL introduced the two-single model. In the engine, "代表作 (signature track)" means the single most important song — corresponding to this SKILL's "lead single (主打)." The engine's "底座 (base)" maps to this SKILL's "base track (底座曲)." The engine doesn't have a "second lead (副主打)" concept; that's an extension in this SKILL. Where engine and SKILL terminology diverge, this SKILL's definitions take precedence.

When everything is done, brief the user: where the working directory is, which files were generated (the album plan [including the 3 cover styles] / candidates and polish / **production handoff** / QA report / creation summary + intermediate files), which two tracks are the lead and second lead, **the chosen cover direction**, **the suggested rework items in the QA report** and **the ignored/incomplete material in the creation summary**, and **point them to the production handoff**: roll the Suno tracks and generate the cover by following it item by item. Make clear: **whether to rework is the user's decision, the skill does no automatic rework**. For real-person material, additionally remind them to "have the family confirm before delivering the finished work."
