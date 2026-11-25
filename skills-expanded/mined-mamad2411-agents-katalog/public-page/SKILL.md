---
name: public-page
description: "Generate public-facing pages (marketing, legal, error, changelog). Use when building landing pages, feature pages, pricing pages, terms of service, 404/500 pages, or changelogs. Triggers on: create landing page, build pricing page, new feature page, create 404 page, terms of service, changelog page."
---

# Public Page Skill

> ⛔ **CRITICAL: Check `git.autoCommit` before committing page changes**
>
> **Trigger:** Before running `git commit` in Step 7.
>
> **Check:** Read `project.json` → `git.autoCommit`
> - If `true` (default): Proceed with commit normally
> - If `false`: **NEVER run `git commit`** — failure to comply violates project constraint
>
> **When autoCommit is disabled:**
> 1. Stage files: `git add .`
> 2. Report staged files and suggested commit message
> 3. Say: "Auto-commit is disabled. Run `git commit -m \"feat: add [page type] page\"` when ready."

Generate and implement public-facing pages for the web application.

---

## The Job

1. **Read project context** from `docs/project.json` (if exists)
2. Understand the page request
3. Gather context from reference documents
4. Implement the page using @public-page-dev
5. Capture screenshots using @screenshot-maintainer
6. Review with critics (@public-page-critic, @seo-critic, @copy-critic)
7. Fix any critical issues
8. Commit the changes

---

## Step 0: Read Project Context

**Before generating any page, read the project manifest to understand the stack:**

```bash
cat docs/project.json 2>/dev/null || echo "NO_PROJECT_JSON"
```

If `docs/project.json` exists, extract key information:

| Field | Use For |
|-------|---------|
| `stack.framework` | Determine file structure and routing conventions |
| `stack.languages` | File extensions (.tsx, .jsx, .vue, .svelte, etc.) |
| `apps` | Where to place page files |
| `styling` | CSS approach (Tailwind, CSS modules, etc.) |
| `styling.darkMode.enabled` | Add dark mode verification |
| `context.designSystem` | Reference design system document |
| `context.brandVoice` | Reference brand voice document |

**Store this context for use when generating pages.**

If no `project.json` exists, ask the user:
```
⚠️ No docs/project.json found. What framework are you using?
   A. Next.js (App Router)
   B. Next.js (Pages Router)
   C. Remix
   D. Plain React (Vite/CRA)
   E. Vue/Nuxt
   F. Other: [please specify]
```

---

## Step 1: Clarify the Request

Determine the page type and requirements:

| Page Type | Key Questions |
|-----------|---------------|
| **Landing** | What's the primary value proposition? What CTA? |
| **Feature** | Which feature? What are the key benefits? |
| **Use Case** | Which persona? What pain points to address? |
| **Pricing** | What tiers? What prices? What differentiates them? |
| **Legal** | Which document (terms, privacy, acceptable use)? |
| **Error** | 404 or 500? Any custom messaging needed? |
| **Changelog** | What format? How far back? |

If the request is clear, proceed. If ambiguous, ask one clarifying question.

---

## Step 2: Gather Context

Read reference documents based on `project.json` or defaults:

**From `project.json` (if available):**
```
{context.designSystem}              # Visual guidelines (e.g., docs/design-system.md)
{context.brandVoice}                # Tone and messaging (e.g., docs/brand-voice.md)
```

**Standard locations (check if exist):**
```
docs/marketing/brand-voice.md        # Tone and messaging
docs/marketing/target-personas.md    # User profiles
docs/marketing/feature-matrix.md     # Feature descriptions
docs/marketing/screenshot-registry.json  # Available screenshots
docs/prd.md                          # Product details
```

If key documents are missing, note what would be helpful and proceed with best practices.

---

## Step 3: Implement the Page

Invoke the @public-page-dev agent with stack context:

```
@public-page-dev: Create a [page type] page.

Page type: [landing / feature / use-case / pricing / legal / error / changelog]
Target: [specific feature, persona, or document type]

Stack Context (from project.json):
- Framework: [stack.framework]
- Language: [stack.languages]
- Styling: [styling.framework]
- Dark mode: [styling.darkMode.enabled]
- File location: [apps.*.structure.pages or routing convention]

Context:
- Brand voice: [summary from brand-voice.md]
- Target audience: [summary from personas]
- Key benefits: [from PRD or feature-matrix]
- Available screenshots: [from registry]

Requirements:
- [any specific requirements from the user]
```

---

## Step 4: Capture Screenshots

If the page needs product screenshots that don't exist:

```
@screenshot-maintainer: Capture new screenshot.
- ID: [descriptive-id]
- URL: [product URL to capture]
- Actions: [any interactions needed]
- Viewport: [dimensions]
- Will be used in: [page path]
```

---

## Step 5: Run Critics

After implementation, run all three critics:

### 5a: Public Page Critic

```
@public-page-critic: Review the new page at [path].
Focus on: conversion, mobile UX, accessibility, brand consistency.
```

### 5b: SEO Critic

```
@seo-critic: Review the new page at [path].
Focus on: meta tags, headings, structured data, technical SEO.
```

### 5c: Copy Critic

```
@copy-critic: Review the copy on [path].
Focus on: clarity, target market fit, accuracy, brand voice.
```

---

## Step 6: Address Feedback

1. Read each review file:
   - `docs/public-page-review.md`
   - `docs/seo-review.md`
   - `docs/copy-review.md`

2. For **Critical Issues**: Fix immediately before proceeding.

3. For **Warnings**: Fix if straightforward, otherwise note for follow-up.

4. For **Suggestions**: Note for future optimization.

5. Delete review files after addressing.

---

## Step 7: Commit

Commit all changes with an appropriate message:

```bash
git add .
git commit -m "feat: add [page type] page at /[path]"
```

---

## Page Type Reference

### Marketing Pages

| Page | Route | Purpose |
|------|-------|---------|
| Landing | `/` | Primary conversion page |
| Pricing | `/pricing` | Tier comparison, pricing details |
| Features Overview | `/features` | All features summary |
| Feature Detail | `/features/[slug]` | Single feature deep-dive |
| Use Case | `/solutions/[persona]` | Persona-specific value prop |
| Changelog | `/changelog` | Product updates |

### Legal Pages

| Page | Route | Purpose |
|------|-------|---------|
| Terms of Service | `/terms` | Usage agreement |
| Privacy Policy | `/privacy` | Data handling |
| Acceptable Use | `/acceptable-use` | Usage rules |

### Error Pages

| Page | Purpose |
|------|---------|
| 404 | Page not found |
| 500 | Server error |

---

## File Structure by Framework

**Determine file structure from `project.json` `stack.framework`:**

### Next.js (App Router)

```
app/
├── (marketing)/              # Marketing route group
│   ├── layout.tsx            # Marketing header/footer
│   ├── page.tsx              # Landing page
│   ├── pricing/page.tsx
│   ├── features/
│   │   ├── page.tsx          # Features overview
│   │   └── [slug]/page.tsx   # Feature detail
│   ├── solutions/
│   │   └── [persona]/page.tsx
│   └── changelog/page.tsx
├── (legal)/                  # Legal route group
│   ├── layout.tsx
│   ├── terms/page.tsx
│   ├── privacy/page.tsx
│   └── acceptable-use/page.tsx
├── not-found.tsx             # 404
└── error.tsx                 # 500

components/marketing/         # Reusable marketing components
```

### Next.js (Pages Router)

```
pages/
├── index.tsx                 # Landing page
├── pricing.tsx
├── features/
│   ├── index.tsx
│   └── [slug].tsx
├── solutions/
│   └── [persona].tsx
├── changelog.tsx
├── terms.tsx
├── privacy.tsx
├── acceptable-use.tsx
├── 404.tsx
└── 500.tsx

components/marketing/         # Reusable marketing components
```

### Remix

```
app/
├── routes/
│   ├── _index.tsx            # Landing page
│   ├── pricing.tsx
│   ├── features._index.tsx
│   ├── features.$slug.tsx
│   ├── solutions.$persona.tsx
│   ├── changelog.tsx
│   ├── terms.tsx
│   ├── privacy.tsx
│   └── acceptable-use.tsx
├── root.tsx                  # Error boundaries here
└── components/marketing/
```

### Plain React (Vite/CRA with React Router)

```
src/
├── pages/
│   ├── Landing.tsx
│   ├── Pricing.tsx
│   ├── Features.tsx
│   ├── FeatureDetail.tsx
│   ├── Solutions.tsx
│   ├── Changelog.tsx
│   ├── Terms.tsx
│   ├── Privacy.tsx
│   ├── AcceptableUse.tsx
│   ├── NotFound.tsx
│   └── ServerError.tsx
├── components/marketing/
└── router.tsx                # Route definitions
```

### Vue/Nuxt

```
pages/
├── index.vue                 # Landing page
├── pricing.vue
├── features/
│   ├── index.vue
│   └── [slug].vue
├── solutions/
│   └── [persona].vue
├── changelog.vue
├── terms.vue
├── privacy.vue
└── acceptable-use.vue

components/marketing/         # Reusable marketing components
```

### SvelteKit

```
src/routes/
├── +page.svelte              # Landing page
├── pricing/+page.svelte
├── features/
│   ├── +page.svelte
│   └── [slug]/+page.svelte
├── solutions/
│   └── [persona]/+page.svelte
├── changelog/+page.svelte
├── terms/+page.svelte
├── privacy/+page.svelte
├── acceptable-use/+page.svelte
└── +error.svelte             # Error page

lib/components/marketing/     # Reusable components
```

### Static Site Generators (Astro, Hugo, Jekyll)

Reference the project's existing structure in `project.json` `apps.*.structure.pages`.

---

## Output

After completing the page:

1. **Files created/modified** — List all files
2. **Screenshots captured** — Any new screenshots
3. **Review summary** — Key issues addressed
4. **Visual verification** — Confirm page looks correct
5. **Next steps** — Any follow-up needed

---

## Examples

### Example 1: Landing Page (Next.js App Router project)

```
User: Create a landing page for Example Scheduler

→ Read docs/project.json (Next.js, TypeScript, Tailwind, dark mode)
→ Read brand-voice.md, personas, PRD
→ @public-page-dev creates app/(marketing)/page.tsx with:
   - Hero: "Schedule Your Install Crews in Half the Time"
   - Features section highlighting calendar, resources, events
   - Pricing preview ($129/mo)
   - FAQ section
   - CTAs: "Start Free Trial"
→ @screenshot-maintainer captures calendar screenshots
→ Critics review (including dark mode verification)
→ Fix critical issues
→ Commit
```

### Example 2: Feature Page (Remix project)

```
User: Create a feature page for team management

→ Read docs/project.json (Remix, TypeScript)
→ Read feature-matrix.md for team management details
→ @public-page-dev creates app/routes/features.team-management.tsx
→ @screenshot-maintainer captures resource panel, team settings
→ Critics review
→ Commit
```

### Example 3: 404 Page (Plain React + Vite project)

```
User: Create a custom 404 page

→ Read docs/project.json (React, Vite, react-router)
→ @public-page-dev creates src/pages/NotFound.tsx with:
   - Friendly message
   - Search box
   - Links to home, support
   - Consistent branding
→ Update router.tsx to use NotFound component
→ @public-page-critic reviews
→ Commit
```

### Example 4: Pricing Page (Vue/Nuxt project)

```
User: Create a pricing page with three tiers

→ Read docs/project.json (Nuxt, Vue 3, TypeScript)
→ @public-page-dev creates pages/pricing.vue with:
   - Three tier cards
   - Feature comparison table
   - FAQ section
   - CTA buttons
→ Critics review
→ Commit
```

---

## Checklist

Before creating the page:

- [ ] Read `docs/project.json` for stack context
- [ ] Identified correct file location based on framework
- [ ] Using correct file extension (.tsx, .jsx, .vue, .svelte, etc.)
- [ ] Referenced design system (if `context.designSystem` set)
- [ ] Referenced brand voice (if `context.brandVoice` set)
- [ ] Dark mode verification included (if `styling.darkMode.enabled`)
- [ ] Used framework-appropriate routing conventions
- [ ] Reused existing marketing components where available

After creating the page:

- [ ] Page renders correctly
- [ ] @public-page-critic review passed
- [ ] @seo-critic review passed  
- [ ] @copy-critic review passed
- [ ] Works in both light and dark mode (if applicable)
- [ ] Mobile responsive
- [ ] Screenshots captured for support/marketing use
