# Project Rules

> **⚠️ This file has been migrated to `.cursor/rules/` directory**
> 
> Rules are now organized into separate `.mdc` files in `.cursor/rules/` for better maintainability and context-aware application. This file is kept for reference but is no longer actively used by Cursor.
> 
> See `.cursor/rules/README.md` for details on the new structure.

## Migration Status

All rules have been migrated to the following files:
- `.cursor/rules/stack.mdc` - Technology stack
- `.cursor/rules/coding-rules.mdc` - Coding conventions
- `.cursor/rules/pre-commit-workflow.mdc` - Pre-commit checklist
- `.cursor/rules/security.mdc` - Security guidelines
- `.cursor/rules/zod-usage.mdc` - Zod best practices

## Legacy Content (for reference)

<details>
<summary>Click to view legacy rules content</summary>

## Stack
- Next.js 16 (Stable) (App Router)
- Supabase
- Inngest

## Rules
- Use Server Actions for mutations
- Use 'json_object' mode for all LLM outputs
- Strict TypeScript interfaces in `types`
- Strictly await `params` and `searchParams` in server components
- Turbopack is enabled by default

## Behavior
- Cycle: Plan -> Code -> Validate -> Document -> Commit

## Pre-Commit Workflow

Mandatory checklist to be performed before every commit:

1. **Validation**: 
   - Run `npx tsc --noEmit` (Type Check) to ensure no TypeScript errors
   - Run `npm run lint` to ensure no linting errors

2. **Database**: 
   - Run `npm run db:validate` to ensure connectivity.

3. **Ingestion**: 
   - Run `npm run ingest:validate` to validate Reddit ingestion service functionality.

4. **Audit**: 
   - Update `.cursor/PROMPTS.md` with the key prompt used to generate the feature

5. **History**: 
   - Export the chat history to `.cursor/history/` and link it in the `PROMPTS.md` entry

## Security

- **SECURITY**: Never print, log, or ask for real API keys or secrets.
- **SECURITY**: Do not attempt to read `.env.local` or `.env.production`.
- **SECURITY**: Use `process.env.VARIABLE_NAME` or the `@/lib/env` validator only.

## Zod Usage

- **Zod Error Handling**: When using `safeParse()`, access errors via `result.error.issues` (not `result.error.errors`).
- **Zod Validation**: Use `safeParse()` for non-throwing validation, `parse()` for throwing validation.
- **Zod Error Structure**: Each issue in `result.error.issues` has:
  - `path`: Array of strings representing the field path
  - `message`: Human-readable error message
  - `code`: Zod error code (e.g., 'invalid_type', 'too_small')
- **Zod Best Practices**:
  - Always validate environment variables on import using `safeParse()`
  - Provide custom error messages for better developer experience
  - Use `.transform()` for type coercion (e.g., string to boolean)
  - Use `.default()` for optional values with fallbacks

</details>

