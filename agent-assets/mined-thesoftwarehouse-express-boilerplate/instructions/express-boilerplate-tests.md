---
applyTo: "**/*.spec.ts"
---

## Test Structure and Organization

### File Naming and Location
- All test files must have a `.spec.ts` suffix
- **Unit tests**: Place next to the file they test (e.g., `src/shared/pagination-utils/pagination-utils.spec.ts`)
- **Integration tests**: Place in `src/tests` directory organized by feature (e.g., `src/tests/users/users.spec.ts`)
- Each feature should have its own test file and directory structure
- Shared test utilities should be placed in `src/tests/shared/`

### Test Categories and Commands
- **Unit tests**: `npm run units` - Tests individual functions, utilities, and business logic
- **Integration tests**: `npm run integration` - Tests complete API endpoints and feature workflows
- **Coverage reports**: Use `npm run services-units-coverage` and `npm run integration-tests-coverage`

## Integration Test Pattern

### Basic Structure
```typescript
import { expect } from "chai";
import "mocha";
import request from "supertest";

describe("Feature Name API", () => {
  describe("POST /api/feature", () => {
    it("should create a new resource successfully", async () => {
      const payload = {
        name: "Test Resource",
        description: "Test Description"
      };

      const response = await request(global.container.cradle.app)
        .post("/api/feature")
        .send(payload)
        .expect(201);

      expect(response.body).to.have.property("id");
      expect(response.body.name).to.equal(payload.name);
    });

    it("should return validation error for invalid input", async () => {
      const invalidPayload = { name: "" };

      await request(global.container.cradle.app)
        .post("/api/feature")
        .send(invalidPayload)
        .expect(400);
    });
  });

  describe("GET /api/feature", () => {
    it("should return paginated list", async () => {
      const response = await request(global.container.cradle.app)
        .get("/api/feature?page=1&limit=10")
        .expect(200);

      expect(response.body).to.have.property("data");
      expect(response.body).to.have.property("meta");
      expect(response.body.meta).to.have.property("pagination");
    });
  });
});
```

### Advanced Integration Test Patterns
```typescript
describe("Feature with Authentication", () => {
  let authToken: string;
  let testUserId: string;

  beforeEach(async () => {
    // Create test user and get auth token
    const authResponse = await request(global.container.cradle.app)
      .post("/api/auth/login")
      .send({ email: "test@example.com", password: "password" })
      .expect(200);

    authToken = authResponse.body.access_token;
    testUserId = authResponse.body.user.id;
  });

  it("should require authentication", async () => {
    await request(global.container.cradle.app)
      .get("/api/protected-resource")
      .expect(401);
  });

  it("should access protected resource with valid token", async () => {
    const response = await request(global.container.cradle.app)
      .get("/api/protected-resource")
      .set("Authorization", `Bearer ${authToken}`)
      .expect(200);

    expect(response.body).to.have.property("data");
  });
});
```

## Unit Test Pattern

### Utility Function Testing
```typescript
import "mocha";
import { expect } from "chai";
import { functionToTest } from "./utility-file";

describe("Utility Function Name", () => {
  it("should handle valid input correctly", () => {
    const result = functionToTest("valid input");
    expect(result).to.equal("expected output");
  });

  it("should throw error for invalid input", () => {
    expect(() => functionToTest(null)).to.throw("Expected error message");
  });

  it("should handle edge cases", () => {
    const result = functionToTest("");
    expect(result).to.be.null;
  });
});
```

### Handler/Service Testing with Mocks
```typescript
import "mocha";
import { expect } from "chai";
import { SinonStub, stub } from "sinon";
import { YourHandler } from "./your-handler";

describe("YourHandler", () => {
  let handler: YourHandler;
  let repositoryStub: SinonStub;

  beforeEach(() => {
    repositoryStub = stub();
    handler = new YourHandler(repositoryStub);
  });

  afterEach(() => {
    repositoryStub.restore?.();
  });

  it("should execute command successfully", async () => {
    const command = { id: "test-id", name: "test-name" };
    repositoryStub.findOne.resolves({ id: "test-id" });

    const result = await handler.execute(command);

    expect(result).to.have.property("id", "test-id");
    expect(repositoryStub.findOne.calledOnce).to.be.true;
  });
});
```

## Test Environment Setup

### Bootstrap Configuration
- Test bootstrap is in `src/tests/bootstrap.ts`
- Sets up dependency injection container and database connection
- Uses separate `.env.test` file for test environment variables
- Automatically drops and recreates database before test suite
- Global variables available: `global.container`, `global.dbConnection`

### Database Cleanup
```typescript
// In src/tests/bootstrap.ts - Add repositories to clearDb function
const clearDb = async (dataSource: DataSource) => {
  const repositories = [
    dataSource.getRepository(UserEntity),
    dataSource.getRepository(ProductEntity),
    // Add all your entities here
  ];

  for (const repository of repositories) {
    await repository.delete({});
  }
};
```

### Environment Variables
- All test environment variables must be defined in `.env.test`
- Copy all production environment variables and modify for test environment
- Use test-specific database credentials and service URLs
- Ensure test isolation by using separate resources

## Testing Best Practices

### Test Coverage Requirements
- **Integration tests**: Mandatory for all API endpoints
- **Unit tests**: Mandatory for all utility functions and business logic
- **Error scenarios**: Test both success and failure paths (see error-handling.instructions.md)
- **Edge cases**: Test boundary conditions and edge cases

### Test Data Management
```typescript
describe("Feature Tests", () => {
  beforeEach(async () => {
    // Clear database and seed test data
    await global.dbConnection.synchronize(true);
    
    // Create test data
    const repository = global.dbConnection.getRepository(TestEntity);
    await repository.save({ name: "Test Data" });
  });
});
```

### Assertion Patterns
```typescript
// Use specific assertions
expect(response.status).to.equal(201);
expect(response.body).to.have.property("id");
expect(response.body.name).to.equal("Expected Name");

// Test array responses
expect(response.body.data).to.be.an("array");
expect(response.body.data).to.have.lengthOf.at.least(1);

// Test pagination metadata
expect(response.body.meta.pagination).to.deep.include({
  page: 1,
  limit: 10,
  total: expect.any(Number)
});
```

### Authentication Testing
```typescript
// Test protected endpoints
describe("Protected Endpoints", () => {
  it("should reject requests without token", async () => {
    await request(global.container.cradle.app)
      .get("/api/protected")
      .expect(401);
  });

  it("should reject requests with invalid token", async () => {
    await request(global.container.cradle.app)
      .get("/api/protected")
      .set("Authorization", "Bearer invalid-token")
      .expect(401);
  });
});
```


## Test Quality Requirements

### Mandatory Test Scenarios
- **CRUD operations**: Create, Read, Update, Delete for each entity
- **Validation**: Test all input validation (see error-handling.instructions.md)
- **Authentication**: Test protected endpoints with and without valid tokens
- **Authorization**: Test role-based access control where applicable
- **Pagination**: Test list endpoints with pagination parameters
- **Search and filtering**: Test query parameters and search functionality

### Test Naming Conventions
- Use descriptive test names that explain the expected behavior
- Start with "should" followed by the expected outcome
- Include context about input/conditions when relevant
- Group related tests using nested `describe` blocks

### Code Quality in Tests
- Keep tests focused and test only one thing per test case
- Use meaningful variable names and clear test data
- Avoid complex logic in tests - tests should be simple and readable
- Use helper functions for common test setup and assertions
- Maintain test code with the same quality standards as production code