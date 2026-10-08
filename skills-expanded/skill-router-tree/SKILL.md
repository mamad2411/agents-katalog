# Skill-Router Tree
> **ID**: skill-router-tree
> **Layer**: SKILL ROUTING (PON37)
> **Priority**: HIGH — Route 8789 skills through ~50 router nodes (not flat injection)
> **Token Cost**: 0 (local routing)

## Problem
8,789 skills flat-injected = context window explodes. Even with lazy loading, name+description of 8789 skills = ~170K tokens. Context window = 200K. No room for actual conversation.

## Solution: Hierarchical Router Tree

### Structure
```
ROOT.md (1 file, ~200 tokens)
├── CATEGORY_ROUTERS/
│   ├── web-dev-router.md (~500 tokens, 120 skills)
│   ├── devops-router.md (~500 tokens, 155 skills)
│   ├── ai-ml-router.md (~500 tokens, 150 skills)
│   ├── security-router.md (~500 tokens, 180 skills)
│   ├── blockchain-router.md (~500 tokens, 131 skills)
│   ├── database-router.md (~500 tokens, 107 skills)
│   ├── mobile-router.md (~500 tokens, 111 skills)
│   ├── cloud-router.md (~500 tokens, 116 skills)
│   ├── game-dev-router.md (~500 tokens, 69 skills)
│   ├── creative-router.md (~500 tokens, 39 skills)
│   ├── productivity-router.md (~500 tokens, 27 skills)
│   ├── reference-router.md (~500 tokens, 216+ files)
│   ├── mcp-router.md (~500 tokens, 4312 files)
│   ├── token-opt-router.md (~500 tokens, 17 skills)
│   ├── resource-router.md (~500 tokens, 6 skills)
│   └── ... (50 total routers)
```

### Routing Rules

#### R1: ROOT-FIRST
```
→ Session start: inject ROOT.md only (~200 tokens)
→ ROOT contains: category names + trigger keywords
→ User says "docker compose" → ROOT routes to devops-router
→ devops-router has: skill names + descriptions for 155 devops skills
→ Only THAT router loads (~500 tokens), not 8789 skills
→ Router matches "docker compose" → loads specific skill
```

#### R2: PROGRESSIVE DEPTH
```
Level 0: ROOT (~200t) — always in context
Level 1: Category router (~500t) — loaded on match
Level 2: Skill name+description (~190t each) — loaded from router
Level 3: Skill full body (varies) — loaded only on invocation
→ Max tokens for skill discovery: 200 + 500 + 190 = 890 tokens
→ Compare: flat 8789 × 190 = 1,670,000 tokens (IMPOSSIBLE)
```

#### R3: MULTI-CATEGORY ROUTING
```
→ User asks "deploy Rust app to Kubernetes"
→ ROOT matches: "Rust" → backend-router, "Kubernetes" → devops-router
→ Load BOTH routers: 500 + 500 = 1000 tokens
→ Each router picks best skill → 2 skills loaded
→ Total: 200 + 1000 + 2×skill = efficient
```

#### R4: CACHE ROUTER DECISIONS
```
→ If user stays in same category (e.g., multiple Docker questions):
→ Router stays loaded, don't re-read ROOT
→ Only load new skill if different trigger
→ Purge router after 5 turns of no match
```

### Router File Format
```markdown
# {Category} Router
> Triggers: docker, k8s, terraform, ansible, ci-cd, helm, ...
> Skills: 155

## Skill Index
- docker-expert: Docker containerization, compose, build, debug
- k8s-master: Kubernetes deployment, RBAC, operators, Helm
- terraform-pro: IaC, state management, modules, providers
- ...
```

## Auto-Generation
```python
# Auto-generate router files from catalog
import os, re
CAT = os.path.expanduser('~/.agents/skills-catalog')
# Categorize by filename prefix
categories = {
    'web-dev': ['frontend', 'backend', 'css', 'js', 'html', 'react', 'vue'],
    'devops': ['devops', 'docker', 'k8s', 'terraform', 'ansible', 'helm', 'ci-'],
    'ai-ml': ['ai-', 'ml-', 'llm', 'gpt', 'neural', 'transformer'],
    'security': ['security', 'cve', 'vuln', 'pentest', 'crypto'],
    'blockchain': ['blockchain', 'web3', 'solidity', 'eth', 'solana', 'defi'],
    'database': ['sql', 'postgres', 'mysql', 'mongo', 'redis', 'database'],
    'mobile': ['ios', 'android', 'flutter', 'react-native', 'mobile'],
    'cloud': ['aws', 'gcp', 'azure', 'cloud', 'lambda', 's3'],
    'game': ['game', 'unity', 'unreal', 'godot', 'bevy'],
    # ... 50 categories
}
# Generate one router .md per category
```

## Config
```yaml
skill_router_tree:
  enabled: true
  root_file: skill-root-router.md
  router_count: 50
  max_routers_loaded: 3
  router_purge_after_turns: 5
  progressive_depth: true
  max_discovery_tokens: 1000
```
