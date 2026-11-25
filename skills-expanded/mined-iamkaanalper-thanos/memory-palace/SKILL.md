---
name: memory-palace
description: Hierarchical memory organization for multi-session context retention. Wings (projects) > Rooms (domains) > Drawers (decisions). Semantic search across all memories with zero cloud dependency. Grok-native port/adaptation of the the original Claude Code AI software team system concept.
when-to-use: For long-running projects, session recovery, decision history, cross-session learning. Use before major work or when context is lost.
---

# Memory Palace (Grok Adaptation)

Hierarchical, persistent memory for Grok sessions and projects. Organizes knowledge so agents and users never lose critical decisions across sessions or compactions.

## Architecture (Adapted for .grok/)

```
Palace (global under ~/.grok/palace/)
  Wing: project-name (from workspace or manifest)
    Room: authentication
      Drawer: "chose JWT over sessions (reason: stateless...)" 
    Room: database
      Drawer: "PostgreSQL + pgvector migration strategy"
    ...
```

Storage: `~/.grok/palace/` as JSONL per wing + index (similar to compound-friction.jsonl pattern we already use).

## When to Store
- Architectural decisions + WHY (constraint, rejected alternatives)
- Error resolutions that took effort
- External constraints (hosting, rate limits, compliance)
- Chosen patterns with evidence

**NEVER:** temp debug, code snippets (git), one-off tasks.

## Operations
- Store: append to wing's JSONL with room, content, tags, timestamp, session, agent.
- Recall: before task, load relevant rooms by keyword/project.
- Search: across wings for patterns ("have I solved X before?").

## Integration with Our Ported System
- **Architect / kraken / planner**: auto store decisions.
- **Self-Learner / compound**: store resolutions as patterns for evolution.
- **Hooks**: on_agent_spawn / pre-compact can inject recall (we can wire later).
- **Ledger / handoff**: reference palace drawers in handoffs for history.
- Complements our friction/compound (palace = structured human decisions; friction = runtime signals).

## Grok Specific Notes
- Storage: ~/.grok/palace/ (index.json + <wing>.jsonl) - dirs created in madde-4.
- Use compound-friction.jsonl style for appends.
- Tie to .grok/projects/ or workspace detection for wing name.
- For full power, combine with our compound_evolution for promoting drawers to rules/skills.
- Auto via hook: on_palace_auto_save (madde-3).
- Recall example (python snippet for agents):

```python
import json
from pathlib import Path
def recall(wing="default", room=None, query=""):
    base = Path.home() / ".grok" / "palace"
    idx = json.loads((base / "index.json").read_text())
    wing_file = base / f"{wing}.jsonl"
    if not wing_file.exists(): return []
    results = []
    for line in wing_file.read_text().splitlines():
        d = json.loads(line)
        if (not room or d.get("room")==room) and (query.lower() in d.get("content","").lower() or query.lower() in " ".join(d.get("tags",[])).lower()):
            results.append(d)
    return results
```

- Status: Enhanced for full layered-recall integration (see .grok/skills/layered-recall/SKILL.md). Now supports 4-scope/3-depth progressive loading on top of palace JSONL + .grok/projects/ per-project MEMORY.md + wip-state. Pre-compact WIP preservation wired. Semantic via compound. Hooks (auto_palace_save, session compressor) integrated. Full recall flow for on_agent_spawn, preflight, compass recovery.

This gives Grok the "never lose context" benefit with 4-6x+ token savings via layered-recall, integrated with compound/friction/preflight/ledger.

See .grok/skills/layered-recall/SKILL.md and original in ~/.claude/skills/memory-palace/ (read-only reference) for full details.