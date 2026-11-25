---
name: docs
description: Documentation workflow — edit markdown docs, technical writing, blog content, release notes without touching source code. Applies Content Writer role. Includes SEO review branch for public-facing content.
argument-hint: [documentation target or section]
---

# Documentation

Safe documentation-only workflow. Edit markdown files without touching application source code, configs, or infrastructure. Applies `content-writer` role for all writing tasks.

**⚠️ CONSTRAINT: This workflow NEVER modifies source code (*.java, *.ts, *.tsx, *.py, *.go), configs (*.yaml, *.yml, *.json), infrastructure (*.tf, Dockerfile, Helm), or dependency files (pom.xml, package.json, requirements.txt).**

## 1. Define Scope

Ask the user (or extract from parent workflow):

- **What documentation?** (technical docs, API reference, README, PRD, design doc, ADR, blog post, release notes, UI copy)
- **Content type**:
  - **Internal** (technical docs, design docs, ADRs) → `content-writer` role only
  - **Public-facing** (blog, landing page, marketing) → `content-writer` role + `seo-engineer` role
- **Action**: Create new / update existing / restructure
- **Target files**: Which `.md` files will be affected

## 2. Apply Roles

| Content Type | Primary Role | Additional Role |
|---|---|---|
| Technical documentation | `content-writer` role | — |
| API reference | `content-writer` role | Stack-specific role for accuracy |
| Blog / landing page content | `content-writer` role | `seo-engineer` role |
| PRD / acceptance criteria | `product-manager` role | — |
| Architecture / ADR | `solution-architect` role | — |
| Release notes | `content-writer` role | — |
| UI microcopy | `content-writer` role | `frontend-engineer` role for context |
| Page content (landing, product) | `content-designer` role | `seo-engineer` role, `ui-ux-designer` role |

## 3. Gather Context

Before writing:

1. **Read project's `AGENTS.md`** — terminology, conventions, tech stack
2. **Read existing docs** — understand structure, tone, terminology already in use
3. **Identify Diátaxis mode** — Tutorial, How-to, Reference, or Explanation
4. **Check related code** (read-only) — verify technical accuracy of claims

## 4. Write Content

Follow `content-writer` role standards:

- **Diátaxis framework** for documentation structure
- **English only** unless explicitly requested otherwise
- **Progressive disclosure** — overview first, details on demand
- **Tested examples** — all code snippets must be accurate
- **Consistent terminology** — match existing project conventions

### For Blog / Public Content

Apply `geo-writer` skill first — macro/meso/micro structure, answer-first sections, entity clarity, schema requirements. Then apply `humanizer` skill — scan for and remove AI writing patterns. Then follow `seo-engineer` role standards:

- **Title tag**: Descriptive, matches search intent
- **Meta description**: Compelling summary
- **Heading hierarchy**: One H1, logical H2→H3 flow
- **Internal links**: Descriptive anchor text to related content
- **Images**: Descriptive alt text
- **Structured data**: Article/BlogPosting schema (JSON-LD) where applicable
- **No keyword stuffing** — write for users, not crawlers

## 5. Verify

- [ ] All internal links are valid (no broken references)
- [ ] Code examples are accurate and match current implementation
- [ ] Terminology is consistent with project conventions
- [ ] Formatting follows existing documentation patterns
- [ ] No secrets, PII, or internal-only information in public content
- [ ] No source code, config, or infrastructure files were modified

### For Public Content — Humanization Checklist

- [ ] Text passed through `geo-writer` skill — structure, answer-first sentences, entity clarity
- [ ] Schema requirements identified and JSON-LD prepared (`Article`, `Person`, `Organization`, `FAQPage`, `HowTo`)
- [ ] `geo-content` rule satisfied
- [ ] Text scanned for AI writing patterns (`humanizer` skill)
- [ ] Anti-AI audit performed for text longer than 2 paragraphs
- [ ] Text sounds natural when read aloud

### For Public Content — SEO Checklist

- [ ] Title and meta description present and unique
- [ ] Heading hierarchy is logical (H1→H2→H3)
- [ ] Internal links with descriptive anchors added
- [ ] Images have alt text
- [ ] Page is indexable (no accidental noindex)
- [ ] Canonical URL is correct
- [ ] Structured data validates (Rich Results Test)

## 6. Summary

```
## Documentation Summary
- **Type**: [technical docs / blog / API reference / release notes / etc.]
- **Content mode**: [Tutorial / How-to / Reference / Explanation]
- **Files changed**:
  - [file1.md]: [created/updated — what changed]
  - [file2.md]: [created/updated — what changed]
- **Role(s) applied**: [`content-writer` role, `seo-engineer` role if public]
- **SEO review**: [pass / N/A for internal docs]
- **Verification**: [links valid, formatting correct, no code files modified]
- **Next steps**: [if any]
```

## Integration

- **Roles**: `content-writer` role (primary), `seo-engineer` role (public-facing content), `product-manager` role (PRDs)
- **Skills**: `geo-writer` skill (GEO/AEO structure pass for public-facing content), `humanizer` skill (AI writing pattern removal for public-facing content)
- **Rules**: `geo-content` (auto-enforces GEO structure and schema on public-facing text), `humanize-content` (auto-enforces humanizer pass)
- **Follow-up**: `seo-review` skill (for public content), `pre-commit` skill, `create-pr` skill
- **Related**: `feature-dev` skill (inline docs during development), `release` skill (release notes)
