---
name: minimax-h3-native-audio-music-video
description: Create, direct, continue, and finish MiniMax H3 music videos in ComfyUI while preserving the supplied source song as exact output audio. Use for native-audio H3 clips, vocal lip-sync prompting, non-vocal performance shots, song segmentation, reference-to-video identity locking, continuation series, or RIFE 120 fps interpolation and 60 fps delivery. Use with minimax-video-series for long-form continuity, review, manifests, assembly, and archive publishing.
---

# MiniMax H3 Native-Audio Music Video

Use the installed `MiniMaxH3NativeAudioLock` node to place supplied audio in H3's joint AV latent, mask audio denoising, and return the same trimmed audio for the saved video. Use `$minimax-video-series` for chapter planning, exact-frame handoffs, review, manifests, concatenation, and publishing.

## Installed components

- Main workflow: `C:\Users\Admin\ComfyUI\user\default\workflows\MiniMaxH3_NativeAudio_MusicVideo_TEMPLATE.json`
- RIFE workflow: `C:\Users\Admin\ComfyUI\user\default\workflows\RIFE_WAN_Method_Interpolation_TEMPLATE.json`
- Audio-lock node: `C:\Users\Admin\ComfyUI\custom_nodes\ComfyUI-H3-NativeAudioLock`
- Frame interpolation: `C:\Users\Admin\ComfyUI\custom_nodes\ComfyUI-Frame-Interpolation`
- RIFE 4.7 checkpoint: `C:\Users\Admin\ComfyUI\custom_nodes\ComfyUI-Frame-Interpolation\ckpts\rife\rife47.pth`
- Required Ref2VA model: `C:\Users\Admin\ComfyUI\models\diffusion_models\minimax_h3_ref2va_pruned_int8_convrot.safetensors`
- Reused encoder: `MiniMax-H3\qwen3vl_32b_minimax_h3_ultra_uncensored_heretic_int8_convrot.safetensors`

Read [references/upstream-and-runtime.md](references/upstream-and-runtime.md) when installing, updating, debugging nodes, or checking provenance. Read [references/official-prompt-adapter.md](references/official-prompt-adapter.md) before directing vocals, instrumentals, diegetic performance, multiple shots, exact lyrics, or visible text.

## Preflight

Run:

```powershell
& 'C:\Users\Admin\ComfyUI\.venv\Scripts\python.exe' `
  'C:\Users\Admin\.codex\skills\minimax-h3-native-audio-music-video\scripts\verify_install.py'
```

Require both `MiniMaxH3NativeAudioLock` and `RIFE VFI` in the running ComfyUI API. If files exist but nodes are missing, restart ComfyUI once and inspect startup logs before changing dependencies.

Copy [assets/music-video.example.json](assets/music-video.example.json) into the project area, replace the placeholders, then lint and inspect every exact prompt:

```powershell
python "$env:USERPROFILE\.codex\skills\minimax-h3-native-audio-music-video\scripts\native_audio_prompt.py" lint --config C:\path\music-video.json
python "$env:USERPROFILE\.codex\skills\minimax-h3-native-audio-music-video\scripts\native_audio_prompt.py" compile --config C:\path\music-video.json --segment 1
```

## Build one native-audio clip

1. Open the main workflow template.
2. Select the character/style reference image.
3. Load the full song, then set `TrimAudioDuration` to the exact scene start and end.
   The audio trim is exact; the video duration must use the next valid H3 frame-grid length described below, not an arbitrary second value.
4. Set the H3 duration control to the valid frame-grid length calculated below. Prefer 5-15-second chapters.
5. Paste the exact compiled segment prompt into the workflow. Keep project metadata out of that prompt.
6. Keep `MiniMaxH3NativeAudioLock` between `MiniMaxH3ReferenceToVideo` and the sampler.
7. Feed the node's `exact_audio` output to `CreateVideo`. Do not use the generated audio decode for the final mux.
8. Keep the Ref2VA INT8 model and the installed Heretic MiniMax encoder selected.
9. Render one take, inspect motion and audio sync, and accept or reject before continuing.

The lock prevents H3 from denoising the supplied audio latent; it does not guarantee visually perfect mouth motion or a byte-identical encoded track. Judge lip sync from the rendered video and use the source song once during final assembly.

## Respect the H3 timing grid

H3 video lengths follow `17k+5` frames. At 24 fps, an exact 10-second window is 240 frames, but the workflow must render 243 frames (10.125 seconds). Compute:

```text
target_frames = round(chapter_seconds * 24)
render_frames = max(5, target_frames) + (5 - (max(5, target_frames) % 17)) % 17
continuation_index = target_frames - 1
```

Trim the conditioning audio to the exact chapter window, render `render_frames`, and direct a stable hold through `continuation_index`. Review and retain only frames `0..continuation_index`; use that indexed frame as the next chapter reference. Assemble the retained, video-only windows to the exact target frame count before muxing audio.

For example, three exact 10-second chapters each render 243 frames but contribute 240 accepted frames. Their silent 24 fps master is exactly 720 frames and 30 seconds. Discard each chapter's encoded audio and mux the untouched full 30-second source song once at final assembly.

## Prompt music-video performance

Use one character reference for each new scene. The compiler emits this locked-audio adaptation:

```text
Use <Picture 1> as the exact identity, wardrobe, style, and scene reference. Use <Audio 1> as the exact performance timeline.

integrated_multimodal_description: [Shot 1] [Visible chronological performance, camera, exact verified singing or closed-lip instrumental direction, and terminal tableau.]

overall_soundscape: [One to four complete sentences describing only separate ambience, actions, and non-verbal sounds.]

non_diegetic_music: [One to three factual sentences describing audience-only instrumentation, tempo, rhythm, and dynamics, or N/A.]
```

For vocal timestamps without verified lyrics, refer only to the exact supplied vocal audio; never invent or transcribe words. When the user supplies verified lyrics, preserve every character inside `<d>[Language] ...</d>` and use a stable speaker ID.

For instrumental timestamps, write: `lips remain fully closed for every frame; perform through body, hands, gaze, and camera rhythm.`

Do not ask for singing during instrumental sections. Do not stack singing, dancing, large camera moves, costume changes, and environment transformations in one short clip.

Treat the official base guide as authoritative for the three core fields, shot grammar, camera language, speakers, exact text, and audio separation. Treat the `<Picture 1>` plus `<Audio 1>` header as a local Ref2VA/AudioLock adaptation because the base guide does not specify R2VA.

## Continue a song as chapters

Segment the song on musical phrases, not arbitrary equal intervals. Record for every chapter:

- exact song start/end timestamps;
- lyric or instrumental state;
- reference image;
- prompt and seed;
- final-frame transition;
- review decision.

Use the accepted prior chapter's indexed final frame as the next reference image. Preserve screen direction and beat phase across a continuation. Use `$minimax-video-series` for the supervised render/review/accept structure, but adapt its ComfyUI graph to include `MiniMaxH3NativeAudioLock`; the standard graph generates its own audio and is not an exact-audio music workflow.

## Interpolate and deliver

Open the RIFE template only after editing and the exact 24 fps frame count are locked. On the RTX 5090, start with float16, batch size 4, and cache clearing every 10 frames; reduce batch size if VRAM pressure appears.

The installed RIFE implementation returns `(N-1)*multiplier+1` frames. A 720-frame master at 5x therefore yields 3,596 frames, not 3,600. Clone the last frame `multiplier-1` times, then explicitly retain every other frame for a 60 fps delivery:

```powershell
ffmpeg -i C:\path\master-120fps.mp4 -vf "tpad=stop_mode=clone:stop=4,select='not(mod(n,2))',setpts=N/(60*TB)" -an -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p C:\path\master-60fps-silent.mp4
ffmpeg -i C:\path\master-60fps-silent.mp4 -i C:\path\original-song.ext -map 0:v:0 -map 1:a:0 -c:v copy -c:a copy -movflags +faststart C:\path\master-60fps.mp4
```

For the example above, require exactly 1,800 frames, 60/1 fps, and 30 seconds. Verify video and decoded-audio durations independently; do not use `-shortest`, which can truncate source audio at packet boundaries. If the source audio codec is not supported by the delivery container, use a lossless compatible audio codec and verify decoded PCM instead of claiming a byte-identical stream. Never mux chapter audio tracks together.

To compare the audible content canonically, hash both source and delivered decoded audio with identical parameters:

```powershell
ffmpeg -v error -i C:\path\original-song.ext -map 0:a:0 -ar 48000 -ac 2 -c:a pcm_s32le -f hash -hash sha256 -
ffmpeg -v error -i C:\path\master-60fps.mp4 -map 0:a:0 -ar 48000 -ac 2 -c:a pcm_s32le -f hash -hash sha256 -
```

Require matching hashes. Interpolate only after chapter replacements and timing edits are final.

## Review rules

- Reject visible identity/anatomy drift, lyrics performed during the wrong timestamp, persistent lip desynchronization, open-mouth motion during instrumental sections, or an unusable final frame.
- Reject a render whose cuts, camera move, visible text, exact words, speaker identity, or diegetic/non-diegetic behavior contradict the compiled prompt.
- Compare source and output duration, stream-copy status where applicable, and canonical decoded-PCM hash.
- Verify the exact accepted 24 fps frame count and final 60 fps frame count; do not infer duration from metadata alone.
- Preserve original 24 fps accepted masters; treat 120/60 fps files as derived deliverables.
- Never stretch audio to repair a video-duration mismatch. Fix chapter duration and rerender.
- Record upstream versions and installed model hashes before updating nodes in a working production.
