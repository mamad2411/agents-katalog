---
name: soundbox-sfx
description: Generate sound effects, foley and ambience locally through the Soundbox MCP server (soundbox.generate / list_sounds / list_models). Use whenever the user wants a sound effect, game SFX, UI sound, ambience bed or any non-spoken audio, or asks to "make a sound", "add sound effects", "generate a whoosh/impact/click". Produces WAV files on disk with absolute paths.
---

# Soundbox: generate sound effects through MCP

Soundbox is a local server that runs open-weight text-to-audio models and
exposes them as MCP tools. You do not need an API key; the user's machine does
the work. Every result is a WAV file on disk and the tool response gives you its
absolute `path`.

## Tools you have

| Tool | Use it for |
|---|---|
| `soundbox.list_models` | Which models are installed/loaded, their max clip length and **licence** |
| `soundbox.list_sounds` | Search the library — the sound may already exist |
| `soundbox.generate` | Make new sounds; blocks until the file is written (seconds to ~1 min) |
| `soundbox.get_sound` | Re-fetch a sound's path/metadata by id |
| `soundbox.delete_sound` | Remove a bad take (only when the user asks) |

If a tool errors with "Cannot reach the Soundbox server", tell the user to
start it (`uv run soundbox`, or open the Soundbox app) — do not try to install
or run models yourself.

## Workflow

1. **Search first.** `soundbox.list_sounds(q=<key nouns>)`. If a hit fits,
   return its `path` — don't regenerate what exists.
2. **Check the model once per session.** `soundbox.list_models`; note which
   is `loaded` (fastest) and its `commercial_use`. If the user's project is
   commercial and the loaded model says `no`, say so before generating and
   pick a `yes`/`conditional` model if one is installed.
3. **Write the prompt as a sound designer would** — see
   [references/prompting.md](references/prompting.md). Material + action +
   space, present tense, no adjectives about emotion:
   - ✅ `heavy oak door slamming shut in a stone corridor, short reverb tail`
   - ❌ `scary door sound`
4. **Pick a duration that matches the event.** One-shots (clicks, hits,
   whooshes) 0.5–2 s; short foley 2–4 s; ambience beds 8–20 s. Long clips of a
   one-shot waste time and produce silence.
5. **Ask for variations when it's a set.** `variations=3` gives three takes of
   the same prompt with different seeds — right for footsteps, hits, UI blips.
   Pass a `seed` back to reproduce a take the user liked.
6. **Tag and name for the library.** `tags=["ui","confirm"]` or the project
   name, so the user can find things in the Soundbox app afterwards.
7. **Return the paths.** Give the user each file's absolute `path`, duration
   and model — and, if you wired the sound into code, the snippet you wrote.

## Handling results

- The response is `{"sounds":[{id,name,path,duration_s,model,seed,...}], model, elapsed_s}`.
- Prefer copying/moving the WAV into the user's project (`assets/sfx/...`)
  over referencing `~/.soundbox/sounds/` from their code.
- Need MP3/OGG? Convert with ffmpeg from the WAV; Soundbox writes WAV.
- Loudness is already normalised (default −16 LUFS) and leading/trailing
  silence trimmed unless the user changed settings.

## When the first take is wrong

Iterate on the prompt, not on the seed:
- Too much reverb / room → add `dry, close-mic`, or `no reverb` in `negative_prompt`
- Wrong material → name it explicitly (`ceramic`, `sheet metal`, `wet gravel`)
- Sounds like music / has a melody → `negative_prompt="music, melody, tones"`
- Too busy → describe **one** event; generate layers separately and let the
  user mix them
- Cuts off → longer `duration_s`; too short an event padded with silence →
  shorter

Only after the prompt is right, use `variations` to get options.

## When it is not this skill

Spoken words are a different set of tools, not a different prompt. For a line
of dialogue, a narration, or a whole scripted scene, use the voice tools —
`soundbox.list_voices`, `soundbox.speak`, and the story tools — and see the
`soundbox-voice-story` skill. `soundbox.generate` will not say words; asking it
to produce "a man saying hello" gets you a texture, not speech.
