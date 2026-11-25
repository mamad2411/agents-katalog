---
name: s2-publishing-domain
description: Book publishing domain knowledge including ISBN, BISAC codes, and industry pricing standards.
user-invocable: false
---

# S2 — Publishing Domain Knowledge

Background knowledge for the book publishing domain. This skill is loaded
automatically by Claude when relevant — it is NOT available as a slash command.

## ISBN-13 Validation (Full Algorithm)

ISBN-13 is a 13-digit identifier. The last digit is a **check digit** computed as:

1. Take the first 12 digits
2. Multiply each digit alternately by **1** and **3** (positions 0-11)
3. Sum all products
4. Check digit = `(10 - (sum % 10)) % 10`

Example: ISBN `9780306406157`
- Digits: 9,7,8,0,3,0,6,4,0,6,1,5,7
- Weights: 1,3,1,3,1,3,1,3,1,3,1,3
- Products: 9,21,8,0,3,0,6,12,0,18,1,15
- Sum: 93
- Check: (10 - (93 % 10)) % 10 = (10 - 3) % 10 = 7 ✓

**Important**: The regex-only validation in `utils/validators.py` is incomplete.
When asked to improve ISBN validation, implement the full check digit algorithm above.

Valid prefixes: `978` (most books) or `979` (overflow and some music).

## BISAC Subject Codes

BISAC (Book Industry Standards and Advisory Committee) codes categorize books:
- Format: 3-letter category + 6-digit number (e.g., `FIC000000`)
- Common prefixes: `FIC` (Fiction), `NON` (Nonfiction), `JUV` (Juvenile),
  `YAF` (Young Adult Fiction), `COM` (Computers), `SCI` (Science)
- The `000000` suffix means "General" within that category

## Pricing Conventions

- Always store prices in **cents** (integer) to avoid floating-point errors
- Display format: `$XX.99` (US convention)
- Common price points: $9.99, $14.99, $24.99, $29.99
- Ebooks typically 30-50% less than physical edition

## Library of Congress Classification (Basics)

- Single letter = broad class (e.g., P = Language and Literature)
- Letter + subclass (e.g., PS = American Literature)
- Used for shelving in academic/research libraries
- Different from Dewey Decimal (used in public libraries)
