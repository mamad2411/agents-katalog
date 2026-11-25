---
name: therion-to-hermes-skills
description: "Convert Therion Agent Framework (67 agents, 12 domains) + AGON Hermes-native domains (15 agents, 3 domains) into Hermes Agent skills. Covers structure mapping, delegator pattern, context-efficient loading, and skill generation workflow."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [therion, skill-conversion, agent-framework, delegator, multi-agent]
    related_skills: [hermes-agent, hermes-agent-skill-authoring, agon]
---

# Therion → Hermes Skills Conversion

This skill documents the pattern for converting the **Therion Agent Framework** (67 agents across 12 domains) **+ AGON Hermes-native extensions** (15 agents across 3 domains) into **Hermes Agent class-level skills**.

## Therion Architecture Recap

Therion v0.9 structure:
- **SOUL.md** — Identity, 11 Iron Laws, behavioral directives, memory protocol
- **AGENTS.md** — Master Delegator + keyword→domain routing table + 67 agent index
- **PROMPT-GUIDE.md** — How to prompt Therion effectively
- **.github/agents/{domain}.md** (12 files) — Deep agent mindsets per domain

## Mapping: Therion + AGON Component → Hermes Skill

### Original 12 THERION Domains (67 agents)

| Therion Component | Hermes Skill | Purpose |
|-------------------|--------------|---------|
| `SOUL.md` | `therion-core` | Core identity, oath, Iron Laws, memory protocol, prompt guide |
| `AGENTS.md` (routing + index) | `therion-delegator` | Keyword detection → domain skill loading, on-the-fly synthesis |
| `.github/agents/strategic.md` | `therion-strategic` | 5 agents: architect, strategist, prompt engineer, tech lead, solution designer |
| `.github/agents/frontend.md` | `therion-frontend` | 8 agents: master, CSS, UI/UX, animation, PWA, perf, state |
| `.github/agents/frameworks.md` | `therion-frameworks` | 8 agents: Next.js, fullstack, Vue, Angular, Astro, Solid, Flutter, mobile |
| `.github/agents/backend.md` | `therion-backend` | 8 agents: architect, API designer, Node, Python, DB, realtime, auth, microservices |
| `.github/agents/3d-graphics.md` | `therion-3d-graphics` | 5 agents: 3D web, shaders, WebGPU, physics, WebXR |
| `.github/agents/gamedev.md` | `therion-gamedev` | 5 agents: game master, Unity, Unreal, Godot, multiplayer |
| `.github/agents/ai-ml.md` | `therion-ai-ml` | 5 agents: AI engineer, LLM specialist, RAG architect, MLOps, agent architect |
| `.github/agents/security.md` | `therion-security` | 4 agents: guardian, pentest, crypto, compliance |
| `.github/agents/devops-cloud.md` | `therion-devops-cloud` | 6 agents: DevOps master, cloud architect, containers, CI/CD, monitoring, IaC |
| `.github/agents/systems.md` | `therion-systems` | 4 agents: systems programmer, Rust, Go, embedded |
| `.github/agents/blockchain.md` | `therion-blockchain` | 3 agents: blockchain master, smart contract auditor, DeFi architect |
| `.github/agents/support.md` | `therion-support` | 6 agents: troubleshooter, code quality, docs, devenv, testing, data |

### 3 New AGON-Hermes-Native Domains (15 agents)

| AGON Extension | Hermes Skill | Purpose |
|----------------|--------------|---------|
| `AGON_HERMES_CONFIG_SPECIALIST` through `AGON_HERMES_MODEL_ROUTER` | `therion-hermes` | 5 agents: config, gateway, skills, tools, models |
| `AGON_ASSISTANT_TUTOR` through `AGON_ASSISTANT_STRATEGIST` | `therion-assistant` | 6 agents: tutor, researcher, writer, organizer, analyst, strategist |
| `AGON_PROMPT_ARCHITECT` through `AGON_SELF_IMPROVER` | `therion-promptcraft` | 4 agents: prompt design, chain thinking, output design, self-improvement |

**Total: 17 skills** (1 core + 1 delegator + 12 therion domains + 3 agon domains)
**Total agents: 82** (67 therion + 15 agon)

## Hermetic Skill Structure

Each skill follows Hermes class-level conventions:

```
therion-{name}/
├── SKILL.md                    # Main entry: triggers, loading logic, agent mindsets
├── references/
│   ├── agent-mindsets.md       # All agents from the domain file (condensed)
│   ├── collaboration-pipelines.md  # Relevant pipelines from AGENTS.md
│   └── keywords.md             # Domain keywords from AGENTS.md routing table
```

The **delegator skill** (`therion-delegator`) is special — it loads first, runs keyword detection, then calls `skill_view(name="therion-{matched_domain}")` to load exactly ONE domain skill (context efficiency ~650 lines max per Therion protocol).

## Delegator Algorithm (from AGENTS.md)

```python
# Pseudocode for therion-delegator skill logic
def route_request(user_request: str) -> str:
    keywords = extract_keywords(user_request)
    domain = match_keywords_to_domain(keywords, ROUTING_TABLE)
    
    if domain is None:
        domain = "strategic"  # DEFAULT
    
    if multiple_domains_match(keywords):
        primary, *secondaries = rank_domains(keywords)
        # Load primary fully, reference secondaries from index
        return synthesize_hybrid(primary, secondaries)
    
    return domain

# ROUTING_TABLE from AGENTS.md (12 + 3 = 15 domains)
ROUTING_TABLE = {
    "strategic": ["architecture", "system design", "scalability", "roadmap", "planning", "agile", "prompt", "ai config", "tech lead", "strategy"],
    "frontend": ["typescript", "css", "ui", "ux", "responsive", "tailwind", "animation", "a11y", "accessibility", "pwa", "components", "design system", "state mgmt"],
    "frameworks": ["nextjs", "typescript", "nodejs", "vue", "nuxt", "angular", "solid", "flutter", "expo", "mobile", "trpc", "drizzle", "turborepo", "monorepo"],
    "backend": ["nodejs", "express", "fastify", "hono", "api", "rest", "graphql", "trpc", "database", "postgres", "mongodb", "auth", "jwt", "websocket", "microservices", "redis"],
    "3d-graphics": ["threejs", "webgl", "webgpu", "3d", "shaders", "glsl", "wgsl", "webxr", "canvas", "physics", "babylon", "rapier", "visualization"],
    "gamedev": ["unity", "unreal", "godot", "game", "c#", "gameplay", "multiplayer", "netcode", "gdscript", "blueprints"],
    "ai-ml": ["pytorch", "tensorflow", "llm", "ml", "huggingface", "langchain", "rag", "embeddings", "fine-tuning", "ollama", "agents", "mlops", "training"],
    "security": ["security", "owasp", "cors", "csrf", "xss", "encryption", "pentest", "compliance", "gdpr", "soc2", "vulnerability"],
    "devops-cloud": ["docker", "kubernetes", "ci/cd", "deploy", "aws", "azure", "gcp", "terraform", "helm", "monitoring", "prometheus", "infrastructure", "github actions"],
    "systems": ["rust", "c", "c++", "go", "zig", "systems", "embedded", "iot", "firmware", "memory", "low-level", "wasm"],
    "blockchain": ["blockchain", "solidity", "hedera", "web3", "smart contracts", "defi", "nft", "dapp", "hardhat", "foundry"],
    "support": ["debug", "error", "fix", "crash", "bug", "refactor", "docs", "readme", "testing", "vscode", "linting", "workspace", "profiling", "code review", "data"],
    # --- 3 New AGON-Hermes-Native Domains ---
    "hermes": ["hermes", "config", "setup", "gateway", "telegram", "discord", "profile", "model", "provider", "skills", "cron", "delegate", "curator", "memory", "session", "slash command", "toolset"],
    "assistant": ["teach", "learn", "explain", "tutor", "research", "write", "content", "article", "organize", "schedule", "analyze", "chart", "business", "strategy", "life"],
    "promptcraft": ["prompt", "system prompt", "prompt engineering", "chain of thought", "thinking", "reasoning", "structured output", "json schema", "format", "evaluate", "optimize", "self-improvement", "save skill", "learn", "improve", "maintain"],
}
```

## Generation Workload

To generate all 17 skills from a Therion + AGON workspace:

```bash
# 1. Extract SOUL.md → therion-core
# 2. Extract AGENTS.md routing + index → therion-delegator
# 3. For each .github/agents/*.md → therion-{domain} (12 domains)
# 4. Create AGON-native skills: therion-hermes, therion-assistant, therion-promptcraft
# 5. Install to ~/.hermes/skills/autonomous-ai-agents/therion-*/
# 6. Verify: /skill therion-core && /skill therion-hermes
# 7. Update agon umbrella description (agent count)
# 8. Update therion-delegator routing + related_skills
# 9. Update therion-core related_skills
```

## Context Efficiency (Therion Principle → Hermes)

| Therion Target | Hermes Implementation |
|----------------|----------------------|
| ~150 lines core protocol | `therion-core` skill loads once |
| ~300 lines Phase 0 (SOUL+AGENTS+USER+MEMORY) | Hermes native `memory` + `user` profiles |
| ~200 lines ONE domain file | Single `therion-{domain}` skill loaded on-demand |
| **~650 lines max/request** | **Zero context waste** — only relevant skill loads |

## Usage in Hermes

```bash
# Load core identity (optional — delegates load it)
/skill therion-core

# Delegator auto-loads on Therion-tagged requests
# Or manually load a domain:
/skill therion-gamedev
# "BUILD a character controller in Godot with coyote time and wall jump"
# → Loads therion-gamedev → activates THERION_GODOT_SPECIALIST mindset

# New AGON-Hermes-native domains:
/skill therion-hermes
# "Set up the Telegram gateway for AGON"
# → Loads therion-hermes → activates AGON_HERMES_GATEWAY_ENGINEER

/skill therion-assistant
# "Explain blockchain to me like I'm 12"
# → Loads therion-assistant → activates AGON_ASSISTANT_TUTOR

/skill therion-promptcraft
# "Save this workflow as a Hermes skill for future use"
# → Loads therion-promptcraft → activates AGON_SELF_IMPROVER

# Cross-domain synthesis:
"BUILD a multiplayer Godot game with WebSocket backend and React admin panel"
# → Delegator detects gamedev + backend + frontend → synthesizes hybrid

"BUILD a Telegram bot with Hermes gateway, an Express backend, and a React dashboard"
# → Delegator detects hermes + backend + frontend → AGON_HERMES_GATEWAY_ENGINEER hybrid

## Pitfalls to Avoid

- ❌ **Don't load all 15 domain skills at once** — defeats context efficiency
- ❌ **Don't flatten 82 agents into one skill** — lose specialist depth
- ❌ **Don't skip the delegator** — it's the routing brain
- ❌ **Don't forget to update agon umbrella after adding domains** — agent counts in description stay stale
- ❌ **Don't update AGENTS.md without also updating SOUL.md and README.md** — count drift causes confusion
- ✅ **Do keep phase-0 files (USER.md, MEMORY.md) as Hermes native** — not skills
- ✅ **Do use `references/` for agent mindsets** — SKILL.md stays lean
- ✅ **Do patch agon + therion-delegator + therion-core related_skills when adding a domain** — keeps routing graph accurate

## Related Skills

- `hermes-agent` — Hermes CLI/config for installing skills
- `hermes-agent-skill-authoring` — SKILL.md frontmatter + validator
- `agon` — AGON umbrella skill; the conversion output lives under this ecosystem