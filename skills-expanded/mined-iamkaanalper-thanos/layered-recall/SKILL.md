---
name: layered-recall
description: "Progressive memory recall with 4 scope layers AND 3 depth layers. Scope: identity > project > room > deep. Depth: IDs only > summary > full. 10-50x token savings through fetch-on-confirmation pattern. Grok-native port of the original Claude Code AI software team system layered-recall using memory-palace backend."
when-to-use: For long-running projects, session recovery, decision history, cross-session learning. Use before major work or when context is lost. Integrates with memory-palace, compound, pre-compact, on_agent_spawn.
---

# Layered Recall (Grok Adaptation)

Progressive memory system with **two orthogonal dimensions** of lazy loading:
1. **Scope layers** - What is relevant (identity, project, domain, deep)
2. **Depth layers** - How much detail to fetch (IDs, summary, full)

Combined savings: 10-50x tokens vs eager loading. Uses .grok/palace/ (JSONL + index) + .grok/projects/ for per-project + compound-friction for runtime signals.

## Depth Pattern (Fetch-on-Confirmation)

Instead of loading full memory entries upfront, agents fetch in 3 depths:

```
Depth 1: IDs only        (~10 tokens per match)
  Agent decides which are worth investigating

Depth 2: Summary         (~50 tokens per match)
  Room, type, preview (first 80 chars)
  Agent confirms relevance

Depth 3: Full content    (~500+ tokens per match)
  Only fetched for confirmed matches
```

**Example flow:**
```
1. Agent searches "auth refresh token" via palace recall
2. Depth 1 returns 8 IDs: d-abc123, d-def456, ...
3. Agent requests Depth 2 for IDs 1-3
4. Sees room=authentication, type=decision, preview="Chose JWT..."
5. Agent confirms IDs 1,3 are relevant
6. Requests Depth 3 only for those 2 entries
7. Gets full content for ~1000 tokens instead of 4000+
```

## The 4 Layers (Scope)

```
Layer 1: Identity (always loaded, ~200 tokens)
   Who is the user? What are their preferences?

Layer 2: Critical Facts (per-project, ~500 tokens)
   Hard constraints, active decisions, blockers

Layer 3: Room Recall (on-demand, ~1-2K tokens)
   Relevant memories for current task domain

Layer 4: Deep Search (when needed, ~2-5K tokens)
   Full semantic search across all memories
```

## Layer Details (Grok Backend)

### Layer 1: Identity (~200 tokens, ALWAYS loaded)
Loaded at every session start via on_agent_spawn or session start hooks.
Contains:
- User preferences (language, style, autonomy level) from .grok/config or palace identity room.
- Global constraints (no emojis, Turkish responses, etc.)
- Tool preferences (which editors, which terminal)

**Source:** .grok/palace/default.jsonl (room=identity) + .grok/projects/default/MEMORY.md (L1 section) + compound context.

### Layer 2: Critical Facts (~500 tokens, per-project)
Loaded when entering a project directory (via project-detect or cwd).
Contains:
- Active architectural decisions from palace/project rooms.
- Known blockers and constraints.
- Current sprint/milestone goals (from thoughts or palace).
- Tech stack and versions.

**Source:** .grok/palace/<wing>.jsonl + .grok/projects/<project>/MEMORY.md (L2) + palace index.

### Layer 3: Room Recall (~1-2K tokens, on-demand)
Loaded when task domain is detected (auth, database, deploy, etc.) via intent or prompt.
Contains:
- Previous decisions in this domain (palace rooms).
- Past errors and fixes (from compound-friction + monster ledger).
- Patterns that worked/failed.

**Source:** Memory palace rooms (filtered by room) + .grok/projects/<project>/wip-state.jsonl + mature instincts if promoted.

**Trigger:** Intent classifier or explicit "recall room=auth" or on_agent_spawn with context.

### Layer 4: Deep Search (~2-5K tokens, explicit)
Only loaded when explicitly needed or when Layers 1-3 don't have enough context.
Contains:
- Full semantic search results (use compound semantic.py or tldr).
- Cross-project pattern matches (from cross-project-learning).
- Historical error resolutions (monster + friction).

**Source:** .grok/palace/ all wings + compound-friction.jsonl + sessions/ for cross.

**Trigger:** Agent explicitly queries, or user asks "have we done this before?", or preflight detects ambiguity.

## Recall Flow (Grok)

```
Session Start
  -> Load Layer 1 (identity) via palace-recall hook or memory-palace
  -> Detect project (project-detect skill) -> Load Layer 2 (facts) from .grok/projects/<name>/MEMORY.md + palace
  -> User sends prompt
  -> Classify intent/domain (or via prompt) -> Load Layer 3 (room) on-demand
  -> If insufficient (use research-confidence 90% or agent decides) -> Load Layer 4 (deep) via semantic search in compound or palace
  -> Pre-compact: before compression, dump WIP to .grok/projects/<name>/wip-state.jsonl + palace
```

## Token Budget (Grok)

| Layer | Tokens | When |
|-------|--------|------|
| L1 | ~200 | Always (on spawn) |
| L2 | ~500 | Per project (cwd detect) |
| L3 | ~1-2K | Per task domain (room filter) |
| L4 | ~2-5K | On demand (explicit or low confidence) |
| **Total max** | **~8K** | Worst case |

vs. loading everything: ~30-50K tokens

**Savings: 4-6x token reduction**

## Integration with Grok Ported System

- **memory-palace skill**: Core backend. Use for store/recall. Layered-recall builds on it with progressive loading.
- **compound-learnings**: Use semantic.py for L4 deep, friction for signals.
- **pre-compact-state rule + auto_session_compressor hook**: Dump active task, modified files, decisions, WIP to palace + .grok/projects/<project>/wip-state.jsonl before compaction.
- **Hooks**: 
  - on_agent_spawn: inject L1 + L2 via palace-recall.
  - auto_palace_save.py: capture decisions to palace (enhance to support layers).
  - auto_session_compressor.py: tie to pre-compact.
- **on_bounded_loop_end, friction**: feed to palace rooms.
- **Agents**: Inherit L1-2, request L3-4 per domain (e.g. architect uses palace for decisions).
- **Ledger / handoff**: reference palace drawers in handoffs for history.
- **Cross-project**: use for promotion (2+ projects patterns to global palace).
- Complements friction/compound (palace = structured human decisions; friction = runtime signals).

## Room Detection Heuristics (Grok)

| Keywords in Context | Room |
|---------------------|------|
| auth, login, session, JWT, OAuth | authentication |
| database, SQL, migration, schema, postgres | database |
| deploy, CI/CD, Docker, K8s, release | deployment |
| React, CSS, component, UI, frontend | frontend |
| API, endpoint, REST, GraphQL, grpc | api |
| test, TDD, coverage, mock, pytest | testing |
| security, XSS, injection, CORS, compliance | security |
| performance, cache, optimize, profiler | performance |
| config, env, settings, terraform | configuration |
| agent, swarm, ledger, handoff, preflight | agents-orchestration |

## When to Store (Grok)

**ALWAYS store (via memory-palace or hooks):**
- Architectural decisions with reasoning (Constraint, Rejected, Confidence from commit-trailers or collaborative-decisions).
- External constraints (client requirements, hosting limits).
- Error resolutions that took effort (from self-learner, monster, coroner).
- Chosen patterns and why alternatives rejected (from compound drafts).

**NEVER store:**
- Code snippets (they're in git).
- Temporary debugging notes.
- Information already in .grok/docs/ or rules.
- Ephemeral task progress (use sessions/plan.md or thoughts for that).

## Operations (Grok Python Helpers)

Use in agents/hooks (adapt from memory-palace recall example + layered):

```python
from pathlib import Path
import json
from datetime import datetime

PALACE = Path.home() / ".grok" / "palace"
PROJECTS = Path.home() / ".grok" / "projects"

def layered_recall(query: str, scope: str = "project", depth: int = 3, wing: str = None):
    """
    Progressive recall.
    scope: 'identity' | 'project' | 'room' | 'deep'
    depth: 1 (IDs), 2 (summary), 3 (full)
    """
    results = []
    # L1: always from palace/default or projects/default/MEMORY.md
    if scope in ("identity", "project", "room", "deep"):
        # load identity
        pass
    # L2: per project
    if scope in ("project", "room", "deep"):
        if wing:
            mem = PROJECTS / wing / "MEMORY.md"
            if mem.exists():
                # parse L2 section
                results.append({"layer":2, "content": mem.read_text()[:500]})
    # L3/L4: from palace JSONL rooms
    if scope in ("room", "deep"):
        for jf in PALACE.glob("*.jsonl"):
            for line in jf.read_text().splitlines():
                d = json.loads(line)
                if query.lower() in d.get("content","").lower() or any(query.lower() in t.lower() for t in d.get("tags",[])):
                    if depth == 1:
                        results.append({"id": d["id"], "room": d.get("room")})
                    elif depth == 2:
                        results.append({"id": d["id"], "room": d.get("room"), "preview": d.get("content","")[:80], "type": d.get("type")})
                    else:
                        results.append(d)
    return results[:10]  # limit

# Store via memory-palace style append to wing jsonl or MEMORY.md L sections
```

## Grok Specific Notes

- Backend: .grok/palace/ (index.json + <wing>.jsonl) + .grok/projects/<name>/ (MEMORY.md, wip-state.jsonl) for per-project + pre-compact.
- Use compound semantic for L4 if needed.
- Auto via hooks: on_palace_auto_save, auto_session_compressor for pre-compact dump.
- Status: Now full layered-recall skill + integration. Memory-palace enhanced for progressive. Pre-compact WIP in projects/.
- Token efficient: always prefer L1-3 before L4. Use in preflight, on_agent_spawn, compass-like recovery.
- See .grok/rules/memory-system.md , pre-compact-state.md , cross-project-learning.md for rules.
- Original in .claude/skills/layered-recall/ and memory-palace/ (read-only reference).

This completes the palace memory recall for Grok: structured, progressive, integrated with existing flywheel, pre-compact, cross-project.

## Usage Example

Before task:
```python
from grok.skills.layered_recall import layered_recall
ctx = layered_recall("jwt auth decision", scope="room", depth=2)
# inject ctx to prompt
```

Auto store from architect/self-learner via hook.