---
name: Elysia Modular Backend Skill
description: A Claude skill to scaffold production-grade modular backends with Elysia.js. Generates typed routes, validation schemas, and service layers following clean architecture principles.
coverImage: /images/ai-files/elysia-modular-backend-skill/coverImage.jpeg
repoLink: https://github.com/theoxys/mpires-dev
installCommand: npx claude skills add @theoxys/elysia-modular-backend
---

# Elysia Modular Backend Skill

A Claude skill that helps you build modular, type-safe backends with [Elysia.js](https://elysiajs.com/) — the TypeScript-first Bun web framework known for its end-to-end type safety and developer ergonomics.

## What it does

- Scaffolds route modules with full TypeScript inference
- Generates TypeBox validation schemas from plain English descriptions
- Creates a service layer separating business logic from transport
- Wires dependency injection with Elysia's plugin system
- Generates OpenAPI docs automatically from route definitions

## Installation

```bash
npx claude skills add @theoxys/elysia-modular-backend
```

Then in Claude Code:

```
/elysia-modular-backend create user authentication module with JWT
```

## Example

Given: *"Create a user module with register, login, and profile endpoints"*

The skill generates a complete, working module:

```typescript
// modules/user/user.routes.ts
import { Elysia, t } from 'elysia'
import { UserService } from './user.service'
import { jwtPlugin } from '../plugins/jwt'

export const userRoutes = new Elysia({ prefix: '/users' })
  .use(jwtPlugin)
  .post('/register', async ({ body }) => UserService.register(body), {
    body: t.Object({
      email: t.String({ format: 'email' }),
      password: t.String({ minLength: 8 }),
      name: t.String()
    })
  })
  .post('/login', async ({ body, jwt }) => {
    const user = await UserService.login(body)
    return { token: await jwt.sign({ userId: user.id }) }
  }, {
    body: t.Object({
      email: t.String({ format: 'email' }),
      password: t.String()
    })
  })
  .get('/me', ({ user }) => user, {
    beforeHandle: [({ user, set }) => {
      if (!user) { set.status = 401; return 'Unauthorized' }
    }]
  })
```

## Architecture principles

- **Separation of concerns** — routes, services, and repositories as distinct layers
- **Schema-first** — TypeBox schemas drive both validation and type inference simultaneously
- **Plugin composition** — each module is an Elysia plugin, making it independently testable
- **Explicit over magic** — no decorators or hidden wiring; readable by any TypeScript developer

## When to use this

Best fit for teams wanting a Bun-native API that prioritizes type safety end-to-end (from DB query to HTTP response) without the ceremony of NestJS or the limitations of Express.
