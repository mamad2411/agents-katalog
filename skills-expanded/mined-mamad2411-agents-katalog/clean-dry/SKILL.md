---
name: clean-dry
description: Use when writing, fixing, editing, or refactoring code with duplicated logic, copy-pasted blocks, or repeated patterns in any programming language. Enforces the DRY principle (Don't Repeat Yourself)—single source of truth, extract shared logic, no WET code.
---

# Clean DRY

## When to Use

Use this skill when writing, fixing, editing, or refactoring code in any programming language.

Also trigger on: copy-pasted blocks, near-identical functions differing by one value, repeated validation/error-handling patterns, duplicated constants or magic numbers, parallel class hierarchies with the same shape, or asks like "this is duplicated", "refactor to remove repetition", "DRY this up".

## Instructions

### D1: Extract Repeated Logic

If the same logic appears twice or more, extract it into a single named function. Duplication is the #1 source of drift—the second copy will be fixed, the third won't.

```text
# Bad - same validation in two places
function saveUser(user):
  if isBlank(user.email): throw "Email required"
  ...

function updateUser(user):
  if isBlank(user.email): throw "Email required"
  ...

# Good - single source of truth
function validateUser(user):
  if isBlank(user.email): throw "Email required"

function saveUser(user):
  validateUser(user)
  ...

function updateUser(user):
  validateUser(user)
  ...
```

### D2: Parameterize, Don't Copy

Two functions that differ only by a value are one function with a parameter.

```text
# Bad - copy-paste with one value changed
function sendWelcomeEmail(user): sendEmail(user, "welcome")
function sendInvoiceEmail(user): sendEmail(user, "invoice")

# Good - one function, one parameter
function sendEmail(user, template):
  ...
```

### D3: Single Source of Truth for Data

Constants, config values, schema definitions, and business rules live in exactly one place. Derive everything else from it.

```text
# Bad - the limit is defined three times
if items.length > 100: ...
MAX_ITEMS = 100
<max>100</max>

# Good - one definition, referenced everywhere
MAX_ITEMS = 100
if items.length > MAX_ITEMS: ...
```

### D4: Beware of Duplication by Abstraction

Merging duplicated code into a wrong abstraction is worse than the duplication. When you extract, the shared behavior must be genuinely identical—same inputs, same outputs, same failure modes. If the cases differ semantically, keep them separate and extract only the truly common sub-steps.

```text
# Bad - forced abstraction that hides different semantics
function process(entity):
  validate(entity)      # entities are different kinds; validation is unrelated
  persist(entity)       # one is a DB row, the other a cache entry
  notify(entity)        # one is required, the other is fire-and-forget

# Good - extract only the genuinely shared part
function persist(entity): ...
function processUser(user): validate(user); persist(user); notifyRequired(user)
function processEvent(event): validate(event); persist(event); notifyOptional(event)
```

### D5: Duplicated Knowledge vs. Duplicated Text

DRY is about knowledge, not text. Two occurrences of `3.14` may be coincidence; two occurrences of the business rule "orders over 100 are discounted 10%" are duplication. If the meaning is shared, extract it. If the value just happens to match, leave it.

```text
# Coincidence - leave it
circleArea = pi * r * r
birthdayMarch = 3.14  # March 14th, unrelated

# Shared knowledge - extract it
DISCOUNT_THRESHOLD = 100
DISCOUNT_RATE = 0.10
```

### Quick Reference

| Rule | Principle | Example |
|------|-----------|---------|
| D1 | Extract repeated logic | `validateUser()` shared by save/update |
| D2 | Parameterize, don't copy | `sendEmail(user, template)` |
| D3 | Single source of truth | One `MAX_ITEMS`, referenced everywhere |
| D4 | No duplication-by-abstraction | Extract only genuinely identical steps |
| D5 | DRY is about knowledge | Extract shared rules, not coincidental values |