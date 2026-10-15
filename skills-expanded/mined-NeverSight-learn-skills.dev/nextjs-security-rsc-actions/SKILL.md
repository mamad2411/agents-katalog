---
name: nextjs-security-rsc-actions
description: Implement and audit security controls for Next.js App Router projects that use Server Components and Server Actions, with emphasis on preventing accidental data exposure. Use when designing a data access model, reviewing `use client` or `use server` code, validating action inputs and authorization, auditing route handlers or middleware, or preparing a Next.js security checklist.
---

# Next.js Security (RSC + Actions)

Apply the security model from Next.js guidance on Server Components and Server Actions as concrete engineering steps, audits, and code changes.

Prefer the Data Access Layer model for new projects. Treat all client-provided inputs as hostile. Validate and re-authorize at read and write boundaries.

## Quick Start

1. Run triage:
```bash
bash scripts/nextjs_security_audit.sh /path/to/nextjs-repo
```
2. Review [article-security-checklist.md](references/article-security-checklist.md).
3. Apply patterns in [secure-code-patterns.md](references/secure-code-patterns.md).
4. Re-run triage and report remaining risks.

## Workflow

## 1) Select One Data Handling Model

- Use one model and avoid mixing patterns excessively:
  - HTTP API model for large existing organizations.
  - Data Access Layer (DAL) model for new projects.
  - Component-level direct data access only for prototypes.
- Flag mixed patterns as audit hotspots.

## 2) Implement Data Access Layer Boundaries

- Keep database and sensitive env access inside DAL modules.
- Mark DAL modules with `import 'server-only'`.
- Return minimized DTOs, not raw database rows.
- Avoid passing large privileged objects through component trees.
- Re-read auth context (`cookies()`, session, membership checks) inside DAL functions.

## 3) Harden Server/Client Component Boundaries

- Audit every `'use client'` module:
  - Require minimal prop types.
  - Reject broad entities (`User`, `Account`, full DB records) as props.
  - Scrutinize sensitive fields (`token`, `secret`, `phone`, payment fields).
- Keep server-only logic in server modules and never rely on SSR execution context as privileged.
- Use taint APIs only as defense-in-depth, not as a primary control.

## 4) Secure Read Paths

- Treat URL params, `searchParams`, and headers as untrusted input.
- Validate and authorize on each read.
- Never perform writes/mutations during rendering.
- Avoid side effects on GET-driven rendering paths.

## 5) Secure Write Paths (Server Actions)

- Treat each exported `"use server"` action as a public endpoint.
- Validate argument shape and type at runtime (for example, with `zod`).
- Re-authorize actor permissions inside the action before mutation.
- Assume action arguments are attacker-controlled.
- For closure actions, understand encryption key behavior and deployment skew; set `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` when operationally required.
- When `.bind(...)` is used, treat bound values as plaintext inputs and re-validate server-side.

## 6) Audit Escape Hatches

- Audit `route.ts` and `middleware.ts` with traditional API security controls.
- For custom handlers, explicitly review CSRF posture, especially custom GET behavior.
- Prefer allow-list middleware logic over deny-list logic.
- Verify POST access to pages with actions matches authorization intent.

## 7) Produce Findings

- Report findings by severity:
  - High: missing authz in actions, raw sensitive DTO exposure to client.
  - Medium: broad client props, unvalidated params, route handler CSRF gaps.
  - Low: pattern drift, inconsistent model usage, missing defense-in-depth checks.
- Include exact files and lines for each finding.
- Include a short “known safe” section for audited areas with no findings.

## Resources

- Use [article-security-checklist.md](references/article-security-checklist.md) for the article-derived checklist and audit prompts.
- Use [secure-code-patterns.md](references/secure-code-patterns.md) for implementation templates and anti-pattern replacements.
- Use `scripts/nextjs_security_audit.sh` for fast triage before deep review.

## Source Note

Base this skill on the Next.js security article published on October 23, 2023.
When policies conflict with newer framework behavior, prefer the latest official Next.js documentation and release notes.
