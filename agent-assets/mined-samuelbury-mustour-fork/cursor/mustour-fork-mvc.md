---
description: use this rule to structure the back end
globs: 
---
rules:
  - name: Enforce Clean MVC-style Backend Architecture in Next.js
    appliesTo:
      - /app/api/**
      - /actions/*.ts      # Server Actions files should be placed directly under /actions, no subfolders
    description: |
      Apply a modular and maintainable backend pattern across both API routes and Server Actions in Next.js.

      🔹 Controllers:
        - API route controllers: /app/api/[resource]/route.ts
        - Server Actions: /actions/[action].ts  # Always place files directly under /actions
        - Responsible for: input validation (with Zod or similar), calling services only.

      🔹 Services:
        - Located in /services/[resource]/*.service.ts
        - Responsible for: business logic, conditional flows, coordination between components.
        - Must not perform DB access or input validation.

      🔹 Repositories:
        - Located in /repository/[resource]/queries.ts and /repository/[resource]/mutations.ts
        - Must contain only pure functions that interact with the DB or external APIs.
        - No business logic or input validation allowed.

      🔹 Validation:
        - Input validation (e.g., using Zod) must be performed only in controllers (API routes or Server Actions).
        - Services and repositories must assume data is already validated.

    enforcement:
      - No direct DB or Prisma access inside `/app/**` or `/services/**`
      - No input parsing/validation inside `/services/**` or `/repository/**`
      - Only `/app/api/**` and `/actions/*.ts` may perform validation
      - `/repository/**` must only include `queries.ts` and `mutations.ts` per entity

    exampleStructure:
      /app
        /api
          /users
            route.ts        # Controller (API)
      /actions
        submitUser.ts      # Controller (Server Action), placed directly here
      /services
        /users
          user.service.ts  # Business logic
      /repository
        /users
          queries.ts       # All read DB logic
          mutations.ts     # All write DB logic
      /types
        user.ts            # Zod schemas for validation (used in controllers)

