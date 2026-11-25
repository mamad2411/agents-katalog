---
name: explainer-architect
version: 1.0.0
description: Engine-independent design of teaching videos (explainers for a mechanism, formula, protocol or data structure) — the drawing teaches and the formula sits beside it, one idea per scene, drawings cued to narration phrases, every scene marked as source, textbook, derived, real run or illustration, facts held in a content file with sources, v1/v2 and A/B versions that never overwrite a render, and a contact-sheet look check before handoff. Use when planning, storyboarding or reviewing an explainer video, whatever draws it (Remotion, Manim or another tool).
---

# Explainer Architect

Decides what a teaching video shows and in which order, and how to check it. It produces the scene plan, the content file and the review, not the code of an engine: for Remotion see [remotion-architect](../../frameworks/remotion-architect/SKILL.md), for Manim see [manim-architect](../../frameworks/manim-architect/SKILL.md). The words and the speech rate belong to [narration-architect](../narration-architect/SKILL.md); a live, presenter-led demo is [demo-script-architect](../demo-script-architect/SKILL.md). Templates and commands are in [RECIPES.md](RECIPES.md); videos for learners (a worked number per concept, predict then reveal, a pointer to a tool as a switch) are in [LEARNERS.md](LEARNERS.md).

## 1. Mental model

- **The drawing teaches; the formula, the code or the table sits beside it as the summary.** A scene that opens with a formula and then decorates it teaches nobody. Draw the object first (a graph being explored, a timeline, a table that fills in, a token that walks a path). The formula appears when the drawing has shown where each of its parts comes from.
- **One idea per scene.** A scene that needs "and also" is two scenes.
- **The picture and the voice split the work.** The picture carries names, numbers and code; the voice carries the reason (narration-architect, section 1).
- **A claim has a source, or it is labelled.** A viewer must be able to tell a fact from a worked example from an invention.

## 2. Interview first

Ask in order and wait for each answer: who watches and what they know already; the one thing they must be able to do or say afterwards; the sources (documents, runs, textbooks) and which are real; length and where the video is shown; which engine draws it (that picks the skill that follows); who supplies the voice (never choose it for the owner).

## 3. The scene rule

1. **Draw in the order the narration says it.** If the voice says A and then B, A appears first. Reorder the words before you reorder the animation.
2. **Cue drawings to phrases, not to seconds.** Keep the narration as data, take the words before the phrase and divide by the speech rate. The cue must fail the build when its phrase is no longer in the narration, so an edit of the words cannot leave the picture behind.
3. **Scene length is `max(animation time, words / rate + lead-in + tail)`.** Use the rate measured on the real voice (narration-architect, section 4). A guessed rate ends scenes before the voice and fires every cue early. Count spoken words (after pronunciation forms), in the cue as well as in the length.
4. **Leave silence.** A new drawing gets a second or two before the voice talks over it, and dense text is never read at the same time as it appears.
5. **End on a stable frame.** The last frame of a scene is the finished drawing, not half an animation.
6. **Do not draw twice what is said once.** If a number is on screen, the voice gives its meaning.

## 4. Provenance

Every scene carries a small chip with the origin of its content:

| Chip | Meaning |
|---|---|
| `SOURCE` | what the cited sources state |
| `TEXTBOOK` | general background; the reference is in the content file |
| `DERIVED` | worked out here from a source's data or formula (a calculation, not the source's claim) |
| `REAL RUN` | taken from a recorded run |
| `ILLUSTRATION` | made up to show an idea; it is not data |

- Made-up values are flagged on screen **and** in the words ("this graph is made up").
- Facts live in a **content file** with a source per fact; the scene reads it. No number appears on screen that the content file does not hold. Shape in [RECIPES.md](RECIPES.md#1-the-content-file).
- The last scene says what was not checked or not run.

## 5. Versions of a video

- **Never overwrite a render that someone has seen or published.** The old one keeps its name (`v1`), the redesign is `v2`, a comparison is `v2.a` and `v2.b`. The same for the narration folder and the content file: copy, then change.
- Keep the old composition or scene id and add the new one beside it, so a reviewer can play both.
- A new look is an option whose default is the old look; existing renders do not move.
- Audio that was generated for the same words is reused by a new version; changed words need new audio.

## 6. Look before you hand off

1. Render, take one frame at about 85% of each scene (its end state) and tile them in a contact sheet ([RECIPES.md](RECIPES.md#2-the-contact-sheet)). Read it for overlap, empty areas, near colours, dense text and a stamp or chip that covers a label.
2. Open the dense scenes at full size; a sheet hides small type.
3. Run the length gate with the real audio: none runs past its scene.
4. Listen once, and check each sentence against its source.
5. Judge at the final resolution, not at the preview size.

## 7. Anti-patterns

- A formula first and a drawing as decoration.
- A made-up value with no label.
- Scene times from a guessed speech rate.
- A cue given in seconds that no one updates when the words change.
- A new render saved over the old one.
- Two ideas in one scene, or a scene with no stable end frame.
- Reading the screen aloud.
- Judging the look from a thumbnail.

## 8. Review checklist

- [ ] Each scene has one idea, drawn in the order it is said.
- [ ] Each scene has its origin chip; every illustration is flagged on screen and in the words.
- [ ] Every number on screen is in the content file with a source.
- [ ] Cues point at phrases, and the build fails if a phrase disappears.
- [ ] The speech rate is measured, and no audio runs past its scene.
- [ ] The last scene says what was not checked.
- [ ] Old versions are untouched; the new render has its own name.
- [ ] A contact sheet and the dense scenes were viewed at final size.
