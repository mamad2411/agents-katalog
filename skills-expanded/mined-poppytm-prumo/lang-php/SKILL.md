---
name: lang-php
description: PHP 8.2+ strict types (declare(strict_types=1)), PHPStan at maximum strictness, PDO prepared statements, and secure password hashing.
---

# PHP Strict Types & Static Analysis Contract

## 1. Strict Typing
- Every PHP file must begin with `declare(strict_types=1);`.
- All class properties, method parameters, and returns must have explicit native types.
- Prohibit error suppression operator `@`.

## 2. Database & SQL Security
- All database queries must use prepared statements with bound parameters (`PDO::prepare`).
