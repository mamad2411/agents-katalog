---
name: prisma-postgres
description: Prisma Postgres setup and operations — Console, create-db CLI, Management API, and the TypeScript SDK. Use when provisioning Prisma Postgres databases, linking a local project, or integrating programmatic provisioning with service tokens or OAuth.
---

# Prisma Postgres

Guidance for creating, managing, and integrating Prisma Postgres across interactive and programmatic workflows.

## Core Workflows

### 1. Console-first workflow

Use Prisma Console for manual setup and operations:

- Open `https://console.prisma.io`
- Create/select workspace and project
- Use Studio in the project sidebar to view/edit data
- Retrieve direct connection details from the project UI

### 2. Quick provisioning with create-db

Use `create-db` when you need a database immediately:

```bash
npx create-db@latest
```

Aliases:

```bash
npx create-pg@latest
npx create-postgres@latest
```

For app integrations, you can also use the programmatic API (`create()` / `regions()`) from the `create-db` npm package.

Temporary databases auto-delete after ~24 hours unless claimed.

### 3. Link an existing local project

Use `prisma postgres link` when the database already exists and you want to wire a local project to it:

```bash
prisma postgres link
```

For CI or other non-interactive environments:

```bash
prisma postgres link --api-key "<your-api-key>" --database "db_..."
```

This flow updates your local `.env` with `DATABASE_URL`, then you can run `prisma generate` and `prisma migrate dev`.

### 4. Programmatic provisioning with Management API

Use API endpoints on:

```text
https://api.prisma.io/v1
```

Explore the schema and endpoints using:

- OpenAPI docs: `https://api.prisma.io/v1/doc`
- Swagger Editor: `https://api.prisma.io/v1/swagger-editor`

Auth options:

- Service token (workspace server-to-server)
- OAuth 2.0 (act on behalf of users)

### 5. Type-safe integration with Management API SDK

Install and use:

```bash
npm install @prisma/management-api-sdk
```

Use `createManagementApiClient` for existing tokens, or `createManagementApiSdk` for OAuth + token refresh.

## References

Read a reference only when the task needs that depth:

- [`references/create-db-cli.md`](references/create-db-cli.md) — instant databases and current CLI flags (`--ttl`, `--copy`, `--quiet`, `--open`) · read for fast setup.
- [`references/management-api.md`](references/management-api.md) — service-token and OAuth API workflows · read for programmatic provisioning.
- [`references/management-api-sdk.md`](references/management-api-sdk.md) — typed SDK usage with token storage · read when integrating from TypeScript/JavaScript.
- [`references/console-and-connections.md`](references/console-and-connections.md) — Console operations, `prisma postgres link`, direct TCP connections, serverless-driver choices.
