---
description: Coding style standards and conventions
alwaysApply: false
---

# Code Style Guidelines

## 🎯 Core Principle: Human Readability First

**Code is written once, read many times.**

### Bad Example (AI-optimized, human-unreadable):
```
function p(u){return u.n+(u.a>18?" (adult)":" (minor)");}
```

### Good Example (Human-readable):
```
function formatUserDisplay(user) {
  const ageCategory = user.age > 18 ? " (adult)" : " (minor)";
  return user.name + ageCategory;
}
```

**Rule: Always prioritize code that humans can understand quickly.**

---

## Naming Conventions

### Choose Names Based on Your Language

**JavaScript/TypeScript:**
- `camelCase` for variables and functions: `getUserData()`
- `PascalCase` for classes and types: `class UserService`
- `UPPER_SNAKE_CASE` for constants: `const MAX_RETRY_ATTEMPTS = 3`

**Python:**
- `snake_case` for functions and variables: `get_user_data()`
- `PascalCase` for classes: `class UserService`
- `UPPER_SNAKE_CASE` for constants: `MAX_RETRY_ATTEMPTS = 3`

**Java/C#:**
- `camelCase` for variables and parameters: `userName`
- `PascalCase` for classes and methods: `GetUserData()`
- `UPPER_SNAKE_CASE` for constants: `MAX_RETRY_ATTEMPTS`

**Go:**
- `camelCase` for private: `getUserData()`
- `PascalCase` for public: `GetUserData()`

### Descriptive Over Concise

```
❌ Bad: fd, usr, tmp, idx, arr, obj, str
✅ Good: fileDescriptor, currentUser, template, index, userArray, userObject, errorMessage
```

### Use Intention-Revealing Names

```javascript
// ❌ Bad
if (x > 100) { }

// ✅ Good
const PRICE_THRESHOLD = 100;
if (productPrice > PRICE_THRESHOLD) { }

// ❌ Bad
function process(data) { }

// ✅ Good
function validateAndSaveUserRegistration(registrationData) { }
```

---

## Code Organization

### Keep Functions Small

**Target: 10-20 lines per function**
**Maximum: 30-40 lines**

```javascript
// ❌ Bad - too much in one function
function processOrder(order) {
  // 50+ lines of validation
  // 30 lines of price calculation
  // 20 lines of inventory check
  // 25 lines of payment processing
  // 15 lines of notification sending
}

// ✅ Good - broken into focused functions
function processOrder(order) {
  validateOrder(order);
  const total = calculateOrderTotal(order);
  checkInventoryAvailability(order.items);
  processPayment(order.paymentMethod, total);
  sendOrderConfirmation(order.customer);
}
```

### Single Responsibility Principle

Each function/class should do ONE thing well.

```python
# ❌ Bad - doing too much
class UserManager:
    def handle_user(self, user_data):
        # validates user
        # saves to database
        # sends email
        # logs activity
        # updates cache
        # triggers webhooks

# ✅ Good - single responsibilities
class UserValidator:
    def validate(self, user_data):
        # only validates

class UserRepository:
    def save(self, user):
        # only saves to database

class NotificationService:
    def send_welcome_email(self, user):
        # only sends emails
```

---

## Reduce Complexity

### Avoid Deep Nesting (Max 3 Levels)

```javascript
// ❌ Bad - deeply nested
function processData(data) {
  if (data) {
    if (data.user) {
      if (data.user.isActive) {
        if (data.user.hasPermission) {
          // do something
        }
      }
    }
  }
}

// ✅ Good - early returns
function processData(data) {
  if (!data) return;
  if (!data.user) return;
  if (!data.user.isActive) return;
  if (!data.user.hasPermission) return;
  
  // do something
}
```

### Extract Complex Conditions

```python
# ❌ Bad - complex inline condition
if user.age >= 18 and user.has_account and user.verified and not user.banned and user.balance > 0:
    allow_purchase()

# ✅ Good - extracted to named function
def can_make_purchase(user):
    is_adult = user.age >= 18
    has_valid_account = user.has_account and user.verified
    not_restricted = not user.banned
    has_funds = user.balance > 0
    return is_adult and has_valid_account and not_restricted and has_funds

if can_make_purchase(user):
    allow_purchase()
```

---

## Comments and Documentation

### When to Comment

✅ **DO comment:**
- WHY you're doing something (business logic, non-obvious decisions)
- Complex algorithms or calculations
- Workarounds for bugs in libraries
- Important assumptions or constraints

❌ **DON'T comment:**
- WHAT the code does (code should be self-explanatory)
- Obvious operations
- Redundant information

```javascript
// ❌ Bad - stating the obvious
// Increment counter by 1
counter++;

// ❌ Bad - redundant
// Get user by ID
function getUserById(id) { }

// ✅ Good - explaining WHY
// We must wait 2 seconds because the external API rate-limits to 30 req/min
await delay(2000);

// ✅ Good - explaining business rule
// Customers with over $10,000 in yearly purchases get automatic premium status
if (yearlyTotal > 10000) {
  user.status = 'premium';
}
```

### Documentation Headers

Add documentation for public APIs:

```typescript
/**
 * Calculates the discounted price for a product based on user tier.
 * 
 * @param product - The product to price
 * @param user - The user making the purchase
 * @returns The final price after applying all applicable discounts
 * @throws {InvalidProductError} If product is not available
 */
function calculatePrice(product: Product, user: User): number {
  // implementation
}
```

---

## Error Handling

### Always Handle Errors

```javascript
// ❌ Bad - no error handling
async function fetchUserData(userId) {
  const response = await fetch(`/api/users/${userId}`);
  const data = await response.json();
  return data;
}

// ✅ Good - proper error handling
async function fetchUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch user: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Error fetching user ${userId}:`, error);
    throw error; // or return a default value
  }
}
```

### Fail Fast with Validation

```python
def process_payment(amount, payment_method):
    # ✅ Validate inputs immediately
    if amount <= 0:
        raise ValueError("Amount must be positive")
    
    if not payment_method:
        raise ValueError("Payment method is required")
    
    if amount > 10000:
        raise ValueError("Amount exceeds maximum transaction limit")
    
    # Now safely process payment
    return charge(payment_method, amount)
```

---

## Code Formatting

### Consistent Spacing

```javascript
// ✅ Good spacing
function calculateTotal(items) {
  let total = 0;
  
  for (const item of items) {
    total += item.price * item.quantity;
  }
  
  return total;
}

// Use blank lines to separate logical sections
function processOrder(order) {
  // Validation section
  validateOrder(order);
  validateInventory(order.items);
  
  // Calculation section
  const subtotal = calculateSubtotal(order.items);
  const tax = calculateTax(subtotal);
  const total = subtotal + tax;
  
  // Processing section
  return createInvoice(order, total);
}
```

### Line Length

**Keep lines under 80-120 characters** for readability.

```javascript
// ❌ Bad - too long
const result = calculateComplexMetric(param1, param2, param3, param4, param5, param6, param7, param8);

// ✅ Good - broken into multiple lines
const result = calculateComplexMetric(
  param1,
  param2,
  param3,
  param4,
  param5,
  param6,
  param7,
  param8
);
```

---

## Language-Specific Guidelines

### JavaScript/TypeScript

```typescript
// Prefer const over let, never use var
const userName = "Alice";
let counter = 0;

// Use arrow functions for callbacks
const numbers = [1, 2, 3].map(n => n * 2);

// Use destructuring
const { name, email } = user;

// Use template literals
const message = `Welcome, ${name}!`;

// Use optional chaining
const city = user?.address?.city;

// Use async/await over promises
async function fetchData() {
  const data = await getData();
  return data;
}
```

### Python

```python
# Follow PEP 8
# Use list comprehensions
squares = [x**2 for x in range(10)]

# Use context managers
with open('file.txt', 'r') as f:
    data = f.read()

# Use f-strings
message = f"Welcome, {name}!"

# Use type hints (Python 3.6+)
def greet(name: str) -> str:
    return f"Hello, {name}"
```

---

## File Organization

### One Concept Per File

```
✅ Good structure:
user-service.js       # UserService class
user-repository.js    # UserRepository class
user-validator.js     # Validation logic
user-types.ts         # Type definitions

❌ Bad structure:
user-stuff.js         # Everything related to users
utils.js              # Random utility functions
helpers.js            # More random functions
```

### Organize Imports

```javascript
// 1. Standard library / built-ins
import fs from 'fs';
import path from 'path';

// 2. Third-party packages
import express from 'express';
import { z } from 'zod';

// 3. Your code
import { UserService } from './services/user-service';
import { config } from './config';
```

---

## Before Committing Code

**Checklist:**
- [ ] Code is readable and understandable
- [ ] Functions are small and focused
- [ ] Names are descriptive
- [ ] No deep nesting (max 3 levels)
- [ ] Appropriate error handling
- [ ] Meaningful comments for complex logic
- [ ] No hardcoded secrets or sensitive data
- [ ] Tests exist and pass
- [ ] Linting passes
- [ ] No console.logs or debug statements

---

## Adapt This Template!

**This is a starting point. Customize it for your project:**
- Add language-specific conventions
- Include framework-specific patterns
- Document team preferences
- Add examples from your codebase
- Update as the team learns and grows
