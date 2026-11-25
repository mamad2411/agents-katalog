---
name: z-brain
description: Zero-overhead cognitive episodic memory for AI agents. Sub-millisecond retrieval via local SQLite FTS5 and context-diet progressive disclosure.
---

# 🧠 Z-Brain — Episodic Cognitive Memory Skill

Z-Brain provides local, zero-infrastructure semantic memory for AI agents. It replaces heavy external database calls with an embedded in-process SQLite FTS5 engine, enforcing progressive disclosure to prevent context window bloat.

---

## 1. Core Workflow: The PRE / POST Cognitive Cycle

Every non-trivial coding, architecture, or debugging task follows the 2-step cycle:

```
[Start Task] ──► PRE: zbrain_fetch("<task description>") ──► [Progressive L0 Index]
                                                                     │ (If deep detail needed)
                                                                     ▼
                                                          zbrain_view(id)
                                                                     │
                                                                     ▼
                                                             [Execute Work]
                                                                     │
[Task Done]  ◄── POST: zbrain_harvest("<problem>|<cause>|<fix>") ◄───┘
```

---

## 2. Tools Reference

### A. PRE-Task Context Fetch (`zbrain_fetch`)
Call before starting complex refactoring, bug fixes, or architecture design:
- **`task`**: High-level description of what you are about to do.
- **`project`**: Current project scope (e.g. `agentic-core`, `ua`, `erp`). Defaults to current project + `global`.
- **`tags`**: Optional filters (e.g. `["tech:ua", "tech:async"]`).
- **`limit`**: Max items (default: 5).

> **Token Advantage**: Returns an ultra-compact **L0 Index** (`~30-50 tokens/atom`) containing only IDs, trust badges, tags, and Gotcha/Fix summaries. It preserves over 80% of context window compared to raw database dumps.

### B. Deep Item Inspection (`zbrain_view`)
Call only when an atom in the L0 index contains a code pattern or gotcha that directly impacts your implementation:
- **`id`**: Integer ID from the L0 index.

### C. POST-Task Knowledge Harvesting (`zbrain_harvest`)
Call immediately after completing non-trivial tasks, bugfixes, or refactoring:
- **`lesson`**: Atomic lesson in `<problem> | <cause> | <fix>` format.
- **`tags`**: At least 2 tags:
  - 1 Domain tag: `inventory`, `sales`, `production`, `rd`, `ua`.
  - 1 Tech tag: `async`, `refactor`, `bug`, `pattern`, `winforms`, `wpf`.
- **`trust_level`**: `verified_fact` (backed by green builds/tests), `observation`, or `hypothesis`.
- **`evidence`**: Verification proof (e.g. `build:ok`, `test:49/49`).
- **`files`**: Optional array of modified or affected file paths.

### D. Quick Query (`zbrain_query`)
Search specific questions or keywords across the local memory base.

### E. Project Timeline & Decisions (`zbrain_timeline`)
Chronological audit of recent architectural decisions, milestones, and discoveries:
- **`project`**: Project name (defaults to current project).
- **`limit`**: Max entries (default: 10).

### F. File-Centric Intelligence (`zbrain_file`)
Look up knowledge atoms and architectural decisions associated with a specific file:
- **`file`**: Target file path or file name.
- **`limit`**: Max entries (default: 5).

### G. Record Decision / Milestone (`zbrain_observe`)
Record technical decisions or milestones into episodic memory:
- **`title`**: Concise title.
- **`summary`**: Rationale or summary.
- **`type`**: `decision`, `milestone`, `discovery`, `refactor`, or `bugfix`.
- **`files`**: Optional array of associated file paths.

### H. Status & Health (`zbrain_status`)
Inspect memory stats, total atoms, SQLite database size, and engine health.

---

## 3. Terminal Dashboard CLI

Prefer terminal commands over heavy web dashboards (Zero RAM bloat, zero port collisions, 100% agent & human parity):
- `z-brain recent [--limit=10] [--project=name]`: Formatted table view of latest knowledge atoms.
- `z-brain timeline [--limit=10] [--project=name]`: Chronological list of project decisions and milestones.
- `z-brain file <path>`: Gotchas, bugfixes, and past decisions attached to a file.
- `z-brain observe "<title> | <summary>" [--project=name] [--type=decision] [--files=f1,f2]`: Record a milestone or decision.
