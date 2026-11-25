---
name: piwigo-plugin-engineering
description: Piwigo plugin integration guidance. Use when working on Piwigo plugins, main.inc.php, maintain.inc.php, plugin admin pages, Smarty .tpl files, Piwigo events/actions, language catalogs, plugin upgrades, or plugin-owned PHP, HTML, CSS, JavaScript, or TypeScript. Do not use for generic PHP, frontend, localization, SQL, security, or browser-test mechanics outside a Piwigo host integration; load the owning skill with this one.
---

# Piwigo Plugin Engineering

## Use When

Use for Piwigo host integration and plugin lifecycle work. Compose with [`php-engineering`](../php-engineering/SKILL.md), [`javascript-typescript-engineering`](../javascript-typescript-engineering/SKILL.md), [`css-scss-styling`](../css-scss-styling/SKILL.md), [`internationalization-localization`](../internationalization-localization/SKILL.md), [`security-review`](../security-review/SKILL.md), applicable SQL skills, and [`php-testing-quality`](../php-testing-quality/SKILL.md) rather than duplicating their mechanics.

## Repository And Host Discovery

Start every workflow by discovering the target Piwigo release, supported PHP range, incumbent plugin, core event/API usage, plugin metadata, asset pipeline, Smarty conventions, localization layout, database adapter, and existing test/deployment fixture. The legacy tutorial below is architectural evidence only: confirm target-version APIs before copying event names, database helpers, asset registration, or lifecycle signatures.

## Plugin Lifecycle

Keep host-compatible entry guards. Keep `main.inc.php` bootstrap-only. Place install, activate, upgrade, deactivate, and uninstall transitions in the target release’s maintenance mechanism, including `maintain.inc.php` where the target version uses it. Make upgrades idempotent and preserve user data unless an explicit uninstall policy says otherwise.

## Hooks, Events, And Entry Points

Register behavior through supported Piwigo events/actions instead of core patches. Namespace or uniquely prefix global symbols. The following is schematic legacy syntax, not a current API contract; replace both placeholders from the target Piwigo source/version before implementation:

```php
add_event_handler('<verified-event>', '<uniquely-prefixed-handler>');
```

Do not name a current event, asset helper, database helper, or maintenance class without target-version evidence.

## Host Compatibility

Treat the plugin metadata’s Piwigo and PHP support promises as test obligations. Do not assume core APIs, Smarty behavior, database adapters, assets, or maintenance signatures are stable across host releases. Test each promised Piwigo/PHP combination with a real supported fixture when compatibility metadata makes the promise.

## PHP, Smarty, HTML, CSS, And JavaScript Composition

PHP validates authorization, CSRF, input, domain behavior, and persistence. Presenters assign escaped, localization-ready view data. Smarty/HTML owns semantic markup; CSS owns presentation; JavaScript/TypeScript progressively enhances through finite `data-*`, JSON, or supported API contracts. Do not interpolate raw PHP or Smarty values into executable JavaScript. Use context-aware escaping and target-version asset-loading conventions.

## Localization

Discover the host catalog paths, translation helpers, and Smarty integration for the target release. Keep message design, formatting, fallback, bidi, pseudolocalization, and localization testing in [`internationalization-localization`](../internationalization-localization/SKILL.md); this skill owns Piwigo catalog layout, helper integration, and compatibility.

## Database And Security Routing

Use the target-version database adapter and route schema/query design to the applicable SQL skill. Use [`security-review`](../security-review/SKILL.md) for admin and event-handler authorization, CSRF, request validation, templates, uploads, paths, deserialization, outbound requests, secrets, and exception/log disclosure.

## Test Levels

Unit-test plugin policy without the host. Integration-test event registration/handler behavior, permissions, localization, templates, database changes, and install/upgrade/uninstall against a real supported Piwigo fixture. Browser-test admin and gallery workflows through public UI with [`playwright-e2e`](../playwright-e2e/SKILL.md). Use [`digital-asset-management`](../digital-asset-management/SKILL.md) for media-catalog domain changes.

## Completion Checklist

- Target Piwigo release, PHP range, and host APIs are evidenced.
- No core patch or unverified lifecycle/hook signature is introduced.
- Bootstrap, maintenance, namespacing, data preservation, templates/assets, catalogs, and permissions follow target conventions.
- Declared compatibility combinations and user-visible workflows have proportionate verification.

## References

- Piwigo wiki: <https://github.com/Piwigo/Piwigo/wiki> — consulted 2026-08-17; discover target-version source/docs before implementation.
- [Piwigo Plugin Tutorial: Hello world!](https://raw.githubusercontent.com/wiki/Piwigo/Piwigo/Plugin-Tutorial:-Hello-world!.md) — legacy architectural evidence, consulted 2026-08-17; not authoritative for current signatures.
