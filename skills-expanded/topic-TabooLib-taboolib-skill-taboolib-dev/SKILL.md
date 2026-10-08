---
name: taboolib-dev
description: >
  Help developers build Minecraft plugins using TabooLib 6.x framework (Kotlin/Java).
  Use when user mentions "taboolib", "TabooLib plugin", "minecraft plugin with taboolib",
  "bukkit plugin framework", "create taboolib project", "taboolib command", "taboolib config",
  "taboolib UI", "taboolib database", "taboolib NMS", "taboolib kether",
  or asks about TabooLib module setup, @Awake lifecycle, cross-version compatibility.
  Covers project setup, module selection, API usage, and troubleshooting.
license: MIT
compatibility: Claude Code, Claude.ai
metadata:
  author: community
  version: 1.0.0
  category: minecraft-development
  tags: [minecraft, kotlin, taboolib, bukkit, plugin-development]
  source-repo: https://github.com/TabooLib/taboolib
  source-commit: 4eaffc793a25962453849ae77597198d1643d765
  source-date: "2026-02-23"
  taboolib-version: 6.1.2-beta12
  gradle-plugin-version: "2.0.31"
---

# TabooLib Plugin Development

## Overview

TabooLib is a Kotlin-based cross-platform Minecraft plugin framework (supports Bukkit/Spigot/Paper, BungeeCord, Velocity). Current stable version: **6.1.2-beta12**, Gradle plugin: **2.0.31**.

Key traits:
- ~30KB runtime footprint (modules downloaded on demand)
- Kotlin DSL APIs for commands, UI, config, database
- Cross-version NMS abstraction (1.8 ~ 1.21+)
- Annotation-driven lifecycle (`@Awake`, `@SubscribeEvent`, `@Schedule`, `@Config`)

## Instructions

### Step 1: Project Setup

When user wants to create a new TabooLib plugin:

1. Generate `build.gradle.kts` with the TabooLib Gradle plugin:

```kotlin
import io.izzel.taboolib.gradle.*

plugins {
    java
    id("io.izzel.taboolib") version "2.0.31"
    kotlin("jvm") version "2.0.0"
}

taboolib {
    env {
        install(UNIVERSAL, BUKKIT)
        // Add modules as needed: CONFIGURATION, LANG, CHAT, NMS, NMS_UTIL, UI, DATABASE, KETHER
    }
    version { taboolib = "6.1.2-beta12" }
}

repositories {
    mavenCentral()
}

dependencies {
    compileOnly("ink.ptms.core:v12004:12004:mapped")
    compileOnly("ink.ptms.core:v12004:12004:universal")
    compileOnly(kotlin("stdlib"))
    taboo("ink.ptms:um:1.2.0") // Universal Minecraft API
}

tasks.withType<JavaCompile> {
    options.encoding = "UTF-8"
}
```

2. Create the plugin main class (use `object`, NOT `class`):

```kotlin
import taboolib.common.platform.Plugin

object MyPlugin : Plugin() {
    override fun onLoad() { }
    override fun onEnable() { info("Plugin enabled!") }
    override fun onActive() { } // Called after server fully started
    override fun onDisable() { }
}
```

3. No `plugin.yml` needed — TabooLib auto-generates it.

### Step 2: Module Selection Guide

Help user pick the right modules based on their needs:

| Need | Module Constant | Notes |
|------|----------------|-------|
| Config files (YAML/TOML/HOCON) | `CONFIGURATION` | Enables `@Config`, `@ConfigNode` |
| Multi-language / i18n | `LANG` | Requires CONFIGURATION |
| Rich text / clickable messages | `CHAT` | Components API |
| NMS / packet operations | `NMS`, `NMS_UTIL` | Cross-version abstraction |
| Chest GUI / Anvil GUI | `UI` | Requires CHAT + NMS |
| Database (MySQL/SQLite) | `DATABASE` | HikariCP connection pool |
| Kether scripting | `KETHER` | Requires CONFIGURATION |
| Bukkit utilities (ItemBuilder etc) | `BUKKIT_ALL` | XMaterial, ItemBuilder |
| PlaceholderAPI / Vault hooks | `BUKKIT_HOOK` | Third-party integration |
| BungeeCord messaging | `PORTICUS` | Cross-server communication |

Module dependencies (auto-resolved by Gradle plugin, but useful to know):
- `UI` depends on `CHAT` + `NMS`
- `LANG` depends on `CONFIGURATION`
- `NMS_UTIL` depends on `NMS`

### Step 3: Core API Patterns

Always follow these patterns when writing TabooLib code:

**Pattern: Singleton Object + @Awake**

```kotlin
@Awake
object PlayerManager {
    private val cache = ConcurrentHashMap<UUID, PlayerData>()

    @Awake(LifeCycle.ENABLE)
    fun init() { /* startup logic */ }

    @SubscribeEvent
    fun onQuit(event: PlayerQuitEvent) {
        cache.remove(event.player.uniqueId)
    }

    @Schedule(async = true, period = 6000L)
    fun autoSave() {
        cache.values.forEach { it.save() }
    }
}
```

**Pattern: Config Injection**

```kotlin
@Awake
object Settings {
    @Config("config.yml", autoReload = true)
    lateinit var config: Configuration

    @ConfigNode("debug")
    var debug = false

    @ConfigNode("settings.max-players")
    var maxPlayers = 100
}
```

**Pattern: Command DSL**

```kotlin
command("myplugin", aliases = listOf("mp"), permission = "myplugin.use") {
    literal("reload") {
        execute<ProxyCommandSender> { sender, _, _ ->
            Settings.config.reload()
            sender.sendMessage("Reloaded!")
        }
    }
    dynamic("player") {
        suggestion<ProxyCommandSender> { _, _ ->
            Bukkit.getOnlinePlayers().map { it.name }
        }
        execute<ProxyCommandSender> { sender, _, argument ->
            sender.sendMessage("Target: $argument")
        }
    }
}
```

**Pattern: Event Listening**

```kotlin
// Annotation-based (recommended)
@Awake
object Listeners {
    @SubscribeEvent
    fun onJoin(event: PlayerJoinEvent) {
        event.player.sendMessage("Welcome!")
    }

    @SubscribeEvent(priority = EventPriority.HIGHEST, ignoreCancelled = true)
    fun onDamage(event: EntityDamageEvent) { /* ... */ }
}

// Functional style
listenEvent<PlayerJoinEvent> {
    it.player.sendMessage("Welcome!")
}
```

**Pattern: Chest UI**

```kotlin
player.openMenu<Chest> {
    title("My Menu")
    rows(3)
    map(
        "# # # # # # # # #",
        "# A # B # C # D #",
        "# # # # # # # # #"
    )
    set('A', buildItem(XMaterial.DIAMOND) { name = "&bDiamond"; colored() })
    onClick('A') { event -> event.clicker.sendMessage("Clicked!") }
    handLocked(false)
}
```

**Pattern: Database Table**

```kotlin
val table = Table<HostSQL, Connection>("player_data", host) {
    add("uuid") { type(ColumnTypeSQL.VARCHAR, 36) }
    add("data") { type(ColumnTypeSQL.TEXT) }
}

// Always use async for DB operations
submitAsync {
    table.createTable(dataSource)
    table.select(dataSource) {
        where { "uuid" eq player.uniqueId.toString() }
    }.firstOrNull()
}
```

**Pattern: Task Scheduling**

```kotlin
// Delayed sync task (20 ticks = 1 second)
submit(delay = 20L) { /* runs on main thread */ }

// Async repeating task
submit(async = true, period = 20L) { /* every 1 second, off main thread */ }

// Annotation-based
@Schedule(async = true, period = 100L, delay = 20L)
fun periodicTask() { /* called automatically */ }
```

**Pattern: NMS Version Guard**

```kotlin
if (MinecraftVersion.isHigherOrEqual(MinecraftVersion.V1_17)) {
    // 1.17+ specific code
}
// majorLegacy: 12004 = 1.20.4
val ver = MinecraftVersion.majorLegacy
```

### Step 4: Validation Checklist

Before the plugin is considered complete, verify:

- [ ] `build.gradle.kts` has correct `taboolib {}` block with needed modules
- [ ] Main class is an `object` extending `Plugin()`, not a `class`
- [ ] All stateful components use `@Awake object`, not global variables
- [ ] Database operations are wrapped in `submitAsync {}`
- [ ] NMS-dependent code has version guards
- [ ] Commands have proper permission nodes
- [ ] Config files use `@Config` + `@ConfigNode` for auto-injection
- [ ] No blocking operations on the main thread

## Examples

### Example 1: Basic Plugin with Config and Command

User says: "Create a TabooLib plugin with a config and a reload command"

Action:
1. Set up `build.gradle.kts` with `UNIVERSAL`, `BUKKIT`, `CONFIGURATION`
2. Create `Plugin` object main class
3. Create `Settings` object with `@Config`
4. Create command with `reload` subcommand
5. Create default `config.yml`

### Example 2: Plugin with Chest GUI

User says: "I need a shop GUI plugin with TabooLib"

Action:
1. Set up with `UNIVERSAL`, `BUKKIT`, `CONFIGURATION`, `CHAT`, `NMS`, `NMS_UTIL`, `UI`, `BUKKIT_ALL`
2. Create config for shop items
3. Build Chest menu with `map()` layout
4. Handle click events for purchase logic
5. Add NMS version check if using version-specific features

### Example 3: Plugin with Database

User says: "Player data storage plugin with MySQL"

Action:
1. Set up with `UNIVERSAL`, `BUKKIT`, `CONFIGURATION`, `DATABASE`
2. Define table schema using `Table` API
3. Create async data load/save in `@SubscribeEvent` handlers
4. Use `submitAsync {}` for all DB operations
5. Configure `config.yml` with database connection settings

## Troubleshooting

### Error: Module not found at runtime
- Cause: Module not installed in `taboolib { env { install(...) } }`
- Solution: Add the missing module constant. Check `references/module-map.md` for dependencies.

### Error: @Awake object not being discovered
- Cause: Missing `@Awake` annotation on the object, or object is in a package not scanned
- Solution: Ensure `@Awake` is on the object declaration. TabooLib scans all classes in the plugin JAR.

### Error: NMS operation fails on specific MC version
- Cause: NMS API changed between versions
- Solution: Use `MinecraftVersion.isHigherOrEqual()` guards. For packet operations, check field names per version.

### Error: Config not reloading
- Cause: `autoReload = true` not set, or `FileWatcher` not active
- Solution: Set `autoReload = true` in `@Config`. For manual reload call `config.reload()`.

### Error: UI clicks not registering
- Cause: Missing `handLocked(false)` or wrong slot mapping
- Solution: Verify `map()` character assignments match `set()` and `onClick()` characters.

### Error: Gradle build fails with TabooLib plugin
- Cause: Version mismatch or repository not configured
- Solution: Ensure `io.izzel.taboolib` plugin version matches, and `mavenCentral()` is in repositories.

### Error: Chinese filename causes server crash on restart
- Known bug: Avoid Chinese characters in config file names. Use ASCII-only filenames.
