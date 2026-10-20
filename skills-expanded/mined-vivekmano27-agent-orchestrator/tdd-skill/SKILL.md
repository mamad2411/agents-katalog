---
name: tdd-skill
description: "Enforce strict Test-Driven Development — Red-Green-Refactor cycle. Write failing tests first, implement minimal code to pass, then refactor. Use when the user says \"write tests first\", \"TDD\", \"test-driven\", \"red green refactor\", or when building features that require high reliability. This skill prevents the agent from skipping to implementation. Also use when the user wants to add a feature with confidence that nothing breaks."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# TDD (Test-Driven Development) Skill

Enforce the Red-Green-Refactor cycle for every feature. The core discipline: no production code exists without a test that demanded it. This produces code that is tested by definition, has minimal complexity, and is safe to refactor.

## When to Use

- User asks to build a feature using TDD or "tests first"
- Business-critical code where correctness matters more than speed (payments, auth, data processing)
- Fixing a bug — write the failing test that reproduces it BEFORE writing the fix
- Refactoring existing code — ensure tests pass before AND after changes
- Building a new service or module from scratch

## When NOT to Use TDD

TDD adds overhead that isn't always justified. Skip it for:
- **One-off scripts** — throwaway migration scripts, data backfills
- **UI layout/styling** — visual changes are better tested with screenshot comparison
- **Boilerplate/config files** — environment configs, CI pipeline YAML, Dockerfiles
- **Prototyping** — exploratory code where requirements are unknown (add tests when direction is confirmed)

Use judgment: if the code has branching logic, use TDD. If it's purely declarative, skip it.

## The TDD Cycle

### 1. RED — Write a Failing Test

Write the test BEFORE any implementation. The test describes the behavior you want, not the code structure:

```typescript
// Jest / Vitest
describe('UserService', () => {
  it('should create a user with valid data', async () => {
    const result = await userService.create({
      email: 'test@example.com',
      name: 'Test User',
      password: 'SecurePass123!',
    });

    expect(result).toBeDefined();
    expect(result.id).toBeDefined();
    expect(result.email).toBe('test@example.com');
    expect(result.passwordHash).not.toBe('SecurePass123!');
  });

  it('should reject duplicate email', async () => {
    await userService.create({ email: 'dup@test.com', name: 'A', password: 'Pass123!' });
    await expect(
      userService.create({ email: 'dup@test.com', name: 'B', password: 'Pass123!' }),
    ).rejects.toThrow('Email already exists');
  });
});
```

```python
# Pytest
class TestUserService:
    async def test_creates_user_with_valid_data(self, service):
        result = await service.create_user(
            email="test@example.com",
            name="Test User",
            password="SecurePass123!",
        )

        assert result.id is not None
        assert result.email == "test@example.com"
        assert result.password_hash != "SecurePass123!"

    async def test_rejects_duplicate_email(self, service):
        await service.create_user(email="dup@test.com", name="A", password="Pass123!")
        with pytest.raises(ValueError, match="Email already exists"):
            await service.create_user(email="dup@test.com", name="B", password="Pass123!")
```

Run the test — it MUST fail. If it passes, either the test is wrong or the feature already exists.

### 2. GREEN — Write Minimal Code to Pass

Implement ONLY what the test requires. No extra features, no premature optimization, no "while I'm here" additions:

```typescript
class UserService {
  async create(data: CreateUserDto): Promise<User> {
    const existing = await this.repo.findByEmail(data.email);
    if (existing) throw new Error('Email already exists');

    const passwordHash = await bcrypt.hash(data.password, 10);
    return this.repo.create({ ...data, passwordHash });
  }
}
```

Run the test — it MUST pass. If it doesn't, fix the implementation, not the test.

### 3. REFACTOR — Improve Without Changing Behavior

Clean up duplication, improve naming, extract helpers. The key constraint: all tests must still pass after refactoring.

```typescript
// Before refactor: inline hash
const passwordHash = await bcrypt.hash(data.password, 10);

// After refactor: extract to method with configurable rounds
private async hashPassword(plaintext: string): Promise<string> {
  return bcrypt.hash(plaintext, this.hashRounds);
}
```

Run tests again — still green? Good. Commit.

## TDD Workflow Per Feature

Follow this sequence for each new feature or behavior:

1. **List behaviors** — write down 3-5 test case names before coding anything
2. **Pick the simplest** — start with the happy path or most basic case
3. **RED** — write one failing test
4. **GREEN** — make it pass with minimal code
5. **REFACTOR** — clean up
6. **Repeat** — pick the next behavior from your list

```
Example: Adding a "cancel order" feature
  1. should cancel a pending order
  2. should reject cancelling a shipped order
  3. should refund payment on cancellation
  4. should send cancellation email
  5. should handle partial refund for partially shipped orders
```

Start with #1. Don't think about #5 until #1-4 are green.

## Framework-Specific Patterns

### NestJS with Test.createTestingModule
```typescript
describe('OrderController', () => {
  let controller: OrderController;
  let mockService: jest.Mocked<OrderService>;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      controllers: [OrderController],
      providers: [{ provide: OrderService, useValue: createMock<OrderService>() }],
    }).compile();

    controller = module.get(OrderController);
    mockService = module.get(OrderService);
  });

  it('should return 201 on valid create', async () => {
    mockService.create.mockResolvedValue(buildOrder());
    const result = await controller.create(validDto);
    expect(result.id).toBeDefined();
  });
});
```

### Django with pytest-django
```python
@pytest.mark.django_db
class TestOrderView:
    def test_creates_order(self, api_client, auth_headers):
        response = api_client.post(
            "/api/v1/orders/",
            data={"items": [{"product_id": 1, "quantity": 2}]},
            **auth_headers,
        )
        assert response.status_code == 201
        assert "id" in response.data
```

## Rules

- NEVER write implementation before the test
- NEVER write more code than needed to pass the current test
- ALWAYS run tests after each change (Red -> Green -> Refactor -> run again)
- ALWAYS refactor after green (even if the cleanup is small)
- One test at a time — don't write 5 tests then implement everything at once
- Commit after each green-refactor cycle — small, atomic commits

## Anti-Patterns

- **Writing tests after code** — defeats the purpose; tests become confirmation bias rather than design feedback
- **Gold-plating in GREEN phase** — adding features the test didn't ask for; this creates untested code
- **Skipping REFACTOR phase** — "it works, ship it" leads to accumulated tech debt; always clean up
- **Testing implementation, not behavior** — asserting on method calls or internal state instead of observable output
- **Giant RED steps** — writing a test that requires 100 lines of implementation to pass; break it into smaller behaviors
- **Abandoning TDD mid-feature** — "I'll just finish this quickly without tests"; the last 20% is where bugs hide
- **Mocking everything** — over-mocking makes tests pass for wrong reasons; mock boundaries, not internals
- **Not running tests frequently** — run after every change, not just at the end; catch failures early

## Checklist

- [ ] Test written BEFORE implementation for every behavior
- [ ] Each test fails when first written (RED confirmed)
- [ ] Implementation is minimal — only enough to pass the current test
- [ ] Tests pass after implementation (GREEN confirmed)
- [ ] Code refactored after each green phase
- [ ] All tests still pass after refactoring
- [ ] Test names describe behavior ("should reject expired tokens") not implementation ("test validateToken")
- [ ] Coverage meets project thresholds (default 80% line coverage)
- [ ] Each RED-GREEN-REFACTOR cycle is one atomic commit
- [ ] Edge cases and error paths have their own tests, not just happy path
