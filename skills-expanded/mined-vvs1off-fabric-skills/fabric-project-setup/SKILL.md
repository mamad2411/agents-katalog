---
name: fabric-project-setup
description: Set up or repair a Minecraft Fabric mod project - build.gradle, gradle.properties, settings.gradle, fabric.mod.json, entrypoints, mixin configs, mappings choice and the client/common source split. Use when creating a new Fabric mod, when a Fabric build fails to configure, when choosing Loom/Loader/Fabric API versions, or when code ends up on the wrong side (client vs server).
---

# Fabric project setup

This skill gets a Fabric mod project into a state where `./gradlew build` works and the
structure matches what current Fabric tooling expects.

## Step 0 - Find out which era you are in (do this first)

Fabric changed fundamentally at **Minecraft 26.1**: the game ships **unobfuscated**, Yarn is
**discontinued**, and Loom has a new plugin id. Almost every "it doesn't compile" problem an
agent causes comes from mixing the two eras.

| | Minecraft **26.1 and newer** | Minecraft **1.21.11 and older** |
|---|---|---|
| Names in code | Mojang official names (`Minecraft`, `GuiGraphicsExtractor`, `KeyMapping`) | Yarn (`MinecraftClient`, `DrawContext`, `KeyBinding`) **or** Mojang mappings |
| `mappings` line in `build.gradle` | **none** - there is nothing to map | `mappings "net.fabricmc:yarn:..."` or `mappings loom.officialMojangMappings()` |
| Loom plugin id | `net.fabricmc.fabric-loom` | `net.fabricmc.fabric-loom-remap` (legacy alias: `fabric-loom`) |
| Mod dependency configs | plain `implementation`, `compileOnly`, `runtimeOnly` | `modImplementation`, `modCompileOnly`, `modLocalRuntime` |
| Output jar task | `jar` | `remapJar` |
| Java | check the template (26.x templates use Java 25) | Java 21 for 1.20.5 - 1.21.x, Java 17 for 1.18 - 1.20.4 |

How to tell which one an **existing** project is in:

```bash
grep -nE "fabric-loom|mappings|modImplementation" build.gradle
grep -nE "minecraft_version|yarn_mappings" gradle.properties
```

- `yarn_mappings` / `mappings "net.fabricmc:yarn` -> Yarn era. Do not add Mojang names to it.
- No `mappings` line and plugin `net.fabricmc.fabric-loom` -> unobfuscated era.
- If you are asked to move a Yarn project to 26.1+, that is a port: use the
  `fabric-version-porting` skill, not this one.

## Step 1 - Look up current versions (never hardcode from memory)

Version numbers in your training data are stale. Fetch them every time:

| What | Where |
|---|---|
| Minecraft, Loader, Loom, Fabric API for a given MC version | https://fabricmc.net/develop/ (pick the version in the dropdown) |
| Machine-readable game/loader versions | `https://meta.fabricmc.net/v2/versions/game` and `https://meta.fabricmc.net/v2/versions/loader` |
| Loader + mappings for one game version | `https://meta.fabricmc.net/v2/versions/loader/<mc_version>` |
| Yarn builds (pre-26.1 only) | `https://meta.fabricmc.net/v2/versions/yarn/<mc_version>` |
| Fabric API builds | https://modrinth.com/mod/fabric-api/versions (version looks like `0.x.y+<mc_version>`) |
| Loom | the `loom_version` in https://github.com/FabricMC/fabric-example-mod (`gradle.properties`) |
| Canonical template | https://github.com/FabricMC/fabric-example-mod or the generator at https://fabricmc.net/develop/template/ |
| Docs for your exact version | https://docs.fabricmc.net/develop/ (use the version selector in the header) |

| Latest Minecraft release vs snapshot (fallback if meta is unreachable) | `https://piston-meta.mojang.com/mc/game/version_manifest_v2.json` -> `latest.release` |
| Fabric API builds as Maven metadata | `https://maven.fabricmc.net/net/fabricmc/fabric-api/fabric-api/maven-metadata.xml` (pick versions ending in `+<your mc version>`) |

If you cannot reach the network, say so and leave clearly marked placeholders
(`minecraft_version=<CHECK fabricmc.net/develop>`) instead of guessing.

Prefer the **latest stable** Minecraft release (meta marks it `"stable": true`; Mojang's
manifest lists it as `latest.release`); do not pick a snapshot, pre-release or release
candidate unless asked. Beware: Fabric API is also built for snapshots, so the `<latest>` in
the Maven metadata is often a snapshot build (e.g. `+26.4` while 26.4 is still a snapshot).
Never treat "a Fabric API build exists" as "this Minecraft version is released".

## Step 2 - Standard layout

```
examplemod/
├── build.gradle
├── gradle.properties
├── settings.gradle
├── gradle/wrapper/...            # commit the wrapper; never hand-edit the jar
├── gradlew / gradlew.bat
└── src/
    ├── main/                     # common code: runs on BOTH client and dedicated server
    │   ├── java/com/example/examplemod/
    │   │   ├── ExampleMod.java           # ModInitializer
    │   │   └── mixin/                    # common mixins
    │   └── resources/
    │       ├── fabric.mod.json
    │       ├── examplemod.mixins.json
    │       └── assets/examplemod/{icon.png, lang/en_us.json}
    └── client/                   # client-only code: rendering, screens, keybinds, HUD
        ├── java/com/example/examplemod/client/
        │   ├── ExampleModClient.java     # ClientModInitializer
        │   └── mixin/                    # client mixins
        └── resources/
            └── examplemod.client.mixins.json
```

The `src/client` source set is created by `splitEnvironmentSourceSets()`. Code in `src/main`
**cannot** import anything from `src/client` - the compiler enforces the side split, which is
the whole point. If common code needs to trigger client behaviour, send a packet or use an
interface implemented on the client side.

## Step 3 - Build files (unobfuscated era, 26.1+)

`gradle.properties` - fill every value from Step 1:

```properties
org.gradle.jvmargs=-Xmx2G
org.gradle.parallel=true
org.gradle.configuration-cache=true

# Fabric - look these up on https://fabricmc.net/develop
minecraft_version=<from fabricmc.net/develop>
loader_version=<from fabricmc.net/develop>
loom_version=<from fabric-example-mod>
fabric_api_version=<from fabricmc.net/develop>

# Mod
mod_version=0.1.0
maven_group=com.example
archives_base_name=examplemod
```

`settings.gradle`:

```groovy
pluginManagement {
    repositories {
        maven { name = 'Fabric'; url = 'https://maven.fabricmc.net/' }
        mavenCentral()
        gradlePluginPortal()
    }
}
rootProject.name = 'examplemod'
```

`build.gradle`:

```groovy
plugins {
    id 'net.fabricmc.fabric-loom' version "${loom_version}"
    id 'maven-publish'
}

version = project.mod_version
group = project.maven_group
base { archivesName = project.archives_base_name }

repositories {
    // Only add repositories for other mods you depend on (Mod Menu, YACL, ...).
    // Loom already adds Fabric, Mojang and Maven Central.
}

loom {
    splitEnvironmentSourceSets()
    mods {
        "examplemod" {                      // must equal the "id" in fabric.mod.json
            sourceSet sourceSets.main
            sourceSet sourceSets.client
        }
    }
}

dependencies {
    minecraft "com.mojang:minecraft:${project.minecraft_version}"
    implementation "net.fabricmc:fabric-loader:${project.loader_version}"
    implementation "net.fabricmc.fabric-api:fabric-api:${project.fabric_api_version}"
}

processResources {
    def version = project.version
    inputs.property "version", version
    filesMatching("fabric.mod.json") { expand "version": version }
}

tasks.withType(JavaCompile).configureEach {
    it.options.release = 25                 // match the template for your MC version
}

java {
    withSourcesJar()
    sourceCompatibility = JavaVersion.VERSION_25
    targetCompatibility = JavaVersion.VERSION_25
}

jar {
    def projectName = project.name
    inputs.property "projectName", projectName
    from("LICENSE") { rename { "${it}_${projectName}" } }
}
```

### Differences for 1.21.11 and older (remapping Loom)

```groovy
plugins {
    id 'net.fabricmc.fabric-loom-remap' version "${loom_version}"   // older templates: 'fabric-loom'
}
dependencies {
    minecraft "com.mojang:minecraft:${project.minecraft_version}"
    mappings loom.officialMojangMappings()          // or: "net.fabricmc:yarn:${project.yarn_mappings}:v2"
    modImplementation "net.fabricmc:fabric-loader:${project.loader_version}"
    modImplementation "net.fabricmc.fabric-api:fabric-api:${project.fabric_api_version}"
}
```

Java release: 21 for 1.20.5 - 1.21.x, 17 for 1.18 - 1.20.4. The distributable jar is produced by
`remapJar` (the plain `jar` output is the `-dev` jar and will not load in a real game).

### Choosing mappings for pre-26.1 projects

- **New** pre-26.1 project: prefer Mojang mappings (`loom.officialMojangMappings()`). It makes
  a later port to 26.1+ a version bump instead of a rename of every symbol.
- **Existing** Yarn project: keep Yarn until you port; switching mappings is a separate,
  deliberate migration (`migrateMappings`), never a side effect of another change.
- Never mix: a Yarn project cannot reference `GuiGraphics`, a Mojang project cannot reference
  `DrawContext`.

## Step 4 - fabric.mod.json

```json
{
  "schemaVersion": 1,
  "id": "examplemod",
  "version": "${version}",
  "name": "Example Mod",
  "description": "What the mod does, in one sentence.",
  "authors": ["YOUR_NAME"],
  "contact": {
    "homepage": "https://example.com",
    "sources": "https://github.com/YOUR_NAME/examplemod",
    "issues": "https://github.com/YOUR_NAME/examplemod/issues"
  },
  "license": "MIT",
  "icon": "assets/examplemod/icon.png",
  "environment": "*",
  "entrypoints": {
    "main": ["com.example.examplemod.ExampleMod"],
    "client": ["com.example.examplemod.client.ExampleModClient"]
  },
  "mixins": [
    "examplemod.mixins.json",
    { "config": "examplemod.client.mixins.json", "environment": "client" }
  ],
  "depends": {
    "fabricloader": ">=<loader_version>",
    "minecraft": "~<minecraft_version>",
    "java": ">=<java_release>",
    "fabric-api": ">=<fabric_api_version without +mc suffix>"
  }
}
```

Rules that are easy to get wrong:

- `id`: 2-64 chars, lowercase `a-z`, digits, `-`, `_`; must start with a letter. It must match
  the `loom { mods { ... } }` key and your asset namespace (`assets/<id>/`).
- `"version": "${version}"` is expanded by `processResources`; do not hardcode it.
- `"environment"`: `"*"` (both), `"client"` (client-only mod, e.g. HUD/minimap mods) or
  `"server"`. A client-only mod should still keep client code in `src/client`.
- `"fabric-api"`: prefer a lower bound such as `">=0.165.0"` (the version you build against)
  over `"*"`, so players with an older Fabric API get a clear Loader error instead of a
  `NoClassDefFoundError` crash.
- `"minecraft"` range: `~1.21.4` means `>=1.21.4 <1.22`; for year-based versions `~26.3` means
  `>=26.3 <26.4`. Use an exact or tilde range - `"*"` lets users crash on incompatible versions.
- Every entrypoint class must exist at that exact fully-qualified name.
- Optional integrations go in `"suggests"` (soft) or `"recommends"`, never in `"depends"`.
  Example: `"suggests": { "modmenu": "*" }` plus a `"modmenu"` entrypoint.
- Schema reference: https://docs.fabricmc.net/develop/loader/fabric-mod-json

## Step 5 - Entrypoints

```java
package com.example.examplemod;

import net.fabricmc.api.ModInitializer;
import net.minecraft.resources.Identifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ExampleMod implements ModInitializer {
    public static final String MOD_ID = "examplemod";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    @Override
    public void onInitialize() {
        // Common setup: registries, payload types, server events, commands.
        LOGGER.info("Initializing {}", MOD_ID);
    }

    public static Identifier id(String path) {
        return Identifier.fromNamespaceAndPath(MOD_ID, path);
    }
}
```

```java
package com.example.examplemod.client;

import net.fabricmc.api.ClientModInitializer;

public class ExampleModClient implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        // Client setup: key mappings, HUD elements, screens, client packet receivers.
    }
}
```

Name check for older versions: `Identifier.fromNamespaceAndPath` is the Mojang name from
1.21.11 onward. Mojang-mapped 1.21 - 1.21.10 call it `ResourceLocation.fromNamespaceAndPath`,
and Yarn calls it `Identifier.of(...)`. Verify against your generated sources instead of
trusting this line.

## Step 6 - Mixin configs

`src/main/resources/examplemod.mixins.json`:

```json
{
  "required": true,
  "package": "com.example.examplemod.mixin",
  "compatibilityLevel": "JAVA_25",
  "mixins": [],
  "injectors": { "defaultRequire": 1 },
  "overwrites": { "requireAnnotations": true }
}
```

`src/client/resources/examplemod.client.mixins.json` is the same with
`"package": "com.example.examplemod.client.mixin"` and the classes listed under `"client"`
instead of `"mixins"`. Set `compatibilityLevel` to your Java release (`JAVA_21` for 1.21.x).
Mixin classes listed here must live **in exactly that package**, and the package must contain
**only** mixin classes. See the `fabric-mixins` skill before writing any.

## Step 7 - Verify

```bash
./gradlew build          # must pass before you claim the setup works
./gradlew genSources     # decompiled Minecraft sources: the source of truth for names
./gradlew runClient      # or runServer, to smoke-test the entrypoints
```

After `genSources`, look up any vanilla class or method name in the generated sources (or with
your IDE's "go to class") **before** writing code against it. Names you remember may be from
another version or another mapping set.

## Common mistakes

- Copying a 1.20/1.21 Yarn tutorial into a 26.x project (`MinecraftClient`, `DrawContext`,
  `Text.literal`, `modImplementation`, a `mappings` line). None of it compiles on 26.1+.
- Adding `mappings loom.officialMojangMappings()` to a 26.1+ project. There is nothing to map;
  remove the line.
- Using `id 'fabric-loom'` on 26.1+ - it is the legacy remapping plugin id.
- Using `modImplementation` with non-remapping Loom, or plain `implementation` for a mod
  dependency with remapping Loom (the mod will not be remapped and will crash at runtime).
- Hardcoding versions from memory, or picking a snapshot as "latest".
- Putting client classes (`Minecraft`, `GuiGraphicsExtractor`, `KeyMapping`, anything in
  `net.minecraft.client`) in `src/main`. It compiles in a single-source-set project and then
  crashes a dedicated server with `ClassNotFoundException` / "attempted to load class ... for
  invalid dist".
- Mod id mismatch between `fabric.mod.json`, `loom.mods`, `MOD_ID` and the `assets/` folder.
- A mixin config `package` that does not match where the classes are, or non-mixin classes
  inside the mixin package.
- Declaring the client mixin config without `"environment": "client"`.
- Forgetting `processResources` expansion and shipping a jar whose version is literally
  `${version}`.
- Distributing the `-dev` jar (pre-26.1) instead of the `remapJar` output.
- Committing `run/`, `build/`, `.gradle/` or anything containing credentials.
