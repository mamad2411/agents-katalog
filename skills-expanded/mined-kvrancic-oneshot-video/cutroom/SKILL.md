---
name: cutroom
description: Make video on this Mac for a named audience, in three jobs. Cut makes short clips from a long recording (a lecture, talk, podcast, interview or stream), chosen by reading the whole transcript, cut on word boundaries, reframed to 9:16 by a camera that follows the speaker, with word-timed captions, graphics, B-roll and titles. Edit makes a whole recorded talk into one video, every camera and microphone synced, fillers cut, a multicam edit with chapters and subtitles, handed back to Premiere Pro or Final Cut Pro. Make builds a narrated story or a music-led promo from a script or a brief, with stock B-roll, titles, a voice and a bed cut on the bar. Use when the user says "clip this", "make shorts / reels / TikToks", "find the viral moments", "Opus Clip", "edit my lecture / talk / keynote", "multicam edit", "remove the filler words", "cut the demo part", "make a promo / trailer / opener / explainer", "a video from this script", "export to Premiere / Final Cut", asks to re-cut a clip or to report a cutroom bug.
---

# cutroom

One tool for three jobs, run on this Mac: short clips cut out of a long recording, a whole recording edited into one finished video, a video made from a script or a brief. The steps are verbs of one command, `cutroom`. Every video is one `plan.json`. Every default is a row of one table, which `cutroom profiles` prints. The audience comes first: the brief names who watches and where. That choice sets the length, the opening, the pace, the captions, the B-roll, the sound and the loudness.

## 1. Check the machine

```bash
cutroom doctor
```

It prints `ok`, `warn` or `MISS` for each part with the command that fixes each gap, then `ready`. Run it before the first job of a session and again whenever a step fails. Where `cutroom` is not on the PATH it is `cli/cutroom` in this skill's folder, the base directory the agent names when it loads this skill: write it out in full in every command. On a Mac where the doctor finds the parts missing, `cli/cutroom setup` fills `~/.cutroom` with the Python environment, the models and Remotion, about 2.6 GB: say what it fetches and, where a person is at the Mac, ask before running it.

`cutroom --help` lists the verbs and `cutroom VERB --help` gives each one's arguments. `cutroom path` prints the tool's own folder.

## 2. Write the brief

```bash
cutroom brief DIR --for "<who watches, in a sentence or two>" --where shorts,linkedin [SOURCES...] [--script script.txt] [--song track.wav]
```

`DIR` is the job's folder: `./cutroom/<name>/` beside where the person works, unless they name another. The verb looks at what it was given, writes `DIR/brief.json` and prints the job, the profile and the page to read next.

- **The profile and who asks for it.** A caller from Hydra names the profile with its form (`--profile stream` from `clip-rewards`). Wherever the form's card names a value, the card wins. Otherwise the person's words choose ("my talk" is `talk`, "the whole lecture" is `lecture`), then the footage. A clip of the person's own talk takes `talk`. `references/audiences.md` gives every profile and placement with its source.
- **A caller's brief answers the intake questions,** so a session on a lane, with nobody at the Mac, asks nobody: it takes the brief and the recommended answers and says in its handover what it chose. A person at the Mac is asked only what the request and the brief leave open, in one AskUserQuestion call with the recommended option first.
- **`references/attention.md`** is the one-page map to Hydra's craft of attention (the hook, the layer, the titles, the post, the bar a video is held to). Read it before writing an opening, a layer or a title. Read it too whenever a brief comes from a Hydra skill that names a form, a hook or a caption id.

## 3. Read the workflow for the job

| Job | Given | Makes | Page |
|---|---|---|---|
| `cut` | a long recording: a stream, a talk, a podcast; or the takes of an ad, which its step 2 makes one project | short clips that stand alone | `workflows/cut.md` |
| `edit` | everything recorded at one event: cameras, a microphone, a screen | the whole talk as one finished video, with chapters | `workflows/edit.md` |
| `make` | a script or a brief, with a logo, a song or a few clips | a narrated video or a music-led film, with B-roll and titles | `workflows/make.md` |

Follow the page from its first step. Each step names the reference to read at that step.

## The rules every job keeps

- **A job's files live in the job's folder** and never in the tool's. Every verb writes under `DIR`; the folder `cutroom path` prints is never written to.
- **Keys come through Hydra's vault,** handed to the one command that needs them without being shown: `hydra vault run PEXELS_API_KEY -- cutroom stock search "..." --dir DIR`. `cutroom keys DIR` prints which keys the job would use, where this Mac has each and the prefix to run each verb with. A missing key ends that verb alone with exit code 3 and prints the `hydra key` line that asks for it on Hydra's page: run that line in the background and go on (`cutroom stock` searches the sources that need no key, `cutroom voice` speaks its draft). On a Mac without Hydra the same names are read from the environment or from `~/.config/cutroom/keys.env`. Never print a key.
- **Every verb reports the same way:** what it did, the files it wrote, then its warnings, with `--json` for the same as one object. Its exit code says what happened: 0 done, 1 failed, 2 a wrong call (a misspelt plan field names the nearest one), 3 a missing key with the command that gets it, 4 a check that warns. Read every warning.
- **A plan with no profile renders under `calm`,** the values cutroom draws with where no audience is named. A value written in a plan wins over its profile's.
- **Word indices, never timestamps.** Every cut is a range of words, so it lands on a word boundary or a pause. Edit the plan, never the output: a re-cut changes the plan and runs the step again. Every cache rebuilds only what changed.
- **Look before handing over.** Read the stills, the reports and the sheets each workflow makes. A fresh session reviews anything that goes public (`references/review.md`).
- **Nothing on screen says what the speaker did not say.** Private people are never named on screen. Claims about named public figures are commentary: flag them in the handover.
- **Never publish or upload anything.** The person posts.
- **Renders are heavy.** Run `df -h /System/Volumes/Data` before one: a render needs about 5 GB. Run long renders in the background and say roughly how long they take.
- **A step that fails** in a way its page cannot fix: `cutroom report DIR --title "<verb>: <what went wrong>" --step "<what was running>" --log <the error output> --note "<what was tried>"` writes `DIR/bug-report.md` with private paths taken out. It sends nothing. Show it to the person, who files it where they choose.

## The references

| Page | Holds |
|---|---|
| `references/audiences.md` | the profiles and the placements, each number with its source |
| `references/selection.md` | choosing the moments: the gate, head and tail, the opening, the marks, ranking |
| `references/plan.md` | the plan's schema, time references, layouts and the make job's plan |
| `references/joins.md` | how cuts, moves and sound meet: pauses, the camera, the voice, the bed under it |
| `references/captions.md` | the presets, where captions sit and how long each page stays |
| `references/graphics.md` | overlays, the kit's components and a graphic of the project's own |
| `references/broll.md` | finding, judging, placing and crediting cutaways |
| `references/titles.md` | the layer, the post's titles and the cover |
| `references/voice.md` | a narration with the time of every word |
| `references/music.md` | beds, beats and sound effects |
| `references/review.md` | the critic, the two reports and the viewer |
| `references/longform.md` | the edit job's files |
| `references/attention.md` | the map to Hydra's craft |
| `references/research.md` | what the research of September 2026 adds up to; the reports are in `docs/research/` |
