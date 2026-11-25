---
name: paper-combat-tag
description: "PvP 戰鬥標記：純邏輯 CombatTagService（UUID + 時間戳、可 JUnit）、傷害歸因矩陣（近戰/射擊物/藥水/TNT/水晶/重生錨/狼）、指令白名單、傳送封鎖、戰鬥登出判死，並以 ServicesManager 公開 CombatTagApi / PvP combat tagging with a Bukkit-free core service, damage attribution matrix, command whitelist, teleport block, combat-logout punishment and a ServicesManager API"
---

# Paper Combat Tag

## Skill Name

`paper-combat-tag`

## Purpose

After players fight, they enter a "combat state" for a while: escape methods (commands, plugin teleports, logging out) are forbidden, and logging out counts as death. The key is attributing **who hit whom** correctly, because damage often is not dealt by a player directly.

The architecture has two layers:

- **Core (`core` package)**: `CombatTagService`, `CommandPolicy`, `KickRule`, `TeleportRule`, `ActionLedger`. Uses only `UUID`, `long` millisecond timestamps and strings, does not import `org.bukkit`, and can be tested directly with JUnit, no MockBukkit needed.
- **Adapter layer (`adapter` package)**: Listeners translate Bukkit events into core inputs, and translate core verdicts into event cancellations, messages and executions.

Other plugins obtain `CombatTagApi` through `ServicesManager` (see [`paper-service-api`](../paper-service-api/SKILL.md) for how).

## Paper Version Requirements

- Paper 1.21.11 / 26.3 (identical on both; uses `DamageSource`, `PlayerKickEvent.Cause`, `PotionEffectType#getEffectCategory()`; the older `PotionEffectTypeCategory` is deprecated for removal in 26.3)
- Pure Paper API, no Paperweight needed
- **Spigot**: Core portable — replace Adventure messages and `PlayerKickEvent.Cause`

## Triggers

- 「戰鬥標記」「combat tag」「combat log」「戰鬥中登出」「PvP 逃跑」
- 「戰鬥中禁止指令」「戰鬥中禁止傳送」「傷害來源判斷」「damage attribution」
- 「射擊物／藥水／TNT／水晶 傷害算誰的」「CombatTagApi」

## Inputs

| Parameter | Example | Description |
|------|------|------|
| `base_package` | `com.example.combat` | Root package; core is in `.core`, API in `.api` (**the API must not be relocated**) |
| `duration_seconds` | `20` | Tag duration in seconds, reset on every hit taken or dealt |
| `command_whitelist` | `msg`, `r`, `tell` | Commands still usable in combat (use the **canonical command name**; aliases are normalized automatically) |
| `logout_mode` | `KILL` / `DROP_ITEMS` | Punishment for logging out in combat |
| `blocked_teleport_causes` | `COMMAND`, `PLUGIN` | `TeleportCause` values to cancel in combat (pearls, chorus fruit and portals are allowed by default) |
| `bypass_permission` | `combattag.bypass` | Holders are not tagged |

## Outputs

- Core: `CombatTagService`, `ActionLedger`, `CommandPolicy`, `KickRule`, `TeleportRule`
- Config: `CombatConfig` (immutable record), `config.yml`
- Adapter layer: `AttackerResolver`, `CombatTagger`, `DamageListener`, `PotionListener`, `BombListener`, `CommandListener`, `TeleportListener`, `KickListener`, `QuitListener`, `DeathListener`, `CombatTicker`
- Public API: `CombatTagApi` (`api` package), `CombatTagApiImpl`
- `CombatTagPlugin` (assembly and registration), `plugin.yml`

## Build Setup

See [`references/paper-api-platform.md`](references/paper-api-platform.md). Tests use JUnit (the core contains no Bukkit, so MockBukkit is not needed):

```groovy
dependencies {
    compileOnly 'io.papermc.paper:paper-api:26.3.build.258-stable' // 1.21.11: '1.21.11-R0.1-SNAPSHOT'
    testImplementation 'org.junit.jupiter:junit-jupiter:5.11.4'
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}

test {
    useJUnitPlatform()
}
```

## Damage Attribution Matrix

| Damage source | How to determine | Notes |
|----------|----------|------|
| Melee | `DamageSource#getCausingEntity()` is a `Player` | Most common |
| Arrows, tridents, snowballs, fishing rods | `Projectile#getShooter()` is a `Player` | `getCausingEntity` is usually already the shooter; use `getDirectEntity` as a fallback |
| Splash / lingering potions | `PotionSplashEvent`: `ThrownPotion#getShooter()` + harmful effect + `getIntensity > 0` | Effects without a damage number, such as poison and wither, do not trigger `EntityDamageEvent` |
| Potion clouds | `AreaEffectCloudApplyEvent`: `AreaEffectCloud#getSource()` | The cloud left after a lingering potion lands |
| TNT | `TNTPrimed#getSource()` (the igniter) | Chain detonations also keep the igniter |
| End crystals | Record when the crystal is hit; look it up within a short window when it explodes | The crystal itself has no "who hit it" field |
| Respawn anchors / beds | Record on right-click (`ActionLedger`); on `BLOCK_EXPLOSION` look up with `getDamageLocation()` | The explosion and the click are in the same tick; window of 1-2 ticks |
| Tamed wolves, etc. | `Tameable#getOwnerUniqueId()` (counts only if the owner is online) | |
| Fire, fall, void (after being hit) | **Do not reset the tag** and do not create a new one | Prevents burning from extending combat indefinitely; use `lastAttacker` for death attribution |
| Self-damage, cancelled events | Ignore | `EventPriority.MONITOR` + `ignoreCancelled = true` |

## Code Template

The full source lives in [`template.md`](template.md) (about 1,150 lines, compiled against Paper 1.21.11 and 26.3 in CI). **Read `template.md` before writing any code for this skill**, and copy from it instead of rebuilding the classes from the table below.

| File | Package | Role |
|------|---------|------|
| `CombatTagService.java` | `.core` | Tag state and timers; no Bukkit |
| `ActionLedger.java` | `.core` | Short-window attribution for crystals / respawn anchors / beds |
| `CommandPolicy.java` | `.core` | Command whitelist while tagged |
| `KickRule.java` | `.core` | Kick reasons exempt from the logout penalty |
| `TeleportRule.java` | `.core` | Teleport causes blocked while tagged |
| `CombatConfig.java` | `.adapter` | Immutable config |
| `CombatMessages.java` | `.adapter` | MiniMessage messages |
| `AttackerResolver.java` | `.adapter` | Damage → responsible player (projectiles, tamed pets, TNT, crystals) |
| `CombatTagger.java` | `.adapter` | Applies the tag to attacker and victim |
| `DamageListener.java` | `.adapter` | Tags on player damage |
| `PotionListener.java` | `.adapter` | Tags on harmful potions and lingering clouds |
| `BombListener.java` | `.adapter` | Records who primed a respawn anchor / bed |
| `CommandListener.java` | `.adapter` | Blocks non-whitelisted commands |
| `TeleportListener.java` | `.adapter` | Blocks teleports while tagged |
| `KickListener.java` | `.adapter` | Exempts whitelisted kick causes from the logout penalty (fires before quit) |
| `QuitListener.java` | `.adapter` | Combat-logout punishment (kill or drop items) |
| `DeathListener.java` | `.adapter` | Untags on death |
| `CombatTicker.java` | `.adapter` | One timer per second: countdown and expiry |
| `CombatTagApi.java` | `.api` | Public API (`api` package) |
| `CombatTagApiImpl.java` | `.adapter` | API implementation |
| `CombatTagPlugin.java` | `.adapter` | Assembly and listener registration |
| `config.yml`, `plugin.yml` | resources | Config and plugin descriptor |

## Recommended Directory Structure

```
src/main/java/com/example/combat/
├── core/                     <- no Bukkit, tested directly with JUnit
│   ├── CombatTagService.java
│   ├── ActionLedger.java
│   ├── CommandPolicy.java
│   ├── KickRule.java
│   └── TeleportRule.java
├── api/                      <- do not relocate, add-only
│   └── CombatTagApi.java
└── adapter/
    ├── CombatTagPlugin.java
    ├── CombatConfig.java / CombatMessages.java
    ├── AttackerResolver.java / CombatTagger.java / CombatTicker.java
    ├── CombatTagApiImpl.java
    └── *Listener.java
src/test/java/com/example/combat/core/
src/main/resources/{config.yml,plugin.yml}
```

## Thread Safety

- The core and all Listeners run only on the **main thread**; `CombatTagService` has no locks, so do not touch it from async tasks
- When an async phase needs data, take a snapshot on the main thread first (for example `remainingSeconds`) and pass the value in
- `CombatTicker` uses `runTaskTimer` (main thread); there is only one timer on the whole server, not one per player
- `onDisable` cancels tasks and calls `clear()`; if the API implementation must support other threads, it has to read an immutable snapshot instead
- See [`references/paper-threading.md`](references/paper-threading.md)

## Fallback

| Error | Cause | Fix |
|------|------|------|
| Hit by an explosion / potion but not tagged | The damage has no causing entity | Check the attribution matrix; crystals, anchors and beds rely on `ActionLedger`, potions on `PotionSplashEvent` |
| Kicked but not punished / let off instead | Judged with `PlayerQuitEvent#getReason()` | Use the `PlayerKickEvent.Cause` whitelist instead, so a second-client login does not become an escape method |
| Alias / namespaced commands bypass the whitelist | Only the string the player typed is compared | Resolve to the canonical name with `CommandMap#getCommand` before comparing |
| Pearls are blocked during combat too | All `TeleportCause` values are blocked | Block only `COMMAND` and `PLUGIN` (adjustable in config) |
| Burning keeps the tag from ever ending | Environmental damage also resets the tag | Never reset on damage without a player attribution |
| Stack trace every second | Exception inside the timer | Boundary catch around `run()`, log only the first |
| A death was cancelled but the tag was cleared | Listener did not set `ignoreCancelled` | `MONITOR` + `ignoreCancelled = true` |
| Other plugins cannot get `CombatTagApi` | The API package was relocated, or `load` was too early | See [`paper-service-api`](../paper-service-api/SKILL.md): `softdepend`, no caching, no relocation |
