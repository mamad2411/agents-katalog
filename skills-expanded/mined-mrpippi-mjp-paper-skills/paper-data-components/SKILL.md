---
name: paper-data-components
description: "Paper Data Component API：不用 NMS 讀寫物品元件（食物、可食用效果、武器屬性、滑翔、裝備、提示框、冷卻），分清 set／unset／reset 與原型預設值，用 PDC 標記自訂物品並以 matchesWithoutData 比對 / Paper data component API: build and read item components without NMS (food, consumable effects, weapon attributes, glider, equippable, tooltip, cooldown), set vs unset vs reset against the prototype, PDC item ids and matchesWithoutData comparisons"
---

# Paper Data Components

## Skill Name

`paper-data-components`

## Purpose

Since 1.20.5 an item is a material plus a map of **data components** (`minecraft:food`, `minecraft:max_stack_size`, `minecraft:tooltip_display`...). Paper exposes them directly through `io.papermc.paper.datacomponent.DataComponentTypes` and `ItemStack#setData` / `getData`, so custom items no longer need `ItemMeta` gymnastics or NMS:

| You want | Component |
|------|------|
| Edible item with effects | `FOOD` + `CONSUMABLE` (`ConsumeEffect.applyStatusEffects`) |
| Weapon stats | `ATTRIBUTE_MODIFIERS` + `WEAPON` (+ `MAX_DAMAGE`) |
| Elytra-like gliding on any chest item | `GLIDER` (no value) + `EQUIPPABLE` |
| Stack size, cooldown, glint | `MAX_STACK_SIZE`, `USE_COOLDOWN`, `ENCHANTMENT_GLINT_OVERRIDE` |
| Clean GUI icons | `TOOLTIP_DISPLAY` (hide parts or the whole tooltip) |
| Custom model | `ITEM_MODEL` (1.21.4+ item model id) or `CUSTOM_MODEL_DATA` |

Every component has a **prototype** value that comes from the item type (an apple's `FOOD`). The three write operations differ:

| Call | Effect | `hasData` | `isDataOverridden` |
|------|------|------|------|
| `setData(type, value)` | override the prototype | true | true |
| `unsetData(type)` | remove it, even if the prototype has it (an apple that cannot be eaten) | false | true |
| `resetData(type)` | drop the override, back to the prototype | prototype | false |

## Paper Version Requirements

- Paper 1.21.11 / 26.3 (every method and builder used here has the same signature on both; both are compile-verified)
- On 1.21.11 the data component API is marked `@ApiStatus.Experimental`; Paper 26.3 removed that marker
- Components exposed by `DataComponentTypes` differ between the versions (compared from both `paper-api` jars):

| Change 1.21.11 → 26.3 | Components |
|------|------|
| Added | `ATTACK_ANIMATION`, `INTERACT_ANIMATION`, `MOB_VISIBILITY`, `VILLAGER_FOOD`, `SULFUR_CUBE_CONTENT`, `CUSHION_COLOR`, `DYE`, `SIGN_TEXT_FRONT`, `SIGN_TEXT_BACK`, `WAXED`, `PROVIDES_POTTERY_PATTERN`, `CAT_SOUND_VARIANT`, `CHICKEN_SOUND_VARIANT`, `COW_SOUND_VARIANT`, `PIG_SOUND_VARIANT` |
| Removed | `SWING_ANIMATION`, `MAP_COLOR` |
| Not exposed by Paper 26.3 (use `nms-data-component`) | `brewing_fuel`, `cooking_fuel`, `compostable`, `block_transformer` |

- `ConsumeEffect.teleportRandomlyEffect(float, boolean)` exists only on 26.3 (1.21.11 has the one-argument form)
- **Spigot**: Paper only — `io.papermc.paper.datacomponent` does not exist in Spigot-API 26.3 (Spigot's `org.bukkit.inventory.meta.components` is a different, `ItemMeta`-based API)

## Triggers

- 「Data Component API」「資料元件」「DataComponentTypes」「setData」「getData」
- 「自訂食物」「custom food」「Consumable」「FoodProperties」「吃了給效果」
- 「自訂武器」「ItemAttributeModifiers」「Weapon component」「滑翔」「GLIDER」「Equippable」
- 「unsetData」「resetData」「isDataOverridden」「matchesWithoutData」「copyDataFrom」「隱藏提示框」

## Inputs

| Parameter | Example | Description |
|------|------|------|
| `package` | `com.example.items` | Output package |
| `items` | healing berry, war hammer, glider vest, menu icon | Which custom items to build |
| `id_key` | `example:item_id` | PDC key that identifies the plugin's items |
| `resource_pack` | `example:war_hammer` item model | Model ids, when the server ships a resource pack |

## Outputs

- `ItemIds.java` — PDC id stamping and lookup (the only reliable way to recognize "our" item)
- `CustomItems.java` — factories for each custom item, built only from components
- `ItemChecks.java` — comparisons and edits: ignore durability, copy cosmetics, repair, strip food

## Build Setup

See [`references/paper-api-platform.md`](references/paper-api-platform.md). Only `paper-api` (`compileOnly`) is required. On 1.21.11 the IDE flags the API as experimental; that is expected.

## Code Template

### `ItemIds.java`

```java
package com.example.items;

import org.bukkit.NamespacedKey;
import org.bukkit.inventory.ItemStack;
import org.bukkit.persistence.PersistentDataType;
import org.bukkit.plugin.Plugin;
import org.jspecify.annotations.Nullable;

/**
 * Identifies custom items by a PDC string. Names, lore and models are cosmetic and players can change them
 * (anvils, other plugins); never use them to recognize an item.
 */
public final class ItemIds {

    private final NamespacedKey key;

    public ItemIds(Plugin plugin) {
        this.key = new NamespacedKey(plugin, "item_id");
    }

    public ItemStack stamp(ItemStack item, String id) {
        item.editPersistentDataContainer(pdc -> pdc.set(key, PersistentDataType.STRING, id));
        return item;
    }

    public @Nullable String idOf(@Nullable ItemStack item) {
        if (item == null || item.isEmpty()) {
            return null;
        }
        return item.getPersistentDataContainer().get(key, PersistentDataType.STRING);
    }

    public boolean is(@Nullable ItemStack item, String id) {
        return id.equals(idOf(item));
    }
}
```

### `CustomItems.java`

```java
package com.example.items;

import io.papermc.paper.datacomponent.DataComponentType;
import io.papermc.paper.datacomponent.DataComponentTypes;
import io.papermc.paper.datacomponent.item.Consumable;
import io.papermc.paper.datacomponent.item.Equippable;
import io.papermc.paper.datacomponent.item.FoodProperties;
import io.papermc.paper.datacomponent.item.ItemAttributeModifiers;
import io.papermc.paper.datacomponent.item.ItemLore;
import io.papermc.paper.datacomponent.item.TooltipDisplay;
import io.papermc.paper.datacomponent.item.UseCooldown;
import io.papermc.paper.datacomponent.item.Weapon;
import io.papermc.paper.datacomponent.item.consumable.ConsumeEffect;
import io.papermc.paper.datacomponent.item.consumable.ItemUseAnimation;
import net.kyori.adventure.key.Key;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.NamedTextColor;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.attribute.Attribute;
import org.bukkit.attribute.AttributeModifier;
import org.bukkit.inventory.EquipmentSlot;
import org.bukkit.inventory.EquipmentSlotGroup;
import org.bukkit.inventory.ItemStack;
import org.bukkit.plugin.Plugin;
import org.bukkit.potion.PotionEffect;
import org.bukkit.potion.PotionEffectType;

import java.util.List;

/**
 * Custom items built from data components only. Each call returns a new stack (ItemStacks are mutable; never hand out
 * a shared instance). Build them on the main thread.
 */
public final class CustomItems {

    public static final String HEALING_BERRY = "healing_berry";
    public static final String WAR_HAMMER = "war_hammer";
    public static final String GLIDER_VEST = "glider_vest";

    private final Plugin plugin;
    private final ItemIds ids;

    public CustomItems(Plugin plugin, ItemIds ids) {
        this.plugin = plugin;
        this.ids = ids;
    }

    /** Edible any time, eaten fast, grants Regeneration II for 5 s, stacks to 16, 5 s shared cooldown. */
    public ItemStack healingBerry() {
        ItemStack item = ItemStack.of(Material.GLOW_BERRIES);
        item.setData(DataComponentTypes.ITEM_NAME, Component.text("Healing Berry", NamedTextColor.LIGHT_PURPLE));
        item.setData(DataComponentTypes.LORE, ItemLore.lore(List.of(Component.text("Restores health over time", NamedTextColor.GRAY))));
        item.setData(DataComponentTypes.FOOD, FoodProperties.food().nutrition(2).saturation(1.0f).canAlwaysEat(true));
        item.setData(DataComponentTypes.CONSUMABLE, Consumable.consumable()
                .consumeSeconds(0.8f)
                .animation(ItemUseAnimation.EAT)
                .addEffect(ConsumeEffect.applyStatusEffects(
                        List.of(new PotionEffect(PotionEffectType.REGENERATION, 100, 1)), 1.0f)));
        item.setData(DataComponentTypes.MAX_STACK_SIZE, 16);
        item.setData(DataComponentTypes.USE_COOLDOWN, UseCooldown.useCooldown(5.0f)
                .cooldownGroup(Key.key("example", "healing_berry")));
        return ids.stamp(item, HEALING_BERRY);
    }

    /** Slow, heavy weapon: +9 attack damage, slower swing, disables shields for 5 s, 500 durability. */
    public ItemStack warHammer() {
        ItemStack item = ItemStack.of(Material.IRON_AXE);
        item.setData(DataComponentTypes.ITEM_NAME, Component.text("War Hammer"));
        item.setData(DataComponentTypes.ATTRIBUTE_MODIFIERS, ItemAttributeModifiers.itemAttributes()
                .addModifier(Attribute.ATTACK_DAMAGE, new AttributeModifier(new NamespacedKey(plugin, "war_hammer_damage"),
                        9.0, AttributeModifier.Operation.ADD_NUMBER, EquipmentSlotGroup.MAINHAND))
                .addModifier(Attribute.ATTACK_SPEED, new AttributeModifier(new NamespacedKey(plugin, "war_hammer_speed"),
                        -3.2, AttributeModifier.Operation.ADD_NUMBER, EquipmentSlotGroup.MAINHAND)));
        item.setData(DataComponentTypes.WEAPON, Weapon.weapon().itemDamagePerAttack(2).disableBlockingForSeconds(5.0f));
        item.setData(DataComponentTypes.MAX_DAMAGE, 500);
        item.setData(DataComponentTypes.ITEM_MODEL, Key.key("example", "war_hammer"));   // needs a resource pack; falls back to a missing-model look without one
        return ids.stamp(item, WAR_HAMMER);
    }

    /** A chestplate-slot item that glides like an elytra, without being an elytra. */
    public ItemStack gliderVest() {
        ItemStack item = ItemStack.of(Material.LEATHER_CHESTPLATE);
        item.setData(DataComponentTypes.ITEM_NAME, Component.text("Glider Vest"));
        item.setData(DataComponentTypes.GLIDER);                                         // non-valued component: present or not
        item.setData(DataComponentTypes.EQUIPPABLE, Equippable.equippable(EquipmentSlot.CHEST).damageOnHurt(false));
        return ids.stamp(item, GLIDER_VEST);
    }

    /** GUI icon: no attribute/enchantment/etc. lines, optional glint. */
    public static ItemStack icon(Material material, Component name, List<Component> lore, boolean glint) {
        ItemStack item = ItemStack.of(material);
        item.setData(DataComponentTypes.ITEM_NAME, name);
        item.setData(DataComponentTypes.LORE, ItemLore.lore(lore));
        item.setData(DataComponentTypes.ENCHANTMENT_GLINT_OVERRIDE, glint);
        item.setData(DataComponentTypes.TOOLTIP_DISPLAY, TooltipDisplay.tooltipDisplay()
                .addHiddenComponents(ICON_HIDDEN)
                .build());
        return item;
    }

    private static final DataComponentType[] ICON_HIDDEN = {
            DataComponentTypes.ATTRIBUTE_MODIFIERS,
            DataComponentTypes.ENCHANTMENTS,
            DataComponentTypes.STORED_ENCHANTMENTS,
            DataComponentTypes.POTION_CONTENTS,
            DataComponentTypes.DYED_COLOR,
            DataComponentTypes.TRIM,
            DataComponentTypes.UNBREAKABLE,
    };
}
```

### `ItemChecks.java`

```java
package com.example.items;

import io.papermc.paper.datacomponent.DataComponentType;
import io.papermc.paper.datacomponent.DataComponentTypes;
import org.bukkit.inventory.ItemStack;

import java.util.Set;

/** Comparisons and in-place edits that are awkward with ItemMeta. All methods are main-thread only. */
public final class ItemChecks {

    /** Components that are "wear", not identity: a damaged sword is still the same sword. */
    private static final Set<DataComponentType> WEAR = Set.of(DataComponentTypes.DAMAGE, DataComponentTypes.REPAIR_COST);

    /** Cosmetic components a re-skin may carry over. */
    private static final Set<DataComponentType> COSMETIC = Set.of(
            DataComponentTypes.CUSTOM_NAME, DataComponentTypes.LORE, DataComponentTypes.ITEM_MODEL,
            DataComponentTypes.CUSTOM_MODEL_DATA, DataComponentTypes.DYED_COLOR, DataComponentTypes.TRIM);

    private ItemChecks() {
    }

    /** Same item apart from durability, anvil cost and stack size. */
    public static boolean sameIgnoringWear(ItemStack a, ItemStack b) {
        return a.matchesWithoutData(b, WEAR, true);   // true = ignore the count; the two-argument form compares it
    }

    /** Copy name, lore, model and colors from {@code skin} onto {@code target}; stats stay untouched. */
    public static void copyCosmetics(ItemStack skin, ItemStack target) {
        target.copyDataFrom(skin, COSMETIC::contains);
    }

    /** Full repair: drop the damage override so the item goes back to its prototype (0 damage). */
    public static void repair(ItemStack item) {
        item.resetData(DataComponentTypes.DAMAGE);
    }

    /** Make any food inedible, including vanilla food whose FOOD comes from the prototype. */
    public static void makeInedible(ItemStack item) {
        item.unsetData(DataComponentTypes.FOOD);
        item.unsetData(DataComponentTypes.CONSUMABLE);
    }

    /** True when the plugin (or a player) changed the component away from the item type's default. */
    public static boolean isCustomized(ItemStack item, DataComponentType type) {
        return item.isDataOverridden(type);
    }
}
```

## Recommended Directory Structure

```
src/main/java/com/example/items/
├── ItemIds.java        <- PDC id: recognize your items
├── CustomItems.java    <- item factories (components only)
└── ItemChecks.java     <- compare / copy / repair / strip
```

## Thread Safety

- `ItemStack` is mutable and not thread-safe: build and edit stacks on the main thread, and never share one instance between inventories (factories return a new stack every call)
- Reading components of a stack that sits in a live inventory from another thread is a data race; copy it on the main thread (`clone()`) before handing it to async code
- See [`references/paper-threading.md`](references/paper-threading.md)

### Key Techniques

| Topic | Approach |
|------|------|
| `ITEM_NAME` vs `CUSTOM_NAME` | `ITEM_NAME` is the item's own name (not italic, cannot be renamed away by anvils, but anvils add a `CUSTOM_NAME` on top); `CUSTOM_NAME` is what an anvil sets. Use `ITEM_NAME` for custom items |
| Builders | `setData(type, builder)` accepts the builder directly (no `.build()` needed); the template still builds `TooltipDisplay` explicitly to show both forms |
| Non-valued components | `GLIDER`, `UNBREAKABLE` and similar are `DataComponentType.NonValued`: `setData(type)` adds, `unsetData(type)` removes |
| Food needs two components | `FOOD` (hunger and saturation) and `CONSUMABLE` (eat time, animation, effects). Without `CONSUMABLE` the item is not eaten at all |
| ItemMeta and components together | They write the same data. Apply `editMeta` first and `setData` after, and never keep an `ItemMeta` across a `setData` call (`setItemMeta(oldMeta)` would overwrite the component) |
| Identity | Recognize custom items by a PDC id (`ItemIds`), never by name, lore or model |
| Comparing | `isSimilar` compares every component; `matchesWithoutData(other, ignored, ignoreCount)` skips the listed ones (durability, repair cost); the two-argument overload also compares stack size |

## Fallback

| Error | Cause | Fix |
|------|------|------|
| Custom food cannot be eaten | Only `FOOD` was set, or `CONSUMABLE` was unset | Set both `FOOD` and `CONSUMABLE` |
| Item name is italic | `CUSTOM_NAME` (or `displayName` in meta) was used | Use `ITEM_NAME` for the base name |
| `setData` changes vanish | An old `ItemMeta` instance was written back with `setItemMeta` after `setData` | Finish meta edits before `setData`; do not hold meta instances |
| `resetData` did not remove the food from an apple | `resetData` restores the prototype, and apples have `FOOD` by default | Use `unsetData` to remove a prototype component |
| Plugin items stop being recognized after an anvil rename | Identification used the name | Use the PDC id from `ItemIds` |
| Two identical-looking items do not stack | A hidden component differs (e.g. different `DAMAGE` or PDC) | Compare with `isSimilar`; build every copy from the same factory |
| `NoSuchFieldError: SWING_ANIMATION` / `MAP_COLOR` on 26.3 | Removed in 26.3 | Use `ATTACK_ANIMATION` / `INTERACT_ANIMATION`; check the version table |
| Need `cooking_fuel`, `brewing_fuel`, `compostable` | Paper does not expose them yet | Use `nms-data-component` for those only |
