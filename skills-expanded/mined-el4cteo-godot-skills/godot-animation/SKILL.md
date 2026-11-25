---
name: godot-animation
description: Animation in Godot 4.7 - AnimationPlayer and libraries, AnimationTree (state machines, blend spaces with sync_mode, one-shots, conditions), root motion, method/audio tracks, Tween recipes incl. tween_await (4.7), skeletons, the 4.6 IK framework (TwoBoneIK3D, FABRIK3D, CCDIK3D, SplineIK3D), LookAt/bone constraints, procedural animation. Use for character animation, cutscenes, UI motion or IK.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#).
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Animation (4.7)

Asset-side work (rigging, clips, root motion export) belongs in Blender. See the `blender-animation` and `blender-export-pipelines` skills if they're installed.

## AnimationPlayer
- Animations live in `AnimationLibrary` resources. The default library is `""`, so `play(&"run")` works, and other libraries are addressed as `&"lib/run"`. Imported GLB clips arrive as a library. Make a clip loop in the import settings (or with a `-loop` suffix) instead of editing the imported animation.
- `play(name, custom_blend, speed)`, `play_backwards`, `queue`, `seek(t, true)`, `speed_scale`. The `animation_finished(name)` signal lives on `AnimationMixer`. `play_with_capture` blends from the current pose.
- Tracks can set any property, call methods (`TYPE_METHOD`), play audio, run Bezier curves or start other animations. Use method tracks for footsteps and hit frames instead of timers.
- 4.6 C# break: `current_animation`, `assigned_animation` and `autoplay` are `StringName`.

## AnimationTree (use it for any character with more than ~3 states)
- Set `anim_player` and a `tree_root` (`AnimationNodeStateMachine` or `AnimationNodeBlendTree`). The AnimationPlayer becomes a clip container only, so don't call `play()` on it anymore.
- Drive it through parameters (`anim_tree.set("parameters/…", v)`, or `anim_tree["parameters/…"] = v` in GDScript):
  - State machine: `var pb: AnimationNodeStateMachinePlayback = tree["parameters/playback"]`, then `pb.travel(&"Jump")` (pathfinds through transitions), `pb.start(&"Idle")`, `pb.get_current_node()`.
  - Conditions on transitions: `parameters/conditions/is_grounded = true`. Advance expressions: set `advance_expression_base_node` and write expressions like `velocity.length() > 0.1`.
  - Blend space: `parameters/Locomotion/blend_position = Vector2(x, y)` (or a float for 1D).
  - One-shot: `parameters/Attack/request = AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE`. Transition node: `parameters/State/transition_request = "crouch"`.
- **4.7:** blend spaces use `sync_mode` (`SYNC_MODE_NONE`, `INDEPENDENT`, `CYCLIC_MUTABLE`, `CYCLIC_CONSTANT`) instead of the old `sync` bool. Cyclic modes keep walk and run feet in phase.
- `callback_mode_process`: physics for gameplay-synced characters, idle for visuals. Use `MANUAL` + `advance(delta)` for deterministic or networked playback.

## Root motion
Set `root_motion_track` (for example `^"Armature/Skeleton3D:Root"`). Each physics frame, read `get_root_motion_position()` and `get_root_motion_rotation()`, then apply them to the CharacterBody (rotate them into world space) and call `move_and_slide()`. See the reference.

## Tween (code animation)
- `create_tween()` on a node binds the tween to that node, which pauses and frees with it. Chain with `.set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)`. `tween_property(obj, "path:sub", final, dur).from(start).as_relative()`, `tween_callback(f)`, `tween_interval(t)`, `tween_method(f, a, b, dur)`, `parallel()`/`set_parallel()`, `set_loops(n)` and `chain()`.
- **`tween_await(signal)` (4.7)** holds the sequence until a signal fires. Add `.set_timeout(s)` when the signal might never come.
- Kill old tweens before starting new ones on the same property (`if t: t.kill()`), or they fight. Use `set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)` for pause-menu animations and `set_process_mode(Tween.TWEEN_PROCESS_PHYSICS)` for physics objects.

## Skeletons, IK and constraints
- Everything that procedurally changes bones is a **`SkeletonModifier3D`** child of `Skeleton3D`. They run in tree order after animation, and each has `influence` and `active`.
- **IK framework (4.6+):** `TwoBoneIK3D` (arms and legs, needs a pole target), `FABRIK3D`, `CCDIK3D` and `JacobianIK3D` (chains), `SplineIK3D` (tails, spines along a Path3D). Settings are indexed lists (`set_setting_count(n)`, `set_root_bone_name(i, …)`, `set_target_node(i, path)`), so one node can solve several limbs. `SkeletonIK3D` is deprecated.
- Limits and helpers: `JointLimitationCone3D`, `BoneTwistDisperser3D`, `LimitAngularVelocityModifier3D` (4.6+).
- Constraints (4.5+): `LookAtModifier3D` (head tracking; 4.7 default `relative = false`), `AimModifier3D`, `CopyTransformModifier3D`, `ConvertTransformModifier3D`. Secondary motion: `SpringBoneSimulator3D` (hair, tails, cloth strips).
- `BoneAttachment3D` attaches weapons and props to a bone.
- 2D: `Skeleton2D` + `Bone2D` with `SkeletonModification2D*` stacks.

## Procedural animation tips
- Use frame-rate-independent smoothing, `x = lerp(x, target, 1.0 - exp(-speed * delta))`, instead of `lerp(x, target, 0.1)`.
- For squash and stretch, put the scale on a visual child node, never on the physics body.

Character AnimationTree driver, root motion, foot IK setup, tween recipes (compiled by the tests): [references/patterns.md](references/patterns.md)
