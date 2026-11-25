---
name: php-essentials
description: Use when writing any PHP — strict types, readonly classes, enums, property hooks, attributes, the rules you don't break.
metadata:
  added: 2026-05-23
  last_reviewed: 2026-05-23
  type: language
  languages: [php]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-23"
  related: [php-composer, php-symfony, security]
---

# PHP essentials

**Iron Law: `declare(strict_types=1);` is the first line of EVERY file — no exceptions. Without it, PHP coerces `"1"` to `1`, `null` to `0`, `"abc"` to a TypeError-that-isn't, and your type hints become decorative. Strict types turn the engine into a type checker. Everything else here is downstream of that.**

**Versions:** PHP `8.5` (GA Nov 2025) · `8.4` still actively supported (security through 2028). 8.4 added property hooks + asymmetric visibility; 8.5 added the pipe operator `|>`, `#[\NoDiscard]`, closures in constant expressions, and `array_first()`/`array_last()`. Target 8.4 as the floor unless you control the runtime — then 8.5.

## The Iron Law in practice

```php
<?php

declare(strict_types=1);   // FIRST executable line, every file, always

namespace App\Order;       // PSR-4: namespace mirrors directory under the root

function total(int $qty, float $price): float
{
    return $qty * $price;   // passing "3" here is a TypeError, not a silent "3"→3
}
```

PSR-4: one class per file, named `ClassName.php`, namespace prefix maps to a `composer.json` `autoload.psr-4` root (`App\` → `src/`). No `require` of class files — the autoloader resolves them. See `Skill(devkit:php-composer)`.

## readonly + constructor property promotion

```php
final class Money
{
    public function __construct(
        public readonly int $cents,        // promoted: declares + assigns the property,
        public readonly string $currency, // readonly: write-once in ctor, then frozen
    ) {}

    public function add(Money $o): self     // mutation returns a NEW instance
    {
        return new self($this->cents + $o->cents, $this->currency);
    }
}

readonly class Point { public function __construct(public float $x, public float $y) {} }
// 8.2+ whole-class readonly: every property readonly, no dynamic props
```

Promotion kills the `private $repo;` + `$this->repo = $repo;` boilerplate — promote every constructor-injected dependency, and combine with `readonly` so injected deps never change after wiring. A `readonly class` is the default shape for DTOs and value objects — data that crosses a boundary should be immutable.

## Enums — replace string/int constants and array-of-magic-values

```php
enum Status: string                      // backed enum — has a scalar value
{
    case Pending = 'pending';
    case Paid    = 'paid';
    case Refunded = 'refunded';

    public function isFinal(): bool       // enums carry methods
    {
        return match ($this) {
            self::Paid, self::Refunded => true,
            self::Pending => false,
        };
    }

    public function label(): string { return ucfirst($this->value); }
}

Status::from('paid');        // → Status::Paid; throws ValueError on unknown
Status::tryFrom('nope');     // → null, no throw — use at trust boundaries
Status::cases();             // → [Pending, Paid, Refunded]
```

Enums implement interfaces and hold constants (`const Default = self::Pending;`). A backed enum where you'd otherwise scatter `'pending'` string literals is non-negotiable. Pure (unbacked) enums for closed sets with no wire representation.

## PHP 8.4 property hooks + asymmetric visibility

```php
class Temperature
{
    public function __construct(private float $celsius) {}

    public float $fahrenheit {                      // virtual property via hooks
        get => $this->celsius * 9 / 5 + 32;
        set (float $f) => $this->celsius = ($f - 32) * 5 / 9;
    }

    public string $name {
        set => trim($value);                        // validate/normalize on write; $value is implicit
    }
}

class Account
{
    public private(set) int $balance = 0;   // public read, private write — no getter boilerplate
}
```

Property hooks replace most trivial getters/setters: a `get` hook computes, a `set` hook normalizes/validates. Asymmetric visibility (`public private(set)`, `protected private(set)`) exposes reads while locking writes to the class — encapsulation without a getter method. Prefer hooks over a `getX()`/`setX()` pair when the logic is a single expression.

## match vs switch

```php
$rate = match ($tier) {                  // strict (===) comparison, expression, exhaustive
    Tier::Free      => 0.0,
    Tier::Pro, Tier::Team => 0.2,        // multi-value arm
    default         => throw new \UnhandledMatchError(),  // or omit → engine throws
};
```

`match` is an expression (returns a value), uses `===` (no `"0" == 0` traps), and throws `UnhandledMatchError` on a miss — no silent fall-through. `switch` uses `==`, needs `break`, and falls through on the slightest slip. Use `match`; reach for `switch` only when an arm needs multiple statements that don't factor into a method.

## Types: union, intersection, DNF, never/true/false, nullsafe

```php
function find(int|string $id): User|null { /* ... */ }        // union
function wrap(Countable&ArrayAccess $c): void { /* ... */ }   // intersection
function pick((A&B)|C $x): void { /* ... */ }                 // DNF (8.2+)

function fail(string $m): never { throw new \RuntimeException($m); }  // never returns

$name = $order?->customer?->name;        // nullsafe: short-circuits to null, no fatal
```

`never` for functions that always throw/exit (the type checker prunes the branch). `true`/`false` as standalone return types for predicate-shaped APIs. `?Type` is shorthand for `Type|null`. DNF combines unions of intersections. Nullsafe `?->` beats nested `isset()` ladders.

## First-class callables + named arguments

```php
$fn = strlen(...);                       // first-class callable syntax → Closure
$up = $repo->find(...);                  // bound to instance
array_map(strtoupper(...), $words);      // no string "strtoupper", no [$obj,'m'] tuple

new HttpClient(timeout: 5, retries: 3);  // named args: order-free, self-documenting
str_replace(subject: $s, search: $a, replace: $b);   // skip-positional clarity
```

`$fn(...)` produces a real `Closure` with the original signature — type-safe, refactor-safe, no stringly-typed callable arrays. Named arguments make multi-flag calls readable and let you skip optional params without positional `null` padding.

## Attributes — structured metadata, not docblock parsing

```php
#[\Attribute(\Attribute::TARGET_METHOD)]
final class Route
{
    public function __construct(public string $path, public string $method = 'GET') {}
}

final class Controller
{
    #[Route('/users/{id}', method: 'GET')]
    public function show(int $id): Response { /* ... */ }
}
// read via Reflection: $ref->getAttributes(Route::class)[0]->newInstance();
```

Attributes are first-class, type-checked metadata read through Reflection — Symfony routing, Doctrine mappings, validation all use them. Stop parsing `@annotations` from docblocks.

## Exceptions — typed, specific, never swallowed

```php
final class OrderNotFoundException extends \RuntimeException {}

try {
    $order = $repo->getOrThrow($id);
} catch (OrderNotFoundException $e) {     // catch the SPECIFIC type
    return $this->notFound($e->getMessage());
}
```

Throw domain-specific exception classes, not bare `\Exception`. Catch the narrowest type that matters. Never `catch (\Throwable) {}` to silence — that's the `@` operator in disguise.

## Fibers

Fibers (8.1+) are the low-level primitive under cooperative concurrency — you almost never touch them directly. ReactPHP/Amp/Revolt build the event loop on top. For async patterns and runtimes, that belongs in a dedicated async skill, not here.

## Anti-patterns

- Missing `declare(strict_types=1)` — the single biggest source of silent coercion bugs; add it everywhere
- `@`-prefixed error suppression (`@file_get_contents(...)`) — hides the failure AND the next 10; check the return, handle it
- `mixed` typed everywhere — defeats the type system; narrow to a union or a DTO
- Associative array as an ad-hoc record (`$user['naem']` typo, no IDE help) — use a `readonly` class or enum
- `switch` for value-returning logic — use `match` (strict, exhaustive, expression)
- Stringly-typed callables (`'strtoupper'`, `[$o, 'm']`) — use `$fn(...)`
- `== ` where `===` is meant — `0 == "abc"` traps; strict comparison always
- Magic string/int constants scattered across the codebase — back them with an enum
- `catch (\Exception $e) {}` empty body — swallowed errors; log + rethrow or handle

## Red flags

| Thought                                       | Reality                                                                          |
| --------------------------------------------- | -------------------------------------------------------------------------------- |
| "strict_types is overkill for a small file"   | small files grow; the coercion bug ships either way — it's one line, add it      |
| "I'll just return an array of fields"         | an array has no type, no autocomplete, no validation — that's a DTO/enum's job   |
| "`@` quiets the warning, ship it"             | it quiets THIS warning and every future one on that call; the bug is still there |
| "getters/setters for everything"              | 8.4 property hooks + asymmetric visibility kill the boilerplate — use them       |
| "`mixed` because the input could be anything" | it can't — enumerate it as a union, or validate to a known type at the boundary  |

## Hand-off

For dependency management, autoloading, version constraints, and repositories: `Skill(devkit:php-composer)`. For the Symfony framework (DI, controllers, attribute routing, Doctrine): `Skill(devkit:php-symfony)`. For input validation, injection, auth, and supply chain: `Skill(devkit:security)`.
