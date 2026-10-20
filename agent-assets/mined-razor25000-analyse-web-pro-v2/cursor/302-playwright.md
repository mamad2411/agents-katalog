---
description: 
globs: 
alwaysApply: false
---
## Context

- Playwright is the tools to create e2e tests
- You can create test in the e2e folder

## Auto-correction

- You must create the test and then use `pnpm test:e2e:ci -g "name-of-the-test"` to auto-correct the code

## Database access

- Always use [prisma.ts](mdc:src/lib/prisma.ts) for databasae access.

## Utils file

- [auth-test.ts](mdc:e2e/utils/auth-test.ts)

## Rules

- Always remove your console.log after the tests passed