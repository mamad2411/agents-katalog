---
name: kendo-ui-localization
description: Use when Kendo UI components must support localization and globalization including culture-aware formatting, message packs, RTL behavior, and locale regression validation.
---

# Kendo UI Localization

## Specialization

Implement and review Kendo UI localization and globalization behavior, including runtime culture switching, localized component text, date/number formatting, and right-to-left layout correctness.

## Trigger Conditions

- Product supports multiple locales.
- Date, number, or currency formatting differs by culture.
- Kendo component messages need translation.
- RTL layouts are required for target locales.
- Locale-specific regressions appear after upgrades.

## Scope Boundaries

In scope:

- Culture script loading and selection strategy.
- Component message localization setup.
- Locale-aware formatting for Grid, DatePicker, and numeric widgets.
- RTL behavior checks for major components.
- Locale regression checklist across supported markets.

Out of scope:

- Product copywriting governance.
- Backend translation workflow tooling.
- Generic accessibility policy beyond locale-specific checks.

## Inputs

- Supported locale list and fallback rules.
- Culture formatting requirements.
- Translation source for Kendo messages.
- Target components and RTL requirements.

## Required Outputs

- Locale initialization contract with fallback handling.
- Component message localization mapping.
- Formatting validation matrix for date/number/currency.
- RTL compatibility checklist for affected widgets.
- Regression plan for locale switch and persisted user preference.

## Core Patterns

### Culture Initialization

```javascript
kendo.culture("fr-FR");

$("#amount").kendoNumericTextBox({
    format: "c",
    decimals: 2
});
```

### Runtime Locale Switch

```javascript
function applyLocale(cultureCode) {
    kendo.culture(cultureCode);
    refreshLocalizedWidgets();
}
```

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Enable one non-default locale | Core formatting behaves correctly |
| L2 Delivery | Support full locale set with fallback | Message and format mappings complete |
| L3 Hardening | Include RTL and regression validation | Locale matrix passes without blockers |
| L4 Expert | Standardize localization architecture | Reusable locale governance contract exists |
