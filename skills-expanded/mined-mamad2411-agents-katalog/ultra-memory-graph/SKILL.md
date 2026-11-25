---
tags: [skill, memory, ai, ultra, core]
category: "AI"
type: master-skill
priority: P0
thermal: COOL
---
# Ultra Memory Graph Skill

> **The skill that remembers everything, connects everything, and recalls instantly.**

## How It Works

This skill uses **Obsidian's Graph View** as a visual memory system for all 10,071 skills. Instead of loading skills into RAM (which causes heat), it uses:

1. **Stub Notes** — Each skill has a tiny note (~400 bytes) in Obsidian with just metadata + links
2. **Graph Links** — Wiki-links connect skills to categories (MOCs) and to each other
3. **Lazy Loading** — Full skill content is gzip-compressed in the catalog, loaded ONLY when needed
4. **Instant Recall** — Obsidian's search + graph traversal finds any skill in <1 second

## Quick Commands

### Find a Skill
```
# In Obsidian: Ctrl+O → type skill name → Enter
# Or use Omnisearch: Ctrl+Shift+F → search keywords
```

### Load Full Skill Content
```bash
# Load any skill on-demand (zero idle cost, loads in <100ms)
~/.agents/skills-catalog/lazy-load.sh "<skill_name>"

# Example:
~/.agents/skills-catalog/lazy-load.sh "pdf-extractor"
```

### Browse by Category
Open any MOC note in Obsidian:
- [[AI MOC]] — 775 skills
- [[Backend MOC]] — 1,193 skills  
- [[Document MOC]] — 281 skills
- [[Security MOC]] — 250 skills
- [[Cloud MOC]] — 271 skills
- [[Blockchain MOC]] — 172 skills
- [[Creative MOC]] — 285 skills
- [[Frontend MOC]] — 176 skills
- [[DevOps MOC]] — 172 skills
- [[Business MOC]] — 162 skills
- [[Mobile MOC]] — 149 skills
- [[Automation MOC]] — 104 skills
- [[Game MOC]] — 92 skills
- [[Productivity MOC]] — 64 skills
- [[Research MOC]] — 52 skills
- [[General MOC]] — 5,873 skills

### Graph View
```
# In Obsidian: Ctrl+G → opens graph view
# Shows all 10,071 skills as nodes connected to category MOCs
# Click any node → opens skill stub → load full skill on-demand
```

## Memory Architecture (Zero Heat)

```
┌─────────────────────────────────────────────┐
│           OBSIDIAN GRAPH VIEW                │
│  10,071 nodes (stub notes, ~400 bytes each)  │
│  16 MOC hubs (category centers)             │
│  Wiki-links = graph edges                    │
│  RAM: ~4MB total (Obsidian's native cache)  │
│  CPU: 0% idle (only renders on view)         │
└──────────────┬──────────────────────────────┘
               │
               │ On-demand load
               ▼
┌─────────────────────────────────────────────┐
│         GZIP CATALOG (48MB)                 │
│  10,071 .md.gz files (compressed)            │
│  Loaded via lazy-load.sh <name>             │
│  CPU: 0% idle (only loads when called)      │
│  RAM: 0KB idle (only loaded skill in RAM)   │
└──────────────┬──────────────────────────────┘
               │
               │ If skill needs to persist
               ▼
┌─────────────────────────────────────────────┐
│       ULTRA MEMORY NOTE                      │
│  Single note in Obsidian: "Ultra Memory"    │
│  Stores conversation context, decisions,    │
│  and learned patterns as wiki-links          │
│  Auto-linked to relevant skills via tags     │
└─────────────────────────────────────────────┘
```

## Thermal Profile (COOL — 30°C)

| Layer | Storage | Idle CPU | Idle RAM | On-Demand |
|-------|---------|----------|----------|-----------|
| Graph stubs | Obsidian vault (39MB on disk) | 0% | ~4MB (Obsidian cache) | Instant |
| Full skills | Gzip catalog (48MB) | 0% | 0KB | <100ms load |
| Memory note | Obsidian note (~10KB) | 0% | ~1KB | Instant |
| Background | None | 0% | 0KB | N/A |
| **TOTAL** | **87MB on disk** | **0%** | **~5MB** | **All 10,071 skills accessible** |

## Memory Recall Pattern

When the AI needs to recall something:

1. **Search Obsidian** → find relevant skill stub (0.1s)
2. **Read stub metadata** → see category, tags, connections (0.1s)
3. **Lazy-load full skill** → get actual content (<0.1s)
4. **Use skill** → apply to current task
5. **Release** → skill content not persisted in RAM

This means: **10,071 skills accessible, but only ~5MB RAM used at any time.**

## Graph Connections

Every skill note links to:
- Its category MOC (e.g., `[[AI MOC]]`)
- Related categories (via MOC cross-links)
- The catalog loader command

This creates a **knowledge graph** where:
- Nodes = skills (10,071)
- Hubs = MOCs (16 categories)
- Edges = wiki-links
- Traversal = graph view or search

## Maximizing Skill Potential

To get the BEST output from any skill:

1. **Stack skills**: Load 2-3 complementary skills at once
   ```bash
   ~/.agents/skills-catalog/lazy-load.sh "pdf-extractor"
   ~/.agents/skills-catalog/lazy-load.sh "ai-prompt-optimizer"  
   ~/.agents/skills-catalog/lazy-load.sh "output-refinery"
   ```

2. **Follow the graph**: Open a skill in Obsidian → check its MOC → find related skills → stack them

3. **Memory persistence**: After using a skill, note the outcome in the Ultra Memory note with a wiki-link to the skill. Next time, the graph remembers.

4. **Thermal guard**: If device feels warm, close Obsidian graph view. Skills still accessible via CLI.
