---
name: fabric-mixins
description: Write, review or fix Mixins in a Fabric mod - choosing between a Fabric API event and a mixin, @Inject, @Redirect, @ModifyVariable, the safer MixinExtras injectors (@WrapOperation, @ModifyExpressionValue, @WrapWithCondition, @Local), accessors/invokers, class tweakers (access wideners), cross-mod compatibility and debugging with mixin.debug.export. Use whenever a task needs to change vanilla behaviour, read private fields, or when a mixin fails to apply.
---

# Fabric mixins

Mixins patch Minecraft's bytecode at load time. They are powerful and fragile: every mixin is a
promise that a specific method, with a specific shape, still exists in the next version and
that no other mod changes it incompatibly. Write as few as possible, as narrow as possible.

## Decision order - try these before writing a mixin

1. **Fabric API event or registry.** Search Fabric API first: lifecycle events
   (`ServerLifecycleEvents`, `ClientTickEvents`), player events (`UseBlockCallback`,
   `AttackEntityCallback`, `PlayerBlockBreakEvents`), HUD (`HudElementRegistry`), screens
   (`ScreenEvents`), loot (`LootTableEvents`), commands (`CommandRegistrationCallback`),
   networking, item tooltips, resource reload listeners, and many more.
   Browse https://github.com/FabricMC/fabric-api (each module's `api` package) and the Fabric
   docs. An event is stable across versions and composes with other mods for free.
2. **Vanilla extension points.** Data-driven content (tags, loot tables, recipes, data
   components, registries) often needs no code patching at all.
3. **Accessor / Invoker mixin** - when you only need to *read/write* a private field or *call*
   a private method.
4. **Class tweaker (access widener)** - when you need to subclass a final class, override a
   final method, or name a private/package-private class.
5. **Injector mixin** - only now. Prefer MixinExtras injectors over `@Redirect`/`@Overwrite`.

Write down (in a comment above the mixin) why steps 1-4 did not work. Reviewers will ask.

## Before writing any injector: confirm the target

Names and signatures change every Minecraft version. Never write a target from memory.

```bash
./gradlew genSources        # then open the class in the IDE or search the generated sources
```

- 26.1+ (unobfuscated): target the Mojang names exactly as they appear in the sources.
- Pre-26.1: target the names of **your project's mappings** (Yarn or Mojang). Loom's mixin
  annotation processor remaps them to intermediary at build time; a mismatch shows as a
  "Cannot remap" warning at compile time - treat that warning as an error.
- Copy method descriptors from the bytecode view or a tool (MCDev IntelliJ plugin, mcsrc.dev),
  not by hand. Descriptor reference: https://docs.fabricmc.net/develop/mixins/bytecode

## Mixin config and conventions

```json
{
  "required": true,
  "package": "com.example.examplemod.mixin",
  "compatibilityLevel": "JAVA_25",
  "mixins": ["LivingEntityMixin", "accessor.LivingEntityAccessor"],
  "client": [],
  "server": [],
  "injectors": { "defaultRequire": 1 },
  "overwrites": { "requireAnnotations": true }
}
```

- `"defaultRequire": 1` makes a mixin that matches nothing **fail loudly** instead of silently
  doing nothing. Keep it.
- Client-only targets (`net.minecraft.client.*`) go in the client config (in
  `src/client/resources`, declared with `"environment": "client"` in `fabric.mod.json`).
- Mixin classes are never referenced from normal code (except accessor interfaces, via a cast).
- Prefix every added member with your mod id to avoid collisions with other mods:
  `examplemod$onTick`, `@Unique private int examplemod$counter;`.
- Mark helper fields/methods you add with `@Unique`.
- Handler methods are `private` (non-static if the target is non-static).

> The targets in the examples below use Mojang names and show the **shape** of each injector.
> Method names and descriptors drift between versions - re-check every one of them in your
> generated sources before reusing it.

## @Inject - run code at a point, optionally cancel

```java
@Mixin(LivingEntity.class)
public abstract class LivingEntityMixin {
    @Inject(method = "jumpFromGround", at = @At("HEAD"), cancellable = true)
    private void examplemod$cancelJump(CallbackInfo ci) {
        if (ExampleConfig.get().disableJump) {
            ci.cancel();
        }
    }

    // getJumpPower is overloaded (getJumpPower() and getJumpPower(float)): give the descriptor.
    @Inject(method = "getJumpPower()F", at = @At("RETURN"), cancellable = true)
    private void examplemod$boostJump(CallbackInfoReturnable<Float> cir) {
        cir.setReturnValue(cir.getReturnValueF() * 1.5f);
    }
}
```

- `CallbackInfo` for `void` targets, `CallbackInfoReturnable<T>` otherwise (boxed type).
- Only declare `cancellable = true` when you actually cancel. Cancelling at `HEAD` skips the
  vanilla method *and every other mod's injection after yours* - it is the least compatible
  thing an `@Inject` can do. Prefer modifying a value.
- To read the target's parameters, add them to the handler signature **before** the
  `CallbackInfo`, in order: `(float amount, CallbackInfo ci)`.
- Common `@At` values: `HEAD`, `RETURN` (every return), `TAIL` (last return only),
  `INVOKE` (before a call; add `shift = At.Shift.AFTER` for after), `FIELD`, `NEW`.
- Use `ordinal` only when you must; it breaks as soon as Mojang adds another matching call.

## MixinExtras - use these instead of @Redirect and most @ModifyVariable

MixinExtras ships inside Fabric Loader (0.15+), so no extra dependency is needed. Imports are
under `com.llamalad7.mixinextras`. Docs: https://github.com/LlamaLad7/MixinExtras/wiki

### @ModifyExpressionValue - change what a call/field read returns

```java
@ModifyExpressionValue(
    method = "travelInWater",
    at = @At(value = "INVOKE",
             target = "Lnet/minecraft/world/entity/LivingEntity;getSpeed()F")
)
private float examplemod$fasterInWater(float original) {
    return original * 1.2f;
}
```

Multiple mods can chain `@ModifyExpressionValue` on the same expression; each receives the
previous mod's result. A `@Redirect` on the same call would conflict and crash.

### @WrapOperation - wrap a call; call the original (or not)

```java
@WrapOperation(
    method = "hurtServer",
    at = @At(value = "INVOKE",
             target = "Lnet/minecraft/world/entity/LivingEntity;actuallyHurt(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/damagesource/DamageSource;F)V")
)
private void examplemod$logDamage(LivingEntity self, ServerLevel level, DamageSource source,
                                  float amount, Operation<Void> original) {
    ExampleMod.LOGGER.debug("{} took {} damage", self, amount);
    original.call(self, level, source, amount);   // keep the chain intact
}
```

- Parameters: the receiver (for non-static calls), then the call's arguments, then
  `Operation<R>` where `R` is the boxed return type (`Void` for `void`).
- **Always call `original.call(...)`** unless skipping the call is the feature. Not calling it
  silently disables every other mod's wrapper on the same call.

### @WrapWithCondition - conditionally skip a void call

```java
@WrapWithCondition(
    method = "render",
    at = @At(value = "INVOKE", target = "Lsome/Target;drawThing(...)V")
)
private boolean examplemod$hideThing(Target instance /*, call args... */) {
    return !ExampleConfig.get().hideThing;   // false = skip the call
}
```

### @Local - read a local variable without @ModifyVariable

```java
@Inject(method = "tick", at = @At(value = "INVOKE", target = "..."))
private void examplemod$readLocal(CallbackInfo ci, @Local(name = "pos") BlockPos pos) { ... }
```

On 26.1+ the game ships parameter and local names, so `@Local(name = ...)` is reliable there.
Pre-26.1 (no local names in obfuscated jars) prefer `@Local(ordinal = n)` by type, and check
it with `mixin.debug.export`.

### Other useful MixinExtras tools

`@ModifyReturnValue` (change a method's return value at `RETURN`, chains with other mods),
`@ModifyReceiver`, `@WrapMethod` (wrap a whole method), `@Share` (pass a value between two
injectors in the same method), `@Cancellable` (cancel from inside a `@WrapOperation`).

## @Redirect and @ModifyVariable - only when nothing else fits

- `@Redirect` **replaces** a call. Only one mod can redirect a given call; a second mod's
  `@Redirect` (or a `@WrapOperation` applied on top of a redirected call in some orders) fails
  with a hard crash. Use `@WrapOperation` instead.
- `@ModifyVariable` targets a local by type and ordinal, which shifts between versions. Use
  `@ModifyExpressionValue` on the expression that produces the value, or `@Local` to read it.
- `@Overwrite` replaces the whole method: incompatible with every other mod touching it. Do not
  use it in a public mod.

## Accessors and invokers

```java
package com.example.examplemod.mixin.accessor;

@Mixin(LivingEntity.class)
public interface LivingEntityAccessor {
    @Accessor("noJumpDelay")
    int examplemod$getNoJumpDelay();

    @Accessor("noJumpDelay")
    void examplemod$setNoJumpDelay(int value);

    @Invoker("getJumpPower")
    float examplemod$invokeGetJumpPower();
}

// usage
int delay = ((LivingEntityAccessor) entity).examplemod$getNoJumpDelay();
```

- Instance accessor methods get the mod-id prefix; static ones (`static T getX() { throw new
  AssertionError(); }`) do not need it.
- `@Mutable` on a setter removes `final` from the target field.
- Constructor invoker: `@Invoker("<init>") static Foo examplemod$new(...)`.
- Accessors work on other mods' classes too; class tweakers only work on vanilla.

## Class tweakers (formerly access wideners)

Needed to subclass a `final` class, override a `final` method, or reference a non-public class.
Requires Loader 0.18+ and Loom 1.12+; older setups use the same syntax under the name
"access widener" with an `accessWidener v2 named` header.

`src/main/resources/examplemod.classtweaker`:

```
classTweaker v1 official
accessible  class   net/minecraft/world/inventory/MenuType$MenuSupplier
accessible  method  net/minecraft/network/chat/TextColor  formatValue  ()Ljava/lang/String;
accessible  field   net/minecraft/world/damagesource/DamageSources  damageTypes  Lnet/minecraft/core/Registry;
```

Wire it up in **both** places, then refresh Gradle and re-run `genSources`:

```groovy
loom { accessWidenerPath = file("src/main/resources/examplemod.classtweaker") }
```
```json
"accessWidener": "examplemod.classtweaker"
```

Run `./gradlew validateAccessWidener` - invalid entries are otherwise silently ignored. Use
`transitive-` directives only when mods depending on yours must see the change. Header details,
v2 features (interface injection, enum extension): https://docs.fabricmc.net/develop/class-tweakers/

## Cross-mod compatibility checklist

- Inject at the narrowest point that works; never cancel at `HEAD` of a widely used method
  (`tick`, `render`, `hurt`, `travel`) unless you are sure.
- Prefer injectors that chain (`@ModifyExpressionValue`, `@ModifyReturnValue`,
  `@WrapOperation`) over injectors that replace (`@Redirect`, `@Overwrite`).
- Use `@Unique` + mod-id prefix for all added state.
- Avoid `ordinal` and `@At("TAIL")` when `@At("RETURN")` works.
- Use `@Mixin(value = X.class, priority = ...)` only to resolve a known conflict; document it.
- Optional mixins targeting another mod: put them in a separate config and gate them with a
  mixin plugin (`IMixinConfigPlugin#shouldApplyMixin` checking
  `FabricLoader.getInstance().isModLoaded("othermod")`), or use `"require": 0` on that injector.
- Known heavy patchers (Sodium, Iris, Lithium, ImmediatelyFast) replace large parts of the
  renderer and game logic. If you inject into rendering or entity ticking, test with them.

## Debugging mixins

Add JVM args to the dev run configs:

```groovy
loom {
    runs {
        configureEach {
            vmArg "-Dmixin.debug.export=true"     // writes transformed classes to run/.mixin.out/
            vmArg "-Dmixin.debug.verbose=true"
            vmArg "-Dmixin.dumpTargetOnFailure=true"
        }
    }
}
```

- `run/.mixin.out/class/...` contains the transformed classes - decompile them to see exactly
  what your injector produced and in which order other mods' injectors ran.
- `-Dmixin.checks.interfaces=true` verifies that mixins implement interface methods.
- Error decoding (target not found, `InvalidInjectionException`, conflicting redirects): see
  the `fabric-crash-debugging` skill.

## Common mistakes

- Writing a mixin for something Fabric API already has an event for (HUD, ticks, block use,
  tooltips, commands, loot tables).
- Guessing a method name or descriptor from memory or a different version/mappings set. Always
  check generated sources first.
- Using Yarn names (`MinecraftClient`, `PlayerEntity`) in a Mojang-named project or vice versa.
- `@Redirect` where `@WrapOperation`/`@ModifyExpressionValue` would do; `@Overwrite` in a
  public mod.
- `cancellable = true` + `ci.cancel()` at `HEAD` as the default way to "change" behaviour.
- Forgetting `original.call(...)` in `@WrapOperation`.
- Wrong `CallbackInfoReturnable` generic (primitive instead of boxed), or missing the
  target's parameters before `ci` when you need them.
- Mixin class not listed in the config, listed in the wrong section (`mixins` vs `client`), or
  in a package different from the config's `package`.
- Client targets in the common config: crashes dedicated servers at startup.
- Referencing a mixin class directly from normal code (`new LivingEntityMixin()`), or putting
  non-mixin helper classes inside the mixin package.
- Non-`@Unique`, non-prefixed fields that collide with another mod's mixin.
- Turning off `defaultRequire` to "fix" a failing mixin - this hides the bug and ships a mod
  that silently does nothing.
- Class tweaker declared in only one of `build.gradle` / `fabric.mod.json`, or not validated.
