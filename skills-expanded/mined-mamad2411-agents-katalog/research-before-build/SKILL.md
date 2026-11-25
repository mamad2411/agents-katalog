---
name: research-before-build
description: Research open-source projects, frameworks, and code on GitHub before building from scratch
version: 2.0.0
triggers:
  - "implement"
  - "add feature"
  - "build"
  - "create new"
  - "need a"
---

# Research Before Build

**ALWAYS search GitHub for open-source projects, frameworks, and reusable code before building from scratch.**

## Philosophy

> "The best code is code you don't have to write."

Before building any significant feature:
1. Search GitHub for **entire projects** to clone/fork as starting point
2. Find **reference implementations** to study architecture
3. Discover **code snippets** and patterns to extract
4. Look for **frameworks/boilerplates** that solve the problem
5. Only build custom if nothing reusable exists

## What to Search For

| Type | Description | Example |
|------|-------------|---------|
| **Starter Templates** | Clone and customize | `nextjs-saas-starter`, `electron-react-boilerplate` |
| **Reference Projects** | Study architecture | Open-source apps doing similar things |
| **Frameworks** | Build on top of | `refine`, `payload`, `medusa` |
| **Code Snippets** | Extract and adapt | Specific implementations in repos |
| **Libraries** | Use as dependency | npm/PyPI packages |

## When to Apply

Use this workflow for:
- New features requiring 100+ lines of code
- Functionality that "feels like a solved problem"
- Infrastructure (auth, caching, queues, search, etc.)
- UI components (forms, tables, modals, etc.)
- Integrations (payments, email, storage, etc.)
- **Entire applications** (admin panels, dashboards, e-commerce)
- **System architecture** patterns

## Research Workflow

### Step 1: Define Requirements

Before searching, clarify:

```markdown
## Requirements Checklist
- [ ] Core functionality needed
- [ ] Tech stack constraints (React, Python, Go, etc.)
- [ ] Scale requirements (users, data volume)
- [ ] Can we use the entire project as base? (clone/fork)
- [ ] Do we just need specific code/patterns to extract?
- [ ] License requirements (MIT, Apache, GPL acceptable?)
```

### Step 2: GitHub Search Strategies

#### A. Find Entire Projects to Clone/Fork

```
# Starter templates and boilerplates
{stack} starter template stars:>500
{stack} boilerplate stars:>1000
{framework} scaffold stars:>500

# Example searches
nextjs saas starter stars:>1000
react admin dashboard stars:>2000
fastapi template stars:>500
electron app boilerplate stars:>1000
```

#### B. Find Reference Implementations

```
# Open-source apps doing what you need
{feature} open source stars:>500
{feature} app stars:>1000 language:{lang}

# Example searches
kanban board react stars:>500
real-time chat application stars:>1000
file manager web stars:>500
markdown editor stars:>1000
```

#### C. Search Code Directly (GitHub Code Search)

```
# Find specific implementations
language:{lang} path:src {function/pattern}
language:typescript "async function upload" path:src
language:python "def websocket_handler"

# Find by file type
filename:auth.ts stars:>100
filename:middleware.py path:src
extension:tsx "useInfiniteScroll"
```

#### D. Find Frameworks to Build On

```
# Headless/extensible frameworks
{domain} framework headless stars:>2000
{domain} cms headless stars:>1000

# Example searches
e-commerce framework headless stars:>2000  → medusa, saleor
admin panel framework stars:>5000          → refine, react-admin
cms headless typescript stars:>3000        → payload, strapi, directus
```

### Step 3: Search Sources (Priority Order)

| Source | Best For | Search Method |
|--------|----------|---------------|
| **GitHub Repos** | Projects to clone/fork | `{keywords} stars:>500` |
| **GitHub Code Search** | Specific implementations | `language:{lang} "{code pattern}"` |
| **GitHub Topics** | Categorized projects | `github.com/topics/{topic}` |
| **Awesome Lists** | Curated collections | `awesome-{domain}` repos |
| **npm/PyPI** | Packaged libraries | Sort by weekly downloads |
| **Dev.to/HN** | Recent comparisons | `{feature} comparison 2025` |

### Step 3: Evaluate Options

For each candidate, assess:

```markdown
## Evaluation Matrix

| Criteria | Weight | Project A | Project B | Project C |
|----------|--------|-----------|-----------|-----------|
| **Fit** (does it solve our problem?) | 30% | | | |
| **Adoption** (stars, downloads, users) | 20% | | | |
| **Maintenance** (last commit, release cadence) | 20% | | | |
| **Documentation** (quality, examples) | 15% | | | |
| **Integration** (fits our stack) | 15% | | | |
| **TOTAL** | 100% | | | |
```

**Red Flags:**
- No commits in 6+ months (unless stable/complete)
- Fewer than 100 GitHub stars for critical functionality
- No TypeScript types (for TS projects)
- Incompatible license
- Single maintainer with no contributors

**Green Flags:**
- Used by major companies
- Active Discord/community
- Comprehensive test suite
- Security audit completed
- Regular release cadence

### Step 4: Decision Framework

```
┌──────────────────────────────────────────────────────────────────┐
│                      DECISION TREE                                │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Is there an open-source PROJECT that does 80%+ of what we need? │
│     │                                                             │
│     ├── YES → CLONE/FORK as starting point                       │
│     │         Customize and extend from there                    │
│     │                                                             │
│     └── NO ↓                                                      │
│                                                                   │
│  Is there a FRAMEWORK we can build on top of?                    │
│     │                                                             │
│     ├── YES → Use framework, add custom features                 │
│     │         (e.g., use Refine for admin, Medusa for e-commerce)│
│     │                                                             │
│     └── NO ↓                                                      │
│                                                                   │
│  Are there REFERENCE PROJECTS to study?                          │
│     │                                                             │
│     ├── YES → Extract patterns, architecture, code snippets      │
│     │         Build custom but informed by what works            │
│     │                                                             │
│     └── NO ↓                                                      │
│                                                                   │
│  Is there a LIBRARY that solves part of it?                      │
│     │                                                             │
│     ├── YES → Use library + build remaining custom               │
│     │                                                             │
│     └── NO → BUILD from scratch (document why nothing fit)       │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Step 5: Reuse Strategies

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **Clone & Customize** | Project does 80%+ of what you need | Fork `cal.com` for scheduling app |
| **Framework + Extend** | Need flexibility but solid foundation | Use `refine` for admin panel |
| **Extract Patterns** | Architecture is right, details differ | Study how `linear` does offline-first |
| **Copy Code Snippets** | Specific implementation needed | Extract auth flow from reference project |
| **Use as Dependency** | Self-contained functionality | Add `tanstack-query` for data fetching |

## Integration Strategies

### Strategy 1: Clone & Customize (Entire Project)

When a project does 80%+ of what you need:

```bash
# Clone the project
git clone https://github.com/great-project/starter.git my-project
cd my-project

# Remove their git history, start fresh
rm -rf .git
git init

# Document the base
echo "Based on: https://github.com/great-project/starter" > BASE_PROJECT.md
echo "Original License: MIT" >> BASE_PROJECT.md

# Customize: rename, rebrand, modify
# Keep their architecture, change the details
```

**Best for:** SaaS starters, admin templates, full-stack boilerplates

### Strategy 2: Fork & Extend

When you'll need to pull upstream updates:

```bash
# Fork the repo (keeps connection to original)
gh repo fork original/repo --clone
cd repo

# Create feature branch for customizations
git checkout -b our-customizations

# Track upstream for updates
git remote add upstream https://github.com/original/repo.git

# Document ALL changes
touch FORK_CHANGES.md
```

**Best for:** Active projects you want updates from

### Strategy 3: Extract Code Patterns

When architecture fits but implementation differs:

```bash
# Clone just to study (don't use as base)
git clone --depth 1 https://github.com/reference/project.git ./reference
```

```markdown
## Code Extracted from {project}

### Pattern: Real-time sync
- Source: `reference/src/sync/`
- Adapted to: `our-app/src/sync/`
- Changes made: {describe adaptations}

### Pattern: Optimistic updates
- Source: `reference/src/hooks/useOptimistic.ts`
- Adapted to: `our-app/src/hooks/useOptimistic.ts`
```

**Best for:** Complex patterns, algorithms, architectural approaches

### Strategy 4: Build on Framework

When a framework exists for your domain:

```typescript
// Use domain-specific framework instead of raw React/Express
// Example: Refine for admin panels

import { Refine } from "@refinedev/core"
import { dataProvider } from "@refinedev/simple-rest"

// Get CRUD, auth, routing out of box
// Just configure and customize
export default function App() {
  return (
    <Refine
      dataProvider={dataProvider("https://api.example.com")}
      resources={[
        { name: "users", list: UserList, edit: UserEdit },
        { name: "orders", list: OrderList }
      ]}
    />
  )
}
```

**Best for:** Admin panels, e-commerce, CMS, dashboards

### Strategy 5: Use as Library/Dependency

When you just need specific functionality:

```typescript
import { createClient } from 'well-maintained-lib'

const client = createClient({
  // configure as documented
})
```

**Best for:** Auth, payments, file upload, email, etc.

## Common Searches by Domain

### Full Applications / Starters

```bash
# SaaS Starters (clone entire project)
nextjs saas starter stars:>1000          # → supastarter, next-saas-starter
react saas boilerplate stars:>500        # → bullet-proof-react, refine
t3 stack template stars:>500             # → create-t3-app

# Admin Dashboards
admin dashboard react stars:>2000        # → react-admin, refine
admin panel template stars:>1000         # → tremor, shadcn-admin

# E-commerce
e-commerce open source stars:>2000       # → medusa, saleor, vendure
storefront template stars:>500           # → next-commerce, medusa-starter
```

### Specific Features

```bash
# Real-time / Collaboration
real-time collaboration stars:>500       # → yjs, liveblocks examples
multiplayer cursor stars:>100            # → study implementations
websocket chat stars:>500                # → clone and adapt

# File Management
file manager web stars:>500              # → filebrowser, cloud-commander
file upload react stars:>300             # → uppy, filepond examples

# Rich Text / Editors
markdown editor react stars:>1000        # → milkdown, tiptap
notion clone stars:>500                  # → study architecture
wysiwyg editor stars:>2000               # → tiptap, lexical, slate
```

### Infrastructure Code

```bash
# Authentication Implementations
authentication flow typescript           # → code search
filename:auth.ts middleware              # → specific files
nextauth example stars:>100              # → reference implementations

# API Patterns
rest api typescript template stars:>500  # → clone as base
graphql server starter stars:>500        # → apollo-server-examples

# Background Jobs
job queue implementation node            # → study patterns
cron scheduler typescript stars:>300     # → bullmq examples
```

### GitHub Topics (Curated Lists)

```
github.com/topics/boilerplate
github.com/topics/starter-template
github.com/topics/saas
github.com/topics/admin-dashboard
github.com/topics/headless-cms
```

### Awesome Lists

```bash
awesome-selfhosted       # → full applications to study/deploy
awesome-react            # → component libraries and patterns
awesome-nextjs           # → Next.js specific projects
awesome-nodejs           # → Node.js frameworks and tools
awesome-python           # → Python frameworks and tools
```

## Documentation Template

After research, document your decision:

```markdown
## Feature: {Feature Name}

### Requirements
- {requirement 1}
- {requirement 2}

### Projects/Code Evaluated

#### Option 1: {Project/Repo Name}
- **URL**: https://github.com/...
- **Stars**: {n} | **Last Commit**: {date}
- **Verdict**: CLONE / FORK / EXTRACT / SKIP
- **Pros**: ...
- **Cons**: ...

#### Option 2: {Framework Name}
- **URL**: https://github.com/...
- **Stars**: {n} | **Last Commit**: {date}
- **Verdict**: USE / SKIP
- **Pros**: ...
- **Cons**: ...

### Decision
**{CLONE/FORK/EXTRACT/FRAMEWORK/LIBRARY/BUILD}**: {project/library name}

### Reuse Plan
- [ ] Base project: {url}
- [ ] Code to extract: {specific files/patterns}
- [ ] Customizations needed: {list}
- [ ] Libraries to add: {list}

### Rationale
{Why this choice - what made it better than alternatives}
```

## Anti-Patterns

### ❌ NIH (Not Invented Here) Syndrome
Building from scratch when mature solutions exist.

### ❌ Premature Abstraction
Wrapping libraries before understanding them.

### ❌ Outdated Research
Using a library without checking recent alternatives.

### ❌ Star Worship
Choosing solely based on GitHub stars without evaluation.

### ❌ Scope Creep Research
Spending days researching instead of making a decision.

## Time Limits

| Feature Size | Research Time | Decision Deadline |
|--------------|---------------|-------------------|
| Small (< 1 day build) | 15-30 min | Same session |
| Medium (1-3 days build) | 1-2 hours | Same day |
| Large (1+ week build) | 2-4 hours | Next day |

---

*"Weeks of coding can save hours of research" - Unknown*
