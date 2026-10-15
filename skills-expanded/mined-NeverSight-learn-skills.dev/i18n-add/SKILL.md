---
name: i18n-add
description: Add or update i18n strings in the frontend. Use whenever you add new user-visible text, a new namespace, or change an existing translation key.
---

# Adding i18n strings

The frontend uses `i18next` with `i18next-browser-languagedetector`.
Locale files live at `frontend/src/i18n/locales/{en,fr}/<namespace>.json`.

## Namespaces

Current namespaces (one JSON file each per locale):

- `common` — verbs (`save`, `cancel`, `delete`), unit labels, errors
- `recipes` — recipe CRUD + import strings
- `shopping` — shopping list strings
- `admin` — admin user/ingredient management
- `settings` — user settings + delete account
- `auth` — login / signup / password recovery
- `dashboard` — dashboard widgets
- `navigation` — sidebar + nav

## Rules

1. **Both locales, always.** Every new key must land in `en` and `fr`
   in the same commit. CI does not currently catch missing keys, but
   the UI will fall back to the key name (visible as `recipes.add.button`
   instead of "Add recipe").

2. **Use the right namespace.** Component code declares one or more
   namespaces:
   ```tsx
   const { t } = useTranslation("recipes")
   const { t: tCommon } = useTranslation("common")
   ```
   Prefer `tCommon` for cross-feature strings.

3. **Unit labels are in `common`.** Read units via
   `tCommon(\`unit_labels.${u}\`, { defaultValue: u })`. The keys exist
   for every `UnitSchema.enum` value.

4. **Interpolation uses i18next's `{{var}}` syntax.**
   ```json
   { "items_count": "{{checked}}/{{total}} items" }
   ```
   ```tsx
   t("card.items_count", { checked: 3, total: 7 })
   ```

5. **Pluralization** uses i18next's `_one` / `_other` keys when needed:
   ```json
   {
     "recipes_count_one": "{{count}} recipe",
     "recipes_count_other": "{{count}} recipes"
   }
   ```
   Call with `t("recipes_count", { count: 3 })`.

## Workflow

1. Add the key to `frontend/src/i18n/locales/en/<namespace>.json`.
2. Add the same key with the French translation to
   `frontend/src/i18n/locales/fr/<namespace>.json`.
3. Use `t("…")` / `tCommon("…")` in the component.
4. Verify in the browser by toggling language: Chrome
   Settings → Languages → "Display Google Chrome in this language".

## Brand voice

Keep English warm and home-centric (see `VISUAL_IDENTITY.md`). French
uses standard culinary terminology — never machine-translate; use
human-quality French.
