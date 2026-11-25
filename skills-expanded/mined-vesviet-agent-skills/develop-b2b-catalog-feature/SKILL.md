---
name: develop-b2b-catalog-feature
description: Develop features for the B2B factory direct catalog — an Astro v5 B2B manufacturing catalog on Cloudflare Pages. Use when adding pages, product data, components, contact forms, or R2 integrations in this project.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, astro_build, astro_check, astro_dev, run_tests]
---

# Develop B2B Catalog Feature

Use this skill when building or modifying features in the B2B factory direct corporate website.

**Prerequisites:** Read `overlays/astro-cloudflare/rules/astro-cloudflare-conventions.md` for generic Astro patterns.

## Core Rules

- Follow all rules from `overlays/astro-cloudflare/rules/astro-cloudflare-conventions.md`
- Follow all rules from `overlays/b2b-factory-catalog/rules/icm-project-rules.md`
- Product data lives in `src/data/products.ts` — typed TypeScript, never loose JSON
- Contact form backend at `src/pages/api/contact.ts` — Turnstile + Resend
- R2 assets accessed via `Astro.locals.runtime.env.catalog_documents`
- B2B professional tone in all copy and component text

## Suggested Process

### 1. Identify scope — new page, component, data update, or API endpoint
### 2. Read existing patterns in `src/pages/`, `src/components/`, `src/data/`
### 3. Implement matching established conventions
### 4. Run `npm run check` before commit

## Failure Modes

- **Product data stored as loose JSON**: a new product is added to a non-typed file instead of `src/data/products.ts`. **Mitigation:** the Core Rules require typed TypeScript; reject loose JSON.
- **Secrets in client code**: an API key or token is added to a client-side component. **Mitigation:** the Core Rules forbid it; verify with `npm run check` and the secrets scan.
- **R2 bindings accessed client-side**: a R2 binding is referenced in a client island. **Mitigation:** the Core Rules require server-side access; refactor to a server endpoint.
- **SEO metadata missing on a new page**: a page ships without title and description. **Mitigation:** the Checklist enforces SEO metadata on every page; reject the change.
- **Tailwind raw values used**: a component uses arbitrary values like `[#1B2A4A]` instead of design tokens. **Mitigation:** the Core Rules require design tokens; reject the change and use the token.

## Output Contracts

When this skill produces a structured handoff, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, and `validation_run` output proving `npm run check` passes.
- **`contracts/schemas/edge-deployment-spec.json`** when a new endpoint or binding is added to the Cloudflare Pages deploy.

Skip structured emission for trivial content edits that do not cross a role boundary.
## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: contact form and R2 endpoints must enforce authn/authz per the active role's policy profile; reject anonymous access to non-public routes.
- **ASI04 Supply Chain**: every Astro, Cloudflare, and Tailwind dependency must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: do not construct Resend or Turnstile payloads from external or user-supplied content without strict schema validation; reject string-concatenated form payloads.
- **ASI07 Inter-Agent Communication**: the implementation result is consumed by Cloudflare Engineer and DevOps Engineer roles; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a deploy as "safe" without the actual smoke test evidence; surface the residual risk honestly.
## Checklist

- [ ] correct location in `src/` structure
- [ ] product data typed in `src/data/products.ts`
- [ ] SEO metadata (title, description) on every page
- [ ] Tailwind utility classes, design tokens from `tailwind.config.js`
- [ ] R2 bindings accessed server-side only
- [ ] secrets in `.dev.vars`, never in client code
- [ ] `npm run check` passes (astro check + eslint + prettier)

## Related Skills

- **review-code**: review against Astro and project conventions
- **navigate-service**: understand the codebase structure
- **commit-code**: commit with proper conventions
- **troubleshoot-service**: debug build or deploy issues
- **write-documentation**: update product catalog docs
