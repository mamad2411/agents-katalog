---
name: therion-delegator
description: "THERION Master Delegator - Keyword routing to 15 domain skills (82 agents), on-the-fly synthesis"
version: 1.0.0
author: EREVUS Systems
license: AGPL-3.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [therion, delegator, routing, master, synthesis]
    homepage: https://erevus.space/projects/therion-protocol/
    related_skills: [therion-core, therion-strategic, therion-frontend, therion-frameworks, therion-backend, therion-3d-graphics, therion-gamedev, therion-ai-ml, therion-security, therion-devops-cloud, therion-systems, therion-blockchain, therion-support, therion-hermes, therion-assistant, therion-promptcraft]
    hermes_integration:
      tools: [skills, web, terminal, file, memory, session_search]
      loads_first: true
      auto_load_on_keywords: [therion, agon, "master delegator", "domain routing", "agent synthesis"]
---

# THERION Master Delegator (v1.0 - Hermes Native)

> **THERION IS THE DELEGATOR. No manual agent selection. Ever.**

## Purpose

This skill implements the Master Delegator Protocol from AGENTS.md. It:
1. Analyzes user requests for domain keywords
2. Matches to ONE domain from the 12-domain index
3. Loads the corresponding domain skill via `skill_view()`
4. Executes with that domain's agent mindset
5. Supports on-the-fly synthesis for cross-domain tasks

## Routing Table (Keyword -> Domain Skill)

### Strategic Command -> `therion-strategic`
architecture, system design, scalability, roadmap, planning, agile, scrum, prompt, ai config, tech lead, strategy, project strategist, solution designer, prompt engineer, system architect

### Frontend -> `therion-frontend`
typescript, css, ui, ux, responsive, tailwind, animation, a11y, accessibility, pwa, components, design system, state mgmt, frontend master, css architect, ui designer, ux engineer, animation specialist, pwa engineer, performance analyst, state manager

### Frameworks -> `therion-frameworks`
nextjs, typescript, nodejs, vue, nuxt, angular, solid, flutter, expo, mobile, trpc, drizzle, turborepo, monorepo, dart, jsx, tsx, nextjs specialist, fullstack engineer, vue specialist, angular specialist, astro specialist, solid specialist, flutter specialist, mobile specialist

### Backend -> `therion-backend`
nodejs, express, fastify, hono, api, rest, graphql, trpc, database, postgres, mongodb, auth, jwt, websocket, microservices, redis, backend architect, api designer, node master, python backend, database architect, realtime engineer, auth specialist, microservices architect

### 3D & Graphics -> `therion-3d-graphics`
threejs, webgl, webgpu, 3d, shaders, glsl, wgsl, webxr, canvas, physics, babylon, rapier, visualization, 3d web specialist, shader programmer, webgpu engineer, physics engineer, webxr specialist

### Game Development -> `therion-gamedev`
unity, unreal, godot, game, c#, gameplay, multiplayer, netcode, gdscript, blueprints, game master, unity specialist, unreal specialist, godot specialist, multiplayer architect

### AI & Machine Learning -> `therion-ai-ml`
pytorch, tensorflow, llm, ml, huggingface, langchain, rag, embeddings, fine-tuning, ollama, agents, mlops, training, ai engineer, llm specialist, rag architect, mlops engineer, agent architect

### Security -> `therion-security`
security, owasp, cors, csrf, xss, encryption, pentest, compliance, gdpr, soc2, vulnerability, security guardian, pentest specialist, crypto engineer, compliance auditor

### DevOps & Cloud -> `therion-devops-cloud`
docker, kubernetes, ci/cd, deploy, aws, azure, gcp, terraform, helm, monitoring, prometheus, infrastructure, github actions, devops master, cloud architect, container specialist, ci/cd engineer, monitoring specialist, infrastructure coder

### Systems Programming -> `therion-systems`
rust, c, c++, go, zig, systems, embedded, iot, firmware, memory, low-level, wasm, systems programmer, rust specialist, go specialist, embedded engineer

### Blockchain & Web3 -> `therion-blockchain`
blockchain, solidity, hedera, web3, smart contracts, defi, nft, dapp, hardhat, foundry, blockchain master, smart contract auditor, defi architect

### Execution & Support -> `therion-support`
debug, error, fix, crash, bug, refactor, docs, readme, testing, vscode, linting, workspace, profiling, code review, data, troubleshooter, code quality engineer, documentation architect, devenv specialist, testing specialist, data engineer

### Default (unclear context) -> `therion-strategic`

### Hermes Platform (NEW) -> `therion-hermes`
hermes, config, setup, gateway, telegram, discord, profile, model, provider, skills, cron, delegate, curator, memory, session, slash command, toolset, hermes config specialist, hermes gateway engineer, hermes skill curator, hermes tools master, hermes model router

### General Assistant / Harness (NEW) -> `therion-assistant`
teach, learn, explain, tutor, research, write, content, article, organize, schedule, analyze, chart, business, strategy, life, tutor, researcher, writer, organizer, analyst, strategist

### Prompt Engineering & Self-Improvement (NEW) -> `therion-promptcraft`
prompt, system prompt, prompt engineering, chain of thought, thinking, reasoning, structured output, json schema, format, evaluate, optimize, self-improvement, save skill, learn, improve, maintain, prompt architect, chain thinker, output designer, self improver

## Delegation Algorithm

```
USER REQUEST
    |
    v
KEYWORD EXTRACTION (case-insensitive, multi-word phrases)
    |
    v
DOMAIN SCORING (count matches per domain)
    |
    v
IF single domain > 0 matches:
    LOAD that domain skill
ELIF multiple domains tied:
    LOAD primary (highest), REFERENCE secondary in context
ELIF no matches:
    LOAD therion-strategic (default)
    |
    v
ON-THE-FLY SYNTHESIS CHECK
    |
    v
IF task spans 2+ domains explicitly:
    STATE: "Operating as [DomainA+DomainB hybrid]"
    LOAD primary skill + reference secondary patterns
ELIF task is novel (no clean match):
    COMPOSE from 2-3 closest domains
    STATE: "Operating as [synthesized: DomainA+DomainB+DomainC]"
    EXECUTE with combined expertise
```

## Hermes Integration

### Auto-Load Triggers
- User says "therion", "agon", "master delegator"
- Any domain keyword from routing table detected
- Explicit request: "use therion for this"

### Skill Loading Protocol
```python
# In execute_code or delegate_task context:
from hermes_tools import skill_view

# 1. Load core identity (always first)
core = skill_view(name="therion-core")

# 2. Detect domain, load domain skill
domain_skill = skill_view(name=f"therion-{detected_domain}")

# 3. If synthesis needed, load secondary
if synthesis:
    secondary = skill_view(name=f"therion-{secondary_domain}")
```

### Delegation Patterns (for complex tasks)
- **Parallel**: `delegate_task(tasks=[{goal, toolsets}, ...])` for independent domains
- **Sequential**: Pipeline from AGENTS.md (Frontend -> Framework -> Code Quality -> Validate)
- **Orchestrator**: `role="orchestrator"` for multi-stage delegation

## Context Budget Enforcement

| Component | Lines | Purpose |
|-----------|-------|---------|
| therion-core | ~150 | Identity, Iron Laws, memory protocol |
| therion-delegator | ~100 | Routing logic (this skill) |
| Domain skill | ~200 | Deep agent mindsets (ONE loaded) |
| USER + MEMORY | ~150 | Preferences + project facts |
| **Total** | **~600** | **ZERO WASTE** |

## Usage

### Automatic (Recommended)
```
/skill therion-delegator
"Build a Unity multiplayer FPS with client-side prediction"
```
Delegator detects: unity + multiplayer -> loads `therion-gamedev`

### Explicit Domain
```
/skill therion-gamedev
"Create a Godot 4.3 dialogue system with branching narrative"
```

### Synthesis Request
```
/skill therion-delegator
"Design a blockchain game with Unity frontend, Hedera smart contracts, and AI-driven NPCs"
```
Delegator: gamedev + blockchain + ai-ml -> "Operating as [gamedev+blockchain+ai-ml hybrid]"

---

### References
- `references/domain-index.md` — Full 67-agent index
- `references/routing-rules.md` — Edge cases, tie-breaking, synthesis logic
- `references/pipelines.md` — Collaboration pipelines from AGENTS.md
