---
name: 3-layer-memory
description: This skill should be used when setting up or managing a compounding three-layer memory system for AI assistants. It applies when users want to create a self-maintaining knowledge graph with automatic fact extraction, entity-based storage, and weekly synthesis. Triggers on "set up memory system", "knowledge graph", "automatic memory", "compounding memory", or requests to manage persistent context across conversations.
license: Complete terms in LICENSE.txt
---

# 3-Layer Memory System

A simple, compounding knowledge graph that evolves as your understanding changes.

## What This System Provides

- **Entity-based storage** — Facts organized by person, company, project — not dumped into a single blob
- **Single-file entities** — One markdown file per entity with YAML frontmatter for structured data
- **Superseding, not deleting** — When facts change, old ones are marked historical; full history preserved
- **Optional automation** — Start manual, add automation only when it hurts

**Result**: Understanding that updates itself. Context stays current without manual edits.

## The Three-Layer Architecture

```
Layer 1: Knowledge Graph   (~/life/entities/)
   └── Single-file entities: maria.person.md, acme-corp.company.md

Layer 2: Daily Notes       (~/life/days/YYYY-MM-DD.md)
   └── Raw event logs — what happened, when

Layer 3: Tacit Knowledge   (~/MEMORY.md)
   └── Patterns, preferences, lessons learned
```

## When to Use This Skill

Use this skill when:
- Setting up the three-layer memory system for the first time
- Creating new entities (people, companies, projects) in the knowledge graph
- Extracting facts from conversations
- Performing weekly synthesis and summary updates
- Querying the knowledge graph for context

## Quick Start

### 1. Initialize the System

Run the initialization script:

```bash
python3 ~/.claude/skills/3-layer-memory/scripts/init_memory_system.py
```

This creates:
```
~/life/
├── entities/              # Knowledge graph (Layer 1)
└── days/                  # Daily notes (Layer 2)
~/MEMORY.md                # Tacit knowledge (Layer 3)
```

### 2. Add to AGENTS.md

Include this section in the repo's AGENTS.md:

```markdown
## Memory — Three Layers

### Layer 1: Knowledge Graph (`~/life/entities/`)
Single-file entities with YAML frontmatter:
- `maria.person.md` — Person entities
- `acme-corp.company.md` — Company entities  
- `ai-project.project.md` — Project entities

Format: human-readable markdown with optional YAML frontmatter for structured facts.

Rules:
- Save facts immediately during conversations
- Mark outdated facts with `[was]` prefix
- Clean up summaries when they feel stale

### Layer 2: Daily Notes (`~/life/days/YYYY-MM-DD.md`)
- Raw timeline of events
- Written during or after conversations
- Simple bullet list format

### Layer 3: Tacit Knowledge (`~/MEMORY.md`)
- Patterns, preferences, lessons learned
- Long-term behavioral knowledge
```

## Layer 1: Knowledge Graph

### Entity Structure

Each entity is a single markdown file:

```
~/life/entities/
├── maria.person.md
├── acme-corp.company.md
└── ai-project.project.md
```

### Entity File Format

```markdown
---
type: person
created_at: 2026-01-15
---

# Maria

> Business partner on AI project (since Jan 2026)

## Key Facts

- [current] Business partner on AI project — Jan 2026
- [current] Company hired 2 developers — Jan 2026
- [was] Former colleague at OldCo — 2025 to Jan 2026

## Context

Met through previous role at OldCo. Company is growing fast.
```

**Frontmatter (optional):** Use YAML frontmatter for structured data when needed.

**Body:** Human-readable markdown. Use `[current]` and `[was]` prefixes to track fact status.

### Creating New Entities

Use the entity management script:

```bash
python3 ~/.claude/skills/3-layer-memory/scripts/manage_entity.py create --type person --name "maria"
```

Or create manually:

```bash
cat > ~/life/entities/maria.person.md << 'EOF'
---
type: person
created_at: 2026-01-15
---

# Maria

## Key Facts

- [current] Business partner on AI project — Jan 2026

## Context

Met through previous role at OldCo.
EOF
```

## Layer 2: Daily Notes

Daily notes capture the raw timeline. Create them during or after conversations:

```markdown
# 2026-01-27

- 10:30am: Shopping trip
- 2:00pm: Doctor follow-up — follow-up in 3 months
- Decided: Calendar events now use emoji categories
```

Simple bullet list. No structured sections required.

Durable facts can be extracted into Layer 1 entities during or after the conversation.

## Layer 3: Tacit Knowledge

MEMORY.md captures how the user operates:

```markdown
# My Memory

## How I Work
- Sprint worker — intense bursts, then rest
- Contact preference: Call > SMS > Email
- Early riser, prefers brief messages

## Lessons Learned
- Don't create cron jobs for one-off reminders
- Weekly reviews are more effective than daily

## Preferences
- Code style: DHH Rails style
- Communication: Async first, urgent = call
```

## Fact Extraction

### Manual (Recommended Default)

Extract facts during the conversation when they come up:

1. Notice a durable fact in conversation
2. Add it to the relevant entity file immediately
3. Use `[current]` prefix for new facts
4. Mark old facts with `[was]` if superseded

### Automated (Optional)

If manual extraction becomes painful, add automation:

```bash
# Extract from recent conversations
python3 ~/.claude/skills/3-layer-memory/scripts/extract_facts.py --since 2026-01-20

# Extract from specific file
python3 ~/.claude/skills/3-layer-memory/scripts/extract_facts.py --file conversation.md
```

## Weekly Synthesis

### Manual (Recommended Default)

When reading an entity file, if the summary feels stale:

1. Read the current facts
2. Rewrite the summary section
3. Mark superseded facts with `[was]`

### Automated (Optional)

If manual synthesis becomes painful:

```bash
# Run synthesis manually
python3 ~/.claude/skills/3-layer-memory/scripts/weekly_synthesis.py

# Or configure a weekly cron job (advanced)
```

## Templates

Use templates in `assets/templates/` for creating new entities:

- `entity.md` — Template for single-file entities
- `daily_notes.md` — Template for daily notes
- `memory_tacit.md` — Template for MEMORY.md

## Best Practices

1. **Start simple** — One layer, manual maintenance. Add complexity only when needed.

2. **Always supersede, never delete** — Use `[was]` prefix to preserve history.

3. **Write daily notes continuously** — Capture events while fresh; extract facts later.

4. **Single source of truth** — One file per entity. No sync issues.

5. **Human-readable first** — If you can't read it in `cat`, it's too complex.

6. **Manual until it hurts** — Don't automate until manual process becomes painful.

7. **Keep MEMORY.md focused** — Patterns and preferences only; specific facts belong in knowledge graph.

## Migration from Complex Systems

If migrating from a more complex memory system:

1. Run initialization script
2. Move entity data to single-file format
3. Convert JSON facts to markdown lists
4. Keep patterns/preferences in MEMORY.md (Layer 3)

## Troubleshooting

**Issue: Facts getting disorganized**
- Simplify entity structure
- Use consistent `[current]`/`[was]` prefixes
- Rewrite summaries when they feel stale

**Issue: Too much maintenance overhead**
- Reduce automation
- Simplify daily notes format
- Fewer structured sections

**Issue: Context window overflow**
- Load only relevant entities
- Keep entity files concise
- Use summaries in daily notes
