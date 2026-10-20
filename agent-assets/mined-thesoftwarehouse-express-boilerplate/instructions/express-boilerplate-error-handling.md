---
applyTo: "**/*.{ts,js}"
---

# Error Handling Instructions

## Overview
This application implements a comprehensive error handling strategy with global error handling middleware, structured error responses, and consistent error patterns across all layers. All errors flow through a centralized error handler to ensure consistent format and proper logging.

**CRITICAL REQUIREMENTS**:
- **ALL errors must flow through global error handler** in `src/middleware/error-handler.ts`
- Use predefined error classes for consistent error handling
- Never expose sensitive information in error messages
- All errors are logged using @tshio/logger with appropriate levels
- Maintain consistent JSON error response format

## Error Architecture

### Global Error Handler
All errors are processed through `src/middleware/error-handler.ts` which:
- Catches all thrown errors from actions, handlers, and middleware
- Transforms errors into consistent JSON responses
- Logs errors with appropriate severity levels
- Prevents sensitive information exposure
- Returns proper HTTP status codes

### Error Flow Pattern
```
Action/Handler/Middleware → Throws Error → Global Error Handler → JSON Response
```

## Error Classes and Usage

### Built-in Error Classes
Use error classes from `src/errors/` for consistent error handling:

```typescript
import { NotFoundError } from "../../../../shared/errors/not-found.error";
import { HttpError } from "../../../../shared/errors/http.error";
import { AppError } from "../../../../shared/errors/app.error";
```

### Error Class Guidelines

#### NotFoundError (404 Not Found)
Use for resources that don't exist:
```typescript
// In handlers
const user = await this.dependencies.userRepository.findOneBy({ 
  id: command.payload.id 
});

if (!user) {
  throw new NotFoundError("User not found");
}
```

#### HttpError (Custom HTTP Status)
Use for business logic violations with specific HTTP status codes:
```typescript
// Business logic validation
if (user.status === 'deleted') {
  throw new HttpError("Cannot update deleted user", 400);
}

// Authorization errors
if (!user.canAccess(resource)) {
  throw new HttpError("Access forbidden", 403);
}

// Conflict errors
if (emailAlreadyExists) {
  throw new HttpError("Email already in use", 409);
}
```

#### AppError (Internal Application Errors)
Reserved for internal application errors:
```typescript
// System-level errors
throw new AppError("Database connection failed");
```

## Error Handling by Layer

### Actions
Actions should throw errors directly and let the global error handler process them:

```typescript
export default class CreateUserAction implements Action {
  async invoke(req: Request, res: Response) {
    // Validation is handled by Celebrate middleware
    
    const result = await this.dependencies.commandBus.execute(
      new CreateUserCommand({
        name: req.body.name,
        email: req.body.email,
      })
    );
    
    // No try/catch needed - global error handler catches thrown errors
    res.status(StatusCodes.CREATED);
    res.json(result.result);
  }
}
```

#### Action Error Guidelines
- **Never use try/catch blocks** - let errors bubble up to global handler
- **Never return error responses manually** - throw errors instead
- **Focus on happy path logic** - error handling is automatic
- **Use appropriate error classes** for different scenarios

### Handlers (Business Logic)
Handlers contain business logic validation and should throw appropriate errors:

```typescript
export default class CreateUserHandler implements CommandHandler<CreateUserCommand> {
  async execute(command: CreateUserCommand) {
    this.dependencies.logger.info("Command CreateUser executed");

    const { name, email } = command.payload;

    const existingUser = await this.dependencies.userRepository.findOneBy({ email });

    if (!existingUser) {
        throw new HttpError("User not found", 404);
    }

    const userEntity = this.dependencies.userRepository.create({ name, email });
    const savedUser = await this.dependencies.userRepository.save(userEntity);

    return { result: savedUser };
  }
}
```

#### Handler Error Guidelines
- **Throw errors as exceptions**, not return them as responses
- **Use NotFoundError** for 404 errors
- **Use HttpError** for custom HTTP errors with specific status codes
- **Include meaningful error messages** for debugging
- **Log important business rule violations** if needed

## Input Validation

### Celebrate/Joi Validation
Input validation errors are automatically handled by Celebrate middleware:

```typescript
export const createUserActionValidation = celebrate(
  {
    body: Joi.object({
      email: Joi.string().email().required(),
      name: Joi.string().trim().min(2).max(50).required(),
    }),
  },
  { abortEarly: false }
);
```

### Validation Error Flow
1. Celebrate validates input against Joi schema
2. Validation failures are caught by global error handler
3. Proper 400 status with validation details returned
4. No manual validation error handling needed

### Business Logic Validation
Separate from input validation, business rules should be validated in handlers:

```typescript
// In handlers - business logic validation
if (user.orders.length > 0) {
  throw new HttpError("Cannot delete user with existing orders", 409);
}
```

## Security Considerations

### Sensitive Information Protection
- **Never expose database details** in error messages
- **Don't reveal internal system information** in responses
- **Use generic messages for authentication/authorization failures**
- **Log detailed errors server-side only**

### Secure Error Examples
```typescript
// Good - Generic message for production
if (!validCredentials) {
  throw new HttpError("Invalid credentials", 401);
}

// Bad - Exposes sensitive information
if (!user) {
  throw new Error("User with email john@example.com not found in users table");
}
```

## Testing Error Scenarios

### Integration Tests for Error Handling
Test error scenarios through API endpoints:

```typescript
describe("Error Handling", () => {
  it("should return 400 for validation errors", async () => {
    const response = await request(app)
      .post("/api/users")
      .send({ invalid: "data" })
      .expect(400);

    expect(response.body).to.have.property("error");
    expect(response.body.error).to.include("validation");
  });

  it("should return 404 for non-existent resources", async () => {
    const nonExistentId = "550e8400-e29b-41d4-a716-446655440000";
    await request(app)
      .get(`/api/users/${nonExistentId}`)
      .expect(404);
  });

  it("should handle business rule violations", async () => {
    const response = await request(app)
      .post("/api/users")
      .send({ email: "existing@example.com" })
      .expect(409);

    expect(response.body.error.message).to.include("already exists");
  });
});
```

### Unit Tests for Error Scenarios
Test error handling in utility functions:

```typescript
describe("Utility Function", () => {
  it("should throw error for invalid input", () => {
    expect(() => functionToTest(null)).to.throw("Expected error message");
  });

  it("should handle edge cases gracefully", () => {
    expect(() => functionToTest("")).to.throw("Invalid input");
  });
});
```

### Required Error Test Coverage
- **Validation errors**: Test all input validation rules and error responses
- **Authentication errors**: Test protected endpoints with and without valid tokens
- **Authorization errors**: Test role-based access control where applicable
- **Not found errors**: Test non-existent resource access
- **Business rule violations**: Test all business logic error scenarios
- **Edge cases**: Test boundary conditions and edge cases

## Best Practices

### Error Handling Guidelines
- **Single source of truth**: All errors flow through global error handler
- **Fail fast**: Validate and throw errors as early as possible
- **Meaningful messages**: Use descriptive error messages for debugging
- **Consistent format**: Use predefined error classes for consistency
- **Security first**: Never expose sensitive information in error responses

### Development Workflow
1. **Design error scenarios** when implementing features
2. **Use appropriate error classes** for different types of failures
3. **Test error paths** alongside success paths
4. **Monitor error logs** in development and production
5. **Refine error messages** based on user feedback and debugging needs

### Common Anti-patterns to Avoid
- **Manual error response creation** instead of throwing errors
- **Try/catch blocks in actions** that swallow errors
- **Returning error objects** instead of throwing exceptions
- **Exposing internal system details** in error messages
- **Inconsistent error response formats** across endpoints
