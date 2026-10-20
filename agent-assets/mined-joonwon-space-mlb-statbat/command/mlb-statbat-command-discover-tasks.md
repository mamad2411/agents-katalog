---
description: Research project analysis docs and codebase state to refresh tasks.md (current work) and todo.md (future work).
---

# Discover Tasks

Use the **discover-tasks** agent for this task. The agent runs on Sonnet for deep research and analysis.

Delegate all work to the `discover-tasks` agent now.

## Document roles

| Doc | Role | Content |
|-----|------|---------|
| `docs/plan/tasks.md` | **Current work** | Immediately actionable tasks. Read by `/auto-task` and `/next-task` |
| `docs/plan/todo.md` | **Future work** | Long-term backlog/roadmap. Not urgent but eventually needed |

## Steps

### 1. Read project docs

Read all of:
- `docs/plan/tasks.md` — current task list
- `docs/plan/todo.md` — future backlog
- `docs/plan/manual-tasks.md` — manual items

### 2. Codebase research

Investigate actual code state vs docs:
- **New files/features** not yet reflected in docs
- **TODO/FIXME/HACK/XXX comments** (`grep -r "TODO\|FIXME\|HACK\|XXX"`)
- **NotImplementedError** stubs in Python files
- **Build errors** (`cd frontend && npx tsc --noEmit`)
- **Lint errors** (`cd backend && ruff check .` if ruff is available)
- **git log** — recent changes needing follow-up

### 3. Refresh task lists

Classify discovered work into the appropriate doc:

**Put in `tasks.md` (current work):**
- Bug fixes
- Build/lint error fixes
- Security vulnerability patches
- Quality improvements (error handling, type fixes)
- Stub implementations (NotImplementedError → real code)

**Put in `todo.md` (future work):**
- New feature ideas
- Large refactoring
- Deployment/infrastructure
- Performance optimization
- Long-term roadmap items

### 4. tasks.md writing rules

```markdown
# MLB StatBat — Tasks

Current work items. Read by `/auto-task` and `/next-task`.
Each item should be completable in a single commit.

---

## Current work

### Priority — Category

- [ ] Task 1 — specific, actionable description
- [ ] Task 2
...
```

- Each item must be **specific** ("add PitchingStats model" not "improve backend")
- Decompose to single-commit size
- Clean up completed items (`[x]`) when 10+ accumulate

### 5. todo.md writing rules

```markdown
# MLB StatBat — TODO

## 🔴 P0 — Category
### [ ] Item 1
- Details

## 🟡 P1 — Category
...
```

- Group by priority
- Collapse completed sections
- Mark items ready for promotion to tasks.md

### 6. Commit

```
git add docs/
git commit -m "docs: update project analysis and task lists"
```

### 7. Output

```
Research complete!

Task lists:
- tasks.md: N current tasks (M new)
- todo.md: N future tasks (M new)
- manual-tasks.md: N manual items

Next: run `/auto-task` or `/next-task` to execute.
```
