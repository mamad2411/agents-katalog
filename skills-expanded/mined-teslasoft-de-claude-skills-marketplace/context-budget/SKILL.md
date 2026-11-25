---
name: context-budget
version: 1.0.0
last_updated: 2026-06-05
description: Manage context efficiently in long conversations using progressive disclosure and tiered loading. Use when hitting context limits, working on large codebases, or optimizing token usage across multi-turn interactions.
triggers:
  - /context-budget
  - manage context
  - context too long
  - hitting context limit
  - optimize token usage
  - too much context
---

# Context Budget Management

Strategies for managing limited context windows efficiently using progressive disclosure and tiered loading.

## When to Use

- Conversation approaching context limits
- Working with large codebases or documentation
- Multi-turn interactions with accumulating context
- Need to balance breadth vs. depth of information
- Optimizing API costs (tokens = money)

## When NOT to Use

- Short, single-turn interactions
- When full context fits comfortably
- Simple Q&A without state accumulation

---

## Quick Start

1. **Assess** current context usage and remaining budget
2. **Tier** information by relevance (core → domain → task → optional)
3. **Summarize** or evict low-priority context
4. **Load** new information only when needed
5. **Monitor** and rebalance as conversation evolves

---

## Core Principle: Progressive Disclosure

**Load information only when needed, in order of relevance.**

```
┌─────────────────────────────────────────────────────────┐
│  ALWAYS LOADED (~500 tokens)                            │
│  • Core identity/constraints                            │
│  • Critical safety rules                                │
│  • Navigation hints to deeper content                   │
└─────────────────────────────────────────────────────────┘
         ↓ Load on demand
┌─────────────────────────────────────────────────────────┐
│  DOMAIN CONTEXT (~2K tokens)                            │
│  • Project-specific rules                               │
│  • Architecture patterns                                │
│  • Key file locations                                   │
└─────────────────────────────────────────────────────────┘
         ↓ Load when task requires
┌─────────────────────────────────────────────────────────┐
│  TASK CONTEXT (~4K tokens)                              │
│  • Specific file contents                               │
│  • API documentation                                    │
│  • Implementation details                               │
└─────────────────────────────────────────────────────────┘
         ↓ Load only for deep work
┌─────────────────────────────────────────────────────────┐
│  FULL CONTEXT (remaining budget)                        │
│  • Complete files                                       │
│  • Full conversation history                            │
│  • Extensive examples                                   │
└─────────────────────────────────────────────────────────┘
```

---

## Context Tiers

### Tier 1: Core (~500 tokens)
**Always present, never evicted.**

- System identity and constraints
- Critical safety/security rules
- Pointers to deeper content
- Session state (current task, branch, etc.)

### Tier 2: Domain (~2K tokens)
**Loaded when entering a domain, evicted when leaving.**

- Project CLAUDE.md / README
- Architecture decisions
- Naming conventions
- Key abstractions and patterns

### Tier 3: Task (~4K tokens)
**Loaded for specific tasks, evicted when task changes.**

- Relevant file contents
- API signatures and docs
- Related test files
- Error messages and stack traces

### Tier 4: Full (remaining)
**Loaded only when deep work requires it.**

- Complete file contents
- Extensive conversation history
- Large documentation sets
- Full codebase context (via repomix bundles)

---

## Strategies

### 1. Observation Masking

Remove low-value observations from context while preserving key information.

**When to use**: Repeated similar operations (file listings, search results)

**How**:
- Keep only unique/relevant results
- Summarize patterns instead of listing all
- Drop intermediate states, keep final

```
BEFORE (high token cost):
- Listed 50 files in src/
- Listed 30 files in tests/
- Listed 20 files in docs/

AFTER (low token cost):
- Project structure: src/ (50 files), tests/ (30), docs/ (20)
- Key patterns: components in src/components/, tests mirror src/
```

### 2. LLM Summarization

Use summarization to compress context while preserving meaning.

**When to use**: Long conversation history, large documents

**How**:
- Summarize completed discussion threads
- Extract key decisions and action items
- Compress verbose outputs to essentials

```
BEFORE: 2000 tokens of debugging discussion
AFTER: "Resolved: Auth timeout caused by missing JWT refresh. Fixed in auth.ts:45."
```

### 3. Lazy Loading

Don't load information until it's needed.

**When to use**: Large reference materials, optional context

**How**:
- Load file contents only when editing
- Fetch documentation only when implementing
- Defer examples until ambiguity arises

### 4. Tiered Eviction

Evict lower-priority context when budget is tight.

**Eviction order** (first to evict → last):
1. Intermediate outputs (superseded by final)
2. Exploration artifacts (search results, file listings)
3. Completed task context
4. Domain context (when switching domains)
5. Core context (never evict)

### 5. Context Checkpointing

Save and restore context states for multi-branch work.

**When to use**: Working on multiple features, context switching

**How**:
- Summarize current state before switching
- Store summaries in persistent notes (git branches, files)
- Restore with targeted loading when resuming

---

## Budget Estimation

### Token Approximations

| Content Type | Tokens/Unit |
|-------------|-------------|
| English text | ~0.75 tokens/word |
| Code | ~0.5 tokens/character |
| JSON/YAML | ~1 token/4 characters |
| Markdown | ~0.8 tokens/word |

### Model Context Limits (approximate)

| Model | Context | Practical Budget |
|-------|---------|------------------|
| Claude Sonnet | 200K | ~150K usable |
| Claude Opus | 200K | ~150K usable |
| GPT-4 | 128K | ~100K usable |
| GPT-4o | 128K | ~100K usable |

**Practical budget** = Total - system prompt - response buffer

---

## Procedure

### Step 1: Assess Current State

Check context usage:
- How many turns in conversation?
- How much file content loaded?
- What's the current task focus?

**Checkpoint**: Identify if approaching limits.

### Step 2: Classify Loaded Information

Sort into tiers:
- What's core (always needed)?
- What's domain (project-specific)?
- What's task (current work)?
- What's optional (can be evicted)?

### Step 3: Apply Strategies

Choose appropriate strategy:
- **Near limit?** → Evict lowest tier, summarize history
- **Switching tasks?** → Checkpoint current, load new task context
- **Need more depth?** → Load specific files on demand
- **Exploration phase?** → Use observation masking

### Step 4: Monitor and Rebalance

After each significant action:
- Did we load new context?
- Can we evict completed task context?
- Should we summarize recent discussion?

---

## Failure Modes & Recovery

| Issue | Recovery |
|-------|----------|
| Hit context limit mid-task | Summarize history, evict exploration artifacts |
| Lost important context | Re-read key files, check conversation summary |
| Slow responses | Reduce loaded context, use lazy loading |
| Inconsistent behavior | Reload core + domain tiers explicitly |

---

## Integration with Other Skills

### /collab
- Use git branches for context checkpointing
- Branch summaries provide restoration points

### /repomix
- Generate compressed codebase bundles
- Load bundles for broad context, files for depth

### /skill-design
- Skills use progressive disclosure by design
- Apply same principles to conversation management

---

## Security & Permissions

- **Required tools**: None (advisory skill)
- **Confirmations**: None (no destructive actions)
- **Trust model**: Context management is metadata-level, no external data

---

## References

- [Context Tiers Deep Dive](references/context-tiers.md)
- [Summarization Techniques](references/summarization.md)

---

## Metadata

```yaml
author: Christian Kusmanow / Claude
version: 1.0.0
last_updated: "2026-01-23"
source:
  - Platform Agent Architecture (60_Science/)
  - JetBrains Context Management Research (2025)
  - Agent Skills progressive disclosure pattern
```
