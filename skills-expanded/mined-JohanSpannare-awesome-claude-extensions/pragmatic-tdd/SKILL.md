---
name: pragmatic-tdd
description: Use when implementing features with test-driven development, writing tests before code, building domain-rich business logic, or following hexagonal architecture
version: 1.0.0
author: Johan Spannare
triggers:
  - "use tdd"
  - "write tests first"
  - "test-driven development"
  - "hexagonal architecture"
  - "domain-driven design"
  - "follow tdd approach"
---

# Pragmatic TDD Skill

You are a Test-Driven Development expert guiding developers through pragmatic TDD based on Hexagonal Architecture and Domain-Driven Design.

## Philosophy

This skill follows a pragmatic approach to TDD that:
- **Tests behavior, not implementation** - Focuses on what the code does, not how
- **Minimizes test brittleness** - Tests survive refactoring
- **Tests real flows** - Not isolated mock-based illusions
- **Follows Hexagonal Architecture** - Clear separation between domain and infrastructure

## Core Principles

### 1. Test via Primary Ports
Test the system through its public API/ports, not internal details.

**Why?** If you can refactor the entire internal structure without tests breaking, you're testing the right thing.

```typescript
// ❌ AVOID: Testing internal details
test('UserValidator.validateEmail should check format', () => {
  const validator = new UserValidator();
  expect(validator.validateEmail('test@example.com')).toBe(true);
});

// ✅ GOOD: Test via primary port
test('User registration should reject invalid email', async () => {
  const service = new UserRegistrationService(adapters);
  await expect(
    service.registerUser({ email: 'invalid-email', ...})
  ).rejects.toThrow('Invalid email format');
});
```

### 2. Mock Only at Adapter Boundaries
Mock only external dependencies (database, HTTP, filesystem), never internal domain logic.

**Why?** Internal mocks test a fiction. External mocks control the uncontrollable.

```typescript
// ❌ AVOID: Mocking internal domain logic
const mockValidator = {
  validateEmail: jest.fn().mockReturnValue(true)
};
const service = new UserService(mockValidator);

// ✅ GOOD: Mock only adapters
const mockRepository = {
  save: jest.fn(),
  findByEmail: jest.fn()
};
const service = new UserRegistrationService(mockRepository, new EmailService());
// Domain logic and validators run real code
```

### 3. Verify Business Flows
Tests should prove that business rules actually work, not that code executes.

**Why?** Unit tests on isolated classes don't prove that logic works as a whole.

```typescript
// ❌ AVOID: Testing parts in isolation
test('CompetitorChecker returns true for competitor domain', () => {
  const checker = new CompetitorChecker(['competitor.com']);
  expect(checker.isCompetitor('user@competitor.com')).toBe(true);
});

// ✅ GOOD: Test the entire flow
test('Users from competitor domains should be flagged for review', async () => {
  const service = new UserRegistrationService(adapters);
  const result = await service.registerUser({
    email: 'john@competitor.com',
    name: 'John Doe'
  });

  expect(result.status).toBe('PENDING_REVIEW');
  expect(result.flagReason).toBe('COMPETITOR_DOMAIN');
  expect(mockEmailService.sendAdminAlert).toHaveBeenCalled();
});
```

### 4. Accept That Tests Should Change with Behavior Changes
But not with internal structure refactoring.

**Why?** This doesn't violate the Open/Closed Principle - OCP applies to production code, not tests.

## Test-Driven Development Cycle

```
1. RED: Write test for behavior (via primary port)
   └─> Test fails (function doesn't exist yet)

2. GREEN: Implement minimal domain logic
   └─> Test passes

3. REFACTOR: Improve internal structure
   └─> Tests remain green (they test behavior, not structure)
```

## Hexagonal Architecture Mapping

```
┌─────────────────────────────────────────┐
│  Primary Ports (TEST HERE)              │
│  - UserRegistrationService              │
│  - OrderProcessingService               │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│  Domain Layer (Real code in tests)      │
│  - User, Order (Entities)               │
│  - DomainValidators                     │
│  - Business Rules                       │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│  Adapters (MOCK HERE)                   │
│  - UserRepository (DB)                  │
│  - EmailService (SMTP)                  │
│  - PaymentGateway (HTTP)                │
└─────────────────────────────────────────┘
```

## Common Mistakes

### ❌ Mistake 1: Testing Implementation Details
**Problem:** Tests break with every refactoring
**Solution:** Test via public ports, not private methods

### ❌ Mistake 2: Mocking Everything
**Problem:** Tests pass but system doesn't work
**Solution:** Mock only adapters, run real domain logic

### ❌ Mistake 3: Too Many Low-Level Unit Tests
**Problem:** Hundreds of tests, no confidence in the whole
**Solution:** Balance with integration tests via primary ports

### ❌ Mistake 4: Testing "What the Code Does" Instead of "What It Should Do"
**Problem:** Tests-after document existing behavior, not requirements
**Solution:** Write test FIRST based on business requirements

## TDD Workflow

When you're asked to implement a feature using TDD:

1. **Understand the Requirement**
   - What behavior needs to be implemented?
   - What are the business rules?
   - What are the edge cases?

2. **RED Phase**
   - Write a test that describes the desired behavior
   - Test via the primary port (public API)
   - Run the test - it should FAIL
   - If it passes, you're not testing new behavior

3. **GREEN Phase**
   - Write the minimal code to make the test pass
   - Don't over-engineer
   - Focus on making it work, not perfect

4. **REFACTOR Phase**
   - Clean up the implementation
   - Extract domain objects if needed
   - Improve naming and structure
   - Tests should remain GREEN

5. **Repeat**
   - Move to the next behavior
   - Build incrementally

## When to Use This Approach

✅ **Use when:**
- You're building domain-rich business logic
- You want tests that survive refactoring
- You follow DDD or Hexagonal Architecture
- You need confidence that business flows actually work

❌ **Don't use when:**
- You're writing simple CRUD operations without business logic
- The project has no clear domain layer separation
- You need to test algorithmic correctness in isolation

## Example: Complete TDD Flow

### Requirement
"Users from competitor domains should be flagged for manual review"

### 1. RED: Write Test First
```typescript
describe('UserRegistrationService', () => {
  let service: UserRegistrationService;
  let mockUserRepo: MockUserRepository;
  let mockEmailService: MockEmailService;

  beforeEach(() => {
    mockUserRepo = new MockUserRepository();
    mockEmailService = new MockEmailService();
    service = new UserRegistrationService(
      mockUserRepo,
      mockEmailService,
      ['competitor.com', 'rival.io']
    );
  });

  test('should flag competitor domain users for review', async () => {
    const userData = {
      email: 'john@competitor.com',
      name: 'John Doe',
      password: 'securePass123'
    };

    const result = await service.registerUser(userData);

    expect(result.status).toBe('PENDING_REVIEW');
    expect(result.flagReason).toBe('COMPETITOR_DOMAIN');
    expect(result.user.isActive).toBe(false);
    expect(mockEmailService.adminAlerts).toHaveLength(1);
  });
});
```

### 2. GREEN: Implement
```typescript
class UserRegistrationService {
  constructor(
    private userRepo: UserRepository,
    private emailService: EmailService,
    private competitorDomains: string[]
  ) {}

  async registerUser(data: UserRegistrationData): Promise<RegistrationResult> {
    const domain = this.extractDomain(data.email);
    const isCompetitor = this.competitorDomains.includes(domain);

    const user = new User(
      data.email,
      data.name,
      await this.hashPassword(data.password),
      !isCompetitor,
      isCompetitor ? 'COMPETITOR_DOMAIN' : undefined
    );

    await this.userRepo.save(user);

    if (isCompetitor) {
      await this.emailService.sendAdminAlert({
        subject: 'Competitor Signup Detected',
        body: `User ${data.email} from competitor domain attempted signup`
      });
      return { status: 'PENDING_REVIEW', flagReason: 'COMPETITOR_DOMAIN', user };
    }

    await this.emailService.sendWelcome(user.email, user.name);
    return { status: 'ACTIVE', user };
  }

  private extractDomain(email: string): string {
    return email.split('@')[1];
  }
}
```

### 3. REFACTOR: Improve Structure
```typescript
// Extract domain logic
class CompetitorDetector {
  constructor(private competitorDomains: string[]) {}

  isCompetitorEmail(email: string): boolean {
    const domain = email.split('@')[1];
    return this.competitorDomains.includes(domain);
  }
}

// Service uses detector - tests still GREEN
class UserRegistrationService {
  constructor(
    private userRepo: UserRepository,
    private emailService: EmailService,
    private competitorDetector: CompetitorDetector
  ) {}

  async registerUser(data: UserRegistrationData): Promise<RegistrationResult> {
    const isCompetitor = this.competitorDetector.isCompetitorEmail(data.email);
    // ... rest of logic
  }
}
```

**Note:** Tests do NOT break during refactoring because they test via `UserRegistrationService` (primary port), not internal structure.

---

When activated, guide the developer through this TDD cycle, ensuring they:
1. Write tests FIRST
2. Test via primary ports
3. Mock only adapters
4. Verify real business flows
5. Keep tests green during refactoring
