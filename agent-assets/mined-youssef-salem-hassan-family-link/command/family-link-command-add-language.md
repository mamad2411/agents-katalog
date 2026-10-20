# Add / update localization (Family-Link)

Manage ARB-based strings for **`family_link`**.

## When to use

- New copy, new keys, or new locale
- User says "translate", "localize", `l10n`, ARB

## Steps

1. Edit **`lib/l10n/arb/app_en.arb`**
2. Edit **`lib/l10n/arb/app_ar.arb`** (same keys)
3. Run **`flutter gen-l10n`**
4. Use **`context.l10n.yourKey`** in widgets

Optional deep docs: **`tech_readme_files/2_development/LOCALIZATION_IMPLEMENTATION.md`**

## Rules

- No hard-coded user-facing strings in **`lib/`** — use ARB + **`context.l10n`**
- Key names: **`camelCase`**, meaningful, feature-prefixed when ambiguous
