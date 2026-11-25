---
name: paper-chest-gui
description: "以 Bukkit API 建立箱子介面 GUI：InventoryHolder 標記介面、單一 GuiListener 取消點擊／拖曳／Shift／數字鍵、每次點擊重新驗證、分頁與去彈跳、gui.yml 圖示、onDisable 關閉所有選單 / Chest-inventory GUIs with the Bukkit API: holder marker interface, one cancelling listener, per-click revalidation, paging, gui.yml icons, safe disable"
---

# Paper Chest GUI

## Skill Name

`paper-chest-gui`

## Purpose

Build chest-style menus (shop lists, confirmation pages, settings pages) with the plain Bukkit/Paper API, without touching NMS.
The point is not how to display them, but how to keep players from duplicating items:

- One `InventoryHolder` per menu kind, all sharing one **marker interface**, so the whole plugin needs only one `GuiListener` to decide "this is my menu"
- Always cancel clicks and drags on the top menu; also cancel Shift-clicks, number keys, double-clicks, and offhand swaps in the **bottom inventory**, otherwise items get moved into the menu or pulled out of it
- **Revalidate** state on every click (permission, balance, whether the listing still exists); never trust what is drawn on screen
- After async work completes, switch back to the main thread and confirm the menu is **still open** before updating it
- Close every open menu in `onDisable` to avoid "ghost items"; guard the `InventoryCloseEvent` handler with `plugin.isEnabled()`

> For form input and confirmation dialogs (yes/no), prefer [`paper-dialog-ui`](../paper-dialog-ui/SKILL.md); no chest slots needed.
> Use `nms-custom-menu` when you need an NMS `AbstractContainerMenu` (custom container logic, special slots).

## Paper Version Requirements

- Paper 1.21.11 / 26.3 (same template for both; `InventoryView` became an interface in 26.2, and this skill only uses `event.getInventory()` and `player.getOpenInventory()`, so it compiles on both)
- Pure Paper API, no Paperweight needed
- **Spigot**: Core portable — `InventoryHolder` and the click guard are Bukkit API; replace Adventure names/titles, `ItemStack#editMeta` and the `TOOLTIP_DISPLAY` data component

## Triggers

- "箱子 GUI", "chest GUI", "InventoryHolder", "選單", "menu", "createInventory"
- "分頁", "paging", "翻頁", "InventoryClickEvent", "物品被拿走", "刷物品", "dupe"
- "gui.yml", "圖示設定", "確認購買"

## Inputs

| Parameter | Example | Description |
|------|------|------|
| `package` | `com.example.shop.gui` | Package of the GUI classes |
| `menu_kinds` | `PagedListMenu`, `ConfirmPurchaseMenu` | Menu kinds to build (one holder per kind) |
| `rows` | `6` | Row count (6 rows = 54 slots; top 45 for content, bottom row for navigation buttons) |
| `icons_file` | `gui.yml` | Icon config file (Material + MiniMessage name/lore) |
| `permission` | `shop.buy` | Permission required for the action (rechecked on every click) |

## Outputs

- `ShopMenu.java` — marker interface (`InventoryHolder` + `onClick`/`onClose`)
- `MenuClick.java` — click data passed to the menu (immutable)
- `NavSlot.java` — fixed navigation slots
- `Icons.java` — loads icons and titles (MiniMessage) from `gui.yml`
- `PlayerItems.java` — drops items at the player's feet when the inventory is full
- `LatestOnly.java` — ticket numbers for "the last click wins"
- `PagedListMenu.java` — paged list holder
- `Menus.java` — open/close/return from async to main thread/`closeAll`
- `GuiListener.java` — the single click, drag, and close listener
- `ShopPlugin.java` — registers the listener and closes menus in `onDisable`
- `gui.yml` — icon and title config

## Build Setup

See [`references/paper-api-platform.md`](references/paper-api-platform.md). Only `paper-api` (`compileOnly`) is needed.

`src/main/resources/gui.yml` (default contents; `Icons.load` writes it to `plugins/<name>/gui.yml` on first run):

```yaml
titles:
  list: "<dark_gray>Shop <gray>(<page>/<pages>)"
  confirm: "<dark_gray>Confirm purchase"
icons:
  prev:
    material: ARROW
    name: "<white>Previous page"
  next:
    material: ARROW
    name: "<white>Next page"
  page:
    material: PAPER
    name: "<gray>Page <white><page><gray>/<white><pages>"
  entry:
    material: STONE
    name: "<white><name>"
    lore:
      - "<gray>Price: <gold><price>"
      - "<dark_gray>Click to buy"
  confirm:
    material: LIME_CONCRETE
    name: "<green>Confirm"
    lore:
      - "<gray>Pay <gold><price>"
  cancel:
    material: RED_CONCRETE
    name: "<red>Cancel"
```

- All player-visible text goes in `gui.yml` (English, MiniMessage); code contains no literals (the only exception is defensive messages such as "something went wrong", which in practice should also move to `lang.yml`)
- Selected/unselected markers in list options reuse the same prefixes (selected `" <white>▸ "`, unselected `"   <gray>"`) so different menus look consistent
- Leave empty slots empty instead of filling them with glass panes; when you really need a "dead slot", use `setHideTooltip(true)` to avoid an empty tooltip box

## Code Template

The full source lives in [`template.md`](template.md) (about 650 lines, compiled against Paper 1.21.11 and 26.3 in CI). **Read `template.md` before writing any code for this skill**, and copy from it instead of rebuilding the classes from the table below.

| File | Package | Role |
|------|---------|------|
| `ShopMenu.java` | `.gui` | Marker interface for this plugin's holders |
| `MenuClick.java` | `.gui` | Immutable snapshot of one click |
| `NavSlot.java` | `.gui` | Fixed slots: 45 content slots, bottom navigation row |
| `Icons.java` | `.gui` | Loads icons from `gui.yml` |
| `PlayerItems.java` | `.gui` | Gives items, dropping at the feet when full |
| `LatestOnly.java` | `.gui` | Last click wins for async work |
| `PagedListMenu.java` | `.gui` | Paged list holder |
| `Menus.java` | `.gui` | Open / close, async results back to the main thread |
| `GuiListener.java` | `.gui` | The single click / drag / close / quit listener |
| `ShopPlugin.java` | root | Registration and closing open menus on disable |

## Recommended Directory Structure

```
src/main/java/com/example/shop/
├── ShopPlugin.java
└── gui/
    ├── ShopMenu.java            ← marker interface
    ├── MenuClick.java
    ├── NavSlot.java
    ├── Icons.java
    ├── PlayerItems.java
    ├── LatestOnly.java
    ├── Menus.java
    ├── GuiListener.java         ← the only listener
    ├── PagedListMenu.java       ← one holder per menu kind
    └── ConfirmPurchaseMenu.java
src/main/resources/
└── gui.yml
```

## Thread Safety

- Events, `onClick`, Inventory creation, and `openInventory` all run on the main thread; JDBC/HTTP run async
- Async lambdas carry only a `UUID` and immutable data (the result of `List.copyOf`), never `Player`, `Inventory`, or `ItemStack`
- Return to the main thread with `Menus.openOnMain` / `updateIfStillOpen`: they already include the three checks "plugin still enabled -> player still online -> menu still open"
- Rapid clicking/paging: synchronous redraws compute against the current state on every click; async loads use `LatestOnly` to discard stale results
- To open another menu or close the window inside an `InventoryClickEvent`, use `openNextTick` / `closeNextTick`
- Inside the `InventoryCloseEvent` handler (`onClose`), run `if (!plugin.isEnabled()) return;` before scheduling any task; `closeAll()` in `onDisable` triggers it synchronously, and scheduling then throws `IllegalPluginAccessException`; synchronous cleanup such as returning items should still run
- See [`references/paper-threading.md`](references/paper-threading.md)

## Fallback

| Error | Cause | Solution |
|------|------|------|
| Players can take the menu icons | Only top-menu clicks were cancelled; Shift/number key/double-click were missed | Use this skill's `GuiListener` (it also cancels guarded actions in the bottom inventory) |
| Dragging items into the menu | `InventoryDragEvent` not handled | Always cancel drags that reach top slots (`rawSlot < topSize`) |
| Item bought but no money deducted / charged twice | Trusted the screen, or double-clicked | Revalidate on every click; debounce; do not give the item if payment fails |
| Async result overwrites the new screen | An older request returned later | Take a ticket with `LatestOnly`; discard stale results |
| NPE / wrong menu opened after async returns | The player went offline or closed the menu | `Menus.updateIfStillOpen` (main thread + still-open check) |
| `IllegalPluginAccessException` (on disable) | The `InventoryCloseEvent` handler schedules work inside `onDisable` | Check `plugin.isEnabled()` before scheduling (blocks scheduling only, not synchronous cleanup) |
| Players have extra/missing items after a server restart | `onDisable` did not close menus | `Menus.closeAll()`, and return held items in `onClose` |
| Items vanish when the inventory is full | The return value of `addItem` was ignored | `PlayerItems.giveOrDrop` |
| Cursor or items get messed up when opening a new menu directly in a click event | Container swapped within the same event | `openNextTick` |
| Icons display in italics | Bukkit italicizes custom names by default | `Icons` turns italics off globally |
| Need to enter text/numbers/confirm | A chest is not a form | Use `paper-dialog-ui`; for NMS custom containers use `nms-custom-menu` |
