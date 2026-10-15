---
name: external-skills-catalog
description: Curated catalog of 60+ external Claude Code skills across 8 categories with quality rankings, install instructions, and fallback strategies
---

# External Skills Catalog

Curated directory of community and official Claude Code skills. Use this when the user needs a capability that vibecosystem doesn't cover natively, or when recommending external tools.

## When to Use

- User asks for a skill/capability that doesn't exist in vibecosystem
- User wants to discover what else is available for Claude Code
- Recommending complementary skills for a specific workflow
- Fallback when internal skills can't fully handle a request

## Quality Ranking

Skills are ranked by reliability and maintenance:

| Tier | Label | Criteria |
|------|-------|----------|
| 1 | Official | Made by Anthropic or verified partners |
| 2 | Well-starred | 50+ GitHub stars, active maintenance, good docs |
| 3 | Community | Open source, functional, may lack polish |

Always prefer higher-tier skills. Mention tier when recommending.

## Catalog by Category

### Document & Content
| Skill | Source | Description | Tier |
|-------|--------|-------------|------|
| PDF extraction | Various MCP servers | Parse, extract, summarize PDF content | 2 |
| Markdown linting | markdownlint | Enforce consistent markdown style | 2 |
| Technical writing | Community | Style guides, API docs, changelogs | 3 |
| Content generation | Community | Blog posts, social media, copywriting | 3 |

### Development & Code
| Skill | Source | Description | Tier |
|-------|--------|-------------|------|
| GitHub integration | Official MCP | Issues, PRs, code search, reviews | 1 |
| Linear integration | Community MCP | Issue tracking, sprint management | 2 |
| Sentry integration | Community MCP | Error tracking, issue resolution | 2 |
| Database clients | Various MCP | PostgreSQL, MySQL, SQLite direct access | 2 |
| Docker management | Community | Container lifecycle, compose orchestration | 3 |
| Regex builder | Community | Visual regex construction and testing | 3 |

### Security & Compliance
| Skill | Source | Description | Tier |
|-------|--------|-------------|------|
| Secret scanning | Community | Detect leaked credentials in repos | 2 |
| Dependency audit | npm audit / snyk | CVE scanning, vulnerability assessment | 2 |
| SBOM generation | Community | Software bill of materials | 3 |
| License checker | Community | Dependency license compliance | 3 |

### Data & Analytics
| Skill | Source | Description | Tier |
|-------|--------|-------------|------|
| BigQuery client | Community MCP | Query, analyze, visualize data | 2 |
| Jupyter integration | Community | Notebook creation and execution | 3 |
| CSV/Excel processing | Community | Data transformation, analysis | 3 |
| Chart generation | Community | Data visualization, dashboards | 3 |

### Marketing & Growth
| Skill | Source | Description | Tier |
|-------|--------|-------------|------|
| SEO analysis | Community | Site audit, keyword research | 3 |
| Social media | Community | Post scheduling, analytics | 3 |
| Email templates | Community | Marketing emails, newsletters | 3 |
| A/B test design | Community | Experiment design, analysis | 3 |

### Creative & Design
| Skill | Source | Description | Tier |
|-------|--------|-------------|------|
| Figma integration | Community MCP | Design token extraction, component mapping | 2 |
| Image generation | Various APIs | AI image creation via MCP | 2 |
| SVG manipulation | Community | Icon creation, optimization | 3 |
| Color palette | Community | Color scheme generation, contrast checking | 3 |

### Project Management
| Skill | Source | Description | Tier |
|-------|--------|-------------|------|
| Notion integration | Official MCP | Pages, databases, project tracking | 1 |
| Slack integration | Official MCP | Messaging, channel management | 1 |
| Jira integration | Community MCP | Issue tracking, sprint boards | 2 |
| Calendar management | Community MCP | Scheduling, reminders | 3 |

### Platform & Infrastructure
| Skill | Source | Description | Tier |
|-------|--------|-------------|------|
| Cloudflare | Community MCP | Workers, DNS, CDN management | 2 |
| Vercel | Community MCP | Deployment, serverless functions | 2 |
| Supabase | Community MCP | Database, auth, storage | 2 |
| AWS CDK | Community | Infrastructure as code patterns | 3 |

## Install Instructions

### Claude Code (CLI)
```bash
# MCP-based skills: add to ~/.claude/mcp.json or project .mcp.json
{
  "mcpServers": {
    "skill-name": {
      "command": "npx",
      "args": ["-y", "@package/mcp-server"]
    }
  }
}

# Prompt-based skills: add to ~/.claude/commands/ or project .claude/commands/
mkdir -p .claude/commands
echo "skill content here" > .claude/commands/skill-name.md
```

### Claude.ai (Web)
MCP skills can be added via Settings > Integrations > MCP Servers.

## Fallback Strategy

When the needed skill doesn't exist:

```
Step 1: WORKAROUND
  → Can an existing vibecosystem skill handle it partially?
  → Example: No "email" skill? Use copywriter agent + manual send

Step 2: COMBO
  → Can 2+ existing skills combine to solve it?
  → Example: No "API mock" skill? Use mocksmith + backend-dev

Step 3: CREATE
  → Is it worth creating a new internal skill?
  → Use /skill-create to generate from session patterns

Step 4: EXTERNAL
  → Search this catalog for a community skill
  → Check: https://github.com/topics/claude-code
  → Check: https://github.com/topics/mcp-server
  → Web search: "claude code [capability] skill 2026"
```

## Discovering New Skills

The external ecosystem grows fast. When this catalog doesn't have what you need:

1. Search GitHub: `claude code skill [keyword]` or `mcp server [keyword]`
2. Check MCP server directories for new integrations
3. Look at Claude Code community discussions
4. Consider building and contributing your own

## Tips

- Always verify external skills before recommending (check repo activity, stars, last commit)
- Prefer MCP-based skills for deeper integration
- Prompt-based skills are easier to install but less powerful
- When recommending, include the install command so the user can act immediately
- If a skill has known issues, mention them upfront
