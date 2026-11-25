---
name: godot-game-feel
description: Game feel and juice in Godot 4.7 - trauma-based screen shake (2D and 3D), hit-stop and slow motion via Engine.time_scale, hit flash shaders, squash and stretch and easing via Tweens, knockback, FOV kicks, damage numbers, randomized sound, rumble, UI juice through offset_transform, accessibility toggles, and recording trailers in Movie Maker. Use when actions feel flat or weak.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#).
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Game Feel and Juice (4.7)

Juice is **feedback layered on a correct mechanic**: tune the controls first (`godot-2d` has coyote time, jump buffering and variable jump height; `godot-3d-gameplay` has controllers), then add feedback. Every player action should answer "did it work, and how much?" within 100 ms through several channels: motion, flash, particles, sound and rumble.

## Toolkit
| Effect | Recipe | Typical values |
|---|---|---|
| Screen shake | trauma 0–1, offset = max × trauma² × noise; decays per second. 2D: `Camera2D.offset` (`godot-2d` reference). 3D: `Camera3D.h_offset/v_offset` + a small roll | hit 0.2–0.3, explosion 0.6–1.0, decay 1.5/s |
| Hit-stop | freeze a few frames on impact: `Engine.time_scale = 0.05`, restore with `get_tree().create_timer(t, true, false, true)` (**`ignore_time_scale = true`**) | 40–90 ms light, 120–200 ms heavy |
| Slow motion | tween `Engine.time_scale` down and back. Multiply sound `pitch_scale` too if you want audio to follow | 0.3 for 0.5 s |
| Hit flash | a shader uniform `flash` 0 → 1 → 0 over ~0.1 s (`modulate` only darkens or tints) | white, 80–120 ms |
| Squash and stretch | tween `scale` on the **visual child**, never on the physics body | land: (1.25, 0.8) → (1, 1) with `TRANS_BACK` |
| Knockback | add an impulse to `velocity` and decay it with `move_toward`; optionally disable input for 0.1–0.2 s | 300–600 px/s, 6–10 m/s |
| FOV kick (3D) | tween `fov` +5–10° on dash or sprint, back on stop | 0.15 s out, 0.3 s back |
| Camera lookahead | offset the camera toward velocity or aim direction, smoothed | 10–20 % of the screen |
| Damage numbers | a `Label` that tweens up, fades and scales; color by damage type; crits bigger | 0.6–0.8 s |
| Particles | one-shot `GPUParticles2D/3D` (`one_shot`, `explosiveness = 1`), `restart()` per hit; spawn a pooled copy, don't reuse one for overlapping hits (`godot-shaders-vfx`) | 8–30 particles |
| Sound | `AudioStreamRandomizer` (`random_pitch` 1.05–1.15, several samples) so repeats don't sound robotic; layer a low thump with a crisp click (`godot-audio`) | |
| Rumble | `Input.start_joy_vibration(device, weak, strong, seconds)`; phones: `Input.vibrate_handheld(ms, amplitude)` | 0.1–0.2 s |
| UI juice | tween `Control.offset_transform_scale`/`_rotation` (4.7): a visual-only transform that containers don't override. Center it with `offset_transform_pivot_ratio = Vector2(0.5, 0.5)` | press 0.92, hover 1.05 |

## Tween cheat sheet
- `create_tween().set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)` overshoots (pop-in). `TRANS_ELASTIC` wobbles, `TRANS_QUAD/CUBIC` are smooth, `TRANS_EXPO` is snappy, `TRANS_BOUNCE` is for landing.
- `tween_property(node, "scale", target, t).from(start)`; `.as_relative()` for offsets; `set_parallel()` for simultaneous tracks; `chain()` to go sequential again.
- Kill the previous tween before starting a new one on the same property (`if _t: _t.kill()`), or rapid hits fight each other.
- Feedback during hit-stop: tweens follow `Engine.time_scale` unless you call `set_ignore_time_scale(true)` on them. Use that for UI and the flash itself.
- `set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)` keeps menu tweens running while the tree is paused.
- Frame-rate independent smoothing: `a = a.lerp(b, 1.0 - exp(-speed * delta))`, not `lerp(a, b, 0.1)`.

## Rules
- **Scale feedback with impact.** A pistol and a rocket must not shake the same. Pass the strength in from the event (damage, speed).
- Keep juice in **components** (`Shaker`, `HitFlash`, `Squash`) or a `Juice` autoload driven by signals, so gameplay code only emits `hit(strength)`.
- Feedback goes on visuals, not on physics: shake the camera, not the world; squash the sprite, not the collider.
- Hit-stop pauses the whole game through `time_scale`. For per-entity freezes in action games, pause only the attacker and the victim (`process_mode = PROCESS_MODE_DISABLED` for N ms).
- **Accessibility**: settings for screen-shake intensity (0–100 %), flashing (off/reduced), rumble on/off and slow-motion off. Read them in the components. Never flash the full screen more than 3 times per second.

## Recording trailers and GIFs (Movie Maker)
- `godot --path . --write-movie out.avi --fixed-fps 60 [scene.tscn] --quit-after 1200` renders every frame offline (no dropped frames even if the scene is heavy). Formats by extension: `.avi` (MJPEG + PCM), `.png` (an image sequence + WAV), `.ogv` (Theora/Vorbis; `editor/movie_writer/ogv/*` settings).
- In the editor: toggle Movie Maker mode (the film icon next to Run) and set `editor/movie_writer/movie_file`. Quality: `editor/movie_writer/video_quality`, `fps`, `mix_rate`.
- Not headless: it needs a GPU. Hide debug UI with a `trailer` feature tag or a command-line user arg (`OS.get_cmdline_user_args()`).

3D shaker, hit-stop, flash shader, squash, knockback, damage numbers, juicy button and a settings-aware Juice autoload (compiled by the tests): [references/patterns.md](references/patterns.md)
