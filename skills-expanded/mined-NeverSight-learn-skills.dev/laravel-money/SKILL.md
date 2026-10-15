---
name: laravel-money
description: "Use the cknow/laravel-money package for Laravel projects that need to model, persist, cast, format, compare, or calculate money safely. Trigger when working on Laravel apps that handle currency, prices, totals, invoices, billing, checkout, discounts, taxes, balances, monetary casts, or any request mentioning money handling, currency formatting, integer minor units, Money value objects, or 'laravel-money'. Prefer this over raw floats for monetary values in Laravel." 
compatible_agents:
  - claude-code
  - cursor
  - windsurf
  - github-copilot
tags:
  - laravel
  - php
  - money
  - currency
  - billing
---

Use **`cknow/laravel-money`** whenever a Laravel project needs money handling.

## Core rule
Never use raw floats for money in application logic.
Prefer:
- integer minor units in storage when possible
- `Money` value objects in code
- explicit currency handling
- Laravel casts / helpers from `laravel-money`

## Install
```bash
composer require cknow/laravel-money
php artisan vendor:publish --provider="Cknow\Money\MoneyServiceProvider"
```

## Use when
- storing prices, totals, balances, fees, taxes, discounts
- formatting money in views / APIs
- casting Eloquent attributes to money
- converting user input into safe money values
- comparing or adding/subtracting money amounts
- avoiding float rounding bugs in Laravel billing flows

## Default guidance
- Store money consistently; prefer smallest units or a clearly documented decimal strategy.
- Always track currency explicitly.
- Avoid mixing currencies silently.
- Do calculations on money objects, not formatted strings.
- Format only at presentation boundaries.

## Common patterns

### Eloquent cast
```php
use Cknow\Money\Casts\MoneyIntegerCast;

protected $casts = [
    'price' => MoneyIntegerCast::class,
];
```

### Create money value
```php
use Cknow\Money\Money;

$price = Money::USD(1999); // $19.99 in minor units when using integer strategy
```

### Arithmetic
```php
$total = $subtotal->add($tax)->subtract($discount);
```

### Formatting
```php
$price->format();
```

## Read references when needed
- Read `references/patterns.md` for installation, model casts, storage choices, request handling, and API/view patterns.
- Read `references/checklist.md` when reviewing an existing Laravel codebase for money bugs.

## Review checklist
- Are floats used for prices or totals?
- Is currency explicit?
- Are calculations done on money objects instead of raw numbers?
- Are DB columns and casts consistent?
- Is formatting deferred until output?
- Are mixed-currency operations prevented or explicit?
