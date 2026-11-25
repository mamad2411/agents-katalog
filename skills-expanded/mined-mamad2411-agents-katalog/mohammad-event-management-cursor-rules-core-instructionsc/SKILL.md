---
description: Read this before writing any code or proposing architectural changes.
globs: *
---
# Mohammad Event Management

**CRITICAL INSTRUCTION FOR CURSOR:**

Before you write any code, scaffold any modules, or suggest architectural changes, you MUST read the documentation located in the `.agent/` directory.

The following files dictate the strict laws of this repository:
- `.agent/rules.md` (Core guidelines and tech stack)
- `.agent/workflow.md` (Strict script instructions for creating modules)
- `.agent/coding-rules.md` (TypeScript and Prisma rules)
- `.agent/database.md` (Database operations and schema instructions)
- `.agent/api-guidelines.md` (API Response mapping and Zod validation)

**Absolute Rule**: Do not manually `mkdir` or `touch` files to create API modules. You must execute `docker compose exec server npm run create:module <module_name>`. Failure to do so breaks the repository's structural standard.
