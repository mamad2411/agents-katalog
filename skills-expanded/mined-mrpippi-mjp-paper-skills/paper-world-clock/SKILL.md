---
name: paper-world-clock
description: "Paper 26.3 世界時鐘 API：每個世界獨立暫停、調整時間流速（白天長度）、固定時間的大廳、以 ClockTimeSkipEvent 攔截 /time 與睡覺跳夜，並處理沒有時鐘的維度（地獄）；僅 26.3 / Paper 26.3 world clock API: pause or speed up time per world (day length), frozen-time lobbies, intercept /time and night skips with ClockTimeSkipEvent, and handle dimensions without a clock (the Nether); 26.3 only"
---

# Paper World Clock

## Skill Name

`paper-world-clock`

## Purpose

Minecraft 26.1 replaced the single "day time" with **world clocks** (`minecraft:overworld`, `minecraft:the_end`), and Paper 26.3 exposes them: a clock can be paused, run at a different rate, and set, per world. That covers requests which used to need a repeating task fighting the day cycle:

| Request | API |
|------|------|
| Lobby is always noon | `setFullTime(clock, 6000)` + `setClockPaused(clock, true)` |
| A day lasts 40 minutes instead of 20 | `setClockRate(clock, 0.5f)` |
| Nobody may change time in the arena world | cancel `ClockTimeSkipEvent` |
| Sleeping skips the night only in the survival world | allow `NIGHT_SKIP` there, cancel it elsewhere |

Observed on Paper 26.3 build 258 with the default configuration (runtime test):

| Fact | Detail |
|------|------|
| Clock registry | `minecraft:overworld`, `minecraft:the_end` |
| Default clock per world | overworld-type worlds (including plugin-created ones) → `minecraft:overworld`; the Nether → **`null`** |
| Shared type, separate state | Two overworld-type worlds return the same `WorldClock`, but pause, rate and time are **per world**: pausing `world` did not pause a second world |
| Rate | rate 4.0 advanced the clock 160 ticks in 40 server ticks; paused advanced 0 |
| Events | `/time add`, `World#setTime` and `World#setFullTime(clock, ...)` each fire one `TimeSkipEvent`, which in 26.3 **extends** `ClockTimeSkipEvent` and adds `getWorld()`; the amount can be negative; cancelling it leaves the time unchanged |
| Legacy API | `World#setTime` / `getTime` still work and act on the world's default clock |

## Paper Version Requirements

- **Paper 26.3 only.** `io.papermc.paper.world.WorldClock`, `WorldClocks`, the clock methods on `World` and `ClockTimeSkipEvent` do not exist in the 1.21.11 API; every template is marked `// @only 26.3`
- On 1.21.11 the closest equivalent is the `advance_time` game rule plus `World#setTime` and a repeating task for custom day lengths
- **Spigot**: Paper only — Spigot-API 26.3 has no clock types

## Triggers

- 「世界時鐘」「world clock」「WorldClock」「時間流速」「白天長度」「day length」
- 「暫停時間」「固定時間」「永遠白天」「freeze time」「setClockRate」「setClockPaused」
- 「ClockTimeSkipEvent」「阻止 /time」「跳夜」「night skip」

## Inputs

| Parameter | Example | Description |
|------|------|------|
| `frozen_worlds` | `lobby` at `6000` | Worlds whose time never moves |
| `day_length` | `survival`: 40 min | Real-time length of a full day (vanilla 20 min) |
| `locked_worlds` | `arena` | Worlds where `/time` and sleeping cannot change time |

## Outputs

- `WorldTime.java` — freeze, unfreeze and day-length helpers that tolerate worlds without a clock
- `TimeLock.java` — listener that blocks time changes in locked worlds and allows night skips where wanted
- `ClockPlugin.java` — applies the settings when worlds load

## Build Setup

See [`references/paper-api-platform.md`](references/paper-api-platform.md). Only `paper-api` (`compileOnly`) for **26.3**; set `api-version: '26.3'`.

## Code Template

### `WorldTime.java`

```java
// @only 26.3
package com.example.clock;

import io.papermc.paper.world.WorldClock;
import org.bukkit.World;

import java.time.Duration;

/**
 * Per-world clock control. Pause, rate and time are stored per world even though overworld-type worlds share the
 * same {@link WorldClock} key. Main thread only.
 */
public final class WorldTime {

    /** Vanilla day: 24000 clock ticks at 20 ticks per second. */
    private static final Duration VANILLA_DAY = Duration.ofMinutes(20);

    private WorldTime() {
    }

    /** Sets the time and stops the clock. Returns false for worlds without a clock (the Nether). */
    public static boolean freeze(World world, long time) {
        WorldClock clock = world.getDefaultClock();
        if (clock == null) {
            return false;
        }
        world.setFullTime(clock, time);
        world.setClockPaused(clock, true);
        return true;
    }

    public static boolean unfreeze(World world) {
        WorldClock clock = world.getDefaultClock();
        if (clock == null) {
            return false;
        }
        world.setClockPaused(clock, false);
        return true;
    }

    /** dayLength 40 min -> rate 0.5; 10 min -> rate 2.0. */
    public static boolean setDayLength(World world, Duration dayLength) {
        WorldClock clock = world.getDefaultClock();
        if (clock == null || dayLength.isZero() || dayLength.isNegative()) {
            return false;
        }
        float rate = (float) VANILLA_DAY.toMillis() / dayLength.toMillis();
        world.setClockRate(clock, rate);
        return true;
    }

    /** Time of day 0..23999 of the world's default clock, or -1 when it has none. */
    public static long timeOfDay(World world) {
        WorldClock clock = world.getDefaultClock();
        return clock == null ? -1 : Math.floorMod(world.getFullTime(clock), 24000L);
    }
}
```

### `TimeLock.java`

```java
// @only 26.3
package com.example.clock;

import org.bukkit.World;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.world.ClockTimeSkipEvent;
import org.bukkit.event.world.TimeSkipEvent;

import java.util.Set;

/**
 * Blocks time changes in locked worlds. In 26.3 {@link TimeSkipEvent} extends {@link ClockTimeSkipEvent} and carries the
 * world; listening to it covers /time, World#setTime and night skips. Cancelling keeps the time.
 */
public final class TimeLock implements Listener {

    private final Set<String> lockedWorlds;
    private final Set<String> nightSkipAllowed;

    public TimeLock(Set<String> lockedWorlds, Set<String> nightSkipAllowed) {
        this.lockedWorlds = Set.copyOf(lockedWorlds);
        this.nightSkipAllowed = Set.copyOf(nightSkipAllowed);
    }

    @EventHandler(ignoreCancelled = true)
    public void onTimeSkip(TimeSkipEvent event) {
        World world = event.getWorld();
        if (!lockedWorlds.contains(world.getName())) {
            return;
        }
        boolean nightSkip = event.getSkipReason() == ClockTimeSkipEvent.SkipReason.NIGHT_SKIP;
        if (!nightSkip || !nightSkipAllowed.contains(world.getName())) {
            event.setCancelled(true);
        }
    }
}
```

### `ClockPlugin.java`

```java
// @only 26.3
package com.example.clock;

import org.bukkit.World;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.world.WorldLoadEvent;
import org.bukkit.plugin.java.JavaPlugin;

import java.time.Duration;
import java.util.Set;

public final class ClockPlugin extends JavaPlugin implements Listener {

    @Override
    public void onEnable() {
        getServer().getPluginManager().registerEvents(new TimeLock(Set.of("lobby", "arena"), Set.of()), this);
        getServer().getPluginManager().registerEvents(this, this);
        getServer().getWorlds().forEach(this::apply);              // worlds loaded before this plugin
    }

    @EventHandler
    public void onWorldLoad(WorldLoadEvent event) {
        apply(event.getWorld());                                    // worlds loaded later (multiverse, arenas)
    }

    private void apply(World world) {
        switch (world.getName()) {
            case "lobby" -> logIfMissing(world, WorldTime.freeze(world, 6000L));            // always noon
            case "world" -> logIfMissing(world, WorldTime.setDayLength(world, Duration.ofMinutes(40)));
            default -> { }
        }
    }

    private void logIfMissing(World world, boolean applied) {
        if (!applied) {
            getLogger().warning("World " + world.getName() + " has no clock; time settings skipped");
        }
    }
}
```

## Recommended Directory Structure

```
src/main/java/com/example/clock/
├── WorldTime.java    <- freeze / unfreeze / day length
├── TimeLock.java     <- block /time and night skip per world
└── ClockPlugin.java  <- apply on enable and on WorldLoadEvent
```

## Thread Safety

- All clock methods and events are main-thread only
- Pause, rate and time are saved with the world (a restart kept rate 0.5 and a paused arena at 6000 in the runtime test); re-applying settings on every load is idempotent and also undoes manual changes
- See [`references/paper-threading.md`](references/paper-threading.md)

### Key Techniques

| Topic | Approach |
|------|------|
| Which clock | `world.getDefaultClock()`; never assume `WorldClocks.OVERWORLD` for every world, and handle `null` |
| Freeze | Set the time first, then pause; a paused clock does not advance even with a rate set (verified) |
| Day length | `rate = 20 min / desired length`; affects the day/night cycle and everything driven by the clock |
| Per world | Pause / rate / time are per world (observed on 26.3 build 258); apply them to each world explicitly |
| Blocking changes | Listen to `TimeSkipEvent` (26.3: a `ClockTimeSkipEvent` subclass with `getWorld()`) and cancel it; `SkipReason.NIGHT_SKIP` is sleeping |
| Old code | `World#setTime` still works on 26.3 and maps to the default clock, but cannot pause or change the rate |

## Fallback

| Error | Cause | Fix |
|------|------|------|
| `NullPointerException` in the Nether | `getDefaultClock()` returns `null` there | Check for `null` (the helpers return false) |
| Settings lost after a world is unloaded and loaded again by another plugin | Applied only in `onEnable` | Also apply in `WorldLoadEvent` |
| `/time set` still works in a locked world | Listener not registered, or it filtered by the wrong world name | Register `TimeLock`; compare `event.getWorld().getName()` |
| Sleeping no longer skips the night anywhere | All `NIGHT_SKIP` events cancelled | Allow `NIGHT_SKIP` for worlds in `nightSkipAllowed` |
| `NoClassDefFoundError: io/papermc/paper/world/WorldClock` | Running on 1.21.11 | This skill is 26.3 only; use the `advance_time` game rule there |
