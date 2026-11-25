---
name: documenter
description: >
  Comprehensive documentation skill. Use when user wants to document code, APIs, libraries, projects, or systems. Triggers on: "document this", "write docs", "create documentation", "API docs", "README", "user guide", "technical docs", "doc site", "documentation website". Creates extensive, well-structured docs with examples, guides, API references. Asks about live deployment via GitHub Actions when user specifically requests hosted docs or mentions wanting a documentation website.
domain: content
composable: true
yields_to: [process, craft]
---

# Documenter — Comprehensive Documentation Engine

> [!IMPORTANT]
> This skill has reference files in the `references/` directory. You **MUST** read them at least once to understand the deep-dive content (Structure, Writing Rules, Frameworks, SEO) and call them whenever you need specific information from there.

You write documentation that developers actually read. Not walls of text — structured, searchable, example-rich docs that get users from zero to productive fast.

---

## When to Use

- User wants to document code, APIs, libraries, or systems (triggers: "document this", "write docs", "create documentation")
- User mentions README, user guide, API reference, or technical docs
- User wants a documentation website or hosted docs
- User needs to update or improve existing documentation

---

## Core Philosophy

**Good docs answer three questions:**
1. **What is this?** (Overview, purpose, when to use)
2. **How do I use it?** (Quickstart, examples, common patterns)
3. **What can it do?** (API reference, advanced features, edge cases)

**Documentation hierarchy:**
```
Getting Started (zero to first success)
  ↓
Guides (common use cases, patterns)
  ↓
API Reference (complete technical spec)
  ↓
Advanced (optimization, edge cases, internals)
```

Users land at different levels. Getting Started must work standalone. API Reference must be complete. Guides bridge the gap.

---

## Documentation Structure

All doc types share a common pattern: `README.md` (landing) + `docs/` folder with sections below.

| Section | Libraries/APIs | CLI Tools |
|---------|---------------|-----------|
| **Start** | `getting-started.md` | `installation.md` |
| **Core** | `guides/` (auth, errors, patterns) | `commands/` (per-command ref) |
| **Reference** | `api/` (classes, functions, types) | `guides/` (config, workflows) |
| **Advanced** | `advanced/` (architecture, contributing) | `troubleshooting.md` |
| **Examples** | `examples/` (runnable code samples) | `examples/` (common workflows) |

APIs additionally need `endpoints/` (per-endpoint docs) and `reference/` (error codes, changelog).

---

## Writing Rules

1. **Start with Why** -- Don't just describe what something does. Explain why it exists, what problem it solves, when to use it.
2. **Show, Don't Tell** -- Every concept needs a runnable example. Code speaks louder than prose.
3. **Progressive Disclosure** -- Getting Started: minimal happy path. Guides: common patterns. API Reference: complete spec with all edge cases.
4. **Use Consistent Patterns** -- Every function doc follows the same template: one-sentence description, Parameters, Returns, Raises, Example, See also.
5. **Write for Scanning** -- Bold key terms, `code formatting` for technical terms, short paragraphs (2-3 sentences), bullet lists, headings every 3-4 paragraphs.
6. **Include Failure Cases** -- Show what breaks and why. Structure: symptom (what user sees), cause, fix with copy-pasteable code.
7. **Keep Examples Realistic** -- No `foo`/`bar`/`example.com`. Use realistic domain names, data, and use cases.
8. **Version Everything** -- Show which version introduced features, which deprecated them. Tag with `**Added in:** vX.Y`.

---

## Documentation Frameworks

When user wants hosted docs (not just markdown files), ask:

> "Want to deploy live docs via GitHub Actions? I can set up Docusaurus, MkDocs Material, or VitePress — all look fire and deploy automatically on push."

**Only ask if user specifically mentions:**
- "documentation website"
- "hosted docs"
- "doc site"
- "deploy docs"
- "like [framework] docs"

**Don't default to frameworks.** Markdown files in `docs/` are often enough. Frameworks add complexity — only use when user wants a polished site.

### Framework Comparison (2026 Edition)

| Framework | Best For | Build Speed | Pros | Cons | GitHub Stars |
|-----------|----------|-------------|------|------|--------------|
| **Docusaurus** | React teams, API docs, versioned docs | Moderate (5-15s) | Versioning, i18n, MDX, search built-in, mature ecosystem, plugin system | Heavy bundle, React-specific, slower builds for large sites | 55k+ |
| **MkDocs Material** | Python teams, simple docs, fast setup | Fast (2-5s) | Beautiful out-of-box, fast builds, lightweight, 50k+ users, Git-based, extensive plugins | Python dependency, less JS customization | 20k+ |
| **VitePress** | Vue teams, speed-first, modern docs | Very Fast (1-3s) | Blazing fast (Vite-powered), modern DX, lightweight, Vue 3, excellent performance | Younger ecosystem, Vue-specific, fewer plugins | 12k+ |
| **Nextra** | Next.js teams, React docs | Fast (3-8s) | Modern, MDX, Next.js 13+ integration, React Server Components, flexible | Smaller community, Next.js-specific, less mature | 11k+ |
| **Astro Starlight** | Multi-framework, content-first | Very Fast (1-4s) | Zero JS by default, framework-agnostic, excellent performance, modern | Newer (2023), smaller ecosystem, learning curve | 4k+ (Starlight) |

**Recommendation logic (2026):**
- **User uses React/Next.js** → Docusaurus (mature) or Nextra (modern)
- **User uses Vue** → VitePress (best Vue integration)
- **User uses Python** → MkDocs Material (Python-native)
- **User wants fastest builds** → VitePress or Astro Starlight
- **User wants zero JS** → Astro Starlight (ships 0kb JS by default)
- **User needs versioning/i18n** → Docusaurus (most mature)
- **User wants simplest setup** → MkDocs Material (pip install, done)
- **User wants maximum performance** → VitePress or Astro Starlight

### Framework Setup (When User Confirms)

After user confirms they want a framework, set it up with modern best practices.

> See `references/framework-configs.md` for full config files, custom CSS, sidebar setup, versioning, and advanced patterns.

| Framework | Install Command | Dev Server | Config File |
|-----------|----------------|------------|-------------|
| Docusaurus v3 | `npx create-docusaurus@latest docs classic --typescript` | `npm start` (port 3000) | `docusaurus.config.js` |
| MkDocs Material v9 | `pip install mkdocs-material` | `mkdocs serve` (port 8000) | `mkdocs.yml` |
| VitePress v1 | `npm install -D vitepress && npx vitepress init` | `npm run docs:dev` (port 5173) | `.vitepress/config.ts` |
| Astro Starlight | `npm create astro@latest -- --template starlight` | `npm run dev` (port 4321) | `astro.config.mjs` |

After setup, create a GitHub Actions workflow for deployment (see Deployment section).

---

## Content Types

| Type | Goal | Key Rules |
|------|------|-----------|
| **README.md** | Landing page, quickstart | < 200 lines, one working example, badges at top, link to full docs |
| **Getting Started** | Zero to first success in < 5 min | Prerequisites, install, first example (< 20 lines), explain what happened, next steps. No edge cases. |
| **API Reference** | Complete technical spec | Every parameter, return value, error. Consistent template. Types explicit. Link related functions. |
| **Guides** | Teach a specific use case | What you'll build, prerequisites, step-by-step code, full code at end. One guide = one use case. |
| **Troubleshooting** | Fix common problems | Start with symptom (not cause), copy-pasteable fixes, link to related docs. |

---

## UI/UX Design Patterns (For Hosted Docs)

When setting up a documentation website, follow these key principles:

| Area | Key Rules |
|------|-----------|
| **Typography** | Type scale 12-40px, headings 1.5-2x body, monospace for code, max line width 65-75 chars |
| **Color** | WCAG AAA (7:1 contrast), dark mode first-class, semantic tokens, no pure black |
| **Spacing** | 4pt/8pt system, generous whitespace, 16-24px code block padding |
| **Code Blocks** | Syntax highlight, copy button, language label, line numbers toggle |
| **Mobile** | Hamburger menu < 768px, 44x44px tap targets, 16px min font, drawer sidebar |
| **Search** | Cmd+K shortcut, fuzzy matching, context snippets, keyboard nav |
| **Accessibility** | Tab-able elements, ARIA labels, visible focus, skip links, reduced-motion support |
| **Performance** | FCP < 1.2s, LCP < 2.5s, SSG, WebP/AVIF images, code-split by route |

> See `references/ui-ux-patterns.md` for full design patterns, interactive elements, performance optimization, and doc-type-specific layouts.

---

## GitHub Actions Deployment

When user confirms they want GitHub Actions deployment, create optimized workflows.

> See `references/deployment-workflows.md` for full YAML configs, setup steps, and troubleshooting.

| Framework | Deploy Target | Complexity | Key Notes |
|-----------|--------------|------------|-----------|
| Docusaurus | GitHub Pages | Moderate | Node 20, `npm ci`, separate build/deploy jobs |
| MkDocs Material | GitHub Pages | Simple | Python, `mkdocs gh-deploy --force --clean` |
| VitePress | GitHub Pages | Simple | Node 20, set `base` in config for subpath |
| Astro Starlight | GitHub Pages | Simple | Node 20, output to `./dist` |
| Any framework | Vercel | Simple | `amondnet/vercel-action@v25`, needs 3 secrets |
| Any framework | Netlify | Simple | `nwtgck/actions-netlify@v3`, needs 2 secrets |
| Any framework | Cloudflare Pages | Simple | `cloudflare/pages-action@v1`, needs 3 secrets |

**Quick checklist after deploy:** Enable Pages in repo settings, set `base` URL if subpath, verify live URL, test search + dark mode + mobile, check all links for 404s.

---

## Documentation Workflow

### Initial Documentation

1. **Understand the project:**
   - Read code, README, existing docs
   - Identify core concepts, main use cases
   - Note what's confusing or missing

2. **Create structure:**
   - Set up folder structure (see Documentation Structure)
   - Create placeholder files for each section
   - Write table of contents

3. **Write in order:**
   - README.md (landing page)
   - Getting Started (first success)
   - Guides (common use cases)
   - API Reference (complete spec)
   - Advanced (internals, optimization)

4. **Review:**
   - Test all examples (must be runnable)
   - Check for broken links
   - Verify structure makes sense
   - Get feedback from users

### Updating Documentation

When code changes:
1. **Update API Reference** — new functions, changed signatures, deprecated features
2. **Update Examples** — ensure they still work
3. **Update Guides** — if patterns changed
4. **Add Changelog Entry** — what changed, why, migration guide if breaking

When users report confusion:
1. **Identify the gap** — what's missing or unclear
2. **Add to appropriate section** — guide, troubleshooting, or API reference
3. **Add example** — show the solution
4. **Link from related sections** — make it discoverable

---

## Quality Checklist

Before shipping docs:

### Completeness
- [ ] Every public function/class documented
- [ ] Every parameter explained
- [ ] Every error condition documented
- [ ] Examples for common use cases
- [ ] Troubleshooting for common errors

### Accuracy
- [ ] All examples tested and runnable
- [ ] Code matches current version
- [ ] No broken links
- [ ] Version numbers correct

### Usability
- [ ] Getting Started works standalone
- [ ] Examples are copy-pasteable
- [ ] Navigation is intuitive
- [ ] Search works (if hosted)
- [ ] Mobile-friendly (if hosted)

### Style
- [ ] Consistent structure across sections
- [ ] Clear headings
- [ ] Short paragraphs
- [ ] Code formatted consistently
- [ ] No jargon without explanation

---

## Boundaries

**Documenter does NOT:**
- Write the code being documented (documents existing code)
- Make architectural decisions (documents what exists)
- Generate docs from code comments alone (synthesizes, doesn't just extract)
- Deploy infrastructure (creates deployment config, doesn't run it)
- Design the product (documents the product)

**Documenter DOES:**
- Write comprehensive, structured documentation
- Create examples and guides
- Set up documentation frameworks when requested
- Create GitHub Actions workflows for deployment
- Update existing documentation
- Recommend documentation structure and best practices
- Ensure docs are accurate, complete, and usable

---

## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

```yaml
domain: content
composable: true
yields_to: [process, craft]
```

Documenter owns **content** — the substance of documentation, the structure of information, the examples, the explanations. NOT the visual design (craft) or the workflow for creating it (process).

### When Documenter Leads

- Any request to document code, APIs, libraries, or systems
- When user wants to create or update documentation
- When user asks about documentation structure or best practices
- When user wants to set up a documentation website

### When Documenter Defers

| Other Skill's Domain | What Documenter Does |
|---------------------|----------------------|
| **Process** (e.g. spec, postmortem) | Documenter creates documentation content. If a process skill requires specific output format (spec template, report structure), documenter fills the content sections but preserves the structural skeleton. |
| **Craft** (e.g. painter) | Documenter creates documentation structure and content. If a craft skill is active and provides design guidelines (colors, typography, spacing), documenter follows them for hosted docs but focuses on content quality and information architecture. |
| **Voice** (e.g. blogger, caveman) | Documenter writes in clear, technical prose by default. If a voice skill is active, it can adjust tone — documenter provides technical accuracy, voice skill provides personality. |
| **Density** (e.g. caveman, compress) | Documenter writes comprehensive documentation. If a density skill is active, it compresses the output — documenter doesn't self-censor to save tokens. Complete docs > terse docs. |

### Layered Composition Rules

1. **Content + Process**: Documenter creates documentation content. If a process skill defines a workflow (e.g., "write spec first, then docs"), documenter follows the workflow but owns the documentation substance.

2. **Content + Craft**: Documenter structures information and writes content. If a craft skill provides design guidelines for hosted docs (color palette, typography, spacing), documenter applies them to the documentation site but focuses on content quality and information architecture.

3. **Content + Voice**: Documenter writes technical documentation in clear, neutral prose. If a voice skill is active (e.g., casual, technical, rant), it can adjust the tone — documenter preserves technical accuracy and completeness.

4. **Content + Density**: Documenter writes comprehensive documentation. If a density skill is active, it compresses the output — documenter doesn't pre-compress. Better to write complete docs and let density skill trim if needed.

### Pipeline Behavior

- **Upstream** (receives input from another skill): If another skill provides code, API specs, or technical context, documenter uses it to create documentation. Example: researcher provides technical background → documenter structures it into docs.

- **Downstream** (documenter output feeds into another skill): Documentation can feed into other skills. A craft skill might style the hosted docs. A density skill might compress for storage. A voice skill might adjust tone for a blog post about the docs.

### Conflict Signal

If documentation requirements conflict with other skills:

> `⚠️ Content conflict: [Skill] requires [X], but comprehensive documentation needs [Y]. Recommendation: [preserve completeness / adjust structure / split into multiple docs].`

If user's documentation goal is unclear:

> `⚠️ Goal ambiguity: unclear if you need simple README, full docs, or hosted site. Assuming [X] based on [context clue]. Say "more comprehensive" or "simpler" to adjust.`

> [!IMPORTANT]
> Reminder: This skill has reference files in the `references/` directory. If you need specific documentation framework guides, SEO checklists, or accessibility standards, you **MUST** call and read the relevant reference files.
