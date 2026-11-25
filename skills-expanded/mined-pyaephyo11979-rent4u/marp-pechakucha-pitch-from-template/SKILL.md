---
name: marp-pechakucha-pitch-from-template
description: Generate a 6-slide Marp PechaKucha pitch deck from a template by auditing the full project codebase for features, stack, tools, and audience
source: auto-skill
extracted_at: '2026-06-24T11:58:38.055Z'
---

## Generating a PechaKucha Pitch Deck from a Project Template

### When to use
When you need to create a short pitch presentation (Marp markdown slides) that summarizes a project's purpose, audience, features, and tech — typically from an existing template with fixed slide titles.

### Approach

#### 1. Read the template
Read the template file (e.g., `slides/template.md`) to understand:
- Marp frontmatter settings (`paginate`, `transition`, `auto-advance`)
- Number of slides and their titles/prompts
- Any required sections (e.g., "MCP", "Skill", "Agent" bullet points)

#### 2. Audit the project systematically
Explore these sources to build a feature inventory:

| Source | What to extract |
|--------|----------------|
| `README.md` | Tech stack, data model, API endpoints, project purpose |
| `AGENT.md` / product spec | Target audience, user story, problem statement, definition of done |
| `prisma/schema.prisma` (or DB schema) | Data models — these map to features |
| `backend/src/modules/` or `controllers/` | Backend feature areas (auth, house, payment, user, role) |
| `backend/src/middlewares/` | Security/infra features (JWT auth, RBAC, rate limiting, encryption) |
| `frontend/src/pages/` | User-facing screens (Home, Search, Dashboard, Login, Register, HouseDetail) |
| `frontend/src/components/` | UI capabilities (forms, layout, reusable UI kit) |
| `.claude/.mcp.json` or MCP config | MCP servers used (for "How I built it" slide) |
| `.qwen/skills/` or `.claude/skills/` | Skills used (for "How I built it" slide) |

#### 3. Map features to slide structure

For a typical 6-slide PechaKucha pitch:

1. **Who's my person?** — Extract from AGENT.md user story. Identify 2-3 distinct user personas (e.g., travelers, homeowners).
2. **Their problem** — Extract pain points from the "Why" or "Story" section of the spec. Be specific and concrete.
3. **What I built** — List 4-6 major features using emoji bullets. Derive from backend modules + frontend pages. Group by capability, not by file.
4. **How I built it** — Fill in MCP (from `.mcp.json`), Skill (from skills directories), Agent (mention which AI agents assisted). Add the tech stack summary.
5. **Why it matters** — Connect features back to the problems from slide 2. Each pain point should have a corresponding solution.
6. **Done checklist** — Match items from the template. Mark completed items with `[x]`.

#### 4. Write the output file
- Preserve exact Marp frontmatter from the template
- Use `---` separators between slides
- Keep HTML comments for slide numbers
- Keep content concise — each slide has only ~20 seconds

### Key gotchas
- Don't just list technical components — frame everything from the user's perspective
- The "How I built it" slide specifically expects MCP, Skill, and Agent — grep for these in project config files rather than guessing
- Keep each slide to 4-6 bullet points max for readability at presentation speed
- The done checklist items come from the template, not from the AGENT.md definition of done
