---
name: php-patterns
description: "When to activate: idiomatic PHP, PHP 8.3, readonly properties, enums, match expression, attributes, named arguments, nullsafe operator, first-class callables, strict_types"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: php
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# PHP Patterns

## When to Use

Writing or reviewing modern PHP (8.1+) code: value objects, domain models, framework-agnostic services, or any PHP file that should use current language features instead of PHP 5/7 idioms.

## Core Patterns

### Strict Types and Typed Properties

Always declare `strict_types` and type every property, parameter, and return value.

```php
<?php

declare(strict_types=1);

final class Money
{
    public function __construct(
        public readonly int $amountCents,
        public readonly string $currency,
    ) {
    }

    public function add(Money $other): self
    {
        if ($this->currency !== $other->currency) {
            throw new InvalidArgumentException('Currency mismatch');
        }

        return new self($this->amountCents + $other->amountCents, $this->currency);
    }
}
```

### Enums Instead of Class Constants

```php
enum OrderStatus: string
{
    case Pending = 'pending';
    case Shipped = 'shipped';
    case Cancelled = 'cancelled';

    public function isTerminal(): bool
    {
        return match ($this) {
            self::Shipped, self::Cancelled => true,
            self::Pending => false,
        };
    }
}

$status = OrderStatus::from($request->get('status'));
```

### match() Over switch

`match` is an expression, uses strict comparison, and has no fallthrough.

```php
$discount = match (true) {
    $total >= 10_000 => 0.15,
    $total >= 5_000  => 0.10,
    $total >= 1_000  => 0.05,
    default          => 0.0,
};
```

### Readonly Value Objects

Prefer immutable value objects over mutable DTOs — build a new instance instead of setters.

```php
final class Address
{
    public function __construct(
        public readonly string $street,
        public readonly string $city,
        public readonly string $postalCode,
    ) {
    }

    public function withCity(string $city): self
    {
        return new self($this->street, $city, $this->postalCode);
    }
}
```

### Nullsafe and First-Class Callables

```php
// Nullsafe chaining — short-circuits to null instead of throwing
$city = $order?->customer?->address?->city;

// First-class callable syntax (PHP 8.1+) instead of string/array callables
$mapped = array_map(strtoupper(...), $names);
$validator = $this->validateEmail(...);
```

### Attributes Instead of Docblock Annotations

```php
#[Route('/orders/{id}', methods: ['GET'])]
final class ShowOrderController
{
    public function __invoke(#[CurrentUser] User $user, string $id): Response
    {
        // ...
    }
}
```

## Checklist

- [ ] `declare(strict_types=1)` at the top of every file
- [ ] All classes `final` unless explicitly designed for extension
- [ ] Constructor property promotion used instead of manual assignment
- [ ] Value objects are `readonly`
- [ ] No `array` type hints where a typed DTO/enum would be clearer
- [ ] `match` used instead of `switch` for value mapping
- [ ] Named arguments used for functions with 3+ parameters of the same type

## Anti-Patterns

```php
// BAD: mutable public properties, no types
class User {
    public $name;
    public $email;
}

// GOOD: readonly, typed, validated at construction
final class User
{
    public function __construct(
        public readonly string $name,
        public readonly string $email,
    ) {
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            throw new InvalidArgumentException("Invalid email: {$email}");
        }
    }
}
```

```php
// BAD: array as ad-hoc struct
function createOrder(array $data): array { /* ... */ }

// GOOD: typed input/output
function createOrder(CreateOrderRequest $request): Order { /* ... */ }
```

## Quick Reference

| Feature | Minimum PHP | Use For |
|---|---|---|
| `readonly` properties | 8.1 | Immutable value objects |
| Enums | 8.1 | Fixed sets of values instead of constants |
| `never` return type | 8.1 | Functions that always throw/exit |
| Intersection types | 8.1 | `Countable&Iterator` style constraints |
| `readonly` classes | 8.2 | Whole-class immutability shorthand |
| Typed class constants | 8.3 | `const int MAX = 10;` |

## See Also

- `skills/php-ecosystem/laravel-patterns.md`
- `skills/php-ecosystem/php-testing.md`
- `skills/php-ecosystem/php-security.md`
