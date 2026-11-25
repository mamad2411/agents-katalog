---
name: develop-b2b-golf-feature
description: Develop features for the B2B Golf niche catalog — an Astro v5 golf apparel site on Cloudflare Pages. Use when adding pages, gallery content, MDX articles, or components for the golf apparel niche.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, astro_build, astro_check, astro_dev, run_tests]
---

# Develop B2B Golf Feature

Use this skill when building or modifying features in the B2B Golf catalog site.

**Prerequisites:** Read `overlays/astro-cloudflare/rules/astro-cloudflare-conventions.md` for generic Astro patterns.

## When to Use

- adding or restructuring pages under `src/pages/`
- adding images to a gallery or regenerating gallery data
- publishing MDX articles or catalog components
- debugging build failures specific to this site

## Core Rules

- Follow all rules from `overlays/astro-cloudflare/rules/astro-cloudflare-conventions.md`
- Follow all rules from `overlays/b2b-catalog-golf/rules/golf-project-rules.md`
- Gallery data auto-generated via `generate_galleries.mjs` — do not edit `generated_galleries.json` manually
- MDX articles use `@tailwindcss/typography` for body styling
- Brand tone: premium, sophisticated, golf/resort focused

## Suggested Process

### 1. Identify scope

Classify the change as page content, gallery update, MDX article, or component; it determines the directories touched and whether gallery regeneration is needed.

### 2. Read existing patterns

Inspect neighboring files in `src/pages/`, `src/components/`, and existing MDX articles; mirror their frontmatter, imports, and styling before writing new code.

### 3. Implement and regenerate galleries

Make the change following project conventions. For galleries: add images to `public/`, then run `node generate_galleries.mjs` and commit the regenerated data.

### 4. Validate

Run `npm run check` before commit; fix type, Astro, and lint errors until clean.

## Failure Modes

- **Gallery JSON hand-edited**: a gallery is updated by editing `generated_galleries.json` directly. **Mitigation:** the Core Rules forbid it; reject the change and require `node generate_galleries.mjs`.
- **MDX frontmatter drift**: a new article uses a different frontmatter shape than the existing articles. **Mitigation:** mirror the existing template (title, date, description, image, tags); reject non-conforming frontmatter.
- **SEO metadata missing on a new page**: a page ships without title and description. **Mitigation:** the Checklist enforces SEO metadata on every page; reject the change.
- **Off-brand voice in copy**: copy drifts from the premium, golf-resort tone. **Mitigation:** the Core Rules enforce brand tone; reject copy that drifts.
- **Build fails on `npm run check`**: a change is merged despite type, Astro, or lint errors. **Mitigation:** the Checklist enforces `npm run check` before commit; reject the change.

## Output Contracts

When this skill produces a structured handoff, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, and `validation_run` output proving `npm run check` passes.
- **`contracts/schemas/edge-deployment-spec.json`** when a new page or component is deployed to Cloudflare Pages.

Skip structured emission for trivial content edits that do not cross a role boundary.
## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: contact or lead-capture endpoints must enforce authn/authz per the active role's policy profile; reject anonymous access to non-public routes.
- **ASI04 Supply Chain**: every Astro, Cloudflare, and gallery-generator dependency must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: do not construct contact-form payloads or external API calls from external or user-supplied content without strict schema validation; reject string-concatenated form payloads.
- **ASI07 Inter-Agent Communication**: the implementation result is consumed by Cloudflare Engineer and DevOps Engineer roles; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a deploy as "safe" without the actual smoke test evidence; surface the residual risk honestly.
## Checklist

- [ ] correct location in `src/` structure
- [ ] gallery data generated via script, not manual JSON edits
- [ ] MDX frontmatter matches existing articles (title, date, description, image, tags)
- [ ] SEO metadata on every page
- [ ] brand tone matches golf/resort positioning
- [ ] `npm run check` passes

## Related Skills

- **review-code**: review against Astro and project conventions
- **navigate-service**: understand the codebase structure
- **commit-code**: commit with proper conventions
- **write-documentation**: update content or catalog documentation
- **troubleshoot-service**: debug build or deploy issues
