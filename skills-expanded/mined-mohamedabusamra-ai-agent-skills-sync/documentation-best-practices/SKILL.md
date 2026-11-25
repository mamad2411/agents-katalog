---
name: documentation-best-practices
description: Write comprehensive documentation including code comments, API documentation, README files, and architecture documentation. Use when documenting code, writing README files, creating API docs, or when the user asks about documentation, comments, or code documentation.
---

# Documentation Best Practices

Write clear, comprehensive documentation that helps developers understand and use your code effectively.

## Code Comments

### When to Comment

**✅ Good - Explain why, not what:**

```typescript
// Use exponential backoff to handle transient network failures
// This prevents overwhelming the server during outages
async function retryWithBackoff(fn: () => Promise<any>) {
  // ...
}

// ❌ Bad - Obvious comments
// Increment counter by 1
counter++;
```

**✅ Good - Document complex logic:**

```typescript
/**
 * Calculates the delivery fee based on distance and order value.
 *
 * Fee structure:
 * - Base fee: $5 for orders under $50
 * - Distance fee: $0.50 per km after first 5km
 * - Free delivery for orders over $100
 */
function calculateDeliveryFee(distance: number, orderValue: number): number {
  // ...
}
```

**✅ Good - Document function parameters and return values:**

```typescript
/**
 * Creates a new user account with email verification.
 *
 * @param userData - User registration data
 * @param userData.email - Valid email address (will be verified)
 * @param userData.password - Password (min 8 chars, will be hashed)
 * @param userData.name - User's full name
 * @returns Promise resolving to created user object
 * @throws {ValidationError} If email is invalid or password too weak
 * @throws {ConflictError} If email already exists
 */
async function createUser(userData: CreateUserData): Promise<User> {
  // ...
}
```

### JSDoc Comments

```typescript
/**
 * Service for managing user orders.
 *
 * @class OrderService
 */
class OrderService {
  /**
   * Creates a new order for a user.
   *
   * @param {CreateOrderData} orderData - Order creation data
   * @param {number} orderData.storeId - Store ID
   * @param {OrderItem[]} orderData.items - Order items
   * @param {number} orderData.longitude - Delivery longitude
   * @param {number} orderData.latitude - Delivery latitude
   * @returns {Promise<Order>} Created order
   * @throws {ValidationError} If order data is invalid
   * @throws {NotFoundError} If store doesn't exist
   *
   * @example
   * const order = await orderService.createOrder({
   *   storeId: 1,
   *   items: [{ productId: 1, quantity: 2 }],
   *   longitude: -122.4194,
   *   latitude: 37.7749
   * });
   */
  async createOrder(orderData: CreateOrderData): Promise<Order> {
    // ...
  }
}
```

## API Documentation

### Swagger/OpenAPI Documentation

```typescript
/**
 * @swagger
 * /users:
 *   post:
 *     summary: Create a new user
 *     description: Creates a new user account with email verification
 *     tags: [Users]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - email
 *               - password
 *               - name
 *             properties:
 *               email:
 *                 type: string
 *                 format: email
 *                 example: user@example.com
 *               password:
 *                 type: string
 *                 format: password
 *                 minLength: 8
 *                 example: SecurePass123!
 *               name:
 *                 type: string
 *                 minLength: 1
 *                 maxLength: 100
 *                 example: John Doe
 *     responses:
 *       201:
 *         description: User created successfully
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/User'
 *       400:
 *         description: Validation error
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Error'
 *       409:
 *         description: User already exists
 */
router.post("/users", createUser);
```

### API Response Examples

```typescript
/**
 * @swagger
 * components:
 *   schemas:
 *     User:
 *       type: object
 *       properties:
 *         id:
 *           type: integer
 *           example: 1
 *         email:
 *           type: string
 *           format: email
 *           example: user@example.com
 *         name:
 *           type: string
 *           example: John Doe
 *         createdAt:
 *           type: string
 *           format: date-time
 *           example: 2024-01-01T00:00:00Z
 *     Error:
 *       type: object
 *       properties:
 *         error:
 *           type: object
 *           properties:
 *             message:
 *               type: string
 *               example: Validation failed
 *             code:
 *               type: string
 *               example: VALIDATION_ERROR
 *             errors:
 *               type: object
 *               additionalProperties:
 *                 type: array
 *                 items:
 *                   type: string
 */
```

## README Files

### Project README Structure

```markdown
# Project Name

Brief description of what the project does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Prerequisites

- Node.js 18+
- PostgreSQL 14+
- Redis 6+

## Installation

\`\`\`bash
npm install
cp .env.example .env
npm run migrate
npm run seed
\`\`\`

## Configuration

Create a `.env` file with the following variables:

\`\`\`
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
JWT_SECRET=your-secret-key
REDIS_URL=redis://localhost:6379
\`\`\`

## Usage

\`\`\`bash

# Development

npm run dev

# Production

npm start

# Run tests

npm test
\`\`\`

## API Documentation

API documentation is available at `/api-docs` when the server is running.

## Project Structure

\`\`\`
src/
├── controllers/ # Request handlers
├── services/ # Business logic
├── models/ # Database models
├── routes/ # Route definitions
├── middlewares/ # Express middlewares
└── utils/ # Utility functions
\`\`\`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## License

MIT
```

## Architecture Documentation

### Architecture Decision Records (ADRs)

```markdown
# ADR-001: Use Repository Pattern for Data Access

## Status

Accepted

## Context

We need to abstract database access to make the codebase more testable and allow for easier database migrations.

## Decision

We will implement the Repository pattern for all data access operations.

## Consequences

### Positive

- Easier to test (can mock repositories)
- Database-agnostic business logic
- Clear separation of concerns

### Negative

- Additional abstraction layer
- More boilerplate code

## Alternatives Considered

- Direct ORM usage in services (rejected - harder to test)
- Active Record pattern (rejected - too tightly coupled)
```

### System Architecture Diagram

```markdown
## System Architecture

\`\`\`
┌─────────────┐
│ Client │
└──────┬──────┘
│
▼
┌─────────────┐
│ API Gateway│
└──────┬──────┘
│
▼
┌─────────────┐ ┌─────────────┐
│ Auth │────▶│ Users │
│ Service │ │ Service │
└─────────────┘ └─────────────┘
│
▼
┌─────────────┐
│ Database │
└─────────────┘
\`\`\`
```

## Code Documentation Standards

### File Headers

```typescript
/**
 * @fileoverview User service for managing user operations
 * @module services/UserService
 * @author Your Name
 * @since 2024-01-01
 */

import { User } from "../models/User";
```

### Type Documentation

```typescript
/**
 * User creation data
 *
 * @interface CreateUserData
 */
interface CreateUserData {
  /** User's email address (must be unique) */
  email: string;

  /** User's password (min 8 characters) */
  password: string;

  /** User's full name */
  name: string;

  /** User's age (optional) */
  age?: number;
}
```

### Complex Algorithm Documentation

```typescript
/**
 * Implements the A* pathfinding algorithm to find the shortest route
 * between two points on a map.
 *
 * Algorithm steps:
 * 1. Initialize open and closed sets
 * 2. Add start node to open set
 * 3. While open set is not empty:
 *    a. Get node with lowest f-score
 *    b. If goal reached, reconstruct path
 *    c. Add current to closed set
 *    d. Check all neighbors
 * 4. Return path or null if no path exists
 *
 * @param start - Starting coordinates
 * @param goal - Goal coordinates
 * @param map - Map data with obstacles
 * @returns Array of coordinates representing the path
 *
 * @see https://en.wikipedia.org/wiki/A*_search_algorithm
 */
function findPath(start: Point, goal: Point, map: Map): Point[] | null {
  // Implementation
}
```

## Best Practices

1. **Document why, not what** - Code should be self-explanatory
2. **Keep comments up to date** - Outdated comments are worse than none
3. **Use JSDoc for public APIs** - Document all exported functions/classes
4. **Include examples** - Show how to use the code
5. **Document edge cases** - Explain unusual behavior
6. **Keep README updated** - First thing developers see
7. **Document architecture decisions** - Use ADRs
8. **Use consistent format** - Follow team conventions
9. **Document breaking changes** - In changelog or migration guide
10. **Review documentation** - As part of code review

## When Writing Documentation

1. **Write for your audience** - Consider who will read it
2. **Be concise but complete** - Don't over-document obvious code
3. **Use examples** - Show real usage scenarios
4. **Keep it updated** - Documentation that's wrong is harmful
5. **Document public APIs** - All exported functions/classes
6. **Explain complex logic** - Algorithms, business rules
7. **Include error cases** - What can go wrong
8. **Use diagrams** - For architecture and flows
9. **Provide migration guides** - For breaking changes
10. **Make it searchable** - Use clear headings and structure
