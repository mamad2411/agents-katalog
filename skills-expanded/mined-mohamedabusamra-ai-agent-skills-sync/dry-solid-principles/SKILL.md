---
name: dry-solid-principles
description: Apply DRY (Don't Repeat Yourself) and SOLID principles when writing, reviewing, or refactoring code. Use when generating new code, reviewing existing code, refactoring, or when the user asks about code quality, DRY, SOLID, or design principles.
---

# DRY and SOLID Principles Code Review

Apply DRY and SOLID principles when writing new code or reviewing existing code. Follow these principles proactively to ensure code quality and maintainability.

## Review Checklist

### DRY (Don't Repeat Yourself)

- [ ] **No duplicated logic**: Same logic appears in multiple places
- [ ] **No repeated code blocks**: Identical or near-identical code blocks exist
- [ ] **Shared utilities extracted**: Common operations moved to reusable functions/utilities
- [ ] **Constants defined once**: Magic numbers/strings extracted to constants
- [ ] **Validation logic centralized**: Similar validation patterns consolidated
- [ ] **Error handling consistent**: Error handling patterns reused, not duplicated

### SOLID Principles

#### S - Single Responsibility Principle
- [ ] **One reason to change**: Each class/function has a single, well-defined purpose
- [ ] **Focused responsibilities**: No mixing of concerns (e.g., data access + business logic + presentation)
- [ ] **Clear naming**: Class/function name clearly indicates its single responsibility

#### O - Open/Closed Principle
- [ ] **Open for extension**: New functionality added via extension (inheritance, composition, plugins)
- [ ] **Closed for modification**: Existing code doesn't need changes to add features
- [ ] **Abstraction used**: Interfaces/abstract classes enable extension without modification

#### L - Liskov Substitution Principle
- [ ] **Subtypes substitutable**: Derived classes can replace base classes without breaking functionality
- [ ] **Contracts preserved**: Subclasses maintain the same contracts/behavior as base classes
- [ ] **No strengthened preconditions**: Subclasses don't impose stricter requirements
- [ ] **No weakened postconditions**: Subclasses don't provide weaker guarantees

#### I - Interface Segregation Principle
- [ ] **Focused interfaces**: Interfaces are specific, not bloated with unrelated methods
- [ ] **No forced implementations**: Classes don't implement methods they don't need
- [ ] **Client-specific interfaces**: Interfaces tailored to what clients actually need

#### D - Dependency Inversion Principle
- [ ] **Depend on abstractions**: High-level modules depend on interfaces, not concrete implementations
- [ ] **Inversion of control**: Dependencies injected rather than created internally
- [ ] **No direct instantiation**: Avoid `new` for dependencies; use dependency injection

## Common Violations to Flag

### DRY Violations

**Repeated validation logic:**
```typescript
// ❌ Bad - duplicated validation
function createUser(data) {
  if (!data.email || !data.email.includes('@')) {
    throw new Error('Invalid email');
  }
  // ...
}

function updateUser(data) {
  if (!data.email || !data.email.includes('@')) {
    throw new Error('Invalid email');
  }
  // ...
}

// ✅ Good - extracted to utility
function validateEmail(email: string): void {
  if (!email || !email.includes('@')) {
    throw new Error('Invalid email');
  }
}
```

**Repeated error handling:**
```typescript
// ❌ Bad - duplicated try-catch
async function getOrder(id) {
  try {
    return await Order.findById(id);
  } catch (error) {
    logger.error(error);
    throw new Error('Failed to fetch order');
  }
}

// ✅ Good - centralized error handling
async function getOrder(id) {
  return await Order.findById(id);
}
// Error handled by middleware
```

### SOLID Violations

**Single Responsibility violations:**
```typescript
// ❌ Bad - multiple responsibilities
class User {
  save() { /* database logic */ }
  sendEmail() { /* email logic */ }
  validate() { /* validation logic */ }
  formatDisplay() { /* presentation logic */ }
}

// ✅ Good - separated concerns
class User { /* data model */ }
class UserRepository { /* database logic */ }
class EmailService { /* email logic */ }
class UserValidator { /* validation logic */ }
```

**Dependency Inversion violations:**
```typescript
// ❌ Bad - depends on concrete class
class OrderService {
  private db = new MySQLDatabase(); // concrete dependency
}

// ✅ Good - depends on abstraction
class OrderService {
  constructor(private db: Database) {} // interface/abstraction
}
```

**Interface Segregation violations:**
```typescript
// ❌ Bad - bloated interface
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
}

class Robot implements Worker {
  work() { /* ... */ }
  eat() { /* forced to implement */ }
  sleep() { /* forced to implement */ }
}

// ✅ Good - segregated interfaces
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

class Robot implements Workable {
  work() { /* only what's needed */ }
}
```

## When Writing New Code

Apply these principles proactively:

1. **Check for existing utilities**: Before writing new code, check if similar functionality already exists
2. **Extract common logic**: If you find yourself repeating code, extract it to a shared utility/service
3. **Single responsibility**: Each new class/function should have one clear purpose
4. **Depend on abstractions**: Use interfaces/types for dependencies, not concrete classes
5. **Design for extension**: Use abstractions and composition to allow future extension without modification
6. **Keep interfaces focused**: Create small, specific interfaces rather than large, general ones

## Review Process

When reviewing existing code:

1. **Scan for duplication**: Look for repeated code patterns, logic, or structures
2. **Check responsibilities**: Verify each class/function has a single, clear purpose
3. **Examine dependencies**: Ensure high-level modules depend on abstractions
4. **Review interfaces**: Check that interfaces are focused and not bloated
5. **Test substitutability**: Verify derived classes can replace base classes safely

## Providing Feedback

Format violations as:

- 🔴 **Critical**: Must fix (e.g., major DRY violation, broken Liskov substitution)
- 🟡 **Warning**: Should fix (e.g., mixed responsibilities, concrete dependencies)
- 🟢 **Suggestion**: Consider improving (e.g., minor duplication, interface could be split)

Include:
- Specific location of the violation
- Explanation of which principle is violated
- Suggested refactoring approach
- Example of improved code when helpful

## Refactoring Guidance

When violations are found:

1. **DRY violations**: Extract common logic to utilities, services, or base classes
2. **SRP violations**: Split classes/functions into focused components
3. **OCP violations**: Introduce abstractions (interfaces, abstract classes) for extension points
4. **LSP violations**: Review inheritance hierarchy and ensure contracts are preserved
5. **ISP violations**: Split large interfaces into smaller, focused ones
6. **DIP violations**: Introduce dependency injection and depend on abstractions
