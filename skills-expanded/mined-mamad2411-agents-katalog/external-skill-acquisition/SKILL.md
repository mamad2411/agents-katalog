---
name: external-skill-acquisition
description: Use when no installed skill covers the task domain and external acquisition is needed. Provides a 3-tier decision flow — auto-install from known repos, manual review from community, or synthesize from documentation. Covers marketplace search, license gates, and same-session prompt injection.
---

# External Skill Acquisition

Workflow for acquiring domain skills when the local skill library doesn't cover the task.

## When to Trigger

Invoke this workflow when **ALL** conditions are true:

1. **No local match**: You checked installed skills in `.claude/skills/` and found nothing for the task domain
2. **Domain expertise needed**: The task requires domain-specific knowledge beyond general coding
3. **Named domain**: The gap involves a recognized field — finance, climate, legal, medical, security, etc.

**DO NOT trigger when**:
- General uncertainty or unfamiliar libraries (use web search instead)
- Task solvable with general coding knowledge
- One-off API questions (use documentation lookup)

## Decision Flow

```
Task arrives → check .claude/skills/
  │
  ├─ Match found → load the skill → DONE
  │
  └─ No match → Is this a named domain expertise gap?
       │
       ├─ NO  → Use general knowledge or web search → DONE
       │
       └─ YES → Proceed to 3-Tier Acquisition ↓
```

## 3-Tier Acquisition

### Tier 1: Auto-Install (MIT/Apache-2.0, verified repos)

Search these repos first — they're community-vetted and license-safe:

| Repo | Focus | Skills |
|------|-------|--------|
| `obra/superpowers` | Dev workflow (TDD, debugging, planning) | ~16 skills |
| `vercel-labs/agent-skills` | Web/React/Next.js | ~50 skills |
| `anthropics/skills` | Claude-specific patterns | ~10 skills |

**Search before installing**:
```bash
# Search marketplace
curl -s "https://api.skyll.app/search?q=<domain-keyword>&limit=5"

# Or use the npx CLI
npx --yes skills find <domain-keyword>
```

If found → install with `/skills-install <owner/repo>`.

### Tier 2: Manual Review (community repos)

If Tier 1 misses, search GitHub for community skills:
```bash
gh search repos "topic:claude-skills topic:agent-skills <domain>" --sort stars --limit 10
```

Before installing from unknown repos:
1. **Check license**: Must be MIT, Apache-2.0, MPL-2.0, BSD-2/3, CC-BY-4.0, or CC-BY-SA-4.0
2. **Check quality**: Read the SKILL.md — does it have clear procedures or just vague advice?
3. **Check freshness**: Last commit within 6 months?

If acceptable → install with `/skills-install <owner/repo>`.

### Tier 3: Synthesize from Documentation

When no existing skill covers the domain, create one from documentation:

1. **Find authoritative docs**: Official API docs, framework guides, specification pages
2. **Extract procedures**: Convert docs into step-by-step agent instructions
3. **Create SKILL.md**: Use `/skills-create <domain-name>` to scaffold, then fill in:
   - Trigger conditions (when to load)
   - Step-by-step procedures
   - Common pitfalls and error handling
4. **Validate**: Run `/skills-validate <name>` to check frontmatter

## Same-Session Use

Newly installed skills won't be auto-discovered until the next session. To use immediately, inject the skill content directly into your working context:

```
# Read the newly acquired skill
skill_content = read(".claude/skills/<new-skill>/SKILL.md")

# Include it in your current context
# The agent will follow the skill's procedures for the remainder of this session
```

## License Gate

Only auto-install skills with these licenses:
- MIT
- Apache-2.0
- MPL-2.0
- BSD-2-Clause / BSD-3-Clause
- CC-BY-4.0 / CC-BY-SA-4.0

Unknown or restrictive licenses → manual review only (Tier 2 with explicit user approval).

## When to Load This Skill

Load `external-skill-acquisition` when:
- Delegating work in an unfamiliar domain and no installed skill matches
- User asks about acquiring or finding domain-specific skills
- Planning work in a novel domain
- Searching for skills to install

**Not needed when**:
- Existing skills cover the domain
- Task is general coding, testing, or infrastructure
- Already know which repo to install from (just use `/skills-install`)
