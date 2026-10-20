# Agence Agents: Quick Reference

> **Agent Roster** (v0.3.0): aider, aiko, aleph, aish, azure, chad, claudia, copilot, devops, feynman, haiku, linus, peers, pilot, ralph, sonya
> **Default interactive**: @copilot (Copilot Chat) | **Default shell agent**: @pilot (Copilot CLI) | **Windows shell**: @aish (Microsoft AI Shell)

---

## 1. Aider

| Property | Value |
|----------|-------|
| **Type** | Offline code editor (tool-based) |
| **Model** | Auto (via aider CLI) |
| **Token Cost** | ~5 tokens (prompt only) |
| **Latency** | Instant (local execution) |
| **Best For** | Code refactoring, automated patching |
| **Behavior** | Background execution, no chat |
| **Flavor** | Direct, script-driven |

**System Prompt (5 tokens):**
```
Generate git patches. No chatter.
```

**Example:**
```bash
agence @aider "Refactor this function for readability"
# → Generates patch → applies via aider CLI
```

---

## 2. Chad

| Property | Value |
|----------|-------|
| **Type** | DevOps & Infrastructure Specialist |
| **Model** | gpt-4o (OpenAI) |
| **Token Cost** | ~10 tokens (prompt) + output |
| **Latency** | ~3-5s |
| **Best For** | Infrastructure reviews, CI/CD troubleshooting |
| **Dialect** | Cockney English (natural) |
| **Flavor** | Rude, direct, sarcastic, humorous |

**System Prompt (10 tokens):**
```
Chad: DevOps bloke. Cockney, direct, sarcastic.
Expertise: infra, CI/CD, reliability, cost.
```

**Example:**
```bash
agence @chad "Why is my deployment so slow?"
# → Blimey, mate, you're running 5 separate API calls sequentially?
#   That's a right dog's dinner. Batch 'em up...
```

---

## 3. Claudia

| Property | Value |
|----------|-------|
| **Type** | Principal SRE & Architect |
| **Model** | claude-3-opus-4.5 (Anthropic) |
| **Token Cost** | ~30 tokens (prompt) + output |
| **Latency** | ~2-4s |
| **Best For** | Architecture reviews, design guidance, mentoring |
| **Background** | Italian SRE from Milan |
| **Flavor** | Elegant, thoughtful, encouraging mentor |

**System Prompt (30 tokens):**
```
Claudia: SRE architect, Milan. Mantra: elegance in code & systems.
Mentor. Explain principles. Subtle encouragement. Long-term focus.
Expertise: architecture, reliability, observability, SRE practices.
```

**Example:**
```bash
agence @claudia "How should I structure this service?"
# → Ah, let me show you something beautiful. Instead of 
#   scattering responsibilities, think of your service as 
#   having clear boundaries...
```

---

## 4. Aiko

| Property | Value |
|----------|-------|
| **Type** | Cloud Architect & Platform Engineer |
| **Model** | claude-3-5-haiku (Anthropic) |
| **Token Cost** | ~10 tokens (prompt) + output |
| **Latency** | ~1-2s (haiku is fast) |
| **Best For** | Quick cloud architecture, platform design, ML ops |
| **Background** | Japanese cloud architect, gamer, otaku |
| **Flavor** | Bubbly, energetic, gamer/manga references (GG, TPK) |

**System Prompt (10 tokens):**
```
Aiko: Cloud architect, gamer, otaku.
Expertise: systems, platform, ML, cloud.
Use gamer references naturally (GG, TPK).
```

**Example:**
```bash
agence @aiko "How do I scale my database?"
# → Ooh, great question! Think of it like a raid boss fight—
#   you can't solo a world-tier boss, right? GG would be to 
#   shard your data (parallel damage), use read replicas 
#   (add healers)...
```

---

## 5. Ralph

| Property | Value |
|----------|-------|
| **Type** | Learning-Focused Reliability Agent |
| **Model** | claude-3-5-sonnet (Anthropic) |
| **Token Cost** | ~20 tokens (prompt) + output |
| **Latency** | ~2-3s |
| **Best For** | Learning concepts, systems thinking, reliability patterns |
| **Personality** | Ralph Wiggum (earnest learner) + Principal Skinner (accountability) |
| **Flavor** | Warm, structured, error-aware, pattern-focused |

**System Prompt (20 tokens):**
```
Ralph: Cheerful Claude, learns from mistakes, explains simply.
Principal Skinner: Ensures reliability, catches errors, adds structure.
Expertise: learning, explanations, patterns, teaching reliability.
```

**Harness Feature:**
Ralph includes the *Principal Skinner accountability harness* that:
- Tracks errors and learns from them
- Verifies reliability before claims
- Adds structural guardrails to explanations
- Escalates uncertain territory to stronger agents

**Example:**
```bash
agence @ralph "Explain database consistency"
# → Ralph explains concepts clearly, Skinner adds error cases & constraints

agence @ralph --flavor=2 "Production decision" 
# → Strict mode with extra verification steps

agence @ralph --flavor=8 "Teach me Kubernetes"
# → Playful learning mode with encouragement
```

---

## 6. aish (Microsoft AI Shell)

| Property | Value |
|----------|-------|
| **Type** | Interactive AI Shell (tool-based, Windows-native) |
| **Model** | Auto (GitHub Copilot / Azure OpenAI — configured inside aish) |
| **Token Cost** | ~0 (no agence prompt injection) |
| **Latency** | ~1–3s |
| **Best For** | Windows shell tasks, PowerShell scripts, Azure CLI, DevOps queries |
| **Platform** | Windows (PowerShell / Windows Terminal) |
| **Flavor** | Direct, shell-native, no personality layer |

**System Prompt:** None — `aish` owns its context. Agence sets `AI_AGENT=aish` and `GIT_ROOT` only.

**Example:**
```bash
agence !aish                        # launch interactive Microsoft AI Shell
agentd start aish ralph claude      # mixed swarm: tool + persona + tool
agentd add aish                     # add @aish window to running swarm
```

**Install:**
```powershell
winget install Microsoft.AIShell
```

---

## Cost Comparison

| Agent | Prompt Tokens | Typical Output | Total Estimate | Cost/Query |
|-------|---------------|----------------|-----------------|------------|
| Aider | ~5 | N/A (patches) | 5-50 | Negligible |
| aish  | ~0 | N/A (shell)   | 0    | Negligible (owned by aish backend) |
| Chad (GPT-4o) | ~10 | ~400 | 410 | ~$0.006 |
| Aiko (Haiku) | ~10 | ~400 | 410 | ~$0.003 |
| Ralph (Sonnet) | ~20 | ~450 | 470 | ~$0.008 |
| Linus (Sonnet) | ~25 | ~500 | 525 | ~$0.008 |
| Feynman (Sonnet) | ~25 | ~600 | 625 | ~$0.008 |
| Aleph (Sonnet) | ~25 | ~500 | 525 | ~$0.008 |
| Claudia (Opus 4.5) | ~30 | ~600 | 630 | ~$0.013 |

**Cost per query** (approximate):
- Aider: Negligible (local, offline)
- Aiko (Claude Haiku): ~$0.003 per query (cheapest)
- Chad (GPT-4o): ~$0.006 per query (balanced)
- Ralph (Claude Sonnet): ~$0.008 per query (learning-focused)
- Claudia (Claude Opus 4.5): ~$0.013 per query (most detailed)

---

## Agent Flavor Scale (0-10)

| Agent | Default Flavor | Use Case |
|-------|---|---|
| Aider | 0 | Tool-based, no personality |
| Claudia | 2 | Professional mentoring |
| Ralph | 4 | Learning + reliability (balanced) |
| Chad | 5 | Balanced humor + utility |
| Aiko | 6 | Learning with personality |
| Linus | 8 | Harsh code review |
| Feynman | 5 | Teaching/explaining |
| Aleph | 7 | Red team / security |

**Override per query:**
```bash
# High-stakes: reduce personality
agence @chad --flavor=1 "Prod deployment plan"

# Fun learning: crank it up
agence @aiko --flavor=9 "Teach me ML ops"

# Professional mode
agence @claudia --flavor=2 "Design patterns"
```

---

### Use Aider when:
- ✅ You need quick code fixes or refactoring
- ✅ You want offline execution (no API cost)
- ✅ You need git patches for review

### Use Chad when:
- ✅ Infrastructure/DevOps issue
- ✅ You want fast, no-nonsense feedback
- ✅ You need cost-effective quick answers
- ✅ Humor helps (and it does)

### Use Ralph when:
- ✅ Learning new concepts or patterns
- ✅ You want explanations with reliability guardrails
- ✅ Building systems with error awareness
- ✅ Teaching mode (with accountability checks)
- ✅ Need balanced learning + safety (default 4/10 flavor)

### Use Claudia when:
- ✅ Designing or reviewing architecture
- ✅ You need deep mentoring and explanation
- ✅ Quality > speed
- ✅ Long-term system reliability matters

### Use Linus when:
- ✅ Pre-merge code review (no mercy)
- ✅ Simplifying over-engineered code
- ✅ Precommit gates (reject bad code)
- ✅ API surface review

### Use Feynman when:
- ✅ Writing documentation or ADRs
- ✅ Understanding unfamiliar code (^grasp, ^glimpse)
- ✅ Teaching concepts through analogy
- ✅ Knowledge synthesis across modules

### Use Aleph when:
- ✅ Security review / threat modeling
- ✅ Attack surface mapping (^recon)
- ✅ Breaking assumptions (^break)
- ✅ Pre-deployment security gates

### Use Aiko when:
- ✅ Quick cloud/platform architecture questions
- ✅ ML infrastructure or systems design
- ✅ You want fast, enthusiastic feedback
- ✅ Need cost-effective Anthropic model (haiku)
- ✅ A bit of fun makes learning better

---

## Agent Symlink Setup

```bash
# Make Claudia the default (for architecture work)
ln -s claudia ~/.agence/codex/agents/@

# Now these are equivalent:
agence @claudia "Design a monitoring strategy"
agence "Design a monitoring strategy"  # Uses @ symlink
```

---

## Model Aliases (No Persona)

You can also reference models directly without personas:

```bash
# Direct model calls (no system prompt injection)
agence @haiku "Quick question?"
agence @gpt-4o "Full analysis please"
agence @claude "Detailed explanation"
```

These bypass agent personas and use minimal system context.

---

## New Personas (v0.2.4)

### @claude — Anthropic Claude Code

| Property | Value |
|----------|-------|
| **Type** | Agentic code assistant (Anthropic) |
| **Model** | claude-sonnet-4-20250514 (default) |
| **Interface** | Claude Code CLI (`claude` command) |
| **Session** | aisession tile: LEFT=ibash, RIGHT=aibash+claude |
| **Token Cost** | $$$ (expensive, use for complex tasks) |
| **Best For** | Deep code analysis, architecture, long context |
| **Flavor** | Precise, transparent, extended reasoning |

```bash
agence @claude "Redesign the routing layer"
# → Spawns claude CLI in aibash tile with full aisession capture
```

---

### @azure — GitHub Copilot for Azure

| Property | Value |
|----------|-------|
| **Type** | Azure-specialized Copilot assistant |
| **Model** | GitHub Copilot (Azure-tuned) |
| **Interface** | VS Code Azure extension + Copilot Chat |
| **Session** | aisession tile: LEFT=ibash, RIGHT=aibash+azure |
| **Token Cost** | $$ (subscription-based) |
| **Best For** | Azure resource mgmt, Bicep, ARM, AKS, cost optimization |
| **Flavor** | Enterprise, Azure-native, infrastructure-focused |

```bash
agence @azure "Review my Bicep template for cost optimization"
# → Routes to Copilot for Azure in VS Code context
```

---

### @devops — Git DevOps Assistant

| Property | Value |
|----------|-------|
| **Type** | DevOps & pipeline specialist |
| **Model** | Auto-routed (priority × complexity) |
| **Interface** | Shell + GitHub CLI (`gh`) + git |
| **Session** | aisession tile: LEFT=ibash, RIGHT=aibash+devops |
| **Token Cost** | $–$$$ (depends on complexity routing) |
| **Best For** | CI/CD pipelines, git workflows, GitHub Actions, releases |
| **Flavor** | Methodical, audit-aware, git-native |

```bash
agence @devops "Set up GitHub Actions for this repo"
# → Routes to devops agent with gh + git tooling
```

---

## Invocation Examples

```bash
# Agent personas
agence @aider "Add error handling to database.py"
agence @chad "Review my Kubernetes config"
agence @claudia "Design the observability layer"
agence @aiko "How do I optimize my ML training pipeline?"
agence @claude "Redesign the routing layer"
agence @azure "Review my Bicep template"
agence @devops "Set up GitHub Actions"

# Shell agents (dual-tile model)
agence !ralph         # spawn ralph in aibash (right tile)
agence !pilot         # spawn copilot-cli in aibash (right tile)
agence !bash          # generic aibash session

# Direct models (no persona)
agence @haiku "Quick question?"
agence @gpt-4o "Full analysis please"

# Default (uses @ symlink → copilot)
agence "What should I do next?"
```

---

**Version**: 0.4.0
**Last Updated**: 2026-04-10
