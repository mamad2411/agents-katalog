---
name: paper-datapack-bundling
description: "Paper 插件內附資料包：在 PluginBootstrap 以 LifecycleEvents.DATAPACK_DISCOVERY 從 jar 載入資料包（配方、函式、進度、標籤），自動啟用、pack.mcmeta 版本範圍（1.21.11 = 94.1、26.3 = 121.0）、依版本選資料夾、DatapackManager 查詢 / Paper plugin-bundled data packs: discover a data pack inside the jar from a PluginBootstrap with LifecycleEvents.DATAPACK_DISCOVERY (recipes, functions, advancements, tags), auto-enable, pack.mcmeta format ranges (1.21.11 = 94.1, 26.3 = 121.0), per-version folders and DatapackManager checks"
---

# Paper Datapack Bundling

## Skill Name

`paper-datapack-bundling`

## Purpose

Some content is easier to write as data pack JSON than as Java: recipes, advancements, functions, loot tables, predicates, worldgen. Instead of asking admins to copy a folder into `world/datapacks/`, a Paper plugin can **ship the data pack inside its jar** and register it during bootstrap:

```java
event.registrar().discoverPack(uri, "content", c -> c.autoEnableOnServerStart(true));
```

What the Paper 26.3 implementation does (read from `PaperDatapackRegistrar`):

| Point | Behavior |
|------|------|
| Pack id | `<plugin name>/<id>`, e.g. `CustomContent/content` |
| Enabled? | `autoEnableOnServerStart` defaults to **false**: without it the pack is only discovered, not enabled |
| Invalid or missing pack | `discoverPack` returns `null` (no exception); check it |
| Position | `TOP` by default (overrides packs below it); `position(true, ...)` pins it there |

The template bundles a pack with a recipe, a load function and its `#minecraft:load` tag, enables it on start, and verifies it from `onEnable`.

## Paper Version Requirements

- Paper 1.21.11 / 26.3 (`DatapackRegistrar`, `DatapackManager` and `LifecycleEvents.DATAPACK_DISCOVERY` have identical signatures on both; both compile-verified)
- Data pack formats (from the vanilla `version.json` of each server):

| MC | Data pack format | `pack.mcmeta` |
|------|------|------|
| 1.21.11 | 94.1 | `"min_format": [94, 1]` |
| 26.2 | 107.1 | |
| 26.3 | 121.0 | `"min_format": 121` |

  Both versions use `min_format` / `max_format`; a range such as `[94, 1]`..`121` accepts both servers. The **contents** must then use JSON that both versions parse: crafting recipes, function files and function tags are written the same way on 1.21.11 and 26.3, while 26.3 renamed many loot table, predicate, advancement trigger and worldgen fields. Ship per-version folders (example 2) for those.
- **Spigot**: Paper only — `PluginBootstrap` and `DATAPACK_DISCOVERY` are Paper API; on Spigot the admin must install the data pack into `world/datapacks/`

## Triggers

- 「插件內附資料包」「bundle datapack」「datapack in plugin jar」「DATAPACK_DISCOVERY」
- 「DatapackRegistrar」「discoverPack」「DatapackManager」「autoEnableOnServerStart」
- 「pack.mcmeta」「pack_format」「min_format」「資料包版本」

## Inputs

| Parameter | Example | Description |
|------|------|------|
| `pack_id` | `content` | Becomes `<plugin>/content` |
| `contents` | recipe, load function, advancement | What the pack contains |
| `versions` | `1.21.11`, `26.3` | Decides the format range or per-version folders |

## Outputs

- `src/main/resources/datapack/` — the bundled pack (`pack.mcmeta`, `data/...`)
- `PackBootstrap.java` — discovers and auto-enables the pack; never throws
- `PackPlugin.java` — confirms in `onEnable` that the pack is enabled and its content loaded

## Build Setup

See [`references/paper-api-platform.md`](references/paper-api-platform.md). Only `paper-api` (`compileOnly`) is required. The plugin needs `paper-plugin.yml` with a `bootstrapper`:

```yaml
name: CustomContent
version: '${version}'
main: com.example.datapack.PackPlugin
bootstrapper: com.example.datapack.PackBootstrap
api-version: '26.3'   # 1.21.11 server: '1.21.11'
```

Gradle copies `src/main/resources/datapack/**` into the jar unchanged. If `processResources` expands `${...}` placeholders, limit `filesMatching` to `paper-plugin.yml` so the JSON files are not touched.

## Code Template

### `src/main/resources/datapack/pack.mcmeta`

```json
{
  "pack": {
    "description": "Example content bundled with the CustomContent plugin",
    "min_format": [94, 1],
    "max_format": 121
  }
}
```

### `src/main/resources/datapack/data/example/recipe/gravel_from_flint.json`

```json
{
  "type": "minecraft:crafting_shaped",
  "category": "building",
  "key": {
    "#": "minecraft:flint"
  },
  "pattern": [
    "##",
    "##"
  ],
  "result": {
    "id": "minecraft:gravel"
  }
}
```

### `src/main/resources/datapack/data/example/function/load.mcfunction`

```mcfunction
scoreboard objectives add example_deaths deathCount
```

### `src/main/resources/datapack/data/minecraft/tags/function/load.json`

```json
{
  "values": [
    "example:load"
  ]
}
```

### `PackBootstrap.java`

```java
package com.example.datapack;

import io.papermc.paper.datapack.Datapack;
import io.papermc.paper.datapack.DiscoveredDatapack;
import io.papermc.paper.plugin.bootstrap.BootstrapContext;
import io.papermc.paper.plugin.bootstrap.PluginBootstrap;
import io.papermc.paper.plugin.bootstrap.PluginProviderContext;
import io.papermc.paper.plugin.lifecycle.event.types.LifecycleEvents;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.logger.slf4j.ComponentLogger;
import org.bukkit.plugin.java.JavaPlugin;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * Registers the data pack under src/main/resources/datapack/ during bootstrap. Never throws: a failure only disables
 * the bundled content, and {@link PackPlugin} reports it.
 */
public final class PackBootstrap implements PluginBootstrap {

    static final String PACK_ID = "content";
    private static final String PACK_ROOT = "/datapack";

    private final List<String> problems = new CopyOnWriteArrayList<>();

    @Override
    public void bootstrap(BootstrapContext context) {
        ComponentLogger log = context.getLogger();
        try {
            context.getLifecycleManager().registerEventHandler(LifecycleEvents.DATAPACK_DISCOVERY, event -> {
                try {
                    URL root = PackBootstrap.class.getResource(PACK_ROOT);
                    if (root == null) {
                        problems.add(PACK_ROOT + " is missing from the jar");
                        return;
                    }
                    URI uri = root.toURI();
                    DiscoveredDatapack pack = event.registrar().discoverPack(uri, PACK_ID, config -> config
                            .title(Component.text("Example content"))
                            .autoEnableOnServerStart(true)            // default false: discovered but not enabled
                            .position(false, Datapack.Position.TOP)); // above vanilla; not pinned
                    if (pack == null) {
                        problems.add("pack rejected (pack.mcmeta missing, invalid or incompatible format)");
                    }
                } catch (URISyntaxException | IOException | RuntimeException e) {
                    log.error("Could not register the bundled data pack", e);
                    problems.add("discovery failed: " + e);
                }
            });
        } catch (RuntimeException e) {
            log.error("Could not register the datapack discovery handler", e);
            problems.add("bootstrap failed: " + e);
        }
    }

    @Override
    public JavaPlugin createPlugin(PluginProviderContext context) {
        return new PackPlugin(List.copyOf(problems));
    }
}
```

### `PackPlugin.java`

```java
package com.example.datapack;

import io.papermc.paper.datapack.Datapack;
import org.bukkit.NamespacedKey;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.List;

public final class PackPlugin extends JavaPlugin {

    private final List<String> bootstrapProblems;

    PackPlugin(List<String> bootstrapProblems) {
        this.bootstrapProblems = List.copyOf(bootstrapProblems);
    }

    @Override
    public void onEnable() {
        bootstrapProblems.forEach(problem -> getLogger().warning("Bundled data pack: " + problem));
        String id = getPluginMeta().getName() + "/" + PackBootstrap.PACK_ID;   // the id Paper assigns
        Datapack pack = getServer().getDatapackManager().getPack(id);
        if (pack == null || !pack.isEnabled()) {
            getLogger().warning("Data pack " + id + " is not enabled; its recipes and functions are unavailable");
            return;
        }
        if (getServer().getRecipe(new NamespacedKey("example", "gravel_from_flint")) == null) {
            getLogger().warning("Data pack " + id + " is enabled but its recipe did not load (check the server log for JSON errors)");
        }
    }
}
```

## Recommended Directory Structure

```
src/main/java/com/example/datapack/
├── PackBootstrap.java
└── PackPlugin.java
src/main/resources/
├── paper-plugin.yml
└── datapack/
    ├── pack.mcmeta
    └── data/
        ├── example/recipe/gravel_from_flint.json
        ├── example/function/load.mcfunction
        └── minecraft/tags/function/load.json
```

## Thread Safety

- The discovery handler runs during bootstrap: no Bukkit server, worlds or players; only resolve the resource and call the registrar
- `DatapackManager` lookups belong on the main thread (`onEnable`, commands)
- See [`references/paper-threading.md`](references/paper-threading.md)

### Key Techniques

| Topic | Approach |
|------|------|
| Find the folder in the jar | `PackBootstrap.class.getResource("/datapack").toURI()`; Paper opens the jar file system itself |
| Enable it | `autoEnableOnServerStart(true)`; otherwise admins must run `/datapack enable` |
| Know it worked | `discoverPack` returns `null` on failure; `getDatapackManager().getPack("<plugin>/<id>").isEnabled()` in `onEnable` |
| One pack, two versions | `min_format` / `max_format` range + only JSON both versions parse |
| Diverging JSON | One folder per version, chosen with `ServerBuildInfo.buildInfo().minecraftVersionId()` (example 2) |
| Data pack vs. Java | Prefer the data pack for recipes, advancements, loot and worldgen; use Java (`paper-custom-recipes`, `paper-registry-events`) when values come from config or code |

## Fallback

| Error | Cause | Fix |
|------|------|------|
| Pack listed by `/datapack list available` but not enabled | `autoEnableOnServerStart` not set | Set it to `true` |
| `discoverPack` returns `null` | `pack.mcmeta` missing or the format range excludes this server | Check the path inside the jar and the `min_format` / `max_format` numbers |
| Log shows "Couldn't parse data file" for one JSON | That file uses a format the running version does not accept (26.3 renamed many loot/predicate fields) | Split per version (example 2) |
| Recipe from the pack missing although the pack is enabled | JSON error in that file only; the rest of the pack still loads | Read the server log around data pack loading |
| `${...}` in JSON replaced or build fails in `processResources` | Resource expansion applied to every file | Restrict `filesMatching` to `paper-plugin.yml` |
| Plugin not loaded at all | Exception escaped bootstrap | Catch everything in the handler, report from `onEnable` |
