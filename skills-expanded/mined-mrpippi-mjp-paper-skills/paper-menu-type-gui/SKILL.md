---
name: paper-menu-type-gui
description: "Paper MenuType 原版介面：不需要方塊就開啟可攜式工作台、鐵砧、切石機、鍛造台、砂輪、織布機、製圖台與自訂交易介面；鐵砧花費上限、方塊實體類介面的暫存陷阱、關閉時歸還物品 / Paper MenuType vanilla menus: open portable crafting tables, anvils, stonecutters, smithing tables, grindstones, looms, cartography tables and custom merchant screens without a block; anvil cost limits, the temporary block-entity trap, returning items on close"
---

# Paper MenuType GUI

## Skill Name

`paper-menu-type-gui`

## Purpose

`MenuType` opens the **real vanilla screen** for a workstation without a block: crafting, anvil, stonecutter, smithing, grindstone, loom, cartography table, merchant and more. Unlike a chest GUI (`paper-chest-gui`) the client runs its normal logic (recipe book, anvil renaming, stonecutter list), and unlike `nms-custom-menu` no NMS is needed.

```java
MenuType.ANVIL.builder().title(Component.text("Portable Anvil")).build(player);   // returns an AnvilView
player.openInventory(view);
```

What the view builder does (read from the Paper 26.3 implementation):

| Builder call | Effect |
|------|------|
| none besides `title` | The menu is bound to the player's own position; **the right choice for portable menus** |
| `location(loc)` | Binds the menu to the block at `loc` (a real anvil there takes damage, a real furnace keeps smelting) |
| `checkReachable(true)` | The menu closes when the player walks out of reach of that position; the default is `false` |

**Two kinds of menus behave differently without a block:**

| Kind | Menus | Without `location` |
|------|------|------|
| Block menus | `CRAFTING`, `ANVIL`, `STONECUTTER`, `SMITHING`, `GRINDSTONE`, `LOOM`, `CARTOGRAPHY_TABLE`, `ENCHANTMENT` | Work normally; vanilla gives the input items back when the screen closes |
| Block-entity menus | `FURNACE`, `SMOKER`, `BLAST_FURNACE`, `BREWING_STAND`, `HOPPER`, `SHULKER_BOX`, `CRAFTER_3X3`, `GENERIC_9X3`, `GENERIC_9X6`, `BEACON`, `LECTERN` | Paper creates a **temporary block entity that is not in the world**: it does not tick (a portable furnace never smelts) and nothing saves its contents |

For a storage GUI use an `Inventory` (`paper-chest-gui`); use block-entity menu types only with `location(...)` pointing at a real block.

## Paper Version Requirements

- Paper 1.21.11 / 26.3 (`MenuType`, the view builders, `AnvilView` and `Bukkit.createMerchant` have identical signatures on both; both compile-verified)
- **Spigot**: Core portable — `MenuType.Typed#builder`, `AnvilView#setMaximumRepairCost` and `Bukkit.createMerchant` exist in Spigot-API 26.3; replace the Adventure titles (`title(Component)`) with Spigot's String titles

## Triggers

- 「MenuType」「可攜式工作台」「portable crafting table」「隨身鐵砧」「portable anvil」
- 「打開原版介面」「open vanilla menu」「切石機介面」「鍛造台介面」「交易介面」「custom merchant」
- 「AnvilView」「setMaximumRepairCost」「Too Expensive」「PrepareAnvilEvent」

## Inputs

| Parameter | Example | Description |
|------|------|------|
| `package` | `com.example.workstations` | Output package |
| `menus` | crafting, anvil, stonecutter, merchant | Which screens to open |
| `anvil_max_cost` | `100` | Raise the vanilla 40-level limit for portable anvils |
| `trades` | 1 emerald → 4 bread | Offers of the custom merchant |

## Outputs

- `Workstations.java` — opens portable block menus with a title
- `PortableAnvil.java` — opens anvils, raises the cost limit for those anvils only, forgets them on close
- `TradeMenu.java` — a custom merchant screen with fixed trades

## Build Setup

See [`references/paper-api-platform.md`](references/paper-api-platform.md). Only `paper-api` (`compileOnly`) is required.

## Code Template

### `Workstations.java`

```java
package com.example.workstations;

import net.kyori.adventure.text.Component;
import org.bukkit.entity.Player;
import org.bukkit.inventory.InventoryView;
import org.bukkit.inventory.MenuType;

/**
 * Portable vanilla workstations. No {@code location(...)}: the menu follows the player, needs no block, and vanilla
 * returns the input items when the screen closes. Main thread only.
 */
public final class Workstations {

    private Workstations() {
    }

    public static void crafting(Player player) {
        open(player, MenuType.CRAFTING.builder().title(Component.text("Portable Crafting")).build(player));
    }

    public static void stonecutter(Player player) {
        open(player, MenuType.STONECUTTER.builder().title(Component.text("Stonecutter")).build(player));
    }

    public static void smithing(Player player) {
        open(player, MenuType.SMITHING.builder().title(Component.text("Smithing")).build(player));
    }

    public static void grindstone(Player player) {
        open(player, MenuType.GRINDSTONE.builder().title(Component.text("Grindstone")).build(player));
    }

    public static void loom(Player player) {
        open(player, MenuType.LOOM.builder().title(Component.text("Loom")).build(player));
    }

    public static void cartography(Player player) {
        open(player, MenuType.CARTOGRAPHY_TABLE.builder().title(Component.text("Cartography")).build(player));
    }

    private static void open(Player player, InventoryView view) {
        player.openInventory(view);
    }
}
```

### `PortableAnvil.java`

```java
package com.example.workstations;

import net.kyori.adventure.text.Component;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.InventoryCloseEvent;
import org.bukkit.event.inventory.PrepareAnvilEvent;
import org.bukkit.inventory.MenuType;
import org.bukkit.inventory.view.AnvilView;

import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

/**
 * Portable anvil whose "Too Expensive!" limit is raised, without changing real anvils.
 * Players with a portable anvil open are tracked by UUID and dropped on close, so a real anvil opened later keeps vanilla limits.
 */
public final class PortableAnvil implements Listener {

    private final int maxCost;
    private final Set<UUID> open = new HashSet<>();

    public PortableAnvil(int maxCost) {
        this.maxCost = maxCost;
    }

    public void open(Player player) {
        AnvilView view = MenuType.ANVIL.builder()
                .title(Component.text("Portable Anvil"))
                .build(player);
        view.setMaximumRepairCost(maxCost);
        player.openInventory(view);
        open.add(player.getUniqueId());          // after openInventory: opening closes the previous screen first
    }

    /** Runs on every input change; the cost limit must be re-applied because vanilla recomputes the view. */
    @EventHandler
    public void onPrepare(PrepareAnvilEvent event) {
        if (open.contains(event.getView().getPlayer().getUniqueId())) {
            event.getView().setMaximumRepairCost(maxCost);
        }
    }

    @EventHandler
    public void onClose(InventoryCloseEvent event) {
        if (event.getView() instanceof AnvilView) {
            open.remove(event.getPlayer().getUniqueId());
        }
    }

}
```

### `TradeMenu.java`

```java
package com.example.workstations;

import net.kyori.adventure.text.Component;
import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.MenuType;
import org.bukkit.inventory.Merchant;
import org.bukkit.inventory.MerchantRecipe;

import java.util.List;

/** A villager-style trade screen with fixed offers and no villager. */
public final class TradeMenu {

    private TradeMenu() {
    }

    public static void open(Player player) {
        Merchant merchant = Bukkit.createMerchant();
        merchant.setRecipes(List.of(
                offer(new ItemStack(Material.EMERALD), new ItemStack(Material.BREAD, 4)),
                offer(new ItemStack(Material.EMERALD, 3), new ItemStack(Material.ARROW, 16))));
        player.openInventory(MenuType.MERCHANT.builder()
                .merchant(merchant)
                .title(Component.text("Wandering Baker"))
                .build(player));
    }

    /** maxUses = Integer.MAX_VALUE: the offer never locks; no villager XP. */
    private static MerchantRecipe offer(ItemStack cost, ItemStack result) {
        MerchantRecipe recipe = new MerchantRecipe(result, 0, Integer.MAX_VALUE, false);
        recipe.addIngredient(cost);
        return recipe;
    }
}
```

## Recommended Directory Structure

```
src/main/java/com/example/workstations/
├── Workstations.java   <- portable block menus
├── PortableAnvil.java  <- anvil + cost limit (Listener)
└── TradeMenu.java      <- custom merchant
```

## Thread Safety

- `build(player)` and `openInventory` are main-thread only; open from a command executor or a scheduled task, never from an async callback
- `PortableAnvil` only touches its UUID set on the main thread (open, prepare and close all run there)
- See [`references/paper-threading.md`](references/paper-threading.md)

### Key Techniques

| Topic | Approach |
|------|------|
| Portable vs. block-bound | Leave `location(...)` out for portable block menus; set it only to drive a real block |
| `checkReachable` | Default `false`. Set `true` with `location(...)` when the player must stay next to that block |
| Anvil cost | `AnvilView#setMaximumRepairCost` (the vanilla limit is 40). Re-apply it in `PrepareAnvilEvent`; `setRepairCost` sets the price of the current result |
| Telling your views apart | Track the players you opened a view for (UUID set, cleared on close), not the title text |
| Merchant | `Bukkit.createMerchant()` + `MerchantRecipe`; `MenuType.MERCHANT.builder().merchant(...)` |
| Storage screens | Do not use block-entity menu types for storage; use `Bukkit.createInventory` with an `InventoryHolder` |

## Fallback

| Error | Cause | Fix |
|------|------|------|
| Portable furnace accepts fuel but never smelts | Block-entity menus without `location` use a temporary block entity that never ticks | Point `location(...)` at a real furnace, or do not offer it |
| Items vanish when a portable hopper / shulker / 9x3 menu closes | The temporary block entity is not saved | Use `Bukkit.createInventory` for storage |
| Anvil still says "Too Expensive!" | The limit was set once and vanilla recomputed the view | Re-apply `setMaximumRepairCost` in `PrepareAnvilEvent` |
| The menu closes immediately | `checkReachable(true)` with the player far from `location` | Leave `checkReachable` at `false` for portable menus |
| Real anvil gets damaged by a "portable" anvil | `location(...)` pointed at that anvil | Leave `location` out |
| `IllegalArgumentException: The given player must be ...` | `build` was called with a non-player `HumanEntity` | Build views only for online `Player`s |
