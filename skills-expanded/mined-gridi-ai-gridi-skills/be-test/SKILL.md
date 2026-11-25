---
name: be-test
description: >
  A skill for writing backend test code based on test cases (TC).
  Implements unit tests and integration tests according to the project's test framework.
  Use this skill for backend test, API test, or unit test writing requests.
---

## 🌐 Language

> All output documents and user-facing messages must be written in the language specified
> by `crew-config.json → preferences.language`. If not set, default to English.

## 🔧 Project Configuration Reference

> **You must read `crew-config.json` first and operate according to the project settings.**
> - `backend.testFramework`: Test framework selection such as Jest, Vitest, pytest, etc.
> - `backend.framework`: Target framework under test
> - `conventions.idStrategy`: ID strategy for test data
>
> If `crew-config.json` does not exist, guide the user to run the `/project-init` skill first.

## ⚠️ ID Strategy (crew-config.json → conventions.idStrategy)

> **Follow the `conventions.idStrategy` setting in `crew-config.json`.**
> - Test data, mocks, and fixtures must also use the same ID strategy
> - **If the setting is missing, use UUID as the default.**

### UUID Usage Example in Tests

```typescript
// ✅ Correct approach: UUID
const mockUser = {
  id: '550e8400-e29b-41d4-a716-446655440000',
  email: 'test@example.com',
};

// Or dynamic generation
import { randomUUID } from 'crypto';
const mockUser = {
  id: randomUUID(),
  email: 'test@example.com',
};

// ❌ Incorrect approach: Numeric ID
const mockUser = {
  id: 1,
  email: 'test@example.com',
};
```

# Backend Test Developer

Generates backend test code based on test case documents.

## Workflow

### 1. Verify Input Documents

Receive the following documents as input:
- Test case document
- Tech spec document (API specification)

```
Example inputs:
- "Write test code based on docs/test-cases/account-test-cases.md"
```

### 2. Project Analysis

1. Understand the existing test structure
2. Identify the test framework in use
3. Analyze test patterns/conventions
4. Understand the mocking strategy

#### Supported Frameworks

| Language | Test Framework | Mocking Library |
|----------|---------------|-----------------|
| Node.js | Jest, Vitest, Mocha | jest.mock, sinon |
| Python | pytest, unittest | pytest-mock, unittest.mock |
| Go | testing, testify | gomock, mockery |
| Java | JUnit 5, TestNG | Mockito, MockK |
| Kotlin | JUnit 5, Kotest | MockK |

### 3. Test Code Generation

#### 3.1 File Structure

```
tests/
├── unit/                    # Unit tests
│   ├── services/
│   │   └── auth.service.test.ts
│   └── utils/
├── integration/             # Integration tests
│   └── api/
│       └── auth.api.test.ts
├── fixtures/                # Test data
│   └── users.fixture.ts
└── helpers/                 # Test utilities
    └── test-utils.ts
```

#### 3.2 Unit Test Example (Jest/TypeScript) - Given-When-Then Format

> Examples shown for Jest/TypeScript. Adapt to your project's test framework as specified in `crew-config.json → backend.testFramework`.

Test code is written in the **Given-When-Then** format. This is the same concept as the AAA (Arrange-Act-Assert) pattern but uses more intuitive naming.

| AAA Pattern | Given-When-Then | Description |
|------------|-----------------|-------------|
| Arrange | Given | Set up preconditions |
| Act | When | Execute the test target |
| Assert | Then | Verify the result |

```typescript
// tests/unit/services/auth.service.test.ts
import { AuthService } from '@/services/auth.service';
import { UserRepository } from '@/repositories/user.repository';
import { hashPassword } from '@/utils/crypto';

jest.mock('@/repositories/user.repository');
jest.mock('@/utils/crypto');

describe('AuthService', () => {
  let authService: AuthService;
  let mockUserRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockUserRepository = new UserRepository() as jest.Mocked<UserRepository>;
    authService = new AuthService(mockUserRepository);
    jest.clearAllMocks();
  });

  describe('signup', () => {
    // TC-AUTH-P-001: Successful sign up
    it('should create a new user with valid credentials', async () => {
      // Given: Valid sign-up input data is prepared
      const input = {
        email: 'test@example.com',
        password: 'Test1234!',
      };
      const hashedPassword = 'hashed_password';
      const expectedUser = {
        id: 'uuid',
        email: input.email,
        createdAt: new Date(),
      };

      // Given: No user is registered with this email
      (hashPassword as jest.Mock).mockResolvedValue(hashedPassword);
      mockUserRepository.findByEmail.mockResolvedValue(null);
      mockUserRepository.create.mockResolvedValue(expectedUser);

      // When: A sign-up attempt is made
      const result = await authService.signup(input);

      // Then: A new user is created
      expect(result).toEqual(expectedUser);
      // Then: Email duplication check is performed
      expect(mockUserRepository.findByEmail).toHaveBeenCalledWith(input.email);
      // Then: Password is hashed
      expect(hashPassword).toHaveBeenCalledWith(input.password);
      // Then: A user record is created
      expect(mockUserRepository.create).toHaveBeenCalledWith({
        email: input.email,
        password: hashedPassword,
      });
    });

    // TC-AUTH-N-001: Duplicate email sign-up failure
    it('should throw error when email already exists', async () => {
      // Given: An email that is already registered exists
      const input = {
        email: 'existing@example.com',
        password: 'Test1234!',
      };
      mockUserRepository.findByEmail.mockResolvedValue({
        id: 'existing-id',
        email: input.email,
      });

      // When & Then: An error is thrown when sign-up is attempted
      await expect(authService.signup(input)).rejects.toThrow(
        'Email already exists'
      );
      // Then: No new user is created
      expect(mockUserRepository.create).not.toHaveBeenCalled();
    });
  });
});
```

#### 3.3 Integration Test Example (Jest/Supertest) - Given-When-Then Format

```typescript
// tests/integration/api/auth.api.test.ts
import request from 'supertest';
import { app } from '@/app';
import { prisma } from '@/lib/prisma';

describe('POST /api/v1/auth/signup', () => {
  beforeEach(async () => {
    await prisma.user.deleteMany();
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  // TC-AUTH-P-001: Successful sign-up API
  it('should return 201 and create user', async () => {
    // Given: Valid sign-up data is prepared
    const input = {
      email: 'test@example.com',
      password: 'Test1234!',
    };

    // When: The sign-up API is called
    const response = await request(app)
      .post('/api/v1/auth/signup')
      .send(input);

    // Then: A 201 response is returned
    expect(response.status).toBe(201);
    // Then: The response includes the email
    expect(response.body.data).toMatchObject({
      email: input.email,
    });
    // Then: The response does not include the password
    expect(response.body.data.password).toBeUndefined();

    // Then: A user has been created in the database
    const user = await prisma.user.findUnique({
      where: { email: input.email },
    });
    expect(user).not.toBeNull();
  });

  // TC-AUTH-N-002: Invalid email format
  it('should return 400 for invalid email format', async () => {
    // Given: Data with an invalid email format is prepared
    const invalidInput = {
      email: 'invalid-email',
      password: 'Test1234!',
    };

    // When: The sign-up API is called
    const response = await request(app)
      .post('/api/v1/auth/signup')
      .send(invalidInput);

    // Then: A 400 response is returned
    expect(response.status).toBe(400);
    // Then: A validation error code is returned
    expect(response.body.error.code).toBe('VALIDATION_ERROR');
  });
});
```

### 4. Test Data Management

#### Fixture Files

```typescript
// tests/fixtures/users.fixture.ts
export const validUser = {
  email: 'test@example.com',
  password: 'Test1234!',
};

export const invalidEmails = [
  'invalid-email',
  '@example.com',
  'user@',
  'user@.com',
];

export const weakPasswords = [
  'short1!',      // Less than 8 characters
  'nospecial1',   // No special characters
  'NOLOWER1!',    // No lowercase letters
];
```

#### Factory Pattern

```typescript
// tests/helpers/factories/user.factory.ts
import { faker } from '@faker-js/faker';

export const createUserInput = (overrides = {}) => ({
  email: faker.internet.email(),
  password: 'Test1234!',
  ...overrides,
});

export const createUser = async (prisma, overrides = {}) => {
  return prisma.user.create({
    data: createUserInput(overrides),
  });
};
```

### 5. Test Coverage Goals

| Area | Minimum Coverage |
|------|-----------------|
| Business logic | 80% |
| API handlers | 70% |
| Utilities | 90% |
| Overall | 75% |

### 6. File Output Location

```
{projectRoot}/tests/unit/{domain}/{filename}.test.ts
{projectRoot}/tests/integration/api/{filename}.api.test.ts
```

## Test Writing Principles

### 1. Given-When-Then Pattern (BDD Style)
- **Given**: Set up preconditions and test data
- **When**: Execute the test target
- **Then**: Verify the result

> Note: This is the same concept as the AAA pattern (Arrange-Act-Assert), but Given-When-Then is more intuitive and easier to connect with business requirements.

### 2. Test Independence
- Each test must be independently executable
- No shared state between tests
- Reset state with beforeEach

### 3. Clear Test Names
```typescript
// Good
it('should return 401 when token is expired')
it('should throw ValidationError when email format is invalid')

// Bad
it('test signup')
it('error case')
```

### 4. TC ID Mapping
- Include TC ID as a comment in each test
- Ensure traceability

## References

- Test patterns guide: [references/test-patterns.md](references/test-patterns.md)
- Mocking guide: [references/mocking-guide.md](references/mocking-guide.md)
