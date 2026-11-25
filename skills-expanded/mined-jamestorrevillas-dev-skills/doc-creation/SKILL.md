---
name: doc-creation
description: Use this skill when creating technical documentation, architecture docs, runbooks, READMEs, API references, changelogs, or any structured technical writing. Trigger on keywords: documentation, docs, README, runbook, architecture doc, technical writing, write a guide, document this, API reference, changelog, how-to guide.
---

# Technical Documentation

## Documentation Philosophy

**Write for the reader who is in a hurry and under stress.**

Good documentation answers the question before the reader finishes asking it. Every doc should have a clear audience and a clear job to do.

---

## Documentation Types & When to Use Each

| Type | Purpose | When to Write |
|---|---|---|
| README | Project overview + quickstart | Every project, day 1 |
| Architecture Doc | How the system is designed and why | Before building complex systems |
| Runbook | Step-by-step operational procedures | For anything ops needs to do repeatedly |
| API Reference | Endpoint contracts | When exposing an API to others |
| ADR | Why a significant decision was made | After every major technical decision |
| Changelog | What changed between versions | Every release |
| How-To Guide | Task-oriented instructions | When users need to do a specific thing |

---

## README Template

```markdown
# [Project Name]

One-sentence description of what this does and why it exists.

## Prerequisites
- [Dependency 1] v[X.X]
- [Dependency 2]

## Getting Started
\`\`\`bash
# Clone and install
git clone [repo]
cd [project]
npm install

# Configure
cp .env.example .env
# Edit .env with your values

# Run
npm run dev
\`\`\`

## Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| DATABASE_URL | Yes | PostgreSQL connection string |
| JWT_SECRET | Yes | Secret for JWT signing |

## Architecture
[Brief overview or link to architecture doc]

## Testing
\`\`\`bash
npm test              # Unit tests
npm run test:e2e      # End-to-end tests
\`\`\`

## Deployment
[How to deploy or link to runbook]

## Contributing
[How to contribute or link to guide]
```

---

## Architecture Document Structure

```markdown
# Architecture: [System/Feature Name]

## Overview
[2-3 sentences: what this does and why it exists]

## Goals & Non-Goals
**Goals:** [what this system is designed to achieve]
**Non-Goals:** [what it explicitly does NOT cover]

## Architecture Diagram
[ASCII diagram or Mermaid diagram]

## Components
### [Component 1]
- **Responsibility:** [what it does]
- **Interface:** [how others interact with it]
- **Dependencies:** [what it needs]

## Data Flow
[How data moves through the system for key use cases]

## Key Decisions
[Link to ADRs or inline rationale for major choices]

## Known Limitations
[Honest description of current constraints]
```

---

## Runbook Template

```markdown
# Runbook: [Operation Name]

**When to use:** [Trigger condition]
**Time required:** ~[X minutes]
**Who can run this:** [Role/permission needed]

## Prerequisites
- [ ] Access to [system]
- [ ] [Tool] installed

## Steps
1. [First action — be specific, include exact commands]
   \`\`\`bash
   [exact command]
   \`\`\`
   Expected output: [what success looks like]

2. [Next step]

## Verification
[How to confirm the operation succeeded]

## Rollback
[If something goes wrong, how to undo]

## Escalation
If stuck after [X minutes]: contact [person/team]
```

---

## Writing Style Guidelines

- **Active voice** — "The system sends a notification" not "A notification is sent"
- **Present tense** — "The function returns..." not "The function will return..."
- **Specific** — "Run `npm install`" not "Install dependencies"
- **Short sentences** — one idea per sentence
- **Examples** — show, don't just tell
- **Maintain it** — outdated docs are worse than no docs. Update docs in the same PR as code changes.

---

## AI-Optimized Documentation (for RAG systems)

Write docs to be machine-readable as well as human-readable:
- Consistent terminology throughout
- Each section is self-contained (can be read without other sections)
- Include explicit labels: "Purpose:", "When to use:", "Example:"
- Modular structure — individual chunks make sense in isolation
