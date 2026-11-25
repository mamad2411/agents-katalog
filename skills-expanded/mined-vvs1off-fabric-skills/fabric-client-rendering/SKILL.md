---
name: fabric-client-rendering
description: Draw things on the Minecraft client with Fabric - HUD elements (HudElementRegistry and the older HUD callbacks), GUI drawing (GuiGraphicsExtractor / GuiGraphics / DrawContext depending on version), text and Components, item tooltips, custom Screens and widgets, and render performance. Use when adding or fixing a HUD overlay, screen, tooltip or any per-frame client drawing code.
---

# Fabric client rendering

All code in this skill is **client-only**: it belongs in `src/client/java` and is registered
from your `ClientModInitializer`. Referencing it from common code crashes dedicated servers.

## Step 0 - Which drawing API does this version have?

The GUI drawing class and the HUD API were renamed several times. Check before writing code:

```bash
grep -E "minecraft_version|yarn_mappings" gradle.properties
grep -n "mappings" build.gradle
```

| Version / mappings | GUI draw class | Screen draw method | Text method | HUD API |
|---|---|---|---|---|
| 26.1+ (Mojang, unobfuscated) | `GuiGraphicsExtractor` | `extractRenderState(graphics, mouseX, mouseY, delta)` | `graphics.text(font, ...)` | `HudElementRegistry` |
| 1.21.6 - 1.21.11, Mojang mappings | `GuiGraphics` | `render(graphics, mouseX, mouseY, delta)` | `graphics.drawString(font, ...)` | `HudElementRegistry` |
| 1.21.6 - 1.21.11, Yarn | `DrawContext` | `render(context, mouseX, mouseY, delta)` | `context.drawText(textRenderer, ...)` | `HudElementRegistry` |
| 1.21.2 - 1.21.5 | as above for your mappings | `render(...)` | as above | `HudLayerRegistrationCallback` (`HudRenderCallback` deprecated) |
| 1.20 - 1.21.1 | as above for your mappings | `render(...)` | as above | `HudRenderCallback` |

Then confirm in the actual dependency, because names keep moving (26.2 moved
`minecraft.setScreen` to `minecraft.gui.setScreen`, for example):

```bash
./gradlew genSources
# open HudElementRegistry / your GUI draw class in the IDE, or read Fabric API's sources jar
```

Version-matched guides with working code: https://docs.fabricmc.net/develop/rendering/hud (use
the version selector at the top of the page).

The examples below use the **26.1+ Mojang names**. Translate through the table for older
versions; the structure is identical.

## HUD elements (HudElementRegistry)

```java
package com.example.examplemod.client;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.rendering.v1.hud.HudElementRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.hud.VanillaHudElements;
import net.minecraft.client.DeltaTracker;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import com.example.examplemod.ExampleMod;

public class ExampleModClient implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        HudElementRegistry.attachElementAfter(
            VanillaHudElements.HOTBAR, ExampleMod.id("coords"), ExampleModClient::extractCoords);
    }

    private static void extractCoords(GuiGraphicsExtractor graphics, DeltaTracker delta) {
        Minecraft mc = Minecraft.getInstance();
        // F1 "hide HUD": mc.gui.hud.isHidden() on 26.3; mc.options.hideGui on older versions.
        if (mc.player == null || mc.gui.hud.isHidden() || !ExampleConfig.get().showCoords) {
            return;
        }
        graphics.text(mc.font, CoordsText.current(mc.player), 4, 4, 0xFFFFFFFF, true);
    }
}
```

`HudElementRegistry` methods: `addFirst`, `addLast`, `attachElementBefore`,
`attachElementAfter` (relative to a `VanillaHudElements` id such as `HOTBAR`, `CHAT`,
`CROSSHAIR`, `BOSS_BAR`, `SCOREBOARD`), `removeElement` and `replaceElement` (for hiding or
wrapping a vanilla element). The API handles layering; you do not manage z offsets.

Rules for HUD code:

- Return early when `mc.player == null`, when the HUD is hidden with F1 (`mc.gui.hud.isHidden()`
  on 26.3, `mc.options.hideGui` on older versions - Fabric does not hide your element for
  you), and when your
  feature is disabled. Also consider hiding while the F3 debug screen is open if your element
  would overlap it (look up the debug-overlay accessor in your version's sources).
- Position relative to `graphics.guiWidth()` / `graphics.guiHeight()` (scaled size), never
  hardcoded pixel assumptions about the window.
- Use `DeltaTracker#getGameTimeDeltaPartialTick(false)` for tick-interpolated animation and
  `Util.getMillis()` for wall-clock animation.

### Older HUD callbacks (pre-1.21.6)

```java
// 1.20 - 1.21.1 (Mojang names shown; Yarn: DrawContext, RenderTickCounter)
HudRenderCallback.EVENT.register((graphics, deltaTracker) -> { /* draw */ });
```

`HudLayerRegistrationCallback` (1.21.2 - 1.21.5) registers layers relative to
`IdentifiedLayer` ids, similar in spirit to `HudElementRegistry`. Check the docs page for that
exact version before using it.

## Drawing primitives

```java
graphics.fill(x1, y1, x2, y2, 0x80000000);                     // ARGB! 0x80 = 50% alpha
graphics.outline(x, y, width, height, 0xFFFF0000);
graphics.fillGradient(x1, y1, x2, y2, 0xFFFF0000, 0xFF0000FF);
graphics.horizontalLine(x1, x2, y, color);
graphics.verticalLine(x, y1, y2, color);

graphics.enableScissor(x1, y1, x2, y2);   // clip; calls must be balanced
// ... draw ...
graphics.disableScissor();

graphics.blit(RenderPipelines.GUI_TEXTURED, ExampleMod.id("textures/gui/icon.png"),
              x, y, 0, 0, 16, 16, 16, 16);   // pipeline, texture, x, y, u, v, w, h, texW, texH
graphics.blitSprite(RenderPipelines.GUI_TEXTURED, spriteId, x, y, w, h);   // GUI atlas sprite
graphics.centeredText(font, component, centerX, y, 0xFFFFFFFF);
graphics.setTooltipForNextFrame(font, component, mouseX, mouseY);
graphics.item(stack, x, y);               // item icon (26.x name; older: renderItem / drawItem)
```

**Colors are ARGB since 1.21.6.** `0xFFFFFF` is fully transparent white and renders nothing.
Use `0xFFFFFFFF`, or wrap RGB with `ARGB.opaque(rgb)`. This is the most common "my text does
not show up" bug when porting older code.

## Text

```java
Component title = Component.translatable("hud.examplemod.title");        // localized
Component value = Component.literal(String.valueOf(count)).withStyle(ChatFormatting.GREEN);
int width = mc.font.width(title);
graphics.text(mc.font, title, x, y, 0xFFFFFFFF, true);   // last arg: drop shadow
```

- Put user-visible strings in `assets/<modid>/lang/en_us.json` and use
  `Component.translatable`. Hardcoded English in `Component.literal` cannot be translated.
- Yarn equivalents: `Text.translatable`, `Text.literal`, `Formatting`, `textRenderer`.

## Tooltips

Append lines to any item's tooltip without a mixin:

```java
ItemTooltipCallback.EVENT.register((stack, tooltipContext, tooltipFlag, lines) -> {
    if (stack.is(Items.COMPASS)) {
        lines.add(Component.translatable("tooltip.examplemod.compass").withStyle(ChatFormatting.GRAY));
    }
});
```

`ItemTooltipCallback` lives in `net.fabricmc.fabric.api.client.item.v1`. For your **own**
items, override the item's tooltip method or use a data component instead. Use
`tooltipFlag.isAdvanced()` to gate debug info behind F3+H.

## Custom screens

```java
public class ExampleScreen extends Screen {
    private final Screen parent;

    public ExampleScreen(Screen parent) {
        super(Component.translatable("screen.examplemod.title"));
        this.parent = parent;
    }

    @Override
    protected void init() {   // called on open AND on every resize - rebuild widgets here
        this.addRenderableWidget(Button.builder(Component.translatable("gui.done"), b -> this.onClose())
            .bounds(this.width / 2 - 100, this.height - 28, 200, 20)
            .build());
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float delta) {
        super.extractRenderState(graphics, mouseX, mouseY, delta);   // background + widgets
        graphics.centeredText(this.font, this.title, this.width / 2, 15, 0xFFFFFFFF);
    }

    @Override
    public void onClose() {
        this.minecraft.gui.setScreen(this.parent);   // 26.2+; earlier: this.minecraft.setScreen(...)
    }
}
```

- Create widgets in `init()`, not in the constructor; `init()` reruns on resize and the
  widget list is cleared each time.
- Always keep a `parent` and return to it (Mod Menu and options screens rely on this).
- Open a screen from a key press or tick handler on the client thread. Opening it from a
  network handler or another thread needs `client.execute(() -> ...)`.
- Prefer vanilla widgets (`Button`, `EditBox`, `CycleButton`, `AbstractSliderButton`) before
  writing custom ones.

## Performance - this code runs every frame

HUD and screen draw methods run 60-500+ times per second. Treat them as a hot loop:

- **No allocations per frame** where avoidable: no `new` objects, no `String.format`, no string
  concatenation in the draw path, no streams/lambdas created per call, no `Component.literal`
  of a value that has not changed. Cache the `Component` and rebuild it only when the
  underlying value changes (e.g. on a tick event, or when the block position differs).
- **No game-state work in render**: no world scans, entity searches, raycasts, file I/O,
  config reads from disk, or registry lookups. Compute in `ClientTickEvents.END_CLIENT_TICK`
  (20 times/s) and draw the cached result.
- Do not log from the render path.
- Avoid one-off textures uploaded each frame; register textures once.
- Measure with the F3 frame-time graph or a profiler (Spark) before and after.

```java
// Good: recompute at most once per tick, only if changed
public final class CoordsText {
    private static Component cached = Component.empty();
    private static BlockPos last = null;

    public static void onTick(Minecraft mc) {             // from END_CLIENT_TICK
        if (mc.player == null) return;
        BlockPos pos = mc.player.blockPosition();
        if (!pos.equals(last)) {
            last = pos;
            cached = Component.translatable("hud.examplemod.coords", pos.getX(), pos.getY(), pos.getZ());
        }
    }

    public static Component current(LocalPlayer player) { return cached; }
}
```

## World rendering

Drawing in the 3D world (outlines, boxes, lines) uses `LevelRenderEvents` (26.1+; named
`WorldRenderEvents` before) and render pipelines, and changes nearly every version as Mojang
rewrites the renderer. Read https://docs.fabricmc.net/develop/rendering/world for your exact
version and copy its structure; do not adapt a world-rendering snippet from another version.

## Common mistakes

- Using `DrawContext`/`MatrixStack`/`TextRenderer` (Yarn) in a Mojang-named project, or
  `GuiGraphics` in a 26.1+ project where it is `GuiGraphicsExtractor`.
- Overriding `render(...)` in a 26.1+ `Screen` - the method is `extractRenderState`; the old
  name compiles only if you also forget `@Override`, then never runs. Always use `@Override`.
- RGB colors (`0xFFFFFF`) after 1.21.6 -> invisible text and fills.
- Using deprecated `HudRenderCallback` on 1.21.6+, or a mixin into the vanilla `Gui` class
  for a simple overlay.
- Allocating strings/components every frame, or doing world queries inside the HUD callback.
- Not checking `mc.player == null` (crash on the title screen) or ignoring the F1 hide-HUD
  state.
- Building widgets in the `Screen` constructor instead of `init()`.
- Forgetting to call `super.extractRenderState(...)` / `super.render(...)` and losing the
  background and all widgets.
- Hardcoded English strings instead of translation keys.
- Placing any of this in `src/main`.
