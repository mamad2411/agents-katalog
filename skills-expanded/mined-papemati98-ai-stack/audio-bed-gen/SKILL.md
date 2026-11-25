---
name: audio-bed-gen
description: Generate instrumental background music beds, short stingers, loops, and mix-ready audio assets through OpenRouter music models such as google/lyria-3-pro-preview. Use when Codex needs narration-safe background music for product demos, AI videos, presentations, explainers, intro/outro clips, or final audio mixing with ElevenLabs voice-over. Do not use to imitate copyrighted songs, artists, or generate deceptive audio.
---

# Audio Bed Gen

Run the examples from the directory containing this `SKILL.md`, or set
`SKILL_ROOT` to that directory. Resolve it once before running commands:

```powershell
if (-not $env:SKILL_ROOT) { throw 'Set SKILL_ROOT to the runtime-discovered directory containing this SKILL.md.' }
$SkillRoot = (Resolve-Path -LiteralPath $env:SKILL_ROOT).Path
if (-not (Test-Path -LiteralPath (Join-Path $SkillRoot 'scripts\openrouter_music.py'))) { throw 'Invalid audio-bed-gen SKILL_ROOT.' }
```

Generate narration-safe instrumental music beds and mix them under voice-over. This skill complements `voice-gen` for narration and `video-gen` for visuals.

## Safety

- Never ask the user to paste an API key into chat.
- Use `OPENROUTER_API_KEY` from the local environment, matching `video-gen`.
- Do not write API keys into `SKILL.md`, scripts, prompts, project files, shell history examples, logs, metadata, or reports.
- Do not generate music in the style of a specific living or copyrighted artist.
- Do not generate covers, imitations of known songs, or material that appears to infringe copyright.
- Default to instrumental-only: no vocals, no lyrics, no choir, no spoken phrases.
- For narrated videos, music must support the voice-over, not compete with it.

## Model Selection

Use model discovery before generation:

```powershell
python (Join-Path $SkillRoot 'scripts\openrouter_music.py') check-key
python (Join-Path $SkillRoot 'scripts\openrouter_music.py') list-models
```

Default model: `google/lyria-3-pro-preview`.

Fallback order only after `list-models` confirms availability:
1. `google/lyria-3-pro-preview`
2. `google/lyria-3-clip-preview`
3. another OpenRouter model clearly listed as audio/music generation capable

If no suitable music model is available, report that clearly and do not fake output with a text model.

## Workflow

1. Define asset purpose: music bed, loop, stinger, intro, outro, transition, or final mix.
2. Read `references/music-bed-direction.md` for prompt and mixing guidance. For Vet-Eye, read `references/vet-eye-audio-plan.md`.
3. Run `check-key` and `list-models`.
4. Generate a short draft first, typically 10-20 seconds.
5. Probe the output with `ffprobe`.
6. If the draft works, generate the target-length bed.
7. Mix with voice-over using `scripts/mix_audio.py`, prioritizing narration intelligibility.
8. If muxing into video, keep the original video stream and replace/add audio only.
9. Report model, prompt, duration, format, output paths, whether vocals/lyrics were avoided, and any fallback.

## Script Usage

Check key:

```powershell
python (Join-Path $SkillRoot 'scripts\openrouter_music.py') check-key
```

List music/audio models:

```powershell
python (Join-Path $SkillRoot 'scripts\openrouter_music.py') list-models
```

Generate custom music:

```powershell
python (Join-Path $SkillRoot 'scripts\openrouter_music.py') generate `
  --model "google/lyria-3-pro-preview" `
  --duration 15 `
  --prompt "Original instrumental modern medical technology music bed, calm, warm, narration-safe, no vocals, no lyrics" `
  --out "output/audio/music-test.mp3" `
  --meta-out "output/audio/music-test.meta.json"
```

Generate Vet-Eye music bed:

```powershell
python (Join-Path $SkillRoot 'scripts\openrouter_music.py') generate-vet-eye `
  --duration 115 `
  --out "output/audio/vet-eye-music-bed.mp3" `
  --meta-out "output/audio/vet-eye-music-bed.meta.json"
```

Probe audio:

```powershell
python (Join-Path $SkillRoot 'scripts\openrouter_music.py') probe `
  --input "output/audio/vet-eye-music-bed.mp3"
```

Mix voice-over with music:

```powershell
python (Join-Path $SkillRoot 'scripts\mix_audio.py') mix `
  --voiceover "output/audio/dog_tor_voiceover_pl.wav" `
  --music "output/audio/vet-eye-music-bed.mp3" `
  --out "output/audio/dog_tor_voiceover_with_music.wav" `
  --duration 115
```

Mux mixed audio into video:

```powershell
python (Join-Path $SkillRoot 'scripts\mix_audio.py') mux-video `
  --video "output/video/vet_eye_smart_imaging_demo.mp4" `
  --audio "output/audio/dog_tor_voiceover_with_music.wav" `
  --out "output/video/vet_eye_smart_imaging_demo_dog_tor_audio_v1.mp4"
```

## Output Report

When finished, report:
- created files;
- model used;
- prompt;
- music duration;
- audio format;
- whether final video has audio;
- whether vocals/lyrics were avoided;
- whether secrets were not logged;
- errors and fallback if any.
