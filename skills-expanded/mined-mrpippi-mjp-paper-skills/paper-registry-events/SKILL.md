---
name: paper-registry-events
description: "Paper 註冊表事件：在 PluginBootstrap 以 RegistryEvents 新增自訂附魔與傷害類型、用 entryAdd 修改原版項目、用 LifecycleEvents.TAGS 加入標籤，並在執行期以 RegistryAccess 取回 / Paper registry events: add custom enchantments and damage types from a PluginBootstrap with RegistryEvents, modify vanilla entries with entryAdd, extend tags with LifecycleEvents.TAGS, and look them up at runtime with RegistryAccess"
---

# Paper Registry Events

## Skill Name

`paper-registry-events`

## Purpose

Since 1.20.5 most game content is data-driven: enchantments, damage types, mob variants, jukebox songs, dialogs and more live in **registries** that are frozen once the server finishes loading. Paper lets a plugin add to and modify these registries **before** they freeze, from a `PluginBootstrap`, with no data pack:

| Goal | API | When it runs |
|------|-----|------|
| Add a new entry (custom enchantment, damage type...) | `RegistryEvents.X.compose()` → `event.registry().register(key, builder -> ...)` | once, while the registry is built |
| Change a vanilla or other plugin's entry | `RegistryEvents.X.entryAdd()` + `.filter(key)` → `event.builder()` | once per matching entry |
| Put entries into tags (enchanting table, armor bypass...) | `LifecycleEvents.TAGS.postFlatten(RegistryKey.X)` → `event.registrar().addToTag(...)` | at startup **and on every `/minecraft:reload`** |
| Use the entry at runtime | `RegistryAccess.registryAccess().getRegistry(RegistryKey.X).get(key)` | from `onEnable` on |

The template registers a **Lifesteal** enchantment and a **Bleed** damage type, raises Sharpness to level 6, puts Lifesteal on the enchanting table and librarian trades, lets Bleed bypass armor, and implements the enchantment's behavior with a listener (the API defines what an enchantment *is*, not what it *does*).

## Paper Version Requirements

- Paper 1.21.11 / 26.3 (the builders and events used here have identical signatures on both; both are compile-verified)
- Pure Paper API, no Paperweight needed; requires `paper-plugin.yml` with a `bootstrapper`
- Registries available through `RegistryEvents` (checked against both `paper-api` jars):

| Registry | 1.21.11 | 26.3 |
|------|------|------|
| `ENCHANTMENT`, `DAMAGE_TYPE`, `GAME_EVENT`, `JUKEBOX_SONG`, `BANNER_PATTERN`, `PAINTING_VARIANT`, `INSTRUMENT`, `DIALOG` | ✅ | ✅ |
| `WOLF_VARIANT`, `CAT_VARIANT`, `FROG_VARIANT`, `CHICKEN_VARIANT`, `COW_VARIANT`, `PIG_VARIANT`, `ZOMBIE_NAUTILUS_VARIANT` | ✅ | ✅ |
| `TRIM_MATERIAL`, `TRIM_PATTERN` (Paper 26.2+), `DECORATED_POT_PATTERN`, `SULFUR_CUBE_ARCHETYPE`, `WORLD_CLOCK`, `TIMELINE` | ❌ | ✅ |

- **Spigot**: Paper only — `RegistryEvents`, `PluginBootstrap` and `LifecycleEvents` are Paper API; Spigot can only add content through a data pack

## Triggers

- 「自訂附魔」「custom enchantment」「新增附魔」「EnchantmentRegistryEntry」
- 「自訂傷害類型」「custom damage type」「DamageTypeRegistryEntry」「DamageSource.builder」
- 「RegistryEvents」「registry modification」「修改原版附魔」「entryAdd」「compose」
- 「附魔台」「addToTag」「LifecycleEvents.TAGS」「postFlatten」「RegistryAccess」

## Inputs

| Parameter | Example | Description |
|------|------|------|
| `namespace` | `example` | Namespace of every key the plugin adds (use the plugin name, lowercase) |
| `enchantments` | `lifesteal` (melee weapons, max III) | Custom enchantments with supported items, levels, costs and slots |
| `damage_types` | `bleed` (bypasses armor) | Custom damage types and the tags they join |
| `vanilla_changes` | Sharpness max level 6 | Existing entries to modify with `entryAdd` |

## Outputs

- `ContentKeys.java` — every `TypedKey` the plugin adds, in one place
- `ContentBootstrap.java` — registers enchantments, damage types, vanilla changes and tags during bootstrap; never throws
- `ContentPlugin.java` — main class returned by `createPlugin`; looks the entries up and reports bootstrap problems
- `LifestealListener.java` — the enchantment's behavior and the Bleed follow-up damage
- `paper-plugin.yml` — declares `bootstrapper`

## Build Setup

See [`references/paper-api-platform.md`](references/paper-api-platform.md). Only `paper-api` (`compileOnly`) is required. The plugin must use `paper-plugin.yml`, because only Paper plugins have a bootstrapper:

```yaml
name: CustomContent
version: '${version}'
main: com.example.content.ContentPlugin
bootstrapper: com.example.content.ContentBootstrap
api-version: '26.3'   # 1.21.11 server: '1.21.11'
```

## Code Template

### `ContentKeys.java`

```java
package com.example.content;

import io.papermc.paper.registry.TypedKey;
import io.papermc.paper.registry.keys.DamageTypeKeys;
import io.papermc.paper.registry.keys.EnchantmentKeys;
import net.kyori.adventure.key.Key;
import org.bukkit.damage.DamageType;
import org.bukkit.enchantments.Enchantment;

/**
 * Keys of everything this plugin adds. Keys are permanent: items and worlds store them, so never rename one
 * after release (add a new key instead).
 */
public final class ContentKeys {

    public static final String NAMESPACE = "example";

    public static final TypedKey<Enchantment> LIFESTEAL = EnchantmentKeys.create(Key.key(NAMESPACE, "lifesteal"));
    public static final TypedKey<DamageType> BLEED = DamageTypeKeys.create(Key.key(NAMESPACE, "bleed"));

    private ContentKeys() {
    }
}
```

### `ContentBootstrap.java`

```java
package com.example.content;

import io.papermc.paper.plugin.bootstrap.BootstrapContext;
import io.papermc.paper.plugin.bootstrap.PluginBootstrap;
import io.papermc.paper.plugin.bootstrap.PluginProviderContext;
import io.papermc.paper.plugin.lifecycle.event.LifecycleEventManager;
import io.papermc.paper.plugin.lifecycle.event.types.LifecycleEvents;
import io.papermc.paper.registry.RegistryKey;
import io.papermc.paper.registry.data.EnchantmentRegistryEntry;
import io.papermc.paper.registry.event.RegistryComposeEvent;
import io.papermc.paper.registry.event.RegistryEvents;
import io.papermc.paper.registry.keys.EnchantmentKeys;
import io.papermc.paper.registry.keys.tags.DamageTypeTagKeys;
import io.papermc.paper.registry.keys.tags.EnchantmentTagKeys;
import io.papermc.paper.registry.keys.tags.ItemTypeTagKeys;
import io.papermc.paper.registry.set.RegistrySet;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.logger.slf4j.ComponentLogger;
import org.bukkit.damage.DamageEffect;
import org.bukkit.damage.DamageScaling;
import org.bukkit.damage.DeathMessageType;
import org.bukkit.enchantments.Enchantment;
import org.bukkit.inventory.EquipmentSlotGroup;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.List;
import java.util.Set;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * Adds and changes registry content before the registries freeze.
 *
 * <p>Rules:
 * <ul>
 *   <li><b>Never throw</b>: an exception here stops Paper from loading the plugin at all. Every handler catches,
 *       logs and records the problem; {@link ContentPlugin} reports it once the server is up</li>
 *   <li>Registry handlers run once. Tag handlers run again on every {@code /minecraft:reload}, so they must be idempotent
 *       ({@code addToTag} is)</li>
 *   <li>There is no Bukkit server yet: only registry and tag work belongs here</li>
 * </ul>
 */
public final class ContentBootstrap implements PluginBootstrap {

    private final List<String> problems = new CopyOnWriteArrayList<>();

    @Override
    public void bootstrap(BootstrapContext context) {
        ComponentLogger log = context.getLogger();
        LifecycleEventManager<BootstrapContext> lifecycle = context.getLifecycleManager();
        try {
            lifecycle.registerEventHandler(RegistryEvents.ENCHANTMENT.compose().newHandler(
                    event -> guarded(log, "enchantments", () -> registerEnchantments(event))));

            lifecycle.registerEventHandler(RegistryEvents.DAMAGE_TYPE.compose().newHandler(
                    event -> guarded(log, "damage types", () -> event.registry().register(ContentKeys.BLEED, b -> b
                            .messageId("example.bleed")               // death message key: death.attack.example.bleed
                            .exhaustion(0.0f)
                            .damageScaling(DamageScaling.NEVER)
                            .damageEffect(DamageEffect.HURT)
                            .deathMessageType(DeathMessageType.DEFAULT)))));

            // Modify a vanilla entry: the filter keeps the handler from touching every enchantment
            lifecycle.registerEventHandler(RegistryEvents.ENCHANTMENT.entryAdd()
                    .newHandler(event -> guarded(log, "sharpness change", () -> event.builder().maxLevel(6)))
                    .filter(EnchantmentKeys.SHARPNESS));

            lifecycle.registerEventHandler(LifecycleEvents.TAGS.postFlatten(RegistryKey.ENCHANTMENT),
                    event -> guarded(log, "enchantment tags", () -> {
                        Set<io.papermc.paper.registry.TypedKey<Enchantment>> lifesteal = Set.of(ContentKeys.LIFESTEAL);
                        event.registrar().addToTag(EnchantmentTagKeys.IN_ENCHANTING_TABLE, lifesteal);
                        event.registrar().addToTag(EnchantmentTagKeys.NON_TREASURE, lifesteal);
                        event.registrar().addToTag(EnchantmentTagKeys.TRADEABLE, lifesteal);
                    }));

            lifecycle.registerEventHandler(LifecycleEvents.TAGS.postFlatten(RegistryKey.DAMAGE_TYPE),
                    event -> guarded(log, "damage type tags",
                            () -> event.registrar().addToTag(DamageTypeTagKeys.BYPASSES_ARMOR, Set.of(ContentKeys.BLEED))));
        } catch (RuntimeException e) {
            log.error("Failed to register bootstrap handlers", e);
            problems.add("bootstrap: " + e.getMessage());
        }
    }

    @Override
    public JavaPlugin createPlugin(PluginProviderContext context) {
        return new ContentPlugin(List.copyOf(problems));
    }

    private void registerEnchantments(RegistryComposeEvent<Enchantment, EnchantmentRegistryEntry.Builder> event) {
        event.registry().register(ContentKeys.LIFESTEAL, b -> b
                .description(Component.text("Lifesteal"))           // shown in the tooltip; clients need no resource pack
                .supportedItems(event.getOrCreateTag(ItemTypeTagKeys.ENCHANTABLE_MELEE_WEAPON))  // anvil / commands
                .primaryItems(event.getOrCreateTag(ItemTypeTagKeys.ENCHANTABLE_SHARP_WEAPON))    // enchanting table
                .weight(2)                                           // rarity: 1 (very rare) .. 1024
                .maxLevel(3)
                .minimumCost(EnchantmentRegistryEntry.EnchantmentCost.of(15, 9))
                .maximumCost(EnchantmentRegistryEntry.EnchantmentCost.of(65, 9))
                .anvilCost(4)
                .activeSlots(EquipmentSlotGroup.MAINHAND)
                .exclusiveWith(RegistrySet.keySet(RegistryKey.ENCHANTMENT, EnchantmentKeys.SMITE)));
    }

    private void guarded(ComponentLogger log, String what, Runnable action) {
        try {
            action.run();
        } catch (RuntimeException e) {
            log.error("Failed to register {}", what, e);
            problems.add(what + ": " + e.getMessage());
        }
    }
}
```

### `ContentPlugin.java`

```java
package com.example.content;

import io.papermc.paper.registry.RegistryAccess;
import io.papermc.paper.registry.RegistryKey;
import org.bukkit.damage.DamageType;
import org.bukkit.enchantments.Enchantment;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.List;

public final class ContentPlugin extends JavaPlugin {

    private final List<String> bootstrapProblems;

    /** Receives the problems collected in {@link ContentBootstrap}, which could not log through Bukkit yet. */
    ContentPlugin(List<String> bootstrapProblems) {
        this.bootstrapProblems = List.copyOf(bootstrapProblems);
    }

    @Override
    public void onEnable() {
        for (String problem : bootstrapProblems) {
            getLogger().warning("Custom content not fully registered: " + problem);
        }
        RegistryAccess registries = RegistryAccess.registryAccess();
        Enchantment lifesteal = registries.getRegistry(RegistryKey.ENCHANTMENT).get(ContentKeys.LIFESTEAL);
        DamageType bleed = registries.getRegistry(RegistryKey.DAMAGE_TYPE).get(ContentKeys.BLEED);
        if (lifesteal == null || bleed == null) {
            getLogger().warning("Lifesteal/Bleed missing from the registries; the enchantment effect stays off");
            return;                                   // disable only this feature
        }
        getServer().getPluginManager().registerEvents(new LifestealListener(this, lifesteal, bleed), this);
    }
}
```

### `LifestealListener.java`

```java
package com.example.content;

import org.bukkit.Bukkit;
import org.bukkit.attribute.Attribute;
import org.bukkit.attribute.AttributeInstance;
import org.bukkit.damage.DamageSource;
import org.bukkit.damage.DamageType;
import org.bukkit.enchantments.Enchantment;
import org.bukkit.entity.Entity;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityDamageByEntityEvent;
import org.bukkit.plugin.Plugin;

import java.util.UUID;

/**
 * What Lifesteal does: heal the attacker for part of the damage, then apply one Bleed tick a second later.
 * Registry entries only describe the enchantment; behavior is plain event code.
 */
public final class LifestealListener implements Listener {

    private static final double HEAL_PER_LEVEL = 0.10;
    private static final long BLEED_DELAY_TICKS = 20L;

    private final Plugin plugin;
    private final Enchantment lifesteal;
    private final DamageType bleed;

    public LifestealListener(Plugin plugin, Enchantment lifesteal, DamageType bleed) {
        this.plugin = plugin;
        this.lifesteal = lifesteal;
        this.bleed = bleed;
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onHit(EntityDamageByEntityEvent event) {
        if (event.getDamageSource().getDamageType() == bleed) {
            return;                                   // our own follow-up damage: no recursion
        }
        if (!(event.getDamager() instanceof Player attacker) || !(event.getEntity() instanceof LivingEntity target)) {
            return;
        }
        int level = attacker.getInventory().getItemInMainHand().getEnchantmentLevel(lifesteal);
        if (level <= 0) {
            return;
        }
        heal(attacker, event.getFinalDamage() * HEAL_PER_LEVEL * level);
        scheduleBleed(target.getUniqueId(), attacker.getUniqueId(), level);
    }

    private static void heal(Player player, double amount) {
        AttributeInstance max = player.getAttribute(Attribute.MAX_HEALTH);
        double cap = max == null ? 20.0 : max.getValue();
        player.setHealth(Math.min(cap, player.getHealth() + amount));
    }

    /** Carries only UUIDs into the task and looks the entities up again: either may be gone a second later. */
    private void scheduleBleed(UUID targetId, UUID attackerId, int level) {
        plugin.getServer().getScheduler().runTaskLater(plugin, () -> {
            Entity entity = Bukkit.getEntity(targetId);
            if (!(entity instanceof LivingEntity target) || target.isDead()) {
                return;
            }
            DamageSource.Builder source = DamageSource.builder(bleed);
            Player attacker = Bukkit.getPlayer(attackerId);
            if (attacker != null) {
                source.withCausingEntity(attacker).withDirectEntity(attacker);   // kill credit and death message
            }
            target.damage(level, source.build());
        }, BLEED_DELAY_TICKS);
    }
}
```

## Recommended Directory Structure

```
src/main/java/com/example/content/
├── ContentKeys.java          <- all TypedKeys
├── ContentBootstrap.java     <- registry + tag handlers (bootstrap phase)
├── ContentPlugin.java        <- looks entries up, reports bootstrap problems
└── LifestealListener.java    <- behavior
src/main/resources/
├── paper-plugin.yml          <- bootstrapper field
└── (optional) a server resource pack with lang entries for death.attack.example.bleed
```

## Thread Safety

- Bootstrap handlers run on the server's startup thread before the Bukkit server exists: do not touch `Bukkit`, worlds, players or schedulers there
- Tag handlers run again on the main thread during `/minecraft:reload`; keep them pure (no IO, no state besides the registrar)
- Runtime lookups (`RegistryAccess`, `Registry#get`) and `LivingEntity#damage` are main-thread only; the delayed Bleed task carries only UUIDs and re-fetches entities
- See [`references/paper-threading.md`](references/paper-threading.md)

### Key Techniques

| Topic | Approach |
|------|------|
| New entry vs. change | `compose()` adds entries; `entryAdd()` + `filter(key)` changes an existing one. `entryAdd` without a filter runs for every entry in the registry |
| Supported vs. primary items | `supportedItems` = where the enchantment may exist (anvil, `/enchant`); `primaryItems` = where the enchanting table offers it. Both take tags from `event.getOrCreateTag(...)` |
| Enchanting table / villagers / loot | Membership in `#in_enchanting_table`, `#tradeable`, `#non_treasure` / `#treasure`, `#on_random_loot`; add with `LifecycleEvents.TAGS.postFlatten(RegistryKey.ENCHANTMENT)` |
| Damage type behavior | Armor, shields, knockback, fire immunity are tags (`DamageTypeTagKeys.BYPASSES_ARMOR`, `NO_KNOCKBACK`...); scaling and death message come from the builder |
| Custom death message | `messageId("example.bleed")` → the client looks up `death.attack.example.bleed`; without a resource pack entry the raw key is shown |
| Enchantment effects | The API sets description, items, levels, costs, slots and exclusivity; effects (damage bonus, attributes...) are not exposed, so implement them in listeners |
| Runtime lookup | `RegistryAccess.registryAccess().getRegistry(RegistryKey.X).get(typedKey)`; `getRegistry(Class)` is deprecated |
| Removing the plugin | Items and worlds keep the keys; an unregistered key cannot be resolved after the plugin is removed. Keep keys stable and keep the plugin installed while such items exist |

## Fallback

| Error | Cause | Fix |
|------|------|------|
| Plugin does not load, no `onEnable` | An exception escaped `bootstrap()` or a handler | Wrap every handler body like `guarded(...)`; report from `onEnable` |
| `bootstrapper` ignored / handlers never run | Declared in `plugin.yml`, or the plugin is not a Paper plugin | Use `paper-plugin.yml` with `bootstrapper:` |
| Lookup returns `null` in `onEnable` | The handler failed, or the key namespace/path differs from the registered one | Share keys through `ContentKeys`; check the bootstrap problems logged at enable |
| Enchantment exists (`/enchant` works) but never appears in the enchanting table | Not in `#in_enchanting_table`, or the item is not in `primaryItems` | Add the tag in `postFlatten`; check `primaryItems` |
| Tag change gone after `/minecraft:reload` | Tags were changed outside the `TAGS` lifecycle event | Only change tags in `LifecycleEvents.TAGS`; it re-runs on every reload |
| Death message shows `death.attack.example.bleed` | Client has no translation for the custom `messageId` | Ship it in a server resource pack, or reuse a vanilla `messageId` |
| Infinite damage loop | The listener reacts to its own follow-up damage | Skip events whose `getDamageSource().getDamageType()` is your type |
| `NoSuchFieldError: TRIM_MATERIAL` (or `WORLD_CLOCK`, `TIMELINE`...) on 1.21.11 | Those registry events only exist on newer Paper | Check the version table above; guard version-specific registrations |
