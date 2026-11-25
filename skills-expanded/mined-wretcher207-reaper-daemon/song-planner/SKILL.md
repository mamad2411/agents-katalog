---
name: song-planner
description: Plan a whole song (form, bars, tempo, key or tuning, drum feel, riffs, extra layers) as a song sheet, get the person's approval, then draft drums, guitars, bass and layers into a new REAPER project tab. Use when someone wants a song started from a written brief, from a riff they played, or from the structure of a reference song.
---

# Song planner

The deliverable is a song the person wants to keep working on. A valid sheet
and a clean draft are the means. The order is fixed and never skipped:

1. **Gather** what the person gave you (brief, riff, reference).
2. **Ask** once, in one short batch, about anything material they left out.
3. **Write the sheet** (`songs/<slug>/sheet.json`) and run `songplan.py check`.
4. **Show** it (`songplan.py show`) and wait for an explicit yes or edits.
   Choosing an option or saying "sounds cool" about one section isn't approval
   of the whole sheet.
5. **Approve** (`songplan.py approve`) only after that yes. Any later edit
   cancels the approval automatically.
6. **Draft** (`songplan.py draft`). It writes into a NEW project tab only.
7. **Audition and revise** with the narrow tools (drum workshop, `shred`,
   `humanize`, `insert_midi_events`), not by redrafting the whole song.

The sheet format and the drafting steps are in `docs/song-planner.md`. The
engines underneath are `skills/drum-apparatus` (drum DSL) and
`skills/guitar-apparatus` (16-cell riff notation). Read the relevant one before
writing drum lanes or riff bars.

## No house style

There are no default tempos, tunings, forms or section lengths. Every choice
comes from what the person said or answered. Don't reach for a "metal song
template", a past project, or the last song's settings. If the brief says
"fast", ask what fast means here rather than picking a BPM.

Ask before writing when these are missing and the input doesn't settle them:
tempo (or a feel you can ground), tuning/low note, rough length or form, which
instruments (from `reaperd.py instrument list`), and the energy arc. Keep it to
one batch. Things the person clearly delegated ("you pick the fills") are yours.

Keep one **wildcard** section or idea in every plan, marked `"wildcard": true`,
so the draft isn't only the obvious reading of the brief.

## From a brief

Turn the words into sections with a job each: what changes, where the energy
goes, where it breathes. Write drum lanes and riff bars that serve that job.
For drum ideas beyond the obvious, run the drum workshop (fresh, contrast and
wildcard candidates) for the key sections and put the chosen DSL lanes in the
sheet. Record the brief verbatim in `source.detail`.

## From a riff the person played

The riff is the anchor, so preserve it. Find it in REAPER (`get_context`,
`get_items`), read it with `reaperd.py riff` / `profile` for audio or
`get_midi_notes` for MIDI, and confirm the tempo and the low note. Transcribe it
into 16-cell riff bars and say which cells you're unsure of. Their riff goes in
its section unchanged. Build the other sections as contrast or development
around it. Never quietly "fix" their timing or notes.

## From a reference song

Take the form only: section order, bar counts, tempo, energy arc, where it
breaks down. Measure it from the audio rather than recalling it from memory, and
state your confidence per boundary. Never copy the reference's riffs, melodies
or drum patterns into the sheet. The parts are new; only the shape is borrowed.
Put the reference and what you took from it in `source.detail`.

## Writing the sheet

- 4/4 and one tempo per song are hard limits of the engines right now. If the
  person wants a meter or tempo change, say so before planning around it.
- `parts` names instruments from the library. An instrument without a saved
  chain still drafts its MIDI, but the track will be silent until the sound
  is loaded and saved (`reaperd.py instrument save`). Tell the person that.
- Drum lanes: lane names and cells per `skills/drum-apparatus`. `feel` sets the
  dynamic center (`ppp`..`fff`); the engine applies humanizing and the golden
  rule, so don't hand-write velocities for drums.
- Riff bars: exactly 16 cells each; a section's riff repeats to fill its bars.
  Bass follows the guitar riff (its roots), so a section where only bass plays
  can't be expressed yet. Say so if the idea needs it.
- Layers (pads, leads, textures): notes in beats from the section start. Check
  register against the instrument's range and the guitars' low end.
- `check` must pass before `show`. Fix every listed problem; don't argue with it.

## After the draft

Report each step's result as the tool printed it, including any track left
silent for lack of a saved sound. A draft that wrote MIDI is ready to audition,
not finished: listening is the acceptance test. Never save the project for the
person; the draft tab stays unsaved until they save it.
