---
name: "readme-patterns"
description: "README patterns and templates: the 5-second test, the README pyramid, badge selection, install and copy-paste quick start sections, section order by project type, section content guidelines, tables of contents, visual elements, and anti-patterns. Use when writing or reviewing a README."
---

# README Patterns

## The 5-Second Test

A developer landing on a README has 5 seconds before they decide to stay or leave. The test:
- Close the README
- Ask: "What does this project do?"
- If you cannot answer in one sentence, the README failed

The one-liner must complete this template: "[Name] is a [category] that [value proposition]."

```markdown
# Bad: feature list as description
A comprehensive toolkit with logging, caching, retry logic, and more.

# Good: one-liner that passes the 5-second test
Retry is a TypeScript library that wraps any async function with
configurable exponential backoff and jitter.
```

## The README Pyramid

Readers scan in layers. Structure content for multiple attention spans:

```
Layer 1: One-liner + badges         (2 seconds)  - Every visitor reads this
Layer 2: Install + Quick Start      (30 seconds) - Evaluating visitors read this
Layer 3: Features + API overview    (2 minutes)  - Interested visitors read this
Layer 4: Full API reference + docs  (10+ min)    - Committed users read this
```

Rules:
- Layers 1-2 must fit on one screen without scrolling
- Never put caveats or warnings before the quick start
- Do not require account creation before showing code

## Badge Selection

### Always Include
```markdown
<!-- CI/CD status - shows the project is actively maintained -->
[![CI](https://github.com/{owner}/{repo}/actions/workflows/ci.yml/badge.svg)](...)

<!-- Version - shows the project is actively released -->
[![npm version](https://img.shields.io/npm/v/{package})](...)

<!-- License - required for legal clarity -->
[![License](https://img.shields.io/github/license/{owner}/{repo})](./LICENSE)
```

### Include If You Have It
```markdown
<!-- Coverage - only add if you actually maintain coverage -->
[![Coverage](https://codecov.io/gh/{owner}/{repo}/branch/main/graph/badge.svg)](...)

<!-- Downloads - social proof when number is meaningful (>100/week) -->
[![npm downloads](https://img.shields.io/npm/dm/{package})](...)
```

### Never Add
- "PRs welcome" (every repo welcomes PRs)
- "Awesome" list badges (self-congratulatory)
- Counter badges that never update
- Badges for tools you do not actually use

## Install Section Pattern

Cover every supported package manager. Users do not switch tools because of a missing one-liner.

```markdown
## Install

```bash
npm install {package-name}
```

```bash
yarn add {package-name}
```

```bash
pnpm add {package-name}
```
```

For non-npm packages, match the ecosystem:
- Python: `pip install`, `uv add`, `poetry add`
- Rust: `cargo add`
- Go: `go get`

## Quick Start: The Copy-Paste Test

Every quick start code block must pass the copy-paste test: paste into a clean project with documented prerequisites and it must work.

```markdown
# Bad: missing imports, unexplained prerequisites
const client = new Client({ token });
const result = await client.search({ query: 'test' });

# Good: complete, runnable example
import { SearchClient } from '@example/search';

const client = new SearchClient({
  token: process.env.SEARCH_TOKEN,
});

const results = await client.search({
  query: 'hello world',
  limit: 10,
});

console.log(results.hits); // [{ id: '1', title: '...', score: 0.9 }]
```

Quick start checklist:
- [ ] Has imports/requires at the top
- [ ] Shows where configuration comes from (env var, not magic constant)
- [ ] Shows what the output looks like (comment with example output)
- [ ] Is under 20 lines
- [ ] Works with only the documented prerequisites

## Project Type Patterns

### Library/SDK README Order
1. Name + one-liner
2. Badges (CI, version, license)
3. Install (all package managers)
4. Quick Start (working example < 20 lines)
5. API (key exports, main class)
6. Configuration (if complex)
7. Contributing
8. License

### CLI Tool README Order
1. Name + one-liner
2. Badges
3. Install (npm -g, brew, direct download)
4. Usage (`tool --help` output or common commands)
5. Examples (real-world command invocations)
6. All flags/options (table)
7. Configuration file format (if applicable)
8. Contributing / License

### Service/API README Order
1. Name + one-liner
2. Architecture diagram (Mermaid or image)
3. Prerequisites (Docker, env vars, ports)
4. Running locally (copy-paste commands)
5. API endpoints overview
6. Environment variables table
7. Deployment
8. Contributing / License

## Anti-Patterns

### The Elevator Pitch README
```
# Bad: marketing copy instead of technical description
Welcome to AwesomeTool, the revolutionary solution that transforms
the way development teams collaborate...

# Good: direct technical description
AwesomeTool is a CLI that syncs local file changes to a remote
Docker container without restarting the container.
```

### The Dependency Wall
```
# Bad: prerequisites buried after installation
npm install my-tool

# Then later in the document...
Note: Requires Node.js 18+, Redis 7+, and PostgreSQL 14+.

# Good: prerequisites before install
## Prerequisites
- Node.js 18+
- Redis 7+ (for session storage)
- PostgreSQL 14+ (for data persistence)

## Install
npm install my-tool
```

### The Stale Screenshot
Only include screenshots if you commit to updating them. A screenshot showing old UI erodes trust faster than no screenshot at all. If you include screenshots, add a comment in the PR template: "Did UI change? Update README screenshot."

### The Promise Without Proof
If you claim the library is "blazing fast" or "zero-dependency," prove it:
```markdown
# Bad
Extremely fast JSON parsing library.

# Good
Parses JSON 2-4x faster than JSON.parse for objects > 10KB.
[Benchmarks](./benchmarks)
```

## Table of Contents

Only add a Table of Contents if the README exceeds four screen-lengths (approximately 1500 words). When added:

```markdown
## Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [API](#api)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
```

Use `#lowercase-with-hyphens` anchor links. GitHub auto-generates anchors from headings.

## References
- [Standard README Specification (RichardLitt)](https://github.com/RichardLitt/standard-readme)
- [Shields.io Badge API](https://shields.io/)
- [GitHub: About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

## Templates by project type

> Structural patterns and content frameworks for different project types.

### Knowledge Base

#### The README Pyramid

Every README serves multiple audiences simultaneously. Structure content as a pyramid:

```
         [Title + One-liner]          <-- 2 seconds: "What is this?"
        [Badges + Visual]             <-- 5 seconds: "Is it healthy?"
       [Install + Quick Start]        <-- 30 seconds: "Can I use it?"
      [Features / API Overview]       <-- 2 minutes: "What can it do?"
     [Detailed Docs + Examples]       <-- 10 minutes: "How exactly?"
    [Contributing + License]          <-- When invested
```

#### Section Content Guidelines

**Title**: Project name. No "Welcome to" or "About". Just the name.

**Description**: One sentence. Format: "{Name} is a {category} that {value proposition}."
- Good: "Zod is a TypeScript-first schema validation library with static type inference."
- Bad: "Welcome to Zod! This project aims to provide validation utilities for TypeScript developers."

**Install**: Show every supported package manager. Most common first.
```markdown
## Install

npm:
\`\`\`bash
npm install project-name
\`\`\`

Yarn:
\`\`\`bash
yarn add project-name
\`\`\`

pnpm:
\`\`\`bash
pnpm add project-name
\`\`\`
```

**Quick Start**: The minimum code to see the project work. Under 15 lines. Must be copy-pasteable.

**API Reference**: For libraries. Table format for simple APIs, linked subpages for complex ones.

**Configuration**: Show the config file format with comments explaining each option. Show defaults.

#### Expandable Sections for Long Content

```markdown
<details>
<summary>Advanced Configuration</summary>

Content that most readers don't need goes here.
It stays out of the way but is accessible.

</details>
```

#### Table of Contents

Include a TOC for READMEs longer than 4 screenfuls:

```markdown
## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [API](#api)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
```

#### Visual Elements

**Screenshots**: Use for GUIs, dashboards, CLI output. Place after description, before install.

```markdown
<p align="center">
  <img src="./docs/screenshot.png" alt="Dashboard showing analytics" width="600">
</p>
```

**Architecture Diagrams**: Use for complex systems. Mermaid works in GitHub:

````markdown
```mermaid
graph LR
    A[Client] --> B[API Gateway]
    B --> C[Auth Service]
    B --> D[Core Service]
    D --> E[(Database)]
```
````

**Demo GIFs**: Use for CLI tools and interactive features. Keep under 5 seconds, under 5MB.

### Patterns

1. **One-Liner Test**: If you can't describe the project in one sentence, the project scope is unclear.
2. **Copy-Paste Test**: Every code example should work when pasted into a fresh project with only the documented prerequisites.
3. **5-Second Test**: A developer should know what the project does within 5 seconds of landing on the README.
4. **Heading Scan Test**: Reading only the headings should tell the story: what, install, use, configure, contribute.
5. **Link Everything**: Every mention of an external tool, service, or concept should link to its documentation.
6. **Version Pinning**: Show version-specific install commands when relevant: `npm install project@^3.0.0`.

### Anti-Patterns

1. **Wall of Text**: No paragraphs longer than 4 lines. Use lists, tables, and code blocks.
2. **Logo Without Substance**: A giant logo with minimal documentation. Content first, branding second.
3. **Stale Badges**: Badges showing failing CI or outdated versions. Remove badges you cannot maintain.
4. **TOC-Only README**: A README that is just a table of contents linking to a docs/ folder. The README must stand alone.
5. **"Under Construction"**: If it is not ready, don't publish it. If it is published, document what exists.
6. **Assumed Knowledge**: "Just run `make`" without explaining prerequisites. Always list dependencies.
7. **Screenshot Overload**: More than 3 screenshots in sequence. Use a gallery link or docs page.

### References

- [Make a README](https://www.makeareadme.com/)
- [Awesome README](https://github.com/matiassingers/awesome-readme)
- [Standard Readme](https://github.com/RichardLitt/standard-readme)
- [GitHub Flavored Markdown Spec](https://github.github.com/gfm/)
- [Shields.io](https://shields.io/)
