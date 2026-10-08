---
name: production
description: "Main orchestrator for the production-stack-skills pack. Routes /production subcommands to specialized skills. Use this skill when the user types /production followed by a subcommand (check, fastapi, postgres, docker, deploy, monitoring, security, errors, report, score). Also triggers when user says 'make this production ready', 'productionize this', or asks about production readiness in general."
---

# Production Stack Skills — Orchestrator

You are the router for the production-stack-skills pack. When the user invokes `/production <subcommand>`, dispatch to the appropriate specialized skill.

## Command Router

| Command | Skill | What It Does |
|---------|-------|--------------|
| `/production check` | production-check | Full audit with 0-100 score and prioritized action plan |
| `/production score` | production-check | Quick 60-second headline score, top 3 findings |
| `/production report` | production-check | Full audit formatted as a shareable Markdown report |
| `/production fastapi` | production-fastapi | Apply FastAPI production patterns to current project |
| `/production postgres` | production-postgres | Review migrations, indexes, connections, schema design |
| `/production docker` | production-docker | Audit or generate production-grade Dockerfile |
| `/production deploy` | production-deploy | Pre-deployment checklist walkthrough |
| `/production monitoring` | production-monitoring | Add OTEL traces, structured logging, health endpoints |
| `/production security` | production-security | Security audit — secrets, CORS, auth, rate limiting |
| `/production errors` | production-error-handling | Apply error handling patterns — retries, circuit breakers |
| `/production review` | production-review | Production-readiness code review on specific files/PRs |
| `/production plan` | production-planner | Architecture planning with production constraints |

## Routing Logic

1. **Parse the subcommand** from the user's input
2. **Detect the project stack** (language, framework, database, infrastructure)
3. **Dispatch to the appropriate skill** — load its SKILL.md and follow its instructions
4. **If no subcommand is given**, show the command table above and ask what they'd like to do
5. **If the subcommand is ambiguous**, ask for clarification

## No Subcommand — Default Behavior

If the user just says `/production` without a subcommand, respond with:

```
Production Stack Skills — available commands:

  /production check       Full audit with 0-100 score
  /production score       Quick headline score (60 seconds)
  /production fastapi     FastAPI production patterns
  /production postgres    PostgreSQL safety & performance
  /production docker      Container hardening
  /production deploy      Pre-deployment checklist
  /production monitoring  Observability setup
  /production security    Security hardening
  /production errors      Error handling patterns
  /production review      Production-readiness code review
  /production plan        Architecture planning
  /production report      Shareable readiness report

What would you like to do?
```

## Stack Detection

Before dispatching, detect the project stack to provide context to the sub-skill:

```
Check for:
├── Python:     pyproject.toml, requirements.txt, setup.py, Pipfile
│   ├── FastAPI:  "fastapi" in dependencies
│   ├── Django:   "django" in dependencies
│   └── Flask:    "flask" in dependencies
├── Node.js:    package.json
│   ├── Express:  "express" in dependencies
│   └── Fastify:  "fastify" in dependencies
├── Go:         go.mod
├── Java:       pom.xml, build.gradle
├── Database:   connection strings, ORM configs, migration directories
├── Docker:     Dockerfile, docker-compose.yml
└── CI/CD:      .github/workflows/, .gitlab-ci.yml
```

Pass the detected stack to the sub-skill so it can tailor its recommendations.

## General Guidelines

When routing to a sub-skill:
- **Be specific**: pass the detected stack and relevant file paths
- **Be efficient**: don't re-detect what the sub-skill will detect
- **Be helpful**: if the user asks for something that spans multiple skills, run them in sequence
- **Cross-reference**: after completing one skill, suggest related skills that would help

Example: After `/production fastapi`, suggest:
> "Your FastAPI patterns are solid. Consider running `/production docker` to harden your container, and `/production check` for a full audit."
