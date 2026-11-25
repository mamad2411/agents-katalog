---
name: juice
description: "Apply a game feel pass to the current Unity scene. Adds screen shake, hit-stop, particles, easing, anticipation, sound layers — each change citing its source in the taste library (Vlambeer principle number, Game Feel chapter, etc.). Trigger after /prototype is playable, or whenever the user says the game feels flat, dead, or mushy."
disable-model-invocation: false
---

# juice

> **Apply taste. Cite the source. Every time.**

## When to invoke

- After `/prototype` is playable and the user wants polish
- User says: "this feels dead" / "needs more juice" / "make it satisfying"
- After major mechanic changes (re-juice the affected systems)

## Hard rules

1. **Every change cites its source.** Format: `✓ Did X (Vlambeer P3, Game Feel ch.7).`
2. **Match the mood from the Vibe Brief.**
   - "Tense, methodical" mood → restrained shake (0.05-0.15), longer hit-stop (100ms+), low-pitch SFX, slow-motion finishers.
   - "Frenetic, ridiculous" mood → max chaos, big shake (0.4+), short hit-stop (30-50ms), pitched-up SFX, particles everywhere.
3. **Read what already exists** before adding. Don't double-shake.
4. **Tunables exposed** to Inspector via `[SerializeField]`. The user must be able to tweak without recompiling.
5. **Pool everything.** Particle bursts and decals use object pools, not Instantiate/Destroy churn.
6. **Press-time feedback is mandatory for any charged input.** When a mechanic uses press-and-hold
   (charge attack, hold-to-aim, hold-to-build), the player MUST get visual feedback ON PRESS, not
   only on release. A growing ring, scaling overlay, particle orbit, color pulse — pick one.
   The crit/sweet-spot window must be visually distinct (color shift, ring flash).
   *Learned from dogfood: a 180+ms gap between LMB press and any visual feedback violated Game Feel
   M2 (response). FEEL-CHECK predicted this before testing; real tester confirmed it.*
   Source: [[game-feel-swink#m2--response]], [[vlambeer-juice#p25--one-frame-ui-tween-in]].

## Unity-specific implementation (concrete)

Always prefer these implementations over hand-rolled equivalents:

### Camera shake → Cinemachine Impulse [UP5]
Setup walkthrough: `templates/cinemachine-impulse-setup.md`. Magnitudes follow [[vlambeer-juice#p3]] table.

```csharp
[SerializeField] CinemachineImpulseSource impulse;
impulse.GenerateImpulseWithForce(0.4f * MOOD_MULT);  // melee landed
```

### Hit-stop → static helper [UP6]
```csharp
public static class HitStop {
    static float _until;
    public static void Freeze(float s) {
        _until = Mathf.Max(_until, Time.realtimeSinceStartup + s);
        Time.timeScale = 0f;
    }
    public static void Tick() {
        if (Time.timeScale == 0f && Time.realtimeSinceStartup >= _until)
            Time.timeScale = 1f;
    }
}
```
**Mandatory:** any coroutine/animation/audio that runs during hit-stop uses `Time.unscaledDeltaTime`, `WaitForSecondsRealtime`, or `AudioSource.ignoreListenerPause = true`.

### Hit flash → MaterialPropertyBlock OR HitFlash shader [UP7, UP13]
**Default:** MaterialPropertyBlock with `_BaseColor` + `_Color` set. **If** you need full-surface override (silhouette flash), use `templates/shaders/HitFlash.shader` and drive `_FlashAmount` from 0→1→0 over 70ms.

### Tweening → DOTween or coroutine + AnimationCurve [UP4]
```csharp
// DOTween (recommended):
transform.DOScale(1.2f, 0.18f).SetEase(Ease.OutBack);
canvasGroup.DOFade(0f, 0.35f).SetEase(Ease.InQuad);

// No-DOTween fallback:
yield return TweenScale(0.18f, AnimationCurve.EaseInOut(0,0,1,1));
```

### Audio mixer with ducking [UP10]
2 mixer groups (Music, SFX) → Music group → Duck Volume effect → sidechain SFX. Threshold -20dB, Ratio 4:1, Attack 50ms, Release 800ms. Combat music dips automatically during impact-heavy moments.

### Mood profile multipliers
Apply to all magnitudes when generating code:
```csharp
const float MOOD_MULT_TENSE_METHODICAL = 0.6f;
const float MOOD_MULT_FRENETIC = 1.5f;
const float MOOD_MULT_MELANCHOLIC = 0.4f;
const float MOOD_MULT_PLAYFUL = 1.0f;
```
Read brief mood, pick multiplier, apply to every Impulse force, hit-stop duration, particle count.

## The juice checklist

Walk through each in order. For each, decide APPLY or SKIP (with reason).

### Layer 1 — Camera

- [ ] **Camera shake on impacts** ([Vlambeer P3](../../taste/vlambeer-juice.md#p3--screen-shake))
  Cinemachine Impulse Source preferred. Hierarchy: bullet < hit < death < player damage.
- [ ] **Camera lerp/damping** ([Vlambeer P9](../../taste/vlambeer-juice.md#p9--camera-lerp))
  Cinemachine framing transposer, X/Y damping 0.3-0.5.
- [ ] **Look-ahead** in movement direction (0.2-0.4)
- [ ] **Camera kick** on key actions ([Vlambeer P10](../../taste/vlambeer-juice.md#p10--camera-kick))
- [ ] **FOV pulse** on dash/sprint (slight widen)

### Layer 2 — Time

- [ ] **Hit-stop on impacts** ([Vlambeer P4](../../taste/vlambeer-juice.md#p4--hit-stop-frame-freeze-on-impact))
  Implement as `HitStop.Freeze(seconds)` coroutine using `Time.timeScale`.
  Don't forget `Time.unscaledDeltaTime` for UI/feedback systems.
- [ ] **Slow-mo on critical moments** ([Vlambeer P17](../../taste/vlambeer-juice.md#p17--slow-mo-on-critical-events))
  Use sparingly. Boss finishers, player near-death.
- [ ] **Sleep frame** on big hits ([Vlambeer P12](../../taste/vlambeer-juice.md#p12--sleep))

### Layer 3 — Particles

- [ ] **Muzzle flash / source effect** for every action
- [ ] **Impact particles** at hit point ([Vlambeer P5](../../taste/vlambeer-juice.md#p5--particles-particles-particles))
- [ ] **Death burst** — 3x intensity of normal hit ([Vlambeer P23](../../taste/vlambeer-juice.md#p23--death-is-a-celebration))
- [ ] **Persistent decals/gibs** ([Vlambeer P6](../../taste/vlambeer-juice.md#p6--permanence-decals-gibs-holes))
- [ ] **Color matching** — particles use the color of the affected entity

### Layer 4 — Animation & motion

- [ ] **Squash & stretch** on jump/land ([Vlambeer P14](../../taste/vlambeer-juice.md#p14--movement-spring-anticipation--follow-through))
- [ ] **Anticipation telegraphs** on enemies ([Vlambeer P15](../../taste/vlambeer-juice.md#p15--anticipation-telegraph))
- [ ] **Easing** on all tweens — never linear ([Vlambeer P20](../../taste/vlambeer-juice.md#p20--tweening-everything-eases))
- [ ] **Knockback** on hit ([Vlambeer P13](../../taste/vlambeer-juice.md#p13--knockback))

### Layer 5 — Visual feedback

- [ ] **White-flash on damaged entities** ([Vlambeer P19](../../taste/vlambeer-juice.md#p19--color-and-contrast-pulse))
- [ ] **Damage numbers** with crit variation ([Vlambeer P21](../../taste/vlambeer-juice.md#p21--damage-numbers))
- [ ] **Combo escalation** if combat ([Vlambeer P22](../../taste/vlambeer-juice.md#p22--combo--streak-feedback))

### Layer 6 — Audio

- [ ] **Every action has a sound** ([Vlambeer P7](../../taste/vlambeer-juice.md#p7--sounds-everything-has-a-sound))
- [ ] **Pitch variation** ±10% on every play
- [ ] **Layered SFX** — primary + secondary + low end
- [ ] **Adaptive music** if scope allows ([Vlambeer P8](../../taste/vlambeer-juice.md#p8--music))

### Layer 7 — Input feel

- [ ] **Input buffering** ~100-150ms ([Vlambeer P24](../../taste/vlambeer-juice.md#p24--input-buffering))
- [ ] **Coyote time** ~80-120ms on platformers

## Procedure

1. **Read the brief mood** → pick the juice profile (restrained vs. max chaos).
2. **Inventory existing juice** — Grep for `Impulse`, `timeScale`, `Particle`, `Animator`. Note what's there.
3. **Pick the top 5 missing items** that match the mood. Don't apply all 20+ at once.
4. **Apply, cite, commit.** For each:
   - Generate the code/prefab change
   - Write a single line: `✓ Added X (Source PN, value reasoning).`
   - Move to next.
5. **Summary at the end**:
   ```
   Juice pass complete — 5 changes applied:
   ✓ Cinemachine Impulse on enemy hit (Vlambeer P3, 0.15 amplitude — your mood is "tense" so restrained)
   ✓ 80ms hit-stop on melee impact (Vlambeer P4 + Game Feel ch.7)
   ✓ White flash 70ms on damaged enemy (Vlambeer P19)
   ✓ Squash on player landing 0.85 → 1.0 over 180ms (Vlambeer P14)
   ✓ Pitch variation ±10% on all weapon SFX (Vlambeer P7)

   Skipped (already present): camera damping, easing on UI.
   Next suggestion: /feel-check to score the change.
   ```

## Anti-patterns

- ❌ Apply juice without citing the source (defeats the moat)
- ❌ Max chaos juice on a "tense" mood game (mismatch)
- ❌ Doubling existing effects (read first)
- ❌ Forgetting `Time.unscaledDeltaTime` for UI when applying hit-stop
- ❌ Instantiating particle bursts without pooling

## Cross-references

- Reads: [[vlambeer-juice]] (primary), [[game-feel-swink]] (theory), [[vibe-brief]] (mood)
- Drives: [[feel-check]] (verify the pass landed)
