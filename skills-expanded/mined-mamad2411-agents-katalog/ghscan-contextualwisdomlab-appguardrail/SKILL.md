# VibeSec Security Skill for Claude Code

Add this file as `CLAUDE.md` in your project root to give Claude Code persistent security awareness.

---

## Security Guardrails

You are working on a production web application. Apply the following security rules consistently throughout all code you generate or modify.

### Authentication

- Every server-side API handler must check that the user is authenticated before accessing any data or performing any action.
- Use the project's established session/auth library (e.g., `getServerSession`, `auth()`, Supabase `getUser()`). Do not invent custom session logic.
- Unauthenticated requests must return `401 Unauthorized`.

### Authorization (Ownership)

- For every user-owned resource (projects, files, messages, orders, etc.), verify that the authenticated user's ID matches the resource's owner field before returning or mutating data.
- Never skip ownership checks because "the ID came from the URL" or "the frontend already filters it."
- Return `403 Forbidden` for ownership violations — not `404`, not `200`, not an empty response.
- When adding any new endpoint that touches user data, include the ownership check in the first version of the code.

### Secrets

- Never place secrets, API keys, service role keys, or JWT signing secrets in code.
- Never use `NEXT_PUBLIC_` prefix for server-only secrets.
- `SUPABASE_SERVICE_ROLE_KEY` must only appear in server-side files (API routes, server actions, edge functions). It must never be imported in components, hooks, or any file that runs in the browser.

### Input Validation

- Validate and sanitize all inputs received from the client (route params, query strings, request bodies, headers).
- Use a schema validation library (Zod, Yup, Joi) for request bodies.
- Never pass raw user input directly into database queries.

### Stripe Webhooks

- Always call `stripe.webhooks.constructEvent(body, signature, secret)` at the top of every Stripe webhook handler. Reject the request immediately if verification fails.
- Never trust `event.data.object.amount` or price data from the client; always retrieve prices from Stripe server-side.

### Supabase

- Row Level Security (RLS) must be enabled on all tables that store user data.
- Write explicit RLS policies; never rely on "no policy" being restrictive.
- Use `createClient` with the `anon` key for client-side operations; use `service_role` only in server-side admin utilities.

### File Uploads

- Validate `Content-Type`, file extension, and file size server-side.
- Generate server-side filenames; never use `req.file.originalname` directly as the stored filename.

### Temporary / Placeholder Code

- Never leave `// TODO: add auth`, `// skip for now`, or mock authentication in code that will run in production.
- If a feature is incomplete, add a clear runtime error or a disabled state rather than a security bypass.

---

## Checklist Before Suggesting Any New Endpoint

- [ ] Is the user authenticated?
- [ ] Is resource ownership verified server-side?
- [ ] Are inputs validated with a schema?
- [ ] Are secrets server-side only?
- [ ] Are there tests for unauthorized and cross-user access?
