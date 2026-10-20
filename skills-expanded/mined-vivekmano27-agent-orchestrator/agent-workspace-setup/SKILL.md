---
name: agent-workspace-setup
description: Generate CLAUDE.md, settings.json, hooks, subagents, commands, and MCP config. Auto-detects tech stack from project files. Use when setting up or managing the development workspace and tooling.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Agent Workspace Setup Skill

Set up project workspaces for agent-orchestrated microservices development.

## When to Use
- Initializing a new monorepo for microservices development
- Adding CLAUDE.md or agent configuration to an existing project
- Generating .env.example, .gitignore, settings.json, or hooks.json
- Auto-detecting tech stack from manifest files

## Monorepo Directory Generation

```bash
mkdir -p services/{api-gateway/src/{common,config,modules},core-service/src/{modules,common,database},core-service/prisma,ai-service/app/{api,services,models,tasks,integrations},ai-service/tests,shared/{proto,schemas}}
mkdir -p apps/{web/src/{app,components,lib,hooks,types},mobile-flutter/lib/{features,core,app},mobile-flutter/test,mobile-kmp/{shared,androidApp,iosApp}}
mkdir -p infrastructure/{docker,terraform,k8s,scripts} docs .github/workflows
```

## Tech Stack Auto-Detection

Detect the stack by reading manifest files in each service directory:

```bash
[ -f services/core-service/package.json ] && grep -q "@nestjs/core" services/core-service/package.json && echo "NestJS"
[ -f services/ai-service/requirements.txt ] && grep -q "django" services/ai-service/requirements.txt && echo "Django"
[ -f apps/web/package.json ] && grep -q "next" apps/web/package.json && echo "Next.js"
[ -f apps/mobile-flutter/pubspec.yaml ] && echo "Flutter"
[ -f apps/mobile-kmp/shared/build.gradle.kts ] && echo "KMP"
```

## CLAUDE.md Template

Generate from detected stack. Must include: Project Overview, Tech Stack, Build & Run commands per service, Test Commands, Lint & Format commands, and Rules (violations are bugs). See the root CLAUDE.md for the canonical format.

## settings.json Generation

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)", "Bash(npx *)", "Bash(pytest *)",
      "Bash(docker-compose *)", "Bash(flutter *)",
      "Bash(git status)", "Bash(git diff *)", "Bash(git log *)",
      "Read", "Write", "Edit", "Grep", "Glob"
    ],
    "deny": ["Bash(rm -rf /*)"]
  }
}
```

## hooks.json Generation

```json
{
  "hooks": [
    { "event": "PreCommit", "command": "npm run lint && npm run format:check", "workingDirectory": "services/core-service" },
    { "event": "PreCommit", "command": "ruff check . && ruff format --check .", "workingDirectory": "services/ai-service" }
  ]
}
```

## .env.example and .gitignore

```bash
# .env.example — include all service configs with safe placeholders
API_GATEWAY_PORT=3000
CORE_SERVICE_PORT=3001
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/core_db
REDIS_URL=redis://localhost:6379
AI_SERVICE_PORT=8000
DJANGO_SECRET_KEY=change-me
ANTHROPIC_API_KEY=
```

```gitignore
node_modules/
dist/
.env
.env.local
*.pyc
__pycache__/
.venv/
.dart_tool/
build/
.next/
coverage/
.idea/
```

## Git Init

```bash
git init
git add -A
git commit -m "chore: initial project scaffold

- Monorepo structure with services and apps
- CLAUDE.md with project conventions
- Docker Compose for local development
- Environment configuration templates"
```

## Anti-Patterns
- **Never hardcode secrets** in CLAUDE.md or .env.example
- **Never skip .gitignore** -- sensitive files leak without it
- **Never generate partial structures** -- include all services from the architecture
- **Never assume a stack** without checking manifest files first

## Checklist
- [ ] All service/app directories created with correct subdirectories
- [ ] CLAUDE.md generated with accurate build, test, and lint commands
- [ ] settings.json and hooks.json created
- [ ] .env.example includes all services with safe defaults
- [ ] .gitignore covers node_modules, .env, __pycache__, build artifacts
- [ ] Tech stack auto-detected from manifest files
- [ ] Git initialized with a conventional initial commit
