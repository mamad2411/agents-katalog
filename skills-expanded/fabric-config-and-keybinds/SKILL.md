---
name: fabric-config-and-keybinds
description: Add key bindings (KeyMappingHelper / KeyBindingHelper) and a configuration system to a Fabric mod - a dependency-free JSON config with Gson, or Cloth Config / YACL screens - plus optional Mod Menu integration. Use when a mod needs a toggle key, user settings, a config screen, or a "Configure" button in Mod Menu, or when key presses fire twice / not at all.
---

# Fabric config and key bindings

Key bindings and config screens are **client-side**: put them in `src/client` and register
them from the `ClientModInitializer`. The config *data* class can live in `src/main` if the
server also reads it.

## Step 0 - Names for your version

| | 26.3+ (SDL input) | 26.1 - 26.2 | 1.21.x Mojang mappings | Yarn (<= 1.21.11) |
|---|---|---|---|---|
| Helper | `KeyMappingHelper.registerKeyMapping` (`...client.keymapping.v1`) | same as 26.3 | `KeyBindingHelper.registerKeyBinding` (`...client.keybinding.v1`) | `KeyBindingHelper.registerKeyBinding` |
| Vanilla class | `KeyMapping` | `KeyMapping` | `KeyMapping` | `KeyBinding` |
| "was pressed" | `consumeClick()` | `consumeClick()` | `consumeClick()` | `wasPressed()` |
| Input type | `InputConstants.Type.KEYBOARD` | `InputConstants.Type.KEYSYM` | `InputConstants.Type.KEYSYM` | `InputUtil.Type.KEYSYM` |
| Key codes | `InputConstants.KEY_H` (**SDL scancodes**; raw: `org.lwjgl.sdl.SDLScancode.SDL_SCANCODE_H`) | `InputConstants.KEY_H` (GLFW key codes) | `InputConstants.KEY_H` / `GLFW.GLFW_KEY_H` | `GLFW.GLFW_KEY_H` |
| Category | `KeyMapping.Category.register(id)` (object) | same | object since 1.21.9, a translation-key **string** before | same split as Mojang |

**Minecraft 26.3 replaced GLFW with SDL for input.** `InputConstants.Type.KEYSYM` no longer
exists, key codes are SDL scancodes (numerically different from GLFW codes), and any
`org.lwjgl.glfw.GLFW` usage stops compiling. Always use the `InputConstants.KEY_*` constants
instead of raw numbers or GLFW constants so the code survives these changes.

Confirm in the decompiled sources for your version before writing code (`InputConstants`,
`KeyMapping` constructors). Docs: https://docs.fabricmc.net/develop/key-mappings

## Key bindings (26.3 shown)

```java
package com.example.examplemod.client;

import com.mojang.blaze3d.platform.InputConstants;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keymapping.v1.KeyMappingHelper;
import net.minecraft.client.KeyMapping;
import com.example.examplemod.ExampleMod;

public class ExampleModClient implements ClientModInitializer {
    private static final KeyMapping.Category CATEGORY =
        KeyMapping.Category.register(ExampleMod.id("main"));

    private static KeyMapping toggleHud;

    @Override
    public void onInitializeClient() {
        toggleHud = KeyMappingHelper.registerKeyMapping(new KeyMapping(
            "key.examplemod.toggle_hud",       // translation key
            InputConstants.Type.KEYBOARD,      // KEYBOARD or MOUSE (26.1 - 26.2 and older: KEYSYM)
            InputConstants.KEY_H,              // default key; use InputConstants.UNKNOWN.getValue() for "unbound"
            CATEGORY
        ));

        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            while (toggleHud.consumeClick()) {          // while, not if: drains queued presses
                ExampleConfig cfg = ExampleConfig.get();
                cfg.hudEnabled = !cfg.hudEnabled;
                ExampleConfig.save();
            }
        });
    }
}
```

`assets/examplemod/lang/en_us.json`:

```json
{
  "key.category.examplemod.main": "Example Mod",
  "key.examplemod.toggle_hud": "Toggle HUD"
}
```

(Category translation key format for the object-style category: `key.category.<namespace>.<path>`.)

Pre-1.21.9 category, for reference: pass a string such as `"category.examplemod.main"` as the
last constructor argument and translate that string.

Key binding rules:

- Register once, in `onInitializeClient`, and keep the returned instance.
- Poll with `consumeClick()` in a `while` loop inside `ClientTickEvents.END_CLIENT_TICK`. Use
  `isDown()` only for "held" behaviour (e.g. zoom while held).
- Key presses are not delivered to `consumeClick` while a screen is open. To react inside a
  screen, use `ScreenKeyboardEvents` (see the docs page) or the screen's own key handler.
- Choose defaults that do not clash with vanilla or very popular mods; unbound by default is
  fine for niche actions. Users rebind in Options -> Controls.
- Never read raw GLFW key state for game actions; it ignores user rebinding.

## Config, option A: plain JSON with Gson (no dependencies)

Gson ships with Minecraft, so this needs nothing extra. Good default for small mods.

```java
package com.example.examplemod.config;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonParseException;
import net.fabricmc.loader.api.FabricLoader;
import com.example.examplemod.ExampleMod;

import java.io.IOException;
import java.io.Reader;
import java.io.Writer;
import java.nio.file.AtomicMoveNotSupportedException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

public final class ExampleConfig {
    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();
    private static final Path PATH = FabricLoader.getInstance().getConfigDir().resolve(ExampleMod.MOD_ID + ".json");
    private static ExampleConfig instance = new ExampleConfig();

    // Fields with defaults. Bump CONFIG_VERSION and migrate when you rename/remove fields.
    public int configVersion = 1;
    public boolean hudEnabled = true;
    public int hudX = 4;
    public int hudY = 4;

    public static ExampleConfig get() { return instance; }

    public static void load() {
        if (Files.notExists(PATH)) { save(); return; }
        try (Reader reader = Files.newBufferedReader(PATH)) {
            ExampleConfig loaded = GSON.fromJson(reader, ExampleConfig.class);
            instance = loaded != null ? loaded.validated() : new ExampleConfig();
        } catch (IOException | JsonParseException e) {
            ExampleMod.LOGGER.error("Invalid config {}, using defaults", PATH, e);
            instance = new ExampleConfig();   // do NOT overwrite the user's broken file silently
        }
    }

    public static void save() {
        try {
            Files.createDirectories(PATH.getParent());
            Path tmp = PATH.resolveSibling(PATH.getFileName() + ".tmp");
            try (Writer writer = Files.newBufferedWriter(tmp)) {
                GSON.toJson(instance, writer);
            }
            try {
                Files.move(tmp, PATH, StandardCopyOption.REPLACE_EXISTING, StandardCopyOption.ATOMIC_MOVE);
            } catch (AtomicMoveNotSupportedException e) {   // some network/synced drives
                Files.move(tmp, PATH, StandardCopyOption.REPLACE_EXISTING);
            }
        } catch (IOException e) {
            ExampleMod.LOGGER.error("Could not save config {}", PATH, e);
        }
    }

    private ExampleConfig validated() {
        hudX = Math.max(0, hudX);
        hudY = Math.max(0, hudY);
        return this;
    }
}
```

Call `ExampleConfig.load()` once from the initializer. Read values through `get()` (in memory);
never read the file from render or tick code.

## Config, option B: a config library with a ready-made screen

| Library | Good for | Where |
|---|---|---|
| **YACL** (Yet Another Config Lib) | Modern, nice screens, built-in serialization | https://modrinth.com/mod/yacl - docs https://docs.isxander.dev/yet-another-config-lib |
| **Cloth Config** | Long-established, many mods use it | https://modrinth.com/mod/cloth-config - docs https://shedaniel.gitbook.io/cloth-config |

Before adding one:

1. Check on Modrinth that a build exists **for your exact Minecraft version**. Libraries lag
   behind new Minecraft releases; if none exists yet, use option A and add a screen later.
2. Copy the Maven repository and coordinates from the library's own docs (do not guess the
   group id or version).
3. Declare it with the right configuration for your Loom flavour and add it to
   `fabric.mod.json` `depends` (it becomes a hard requirement for players).

```groovy
// 26.1+ (non-remapping Loom)
repositories { maven { url = "<library maven from its docs>" } }
dependencies { implementation "<group>:<artifact>:<version>" }

// <= 1.21.11 (remapping Loom)
dependencies { modImplementation "<group>:<artifact>:<version>" }
```

Generate the screen from the library and return it as a `Screen` with a parent - that is all
Mod Menu needs.

## Mod Menu integration (optional, soft dependency)

Mod Menu shows a "Configure" button if you provide a `modmenu` entrypoint.

`build.gradle` - compile against it, run with it in dev, but do not require it:

```groovy
repositories { maven { name = "Terraformers"; url = "https://maven.terraformersmc.com/releases/" } }
dependencies {
    // 26.1+:
    compileOnly "com.terraformersmc:modmenu:${project.modmenu_version}"
    localRuntime "com.terraformersmc:modmenu:${project.modmenu_version}"
    // <= 1.21.11 use modCompileOnly / modLocalRuntime instead
}
```

Look up `modmenu_version` for your Minecraft version on https://modrinth.com/mod/modmenu/versions.

```java
package com.example.examplemod.client.compat;

import com.terraformersmc.modmenu.api.ConfigScreenFactory;
import com.terraformersmc.modmenu.api.ModMenuApi;

public class ModMenuIntegration implements ModMenuApi {
    @Override
    public ConfigScreenFactory<?> getModConfigScreenFactory() {
        return parent -> new ExampleConfigScreen(parent);
    }
}
```

`fabric.mod.json`:

```json
"entrypoints": {
  "main": ["com.example.examplemod.ExampleMod"],
  "client": ["com.example.examplemod.client.ExampleModClient"],
  "modmenu": ["com.example.examplemod.client.compat.ModMenuIntegration"]
},
"suggests": { "modmenu": "*" }
```

The `modmenu` entrypoint is only instantiated when Mod Menu is installed, so the soft
dependency is safe as long as **no other class** references Mod Menu types.

A hand-written `ExampleConfigScreen` is a normal `Screen` (see the `fabric-client-rendering`
skill) with widgets such as `CycleButton.onOffBuilder(...)` that write to the config and
call `ExampleConfig.save()` in `onClose()`.

## Syncing config with a server

Client-only preferences (HUD position, colours) stay on the client. Gameplay rules that the
server enforces must be read **on the server** from the server's config; if the client needs
to know them, send them with a payload (see `fabric-networking`). Never let a client config
value decide a gameplay outcome on the server.

## Common mistakes

- Using `KeyBindingHelper`/`KeyBinding`/`wasPressed()` on 26.1+, or `KeyMappingHelper` on
  1.21.x.
- `if (key.consumeClick())` instead of `while` - presses get lost or delayed.
- Registering the key mapping inside the tick event or re-registering on every world join.
- Passing a string category on 1.21.9+ or a `Category` object on older versions.
- Forgetting the translation keys, so Controls shows `key.examplemod.toggle_hud`.
- Reading/writing the config file every frame or tick.
- Writing the config non-atomically, or overwriting a user's malformed config with defaults
  without telling them.
- Hard `depends` on Mod Menu, or referencing Mod Menu classes outside the `modmenu`
  entrypoint class (crash when it is absent).
- Using `modImplementation` with non-remapping Loom (26.1+) or `implementation` for mods with
  remapping Loom.
- Adding a config library that has no build for the target Minecraft version.
- Trusting client-side config on the server.
