---
applyTo:
  - '**/*.php'
description: |
  PHP 8.3+ development standards for ICTServe project.
  Enforces strict typing, modern syntax, PSR-12/PER compliance, and
  clean object-oriented design patterns.
tags:
  - php
  - backend
  - standards
  - psr
  - type-safety
version: '1.0.0'
lastUpdated: '2025-02-24'
---

# PHP — ICTServe Language Standards

## Overview

This rule defines the core PHP language standards for the ICTServe project. While Laravel provides the framework, the underlying PHP code must adhere to modern standards (PHP 8.3+) to ensure type safety, readability, and performance.

| Attribute | Value |
| :--- | :--- |
| **Language Version** | PHP 8.3 / 8.4 (Active Support) |
| **Applies To** | All backend logic (`app/`, `config/`, `database/`, `routes/`) |
| **Traceability** | D17 (Backend Code Quality), D18 (Security Standards) |
| **Coding Style** | PSR-12 / PER Coding Style (via Laravel Pint) |

## Core Principles

1. **Strict Typing**: Every file must declare `strict_types=1`.
2. **Type Hints**: explicit type declarations for all properties, arguments, and return values.
3. **Modern Syntax**: Prefer constructor promotion, `match` expressions, and `readonly` classes.
4. **Composition**: Prefer composition and traits over deep inheritance hierarchies.
5. **Attributes**: Use native PHP Attributes (`#[Attribute]`) over PHPDoc annotations.

## Modern PHP Features (8.3 & 8.4)

### Property Hooks (PHP 8.4)
Use property hooks to reduce boilerplate for getters and setters.

```php
// Old Way
private string $name;
public function getName(): string { return $this->name; }
public function setName(string $value): void { 
    if (strlen($value) === 0) throw new ValueError();
    $this->name = $value; 
}

// New Way (Preferred)
public string $name {
    get => $this->name;
    set {
        if (strlen($value) === 0) throw new ValueError();
        $this->name = $value;
    }
}
````

### Typed Class Constants

Always type constants to prevent accidental type coercion.

```php
class Status
{
    public const string PENDING = 'pending';
    public const int TIMEOUT = 30;
}
```

### The `#[Override]` Attribute

Always use `#[Override]` when implementing an interface method or overriding a parent method to catch typos during development.

```php
class AssetController extends Controller
{
    #[Override]
    public function authorize(string $ability, mixed $arguments = []): Response
    {
        // Custom logic
    }
}
```

## Type Safety Standards

### Strict Types Declaration

**Every** PHP file must start with strict types declaration. This prevents PHP from silently coercing types (e.g., passing "1" string into an integer requirement).

```php
<?php

declare(strict_types=1);

namespace App\Services;
```

### Type Hinting

Do not leave types to chance. Use `mixed` only as a last resort.

```php
// BAD
public function calculate($amount, $tax)
{
    return $amount + $tax;
}

// GOOD
public function calculate(float $amount, float|null $tax = null): float
{
    return $amount + ($tax ?? 0.0);
}
```

### Union and Intersection Types

Use native union types instead of PHPDoc `@var`.

```php
// BAD: PHPDoc dependency
/** @var User|null */
private $user;

// GOOD: Native Union
private User|null $user;

// GOOD: Intersection (Object must satisfy both)
public function setLogger(Logger&Countable $logger): void
{
    // ...
}
```

## Class Structure

### Constructor Property Promotion

Reduce boilerplate by defining properties in the constructor.

```php
// BAD
class CreateAssetDTO
{
    public string $name;
    public string $tag;

    public function __construct(string $name, string $tag)
    {
        $this->name = $name;
        $this->tag = $tag;
    }
}

// GOOD
class CreateAssetDTO
{
    public function __construct(
        public string $name,
        public string $tag,
    ) {}
}
```

### Readonly Classes

Use `readonly` classes for Data Transfer Objects (DTOs) and Value Objects.

```php
readonly class AssetData
{
    public function __construct(
        public string $name,
        public string $status,
        public ?DateTimeImmutable $acquiredAt,
    ) {}
}
```

### Enums

Use Enums instead of string constants or simple arrays for fixed lists of values.

```php
enum AssetStatus: string
{
    case AVAILABLE = 'available';
    case BORROWED = 'borrowed';
    case MAINTENANCE = 'maintenance';

    public function label(): string
    {
        return match($this) {
            self::AVAILABLE => 'Tersedia',
            self::BORROWED => 'Dipinjam',
            self::MAINTENANCE => 'Penyelenggaraan',
        };
    }
}
```

## Control Structures

### Match Expression

Prefer `match` over `switch`. `match` is an expression (returns a value), does strict comparison (`===`), and throws an exception on unhandled values.

```php
// BAD (Switch)
switch ($status) {
    case 'active':
        $color = 'green';
        break;
    case 'pending':
        $color = 'yellow';
        break;
    default:
        $color = 'gray';
}

// GOOD (Match)
$color = match ($status) {
    'active' => 'green',
    'pending' => 'yellow',
    default => 'gray',
};
```

### Named Arguments

Use named arguments when a function has many parameters, boolean flags, or when skipping optional defaults.

```php
// BAD: What do these booleans mean?
set_cookie('session', $id, 0, '/', '', true, true);

// GOOD
set_cookie(
    name: 'session',
    value: $id,
    secure: true,
    httponly: true,
);
```

## Null Handling

### Null Coalescing Assignment

Use `??=` to assign values if the variable is null.

```php
// BAD
if (!isset($config['timeout'])) {
    $config['timeout'] = 30;
}

// GOOD
$config['timeout'] ??= 30;
```

### Null Safe Operator

Use `?->` to access properties on objects that might be null.

```php
// BAD
$country = null;
if ($user !== null && $user->address !== null) {
    $country = $user->address->country;
}

// GOOD
$country = $user?->address?->country;
```

## Arrays and Iteration

### Array Destructuring

Use short syntax `[]` and destructuring for cleaner array handling.

```php
$data = ['John', 'Doe', 'john@example.com'];

// Destructuring
[$firstName, $lastName, $email] = $data;

// Inside loops
foreach ($users as ['id' => $id, 'name' => $name]) {
    // ...
}
```

### Array Unpacking

Use `...` to merge arrays.

```php
$default = ['a' => 1, 'b' => 2];
$new = ['b' => 3, 'c' => 4];

// Standard merge
$merged = [...$default, ...$new]; 
// Result: ['a' => 1, 'b' => 3, 'c' => 4]
```

## References and Resources

* **PHP Manual**: [https://www.php.net/docs.php](https://www.php.net/docs.php)
* **PHP 8.3 Release**: [https://www.php.net/releases/8.3/en.php](https://www.php.net/releases/8.3/en.php)
* **PHP 8.4 Release**: [https://www.php.net/releases/8.4/en.php](https://www.php.net/releases/8.4/en.php)
* **PHP-FIG (PSR-12/PER)**: [https://www.php-fig.org/psr/psr-12/](https://www.php-fig.org/psr/psr-12/)
* **Laravel Pint**: [https://laravel.com/docs/pint](https://laravel.com/docs/pint)

## Compliance Checklist

When writing PHP code for ICTServe, ensure:

* [ ] File begins with `declare(strict_types=1);`.
* [ ] No `switch` statements; use `match` expressions.
* [ ] All method arguments and return types are strictly typed.
* [ ] Use `readonly` classes for DTOs.
* [ ] Use `enum` for status/category fields.
* [ ] Use Named Arguments for functions with \>3 parameters or boolean flags.
* [ ] Use Constructor Property Promotion for simple data classes/models.
* [ ] Use `CarbonImmutable` or `DateTimeImmutable` for dates (never mutable).
* [ ] Use `#[Override]` attribute when overriding parent methods.
* [ ] Avoid `else` blocks by using early returns (`guard clauses`).

| Field | Value |
| :--- | :--- |
| **Status** | Active for ICTServe PHP development |
| **Version** | 1.0.0 |
| **Last Updated** | 2025-02-24 |
