---
name: fabric-version-porting
description: Port a Fabric mod from one Minecraft version to another - including the big Yarn -> Mojang mappings migration required for Minecraft 26.1+, Fabric API renames, reading Fabric and Minecraft changelogs, and fixing compile errors and broken mixins until the build passes. Use when asked to update, port, bump or "make it work on" a different Minecraft version.
---

# Fabric version porting

Porting is a loop: **bump -> build -> read the first error -> look up the new API -> fix ->
build again**. The skill is in doing it in the right order and never guessing new names.

## Step 1 - Establish where you are and where you are going

```bash
grep -E "minecraft_version|yarn_mappings|loader_version|loom_version|fabric_api_version" gradle.properties
grep -nE "fabric-loom|mappings|modImplementation" build.gradle
git status                      # must be clean - commit or stash first
```

Then classify the jump:

| From | To | Difficulty |
|---|---|---|
| X.Y.a | X.Y.b (patch, e.g. 1.21.4 -> 1.21.5) | Can still be large: Mojang ships big refactors in "minor" drops |
| any 1.21.x, **Yarn** | **26.1+** | **Two migrations**: Yarn -> Mojang names first, then the version bump. Never both at once |
| any 1.21.x, Mojang mappings | 26.1+ | Remove remapping (plugin id, `mappings` line, `mod*` configs), then fix renames |
| 26.x | 26.y | Mojang names on both sides; normal version bump |

Create a branch: `git switch -c port/<target-version>`.

## Step 2 - Gather the change information (read before editing)

| Source | What it tells you |
|---|---|
| https://fabricmc.net/blog/ | Fabric's "Fabric for Minecraft X" post: Loader/Loom/API breaking changes, renamed APIs |
| https://docs.fabricmc.net/develop/porting/ | Version-specific porting guide (use the version selector); for 26.1 there is a full Fabric API rename list and an IntelliJ migration map |
| https://fabricmc.net/develop/ | The exact Loader / Loom / Fabric API versions for the target |
| https://github.com/FabricMC/fabric-example-mod (history) | How the template's `build.gradle`, Java version and Gradle version changed |
| Minecraft.net Java Edition release article + Minecraft Wiki version page | Gameplay and data-format changes |
| NeoForge's version primers (`neoforged.net` blog / `NeoForged/.github` primers) | Very detailed vanilla code changes between versions; loader-agnostic for vanilla classes |
| Your dependencies' Modrinth pages | Whether Mod Menu, YACL, etc. have a build for the target yet |

If a required dependency has no build for the target version, stop and tell the user - do not
remove features silently.

## Step 3 - (Only if leaving Yarn) migrate mappings on the OLD version first

Do this while still on the old Minecraft version, so the code compiles before and after.

```bash
# Requires Loom 1.13+ on the old version. Replace 1.21.11 with your CURRENT version.
./gradlew migrateMappings --mappings "net.minecraft:mappings:1.21.11" --overrideInputsIHaveABackup
./gradlew migrateClientMappings --mappings "net.minecraft:mappings:1.21.11" --overrideInputsIHaveABackup   # split source sets
./gradlew migrateClassTweakerMappings --mappings "net.minecraft:mappings:1.21.11" --overrideInputsIHaveABackup
```

Then in `build.gradle` replace the Yarn line with `mappings loom.officialMojangMappings()`,
remove `yarn_mappings` from `gradle.properties`, refresh Gradle and build.

- `migrateMappings` does **not** handle Kotlin; use the Ravel IntelliJ plugin for Kotlin (it
  also handles complex projects better because it resolves through the IDE).
- Mixin targets in string form (`method = "..."`, `target = "L...;"`) are often **not**
  rewritten. Grep every mixin and fix the strings by hand:
  `grep -rn "target = \|method = " src/*/java/**/mixin`.
- Commit this step on its own: `git commit -m "Migrate Yarn to Mojang mappings"`.

Docs: https://docs.fabricmc.net/develop/porting/mappings/

## Step 4 - Bump the build

1. Gradle wrapper: `./gradlew wrapper --gradle-version <version the template uses>` (run twice
   if the first run upgrades the wrapper only).
2. `gradle.properties`: `minecraft_version`, `loader_version`, `loom_version`,
   `fabric_api_version`, and every dependency version - all from Step 2 sources.
3. Java: set `options.release`, `sourceCompatibility`, mixin `compatibilityLevel`, and
   `fabric.mod.json` `"java"` to what the target requires (26.x template: 25; 1.20.5 - 1.21.x: 21).
4. Crossing into 26.1+:
   - plugin id `net.fabricmc.fabric-loom-remap` / `fabric-loom` -> `net.fabricmc.fabric-loom`
   - delete the `mappings` line
   - `modImplementation` -> `implementation`, `modCompileOnly` -> `compileOnly`,
     `modLocalRuntime` -> `localRuntime`, `modApi` -> `api`
   - anything using `remapJar` (publishing tasks, CI artifact paths) -> `jar`
5. `fabric.mod.json`: update `depends.minecraft` (`~<target>`), `fabricloader`, `java`.
6. `./gradlew --refresh-dependencies build` (or `./gradlew build --refresh-dependencies`).

## Step 5 - Fix compile errors systematically

- Work through errors **in order of dependency**: registration/common code first, then client,
  then mixins. Fixing a core type often clears dozens of errors at once.
- For each unknown symbol, find the new name - do not invent one:
  1. Search the Fabric API rename list / porting page for that version.
  2. Search generated sources (`./gradlew genSources`) for the class or for a nearby string or
     constant you know is still there.
  3. Look at how vanilla itself does it now (e.g. how vanilla's own HUD or screens draw).
  4. Use https://mappings.dev or Linkie (https://linkie.shedaniel.dev) to translate between
     Yarn / Mojang / intermediary names for older versions.
- Use the IntelliJ migration map from the 26.1 porting page to bulk-rename Fabric API classes.
- Keep behaviour identical; a port is not the time to refactor.

### Typical renames you will meet

Fabric API 26.1 (Yarn-flavoured names -> official names), excerpt:

| Old | New |
|---|---|
| `KeyBindingHelper.registerKeyBinding` (`client.keybinding.v1`) | `KeyMappingHelper.registerKeyMapping` (`client.keymapping.v1`) |
| `PayloadTypeRegistry.playS2C()` / `playC2S()` | `clientboundPlay()` / `serverboundPlay()` |
| `S2CPlayChannelEvents` / `C2SPlayChannelEvents` | `ClientboundPlayChannelEvents` / `ServerboundPlayChannelEvents` |
| `PacketByteBufs` | `FriendlyByteBufs` |
| `WorldRenderEvents` / `WorldRenderContext` (`rendering.v1.world`) | `LevelRenderEvents` / `LevelRenderContext` (`rendering.v1.level`) |
| `ClientTickEvents.EndWorldTick` / `ServerWorldEvents` | `EndLevelTick` / `ServerLevelEvents` |
| `ItemGroupEvents`, `FabricItemGroup` (`itemgroup.v1`) | `CreativeModeTabEvents`, `FabricCreativeModeTab` (`creativetab.v1`) |
| `ClientCommandManager` | `ClientCommands` |
| `BlockRenderLayerMap` | `ChunkSectionLayerMap` |
| `ColorProviderRegistry.BLOCK` | `BlockColorRegistry` |
| `TooltipComponentCallback` | `ClientTooltipComponentCallback` |
| `EntityModelLayerRegistry` | `ModelLayerRegistry` |
| `FabricTagProvider` (and nested `...TagProvider`) | `FabricTagsProvider` (`...TagsProvider`) |
| `ExtendedScreenHandlerType` (`screenhandler.v1`) | `ExtendedMenuType` (`menu.v1`) |
| `FuelRegistryEvents` | `FuelValueEvents` |

Full list: https://docs.fabricmc.net/26.1/develop/porting/fabric-api

Vanilla, Yarn -> Mojang (the names you will see most):

| Yarn | Mojang |
|---|---|
| `MinecraftClient` | `Minecraft` |
| `DrawContext` | `GuiGraphics` (26.1+: `GuiGraphicsExtractor`) |
| `TextRenderer` | `Font` |
| `Text` / `Formatting` | `Component` / `ChatFormatting` |
| `PlayerEntity` / `ServerPlayerEntity` / `ClientPlayerEntity` | `Player` / `ServerPlayer` / `LocalPlayer` |
| `World` / `ServerWorld` / `ClientWorld` | `Level` / `ServerLevel` / `ClientLevel` |
| `BlockState`, `BlockPos` | unchanged |
| `Identifier.of(ns, path)` | `Identifier.fromNamespaceAndPath(ns, path)` (`ResourceLocation` before 1.21.11) |
| `ItemStack#getItem`, `Item.Settings` | `ItemStack#getItem`, `Item.Properties` |
| `ScreenHandler` | `AbstractContainerMenu` |
| `MatrixStack` | `PoseStack` |
| `KeyBinding#wasPressed` | `KeyMapping#consumeClick` |
| `Registries.ITEM` / `Registry.register` | `BuiltInRegistries.ITEM` / `Registry.register` |
| `NbtCompound` | `CompoundTag` |
| `CustomPayload` / `PacketCodec` | `CustomPacketPayload` / `StreamCodec` |

26.1 -> 26.2 also renamed vanilla rendering entry points (for example `Screen#render` ->
`extractRenderState`, `GuiGraphics#drawString` -> `text`, `minecraft.setScreen` ->
`minecraft.gui.setScreen`). 26.3 replaced GLFW with **SDL** for input: `InputConstants.Type.KEYSYM`
became `KEYBOARD`, key codes are SDL scancodes, and `org.lwjgl.glfw` imports stop compiling (use
`InputConstants.KEY_*` constants). The F1 flag moved from `options.hideGui` to
`gui.hud.isHidden()`. Expect similar churn in every release and verify in sources.

## Step 6 - Fix mixins (they fail at runtime, not compile time)

A mixin whose target moved still compiles. Find them before users do:

1. `./gradlew build` and read every mixin annotation-processor warning ("Cannot find target",
   "Cannot remap") - treat each as an error.
2. `./gradlew runClient` (and `runServer`) with `"defaultRequire": 1` in the mixin configs;
   any target that no longer matches crashes at startup with the mixin and method named.
3. For each failing mixin, open the target in the new sources and re-derive the injection
   point. Often the logic moved to another method or class; sometimes a new Fabric API event
   makes the mixin unnecessary - prefer deleting the mixin when it does.
4. Re-run with `-Dmixin.debug.export=true` to inspect the result (see `fabric-mixins`).

## Step 7 - Verify behaviour, then finish

- `./gradlew build` passes with no new warnings.
- `runClient`: join a singleplayer world, exercise every feature, open every screen.
- `runServer` (if the mod is not client-only): starts without `ClassNotFoundException` or
  "invalid dist" errors; join it from the dev client if possible.
- Update `CHANGELOG.md`, `mod_version` (porting alone is usually a minor/patch bump - see
  `fabric-release`), README "supported versions", and CI matrices.
- Commit in logical steps: mappings migration, build bump, code fixes, mixin fixes.

## Supporting several versions

If the user needs more than one Minecraft version at once, do not interleave versions with
`if` checks at runtime. Use one git branch per version (simplest) or a preprocessor-based
multi-version setup (e.g. Stonecutter). Ask the user before introducing the latter.

## Common mistakes

- Bumping Minecraft and migrating Yarn -> Mojang in the same step; nothing compiles and the
  migration tools stop working (they need the old version to resolve names).
- Guessing new names from memory instead of the rename list or generated sources.
- Keeping a `mappings` line, `modImplementation`, `remapJar` or the old plugin id after moving
  to 26.1+.
- Forgetting to bump Java (`options.release`, mixin `compatibilityLevel`, `fabric.mod.json`).
- Updating `build.gradle` but not `fabric.mod.json` `depends.minecraft`, so the mod refuses to
  load (or worse, loads on the wrong version).
- Declaring the port finished when it compiles. Mixins and registries fail at runtime - run the
  client and server.
- Silently deleting a feature or a mixin that no longer compiles. Report it to the user.
- Dropping a dependency because "it has no version yet" without asking.
- Large opportunistic refactors during the port, which make regressions impossible to bisect.
