---
name: paper-client-side-effects
description: "只用 Paper API 做每位玩家各自看到的錯覺：虛擬世界邊界紅框、個人時間／天氣、hidePlayer 可見性、夜視並在事件後重新套用 / Per-player illusions with Paper API only: virtual world border vignette, personal time/weather, hidePlayer visibility, night vision with reconcile-after-event"
---

# Paper Client-Side Effects

## Skill Name

`paper-client-side-effects`

## Purpose

When you need an effect that "only one player can see" (low-health vignette, personal time/weather, hiding other players in the lobby, passive night vision), **use the Paper API first, then consider packets or NMS**. All of these effects have ready-made methods and do not need `nms-packet-sender`:

| Effect | API | How to clear |
|------|-----|----------|
| Red vignette | `Server#createWorldBorder` + `Player#setWorldBorder` | `setWorldBorder(null)` |
| Personal time | `Player#setPlayerTime(long, boolean)` | `resetPlayerTime()` |
| Personal weather | `Player#setPlayerWeather(WeatherType)` | `resetPlayerWeather()` |
| Hide player | `Player#hidePlayer(Plugin, Player)` | `showPlayer(Plugin, Player)` |
| Night vision | `addPotionEffect` with infinite duration | Reapply with `reconcile()` after events |
| Screen post effect (26.3+) | `Player#postEffects().add(Key)` | `postEffects().remove(Key)`; persists in player data, so remove it on quit and disable (example 4) |

The common root of these bugs is "**the effect is silently removed or replaced by something else after being applied**": the real border changed, the player changed worlds, died and respawned, drank milk, or `/effect clear` was run. The fix is to keep the "desired state" in a central `EffectState` and call `reconcile()` after every triggering event to reapply it, instead of patching each event separately.

## Paper Version Requirements

- Paper 1.21.11 / 26.3 (the methods and events used here have identical signatures in both versions; both are compile-verified)
- `Player#postEffects()` (example 4) exists only on 26.3 and is marked `// @only 26.3`
- Pure Paper API; no Paperweight, ProtocolLib, or PacketEvents needed
- **Spigot**: Core portable — per-player world border, time, weather and `hideEntity` exist in Spigot; replace Adventure, `Tick` and the Paper world border events (`io.papermc.paper.event.world.border`)

## Triggers

- 「虛擬世界邊界」「紅色邊框」「低血量紅框」「virtual world border」「warning distance」
- 「個人時間」「個人天氣」「setPlayerTime」「setPlayerWeather」
- 「隱藏玩家」「hidePlayer」「大廳顯示玩家」「per-viewer visibility」
- 「夜視被牛奶清掉」「EntityPotionEffectEvent」「重新套用效果」「restore effect」
- 「後製效果」「畫面濾鏡」「posteffect」「post effect」「postEffects」

## Inputs

| Parameter | Example | Description |
|------|------|------|
| `base_package` | `com.example.effects` | Output package |
| `low_health_threshold` | `8.0` | Health below which the vignette starts (half a heart is 1) |
| `effects` | `border, time, weather, night-vision, visibility` | Which effects are needed |
| `preference_source` | `SettingsApi` (see `paper-service-api`) | Where player preferences come from |
| `visibility_rule` | Hide non-friends only in the lobby | Decides "who cannot see whom" |

## Outputs

- `EffectPrefs.java` — a single player's preferences (immutable record + enum)
- `EffectPreferences.java` — preference source interface
- `BorderTint.java` — pure calculation of vignette intensity and warning distance
- `LowHealthBorderEffect.java` — apply/clear the virtual border
- `PersonalTimeWeatherEffect.java` — personal time and weather
- `NightVisionEffect.java` — infinite night vision
- `EffectState.java` — central state and `reconcile()`
- `EffectListener.java` — events that trigger `reconcile()`
- `PlayerVisibilityService.java` — plugin-scoped `hidePlayer`
- `SettingsApi.java` / `SettingsHook.java` — preference source hook (see `paper-service-api`)
- `EffectsPlugin.java` — assembly

## Build Setup

See [`references/paper-api-platform.md`](references/paper-api-platform.md). Only `paper-api` is needed:

```groovy
dependencies {
    compileOnly 'io.papermc.paper:paper-api:26.3.build.258-stable'
}
```

## Code Template

The full source lives in [`template.md`](template.md) (about 750 lines, compiled against Paper 1.21.11 and 26.3 in CI). **Read `template.md` before writing any code for this skill**, and copy from it instead of rebuilding the classes from the table below.

| File | Package | Role |
|------|---------|------|
| `EffectPrefs.java` | `.effects` | Immutable per-player preferences |
| `EffectPreferences.java` | `.effects` | Preference source interface |
| `BorderTint.java` | `.effects` | Vignette strength calculation (pure) |
| `LowHealthBorderEffect.java` | `.effects` | Low-health red vignette via a virtual border |
| `PersonalTimeWeatherEffect.java` | `.effects` | Per-player time and weather |
| `NightVisionEffect.java` | `.effects` | Passive night vision |
| `EffectState.java` | `.effects` | Central state and reconcile |
| `EffectListener.java` | `.effects` | Events that trigger reconcile |
| `PlayerVisibilityService.java` | `.effects` | Plugin-scoped player hiding |
| `SettingsApi.java` | `.settings.api` | Settings plugin API (separate plugin, JDK types only) |
| `SettingsHook.java` | `.effects` | Consumer side: preference source backed by the Settings plugin |
| `EffectsPlugin.java` | `.effects` | Assembly |

## Recommended Directory Structure

```
src/main/java/com/example/effects/
├── EffectsPlugin.java
├── EffectPrefs.java
├── EffectPreferences.java
├── BorderTint.java                    <- pure functions, unit-testable
├── EffectState.java                   <- central state + reconcile()
├── EffectListener.java                <- event -> reconcile on the next tick
├── LowHealthBorderEffect.java
├── PersonalTimeWeatherEffect.java
├── NightVisionEffect.java
├── PlayerVisibilityService.java
└── SettingsHook.java                  <- compileOnly dependency on the Settings api package
```

## Thread Safety

- Call all methods **on the main thread only**: `Player#setWorldBorder`, `addPotionEffect`, and `hidePlayer` all touch entities and tracking state
- The `HashMap`s inside `EffectState`, `LowHealthBorderEffect`, and `PlayerVisibilityService` are not thread-safe, for the same reason: do not touch them from async threads
- The preference source (`EffectPreferences`) must read an in-memory cache; call `refresh` only after the database load finishes, load async and apply back on the main thread (see [`references/paper-threading.md`](references/paper-threading.md))
- After scheduling to the next tick with `runTask` inside an event, **look up the `Player` again by UUID**, because the player may have gone offline

## Fallback

| Symptom | Cause | Solution |
|------|------|------|
| Vignette stays forever | `setWorldBorder(null)` not called on disable / world change / preference off | Call `clear` on all three paths; use `clearAll` in `onDisable` |
| Vignette position wrong after the real border shrinks | The virtual border is a stale copy | Listen to `WorldBorderBoundsChangeEvent`/`FinishEvent`/`CenterChangeEvent` and re-copy on the next tick; the periodic scan is the safety net |
| Vignette drawn at old-world coordinates after a world change | The old world's virtual border was not cleared | In `PlayerChangedWorldEvent`, `clear` first and then recalculate |
| Vignette not updated after health is changed by `setHealth` | That path fires no event | Use a periodic scan (4 ticks in this skill) instead of listening to damage events |
| Night vision gone after milk / `/effect clear` / death | Not reapplied | `EntityPotionEffectEvent` -> `reconcile()` on the next tick |
| After enabling the preference, night vision only lasts until the old potion expires | Checked "has night vision" and was fooled by a finite potion | Check `effect.isInfinite()` |
| A newly joined player can see players who should be hidden | Only existing viewers were handled | `joined()` recalculates in both directions |
| A hidden player stays invisible after relogging | `showPlayer` not called before quit | `quit()` shows them first, then drops the record |
| A hidden player disappears from the TAB list | Bukkit behavior of `hidePlayer` | Accept this behavior, or let a TAB plugin control it |
| Adding an effect directly in an event has no effect / recurses infinitely | State not settled at event time; triggers itself | Always `reconcile` after `runTask`, and skip the infinite effect we applied ourselves |
| `NoClassDefFoundError: SettingsApi` | Settings is not installed and the API type appears in a field/signature | Keep API types only inside a method body `try` (see `paper-service-api`) |
| A post effect is still on the screen after relogging or a restart | Post effects are saved in the player data file | Remove the plugin's own key on quit, expiry and `onDisable` (example 4) |
| Need something beyond screen-wide effects (fake blocks, fake entities) | The Paper API cannot do it | Only then switch to `nms-packet-sender` |
