---
name: prototype
description: "Build a playable Unity scene that supports the Vibe Brief's verb and core loop, in under 30 minutes. Project-aware — reads Input System version, render pipeline, existing controllers, Cinemachine setup, and generates code that fits the actual project, not a generic template. Trigger after /vibe-start, or whenever the user wants a fresh playable from current brief."
disable-model-invocation: false
---

# prototype

> **30 minutes to playable.**
> Project-aware code that fits your Unity setup. Never generic.

## When to invoke

- Right after `/vibe-start` (the brief is fresh)
- User says: "build me a scene" / "let me play it" / "prototype this" / "let's get something running"
- The user wants to test an idea quickly

## Pre-conditions

1. Vibe Brief exists at `Assets/_Project/vibe-brief.md`.
   - If not, **run `/vibe-start` first**. Don't skip.
2. A Unity project exists (or we'll create one — see Step 1).

## Hard rules

1. **The first playable build must work within 30 minutes**, including code, scene, and inputs.
2. **Read the project before writing code.** Never spit out generic Unity code.
3. **Placeholder art is mandatory** — no waiting on assets. Capsules, cubes, primitives.
   ([Tyroller M4](../../taste/tyroller-mistakes.md#m4--premature-visual-style))
4. **Verb-first.** The player must be doing the brief's VERB within 10 seconds of pressing play.
   ([Tyroller M13](../../taste/tyroller-mistakes.md#m13--ignoring-the-first-30-seconds))
5. **One scene, one verb.** No menus, no tutorial. Just the verb in a sandbox.
6. **Visual asymmetry on the player.** If the player can rotate (most games), the placeholder
   must have a readable facing direction — a small forward indicator (nose cube, arrow, decal),
   different head color, etc. **A bare capsule or sphere has no readable facing** — even if
   `transform.rotation` is updating, the user can't see it. *Learned from dogfood: real tester
   said "couldn't move with mouse" when in fact the rotation was working — they just couldn't see
   it on a symmetric capsule.*
   Source: [[game-feel-swink#m5--metaphor]] — the action must read as the thing it represents.

## Unity pattern selection (decision tree)

Before generating code, check [[unity-patterns]] and apply when appropriate:

| Detected need | Apply pattern | When |
|---|---|---|
| Tunable stats per archetype (weapons, enemies) | **UP1** ScriptableObject Configs | Always when there are >1 weapon/enemy types |
| Systems that shouldn't reference each other | **UP2** Event Channels | Score updates UI, kills feed a popup, etc. |
| Spawned objects (bullets, particles, popups) | **UP3** Object Pooling | Any object spawned >5 times per minute |
| Movement / fade / scale animation | **UP4** Tweening | Use DOTween if available, else coroutine + curve |
| Camera shake | **UP5** Cinemachine Impulse | Always for impacts |
| Frame freeze on hit | **UP6** Time.timeScale + unscaledDeltaTime | Always for melee/heavy hits |
| Per-instance color override | **UP7** MaterialPropertyBlock | Hit flash, damage tint, status effects |
| Code-only input | **UP9** InputAction in code | Prototype scope — skip PlayerInput component |
| Save state | **UP11** JsonUtility | Non-jam scope only |

For each generation, **cite the UP# in code comments**:
```csharp
// [UP3] pooled bullets to avoid Instantiate/Destroy hitches
private ObjectPool<Bullet> _pool;
```

## Templates you can use

Drop-in templates live in `templates/`:
- `templates/scriptable-objects/WeaponConfig.cs` — example tunable config
- `templates/scriptable-objects/EnemyConfig.cs` — enemy stats + telegraph
- `templates/scriptable-objects/IntEventChannel.cs` — decoupled event bus
- `templates/cinemachine-impulse-setup.md` — Cinemachine 3.0 setup walkthrough
- `templates/shaders/HitFlash.shader` — URP unlit + _FlashAmount

## Procedure

### Step 1 — Read the project

Use Read/Glob to gather:

| File / pattern | What to extract |
|---|---|
| `ProjectSettings/ProjectVersion.txt` | Unity version (e.g., 6000.0.23f1) |
| `Packages/manifest.json` | Input System (com.unity.inputsystem), Cinemachine (com.unity.cinemachine), URP (com.unity.render-pipelines.universal), Recorder |
| `Assets/Settings/*` | URP asset, render pipeline asset references |
| `Assets/**/*.cs` (existing) | Existing player controllers, managers, namespaces in use |
| `ProjectSettings/InputManager.asset` or `Assets/**/*.inputactions` | Input setup (old vs new system) |
| `Assets/**/*.unity` | Existing scenes — note conventions |

**Output a one-line project profile:**
> Unity 6000.0.23f1 · URP · new Input System (InputActions found at `Assets/Settings/Game.inputactions`) · Cinemachine 3.0 · Namespace convention `Studio.{ProjectName}`

If something is missing (e.g., no Input System), tell the user what'll be installed:
> ⚠ No Input System detected. I'll add `com.unity.inputsystem` to `Packages/manifest.json` and an InputActions asset.

### Step 2 — Read the brief

Read `Assets/_Project/vibe-brief.md`. Extract:
- Verb (drives what we build)
- Mood (drives polish style)
- Core loop (drives the scene layout)
- Anti-features (drives what we DON'T build)

### Step 3 — Pick a prototype template

Based on the verb, choose a base archetype:

| Verb cluster | Template |
|---|---|
| run, jump, climb, swing | **Platformer** — Rigidbody2D/3D, ground check, jump buffer, coyote time |
| shoot, slash, parry | **Action** — top-down or side, weapon prefab, telegraphed dummy enemy |
| drive, drift, race | **Vehicle** — wheel collider stack or arcade controller |
| build, place, manage | **Builder** — grid + cursor + placement preview |
| explore, deduce, talk | **Investigation** — character controller + interactable prompts |
| weave, dodge, survive | **Survivor-like** — auto-attack + enemy waves |

If verb doesn't match, **ask the user once** which is closest. Don't guess wildly.

### Step 4 — Generate the scene

Create these in `Assets/_Project/Prototype/`:

```
Assets/_Project/Prototype/
├── Scenes/
│   └── Prototype.unity
├── Scripts/
│   ├── PlayerController.cs        (matches detected Input System)
│   ├── PrototypeBootstrap.cs      (auto-loads scene, sets timescale)
│   └── (verb-specific scripts)
├── Prefabs/
│   ├── Player.prefab              (capsule + script + collider)
│   └── (one verb-relevant prefab — dummy enemy / target / building)
└── Input/
    └── PrototypeInput.inputactions (if new Input System)
```

**Code rules:**

- Match the project's existing namespace convention. If none, use `Prototype`.
- If new Input System: subscribe in `OnEnable`, unsubscribe in `OnDisable`. Use `InputAction.CallbackContext`.
- If old Input Manager: use `Input.GetAxisRaw`, document the choice.
- Use `[SerializeField] private` for tunables (speed, jump force). Expose to Inspector.
- Cinemachine if present: create a `CinemachineCamera` following the player, set damping per [Vlambeer P9](../../taste/vlambeer-juice.md#p9--camera-lerp).
- Default tunables tuned for "feels okay" — not perfect. `/juice` polishes later.
- One-line XML doc on each public field/method. No essays.

### Step 5 — Verify the 30-second start

Before claiming done:

- [ ] Player exists in the scene at origin (or sensible start)
- [ ] Pressing Play → player can perform the VERB within 10 seconds
- [ ] At least one object to interact with (target, enemy, platform, etc.)
- [ ] Camera follows player with damping (no snap)
- [ ] Scene fits the brief's mood at a glance (lighting roughed in)

If you can't verify because Unity isn't running, **say so explicitly**:
> ⚠ I generated code and scene assets but cannot run Unity from here.
> Open `Assets/_Project/Prototype/Scenes/Prototype.unity` and press Play.
> Expected: capsule moves on WASD/gamepad, jumps on Space, camera follows.
> If anything feels off, run `/feel-check` and I'll diagnose.

### Step 6 — Hand-off

End with options:

> ✓ Prototype scene built. Code targets Unity 6000.0.23f1 + new Input System + URP.
>
> What's next?
> - **Press Play** in Unity and try it. If it works, run `/juice` for game feel pass.
> - **If something's broken**, paste the console error and I'll fix.
> - **If it doesn't feel right**, run `/feel-check`.

## Anti-patterns (do NOT do)

- ❌ Generate generic Unity code without reading the project ([this is THE differentiator](../../README.md#2-project-aware-code))
- ❌ Build menus, tutorials, settings — none of that. Just the verb.
- ❌ Spend >30 min before showing anything playable
- ❌ Use placeholder code with `TODO` markers in critical paths
- ❌ Add features not in the brief (scope creep, [Tyroller M1](../../taste/tyroller-mistakes.md#m1--scope-explosion))
- ❌ Wait on art assets — use primitives
- ❌ Forget to handle the case where the project is new/empty

## Cross-references

- Reads: [[vibe-brief]] (the project's), [[vlambeer-juice]] (default tunables)
- Drives: [[juice]] (polish pass), [[feel-check]] (verify feel), [[grab-asset]] (replace placeholders)
- Anti-pattern sources: [[tyroller-mistakes#M1]], [[tyroller-mistakes#M4]], [[tyroller-mistakes#M13]]
