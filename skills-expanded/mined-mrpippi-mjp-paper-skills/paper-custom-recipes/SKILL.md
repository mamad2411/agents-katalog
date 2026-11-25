---
name: paper-custom-recipes
description: "Paper 自訂配方：有形狀／無形狀合成、ItemTypeChoice 多材料、ExactChoice 自訂物品、TransmuteRecipe 升級保留附魔、26.3 BrewingRecipe（1.21.11 用 PotionMix）、批次註冊後只同步一次、配方書解鎖與停用時移除 / Paper custom recipes: shaped and shapeless crafting, ItemTypeChoice alternatives, ExactChoice custom items, TransmuteRecipe upgrades that keep enchantments, 26.3 BrewingRecipe (PotionMix on 1.21.11), batch registration with one resync, recipe book unlocks and cleanup on disable"
---

# Paper Custom Recipes

## Skill Name

`paper-custom-recipes`

## Purpose

Register crafting and brewing recipes from a plugin, keep them in sync with clients, and remove them cleanly:

| Recipe | API | Typical use |
|------|-----|------|
| Shaped / shapeless | `ShapedRecipe`, `ShapelessRecipe` + `RecipeChoice` | New items from vanilla materials |
| Several acceptable materials | `RecipeChoice.itemType(ItemType...)` | "any stick or blaze rod" |
| A custom item as ingredient | `RecipeChoice.exactChoice(stack)` (1.21.11: `new RecipeChoice.ExactChoice(stack)`) | Recipes that consume plugin items |
| Change the item type, **keep its components** | `TransmuteRecipe` | Iron sword + diamond → diamond sword with the same enchantments, name and damage |
| Brewing | 26.3: `BrewingRecipe` (a normal `Recipe`); 1.21.11: `PotionMix` through `PotionBrewer` | New potions |

Every recipe change makes the server resend the recipe list to all players, so registering 20 recipes one by one sends it 20 times. The template registers the whole batch with one resync: `Bukkit.addRecipes(list)` / `removeRecipes(keys)` on 26.3, `addRecipe(recipe, false)` + one `Bukkit.updateRecipes()` on 1.21.11.

## Paper Version Requirements

- Paper 1.21.11 / 26.3 (both compile-verified with deprecation warnings enabled; differing lines carry `// @1.21.11:`, the brewing class is split with `// @only`)
- `ShapedRecipe`, `ShapelessRecipe`, `TransmuteRecipe`, `RecipeChoice.itemType(...)` and `Bukkit.updateRecipes()` are the same on both versions
- Changed in 26.3 (Javadoc): `Bukkit.addRecipe(Recipe, boolean)` and `removeRecipe(NamespacedKey, boolean)` are deprecated because Minecraft always resends on every change — use the new `addRecipes(Iterable)` / `removeRecipes(Iterable)` batch methods; the `ExactChoice` constructors are deprecated for removal (since 26.2) in favor of `RecipeChoice.exactChoice(...)`
- Brewing:

| Version | API | Remove with |
|------|-----|------|
| 26.3 | `new BrewingRecipe(key, result, input, ingredient)` + `Bukkit.addRecipe` | `Bukkit.removeRecipe(key)` |
| 1.21.11 | `new PotionMix(key, result, input, ingredient)` + `Bukkit.getPotionBrewer().addPotionMix` | `removePotionMix(key)` |

  In 26.3 `PotionBrewer` and `PotionMix` are deprecated in favor of the data-driven `BrewingRecipe`.
- **Spigot**: Core portable — `ShapedRecipe`, `ShapelessRecipe`, `TransmuteRecipe` and `ExactChoice` exist in Spigot-API 26.3; replace `RecipeChoice.itemType(...)` (Paper only) with `MaterialChoice` and `ItemStack.of` with `new ItemStack`. Spigot's `BrewingRecipe` has a different constructor (`NamespacedKey, ItemStack`), so the brewing class must be rewritten for Spigot

## Triggers

- 「自訂配方」「custom recipe」「ShapedRecipe」「ShapelessRecipe」「addRecipe」
- 「TransmuteRecipe」「升級保留附魔」「keep enchantments upgrade」
- 「釀造配方」「BrewingRecipe」「PotionMix」「custom potion recipe」
- 「ExactChoice」「ItemTypeChoice」「updateRecipes」「配方書」「discoverRecipe」

## Inputs

| Parameter | Example | Description |
|------|------|------|
| `package` | `com.example.recipes` | Output package |
| `recipes` | trident, sword upgrade, healing brew | Which recipes to add |
| `unlock` | on join | When players get the recipes in their recipe book |

## Outputs

- `CustomRecipes.java` — builds every recipe, registers them with one resync, unlocks and removes them
- `Brewing.java` — the brewing recipe for 26.3 (`BrewingRecipe`) and 1.21.11 (`PotionMix`), selected at compile time
- `RecipesPlugin.java` — wiring: register on enable, unlock on join, remove on disable

## Build Setup

See [`references/paper-api-platform.md`](references/paper-api-platform.md). Only `paper-api` (`compileOnly`) is required.

## Code Template

### `CustomRecipes.java`

```java
package com.example.recipes;

import org.bukkit.Bukkit;
import org.bukkit.Keyed;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.ItemType;
import org.bukkit.inventory.Recipe;
import org.bukkit.inventory.RecipeChoice;
import org.bukkit.inventory.ShapedRecipe;
import org.bukkit.inventory.ShapelessRecipe;
import org.bukkit.inventory.TransmuteRecipe;
import org.bukkit.inventory.recipe.CraftingBookCategory;
import org.bukkit.plugin.Plugin;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;

/**
 * Owns the plugin's crafting recipes. Main thread only.
 *
 * <p>Keys are stable ({@code <plugin>:<name>}): players' recipe books store them, and a key that changes between
 * versions leaves dead entries behind.
 */
public final class CustomRecipes {

    private final Plugin plugin;
    private final List<NamespacedKey> registered = new ArrayList<>();

    public CustomRecipes(Plugin plugin) {
        this.plugin = plugin;
    }

    /**
     * Builds every recipe and adds the missing ones with a single resync to players. Safe to call again: after
     * /minecraft:reload (which drops plugin recipes) it re-adds them, and keys that still exist are skipped.
     */
    public void registerAll(ItemStack customIngredient) {
        List<Recipe> all = build(customIngredient);
        List<Recipe> fresh = new ArrayList<>();
        for (Recipe recipe : all) {
            if (Bukkit.getRecipe(((Keyed) recipe).getKey()) == null) {   // skip keys that are still registered
                fresh.add(recipe);
            }
        }
        try {
            Bukkit.addRecipes(fresh); // @1.21.11:             fresh.forEach(r -> Bukkit.addRecipe(r, false)); Bukkit.updateRecipes();
        } catch (RuntimeException e) {
            plugin.getLogger().log(Level.WARNING, "Invalid recipe in batch", e);
        }
        registered.clear();
        for (Recipe recipe : all) {
            NamespacedKey key = ((Keyed) recipe).getKey();
            if (Bukkit.getRecipe(key) != null) {
                registered.add(key);
            }
        }
    }

    /** Keys of the recipes that were actually added (for recipe book unlocks). */
    public List<NamespacedKey> keys() {
        return List.copyOf(registered);
    }

    /** onDisable: remove everything this plugin added with a single resync. */
    public void unregisterAll() {
        Bukkit.removeRecipes(registered); // @1.21.11:         registered.forEach(k -> Bukkit.removeRecipe(k, false)); Bukkit.updateRecipes();
        registered.clear();
    }

    private List<Recipe> build(ItemStack customIngredient) {
        List<Recipe> recipes = new ArrayList<>();
        try {
            recipes.add(trident());
            recipes.add(diamondSwordUpgrade());
            recipes.add(infusedBread(customIngredient));
        } catch (RuntimeException e) {                          // e.g. an empty RecipeChoice
            plugin.getLogger().log(Level.WARNING, "Could not build a recipe", e);
        }
        return recipes;
    }

    /** Shaped recipe; the handle accepts a stick or a blaze rod. */
    private ShapedRecipe trident() {
        ShapedRecipe recipe = new ShapedRecipe(key("trident"), ItemStack.of(Material.TRIDENT));
        recipe.shape(" PP", " HP", "H  ");
        recipe.setIngredient('P', RecipeChoice.itemType(ItemType.PRISMARINE_SHARD));
        recipe.setIngredient('H', RecipeChoice.itemType(ItemType.STICK, ItemType.BLAZE_ROD));
        recipe.setCategory(CraftingBookCategory.EQUIPMENT);
        return recipe;
    }

    /**
     * Transmute: the result keeps every component of the input (enchantments, name, damage, trims). The output type
     * changes from iron sword to diamond sword; the material slot is consumed.
     */
    private TransmuteRecipe diamondSwordUpgrade() {
        TransmuteRecipe recipe = new TransmuteRecipe(key("diamond_sword_upgrade"), Material.DIAMOND_SWORD,
                RecipeChoice.itemType(ItemType.IRON_SWORD),
                RecipeChoice.itemType(ItemType.DIAMOND));
        recipe.setCategory(CraftingBookCategory.EQUIPMENT);
        return recipe;
    }

    /** ExactChoice matches the full item (components included), so plugin items cannot be faked with renamed vanilla items. */
    private ShapelessRecipe infusedBread(ItemStack customIngredient) {
        ShapelessRecipe recipe = new ShapelessRecipe(key("infused_bread"), ItemStack.of(Material.BREAD, 2));
        recipe.addIngredient(RecipeChoice.exactChoice(customIngredient)); // @1.21.11:         recipe.addIngredient(new RecipeChoice.ExactChoice(customIngredient));
        recipe.addIngredient(RecipeChoice.itemType(ItemType.WHEAT));
        recipe.setCategory(CraftingBookCategory.MISC);
        return recipe;
    }

    private NamespacedKey key(String name) {
        return new NamespacedKey(plugin, name);
    }
}
```

### `Brewing.java` (26.3)

```java
// @only 26.3
package com.example.recipes;

import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.inventory.BrewingRecipe;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.ItemType;
import org.bukkit.inventory.RecipeChoice;
import org.bukkit.inventory.meta.PotionMeta;
import org.bukkit.plugin.Plugin;
import org.bukkit.potion.PotionType;

/** Awkward Potion + Glow Berries -> Potion of Regeneration. 26.3: brewing recipes are ordinary recipes. */
public final class Brewing {

    private final NamespacedKey key;

    public Brewing(Plugin plugin) {
        this.key = new NamespacedKey(plugin, "regeneration_from_glow_berries");
    }

    /** Idempotent: also used to re-add the recipe after /minecraft:reload dropped it. */
    public boolean register() {
        if (Bukkit.getRecipe(key) != null) {
            return true;
        }
        BrewingRecipe recipe = new BrewingRecipe(key,
                potion(PotionType.REGENERATION),
                RecipeChoice.exactChoice(potion(PotionType.AWKWARD)),       // bottom slots
                RecipeChoice.itemType(ItemType.GLOW_BERRIES));                // top slot
        return Bukkit.addRecipe(recipe);              // 26.3 always resends on a recipe change
    }

    public void unregister() {
        Bukkit.removeRecipe(key);
    }

    static ItemStack potion(PotionType type) {
        ItemStack stack = ItemStack.of(Material.POTION);
        stack.editMeta(PotionMeta.class, meta -> meta.setBasePotionType(type));
        return stack;
    }
}
```

### `Brewing.java` (1.21.11)

```java
// @only 1.21.11
package com.example.recipes;

import io.papermc.paper.potion.PotionMix;
import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.ItemType;
import org.bukkit.inventory.RecipeChoice;
import org.bukkit.inventory.meta.PotionMeta;
import org.bukkit.plugin.Plugin;
import org.bukkit.potion.PotionType;

/** Same recipe for 1.21.11, where brewing goes through PotionBrewer (deprecated in 26.3). */
public final class Brewing {

    private final NamespacedKey key;

    public Brewing(Plugin plugin) {
        this.key = new NamespacedKey(plugin, "regeneration_from_glow_berries");
    }

    /** Idempotent: remove first so a second call does not register the mix twice. */
    public boolean register() {
        Bukkit.getPotionBrewer().removePotionMix(key);
        Bukkit.getPotionBrewer().addPotionMix(new PotionMix(key,
                potion(PotionType.REGENERATION),
                new RecipeChoice.ExactChoice(potion(PotionType.AWKWARD)),
                RecipeChoice.itemType(ItemType.GLOW_BERRIES)));
        return true;
    }

    public void unregister() {
        Bukkit.getPotionBrewer().removePotionMix(key);
    }

    static ItemStack potion(PotionType type) {
        ItemStack stack = ItemStack.of(Material.POTION);
        stack.editMeta(PotionMeta.class, meta -> meta.setBasePotionType(type));
        return stack;
    }
}
```

### `RecipesPlugin.java`

```java
package com.example.recipes;

import io.papermc.paper.event.server.ServerResourcesReloadedEvent;
import org.bukkit.Material;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.inventory.ItemStack;
import org.bukkit.plugin.java.JavaPlugin;

public final class RecipesPlugin extends JavaPlugin implements Listener {

    private CustomRecipes recipes;
    private Brewing brewing;
    private ItemStack ingredient;

    @Override
    public void onEnable() {
        recipes = new CustomRecipes(this);
        brewing = new Brewing(this);
        ingredient = ItemStack.of(Material.GLOW_BERRIES);          // replace with your custom item (see paper-data-components)
        recipes.registerAll(ingredient);
        if (!brewing.register()) {
            getLogger().warning("Brewing recipe was not added");
        }
        getServer().getPluginManager().registerEvents(this, this);
        for (Player online : getServer().getOnlinePlayers()) {     // /reload or late enable
            online.discoverRecipes(recipes.keys());
        }
    }

    @Override
    public void onDisable() {
        if (brewing != null) {
            brewing.unregister();
        }
        if (recipes != null) {
            recipes.unregisterAll();                                // one resync
        }
    }

    /**
     * /minecraft:reload rebuilds the recipe list from data packs and drops every plugin recipe (crafting and brewing;
     * observed on Paper 26.3). Add them back.
     */
    @EventHandler
    public void onResourcesReloaded(ServerResourcesReloadedEvent event) {
        recipes.registerAll(ingredient);
        brewing.register();
    }

    /** The recipe book only shows recipes a player has discovered; crafting works either way. */
    @EventHandler
    public void onJoin(PlayerJoinEvent event) {
        event.getPlayer().discoverRecipes(recipes.keys());
    }
}
```

## Recommended Directory Structure

```
src/main/java/com/example/recipes/
├── CustomRecipes.java   <- crafting recipes, one resync
├── Brewing.java         <- BrewingRecipe (26.3) or PotionMix (1.21.11)
└── RecipesPlugin.java   <- enable / join / disable wiring
```

## Thread Safety

- `Bukkit.addRecipe`, `removeRecipe`, `updateRecipes` and `discoverRecipes` are main-thread only
- Recipes are global server state: register them once in `onEnable`, never per player or per event
- See [`references/paper-threading.md`](references/paper-threading.md)

### Key Techniques

| Topic | Approach |
|------|------|
| Resync cost | 26.3: `Bukkit.addRecipes(list)` / `removeRecipes(keys)` (the `boolean resend` overloads are deprecated); 1.21.11: `addRecipe(recipe, false)` for each, then one `Bukkit.updateRecipes()` |
| Alternatives | `RecipeChoice.itemType(a, b, ...)` (Paper) accepts any of the listed item types |
| Custom ingredients | `ExactChoice` compares the whole item; for "any item with my PDC id" check the ingredient in `PrepareItemCraftEvent` instead |
| Keep enchantments on upgrade | `TransmuteRecipe` copies the input's components to the result; a shaped recipe would produce a fresh item |
| Brewing input | The bottom slots match the `input` choice; an `ExactChoice` of an Awkward Potion only accepts that exact potion |
| Recipe book | `discoverRecipes(keys)` on join; crafting works without it, the book just hides undiscovered recipes |
| Cleanup | Remove every key on disable; a recipe left behind after the plugin is gone keeps producing items |
| `/minecraft:reload` | Drops plugin recipes (crafting and brewing) and rebuilds from data packs; re-register in `ServerResourcesReloadedEvent` (`registerAll` and `Brewing#register` are idempotent) |

## Fallback

| Error | Cause | Fix |
|------|------|------|
| `IllegalStateException: Duplicate recipe` | The key is already registered (second enable, `/reload`) | Remove on disable; skip keys that already exist (`Bukkit.getRecipe(key) != null`) |
| Clients lag or freeze when the plugin enables | Each `addRecipe(recipe)` resent the whole recipe list | 26.3: `addRecipes(list)`; 1.21.11: `addRecipe(recipe, false)` + one `updateRecipes()` |
| Deprecation warnings for `addRecipe(Recipe, boolean)` / `new ExactChoice(...)` on 26.3 | Deprecated in 26.3 / 26.2 | `addRecipes` / `removeRecipes`, `RecipeChoice.exactChoice(...)` |
| Upgraded sword loses its enchantments | Built with a shaped/shapeless recipe | Use `TransmuteRecipe` |
| Custom ingredient recipe never matches | `ExactChoice` item differs in any component (name, PDC, damage) | Build the ingredient from the same factory, or validate in `PrepareItemCraftEvent` |
| Recipe missing from the recipe book but craftable | Not discovered | `discoverRecipes` on join |
| All plugin recipes gone after `/minecraft:reload` | The reload rebuilt the recipe list from data packs only | Re-register in `ServerResourcesReloadedEvent`, or ship the recipes in a data pack (`paper-datapack-bundling`) |
| `NoClassDefFoundError: BrewingRecipe` on 1.21.11 | `BrewingRecipe` exists only on 26.3 | Use the `PotionMix` variant (`// @only 1.21.11`) |
| Deprecation warnings for `PotionBrewer` / `PotionMix` on 26.3 | Replaced by `BrewingRecipe` | Use the 26.3 variant |
