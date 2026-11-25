---
name: fabric-crash-debugging
description: Diagnose and fix Minecraft Fabric crashes and load failures - reading crash reports and latest.log, Mixin errors (InvalidInjectionException, "could not find any targets", "@Redirect conflict", MixinApplyError), dependency and version resolution errors from Fabric Loader, client/server class-loading crashes (ClassNotFoundException, "invalid dist"), NoSuchMethodError/NoSuchFieldError from version mismatches, and Gradle/Loom build failures. Use whenever the user pastes a crash report, a stack trace, a log, or says the game or build crashes.
---

# Fabric crash debugging

Crashes are evidence. Read them in a fixed order and you will find the cause in the first 50
lines almost every time. Never "fix" a crash by guessing; locate the frame first.

## Where to look

| File | Contains |
|---|---|
| `run/crash-reports/crash-<date>-<side>.txt` (dev) / `.minecraft/crash-reports/` | Full crash report for crashes after the game started |
| `run/logs/latest.log` | Everything, including Loader resolution errors and mixin failures that happen *before* a crash report can be written |
| `run/logs/debug.log` | Same with debug level (if enabled) |
| `hs_err_pid*.log` in the run dir | **Native/JVM** crash (GPU driver, out of memory) - not a Java bug in your mod |
| Gradle output / `--stacktrace` | Build-time failures |

If the user pastes only the last lines, ask for the whole crash report or `latest.log` - the
cause is near the **top**, the bottom is just `main` unwinding.

## Reading a crash report, in order

1. **Description line** (`Description: ...`) - what the game was doing (ticking entity,
   rendering screen, initializing game, loading level).
2. **The exception type and message** - the first `java.lang....` / `org.spongepowered...`
   line.
3. **`Caused by:` chain** - scroll to the **last** `Caused by:`; it is usually the real cause.
4. **The first stack frame in mod code** - look for your package (`com.example.examplemod`)
   or a mixin handler (`handler$xyz000$examplemod$methodName`, or the merged method name with
   your `examplemod$` prefix). That frame is your starting point.
5. **"Mixins in Stacktrace"** / mixin info section (Fabric adds it) - lists which mods' mixins
   are applied to the classes in the stack. A different mod may be the cause.
6. **System details** at the bottom: Minecraft version, Java version, Loader version, mod list.
   Check for duplicates and for mods built for another Minecraft version.

## Loader resolution errors (game never starts)

`latest.log` shows `Incompatible mods found!` or `Mod resolution encountered an incompatible
mod set!` with lines like:

```
- Mod 'Example Mod' (examplemod) 0.1.0 requires version 0.165.0 or later of fabric-api, which is missing!
- Mod 'Example Mod' (examplemod) 0.1.0 requires any version of minecraft between 26.2 and 26.3 (exclusive), but only the wrong version is present: 26.3!
```

Fixes: install/update the named dependency, or correct the range in `fabric.mod.json`
`depends`. Also check for: two copies of the same mod, a mod with a duplicate id, a
`breaks` entry triggering, wrong `"java"` range.

## Mixin failures

| Message | Meaning | Fix |
|---|---|---|
| `InvalidInjectionException: Critical injection failure: @Inject annotation on X could not find any targets matching 'foo'` | The target method name/descriptor does not exist (renamed, signature changed, wrong mappings, wrong side) | Re-check the target in generated sources for this exact version; fix `method`/`target` strings |
| `... could not find any targets matching ... in ...` from `@At(INVOKE, target=...)` | The call you inject at is gone or its descriptor changed | Re-derive the `target` descriptor; consider a different anchor |
| `Injection validation failed: ... expected N invocation(s) but M succeeded` (`require`/`defaultRequire`) | Fewer matches than required | Same as above; don't lower `require` to hide it |
| `InvalidInjectionException: Invalid descriptor on handler` / `Expected (L...;)V but found ...` | Handler signature wrong: missing/extra params, wrong `CallbackInfo` type, primitive vs boxed in `CallbackInfoReturnable<T>`, wrong `Operation<T>` | Make the handler match the target exactly (params in order, then `ci`/`cir`/`original`) |
| `@Redirect conflict. Skipping ... with priority ...` / `... is already redirected by ...` | Two mods redirect the same call | Replace your `@Redirect` with `@WrapOperation`/`@ModifyExpressionValue` |
| `MixinApplyError` / `MixinTransformerError: An unexpected critical error was encountered` | Wrapper - read the nested `Caused by:` for the real one | Follow the cause |
| `Mixin target X was not found` / `ClassNotFoundException` for a target | Target class does not exist on this side or version (often a client class in the common config) | Move the mixin to the client config, or fix the class name |
| `IllegalClassLoadError: ... is in a defined mixin package` | Normal code references a class inside the mixin package | Move helper classes out of the mixin package; access accessor interfaces only by cast |
| `NoSuchMethodError` pointing at a mixin-added method | Missing `@Unique` / name collision or a non-applied mixin | Add `@Unique` + mod-id prefix; make sure the mixin is listed in the config |

Tools:

- Add `-Dmixin.debug.export=true` to the run config, reproduce, and read
  `run/.mixin.out/class/...` (decompile in the IDE) to see what was actually generated and which
  mods touched that class.
- `-Dmixin.debug.verbose=true` logs each mixin as it applies.
- `-Dmixin.dumpTargetOnFailure=true` dumps the target class when an injection fails.

## Client / server side crashes

Typical messages on a **dedicated server**:

```
java.lang.RuntimeException: Cannot load class net.minecraft.client.Minecraft in environment type SERVER
java.lang.NoClassDefFoundError: net/minecraft/client/gui/screens/Screen
java.lang.ClassNotFoundException: net.minecraft.client.player.LocalPlayer
```

Cause: common code (`src/main`, the `main` entrypoint, a common mixin, a payload record, a
static initializer, or a lambda) references a client-only class. The JVM loads the class the
first time a method that mentions it is **verified**, so even an unexecuted branch can crash.

Fixes:

- Enable `splitEnvironmentSourceSets()` (see `fabric-project-setup`) so the compiler rejects
  this; move client code to `src/client`.
- Move client mixins to the client mixin config.
- Never put client types in method signatures, fields or lambdas of common classes. Route
  through the `client` entrypoint, an interface, or a packet.
- Logical-side bugs (singleplayer works, server does not) usually mean logic ran on
  `level.isClientSide()`, or the client mutated state the server never learned about.

## Version-mismatch errors

```
java.lang.NoSuchMethodError: 'void net.minecraft.client.gui.GuiGraphics.drawString(...)'
java.lang.NoSuchFieldError: ...
java.lang.AbstractMethodError: Receiver class ... does not define or inherit an implementation of ...
java.lang.IncompatibleClassChangeError
```

A mod (yours or another) was compiled against a different Minecraft or library version than
the one running. Check: the mod jar targets this exact MC version; `fabric.mod.json` range is
not too wide (`"minecraft": "*"`); the dependency jar matches; you are not running the `-dev`
jar (pre-26.1) outside the dev environment.

## Common runtime exceptions in mod code

- `NullPointerException` on `Minecraft.getInstance().player` / `.level` - accessed on the title
  screen or during world join. Guard with null checks.
- `ConcurrentModificationException` / "Accessing LegacyRandomSource from multiple threads" /
  "Async ... not on the main thread" - world access from a network or worker thread; schedule it
  with `server.execute(...)` / `client.execute(...)`.
- `IllegalStateException: Registry is already frozen` / registering too late - register in
  `onInitialize`, not on world load or lazily.
- `Missing model`/purple-black textures: not a crash; the log says which resource path was
  expected (`assets/<modid>/...`). Check namespace and file names (lowercase).

## Build (Gradle / Loom) failures

| Symptom | Likely cause |
|---|---|
| `Plugin [id: 'net.fabricmc.fabric-loom'...] was not found` | Missing Fabric maven in `settings.gradle` `pluginManagement`, or wrong plugin id for this MC era |
| `Unsupported class file major version` / `requires Java NN` | Gradle running on a JDK older than required; set `JAVA_HOME` / IDE Gradle JDK |
| `Could not find net.fabricmc.fabric-api:fabric-api:...` | Version typo or a version that does not exist for that MC version - re-check on fabricmc.net/develop |
| Errors mentioning `mappings` on 26.1+ | A leftover `mappings` line - remove it |
| Weird cache errors, half-downloaded jars | `./gradlew build --refresh-dependencies`; as a last resort delete `.gradle/loom-cache` |
| `Cannot remap` / mixin AP warnings (pre-26.1) | Mixin target names not in the project's mappings - fix them, they will crash at runtime |

Run with `--stacktrace` (or `--info`) to get the real cause of a Gradle failure.

## Workflow when the cause is not obvious

1. Reproduce in dev with only your mod + Fabric API.
2. If it only happens with other mods, add them back in halves (binary search) until the
   pair is found; then read the mixin section of the crash report for both.
3. Add a breakpoint at the first mod frame and run `runClient` in debug mode, or add a
   `LOGGER.debug` with the values involved.
4. Write down the root cause before changing code, and make the smallest fix.

## Common mistakes

- Reading only the bottom of the stack trace.
- Lowering `require`/`defaultRequire` or wrapping code in `try/catch(Throwable)` to make a
  crash "go away" - the feature silently stops working.
- Blaming Fabric API or Minecraft before checking which mod's frame or mixin is involved.
- Treating `hs_err_pid` (native) crashes as Java bugs in the mod.
- Fixing a dedicated-server `ClassNotFoundException` by wrapping the call in an `isClient`
  check instead of moving the code out of the common class.
- Asking the user for "the error" and then working from a screenshot of the last 10 lines -
  ask for the full `latest.log` or crash report file.
