---
name: voice-gen
description: Generate, test, and manage AI voiceover audio through ElevenLabs text-to-speech. Use when Codex needs narration, voiceover, podcast/dialogue snippets, product demo audio, explainer voice, ad reads, localization reads, character voices, or project-bound audio assets. Includes a local DPAPI-based secret gateway for ELEVENLABS_API_KEY, voice/model discovery, safe TTS generation, and output reporting. Never ask the user to paste an ElevenLabs API key into chat.
---

# Voice Gen

Run the examples from the directory containing this `SKILL.md`, or set
`SKILL_ROOT` to that directory:

```powershell
if (-not $env:SKILL_ROOT) { throw 'Set SKILL_ROOT to the runtime-discovered directory containing this SKILL.md.' }
$SkillRoot = (Resolve-Path -LiteralPath $env:SKILL_ROOT).Path
if (-not (Test-Path -LiteralPath (Join-Path $SkillRoot 'scripts\elevenlabs_voice.py'))) { throw 'Invalid voice-gen SKILL_ROOT.' }
```

Generate voiceover assets through ElevenLabs TTS. Use this skill alongside `imagegen` and `video-gen` when a project needs a complete audio-visual asset stack.

## Safety

- Never ask the user to paste an API key into chat.
- Prefer the local DPAPI gateway:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $SkillRoot 'scripts\elevenlabs_key.ps1') set
```

- The generation script reads `ELEVENLABS_API_KEY` from the current environment, Windows User/Machine environment variables, or the DPAPI gateway file.
- Do not write API keys into `SKILL.md`, scripts, prompts, project files, logs, reports, or shell history examples.
- Do not clone voices, imitate living people, or generate deceptive impersonation unless the user explicitly provides the rights/consent and the use is legitimate.
- Label generated audio as generated when used as evidence, compliance material, or client-facing review material.

## Workflow

1. Clarify the audio job: narration, ad read, app voice, dialogue, character, localization, tutorial, or temp voice.
2. Write or polish the script for speech. Keep it natural: short sentences, clear pauses, pronunciation notes, and no visual-only wording.
3. Check the key and quota before paid generation:

```powershell
python (Join-Path $SkillRoot 'scripts\elevenlabs_voice.py') check-key
```

4. Discover models and voices when the current roster matters:

```powershell
python (Join-Path $SkillRoot 'scripts\elevenlabs_voice.py') list-models
python (Join-Path $SkillRoot 'scripts\elevenlabs_voice.py') list-voices --limit 20
```

5. Choose a voice by `voice_id`. If no voice is specified, ask the user to choose from `list-voices`; do not guess for final assets.
6. Generate a short sample first, then final audio:

```powershell
python (Join-Path $SkillRoot 'scripts\elevenlabs_voice.py') tts `
  --voice-id "<voice_id>" `
  --text "The first move is what sets everything in motion." `
  --model "eleven_multilingual_v2" `
  --out "output/voice/sample.mp3"
```

7. Listen or inspect the output before using it. Check pacing, pronunciation, tone, clipping, and whether the voice fits the target audience.
8. Save project-bound audio under the project or deliverable asset folder, not temp.

## Defaults

- Stable default model: `eleven_multilingual_v2`.
- Stable default output format: `mp3_44100_128`.
- For expressive creative reads, run `list-models` and pick the current expressive TTS model available on the account.
- For real-time or draft reads, choose a low-latency model only after `list-models` confirms it is available.

## Voice Direction

Give the model performance direction through the script, not hidden magic:
- Use punctuation for pacing.
- Add pronunciation notes in the text only when needed.
- For ads: specify audience, energy, and CTA.
- For tutorials: prefer calm clarity over theatrical delivery.
- For characters: define age range, texture, emotional state, and scene context.

## Output Report

When finished, report:
- voice id and voice name if known;
- model id;
- prompt/script source;
- output format;
- output audio path;
- whether the asset is generated, draft, or final.

## Source Notes

Read `references/elevenlabs-api.md` for the checked endpoint map and doc links.
