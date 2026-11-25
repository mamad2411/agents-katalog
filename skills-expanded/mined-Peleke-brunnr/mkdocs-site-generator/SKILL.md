---
name: mkdocs-site-generator
description: Generate a complete MkDocs documentation site with GitHub Pages CI/CD for any TypeScript/Node.js codebase. Covers discovery, architecture, scaffold, content generation, CI/CD setup, and cross-reference verification. Use when setting up docs for a new or existing project.
license: Complete terms in LICENSE.txt
metadata:
  openclaw:
    emoji: "\U0001F4DA"
    requires:
      bins: ["python3", "pip", "gh"]
---

# MkDocs Site Generator

> Generates a complete MkDocs documentation site with GitHub Pages CI/CD for any TypeScript/Node.js codebase.

## TL;DR Execution Flow

```
Phase 0: Pre-flight checks (Python, conflicts, GH Pages status)
Phase 1: Deep codebase discovery (identity, API surface, feature mapping, test examples)
Phase 2: Documentation architecture (nav structure, content plan, diagram plan)
Phase 3: Configuration scaffold (mkdocs.yml, requirements.txt, directory tree, workflow)
  3.5:   Theme compatibility check (verify features work with chosen theme)
Phase 4: Content generation (home, getting-started, guides, reference, changelog)
Phase 5: GitHub Actions workflow (deploy-pages or mike, enable GH Pages)
Phase 6: Build, test, deploy (local build --strict, PR, merge, verify)
Phase 7: Quality checklist (content, technical, CI/CD, deployment)
```

**Critical path:** Phase 1.8 (feature area mapping) determines Phase 2 (nav structure) determines Phase 4 (what pages to write). Get 1.8 right and everything else follows.

## When to Use

- Setting up docs for a new or existing TypeScript library
- Adding GitHub Pages deployment to a project
- Migrating from another docs system to MkDocs

## Inputs

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `project_root` | path | cwd | Project root directory |
| `theme` | `"material"` \| `"readthedocs"` | `"readthedocs"` | MkDocs theme |
| `site_url` | string | inferred from repo | Published URL |
| `custom_domain` | string \| null | null | Custom domain (creates CNAME) |
| `versioning` | boolean | false | Enable mike for versioned docs |
| `api_docs` | `"typedoc"` \| `"manual"` \| `"none"` | `"manual"` | API docs strategy |
| `reference_projects` | path[] | [] | Projects to match patterns from |

---

## Phase 0: Pre-Flight Checks

Before starting, verify the environment and check for conflicts.

### 0.1 Environment

```bash
# Python available?
python3 --version  # Need 3.10+

# pip available?
pip --version

# gh CLI available and authenticated?
gh auth status

# Are we in a git repo?
git rev-parse --is-inside-work-tree
```

### 0.2 Conflict Detection

```
Check for existing docs infrastructure:
- docs/ directory         → Existing content to migrate or avoid overwriting
- mkdocs.yml              → Already configured — update don't overwrite
- .readthedocs.yml        → ReadTheDocs hosted — different setup
- requirements.txt        → Merge deps, don't overwrite
- .github/workflows/docs* → Existing workflow — update don't duplicate
- site/ in .gitignore     → Already excluded (good)
- gh-pages branch         → May indicate previous docs deployment

If ANY exist, switch to "update" mode — merge with existing, don't clobber.
```

### 0.3 GitHub Pages Status

```bash
# Check if Pages is already configured
gh api "/repos/{OWNER}/{REPO}/pages" 2>/dev/null
# 404 = not configured (we'll set it up)
# 200 = already configured (check build_type, may need update)
```

---

## Phase 1: Deep Codebase Discovery

**Goal:** Understand the project completely before writing a single line of docs.

### 1.1 Project Identity

Read and extract:

```
package.json (or pyproject.toml, Cargo.toml):
  - name           → site title, install commands
  - version        → changelog reference
  - description    → site_description, hero text
  - author         → site_author, copyright
  - license        → footer
  - repository     → repo_url, repo_name
  - homepage       → site_url fallback
  - keywords       → SEO, categorization
  - engines        → prerequisites section
```

### 1.2 Build & Dev Commands

Extract from scripts/Makefile/justfile:

```
- install command    → Installation page
- build command      → Contributing page
- test command       → Contributing page
- lint command       → Contributing page
- any docs command   → Existing docs setup (avoid conflicts)
```

### 1.3 Source Architecture Map

```
For each directory under src/:
  1. List all .ts files (excluding .test.ts, .spec.ts)
  2. Identify index.ts / barrel exports
  3. Count exported symbols per file
  4. Note directory nesting depth

Output: Module map with hierarchy
  src/
  ├── index.ts          (re-exports: 25 symbols)
  ├── types.ts          (10 types, 4 interfaces)
  ├── bus.ts            (1 function, 1 interface)
  ├── transport/
  │   └── memory.ts     (1 function)
  ├── store/
  │   └── noop.ts       (1 function)
  └── ...
```

### 1.4 Public API Surface

For EVERY exported symbol, capture:

```
- Symbol name
- Kind: type | interface | class | function | const | enum
- Module path (e.g., clock/types.ts)
- Signature (params + return type for functions)
- Properties (for interfaces/classes)
- JSDoc/TSDoc comment (if any)
- Generic parameters
- Related symbols (extends, implements, uses)
```

**Critical:** Read the main entry point (index.ts) to get the EXACT public API. Only document what's exported.

### 1.5 Architecture Patterns

Identify and document:

```
- Core abstractions (interfaces that define plugin points)
- Default implementations (what ships out of the box)
- Factory functions (createX pattern)
- Dependency graph (what imports what)
- Extension model (how users plug in custom implementations)
- Signal flow / data flow (how data moves through the system)
```

### 1.6 Existing Documentation Inventory

Check for:

```
- README.md           → Reuse intro, examples, badges
- CHANGELOG.md        → Link or include
- CONTRIBUTING.md     → Link or include
- LICENSE             → Footer reference
- docs/ directory     → Existing content to migrate
- JSDoc comments      → Pull into API reference
- Code examples in tests → Extract as doc examples
- Architecture diagrams  → Include or recreate
```

### 1.7 Reference Project Analysis (Optional)

If reference projects provided, extract:

```
- mkdocs.yml config     → Match theme, extensions, features
- docs/ tree structure   → Match navigation pattern
- .github/workflows/     → Match CI/CD pattern
- Custom CSS/JS          → Match styling
- Plugin choices         → Match tooling
```

### 1.8 Feature Area Mapping

**This is the most important analysis step.** Map the codebase to user-facing feature areas. This determines guide pages.

**Heuristic: Group by user capability, not by file/directory.**

```
Step 1: List all factory functions / constructors the user calls directly
        (e.g., createSignalBus, createIntervalClock, createFileWatcherSource)

Step 2: Group them by what the user is trying to DO:
        - "I want to set up a signal bus" → Signal Bus guide
        - "I want to schedule things" → Clock System guide
        - "I want to react to external events" → Sources guide
        - "I want to customize behavior" → Pluggable Layers guide

Step 3: For each group, identify:
        - Primary factory function(s)
        - Configuration types/options
        - Related interfaces
        - Common patterns from tests
        - Edge cases / gotchas

Step 4: Order guides by dependency / learning path:
        - Core concept first (the thing everything else plugs into)
        - Then producers (things that create events/signals)
        - Then customization (swappable implementations)
        - Then advanced topics (testing, integration)
```

**Key rule:** If a user would say "I want to do X" and that X maps to a coherent set of APIs, it's a guide page. If it's a single function with no configuration, it belongs in the reference section, not a dedicated guide.

### 1.9 Extract Examples from Tests

**Tests are the source of truth for working code examples.**

```
For each test file:
  1. Scan for describe/it blocks that demonstrate core usage patterns
  2. Look for setup patterns (beforeEach) — these show idiomatic initialization
  3. Find integration tests — these show multi-component examples
  4. Extract the ARRANGE section of arrange-act-assert — this is the user's code

Priority for example extraction:
  1. Integration tests (show real-world usage)
  2. "basic usage" or "happy path" tests
  3. Configuration/options tests (show available options)
  4. Edge case tests (show gotchas for "Advanced" sections)
```

---

## Phase 2: Documentation Architecture

### 2.1 Navigation Structure Decision

**Decision tree based on feature area count (from Phase 1.8 mapping):**

#### Small Library (≤ 3 feature areas)

```yaml
nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - API Reference: reference.md
  - Changelog: changelog.md
```

#### Medium Library (4-8 feature areas)

```yaml
nav:
  - Home: index.md
  - Getting Started:
    - Installation: getting-started/installation.md
    - Quick Start: getting-started/quickstart.md
    - Core Concepts: getting-started/concepts.md
  - Guides:
    - [one page per major feature area]
  - Reference:
    - Types: reference/types.md
    - [one page per module group]
  - Changelog: changelog.md
```

#### Large Library (9+ feature areas)

```yaml
nav:
  - Home: index.md
  - Getting Started:
    - getting-started/index.md
    - Installation: getting-started/installation.md
    - Quick Start: getting-started/quickstart.md
    - Core Concepts: getting-started/concepts.md
  - Guides:
    - guides/index.md
    - [one page per feature area with index]
  - API Reference:
    - reference/index.md
    - [organized by module group]
  - Architecture:
    - architecture/index.md
    - Design Decisions: architecture/decisions.md
  - Changelog: changelog.md
```

### 2.2 Content Plan

For each page, define BEFORE writing:

```
Page: [filename]
  Title: [H1]
  Purpose: [one sentence - why does this page exist?]
  Audience: [who reads this?]
  Prerequisites: [what should they already know?]
  Outline:
    - H2: [section]
      - Content source: [which code/docs to pull from]
      - Code examples: [yes/no, from where]
      - Diagrams: [yes/no, what kind]
    - H2: [section]
      ...
  Links to: [other pages this references]
  Linked from: [other pages that reference this]
```

### 2.3 Mermaid Diagram Plan

Identify diagrams needed:

```
- Architecture overview (block diagram or flowchart)
- Data flow (sequence diagram)
- Type hierarchy (class diagram, if applicable)
- Plugin/extension model (component diagram)
```

---

## Phase 3: Configuration Scaffold

See `reference/templates.md` for full mkdocs.yml, requirements.txt, and workflow templates.

### 3.1 mkdocs.yml

Choose ReadTheDocs or Material theme template from `reference/templates.md`.

### 3.2 requirements.txt

```
# ReadTheDocs theme (built-in, no extra package needed)
mkdocs>=1.6,<2
pymdown-extensions>=10.14

# OR Material theme (bundles pymdownx):
# mkdocs-material>=9.5,<10
```

### 3.3 .gitignore Addition

```
# MkDocs build output
site/
```

### 3.4 Directory Structure

```
{project_root}/
├── mkdocs.yml
├── requirements.txt          (or add to existing)
├── docs/
│   ├── index.md
│   ├── getting-started/
│   │   ├── installation.md
│   │   ├── quickstart.md
│   │   └── concepts.md
│   ├── guides/
│   │   └── {feature}.md
│   ├── reference/
│   │   ├── types.md
│   │   └── {module}.md
│   └── changelog.md
└── .github/
    └── workflows/
        └── docs.yml
```

---

## Phase 3.5: Theme Compatibility Reference

### ReadTheDocs Theme

| Feature | Status | Notes |
|---------|--------|-------|
| Dark mode | Not available | Single light theme only |
| Code copy button | Not available | Users must select + copy manually |
| Tabbed navigation | Sidebar tree only | No top-level tabs |
| Mermaid diagrams | Requires CDN JS | Add `extra_javascript` for mermaid CDN |
| Admonitions | Supported | Built-in styling |
| pymdownx extensions | Requires separate install | `pip install pymdown-extensions` |
| Search | Basic built-in | No suggestions or highlighting |
| prev/next navigation | Built-in | Automatic based on nav order |
| Table of contents | Sidebar + in-page | `toc: permalink: true` |

**Mermaid with ReadTheDocs theme:**
```yaml
# mkdocs.yml — MUST include both:
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format

extra_javascript:
  - https://unpkg.com/mermaid@11/dist/mermaid.min.js
```

### Material Theme

| Feature | Status | Notes |
|---------|--------|-------|
| Dark mode | Built-in toggle | palette with scheme: slate |
| Code copy button | Built-in | `content.code.copy` feature |
| Tabbed navigation | Built-in | `navigation.tabs` feature |
| Mermaid diagrams | Built-in | No extra JS needed |
| Admonitions | Built-in + collapsible | `pymdownx.details` for collapsible |
| pymdownx extensions | Bundled | Comes with `mkdocs-material` |
| Search | Advanced | Suggestions, highlighting, sharing |
| prev/next navigation | Footer links | `navigation.footer` feature |
| Table of contents | Sidebar | `toc.follow` for scroll tracking |

### Admonition Usage Guide

| Type | When to Use |
|------|-------------|
| `!!! note` | Background info the reader should know |
| `!!! tip` | Helpful best practice or shortcut |
| `!!! warning` | Potential pitfall or gotcha |
| `!!! info` | Technical detail or specification |
| `!!! example` | Extended code example with explanation |
| `!!! danger` | Breaking change, data loss, or security concern |

**Rule of thumb:** Max 2 admonitions per page section.

---

## Phase 4: Content Generation

### Writing Standards

**Voice:** Second person ("you"), active voice, present tense.
**Level:** Assume the reader knows TypeScript. Don't explain language features.
**Length:** Prefer short paragraphs (2-3 sentences). Use lists and tables over prose.

**Code examples must:**
- Be copy-pasteable (no `...` or `// rest of code`)
- Import from the package name (not relative paths)
- Include type annotations that the user would actually write
- Come from or be validated against test files when possible

**DO:**
- Show the output/result of code examples where relevant
- Use real variable names from the domain (not `foo`, `bar`)
- Link to related pages on first mention

**DON'T:**
- Explain what TypeScript generics are
- Repeat the same information on multiple pages (link instead)
- Use "simply" or "just" (what's simple to you isn't to the reader)
- Document internal/private APIs

See `reference/page-templates.md` for the full template for each page type (home, install, quickstart, concepts, guides, reference, changelog).

---

## Phase 5: GitHub Actions Workflow

See `reference/templates.md` for the full workflow YAML for both deploy-pages and mike approaches.

### Enable GitHub Pages

```bash
# For deploy-pages workflow (recommended):
gh api --method POST "/repos/{OWNER}/{REPO}/pages" \
  -f "build_type=workflow"

# For mike/gh-pages branch workflow:
gh api --method POST "/repos/{OWNER}/{REPO}/pages" \
  -f "source[branch]=gh-pages" \
  -f "source[path]=/" \
  -f "build_type=legacy"

# Verify configuration:
gh api "/repos/{OWNER}/{REPO}/pages"
```

---

## Phase 6: Build, Test, Deploy

### 6.1 Local Build

```bash
pip install -r requirements.txt
mkdocs build --strict
```

### 6.2 Fix Common Issues

| Issue | Fix |
|-------|-----|
| `WARNING: Page not in nav` | Add page to nav in mkdocs.yml or delete the file |
| `WARNING: Missing link target` | Fix broken `[text](path)` links |
| `ERROR: Config value 'theme'` | Install correct theme package |
| `pymdownx not found` | Add `pymdown-extensions` to requirements.txt |
| `mermaid not rendering` | Add superfences custom_fences config + mermaid JS |

### 6.3 Git Workflow

```bash
git checkout -b docs/mkdocs-site
git add mkdocs.yml requirements.txt docs/ .github/workflows/docs.yml
git commit -m "docs: add MkDocs site with GitHub Pages CI"
git push -u origin docs/mkdocs-site
gh pr create --title "docs: add MkDocs documentation site" --body "..."
gh pr merge --squash
```

### 6.4 Post-Deploy Verification

```bash
gh api "/repos/{OWNER}/{REPO}/pages" --jq '.status'
curl -sI "https://{OWNER}.github.io/{REPO}/" | head -5
```

---

## Phase 7: Cross-Reference Verification

**MANDATORY.** After writing all content, launch fresh verification agents:

### Agent 1: Exports ↔ Docs

Compare `src/index.ts` exports against `docs/reference/exports.md` and `docs/reference/types.md`. Every exported symbol must be documented. Every type definition must match source exactly (including default type parameters).

### Agent 2: Guides ↔ Source

Compare every code example and API description in guide pages against actual source files. Verify import paths, function signatures, option properties, interface methods.

### Fix Any Discrepancies

Commit fixes, rebuild with `--strict`, push.

---

## Phase 8: Quality Checklist

### Content Quality
- [ ] Every exported symbol is documented in reference section
- [ ] Architecture diagram is present and accurate
- [ ] All code examples are copy-pasteable and actually work
- [ ] Quick start builds to a working result
- [ ] No placeholder text ("Lorem ipsum", "TODO", etc.)
- [ ] Cross-references between related pages

### Technical Quality
- [ ] `mkdocs build --strict` passes with zero warnings
- [ ] All internal links resolve
- [ ] Mermaid diagrams render correctly
- [ ] Code syntax highlighting works for TypeScript
- [ ] Table of contents generates correctly

### CI/CD Quality
- [ ] GitHub Actions workflow file is valid
- [ ] Workflow triggers on docs/ and mkdocs.yml changes
- [ ] Workflow includes `workflow_dispatch` for manual triggers
- [ ] GitHub Pages is enabled (build_type matches workflow approach)
- [ ] Concurrency group prevents parallel deploys

### Deployment Quality
- [ ] Site loads at expected URL
- [ ] Navigation works on all pages
- [ ] No 404s on any nav link

---

## Anti-Patterns

1. **Don't generate API docs with placeholder descriptions** — If you can't write a real description, quote the source code.
2. **Don't create deep nesting** — 3 levels max in navigation.
3. **Don't duplicate README wholesale** — Extract and improve, don't copy-paste.
4. **Don't use Material theme features with ReadTheDocs theme** — They're incompatible (e.g., content.code.copy only works in Material).
5. **Don't include test files in API reference** — Only document the public API.
6. **Don't skip the architecture diagram** — It's the single most valuable piece of documentation.
7. **Don't use `mkdocs gh-deploy` with `deploy-pages` action** — Pick one approach.
8. **Don't forget `site/` in .gitignore** — Build artifacts should never be committed.
