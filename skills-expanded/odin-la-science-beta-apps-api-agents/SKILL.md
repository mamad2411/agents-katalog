# OLS Backend — AGENTS.md

Inherits the root [AGENTS.md](../../AGENTS.md).

**MANDATORY**: read [CONVENTIONS.md](CONVENTIONS.md) before changing any code.

## Landmarks

- **Auth**: `src/auth/` — JWT, sessions, OAuth (Google, CAS), MFA, guards, schedulers
- **Guards**: `src/auth/jwt-auth.guard.ts`, `src/auth/deny-guest.guard.ts`, `src/auth/throttler-behind-proxy.guard.ts`
- **Modules**: `src/modules/{module}/` — controller, service, module, dto/
- **Common**: `src/common/` — GlobalExceptionFilter, AuditLogInterceptor, circuit-breaker
- **ORM**: Prisma, `prisma/schema.prisma` — source of truth for the DB schema
- **Config**: `src/config/env.validation.ts` — environment variable validation (Zod, boot fail-fast)
- **Commands**: see [README.md](README.md)

## Where to find what

| Need                        | File                                                                      |
| --------------------------- | ------------------------------------------------------------------------- |
| Commands (build, test, dev) | [README.md](README.md)                                                    |
| Rules and conventions       | [CONVENTIONS.md](CONVENTIONS.md)                                          |
| DB schema                   | [prisma/schema.prisma](prisma/schema.prisma)                              |
| Generated OpenAPI schema    | [docs/openapi.json](docs/openapi.json)                                    |
| Module creation guide       | [module-creation-guide.md](../../docs/tutorials/module-creation-guide.md) |
