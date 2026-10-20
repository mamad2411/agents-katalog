---
applyTo: "**/*.md"
---

# Markdown Conventions

## Structure

- Use ATX headers (`#`, `##`, `###`)
- One blank line between sections
- Use tables for structured data
- Use fenced code blocks with language identifiers

## Artifact Naming

| Step | Prefix | Example |
|------|--------|---------|
| Requirements | `01-` | `01-requirements.md` |
| Architecture | `02-` | `02-architecture-assessment.md` |
| Design | `03-` | `03-design-diagram.drawio` |
| Governance | `04-gov-` | `04-governance-constraints.md` |
| Planning | `04-` | `04-implementation-plan.md` |
| Deployment | `06-` | `06-deployment-summary.md` |
| As-Built | `07-` | `07-technical-design-document.md` |

## No Hardcoded Counts

Never hardcode entity counts (agents, skills, tools, MCP servers) in prose.
Use descriptive language instead. Reference `count-manifest.json` when exact numbers are needed.
