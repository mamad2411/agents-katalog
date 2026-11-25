---
name: "content-strategy-patterns"
description: "Documentation strategy patterns: the Diátaxis classification test, ROT analysis and staleness signals, single-source publishing, navigation depth and breadth, content versioning, documentation metrics, and anti-patterns. Use when planning or auditing a documentation set."
---

# Content Strategy Patterns

## Diátaxis Framework

The four content types serve fundamentally different user needs. Mixing types in a single article creates confusion.

| Type | User Need | User State | Analogy |
|------|-----------|-----------|---------|
| Tutorial | Learning | Studying | Teaching a child to cook |
| How-To | Accomplishing a task | Working | Recipe for experienced cook |
| Reference | Looking up information | Working | Ingredient reference card |
| Explanation | Understanding | Studying | Article on nutrition science |

### Diátaxis classification test

Ask: "What is the user doing when they need this content?"

- Learning a new skill for the first time → Tutorial
- Trying to complete a specific task they know they want to do → How-To
- Looking up a specific value, option, or format → Reference
- Trying to understand why something works the way it does → Explanation

### Type-mixing anti-patterns

```
# Bad: explanation mixed into how-to (slows down task completion)
## How to Connect to the Database

PostgreSQL is a relational database management system originally developed
at the University of California Berkeley. It uses a client-server model...
[2 paragraphs of background]

Here's how to connect:
1. Install the driver...

# Good: how-to is just the task
## How to Connect to the Database

**Prerequisites**: PostgreSQL 14+, `pg` npm package installed

1. Import the client: `import { Client } from 'pg'`
2. Configure the connection: ...
3. Test the connection: ...

For background on the connection pool design, see [Connection Architecture](/concepts/connection-pool).
```

## ROT Analysis

Use ROT to classify articles for action in a content audit:

| Category | Definition | Signal | Action |
|----------|-----------|--------|--------|
| **Redundant** | Duplicate or heavily overlapping content | 2+ articles answer the same question | Merge or redirect |
| **Outdated** | References deprecated features, old UI, or past versions | Last updated date, version references | Rewrite or archive |
| **Trivial** | Low-value content that provides little help | Low traffic, thin content, stub articles | Delete or merge |

### Staleness signals

- Last-modified date > 18 months for active product area
- Version number in article doesn't match current (e.g., "v2" when product is on v4)
- Screenshots showing old UI
- References to deprecated endpoints, methods, or services
- Step counts that don't match current UI flow

## Single-Source Publishing

When the same content must appear in multiple contexts, use includes/snippets rather than copy-paste:

```markdown
<!-- shared-snippet: auth-note.md -->
> **Authentication required**: All endpoints require a Bearer token.
> Obtain tokens via POST /auth/token.

<!-- In API guide -->
## Working with the API
%%include auth-note.md%%

<!-- In quickstart -->
## Making Your First Request
%%include auth-note.md%%
```

Docusaurus uses `{@import}`, MkDocs uses `snippets`, GitBook uses `{% include %}`.

## Navigation Depth and Breadth

**Rule of 7 (Miller's Law applied to navigation)**: Top-level navigation items should number 5-7. Beyond that, users cannot hold the structure in working memory.

**3-click rule**: Every article should be reachable within 3 clicks from the home page.

**Breadth vs depth tradeoff**:
- Shallow-broad: 7 top categories, each with many articles directly under them. Good for search-first users.
- Deep-narrow: 3 top categories, 3 sub-levels each. Good for users who browse the hierarchy.

Most developer docs benefit from shallow-broad: developers typically search or use Ctrl+K, not breadcrumb navigation.

## Content Versioning Strategies

| Strategy | Tools | When to use |
|----------|-------|-------------|
| Per-version branches | Docusaurus versioning, git branches | Major versions with breaking changes; active support for 2+ versions |
| Conditional content | MDX `{props.version}`, Hugo shortcodes | Minor differences between versions; single codebase preferred |
| Version-agnostic + migration guides | Single docs + migration guide articles | When API is stable; changes are additive |
| Date-stamped snapshots | PDF exports, archive folders | Compliance, regulated industries |

## Documentation Metrics

**Measure what indicates user success, not just page views:**

| Metric | What it indicates | Tool |
|--------|------------------|------|
| Search success rate | Users find what they searched for | Algolia Analytics, Docsearch |
| Time-to-first-success | How long from landing to completing quickstart | Custom GA4 events |
| Search exit rate | Users search and leave without clicking | GA4 + Algolia |
| Article helpfulness rating | Thumbs up/down feedback | Built into Docusaurus, MkDocs Material |
| Support ticket deflection | Reduction in tickets for topics covered in docs | Zendesk integration, correlation |

**Threshold targets** (baseline to aim for):
- Search click-through rate > 60% (user found a relevant result)
- Article helpfulness > 70% positive
- Quickstart completion > 40% (users who start, finish)

## Anti-Patterns

### Organizing by internal team structure
```
# Bad: users don't care about internal org
/platform-team/
/infrastructure-team/
/product-team/

# Good: organize by user goal
/get-started/
/deploy/
/configure/
```

### Writing for the happy path only
Every how-to should anticipate failure. At minimum: what to do if a prerequisite is not met, what to do if the expected output doesn't appear.

### Version-agnostic screenshots
Screenshots without version context become wrong immediately after a UI change. Add version stamps or prefer text-based instructions where the UI changes frequently.

### Orphan articles
Articles with no inbound links or navigation path. Users can only find them via search. Run link graph analysis to identify orphans.

## References
- [Diátaxis Framework](https://diataxis.fr/) - Daniele Procida
- [Every Page Is Page One](https://everypageispageone.com/) - Mark Baker
- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Docusaurus versioning](https://docusaurus.io/docs/versioning)
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
