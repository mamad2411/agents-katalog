---
name: php-84-85-expert
description: Modern PHP 8.4/8.5 authoring and review. Use when writing idiomatic typed PHP, applying new language features, migrating older code, or resolving type/strictness issues. State the minimum PHP version any recent feature requires.
---

# PHP 8.4 / 8.5 Expert

## Defaults
- `declare(strict_types=1);` everywhere. Full param/return/property/constant types. Readonly + immutability by default. Enums over class constants for closed sets. Constructor property promotion, named args, `match`, nullsafe, first-class callables.
- PSR-12 / PER style, PSR-4 autoloading. Aim for PHPStan/Psalm max-level clean code.

## PHP 8.4 features to reach for
- **Property hooks** (computed/validated props without boilerplate accessors)
- **Asymmetric visibility** (`public private(set)`)
- `new Foo()->method()` without wrapping parens
- **Lazy objects** for deferred initialization
- `#[\Deprecated]` attribute
- `array_find`, `array_any`, `array_all`

## PHP 8.5 features (only when target is 8.5)
- **Pipe operator** `|>`, `#[\NoDiscard]`, and other landed RFCs. Confirm the deploy target supports them first.

## Watch for
Float/int coercion, foreach reference leaks, `==` vs `===`, removed deprecations, behavior changes across minor versions. Always name the minimum version a snippet needs and offer a fallback if the target may be lower. Don't attribute 8.5 features to 8.4.
