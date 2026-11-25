---
name: ehyland
description: Eamon Hyland's opinionated tooling and conventions for TypeScript projects. Use when setting up new projects, configuring a linter, monorepos, library publishing, or when the user mentions Eamon's preferences.
metadata:
  author: Eamon Hyland
  version: "2026.2.08"
---

# Eamon Hyland's Preferences

| Category             | Preference                         |
| -------------------- | ---------------------------------- |
| Package Manager      | Bun for apps, pnpm for libraries   |
| Language             | TypeScript (strict mode, ESM only) |
| Linting & Formatting | Oxlint and Oxfmt                   |
| Testing              | Bun for apps, Vitest for libraries |
| Git Hooks            | simple-git-hooks + lint-staged     |
| Bundler              | Bun for apps, tsdown for libraries |

---

## Core Conventions

### Client-Server Communication

- Prefer tRPC with React Query for fullstack projects (when the server and client are in the same package). See [bun-trpc-setup](./references/bun-trpc-setup.md).
- Otherwise prefer GraphQL. See [bun-graphql-setup](./references/bun-graphql-setup.md).

### TypeScript

- Never use `@ts-ignore`
- Never use `as any` casting or `as unknown as <some-other-type>`

### Test Conventions

- Test files: `foo.ts` → `foo.test.ts` (same directory)
- Use `describe`/`it` API (not `test`)

---

## Core References

| Topic                      | Description                                     | Reference                                              |
| -------------------------- | ----------------------------------------------- | ------------------------------------------------------ |
| Server Configuration       | Environment variables and validation with Zod   | [server-config](./references/server-config.md)         |
| Package Scripts            | Recommended scripts for development and CI      | [scripts](./references/scripts.md)                     |
| Linting & Formatting       | Oxlint and Oxfmt configuration                  | [linting](./references/linting.md)                     |
| Git Hooks                  | Simple-git-hooks and lint-staged setup          | [git-hooks](./references/git-hooks.md)                 |
| Bun and tRPC SPA Setup     | Guidance for setting up a SPA with Bun and trpc | [bun-trpc-setup](./references/bun-trpc-setup.md)       |
| Bun and GraphQL Setup      | Configuration for Bun.serve with Yoga GraphQL   | [bun-graphql-setup](./references/bun-graphql-setup.md) |
| SQLite with Drizzle        | SQLite setup with Drizzle ORM in Bun runtime    | [sqlite-drizzle](./references/sqlite-drizzle.md)       |
| Deployment and CI/CD Setup | Buildkite pipelines, docker configuration       | [deployment](./references/deployment.md)               |
