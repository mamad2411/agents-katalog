---
applyTo: "**/actions/*.action.ts"
---

# REST API Actions Instructions

## Purpose
Actions are thin controllers responsible for handling HTTP requests, validating input, and delegating business logic to handlers. They should not contain business logic themselves.

**CRITICAL REQUIREMENTS**:
- **ALL actions MUST have comprehensive integration tests** in `src/tests/` directory
- Integration tests MUST cover success scenarios, validation errors, and edge cases (see error-handling.instructions.md)
- NO action should be merged without corresponding integration tests

## Core Guidelines
- Every action must have a corresponding integration test.
- Always use `@tshio/command-bus` for command handlers and `@tshio/query-bus` for query handlers.
- Name action files descriptively (e.g., `create-user.action.ts`, `delete-user.action.ts`, `get-users.action.ts`).
- Use appropriate HTTP status codes (e.g., 200 for success, 201 for created, 204 for no content, 400 for bad request, 404 for not found, 500 for server error).
- Validate input using Celebrate/Joi before processing.
- Delegate business logic to handlers, not actions.
- Add logging for important events and errors using injected logger.
- Document the purpose of each action and expected input/output.

## List Endpoints
- Use `GET` for list endpoints.
- Use `src/shared/pagination-utils/pagination-utils.ts` for TypeORM options and pagination.
- Always return a JSON response using `makePaginationResult` function.
- Response includes `meta` and `data` fields with pagination, filter, sort, and search info.
- Example request: `GET /users?page=1&limit=10&sort[firstName]=ASC&filter[lastName]=Nowak&search=test`
- Example response:
```json
{
  "meta": {
    "pagination": {
      "page": 1,
      "total": 0,
      "limit": 10,
      "totalPages": 0
    },
    "filter": {
      "firstName": ["Ewa", "Adam"],
      "lastName": "Nowak"
    },
    "sort": {
      "firstName": "ASC"
    },
    "search": "test"
  },
  "data": [{ ... }]
}
```
- Use `filter[field]=value` for filtering, `sort[field]=ASC|DESC` for sorting, `search=term` for text search, and `page=1&limit=10` for pagination.

## Single Item Endpoints
- Use `GET` for single item endpoints.
- Use singular nouns for single item paths (e.g., `/users/123e4567-e89b-12d3-a456-426614174000`).
- Always return a JSON response with the item data.
- Example request: `GET /users/123e4567-e89b-12d3-a456-426614174000`
- Example response:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "firstName": "Ewa",
  "lastName": "Nowak",
  "email": "ewa.nowak@example.com"
}
```

## Example Actions

### Create Action (Command)
```typescript
import { celebrate, Joi } from "celebrate";
import { Request, Response } from "express";
import { CommandBus } from "@tshio/command-bus";
import { StatusCodes } from "http-status-codes";
import { CreateUserCommand } from "../commands/create-user.command";
import { Action } from "../../../../shared/http/types";

export const createUserActionValidation = celebrate(
  {
    headers: Joi.object(),
    body: Joi.object({
      name: Joi.string().required(),
      email: Joi.string().email().required(),
    }),
  },
  { abortEarly: false }
);

export interface CreateUserActionDependencies {
  commandBus: CommandBus;
}

class CreateUserAction implements Action {
  constructor(private dependencies: CreateUserActionDependencies) {}

  async invoke(req: Request, res: Response) {
    const result = await this.dependencies.commandBus.execute(
      new CreateUserCommand({
        name: req.body.name,
        email: req.body.email,
      })
    );
    
    res.status(StatusCodes.CREATED);
    res.json(result.result);
  }
}

export default CreateUserAction;
```

### Single Item Action (Query)
```typescript
import { celebrate, Joi } from "celebrate";
import { Request, Response } from "express";
import { QueryBus } from "@tshio/query-bus";
import { GetUserQuery } from "../queries/get-user.query";
import { Action } from "../../../../shared/http/types";

export const getUserActionValidation = celebrate(
  {
    headers: Joi.object(),
    params: Joi.object({
      id: Joi.string().uuid().required(),
    }),
  },
  { abortEarly: false }
);

export interface GetUserActionDependencies {
  queryBus: QueryBus<any>;
}

class GetUserAction implements Action {
  constructor(private dependencies: GetUserActionDependencies) {}

  async invoke(req: Request, res: Response) {
    const queryResult = await this.dependencies.queryBus.execute(
      new GetUserQuery({ id: req.params.id })
    );
    res.json(queryResult.result);
  }
}

export default GetUserAction;
```

### List Action (Query with Pagination)
```typescript
import { celebrate, Joi } from "celebrate";
import { Request, Response } from "express";
import { QueryBus } from "@tshio/query-bus";
import { UsersQuery } from "../queries/users.query";
import { Action } from "../../../../shared/http/types";

export const getUsersActionValidation = celebrate(
  {
    headers: Joi.object(),
    query: Joi.object({
      page: Joi.string().optional(),
      limit: Joi.string().optional(),
      sort: Joi.object().optional(),
      filter: Joi.object().optional(),
      search: Joi.string().optional(),
    }),
  },
  { abortEarly: false }
);

export interface GetUsersActionDependencies {
  queryBus: QueryBus<any>;
}

class GetUsersAction implements Action {
  constructor(private dependencies: GetUsersActionDependencies) {}

  async invoke(req: Request, res: Response) {
    const queryResult = await this.dependencies.queryBus.execute(
      new UsersQuery({
        ...req.query,
        page: Number(req.query.page),
        limit: Number(req.query.limit),
      })
    );
    res.json(queryResult.result);
  }
}

export default GetUsersAction;
```

### Update Action (Command)
```typescript
import { celebrate, Joi } from "celebrate";
import { Request, Response } from "express";
import { CommandBus } from "@tshio/command-bus";
import { UpdateUserCommand } from "../commands/update-user.command";
import { Action } from "../../../../shared/http/types";

export const updateUserActionValidation = celebrate(
  {
    headers: Joi.object(),
    params: Joi.object({
      id: Joi.string().uuid().required(),
    }),
    body: Joi.object({
      name: Joi.string().optional(),
      email: Joi.string().email().optional(),
    }),
  },
  { abortEarly: false }
);

export interface UpdateUserActionDependencies {
  commandBus: CommandBus;
}

class UpdateUserAction implements Action {
  constructor(private dependencies: UpdateUserActionDependencies) {}

  async invoke(req: Request, res: Response) {
    const result = await this.dependencies.commandBus.execute(
      new UpdateUserCommand({
        id: req.params.id,
        ...req.body,
      })
    );
    res.json(result.result);
  }
}

export default UpdateUserAction;
```

### Delete Action (Command)
```typescript
import { celebrate, Joi } from "celebrate";
import { Request, Response } from "express";
import { CommandBus } from "@tshio/command-bus";
import { StatusCodes } from "http-status-codes";
import { DeleteUserCommand } from "../commands/delete-user.command";
import { Action } from "../../../../shared/http/types";

export const deleteUserActionValidation = celebrate(
  {
    headers: Joi.object(),
    params: Joi.object({
      id: Joi.string().uuid().required(),
    }),
  },
  { abortEarly: false }
);

export interface DeleteUserActionDependencies {
  commandBus: CommandBus;
}

class DeleteUserAction implements Action {
  constructor(private dependencies: DeleteUserActionDependencies) {}

  async invoke(req: Request, res: Response) {
    await this.dependencies.commandBus.execute(
      new DeleteUserCommand({ id: req.params.id })
    );
    res.status(StatusCodes.NO_CONTENT).send();
  }
}

export default DeleteUserAction;
```

## Advanced Patterns

### Input Sanitization and Transformation
Use Joi custom methods for input transformation:

```typescript
export const createUserActionValidation = celebrate(
  {
    body: Joi.object({
      email: Joi.string().email().lowercase().trim().required(),
      name: Joi.string().trim().min(2).max(50).required(),
    }),
  },
  { abortEarly: false }
);
```

### Complex Filtering for List Endpoints
For advanced filtering, extend validation patterns:

```typescript
export const getUsersActionValidation = celebrate(
  {
    query: Joi.object({
      // Pagination
      page: Joi.string().optional(),
      limit: Joi.string().optional(),
      
      // Sorting - single or multiple fields
      sort: Joi.object().pattern(
        Joi.string(), 
        Joi.string().valid('ASC', 'DESC')
      ).optional(),
      
      // Filtering - exact matches
      filter: Joi.object().pattern(
        Joi.string(),
        Joi.alternatives().try(
          Joi.string(),
          Joi.array().items(Joi.string())
        )
      ).optional(),
      
      // Text search across multiple fields
      search: Joi.string().min(3).optional(),
    }),
  },
  { abortEarly: false }
);
```

## Testing Requirements

**MANDATORY**: Every action MUST have comprehensive integration tests.

### Integration Test Structure
Create tests in `src/tests/` directory following this pattern:

```typescript
import { expect } from "chai";
import "mocha";
import request from "supertest";

describe("/api/users integration", () => {
  beforeEach(async () => {
    // Clear database before each test
    // Use your database clearing utility
  });

  describe("POST /api/users", () => {
    it("should create user with valid data", async () => {
      const userData = {
        name: "John Doe",
        email: "john.doe@example.com"
      };

      return request(await global.container.cradle.app)
        .post("/api/users")
        .send(userData)
        .expect(201)
        .then((response) => {
          expect(response.body).to.have.property("id");
          expect(response.body.name).to.equal(userData.name);
          expect(response.body.email).to.equal(userData.email);
        });
    });

    it("should return 400 for invalid email", async () => {
      const userData = {
        name: "John Doe",
        email: "invalid-email"
      };

      return request(await global.container.cradle.app)
        .post("/api/users")
        .send(userData)
        .expect(400);
    });

    it("should return 400 for missing required fields", async () => {
      return request(await global.container.cradle.app)
        .post("/api/users")
        .send({})
        .expect(400);
    });
  });

  describe("GET /api/users", () => {
    it("should return paginated users list", async () => {
      return request(await global.container.cradle.app)
        .get("/api/users?page=1&limit=10")
        .expect(200)
        .then((response) => {
          expect(response.body).to.have.property("meta");
          expect(response.body).to.have.property("data");
          expect(response.body.meta).to.have.property("pagination");
        });
    });

    it("should filter users by search term", async () => {
      return request(await global.container.cradle.app)
        .get("/api/users?search=john")
        .expect(200);
    });
  });

  describe("GET /api/users/:id", () => {
    it("should return specific user", async () => {
      // First create a user, then fetch it
      const createResponse = await request(await global.container.cradle.app)
        .post("/api/users")
        .send({ name: "Test User", email: "test@example.com" });

      return request(await global.container.cradle.app)
        .get(`/api/users/${createResponse.body.id}`)
        .expect(200)
        .then((response) => {
          expect(response.body.id).to.equal(createResponse.body.id);
        });
    });

    it("should return 404 for non-existent user", async () => {
      const nonExistentId = "550e8400-e29b-41d4-a716-446655440000";
      return request(await global.container.cradle.app)
        .get(`/api/users/${nonExistentId}`)
        .expect(404);
    });
  });
});
```

### Test Coverage Requirements
Your tests MUST cover:
- ✅ Success scenarios for all endpoints
- ✅ Validation errors (400 responses)
- ✅ Not found errors (404 responses)  
- ✅ Authentication/authorization errors (if applicable)
- ✅ Edge cases and boundary conditions
- ✅ Pagination and filtering functionality

## Best Practices
- Keep actions minimal and focused on request/response logic.
- Always validate input before processing.
- Use dependency injection to resolve handlers.
- Throw errors directly; rely on global error handling.
- Use consistent response formats across all endpoints.
- Follow RESTful conventions for HTTP methods and status codes.
- Include comprehensive integration tests for every action.
- Use appropriate HTTP status codes from `http-status-codes` package.

## GraphQL Actions
If your project supports GraphQL, resolvers should follow similar principles: validate input, delegate to handlers, and format responses.
