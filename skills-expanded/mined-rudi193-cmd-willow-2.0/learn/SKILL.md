---
name: learn
description: Extract a reusable pattern and weave it into the knowledge graph via edges
---

@markdownai v1.0

# /learn — Extract and Edge

Use when something non-obvious was discovered: a workaround, a subtle invariant, a constraint that affects future work.

Learned patterns live as edges in the knowledge graph, not as orphaned files. They are discovered by traversing relationships, not by searching.

## What to learn

- Operational constraints discovered during work
- Workarounds for library/API quirks
- Version-specific fixes or incompatibilities
- Architecture patterns or gotchas
- Integration patterns that save time
- Performance characteristics not obvious from code

## What NOT to learn

- Code patterns derivable by reading the repo
- Git history (use `git log`)
- Task state or in-progress work from this session
- Anything already in CLAUDE.md or documented code

## Steps

1. **Name the pattern** — one short title. Examples:
   - "WillowStore auto-embeds on __init__ when _VEC_AVAILABLE"
   - "Skills consolidation by mode reduces duplication"
   - "Gleipnir rate window resets per app_id independently"

2. **Search existing atoms** — `kb_search` for the pattern name and related keywords. If an identical pattern atom exists, update its edges instead of creating a duplicate.

3. **Identify related atoms** — list 2-4 atoms this pattern connects to:
   - Problem it solves
   - Module/system it affects
   - Similar patterns or constraints
   - Use cases that trigger it

4. **Create the pattern atom** — `kb_ingest`:
   ```json
   {
     "app_id": "hanuman",
     "title": "<pattern name>",
     "summary": "<one-sentence constraint or insight>",
     "source_type": "discovered_pattern",
     "category": "pattern",
     "domain": "hanuman"
   }
   ```

5. **Create edges** — for each related atom, call `soil_add_edge`:
   ```json
   {
     "app_id": "hanuman",
     "from_id": "<pattern_atom_id>",
     "to_id": "<related_atom_id>",
     "relation": "relates_to|solves|affects|contradicts|implements",
     "context": "<why this edge matters>"
   }
   ```

6. **Confirm** — report the pattern atom ID and edge count.

## Rules

- No files. The pattern is the atom; edges are the connections.
- One pattern per atom. Keep it focused.
- Edges are what make learned patterns discoverable. Create at least 2 edges.
- If a pattern already exists, add edges instead of duplicating.
- Learned patterns are active citizens in the graph, not passive references.
