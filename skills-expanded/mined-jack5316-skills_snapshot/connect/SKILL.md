---
name: connect
description: Find and surface relationships between notes, ideas, and concepts across the knowledge base. Use when asked to connect, link, or find relationships between notes/ideas, or /connect.
---

# Connect Skill

Finds relationships between notes, ideas, and concepts across the vault. Prioritizes surprising links over obvious ones. Best used before writing essays or weekly reviews.

## How It Works

1. Identify the seed note or concept
2. Scan for related notes by shared concepts, recurring names, contradictions, cause-effect chains, or chronological threads
3. Map connections with a brief reason for each link
4. Surface unexpected/non-obvious links — prioritize these
5. Suggest a synthesis note if 3+ notes converge; generate a MOC if 5+ connect

## Output Format

```markdown
**Seed:** [[note-name]]

**Direct connections:**
- [[note-a]] — shared concept: X

**Weak/unexpected connections:**
- [[note-c]] — tangentially related via Z

**Synthesis opportunity:** [optional]
```

If 5+ notes connect, outputs a MOC at `Maps/[Concept] MOC.md`.

This skill is prompt-based — invoke it by asking Claude to connect notes or find relationships.
