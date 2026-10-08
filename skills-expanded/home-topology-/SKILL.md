# Cursor AI Rules for home-topology Project

> These rules guide AI behavior when working on this project.
> This file is automatically loaded by Cursor AI in every conversation.

---

## 1. Project Identity

- **Name**: home-topology
- **Package**: home_topology (Python import)
- **Purpose**: Platform-agnostic home topology kernel with pluggable modules
- **Python**: 3.11+ (uses `str | None` syntax)
- **Status**: v0.1.0-alpha (Foundation + OccupancyModule complete)

---

## 2. Documentation Structure (When to Read What)

### 🎯 Before Starting ANY Task
**Read**: `docs/project-status.md`
- Check what's already in progress
- Avoid duplicate work
- Update status as you work

### 🏗️ For Architecture Decisions
**Read**: `docs/architecture.md` (kernel architecture)
**Then**: Check `docs/adr-log.md` for prior decisions
**If new decision**: Add to `docs/adr-log.md` with rationale

### 📦 For Module Implementation
**Read**: 
- `docs/modules/occupancy-design.md` (if working on occupancy)
- `docs/modules/automation-architecture.md` (if working on automation)
- Specific module design docs as needed

### 💻 For Coding Style
**Read**: `docs/coding-standards.md`
- File naming, type hints, docstrings
- Architecture patterns
- Testing standards

### ❓ When Unsure
**Read**: `docs/decisions-pending.md`
- Check if question already exists
- If not, ADD it with priority level

### 🤝 For Contribution Workflow
**Read**: `.github/pull_request_template.md` and `docs/coding-standards.md`

---

## 3. Core Architectural Rules (Don't Read Docs, Just Follow)

### Separation of Concerns
- `LocationManager`: Topology + config storage ONLY
- `Modules`: Behavior + runtime state ONLY
- `EventBus`: Event routing ONLY

### Module Requirements
Every module MUST implement:
- `id: str` property
- `CURRENT_CONFIG_VERSION: int` property
- `attach(bus, loc_manager)` method
- `default_config()` method
- `location_config_schema()` method
- Optional: `dump_state()`, `restore_state()`, `migrate_config()`

### Event Model
```python
Event(
    type: str,              # "sensor.state_changed", "occupancy.changed"
    source: str,            # "ha", "occupancy", "actions"
    location_id: Optional[str],
    entity_id: Optional[str],
    payload: Dict[str, Any],
    timestamp: datetime,    # UTC, use datetime.now(UTC)
)
```

### No Platform Dependencies
- NEVER import `homeassistant.*` in `src/home_topology/`
- HA integration is separate adapter (future)

---

## 4. Coding Standards (Quick Reference)

### File Naming
- Directories: lowercase, no underscores (except `src/home_topology/`)
- Python modules: `snake_case.py`
- Tests: `test_*.py`

### Code Style
- Formatter: `black` (line length 100)
- Linter: `ruff`
- Type checker: `mypy` (strict mode)
- All public functions MUST have type hints and docstrings

### Testing
- Target: >90% coverage for core, >80% for modules
- Use pytest fixtures for setup
- AAA pattern (Arrange, Act, Assert)

---

## 5. Workflow Rules

### Starting Work
1. Read `docs/project-status.md` first
2. Move task to "In Progress"
3. Create feature branch
4. Read relevant module design doc

### Making Changes
1. Code + tests together (test coverage must not decrease)
2. Update CHANGELOG.md and docs in same commit
3. Run `make check` before committing

### Big Decisions
1. Check `docs/adr-log.md` - already decided?
2. If new: Add to `docs/adr-log.md` with context + rationale
3. Update `docs/project-status.md` decision log section

### Finishing Work
1. Tests pass (`make test`)
2. Linting passes (`make check`)
3. CHANGELOG.md and docs updated
4. Move task to "Completed" in `docs/project-status.md`
5. Create PR with description

---

## 6. Documentation Workflow (CRITICAL)

### ❌ NEVER Create These Files:
- `2025.XX.XX-*.md` - Dated completion reports
- `YYYY.MM.DD-summary.md` - Work summaries
- Any standalone "what we did" reports

**Why?** Information belongs in proper locations, not duplicate reports.

---

### ✅ Documentation Workflow by Task Type

#### For Design Work (Pre-Implementation)

**Create/Update:**
1. **Design doc** in proper location:
   - Module design → `docs/modules/{module}-design.md`
   - Integration guide → `docs/integration/{feature}.md`
   - Core architecture → Update `docs/architecture.md`

2. **Add to roadmap**:
   - Add to `docs/project-status.md` under "Future Features (Designed)"
   - Include target version, status, brief description

3. **DONE** - No summary files!

**Example:**
```
✅ Created: docs/modules/presence-module-design.md
✅ Updated: docs/project-status.md (added to Future Features)
❌ NO: docs/2025.12.09-presence-design-complete.md
```

---

#### For Implementation Work (Code Changes)

**Update:**
1. **CHANGELOG.md** - Add under `[Unreleased]` section:
   - `### Added` - New features
   - `### Changed` - Changes to existing functionality
   - `### Fixed` - Bug fixes
   - `### Documentation` - Doc updates

2. **Architecture docs** (if core API changed):
   - Update `docs/architecture.md` with new methods/classes
   - Keep version number current

3. **ADR-LOG.md** (if architectural decision):
   - Add ADR entry with context, decision, rationale
   - Only for significant architectural choices

4. **project-status.md** (if major milestone):
   - Move items from Planned → Completed
   - Update metrics

5. **DONE** - No completion reports!

**Example:**
```
✅ Updated: CHANGELOG.md (added alias support to [Unreleased])
✅ Updated: docs/architecture.md (v1.6 with new methods)
✅ Added: ADR-020 to docs/adr-log.md
❌ NO: docs/2025.12.09-core-enhancements.md
```

---

### Document Purpose Reference

| Document | Purpose | Update When |
|----------|---------|-------------|
| **CHANGELOG.md** | User-facing changes | Every feature/fix/change |
| **docs/architecture.md** | Current system design | Core API changes |
| **docs/adr-log.md** | Architectural decisions | Big design choices |
| **docs/project-status.md** | Roadmap & work tracking | Sprint changes, milestones |
| **docs/modules/*.md** | Module specifications | Designing/changing modules |
| **docs/integration/*.md** | Integration guides | Platform-specific features |
| **docs/decisions-pending.md** | Open questions | Need team input |
| ~~**2025.XX.XX-*.md**~~ | ~~Nothing~~ | ~~NEVER~~ ❌ |

---

### Why No Completion Reports?

**Bad:**
```
docs/2025.12.09-core-enhancements.md (282 lines)
  - Lists what changed ← Already in CHANGELOG.md
  - Lists files modified ← Git handles this
  - Lists design decisions ← Already in ADR-LOG.md
  - Lists tests passing ← CI handles this
  = 100% duplicate information
```

**Good:**
```
CHANGELOG.md: "Added alias support with 6 new methods"
docs/architecture.md: Updated LocationManager API documentation
docs/adr-log.md: ADR-020 explains why aliases in core
Git commit: Shows exact files changed
= Single source of truth for each piece of information
```

---

## 7. Smart Document Loading Strategy

### Instead of Reading Everything:
```python
# ❌ DON'T DO THIS
read_file("docs/architecture.md")
read_file("docs/coding-standards.md") 
read_file("docs/project-status.md")
read_file("docs/modules/occupancy-design.md")
# ... spam all docs

# ✅ DO THIS
# Task: "Add timeout tests for occupancy"
read_file("docs/project-status.md")  # Check status
read_file("docs/modules/occupancy-design.md")  # Get implementation details
# That's it! Other rules are in this .cursorrules file
```

### Use grep/codebase_search:
```python
# Looking for how EventBus is used?
grep("EventBus", path="src/")

# Looking for occupancy timeout logic?
codebase_search("how are occupancy timeouts calculated", ["src/home_topology/modules/occupancy"])
```

---

## 8. Smart Document Loading Strategy

### Instead of Reading Everything:
```python
# ❌ DON'T DO THIS
read_file("docs/architecture.md")
read_file("docs/coding-standards.md") 
read_file("docs/project-status.md")
read_file("docs/modules/occupancy-design.md")
# ... spam all docs

# ✅ DO THIS
# Task: "Add timeout tests for occupancy"
read_file("docs/project-status.md")  # Check status
read_file("docs/modules/occupancy-design.md")  # Get implementation details
# That's it! Other rules are in this .cursorrules file
```

### Use grep/codebase_search:
```python
# Looking for how EventBus is used?
grep("EventBus", path="src/")

# Looking for occupancy timeout logic?
codebase_search("how are occupancy timeouts calculated", ["src/home_topology/modules/occupancy"])
```

---

## 9. Quick Decision Tree

```
Am I working on kernel core (Location, EventBus, Manager)?
├─ YES → Read DESIGN.md
└─ NO
    │
    Am I implementing a module?
    ├─ YES → Read docs/modules/{module}-design.md
    └─ NO
        │
        Am I making an architectural decision?
        ├─ YES → Read ADR-LOG.md, then add new entry
        └─ NO
            │
            Do I have a question?
            ├─ YES → Read DISCUSSION-NEEDED.md, check if answered
            └─ NO → Check WORK-TRACKING.md and code!
```

---

## 10. Anti-Patterns to Avoid

### ❌ Don't:
- Read all docs at start of every conversation
- Ignore WORK-TRACKING.md (leads to duplicate work)
- Make big decisions without logging in ADR-LOG.md
- Create new patterns without checking CODING-STANDARDS.md
- Forget to update docs when changing code
- **Create dated completion reports (2025.XX.XX-*.md)**
- **Duplicate information across multiple docs**

### ✅ Do:
- Read only what's needed for current task
- Always update WORK-TRACKING.md
- Log decisions immediately
- Update docs in same commit as code
- Use grep/search before reading entire files
- **Put each piece of information in ONE proper place**
- **Update CHANGELOG.md for all user-facing changes**

---

## 11. Example Scenarios

### ❌ Don't:
- Read all docs at start of every conversation
- Ignore WORK-TRACKING.md (leads to duplicate work)
- Make big decisions without logging in ADR-LOG.md
- Create new patterns without checking CODING-STANDARDS.md
- Forget to update docs when changing code

### ✅ Do:
- Read only what's needed for current task
- Always update WORK-TRACKING.md
- Log decisions immediately
- Update docs in same commit as code
- Use grep/search before reading entire files

### Scenario: "Add motion sensor support to occupancy"
```
1. Read docs/project-status.md (check if already in progress)
2. Read docs/modules/occupancy-design.md (understand signals)
3. grep("motion", path="src/home_topology/modules/occupancy/")
4. Code + test
5. Update CHANGELOG.md (add to [Unreleased] → Added)
6. Update docs/project-status.md
```
**Don't need**: docs/architecture.md, docs/coding-standards.md (covered by .cursorrules)
**Don't create**: 2025.XX.XX-motion-sensor-complete.md ❌

### Scenario: "Design new EnergyModule"
```
1. Read docs/architecture.md (understand module architecture)
2. Read docs/modules/occupancy-design.md (example module)
3. Check docs/adr-log.md (prior module decisions)
4. Create docs/modules/energy-design.md
5. Add to docs/project-status.md (Future Features section)
```
**Don't create**: 2025.XX.XX-energy-design.md ❌

### Scenario: "Fix a bug"
```
1. Read docs/project-status.md (log the bug)
2. grep the error or use codebase_search
3. Fix + test
4. Update CHANGELOG.md (add to [Unreleased] → Fixed)
5. Update docs/project-status.md (completed)
```
**Don't need**: Design docs unless bug is architectural

### Scenario: "Implement alias support feature"
```
1. Code + tests
2. Update CHANGELOG.md:
   [Unreleased]
   ### Added
   - Alias support in Location dataclass
   - 6 alias management methods in LocationManager
3. Update docs/architecture.md (document new methods)
4. Add ADR-020 to docs/adr-log.md (why aliases in core)
5. DONE
```
**Don't create**: docs/2025.12.09-alias-implementation.md ❌

---

## 12. Commit Message Format

```
<type>(<scope>): <subject>

<body>

Updated WORK-TRACKING.md: [task moved to completed]
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

---

## 13. Testing Requirements

- All new code MUST have tests
- Test coverage MUST NOT decrease
- Run `make check` before every commit
- Pytest fixtures in `tests/` for common setup

---

## 14. Project-Specific Conventions

### Entity Naming for Auto-Detection
- Motion: `binary_sensor.*_motion` or `binary_sensor.pir_*`
- Presence: `binary_sensor.*_presence`, `ble_*`, `*_radar`
- Doors: `binary_sensor.*_door`
- Media: `media_player.*`

### Timeout Units
- Engine internally: **minutes**
- Module config: **seconds**
- Convert at module boundary

### Import Order
```python
# 1. Standard library
import os
from datetime import datetime

# 2. Third-party (if any - avoid in core!)

# 3. Local imports
from home_topology.core import Location
from home_topology.modules.base import LocationModule
```

---

## 15. When to Ask User vs Decide

### Ask User When:
- Breaking changes to API
- New external dependencies
- Architectural direction unclear
- Multiple valid options with trade-offs

### Decide and Log When:
- Implementation details
- Code organization
- Small refactors
- Bug fixes
- Test strategies

---

## 16. Performance Guidelines

- Synchronous EventBus is fine for <100 events/sec
- Hierarchy queries are O(depth), acceptable for <10 levels
- State in memory, persist via dump_state()
- Profile only if actual performance issue

---

## 17. Summary: The Golden Rules

1. **ALWAYS read WORK-TRACKING.md first**
2. **NEVER create dated completion reports (2025.XX.XX-*.md)**
3. **ALWAYS update CHANGELOG.md for user-facing changes**
4. **Log architectural decisions in ADR-LOG.md**
5. **Update docs with code, not after**
6. **Don't read docs you don't need**
7. **Use grep/search before reading full files**
8. **Test everything, maintain coverage**
9. **Type hints + docstrings = mandatory**
10. **No HA dependencies in core**
11. **ALWAYS use 2025 for current dates (NOT 2024!)** ⚠️

---

## Quick Reference

| Task | Read |
|------|------|
| Any task | docs/project-status.md |
| Kernel work | docs/architecture.md |
| Module work | docs/modules/{module}-design.md |
| Big decision | docs/adr-log.md |
| Question | docs/decisions-pending.md |
| Code style | This file (don't read docs/coding-standards.md) |

---

**This file is your compass. Follow it, and you won't get lost in the docs.**

Last Updated: 2025-12-09
