---
name: godot-audio
description: Audio in Godot 4.7 - bus layout and effects, volume in linear vs dB, SFX players with polyphony and randomization, 3D positional audio (attenuation, doppler, Area reverb buses), adaptive music with AudioStreamInteractive/Synchronized/Playlist, procedural audio and capture, import/loop settings, web playback type. Use for sound effects, music systems, mixers or audio settings menus.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#).
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Audio (4.7)

Headless runs use the Dummy audio driver, so code paths execute but nothing is heard. Ask the user to listen.

## Bus layout (`default_bus_layout.tres`)
`Master` ← `Music`, `SFX` (← `UI`, `Footsteps`), `Voice`, `Ambience`. Players pick a bus (`bus = &"SFX"`). Put effects on buses, not per player: Reverb on an `SFX_Reverb` bus fed by sends, a Compressor on Music with a voice sidechain (ducking), and `AudioEffectHardLimiter` on Master (`AudioEffectLimiter` is deprecated).
Code: `AudioServer.get_bus_index(&"Music")`, `set_bus_volume_linear(i, 0.8)` (4.4+; use it for sliders), `set_bus_volume_db`, `set_bus_mute`, `add_bus_effect` and `set_bus_effect_enabled`.
Settings sliders should be **linear 0..1**. `linear_to_db()`/`db_to_linear()` convert when needed. Never put dB on a slider directly.

## Players
- `AudioStreamPlayer` (UI and music), `AudioStreamPlayer2D` and `AudioStreamPlayer3D` (positional). `volume_linear` exists too.
- Overlapping SFX (gunshots, footsteps): raise `max_polyphony` on one player instead of spawning players. Use `AudioStreamRandomizer` (random pitch in semitones, 4.7 `random_pitch_semitones`, random volume, several variations) as the stream.
- Fire and forget: spawn a player, `play()`, then `finished.connect(queue_free)`. Pool them for heavy use (see the reference).
- 3D: tune `unit_size` and `max_distance`, `attenuation_model` (inverse, inverse square, log, disabled), `attenuation_filter_cutoff_hz` (muffles distance), `doppler_tracking` on the player **and** the `AudioListener3D`/camera, and `panning_strength`. Reverb zones: `Area3D.reverb_bus_enabled` + `reverb_bus_name`, or `audio_bus_override`.
- 4.7 change: `AudioStreamPlayer2D/3D.area_mask` defaults to 0. If you rely on Area bus overrides, set the mask to the areas' layer.

## Music systems (no code-side crossfading hacks)
- `AudioStreamInteractive`: clips (intro, explore, combat, boss) plus transition rules (`add_transition(from, to, from_time, to_time, fade_mode, fade_beats, …)`) with beat- or bar-synced switches. Switch at runtime with `(player.get_stream_playback() as AudioStreamPlaybackInteractive).switch_to_clip_by_name(&"combat")`. Set BPM, beat count and bar beats on the imported Ogg/WAV for musical timing.
- `AudioStreamSynchronized`: layered stems that play in sync. Fade layers with `set_sync_stream_volume(i, db)` (vertical layering).
- `AudioStreamPlaylist`: sequential or shuffled tracks with fades.
- Keep music on its own player under the `Music` bus. Set `process_mode = PROCESS_MODE_ALWAYS` if it should keep playing in pause menus.

## Import
Use Ogg Vorbis for music and long ambience (streamed) and WAV for short SFX (low latency). Set loops in the Import dock (`loop` for Ogg, `edit/loop_mode` for WAV) instead of in code. Trim silence on import for snappy SFX.

## Procedural and analysis
- `AudioStreamGenerator` + `push_frame()`/`push_buffer()` in `_process`, for synths and retro beeps.
- `AudioEffectCapture` on a bus records or streams audio. `AudioEffectSpectrumAnalyzer` + `get_magnitude_for_frequency_range` makes visualizers.
- Microphone: `AudioStreamMicrophone` needs `audio/driver/enable_input = true` and OS permission on mobile.

## Web and mobile
- Web: browsers block audio until the first user input, so start music after a click or tap. The default playback type can be set to Sample (`audio/general/default_playback_type`, experimental) for lower latency on web.
- Mobile: keep simultaneous voices low. Pause audio on `NOTIFICATION_APPLICATION_PAUSED`.

Bus volume settings, SFX pool, adaptive music controller, procedural beep (compiled by the tests): [references/patterns.md](references/patterns.md)
