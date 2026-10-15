---
name: agent-onboard
description: 'Agent-optimized developer onboarding. Given a codebase, produces a compact onboarding reference: quick start, stack, key commands, key files, env vars, architecture digest. Target under 80 lines. Use when user says "onboard me", "onboarding", "how to set up", "getting started", "quick start".'
requires-devkits: auto-detect
---

# Agent Onboard -- Compact Developer Onboarding

Produces a developer onboarding reference optimized for scanning. Target: under 80 lines. Quick start must be under 5 commands.

---

## Workflow

### Step 1: Scan Sources

Read in order:
1. `docs/agent-docs/CONTEXT.md` (if exists) -- skip to generation, this has everything
2. `README.md` -- project name, purpose, quick start
3. `docker-compose.yml` -- services, ports, dependencies
4. `.env.example` -- required environment variables
5. `package.json` -- scripts section for common commands
6. `docs/agent-docs/STACK.md` (if exists) -- dependency versions

### Step 2: Generate Onboarding

Output exactly this template:

```
# Onboarding: [Project Name]

> Quick start time: [estimated minutes]

## Quick Start
```bash
git clone [url] && cd [dir]
cp .env.example .env
docker compose up
```
Open: [URLs]

## Stack
| Layer | Tech |
|-------|------|
| [layer] | [name + version] |

## Key Commands
| Task | Command |

## Key Files
| File | Purpose |

## Env Vars
| Variable | Required | Default/Example |

## Architecture (1-min digest)
```
[Text dependency graph: A → B → C]
```

### Top 3 Modules
| Module | Purpose |

### Top 3 Routes
| Route | Purpose |
```

---

## Format Rules

1. **Quick start must be under 5 commands.** If it requires more, simplify or note that setup needs improvement.
2. **Port table embedded in Quick Start URLs.** `http://localhost:5173 (client)` directly under the commands.
3. **Key commands table** extracts from `package.json` scripts: `dev`, `build`, `test`, `lint`, `typecheck`, `db:generate`, `db:migrate`, `db:seed`.
4. **Key files table** limit to 10 entries. Only the files a developer edits daily.
5. **Architecture digest** uses text graph + module/route tables. No paragraphs.
6. **Target under 80 lines** including code blocks. If exceeding, trim non-essential rows.

---

## What NOT to do

- No architecture theory. No "this project follows Clean Architecture which means..."
- No personalized sections ("You're a backend dev, focus on...").
- No team contact info unless found in existing docs.
- No external service setup (Stripe, SendGrid) unless in `.env.example`.
- No testing strategy explanation. Commands only.
- No CI/CD pipeline explanation. Commands only.
- No "Resources" section with links to external docs.
- No project structure tree if `docs/agent-docs/CONTEXT.md` exists. Reference it instead.
