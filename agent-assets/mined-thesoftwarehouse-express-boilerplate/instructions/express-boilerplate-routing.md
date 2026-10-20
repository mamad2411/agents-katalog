---
applyTo: "**/routing.ts"
---

# Routing Instructions

## Overview
Routing in this application follows a hierarchical structure that separates concerns and enables modular development. The routing system consists of three main layers:
1. **Feature Routing** (`src/app/features/{feature}/routing.ts`) - Individual feature endpoints
2. **Global Routing** (`src/app/router.ts`) - Feature registration and global routes
3. **Application Routing** (`src/app/app.ts`) - Application-wide middleware and configuration

**CRITICAL REQUIREMENTS**:
- All routes are automatically tested through REST API integration tests
- Follow RESTful conventions for HTTP methods and paths
- Use middleware for validation, authentication, and request processing
- Maintain consistent route structure across features

## Routing Hierarchy

### Feature Routing Pattern
Each feature has its own routing file that defines endpoints and their middleware:

```typescript
import express from "express";
import { Action } from "../../../shared/http/types";

// Import validation middleware
import { createUserActionValidation } from "./actions/create-user.action";
import { getUserActionValidation } from "./actions/get-user.action";
import { getUsersActionValidation } from "./actions/get-users.action";
import { updateUserActionValidation } from "./actions/update-user.action";
import { deleteUserActionValidation } from "./actions/delete-user.action";

export interface UsersRoutingDependencies {
  createUserAction: Action;
  getUserAction: Action;
  getUsersAction: Action;
  updateUserAction: Action;
  deleteUserAction: Action;
}

export const usersRouting = (actions: UsersRoutingDependencies) => {
  const router = express.Router();

  // List endpoint - GET /
  router.get(
    "/",
    [getUsersActionValidation],
    actions.getUsersAction.invoke.bind(actions.getUsersAction)
  );

  // Create endpoint - POST /
  router.post(
    "/",
    [createUserActionValidation],
    actions.createUserAction.invoke.bind(actions.createUserAction)
  );

  // Single item endpoint - GET /:id
  router.get(
    "/:id",
    [getUserActionValidation],
    actions.getUserAction.invoke.bind(actions.getUserAction)
  );

  // Update endpoint - PUT /:id
  router.put(
    "/:id",
    [updateUserActionValidation],
    actions.updateUserAction.invoke.bind(actions.updateUserAction)
  );

  // Delete endpoint - DELETE /:id
  router.delete(
    "/:id",
    [deleteUserActionValidation],
    actions.deleteUserAction.invoke.bind(actions.deleteUserAction)
  );

  return router;
};
```

### Global Routing Registration
Register feature routes in `src/app/router.ts`:

```typescript
import express from "express";

export interface RoutingDependencies {
  usersRouting: express.Router;
  ordersRouting: express.Router;
  productsRouting: express.Router;
}

export const createRouter = ({
  usersRouting,
  ordersRouting,
  productsRouting,
}: RoutingDependencies) => {
  const router = express.Router();

  // Register feature routes with descriptive paths
  router.use("/users", usersRouting);
  router.use("/orders", ordersRouting);
  router.use("/products", productsRouting);

  return router;
};
```

### Container Registration
Register routing dependencies in `src/container/routing.ts`:

```typescript
import { AwilixContainer, Lifetime, asClass, asFunction } from "awilix";
import { usersRouting } from "../app/features/users/routing";
import { ordersRouting } from "../app/features/orders/routing";

export async function registerRouting(container: AwilixContainer) {
  // Auto-load all action classes
  container.loadModules(["src/app/**/*.action.js"], {
    formatName: "camelCase",
    resolverOptions: {
      lifetime: Lifetime.SCOPED,
      register: asClass,
    },
  });

  // Register routing functions
  container.register({
    usersRouting: asFunction(usersRouting),
    ordersRouting: asFunction(ordersRouting),
  });

## RESTful Route Conventions

### Standard HTTP Methods and Paths
Follow these conventions for consistent API design:

| Operation | Method | Path | Example | Purpose |
|-----------|--------|------|---------|---------|
| List | `GET` | `/` | `GET /users` | Retrieve paginated list |
| Create | `POST` | `/` | `POST /users` | Create new resource |
| Read | `GET` | `/:id` | `GET /users/123` | Retrieve single resource |
| Update | `PUT` | `/:id` | `PUT /users/123` | Update entire resource |
| Partial Update | `PATCH` | `/:id` | `PATCH /users/123` | Update specific fields |
| Delete | `DELETE` | `/:id` | `DELETE /users/123` | Remove resource |

### Route Order Importance
Order routes from most specific to least specific:

```typescript
export const usersRouting = (actions: UsersRoutingDependencies) => {
  const router = express.Router();

  // Specific routes first
  router.post("/bulk", actions.bulkCreateUsersAction.invoke.bind(actions.bulkCreateUsersAction));
  router.get("/search", actions.searchUsersAction.invoke.bind(actions.searchUsersAction));
  
  // Standard CRUD routes
  router.get("/", actions.getUsersAction.invoke.bind(actions.getUsersAction));
  router.post("/", actions.createUserAction.invoke.bind(actions.createUserAction));
  
  // Parameterized routes last
  router.get("/:id", actions.getUserAction.invoke.bind(actions.getUserAction));
  router.put("/:id", actions.updateUserAction.invoke.bind(actions.updateUserAction));
  router.delete("/:id", actions.deleteUserAction.invoke.bind(actions.deleteUserAction));

  return router;
};
```

## Middleware Integration

### Validation Middleware
Always include validation middleware for each endpoint:

```typescript
// Single validation middleware
router.post(
  "/",
  [createUserActionValidation],
  actions.createUserAction.invoke.bind(actions.createUserAction)
);

// Multiple middleware chain
router.put(
  "/:id",
  [
    authenticationMiddleware,        // Check if user is logged in
    updateUserActionValidation,      // Validate request data
    authorizationMiddleware,         // Check if user can update
  ],
  actions.updateUserAction.invoke.bind(actions.updateUserAction)
);
```

### Authentication and Authorization
Add security middleware for protected endpoints:

```typescript
import { authenticateToken } from "../../../middleware/auth.middleware";
import { authorizeRole } from "../../../middleware/role.middleware";

export const usersRouting = (actions: UsersRoutingDependencies) => {
  const router = express.Router();

  // Public endpoints (no auth required)
  router.post("/register", [registerUserActionValidation], actions.registerUserAction.invoke.bind(actions.registerUserAction));
  router.post("/login", [loginActionValidation], actions.loginAction.invoke.bind(actions.loginAction));

  // Protected endpoints (auth required)
  router.get(
    "/",
    [authenticateToken, getUsersActionValidation],
    actions.getUsersAction.invoke.bind(actions.getUsersAction)
  );

  // Admin-only endpoints
  router.delete(
    "/:id",
    [
      authenticateToken,
      authorizeRole(['admin']),
      deleteUserActionValidation
    ],
    actions.deleteUserAction.invoke.bind(actions.deleteUserAction)
  );

  return router;
};
```

## Advanced Routing Patterns

### Nested Resources
Handle nested resource relationships:

```typescript
// For routes like /users/:userId/orders
export const userOrdersRouting = (actions: UserOrdersRoutingDependencies) => {
  const router = express.Router({ mergeParams: true }); // Important for nested params

  router.get("/", [getUserOrdersActionValidation], actions.getUserOrdersAction.invoke.bind(actions.getUserOrdersAction));
  router.post("/", [createUserOrderActionValidation], actions.createUserOrderAction.invoke.bind(actions.createUserOrderAction));
  router.get("/:orderId", [getUserOrderActionValidation], actions.getUserOrderAction.invoke.bind(actions.getUserOrderAction));

  return router;
};

// In main router
router.use("/users/:userId/orders", userOrdersRouting);
```

### Versioned APIs
Support API versioning:

```typescript
// src/app/router.ts
export const createRouter = ({ v1Router, v2Router }: RoutingDependencies) => {
  const router = express.Router();

  router.use("/v1", v1Router);
  router.use("/v2", v2Router);
  
  // Default to latest version
  router.use("/", v2Router);

  return router;
};
```

### Query Parameter Routing
Handle complex query parameters:

```typescript
// Routes with different behavior based on query params
router.get(
  "/",
  [getUsersActionValidation],
  (req, res, next) => {
    // Route to different actions based on query params
    if (req.query.export === 'csv') {
      return actions.exportUsersAction.invoke(req, res, next);
    }
    return actions.getUsersAction.invoke(req, res, next);
  }
);
```

## Application Integration

### Main Application Setup
Routes are integrated in `src/app/app.ts`:

```typescript
// All feature routes are prefixed with /api
app.use("/api", router);

// Results in URLs like:
// POST /api/users
// GET /api/users/123
// PUT /api/orders/456
```

### Health Check and Documentation
Standard endpoints are configured at application level:

```typescript
// Health check endpoint
app.get("/health", (req, res) => {
  res.status(200).json({ status: "ok" });
});

// API documentation
app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// GraphQL endpoint
app.use("/graphql", graphQLMiddleware);
```

## Best Practices

### Route Organization
- **Feature-based**: Group routes by business feature, not technical concern
- **Consistent naming**: Use plural nouns for resources (`/users`, not `/user`)
- **Hierarchical**: Organize nested resources logically
- **Descriptive paths**: Use clear, descriptive route paths

### Middleware Best Practices
- **Order matters**: Place authentication before authorization
- **Validation first**: Validate input before processing
- **Reusable middleware**: Create reusable middleware functions

### Security Considerations
- **Authentication**: Protect sensitive endpoints
- **Authorization**: Check user permissions
- **Rate limiting**: Add rate limiting for public endpoints
- **Input validation**: Always validate incoming data

### Performance Optimization
- **Route caching**: Cache responses for expensive operations
- **Compression**: Use compression middleware
- **Static files**: Serve static files efficiently
- **Connection pooling**: Optimize database connections

### Testing Integration
Routes are tested through integration tests:

```typescript
describe("Users API", () => {
  it("should create user via POST /api/users", async () => {
    await request(app)
      .post("/api/users")
      .send({ name: "John Doe", email: "john@example.com" })
      .expect(201);
  });

  it("should get user via GET /api/users/:id", async () => {
    const user = await createTestUser();
    await request(app)
      .get(`/api/users/${user.id}`)
      .expect(200)
      .expect(res => {
        expect(res.body.id).to.equal(user.id);
      });
  });
});
```

This routing structure ensures scalable, maintainable, and testable API endpoints while following REST conventions and security best practices.
