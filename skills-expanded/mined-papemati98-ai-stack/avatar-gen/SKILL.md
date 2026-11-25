---
name: avatar-gen
description: Generate audio-driven talking avatar and lip-sync videos from a still image or source video using dedicated avatar/lip-sync APIs such as Hedra. Use when Codex needs a speaking presenter, animated character, talking-head avatar, DOG TOR style narrator, or image-to-video lip-sync synced to pre-recorded audio. Prefer this over general video generation for talking avatars. Never use to impersonate real people deceptively or to create fake evidence.
---

# Avatar Gen

Run the examples from the directory containing this `SKILL.md`, or set
`SKILL_ROOT` to that directory before resolving the scripts:

```powershell
if (-not $env:SKILL_ROOT) { throw 'Set SKILL_ROOT to the runtime-discovered directory containing this SKILL.md.' }
$SkillRoot = (Resolve-Path -LiteralPath $env:SKILL_ROOT).Path
if (-not (Test-Path -LiteralPath (Join-Path $SkillRoot 'scripts\avatar_gen.py'))) { throw 'Invalid avatar-gen SKILL_ROOT.' }
```

Use this skill for audio-driven talking avatars: image or face video plus final audio becomes a lip-synced presenter video. Do not use `video-gen` for speaking mouths; keep `video-gen` for intro, transitions, b-roll, and neutral clips.

## Safety

- Never ask the user to paste an API key into chat, code, manifests, prompts, or CLI arguments.
- Store Hedra credentials through the local DPAPI gateway:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $SkillRoot 'scripts\hedra_key.ps1') set
```

- Check credential presence without printing values:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $SkillRoot 'scripts\hedra_key.ps1') status
python (Join-Path $SkillRoot 'scripts\avatar_gen.py') check-key
```

- The Python helper reads `HEDRA_API_KEY` from current process env, Windows User env, Windows Machine env, or the DPAPI gateway.
- Do not log request headers. Do not save `HEDRA_API_KEY`, raw headers, full curls, or secrets in manifests.
- Do not impersonate real people without rights and consent. Fictional DOG TOR project assets are acceptable.
- If an API returns a watermark, report it. Do not hide it.

## Core Workflow

1. Prepare a stable front-facing avatar image and final voiceover audio. The same audio must be used for the avatar and final video mix.
2. Run `check-key` and `list-models` before paid generation.
3. Generate a 15-25 second proof first. Do not render a full 114 second film until the proof passes visual QC.
4. Inspect the proof for identity drift, mouth timing, eye/nose/glasses deformation, watermark, and whether it still works as a 220-280 px inset.
5. If two avatar providers fail quality, stop and report the limitation instead of returning to generic image-to-video for talking mouths.

## Hedra Commands

List models:

```powershell
python (Join-Path $SkillRoot 'scripts\avatar_gen.py') list-models --meta-out "outputs\avatar_models.json"
```

DOG TOR proof:

```powershell
python (Join-Path $SkillRoot 'scripts\avatar_gen.py') proof-dog-tor `
  --image "outputs\dog_tor_upgrade\assets\dog_tor_reference.png" `
  --audio "outputs\dog_tor_upgrade\audio\dog_tor_voiceover_proof_20s.wav" `
  --out "outputs\dog_tor_avatar_proof\hedra_dog_tor_proof.mp4" `
  --duration-ms 20000 `
  --meta-out "outputs\dog_tor_avatar_proof\hedra_dog_tor_proof.meta.json"
```

Generic generation:

```powershell
python (Join-Path $SkillRoot 'scripts\avatar_gen.py') generate `
  --image "avatar.png" `
  --audio "voice.wav" `
  --prompt "Calm professional presenter, natural lip-sync, stable head position." `
  --duration-ms 20000 `
  --aspect-ratio "1:1" `
  --resolution "720p" `
  --out "talking_avatar.mp4" `
  --meta-out "talking_avatar.meta.json"
```

## References

- Read `references/hedra-api.md` when implementing or debugging Hedra API calls.
- Read `references/dog-tor-avatar-plan.md` when working on Vet-Eye DOG TOR v4, proof timing, QC, and the distinction between avatar generation and the final film montage.
