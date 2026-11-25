---
name: shot-director
description: Plan, write and review shots like a film director. Use whenever a video is being planned, prompted or critiqued, including AI video generation prompts (Sora, Veo, Kling, Runway, Seedance, Hailuo and similar), storyboards, shot lists, animatics, HyperFrames or Remotion compositions, camera notes on a cut, or any request for something "cinematic". Turns vague adjectives into executable camera instructions: 22 camera moves with example prompts, prompt templates, cheat sheets by feeling and by scene task, a failure checklist, and Nolan-style direction of time and space (scale, screen direction, converging timelines, rhythm).
license: MIT
---

# Shot Director

An adjective makes the model guess. A camera instruction tells it what to do.

This skill turns "make it cinematic" into shots a model, a renderer or a crew can execute: where the viewer stands, how the camera moves, where it stops, what never changes, and why the shot exists at all. It is tool-agnostic. Use it to write prompts for generative video, to plan a HyperFrames/Remotion/Blender film, or to give precise notes on a cut.

## Workflow

Work through these in order. Skip a step only when the brief already answers it.

1. **Brief and clocks.** Pin down the story in one sentence, the feeling the viewer should leave with, the duration, and the music or tempo if there is one. Decide the three clocks: *story time* (how long events take in the world), *screen time* (how long we watch), *rhythm* (how often things change; lock it to the beat grid when there is music: one beat = 60/BPM s, one 4/4 bar = 240/BPM s; if the duration isn't a whole number of bars, land the last cut or the title on a downbeat and let the tail ring out). Note the delivery aspect ratio. Read `references/time-and-space.md` for anything longer than a single shot.
2. **Structure.** List the beats. Decide whether a second timeline should cross-cut and converge, which screen direction each sequence keeps, where the geography is established, and where the one held moment of stillness goes.
3. **Shot list.** Write every shot in the six layers (`references/foundations.md`): subject and action, shot size, angle and height, lens and focus, camera move, pace and limits. Every shot gets one main move (two at most, joined by a trigger), a start frame, an end frame and its holds. Every wide shot gets a scale reference.
4. **Choose the moves.** Pick each move from what the viewer should feel or what the scene must do, never from what looks impressive: `references/cheat-sheets.md`. Check look-alike pairs (pan vs truck, zoom vs dolly, POV vs FPV...) in the "pairs that look alike" section at the top of `references/moves.md` before writing them down; open the rest of that file only for the move you need.
5. **Write the instructions.** Use `references/templates.md` and the six-item move spec in `references/instructions.md`. For still-image pipelines with a depth camera, translate with `references/depth-renderer.md`.
6. **Review.** Before generating, and again on every result, check `references/review.md`, both the shot-level list and the sequence checks (direction, geography, scale, rhythm, held moment). Give notes in the same language as the shot list: shot, timestamp, move, direction, start → end, speed, what stays still.

## Shot list format

Use this table (or the same fields as a list) for every plan:

| # | In (tc) | Beat / purpose | Size · angle · lens | Subject action | Move (type, direction, speed) | Start → end frame | Holds | Sound / cut cue | Dur |
|---|---|---|---|---|---|---|---|---|---|

- **Purpose** answers: what does the audience learn or feel here that they didn't before? If nothing, cut the shot.
- **Holds** include the scale reference and screen direction where they matter.
- **Sound / cut cue** is the beat, sound or action the cut lands on.

## Rules that matter most

- **One main move per shot.** Two at most, joined by a trigger ("when she passes the second pillar…"). Everything else is a cut.
- **Every move is sealed:** a start, an end, a speed, and what must not change. "Pan right" alone pans until the clip ends.
- **Never mix zoom and dolly by accident.** Push for walking in, zoom for optical enlargement, both in opposite directions only for a dolly zoom.
- **Describe the subject's blocking, not just the camera,** or both drift.
- **Static first when unsure.** If the action and composition don't work still, no move will save them. Then add one move and compare.
- **Frame for the delivery ratio.** In vertical 9:16, tilts, pedestals, cranes and depth carry the frame while trucks and pans read narrow; keep caption and UI safe zones clear. In wide formats, lateral moves and landscape scale gain.
- **Frame 0 is the poster.** Most platforms use the first frame as the thumbnail: open on a composed frame, never on black.
- **Time and space are materials.** Scale needs a ruler; geography before action; hold the line; stage in depth; shrink shot length toward the climax; hold a beat longer than comfortable before a reveal.

## House defaults

These come from the film the skill was built on (HOME, a 2-minute sci-fi short). Treat them as defaults and override them from the brief.

- Continuous film feel: real parallax and motion inside the frame, never a plain zoom on a still.
- No white flashes or unmotivated strobes.
- Physically plausible: heavy things stay heavy and still unless the story moves them.
- Even, readable pacing; music-led. Add sound effects only when asked or when the story turns on a sound (a signal, an alarm, a knock), and say so in the plan.

## References

| File | Read it when |
|---|---|
| `references/foundations.md` | Starting any shot: three questions, blocking, six layers, prompt order |
| `references/moves.md` | Choosing or naming a move: 9 look-alike pairs, 12 basic + 10 advanced moves with example prompts |
| `references/instructions.md` | Writing the move spec, multi-move choreography, staged long takes |
| `references/templates.md` | You want a fill-in prompt (single move, follow, reveal, handheld, gimbal, FPV, dolly zoom, long take, choreography) |
| `references/cheat-sheets.md` | Picking a move by feeling or by scene task; worked "same scene, different feelings" examples |
| `references/time-and-space.md` | Planning a sequence or film: scale, geography, screen direction, clocks, converging timelines, moves in time, light, colour, match cuts, director toolbox |
| `references/review.md` | Checking a shot list or a generated clip |
| `references/depth-renderer.md` | The film is built from stills with a depth-parallax camera (pairs with the `still-to-film` skill) |

## Credits

The move vocabulary, templates and cheat sheets are adapted (rewritten in English with new examples) from Adrian Punk's two-part Chinese guide on AI video camera movement, [@AdrianPunk115](https://x.com/AdrianPunk115). The time-and-space chapter, the review format and the depth-renderer mapping are original to this skill.
