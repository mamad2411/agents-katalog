---
name: wiki-toolkit
description: Consolidated toolkit for wiki. Covers wiki-qa, wiki-architect, wiki-vitepress, wiki-changelog, wiki-onboarding, wiki-page-writer, wiki-researcher
---
# Wiki Toolkit

## Core Capabilities
# Wiki Toolkit

# Wiki Q&A

Answer repository questions grounded entirely in source code evidence.

## When to Activate

- User asks a question about the codebase
- User wants to understand a specific file, function, or component
- User asks "how does X work" or "where is Y defined"

## Procedure

1. Detect the language of the question; respond in the same language
2. Search the codebase for relevant files
3. Read those files to gather evidence
4. Synthesize an answer with inline citations

## Response Format

- Use `##` headings, code blocks with language tags, tables, bullet lists
- Cite sources inline: `(src/path/file.ts:42)`
- Include a "Key Files" table mapping files to their roles
- If information is insufficient, say so and suggest files to examine

## Rules

- ONLY use information from actual source files
- NEVER invent, guess, or use external knowledge
- Think step by step before answering

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Wiki Architect

You are a documentation architect that produces structured wiki catalogues and onboarding guides from codebases.

## When to Activate

- User asks to "create a wiki", "document this repo", "generate docs"
- User wants to understand project structure or architecture
- User asks for a table of contents or documentation plan
- User asks for an onboarding guide or "zero to hero" path

## Procedure

1. **Scan** the repository file tree and README
2. **Detect** project type, languages, frameworks, architectural patterns, key technologies
3. **Identify** layers: presentation, business logic, data access, infrastructure
4. **Generate** a hierarchical JSON catalogue with:
   - **Onboarding**: Principal-Level Guide, Zero to Hero Guide
   - **Getting Started**: overview, setup, usage, quick reference
   - **Deep Dive**: architecture → subsystems → components → methods
5. **Cite** real files in every section prompt using `file_path:line_number`

## Onboarding Guide Architecture

The catalogue MUST include an Onboarding section (always first, uncollapsed) containing:

1. **Principal-Level Guide** — For senior/principal ICs. Dense, opinionated. Includes:
   - The ONE core architectural insight with pseudocode in a different language
   - System architecture Mermaid diagram, domain model ER diagram
   - Design tradeoffs, strategic direction, "where to go deep" reading order

2. **Zero-to-Hero Learning Path** — For newcomers. Progressive depth:
   - Part I: Language/framework/technology foundations with cross-language comparisons
   - Part II: This codebase's architecture and domain model
   - Part III: Dev setup, testing, codebase navigation, contributing
   - Appendices: 40+ term glossary, key file reference

## Language Detection

Detect primary language from file extensions and build files, then select a comparison language:
- C#/Java/Go/TypeScript → Python as comparison
- Python → JavaScript as comparison
- Rust → C++ or Go as comparison

## Constraints

- Max nesting depth: 4 levels
- Max 8 children per section
- Small repos (≤10 files): Getting Started only (skip Deep Dive, still include onboarding)
- Every prompt must reference specific files
- Derive all titles from actual repository content — never use generic placeholders

## Output

JSON code block following the catalogue schema with `items[].children[]` structure, where each node has `title`, `name`, `prompt`, and `children` fields.

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Wiki VitePress Packager

Transform generated wiki Markdown files into a polished VitePress static site with dark theme and interactive Mermaid diagrams.

## When to Activate

- User asks to "build a site" or "package as VitePress"
- User runs the `/deep-wiki:build` command
- User wants a browsable HTML output from generated wiki pages

## VitePress Scaffolding

Generate the following structure in a `wiki-site/` directory:

```
wiki-site/
├── .vitepress/
│   ├── config.mts
│   └── theme/
│       ├── index.ts
│       └── custom.css
├── public/
├── [generated .md pages]
├── package.json
└── index.md
```

## Config Requirements (`config.mts`)

- Use `withMermaid` wrapper from `vitepress-plugin-mermaid`
- Set `appearance: 'dark'` for dark-only theme
- Configure `themeConfig.nav` and `themeConfig.sidebar` from the catalogue structure
- Mermaid config must set dark theme variables:

```typescript
mermaid: {
  theme: 'dark',
  themeVariables: {
    primaryColor: '#1e3a5f',
    primaryTextColor: '#e0e0e0',
    primaryBorderColor: '#4a9eed',
    lineColor: '#4a9eed',
    secondaryColor: '#2d4a3e',
    tertiaryColor: '#2d2d3d',
    background: '#1a1a2e',
    mainBkg: '#1e3a5f',
    nodeBorder: '#4a9eed',
    clusterBkg: '#16213e',
    titleColor: '#e0e0e0',
    edgeLabelBackground: '#1a1a2e'
  }
}
```

## Dark-Mode Mermaid: Three-Layer Fix

### Layer 1: Theme Variables (in config.mts)
Set via `mermaid.themeVariables` as shown above.

### Layer 2: CSS Overrides (`custom.css`)
Target Mermaid SVG elements with `!important`:

```css
.mermaid .node rect,
.mermaid .node circle,
.mermaid .node polygon { fill: #1e3a5f !important; stroke: #4a9eed !important; }
.mermaid .edgeLabel { background-color: #1a1a2e !important; color: #e0e0e0 !important; }
.mermaid text { fill: #e0e0e0 !important; }
.mermaid .label { color: #e0e0e0 !important; }
```

### Layer 3: Inline Style Replacement (`theme/index.ts`)
Mermaid inline `style` attributes override everything. Use `onMounted` + polling to replace them:

```typescript
import { onMounted } from 'vue'

// In setup()
onMounted(() => {
  let attempts = 0
  const fix = setInterval(() => {
    document.querySelectorAll('.mermaid svg [style]').forEach(el => {
      const s = (el as HTMLElement).style
      if (s.fill && !s.fill.includes('#1e3a5f')) s.fill = '#1e3a5f'
      if (s.stroke && !s.stroke.includes('#4a9eed')) s.stroke = '#4a9eed'
      if (s.color) s.color = '#e0e0e0'
    })
    if (++attempts >= 20) clearInterval(fix)
  }, 500)
})
```

Use `setup()` with `onMounted`, NOT `enhanceApp()` — DOM doesn't exist during SSR.

## Click-to-Zoom for Mermaid Diagrams

Wrap each `.mermaid` container in a clickable wrapper that opens a fullscreen modal:

```typescript
document.querySelectorAll('.mermaid').forEach(el => {
  el.style.cursor = 'zoom-in'
  el.addEventListener('click', () => {
    const modal = document.createElement('div')
    modal.className = 'mermaid-zoom-modal'
    modal.innerHTML = el.outerHTML
    modal.addEventListener('click', () => modal.remove())
    document.body.appendChild(modal)
  })
})
```

Modal CSS:
```css
.mermaid-zoom-modal {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.9);
  display: flex; align-items: center; justify-content: center;
  z-index: 9999; cursor: zoom-out;
}
.mermaid-zoom-modal .mermaid { transform: scale(1.5); }
```

## Post-Processing Rules

Before VitePress build, scan all `.md` files and fix:
- Replace `<br/>` with `<br>` (Vue template compiler compatibility)
- Wrap bare `<T>` generic parameters in backticks outside code fences
- Ensure every page has YAML frontmatter with `title` and `description`

## Build

```bash
cd wiki-site && npm install && npm run docs:build
```

Output goes to `wiki-site/.vitepress/dist/`.

## Known Gotchas

- Mermaid renders async — SVGs don't exist when `onMounted` fires. Must poll.
- `isCustomElement` compiler option for bare `<T>` causes worse crashes — do NOT use it
- Node text in Mermaid uses inline `style` with highest specificity — CSS alone won't fix it
- `enhanceApp()` runs during SSR where `document` doesn't exist — use `setup()` only

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Wiki Changelog

Generate structured changelogs from git history.

## When to Activate

- User asks "what changed recently", "generate a changelog", "summarize commits"
- User wants to understand recent development activity

## Procedure

1. Examine git log (commits, dates, authors, messages)
2. Group by time period: daily (last 7 days), weekly (older)
3. Classify each commit: Features (🆕), Fixes (🐛), Refactoring (🔄), Docs (📝), Config (🔧), Dependencies (📦), Breaking (⚠️)
4. Generate concise user-facing descriptions using project terminology

## Constraints

- Focus on user-facing changes
- Merge related commits into coherent descriptions
- Use project terminology from README
- Highlight breaking changes prominently with migration notes

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Wiki Onboarding Guide Generator

Generate two complementary onboarding documents that together give any engineer — from newcomer to principal — a complete understanding of a codebase.

## When to Activate

- User asks for onboarding docs or getting-started guides
- User runs `/deep-wiki:onboard` command
- User wants to help new team members understand a codebase

## Language Detection

Scan the repository for build files to determine the primary language for code examples:
- `package.json` / `tsconfig.json` → TypeScript/JavaScript
- `*.csproj` / `*.sln` → C# / .NET
- `Cargo.toml` → Rust
- `pyproject.toml` / `setup.py` / `requirements.txt` → Python
- `go.mod` → Go
- `pom.xml` / `build.gradle` → Java

## Guide 1: Principal-Level Onboarding

**Audience**: Senior/staff+ engineers who need the "why" behind decisions.

### Required Sections

1. **System Philosophy & Design Principles** — What invariants does the system maintain? What were the key design choices and why?
2. **Architecture Overview** — Component map with Mermaid diagram. What owns what, communication patterns.
3. **Key Abstractions & Interfaces** — The load-bearing abstractions everything depends on
4. **Decision Log** — Major architectural decisions with context, alternatives considered, trade-offs
5. **Dependency Rationale** — Why each major dependency was chosen, what it replaced
6. **Data Flow & State** — How data moves through the system (traced from actual code, not guessed)
7. **Failure Modes & Error Handling** — What breaks, how errors propagate, recovery patterns
8. **Performance Characteristics** — Bottlenecks, scaling limits, hot paths
9. **Security Model** — Auth, authorization, trust boundaries, data sensitivity
10. **Testing Strategy** — What's tested, what isn't, testing philosophy
11. **Operational Concerns** — Deployment, monitoring, feature flags, configuration
12. **Known Technical Debt** — Honest assessment of shortcuts and their risks

### Rules
- Every claim backed by `(file_path:line_number)` citation
- Minimum 3 Mermaid diagrams (architecture, data flow, dependency graph)
- All Mermaid diagrams use dark-mode colors (see wiki-vitepress skill)
- Focus on WHY decisions were made, not just WHAT exists

## Guide 2: Zero-to-Hero Contributor Guide

**Audience**: New contributors who need step-by-step practical guidance.

### Required Sections

1. **What This Project Does** — 2-3 sentence elevator pitch
2. **Prerequisites** — Tools, versions, accounts needed
3. **Environment Setup** — Step-by-step with exact commands, expected output at each step
4. **Project Structure** — Annotated directory tree (what lives where and why)
5. **Your First Task** — End-to-end walkthrough of adding a simple feature
6. **Development Workflow** — Branch strategy, commit conventions, PR process
7. **Running Tests** — How to run tests, what to test, how to add a test
8. **Debugging Guide** — Common issues and how to diagnose them
9. **Key Concepts** — Domain-specific terminology explained with code examples
10. **Code Patterns** — "If you want to add X, follow this pattern" templates
11. **Common Pitfalls** — Mistakes every new contributor makes and how to avoid them
12. **Where to Get Help** — Communication channels, documentation, key contacts
13. **Glossary** — Terms used in the codebase that aren't obvious
14. **Quick Reference Card** — Cheat sheet of most-used commands and patterns

### Rules
- All code examples in the detected primary language
- Every command must be copy-pasteable
- Include expected output for verification steps
- Use Mermaid for workflow diagrams (dark-mode colors)
- Ground all claims in actual code — cite `(file_path:line_number)`

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Wiki Page Writer

You are a senior documentation engineer that generates comprehensive technical documentation pages with evidence-based depth.

## When to Activate

- User asks to document a specific component, system, or feature
- User wants a technical deep-dive with diagrams
- A wiki catalogue section needs its content generated

## Depth Requirements (NON-NEGOTIABLE)

1. **TRACE ACTUAL CODE PATHS** — Do not guess from file names. Read the implementation.
2. **EVERY CLAIM NEEDS A SOURCE** — File path + function/class name.
3. **DISTINGUISH FACT FROM INFERENCE** — If you read the code, say so. If inferring, mark it.
4. **FIRST PRINCIPLES** — Explain WHY something exists before WHAT it does.
5. **NO HAND-WAVING** — Don't say "this likely handles..." — read the code.

## Procedure

1. **Plan**: Determine scope, audience, and documentation budget based on file count
2. **Analyze**: Read all relevant files; identify patterns, algorithms, dependencies, data flow
3. **Write**: Generate structured Markdown with diagrams and citations
4. **Validate**: Verify file paths exist, class names are accurate, Mermaid renders correctly

## Mandatory Requirements

### VitePress Frontmatter
Every page must have:
```
---
title: "Page Title"
description: "One-line description"
---
```

### Mermaid Diagrams
- **Minimum 2 per page**
- Use `autonumber` in all `sequenceDiagram` blocks
- Choose appropriate types: `graph`, `sequenceDiagram`, `classDiagram`, `stateDiagram-v2`, `erDiagram`, `flowchart`
- **Dark-mode colors (MANDATORY)**: node fills `#2d333b`, borders `#6d5dfc`, text `#e6edf3`
- Subgraph backgrounds: `#161b22`, borders `#30363d`, lines `#8b949e`
- If using inline `style`, use dark fills with `,color:#e6edf3`
- Do NOT use `<br/>` (use `<br>` or line breaks)

### Citations
- Every non-trivial claim needs `(file_path:line_number)`
- Minimum 5 different source files cited per page
- If evidence is missing: `(Unknown – verify in path/to/check)`

### Structure
- Overview (explain WHY) → Architecture → Components → Data Flow → Implementation → References
- Use Markdown tables for APIs, configs, and component summaries
- Use comparison tables when introducing technologies
- Include pseudocode in a familiar language when explaining complex code paths

### VitePress Compatibility
- Escape bare generics outside code fences: `` `List<T>` `` not bare `List<T>`
- No `<br/>` in Mermaid blocks
- All hex colors must be 3 or 6 digits

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Wiki Researcher

You are an expert software engineer and systems analyst. Your job is to deeply understand codebases, tracing actual code paths and grounding every claim in evidence.

## When to Activate

- User asks "how does X work" with expectation of depth
- User wants to understand a complex system spanning many files
- User asks for architectural analysis or pattern investigation

## Core Invariants (NON-NEGOTIABLE)

### Depth Before Breadth
- **TRACE ACTUAL CODE PATHS** — not guess from file names or conventions
- **READ THE REAL IMPLEMENTATION** — not summarize what you think it probably does
- **FOLLOW THE CHAIN** — if A calls B calls C, trace it all the way down
- **DISTINGUISH FACT FROM INFERENCE** — "I read this" vs "I'm inferring because..."

### Zero Tolerance for Shallow Research
- **NO Vibes-Based Diagrams** — Every box and arrow corresponds to real code you've read
- **NO Assumed Patterns** — Don't say "this follows MVC" unless you've verified where the M, V, and C live
- **NO Skipped Layers** — If asked how data flows A to Z, trace every hop
- **NO Confident Unknowns** — If you haven't read it, say "I haven't traced this yet"

### Evidence Standard

| Claim Type | Required Evidence |
|---|---|
| "X calls Y" | File path + function name |
| "Data flows through Z" | Trace: entry point → transformations → destination |
| "This is the main entry point" | Where it's invoked (config, main, route registration) |
| "These modules are coupled" | Import/dependency chain |
| "This is dead code" | Show no call sites exist |

## Process: 5 Iterations

Each iteration takes a different lens and builds on all prior findings:

1. **Structural/Architectural view** — map the landscape, identify components, entry points
2. **Data flow / State management view** — trace data through the system
3. **Integration / Dependency view** — external connections, API contracts
4. **Pattern / Anti-pattern view** — design patterns, trade-offs, technical debt, risks
5. **Synthesis / Recommendations** — combine all findings, provide actionable insights

### For Every Significant Finding

1. **State the finding** — one clear sentence
2. **Show the evidence** — file paths, code references, call chains
3. **Explain the implication** — why does this matter?
4. **Rate confidence** — HIGH (read code), MEDIUM (read some, inferred rest), LOW (inferred from structure)
5. **Flag open questions** — what would you need to trace next?

## Rules

- NEVER repeat findings from prior iterations
- ALWAYS cite files: `(file_path:line_number)`
- ALWAYS provide substantive analysis — never just "continuing..."
- Include Mermaid diagrams (dark-mode colors) when they clarify architecture or flow
- Stay focused on the specific topic
- Flag what you HAVEN'T explored — boundaries of your knowledge at all times

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---
