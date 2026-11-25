# Backend Testing Skill

Guidelines for writing and maintaining backend tests in Rent4U.

## Stack

- **Runner:** Jest 30
- **HTTP testing:** Supertest 7
- **Database:** SQLite in-memory (for isolation)
- **Auth mocking:** JWT tokens generated with the test SECRET

## Directory Structure

```
backend/src/__tests__/
├── controllers/
│   ├── user_controller.test.js
│   └── house_controller.test.js
├── middlewares/
│   ├── auth.test.js
│   └── roleCheck.test.js
├── routes/
│   ├── user_routes.test.js
│   └── house_routes.test.js
└── helpers/
    ├── setup.js          # Prisma reset + seed before each suite
    ├── factories.js       # User/House/Image factory functions
    └── auth.js            # Token generation helpers
```

## Conventions

### Test File Naming
- One test file per controller or middleware
- Name: `<module>.test.js`
- Group tests with `describe('<ModuleName>')`, nest with `describe('<functionName>')`

### Test Structure (AAA Pattern)
```js
describe('createUser', () => {
  it('should create a user with valid data', async () => {
    // Arrange
    const payload = { name: 'Test', email: 'test@test.com', password: 'pass123', username: 'testuser', roleId: 3 };

    // Act
    const res = await request(app).post('/users').send(payload);

    // Assert
    expect(res.status).toBe(201);
    expect(res.body.data).toHaveProperty('id');
    expect(res.body.data.email).toBe('test@test.com');
  });
});
```

### Database Isolation
```js
// helpers/setup.js
const { PrismaClient } = require('../generated/prisma/client');

let prisma;

beforeAll(async () => {
  prisma = new PrismaClient({ datasourceUrl: 'file:./test.db' });
  await prisma.$executeRaw`DELETE FROM Image`;
  await prisma.$executeRaw`DELETE FROM House`;
  await prisma.$executeRaw`DELETE FROM User`;
  await prisma.$executeRaw`DELETE FROM Role`;
});

afterEach(async () => {
  // Clean all tables after each test
  await prisma.$executeRaw`DELETE FROM Image`;
  await prisma.$executeRaw`DELETE FROM House`;
  await prisma.$executeRaw`DELETE FROM User`;
});

afterAll(async () => {
  await prisma.$disconnect();
});
```

### Factory Helpers
```js
// helpers/factories.js
const bcrypt = require('bcrypt');

const createTestUser = async (prisma, overrides = {}) => {
  const defaults = {
    name: 'Test User',
    username: `user_${Date.now()}`,
    email: `test_${Date.now()}@test.com`,
    password: await bcrypt.hash('password123', 10),
    roleId: 3, // User role
  };
  return prisma.user.create({ data: { ...defaults, ...overrides } });
};

const createTestHouse = async (prisma, ownerId, overrides = {}) => {
  const defaults = {
    name: 'Test House',
    city: 'Yangon',
    address: '123 Test St',
    price: 50000,
    description: 'A nice test house',
    rooms: 2,
    bathrooms: 1,
    dateAvailable: new Date(),
    isAvailable: true,
    ownerId,
  };
  return prisma.house.create({ data: { ...defaults, ...overrides } });
};

module.exports = { createTestUser, createTestHouse };
```

### Auth Helpers
```js
// helpers/auth.js
const jwt = require('jsonwebtoken');

const generateToken = (userId, role = 'User') => {
  return jwt.sign({ userId, role }, process.env.SECRET || 'test-secret', { expiresIn: '1h' });
};

const authHeader = (token) => `Bearer ${token}`;

module.exports = { generateToken, authHeader };
```

## What to Test

### Controllers — Required Cases
| Case | Example |
|------|---------|
| Happy path | Valid input → 201 + correct body |
| Missing required fields | No email → 400 |
| Invalid data types | String where number expected → 400 |
| Not found | GET /users/999 → 404 |
| Unauthorized | No token → 401 |
| Forbidden | Wrong role → 403 |
| Duplicate unique fields | Same email twice → 409 |

### Middlewares — Required Cases
| Middleware | Test |
|-----------|------|
| `authenticateToken` | Valid token → calls next() |
| `authenticateToken` | Missing token → 401 |
| `authenticateToken` | Expired/invalid token → 403 |
| `checkRole('Admin')` | Matching role → calls next() |
| `checkRole('Admin')` | Wrong role → 403 |

## Running Tests

```bash
# All tests
bun test

# With coverage
bun test --coverage

# Single file
bun test -- user_controller.test.js

# Watch mode
bun test --watch
```

## Quality Checklist

- [ ] Each test has a clear `it('should ...')` description
- [ ] Tests are independent — no shared mutable state between tests
- [ ] Database is cleaned between tests
- [ ] Error responses include a `message` field
- [ ] No hardcoded IDs — use factory-created IDs
- [ ] Auth tests cover both valid and invalid tokens
- [ ] Edge cases: empty strings, null, undefined, very long inputs
