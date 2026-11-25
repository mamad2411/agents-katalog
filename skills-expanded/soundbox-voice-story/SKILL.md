---
name: soundbox-voice-story
description: Write, voice and arrange spoken audio locally through the Soundbox MCP server — one-off narration with soundbox.speak, or a persistent multi-track "story" (create_story / add_lines / speak_story / export_story). Use whenever the user wants dialogue, narration, a voiceover, a scripted scene, a podcast segment, character lines for a game, or asks to "read this aloud", "make a voiceover", "write a scene with two characters". Produces WAV files on disk with absolute paths.
---

# Soundbox: speech, scripts and stories

Soundbox runs text-to-speech models on the user's machine and exposes them over
MCP. No API key; their hardware does the work. Every result is a WAV on disk and
the response gives you its absolute `path`.

This is the *spoken* half of Soundbox. `soundbox.generate` makes sound effects
and music and will not say words — asking it for "a man saying hello" gets you a
texture. For anything with words in it, use the tools below.

## Which shape of job is this

**One read, nothing to keep** → `soundbox.speak`. A line, or several lines with
different voices for a dialogue. Comes back as one joined sound.

**Something you will revise** → a story. A story persists, every line can be
re-read on its own without touching the others, and the lines carry a place in
time so they can be arranged and mixed down. Use it for a scene, a narration
over other audio, a podcast segment, anything where the user will say "the
third line sounds wrong".

If in doubt, build a story. Re-reading one line of a story costs seconds;
re-running `soundbox.speak` on a changed script re-reads all of it.

## Tools

| Tool | Use it for |
|---|---|
| `soundbox.list_voices` | The cast. Do this first — lines need real voice ids |
| `soundbox.speak` | One-off read, no story kept |
| `soundbox.create_story` | Start a script that persists |
| `soundbox.list_stories` / `soundbox.get_story` | Find and inspect what exists |
| `soundbox.add_lines` | Append lines, pauses, or existing library sounds |
| `soundbox.update_line` | Reword, recast, or move a line in time |
| `soundbox.speak_story` | Read every line that has no audio yet. **Slow** |
| `soundbox.export_story` | Mix the arrangement down to one sound |
| `soundbox.open_in_studio` | Put an existing library sound on a timeline, split into stems |
| `soundbox.delete_line` / `soundbox.split_line` | Remove a line, or cut a voiced one in two |
| `soundbox.mix_track` | Name, mute, solo or set the level of a whole lane |
| `soundbox.add_device` / `set_device` / `remove_device` | A lane's effects: EQ, compressor, reverb and the rest |
| `soundbox.remove_track` | Delete a lane and the clips on it |

## The workflow

1. `soundbox.list_voices`. Note the ids and which are `builtin` — a builtin
   belongs to one model family and fails with any other model.
2. `soundbox.create_story` with a title that says what it is.
3. `soundbox.add_lines` — the whole script in one call. Give every line a
   `speaker` even when the voice is the same; it is what makes the script
   readable back to the user.
4. `soundbox.speak_story`. This is the minutes-long step: one subprocess per
   line. Tell the user before you start. Leave `model` off: each line is read
   on its own voice's model (`model_id` in `list_voices`), and passing one
   reads every voice on it. If the result has `notes`, a voice's model was not
   installed and its lines were read on another; tell the user.
5. `soundbox.get_story` to see what landed, then `soundbox.update_line` for
   anything wrong, then `speak_story` again — it only re-reads silent lines
   unless you pass `regenerate: true`.
6. `soundbox.export_story` when the user wants one file.

## Casting

A line with no `voice_id` uses the model's default voice, and some families
(Chatterbox and other cloning-only models) have no default at all — those lines
fail. Cast every line explicitly unless you have checked otherwise.

Two characters should get two voices. A dialogue read entirely in one voice is
the most common way this comes out wrong, and it is invisible until playback.

## Timing

Lines lay out end to end as they are voiced, which is right for dialogue and
wrong for anything overlapping. To place audio deliberately:

- `track_index` is the lane. Different lanes play at once — narration on 0,
  music bed on 1.
- `start_s` is when it starts. Omit it and the line follows whatever is already
  on its track.
- `duration_s` with `trim_start_s` shortens a clip without destroying audio, so
  a clip can always be lengthened again.
- A `kind: "pause"` line is a written beat of silence; its length is
  `duration_s`. Prefer it to padding text with full stops.

`soundbox.add_lines` also takes a `sound_id`, which drops an existing library
sound onto the timeline — a music bed under narration, or an effect from
`soundbox.generate`.

## Mixing

`soundbox.mix_track` controls a whole lane: name, mute, solo, level. These
belong to the lane, not the clips on it, so muting a track does not forget
which individual clips you had silenced. Solo beats mute — the moment anything
is soloed, only soloed lanes are heard.

Each lane also has an insert chain, the studio's device rack.
`soundbox.add_device` puts an EQ, compressor, reverb, delay, distortion, gate,
limiter or autotune on it; `soundbox.set_device` turns knobs or bypasses one;
`soundbox.remove_device` takes it off. Values are in stored units: seconds,
not milliseconds. "Warmer" on a voice is usually a little low lift and a high
cut on the EQ; "tame the sibilance" is a high cut and gentle compression. The
user hears devices in the studio, but `soundbox.export_story` mixes dry, so say
so before an export that depends on them.

Name your lanes when a story has more than one. "Track 1" tells the user
nothing; "Narration" and "Music bed" tell them what they are looking at.

`soundbox.remove_track` deletes the lane *and its clips*, and lanes above slide
down. Check `soundbox.get_story` first if you are not certain what is on it —
this is not something undo covers.

## Delivery

How a line is *performed* is a separate lever from what it says, and it is not
in the text. Writing `(whispering)` into a line makes the model say the word
"whispering" out loud. Pass `delivery` instead:

- `soundbox.create_story` — for the whole script. Usually the right place: one
  delivery throughout, exceptions on a line or two.
- `soundbox.add_lines` — per line, when you already know one line differs.
- `soundbox.update_line` — for the exception you found afterwards. `{}` puts a
  line back on the story's. Either way the line has to be re-read before the
  change is audible.

**The names differ per model family, and `soundbox.list_models` is the
authority.** A text-to-speech model returns a `delivery` list — each entry with
its range, its default, and which group it belongs to. `delivery` entries in
the `"delivery"` group change the performance; `"sampling"` and `"quality"`
change how hard the model works at it.

Two things make guessing expensive:

- **An unknown name is ignored silently.** Not an error — a setting that does
  nothing. `exaggeration` is real on Chatterbox; `emotion`, `speaking_rate` and
  `instruct` are not, and passing them looks identical to passing nothing.
- **A model with no `delivery` list has no knobs at all.** Its words and its
  voice are the only controls. Say so rather than pretending otherwise.

Worked example — Chatterbox, whose one real performance knob is `exaggeration`
(0–2, default 0.5):

```json
{ "title": "Interrogation", "delivery": { "exaggeration": "1.4" } }
```

## Getting the read right

Delivery knobs are a small lever; the words are a large one. The model reads
what you write, including punctuation, so rewrite for the ear before reaching
for settings:

- Spell out what should be spoken: "twenty sixteen", not "2016"; "THQ Nordic",
  not "THQ."
- Commas and full stops become pauses. A comma where you want a beat is more
  reliable than hoping.
- Keep a line to a sentence or two. Long paragraphs drift in delivery and cost
  you the whole line when one word is wrong.

## Reporting back

The story tools answer with a short summary — how many lines, how many are
voiced, how long it runs — and an `open_in_studio` link. Hand the user that
link. A timeline is a thing to look at, and listing its clips back at them in
chat is not the same as showing it; it is also how you fill a conversation with
JSON nobody reads.

Say what changed and give the link. "Six lines, all voiced, 41s — open it in
the studio: <link>" is the whole report. Reach for `soundbox.get_story` only
when you need the lines to reason about them.

## Say what it cost

Speaking is slow and runs on the user's GPU. Before a long `speak_story`, say
roughly how many lines are about to be read. After exporting, give the absolute
path — that is the thing they actually wanted.
