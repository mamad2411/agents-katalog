---
name: kitchen-library
description: Personal Kuschi kitchen library on GitHub Pages — data layout, user recipes, Riviera, theme.css, order list, master ingredients, and git workflow.
---

# Kitchen library hub

Read before large edits to HTML, JSON recipe data, or `.cursor` rules.

## Purpose

Static **GitHub Pages** site: main catalog ([index.html](index.html)), user-defined **kitchen books** ([kitchen-book.html?b=…](kitchen-book.html)), Riviera prep-chef set ([riviera.html](riviera.html)). Optimized for a small kitchen tablet. Main search uses precomputed per-recipe haystacks + memoised filters; see README “Main index performance” for `kuschiShowFilterMs` / `kuschiDebugPerf`.

## Agent shipping (after you change code)

Matches [.cursor/rules/ship-after-change.mdc](../../rules/ship-after-change.mdc) — do this by default when finishing a task unless the user says not to commit/push.

1. **Test** — `node --check` on any edited `assets/*.js`; when HTML/behaviour changed, quick static server from repo root + browser spot-check on affected pages if you can.
2. **Commit** — Conventional Commits; small, focused messages.
3. **Push** — `git push origin` the current branch (`main` is normal for small updates).

Skip only if the user explicitly opts out.

## LLM context (tokens)

Follow **`~/.cursor/rules/token-efficiency.mdc`** (global). This repo’s **[`.cursorignore`](../../../.cursorignore)** keeps bulk indexes (`claude_index/`, `alpha_catalog/`, etc.) out of broad Cursor index context; still use **targeted reads** for `recipe_detail/` (SSOT). Optional **local code-search MCP** options and a pilot checklist live in **[PrepFlow `AGENTS.md`](../../../../Prepflow-Ecosystem/prepflow-web/AGENTS.md)** under “Cursor: token-efficient discovery” — use there first if you add MCP; this static site rarely needs it.

## Directories

| Path | Role |
|------|------|
| `assets/theme.css` | **Shared** theme: `:root` tokens, search, filters, modal shell, footer, spin, form helpers, base `.grid` |
| `alpha_catalog/` | **Browser** catalog — **8** merged `catalog_XX.json` + `manifest.json` (from `rebuild_catalog_from_detail.py`) |
| `claude_index/` | Compact shards — same rebuild script (from `recipe_detail/`) |
| `recipe_detail/detail_*.json` | **SSOT** full payloads: `detail_{Letter}_{bucket}.json` (64 buckets, FNV-1a on id). Letter is usually the first ASCII letter of the English `name`, but can differ after imports — compact rows carry **`_detailLetter`** so modals fetch the correct sub-shard. Regenerate layout with `repartition_detail_shards.py` / `repartition_detail_subshards.py`. |
| `kitchen_library_*.json` | Additional library chunks |
| `assets/user-recipes.js` | **localStorage** helpers (browser-only) — see keys below |
| `aroma_data/*.json`, [aroma.html](aroma.html), [assets/aroma-hints.js](assets/aroma-hints.js) | **Aroma Bible** extract: food↔spice index, harmony data, recipe hints + [aroma.html](aroma.html) lookup — see [.cursor/skills/aroma-bible/SKILL.md](../aroma-bible/SKILL.md). [aroma.html](aroma.html) uses full `ingredients.json`. **Recipe modals** (kitchen / Riviera / books) use [assets/aroma-hints.js](assets/aroma-hints.js) with **`ingredients_modal_core.json`** (~half size) and **`combined_data/ingredients_unified_modal.json`** (slim flavor rows for “More flavour”); regenerate both with `node scripts/build_aroma_modal_data.mjs` after editing `ingredients.json` or `ingredients_unified.json`. |
| [flavor.html](flavor.html), [pairing-atlas.html](pairing-atlas.html), [notebooklm-gallery.html](notebooklm-gallery.html), `notebooklm/manifest.json`, `aroma_data/aroma_matrix_meta.json`, `combined_data/`, `flavour_data/flavour_knowledge_db_v1.1.json`, `flavor_data/`, `thesaurus_data/`, `scripts/run_all_extractions.sh`, `scripts/merge_all_sources.py` | **Flavor** + **Aroma matrix** (`pairing-atlas.html`: G1–G8 grid, unified-data drawer, harmony heatmap, food×spice table) + **Visual guides**; `ingredients_unified.json` is **schema v2** (`ingredients` + `kitchen_context` bundle); regenerate merge with `python3 scripts/merge_all_sources.py` after extractions; `flavor.html?q=` deep-links; **Kitchen toolkit** tab + Explore overlays use `flavour_data/flavour_knowledge_db_v1.1.json` (replace file when the DB is updated) |
| [pantry.html](pantry.html) | Pantry tokens → `alpha_catalog` match; opens `index.html?open=<id>` |
| `riviera_sources/current/Riviera_Source_Of_Truth_2026-07-08.md`, `riviera_sources/current/Riviera_Recipe_Catalog_Source_Of_Truth_2026-07-08.json` | **Riviera SSOT:** the 23 live ChatGPT Riviera project sources are the baseline; `Riviera_Tapas_House_Standards_Overlay_2026-07-08.md` is the only July 8 overlay for the 16 tapas/canape house standards. Edit the structured recipe catalog first for built-in recipe changes, then sync `riviera_data/builtins.json` with `python3 scripts/sync_riviera_recipe_catalog.py --write`; `--check` must pass before PDF generation or shipping. Rebuild merged docs with `python3 scripts/build_riviera_source_of_truth.py`. Treat `function_packages.json` and generated PDFs as operational representations for non-overlay conflicts. |
| `assets/order-list.js` | Shared **order list** modal logic ([riviera.html](riviera.html), [kitchen-book.html](kitchen-book.html)) |
| [kitchen-book.html](kitchen-book.html) | Per-device **kitchen books** (`?b=id`): search, add recipe (manual + Gemini), QR, **order list** (per-book storage), **Admin** PIN for delete book / remove recipe |
| `assets/screen-wake.js` | **Keep screen on** toggle (`[data-kuschi-wake]`) — shown in recipe detail modals only |
| `scraped_raw/`, `pdf/` | Source / export artifacts |
| `scripts/rebuild_catalog_from_detail.py` | After `recipe_detail/` edits (or merges): regenerates `claude_index/`, `alpha_catalog/`, pantry hay — **run this before commit** for the live site. |
| `scripts/detect-nonenglish-recipes.py`, `translate_recipes.py`, `sync_claude_index_from_detail.py`, `repartition_detail_shards.py`, `repartition_detail_subshards.py` | Optional: translate to English, targeted `claude_index` sync, repartition detail after name-first-letter changes — see [README.md](../../../README.md); full pipeline still ends with **rebuild** + `check-recipe-shards.py`. |

### Aroma modal data — when to shard further (agent checklist)

Slim artifacts (`ingredients_modal_core.json`, `ingredients_unified_modal.json` via `node scripts/build_aroma_modal_data.mjs`) are enough while files stay small and modals stay responsive.

**Escalate** (implement without asking the user first if you hit these while editing aroma/unified or profiling modals):

1. **`ingredients_unified_modal.json`** grows past **~400–500KB** *or* “More flavour” still causes long main-thread tasks after existing deferrals — add **sharded** slim files (e.g. by normalized name prefix or hash bucket), a tiny **routing index** (recipe-line tokens → candidate shard keys; **fallback fetch all shards** if index misses to avoid false negatives), and teach `ensureUnifiedLoaded` in [assets/aroma-hints.js](assets/aroma-hints.js) to fetch only candidates + merge. Mirror patterns in [.cursor/skills/big-static-data-frontend/SKILL.md](../big-static-data-frontend/SKILL.md) (Pantry routing index, `siteBaseUrl()`).
2. **`ingredients_modal_core.json`** passes **~150KB** *or* row count **≫200** — consider splitting the core file by bucket; keep **one merge** in memory after `Promise.all` (or batched concurrency), update [sw.js](../../../sw.js) `CACHEABLE`, and extend `scripts/build_aroma_modal_data.mjs`.

Regenerate slim outputs after any source change; bump `CACHE_NAME` in [sw.js](../../../sw.js) when adding new static URLs clients must fetch.

## User data (client-side)

- **Kitchen** recipes: `kuschi_user_recipes_kitchen_v1` — merged into the main list; detail view does **not** use `recipe_detail/` fetch for `user-*` ids.
- **Custom kitchen books:** `kuschi_custom_kitchen_books_v1` — JSON array of `{ id, name, createdAt }`. Per-book recipes: `kuschi_book_<id>_recipes_v1` (same shape as kitchen user recipes). **Per book, fully isolated from Riviera and other books:** `kuschi_book_<id>_order_overrides_v1`, `kuschi_book_<id>_order_extras_v1`, `kuschi_book_<id>_master_v1` (same shapes as Riviera order/master). `deleteCustomBook` removes recipe + order + master keys for that id. Helpers include `loadBookOrderOverrides`, `saveBookOrderOverrides`, `loadBookOrderExtras`, `addBookOrderExtra`, `updateBookOrderExtra`, `removeBookOrderExtra`, `loadBookMaster`, `upsertBookMasterIngredient`, `resolveBookDefaultZone`, `exportBookOrderBundle`, `exportBookMaster` on [assets/user-recipes.js](assets/user-recipes.js). Open [kitchen-book.html](kitchen-book.html) with query `?b=<id>`; home hero **Order list** uses [assets/order-list.js](assets/order-list.js) with book-scoped storage only.
- **Kitchen book admin session:** `sessionStorage` key `kuschi_kitchen_book_admin_session` — value `1` when unlocked. Footer **Admin** / **Lock**; PIN `KITCHEN_BOOK_ADMIN_PIN` in [kitchen-book.html](kitchen-book.html) (same value as Riviera for one mental model). While unlocked: **Delete this kitchen book** and recipe detail **Remove from this book** are available. Order list editing does not require admin (same as Riviera order list).
- **Riviera** recipes: `kuschi_user_recipes_riviera_v1` — prepended to visible built-ins in [riviera.html](riviera.html) (see hidden built-ins below).
- **Riviera hidden built-ins:** `kuschi_riviera_hidden_builtin_ids_v1` — JSON array of built-in recipe `id` strings to hide on this device only. Helpers: `loadRivieraHiddenBuiltinIds`, `hideRivieraBuiltin`, `restoreAllHiddenRivieraBuiltins` in [assets/user-recipes.js](assets/user-recipes.js). `mergeRivieraRecipes()` filters `BUILTIN_RECIPES` against this list. Order overrides may still contain keys for hidden recipes until edited or cleared.
- **Riviera admin session:** `sessionStorage` key `kuschi_riviera_admin_session` — value `1` when unlocked. Footer **Admin** opens PIN entry; correct PIN sets the session (fixed value `RIVIERA_ADMIN_PIN` in [riviera.html](riviera.html)). **Lock** clears the session. While unlocked: recipe detail modal shows **Hide from my list** (built-ins) or **Remove recipe** (user-saved); footer **Restore hidden built-ins** clears the hidden-id list. PIN is only casual protection (visible in source).
- **Master ingredients:** `kuschi_master_ingredients_v1` — `{ id, name, defaultZone }` with `defaultZone` in `freezer` \| `coldroom` \| `drystore` \| `other`. Used to default zones for matching ingredient names on the Riviera order list.
- **Riviera order overrides:** `kuschi_riviera_order_overrides_v1` — map `recipeId::ingredientIndex` → `{ zone?, orderQty?, included? }`.
- **Riviera order extras:** `kuschi_riviera_order_extras_v1` — manual lines from “Add ingredient” on the order list modal.
- **Riviera order list UI:** [riviera.html](riviera.html) + [assets/order-list.js](assets/order-list.js) — ingredients grouped **by storage zone** (not by recipe); per-line order qty, zone, include checkbox; **Remember for next time & add**; copy plain text, **Copy order data JSON** (`exportOrderBundle`), **Copy remembered ingredients (JSON)** (`exportMaster`). Recipe lines merge on **`canonicalOrderMergeKey(item)` only** (same name across zones becomes one row; listed under the majority zone; recipe hint prefixes by zone when amounts split). Canonical key: [assets/user-recipes.js](assets/user-recipes.js) — NFKC, `&`/dashes/punctuation, **`INGREDIENT_CANON_ALIASES`** (regex replacements), conservative per-token plural trim (`ies`→`y`, `oes`/`xes`/`ches`/`shes`, trailing `s`). Manual **order extras** with the same canonical name fold in if their zone appears in that merged row (sub-row for manual qty/remove; changing the parent row zone updates folded extras). Shared **order list** styles: [assets/theme.css](assets/theme.css) (`#orderListOverlay`, `#kbOrderListOverlay`).
- **Riviera stocktake catalog:** [riviera_data/stocktake_catalog.json](riviera_data/stocktake_catalog.json) (~365 built-in rows: zone, default qty/brand/UOM; `category` in JSON is for the generator only). [riviera.html](riviera.html) loads it on first stocktake open; [assets/stocktake-list.js](assets/stocktake-list.js) renders them after recipe/order rows, flat per zone A–Z by name; row ids `builtin:<id>` in `kuschi_riviera_stocktake_v1` `lines` override defaults. **Clear counted** removes `builtin:*` keys so defaults return. Regenerate data with `python3 scripts/generate_riviera_stocktake_data.py`.
- **Add recipe → Paste & format (Kitchen + Riviera):** [assets/recipe-gemini-format.js](assets/recipe-gemini-format.js), [assets/recipe-import-helpers.js](assets/recipe-import-helpers.js) — paste text, optional **PDF/image/DOCX** file, optional **recipe URL** (direct `fetch` when CORS allows, else optional **fetch proxy URL** in `localStorage`). Legacy `.doc` not supported. Gemini API key in `kuschi_gemini_api_key_v1`.
- **`removeRivieraRecipe(id)`** — removes one user-saved Riviera recipe from `kuschi_user_recipes_riviera_v1` (exposed on `KuschiUserRecipes`).
- **Casing on save:** [assets/user-recipes.js](assets/user-recipes.js) applies title case to names, ingredient lines, labels, etc.; method/service lines get a leading capital only; **yield** and **qty** strings are left as typed; **protein** / **tags** on the kitchen page stay lowercase for filters.
- **Backup:** Use JSON copy buttons in the UIs to paste into files and commit from a dev machine if desired.

## Riviera “Prep Chef” PDF vs built-ins (dedupe on add)

The house **Recipes for Prep Chef** PDF uses longer titles than the site cards. Saving a new Riviera recipe from the add modal runs **dedupe** so PDF-style names do not create a second copy of an existing built-in or an existing user-saved Riviera recipe.

- **Logic:** [assets/user-recipes.js](assets/user-recipes.js) — `normalizeRivieraNameForDedupe`, `coreRivieraNameForDedupe` (text before first ` with `), `findRivieraDuplicate(name, BUILTIN_RECIPES)`, optional third arg overrides the user list (defaults to `loadRiviera()`). Explicit `RIVIERA_PREP_CHEF_ALIAS_TO_ID` maps normalized PDF headings to built-in `id`.
- **Hook:** [riviera.html](riviera.html) `submitRivieraRecipe()` calls `findRivieraDuplicate` before `addRivieraRecipe`; on match, shows an alert and does not save.

| PDF-style title (concept) | Built-in `id` in `BUILTIN_RECIPES` |
|---------------------------|-------------------------------------|
| Chorizo and Mozzarella Arancini… | `arancini` |
| Calamari Fritti… | `calamari` |
| Kilpatrick Oyster… | `oysters-kilpatrick` |
| Slow Cooked Veal Meatballs… | `veal-meatballs` |
| Lemon Pepper Chicken Skewer with Tzatziki… | `chicken-skewer` (site card: Herbed Labneh) |
| Crispy Fried Chorizo Potatoes… | `chorizo-potatoes` |
| Chargrilled Lamb Cutlet… | `lamb-cutlet` |
| Crispy Reef Fish Slider… | `fish-slider` |
| Romesco | `romesco` |
| Lemon & Dill Aioli | `lemon-dill-aioli` |
| Lemon & Thyme Aioli | `lemon-thyme-aioli` |
| Vodka Sauce | `vodka-sauce` |
| Whipped Butter | `whipped-butter` |
| Riviera House Emulsion | `riviera-emulsion` |
| Camembert, Pecan & Cranberry Cigars… | `camembert-cigars` |
| Beef Kofta… | `beef-kofta` |

## Theme and units

- **Theme:** [.cursor/rules/theme.mdc](.cursor/rules/theme.mdc) — canonical shared styles live in [assets/theme.css](assets/theme.css).
- **Units:** [.cursor/rules/metric-units.mdc](.cursor/rules/metric-units.mdc).

## Git workflow

- See [.cursor/rules/git-workflow.mdc](.cursor/rules/git-workflow.mdc) and [.cursor/rules/git.md](.cursor/rules/git.md).

## Delivery status (hub note)

Phases 1–2: Cursor rules, hub skill, user recipes, Riviera modals, git workflow, title casing on save.  
Phase 3: `theme.css` + README refresh; Riviera order list by zone + master DB + JSON export; hub doc updates (this file).
