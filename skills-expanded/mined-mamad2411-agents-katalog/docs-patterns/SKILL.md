---
name: docs-patterns
description: "Technical documentation patterns, templates, and best practices. Reference material for docs-writer, docs-planner, and docs-reviewer agents when producing or evaluating documentation. Covers writing style, document structure, markdown conventions, and audience-specific guidance."
compatibility: cursor
---
# Documentation Patterns — Writing & Structure Reference

Quick-reference guide for technical documentation. Used by the docs planner ecosystem to produce consistent, high-quality documentation.

## When to Apply

Reference these patterns when:
- Writing any form of technical documentation
- Reviewing documentation for quality and consistency
- Choosing document structure for a given audience
- Deciding what sections a document type requires

---

## 1. Writing Fundamentals

### The Inverted Pyramid

Lead with the most important information. Structure every document and section so that a reader who stops at any point has gotten the most valuable content available.

```
Most important (what + why)
├── Supporting details (how)
├── Additional context (background, alternatives)
└── Reference material (appendix, links)
```

### Audience Calibration

| Audience | Tone | Detail Level | Jargon | Examples |
|----------|------|-------------|--------|----------|
| New contributor | Welcoming, explicit | High — assume nothing | Define all terms | Step-by-step walkthrough |
| Team developer | Direct, concise | Medium — assume project context | Project jargon OK | Key patterns, gotchas |
| Stakeholder / PM | Business-focused | Low-medium — outcome oriented | Minimize, explain tech | Impact, metrics, timelines |
| End user | Friendly, task-oriented | High for tasks, low for theory | Avoid entirely | Goal-oriented walkthroughs |
| Future self/team | Precise, complete | High for decisions/context | Acceptable | Why, not just what |

### Sentence-Level Rules

- **Active voice**: "The system validates the token" not "The token is validated by the system"
- **Imperative mood for instructions**: "Run the migration" not "You should run the migration"
- **Concrete over abstract**: "Responds in under 200ms" not "Responds quickly"
- **Short sentences**: If a sentence has more than one comma, consider splitting it
- **No weasel words**: Avoid "simply", "just", "easily", "obviously", "clearly"
- **No future tense for current state**: "The API returns JSON" not "The API will return JSON" (unless it is genuinely future)

### Paragraph Structure

- One idea per paragraph
- First sentence is the topic sentence (supports scanning)
- 3-5 sentences maximum
- Blank line between paragraphs

---

## 2. Markdown Conventions

### Headers

```markdown
# Document Title (H1 — exactly one per document)

## Major Sections (H2)

### Subsections (H3)

#### Rarely needed (H4 — if you need H5+, restructure)
```

- Never skip levels (no H1 then H3)
- Use sentence case for headers: "Getting started" not "Getting Started" (unless project convention differs)
- No trailing punctuation on headers

### Code Blocks

Always use fenced code blocks with language hints:

````markdown
```bash
npm install
npm run dev
```

```typescript
interface User {
  id: string;
  name: string;
}
```

```yaml
name: CI Pipeline
on: [push, pull_request]
```
````

- Use `bash` for shell commands (not `sh` or `shell`)
- Use `console` for output that includes both commands and their output
- Inline code for: file names (`README.md`), function names (`fetchUser()`), config values (`true`), CLI flags (`--verbose`)

### Tables

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |
```

- Use tables for structured comparisons, reference data, or option matrices
- Left-align text columns, right-align numbers
- Keep cell content concise — if a cell needs multiple lines, use a list instead

### Lists

- Use `-` for unordered lists (not `*`)
- Use `1.` for ordered lists where sequence matters
- Use `- [ ]` for checklists/task lists
- Nest with 2-space indent
- Keep list items parallel in structure (all start with verbs, or all are noun phrases)

### Links

```markdown
[visible text](URL)                    # external link
[other doc](./docs/other.md)           # relative link (preferred for repo docs)
[section](#section-name)               # anchor link within same doc
```

- Use relative links for references within the same repository
- Use descriptive link text: "see the [configuration guide](./docs/config.md)" not "click [here](./docs/config.md)"

### Admonitions / Callouts

```markdown
> **Note:** Additional context that is helpful but not critical.

> **Warning:** Important information that could cause problems if ignored.

> **Important:** Critical information required for correct usage.
```

---

## 3. Document Type Patterns

### README — The 30-Second Test

A good README answers these questions within 30 seconds of scanning:
1. What is this project?
2. Why would I use it?
3. How do I get started?

**Required sections** (in order):
1. Title + one-line description
2. Overview (2-3 paragraphs)
3. Getting Started (prerequisites, install, quick start)
4. Usage (key patterns)

**Recommended sections:**
5. Configuration
6. Architecture (for non-trivial projects)
7. Contributing
8. License

**Anti-patterns:**
- Badge walls at the top before the description
- Extremely long README when content should be in separate docs
- "TODO" sections left in published READMEs
- Installation instructions that have never been tested on a clean environment

### PRD — The Decision Enabler

A good PRD enables a team to decide: build this or not, and if yes, what exactly.

**Structure priorities:**
1. Problem > Solution (spend more space on the problem than the solution)
2. Requirements must be testable ("users can reset their password via email" not "improve account security")
3. Non-goals are as important as goals (they prevent scope creep)
4. Success metrics must be measurable before launch, not just after

**Common mistakes:**
- Solution masquerading as a problem statement
- Requirements that are actually implementation details
- Missing non-functional requirements (performance, security, accessibility)
- No explicit non-goals section

### Epic — The Implementation Contract

A good epic is a contract between planning and implementation. The implementer should be able to start work without a verbal walkthrough.

**Story sizing heuristic:**
- **Small**: 1-2 files changed, clear pattern to follow, < 1 day
- **Medium**: 3-5 files, some design decisions, 1-2 days
- **Large**: 5+ files or new patterns needed, 2-3 days
- **Too large**: > 3 days — break it down further

**Acceptance criteria rules:**
- Start with a verb: "Displays...", "Returns...", "Sends...", "Prevents..."
- Be testable: someone can verify yes/no whether the criterion is met
- Cover the happy path AND key error cases
- Include performance criteria if relevant ("loads in < 500ms")

**Anti-patterns:**
- Stories without acceptance criteria
- Circular dependencies between stories
- Estimates without reading the codebase
- "Investigate" stories with no definition of done

### ADR — The Decision Record

A good ADR explains the decision to someone joining the team 2 years from now.

**The litmus test:** Can someone who disagrees with the decision understand WHY it was made after reading this ADR?

**Key principles:**
- Context should explain the forces at play, not just the technical landscape
- Alternatives must be genuinely considered, not straw men
- Consequences must include real downsides, not just benefits
- Status should be accurate (Proposed until actually accepted)

**Numbering:** Sequential integers (ADR-001, ADR-002). Never reuse numbers, even for superseded ADRs.

### Changelog — The Release Narrative

A good changelog tells users what changed, why they should care, and if they need to do anything.

**Keep a Changelog format** (the standard):
- Group by: Added, Changed, Deprecated, Removed, Fixed, Security
- Newest version first
- Include dates with each version
- Human-readable descriptions (not commit hashes)
- Link each version to a diff/compare URL

**Writing entries:**
- "Added dark mode support for all screens" not "feat: dark mode"
- "Fixed crash when opening empty folders" not "fix: null check"
- Mention breaking changes prominently with migration instructions

### Contributing Guide — The Welcome Mat

A good contributing guide gets someone from "I want to help" to "I submitted a PR" with zero blocked moments.

**The 5-minute test:** Can a new contributor set up the dev environment and run tests within 5 minutes of reading this guide?

**Must include:**
1. How to set up the development environment (exact commands)
2. How to run tests
3. How to submit a change (branching, PR process)
4. Code style expectations (or link to linter config)

---

## 4. Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Documentation rot | Docs written once, never updated | Include doc updates in PR checklists; review docs quarterly |
| Copy-paste tutorials | Entire tutorial pasted with no project context | Write project-specific instructions; link to official docs for background |
| Wall of text | No headers, lists, or code blocks | Structure with headers every 3-5 paragraphs; use lists for steps |
| Assumed knowledge | "Set up the database" with no details | Spell out every command; link to prerequisite knowledge |
| Version lies | "Requires Node 14" when it actually needs 18 | Verify versions in CI; automate version checks in docs |
| Dead links | References to moved/deleted content | Check links in CI; use relative links within repos |
| Passive voice overuse | "The request is processed by the server" | Rewrite: "The server processes the request" |

---

## 5. File Organization Patterns

### Flat docs directory (small projects)
```
docs/
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── architecture.md
└── api.md
```

### Categorized docs (medium projects)
```
docs/
├── getting-started/
│   ├── installation.md
│   └── quick-start.md
├── guides/
│   ├── configuration.md
│   └── deployment.md
├── architecture/
│   ├── overview.md
│   └── adr/
│       ├── ADR-001-database-choice.md
│       └── ADR-002-api-design.md
├── api/
│   └── reference.md
└── planning/
    ├── epics/
    └── roadmap.md
```

### Docs-as-code (large projects)
```
docs/
├── docusaurus.config.js (or mkdocs.yml, etc.)
├── src/
│   └── pages/
├── docs/
│   ├── intro.md
│   ├── getting-started/
│   ├── guides/
│   ├── api/
│   └── contributing/
└── static/
    └── img/
```
