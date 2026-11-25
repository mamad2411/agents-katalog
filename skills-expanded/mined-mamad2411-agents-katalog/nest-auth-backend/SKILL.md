---
name: nest-auth-backend
description: >-
  Conventions for the NestJS + MongoDB backend in this repo: module layout, repository ports and
  adapters, the global JWT guard, the session/refresh-token model, validation and error handling.
  Use whenever adding or changing an endpoint, module, DTO, persistence code, or anything in the
  auth flow under backend/.
---

# NestJS auth backend conventions

NestJS **12**, native **ESM** (`"type": "module"`, `nodenext`). Relative imports must end in
`.js` (`import { X } from './x.js'`). Tests run on Vitest. See ADR-0006.

## Module shape

```
modules/<feature>/
  domain/                 plain TS types + domain errors (no Nest, no Mongoose)
  dto/                    class-validator request DTOs + Swagger response DTOs
  <feature>.repository.ts abstract class = port AND DI token
  infrastructure/
    mongoose/             schema + adapter (extends the port)
    in-memory/            Map-backed adapter with identical behaviour (tests / demo)
  <feature>.service.ts    use-case logic, depends on the port only
  <feature>.controller.ts thin: DTO in -> service -> response DTO out
  <feature>.module.ts
```

Bind new ports in `persistence/persistence.module.ts` for **both** drivers. Never import a
Mongoose model outside `infrastructure/mongoose`.

## Endpoint checklist

1. DTO with class-validator rules + `@ApiProperty` examples. Use shared transforms (`toNormalizedEmail`, `trimString`).
2. Controller method with `@ApiOperation` and one `@Api*Response({ type: ErrorResponseDto })` per error status.
3. Protected by default. Add `@Public()` only for anonymous routes. Read the user with `@CurrentUser()`.
4. Credential endpoints sit under `AuthController` (already `@UseGuards(ThrottlerGuard)`).
5. Throw `HttpException` subclasses. Map domain errors (e.g. `EmailAlreadyTakenError` -> 409) in the service.
6. Responses go through mappers (`toPublicUser`). Never return a raw domain/DB object containing hashes.

## Session model (don't weaken it)

- Access JWT: 15m, body only, `JWT_ACCESS_SECRET`, HS256 pinned.
- Refresh JWT: 7d, httpOnly SameSite=Strict cookie at `/api/auth`, `JWT_REFRESH_SECRET`.
- Only `sha256(refresh)` is stored. Rotation goes through `rotateRefreshTokenHash` (compare-and-swap). A failed swap means reuse: revoke (`setRefreshTokenHash(id, null)`) and return 401.
- Sign-in: always call `hasher.verify(user?.passwordHash, pw)` (dummy hash path) and use one generic error.

## Security rules

- `ValidationPipe` is `whitelist + forbidNonWhitelisted + transform`. Don't loosen it per route.
- Queries with user input use `$eq` or typed values. Never spread request bodies into queries.
- New secrets/config: Joi schema in `config/env.validation.ts` (wired through `ConfigModule.validate`) + `configuration.ts` + `.env.example` + `docs/deployment.md`.
- API surface changed? Run `npm run openapi` and commit the updated contract (`npm run openapi:check` fails on drift).
- Log with the Nest `Logger` (pino-backed) using structured objects: `logger.warn({ userId }, 'msg')`. Never log passwords, tokens or hashes.

## Anti-patterns (reject in review)

- Business logic in controllers or adapters.
- `@InjectModel` in a service.
- `@Public()` on anything that reads user data.
- Returning different errors for "unknown email" and "wrong password".
- Storing raw refresh tokens, or putting the access token in a cookie readable by JS.
