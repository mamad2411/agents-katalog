---
name: memory-manager
description: |
  Memory management guide. Load this skill when you detect
  information worth persisting (user identity, preferences,
  domain knowledge, procedures, lessons learned, etc.).
  Defines memory categories, file format, and management workflow.
  Recommend using a subagent for memory operations to avoid
  polluting the current context.
---

# Memory Management Guide

## When to Trigger

- User explicitly says "remember this" / "always do it this way"
- User shares personal info (name, role, team, etc.)
- User repeatedly corrects the same type of mistake (unrecorded preference)
- User shares lessons learned or past mistakes
- Important decision made or workflow established
- User shares domain knowledge or project context

## Memory Categories

All memory files live in `skills/memory-*/`. Organized along 3 orthogonal dimensions:

| Category | Dimension | Content | Decision rule |
|----------|-----------|---------|---------------|
| `memory-profile/` | **What is true** | Facts: identity, context, domain knowledge, relationships | Objective facts about user or environment |
| `memory-procedures/` | **How to do** | Workflows, steps, templates, conventions, tool usage | "To do X, follow these steps" |
| `memory-directives/` | **Should / shouldn't** | Preferences, rules, constraints, lessons, corrections | "Do/don't do X because Y" |

### Classification Tips

- **Profile vs Directives**: "Uses PostgreSQL" is profile (fact); "Always backup before migration" is directive (rule)
- **Profile vs Procedures**: "Project uses Turborepo" is profile (fact); "Run `turbo build` before deploy" is procedure (step)
- **Procedures vs Directives**: "Deploy steps: CI → review → prod" is procedure; "Never skip code review" is directive
- **Directives = preferences + lessons**: "Reply in Chinese" (preference) and "Don't use .returning() on SQLite" (lesson) both answer "should/shouldn't"

### When None Fit

If existing categories can't classify the information, create a new one:

1. Create `skills/memory-{name}/SKILL.md`
2. Add YAML frontmatter (name + description)
3. Ensure the new category is **orthogonal** to existing ones — it should answer a different question
4. Note: new categories appear in the skill list on next session

## File Format

Every SKILL.md must have YAML frontmatter:
- `name`: skill identifier (memory-{category})
- `description`: **Critical field — determines whether the skill gets loaded.** See below.

Body uses markdown lists, one memory per line.

### Frontmatter Description (Critical)

The description is the **only always-visible** information — the agent uses it to decide whether to load the skill. The more detailed and keyword-rich, the more likely relevant memories get surfaced.

**Principle: be as detailed as possible, within 1000 tokens.**

**Must include:**
1. One-sentence category purpose
2. Current entry count
3. **Keyword summary of all entries** — let the agent judge relevance from description alone
4. List reference/ filenames if any

**Good example:**
```yaml
description: |
  Normative knowledge. 5 entries.
  Covers: reply language (Chinese), style (concise), commit approval
  (confirm first), format (markdown tables), proactivity (offer options).
```

**Bad example:**
```yaml
description: |
  User preferences. 5 entries.
```

### Tiered Storage & Token Budget

```
SKILL.md frontmatter description  ≤1000 tokens  ← Always visible (decides loading)
SKILL.md body                     ≤10k tokens   ← Loaded on demand (skill())
reference/*.md                    Unlimited      ← Read on demand (Read tool)
```

When body approaches 10k tokens, move details to `reference/` subdirectory. Keep only summary index in body:
```markdown
## Deploy Workflow
- Overview (see [reference/deploy.md](./reference/deploy.md) for details)
```

## Management Operations (Use Subagent)

To avoid polluting the current conversation context, use the Agent tool to spawn a subagent:

```
Agent(
  subagent_type="general-purpose",
  description="Update memory: directives",
  prompt="Read skills/memory-directives/SKILL.md.
         Append this memory: [content].
         Update frontmatter description summary (entry count, keywords).
         If body exceeds 10k tokens, move details to reference/."
)
```

## Guidelines

- Each memory should be atomic: one fact / preference / lesson = one entry
- Avoid recording what can be inferred from code or environment
- Periodically merge duplicates, remove outdated entries
- **Always update frontmatter description after modifying body** — this is key to memory retrieval. Ensure new entry keywords appear in description, within 1000 tokens
