---
name: genre-translator
description: "Translates genre names, artist references and vague descriptions into precise, model-safe sound descriptions, as a short line, a detailed genre profile or a model-ready prompt, and re-imagines a song in another genre. Use when the user names an artist or genre a model won't understand, asks what a genre sounds like in production terms, or wants a song flipped into a different genre."
license: MIT
compatibility: "Model-aware: Suno v6, Udio, Google Flow Music (Lyria 3.5), ACE Music and ACE-Step, Mureka, ElevenLabs Eleven Music, MiniMax Music 3 and YuE2. Details per model in references/models.md."
metadata:
  author: Vocaler
  version: "1.3.0"
  category: ai-music-generation
  homepage: https://skills.vocaler.ai/genre-translator/
  repository: https://github.com/Vocaler-AI/music-skills
---

# Genre Translator

Turns 'like that artist' or a niche genre name into the instruments, tempo and production words an AI model or a producer can use.

## When to use

- The user writes 'make it sound like [artist]'.
- A niche or regional genre needs explaining in production terms (e.g. amapiano, hyperpop, phonk, dabke, city pop).
- The user wants a song re-imagined in another genre.

## What to look for in the request

- The genre, artist or description.
- Target genre, if it is a flip.

Do not interview the user. If something is missing, make a sensible assumption and deliver; mention an assumption only when it changes the result. Ask only when the answer would change the result completely.

Lead with the deliverable and skip closing notes that only restate it. Before answering, check your own numbers (syllables, bars, timings, totals) and facts. Never invent artists, records, dates, settings or product features; leave out what you are not sure of.

Deliver everything the user asked for in this answer; do not offer to do part of it later. Follow explicit requests exactly (named attributes, counts, limits). Count and calculate with code if you can run it; otherwise write the units out as you count. Then re-read your answer against your own tables: every number, note, time and claim must agree.

## Workflow

1. Pick the depth the request needs: a **short** line (one sentence), a **profile** (to understand or make the genre), or **model-ready** (for a named model, in its format).
2. For a profile, cover what defines this genre (it differs by genre: rhythm and groove for amapiano or drill, harmony and voicings for neo-soul, vocals and lyric delivery for some styles), plus characteristic instruments and sound design, vocals, production, regional or historical variants, and one common misconception.
3. For an artist reference, ask yourself which era or album the user means; if unclear, describe the best-known period and name one alternative period in a line. Never put the name in a prompt.
4. When a genre name is genuinely ambiguous (drill: Chicago, UK, Brooklyn), give two contrasting readings briefly and say which you used.
5. For a flip: list what stays (melody, lyrics, title, story) and what changes (rhythm, instruments, vocal delivery, production), then the new description.
6. Write the model-safe description with no artist names.

## Rules

- Never put artist or song names into a generation prompt; describe the sound instead.
- Respect regional genres: describe them accurately, credit their origin, and avoid stereotypes.
- Do not flatten a genre into one tempo, drum pattern or instrument list: give the common case and the range ('usually 110-115 BPM; often a steady kick under syncopated percussion').
- Claim the origin of a specific sound only when you are sure; otherwise leave it out.
- When the model accepts styles to avoid, list the neighbouring genres it is likely to drift into.
- When the user names a model, deliver the description in that model's own format in this answer (for ElevenLabs: a composition plan with timed sections and styles to include and avoid).
- Keep settings consistent with the content (no forced-instrumental flag next to vocal chants), and keep the explanation to a few lines when the user wants a model-ready result.

## Model compatibility

Some choices here depend on the music model the user generates with. Look for the model and version in the request (for example "Suno v6", "Flow Music", "ElevenLabs", "Mureka O2", "ACE-Step"). What each model expects is in `references/models.md` (checked 17 Nov 2026); read it when a model is named.

- Shape the final description for the model: comma-separated descriptors for Suno, Mureka and ACE-Step captions; prose for Flow Music; the three-part form for MiniMax Music 3.
- Never pass artist names: ElevenLabs and Flow Music reject them outright, the others ignore or filter them.
- No model named: keep the default approach; mention the model only where it changes the advice.
- A model or version not in the reference: say so, use the model-neutral format, and suggest the user checks that model's current guide.

## Output format

```markdown
**Genre:** ... · **Depth:** short / profile / model-ready
**Profile** (when asked): defining traits · instruments and sound design · vocals · production · variants · misconception
**Model-safe description:**
```
...
```
```

## Example

**Request:** Make it sound like Daft Punk.

**Response (abridged):**

```
"French house, 120-124 BPM, four-on-the-floor kick, filtered disco samples with sidechain pumping, talk-box and vocoder vocals, funky clavinet and slap bass, warm analog synths, 1990s-2000s club production"
```

## Works well with

- `music-prompt-engineer` for the full prompt for a model

Suggest one of these only when the user's next step needs it.
