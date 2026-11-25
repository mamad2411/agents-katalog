---
alwaysApply: true
---


# Cursor Rules

**KEEP IT SIMPLE.** Prefer the smallest change that solves the problem.
**No code dumps.** Only write what the task explicitly asks—no extras.

## How to Use These Rules (very simple)

* Follow this file for all edits and generations.
* If unclear, ask 1 short clarifying question, then proceed.
* Make the **minimal diff**. Keep changes small and focused.
* Before marking “done”, run: `make cc` (lint + format + typecheck).

## Project Conventions

* Use the `pnpm` package manager.
* Next.js **App Router Convention**
* `*/layout.tsx` should ALWAYS BE SERVER COMPONENTS.
* `*/page.tsx` should ALWAYS BE SERVER COMPONENTS.
* **Fetch data in Server Components** (or **Server Actions** for FastAPI) and pass results to Client Components.
* **Components use shadcn/ui**. Prefer existing components. If missing: `npx shadcn@latest add <component>`.
* **Business logic** (no fetch) → **client hooks** in `src/hooks/`.
* `globals.css` stores **theme tokens** and global styles.
* **File names:** **kebab-case** (e.g., `user-card.tsx`, `fetch-user.server.ts`).
* Keep files short. If a file grows >200 lines, consider splitting into smaller files/components.
* Do not use relative imports. Use absolute imports. You have aliases:
    - "components": "@/components",
    - "lib": "@/lib",
    - "hooks": "@/hooks"
    - "types": "@/types"
  

## Types

* **Type everything.** No implicit `any`.
* Add explicit types for params, returns, and objects.
* Use **zod** schemas at boundaries (API inputs/outputs, forms, external data).
* Skip zod for internal types (component props, store state).

## Control Flow

* Prefer **`switch/case`** or small lookup maps over long `if/else` chains.

## FastAPI Calls

* Use **Server Actions / server functions** in `app/**` for all FastAPI fetches.
* **Never call FastAPI from Client Components.**
* Handle and surface errors (see Errors).

## shadcn/ui Usage

* Always import from `@/components/ui/*`.
* Use provided variants (`variant`, `size`) instead of custom CSS.
* Theming via CSS variables in `globals.css`.
* For new UI needs, **add** the component via CLI—don’t reinvent.

## Styling

* Tailwind + tokens from `:root` / `.dark`.
* Avoid custom CSS unless necessary; prefer utility classes.
* No inline styles except quick one-offs.

## Errors

### Exception Classes
* Create typed error classes in `src/lib/errors.ts`: `AppError` (base), `ValidationError`, `AuthError`, `NotFoundError`, `ExternalServiceError`.
* Include `statusCode`, `userMessage`, `technicalDetails`.

### Server Actions
* Return typed results: `{ success: true, data }` or `{ success: false, error }`.
* **Never throw** in Server Actions—return error states.

### UI Feedback
* Use **shadcn Sonner** toasts for user feedback:
  - **Error** (red): user-actionable failures
  - **Warning** (yellow): non-blocking issues
  - **Info** (blue): neutral updates
  - **Success** (green): confirmations
* Use `error.tsx` for catastrophic UI crashes.

### Logging
* Log all server errors with full context (userId, action, timestamp, stack).
* **Never** expose stack traces or secrets to users.
* User messages: generic and safe. Technical details: server logs only.


## Security

* **No secrets in client code.**
* Use environment variables on the server.
* Validate and sanitize all external inputs.

## Done Checklist

* Minimal diff.
* Types added/updated.
* Errors handled.
* `make cc` passes.
* UI uses shadcn/ui and follows tokens.