# AGENTS.md: Work Context Coordination

**Capability ID**: chora.coordination.work_context
**For**: AI Agents (Claude Code, cursor, etc.)
**Version**: 1.0.0
**Last Updated**: 2025-11-20

---

## Quick Reference

**Purpose**: Enable concurrent development across multiple work contexts (tabs, developers, sessions) with conflict prevention and intelligent work partitioning.

**Key Insight**: Treat each tab as a "developer" - tab-as-dev pattern unifies multi-tab and multi-developer coordination.

**When to Use**:
- Working in multiple Claude Code tabs simultaneously
- Multiple developers working in same repository
- Async work sessions (morning/afternoon contexts)

---

## Agent Patterns

### Pattern 1: Register Work Context on Session Start

**When**: Claude Code tab opens and begins work

**Action**:
```bash
# Detect current branch and domain
CURRENT_BRANCH=$(git branch --show-current)
WORK_DOMAIN="docs"  # or scripts/, tests/, etc.

# Register context
just work-context-register tab-1 tab "$CURRENT_BRANCH" "$WORK_DOMAIN/**/*"
```

**Why**: Establishes awareness of active work for conflict detection

---

### Pattern 2: Check Conflicts Before Editing Shared Files

**When**: About to edit high-risk files (justfile, INDEX.md, CODEOWNERS, etc.)

**Action**:
```bash
# Query who else is working on file
just who-is-working-on justfile

# If conflict detected, coordinate:
# - Ask user: "tab-2 is editing justfile. Coordinate or defer?"
# - Suggest: "Work on low-conflict files first"
```

**Why**: Proactive conflict avoidance (vs reactive merge resolution)

---

### Pattern 3: Suggest Work Partitioning

**When**: User asks "What should I work on?" or starting new task

**Action**:
```bash
# Show work dashboard
just work-dashboard

# Analyze conflicts:
# - If tab-2 is in docs/, suggest scripts/ for tab-1
# - If justfile has conflicts, defer justfile edits
# - Prioritize isolated work (separate domains)
```

**Why**: Minimize conflict risk through intelligent task assignment

---

### Pattern 4: Update AGENTS.md with Multi-Context Sections

**When**: Adopting work-context-coordination in new repository

**Action**:
1. Add "## Multi-Context Coordination" to domain AGENTS.md files
2. Document conflict zones (high-risk files)
3. Provide collaboration decision tree (solo/async/sync)
4. Link to `.chora/work-contexts.yaml` for live state

**Why**: Self-documenting coordination patterns in awareness files

---

## CLI Commands (Justfile Recipes)

### Register Context
```bash
just work-context-register <ID> <TYPE> <BRANCH> <FILES>

# Example: Register tab-1 working on docs
just work-context-register tab-1 tab tab1/feat/x "docs/**/*.md"
```

### Show Dashboard
```bash
just work-dashboard

# Output:
# Active Work Contexts:
#   tab-1 (tab): docs/**/*.md
#   tab-2 (tab): scripts/**/*.py, justfile
#
# Conflict Zones:
#   ⚠️  justfile (tab-1 + tab-2)
```

### Query File Ownership
```bash
just who-is-working-on <FILE>

# Example:
just who-is-working-on justfile
# Output: tab-1 (tab), tab-2 (tab)  [CONFLICT]
```

---

## Decision Tree: When to Coordinate

```
Are you editing a file?
├─ YES: Is it a shared file (justfile, INDEX.md, CODEOWNERS)?
│  ├─ YES: Check `just who-is-working-on <file>`
│  │  ├─ Conflict detected (2+ contexts)?
│  │  │  ├─ Coordinate with other context
│  │  │  └─ OR defer to low-conflict work
│  │  └─ No conflict: Proceed
│  └─ NO: Proceed (low risk)
└─ NO: Starting new task?
   └─ Run `just work-dashboard`
      ├─ High-conflict zones identified?
      │  └─ Avoid those files, work in isolated domain
      └─ No conflicts: Choose any task
```

---

## Integration with Existing SAPs

### SAP-051 (Git Workflow)
- **Branch naming**: Contexts use branch prefixes (`tab1/`, `tab2/`, `alice/`, `bob/`)
- **Pre-merge**: Run `just conflict-check` before merging context branch
- **Conventional commits**: All contexts follow same format

### SAP-052 (Code Ownership)
- **CODEOWNERS**: Work partitioning respects ownership zones
- **Conflict zones**: Ownership data informs risk scoring
- **Reviewer assignment**: Suggest reviewers based on context ownership

### SAP-053 (Conflict Resolution)
- **Pre-merge detection**: `just conflict-check main` before merging
- **Conflict types**: Detect file/content/semantic across contexts
- **Resolution guidance**: Link to SAP-053 resolution patterns

### SAP-049 (Namespace Resolution)
- **Modern namespace**: `chora.coordination.work_context`
- **Legacy aliases**: SAP-054, SAP-055 (deprecated 2026-06-01)
- **Deprecation warnings**: Tools warn about legacy identifiers

---

## Adoption Workflow

### L1: Essential (Lightweight Pilot)

**Setup** (5 minutes):
1. Create `.chora/work-contexts.yaml` (empty initially)
2. Copy `scripts/who-is-working-on.sh` and `scripts/detect-conflicts.sh`
3. Add justfile recipes (work-context-register, work-dashboard, who-is-working-on)
4. Add "Multi-Context Coordination" section to AGENTS.md

**Daily Usage**:
1. Register context on session start: `just work-context-register tab-1 tab <branch> <files>`
2. Check dashboard before editing shared files: `just work-dashboard`
3. Query file ownership when conflicts suspected: `just who-is-working-on <file>`

**Expected Impact**:
- 20-30% reduction in coordination overhead
- 15-25% fewer merge conflicts

---

### L2: Intermediate (Automated Registration)

**Enhancement** (2-3 hours):
1. Git hooks: Auto-register context on branch checkout
2. Auto-update work-contexts.yaml on file edits
3. Pre-commit hook: Warn about conflict zones

**Expected Impact**:
- 40-50% coordination time savings
- Automatic conflict detection

---

### L3: Advanced (Capability Server)

**Upgrade** (8-12 hours):
1. Deploy chora-coordination capability server
2. REST API + MCP tools + CLI
3. Real-time dashboard (WebSocket updates)
4. Proactive conflict alerts

**Expected Impact**:
- 60-80% conflict reduction
- 50-70% coordination time savings

---

## Troubleshooting

### Issue: "No context found for file"

**Cause**: File not in any context's file patterns

**Solution**:
1. Check `.chora/work-contexts.yaml` for registered patterns
2. Expand file patterns: `"docs/*.md"` → `"docs/**/*.md"` (recursive)
3. Or register new context covering that file

---

### Issue: "Conflict detected but no actual conflict"

**Cause**: Both contexts reference same file pattern but editing different files

**Solution**:
1. Narrow file patterns: `"docs/*.md"` → `"docs/AGENTS.md"` (specific file)
2. Or use glob patterns: `"docs/{AGENTS,CLAUDE}.md"` (explicit list)

---

### Issue: "Dashboard shows stale contexts"

**Cause**: Contexts not unregistered after session ends (manual pilot limitation)

**Solution**:
1. Manually edit `.chora/work-contexts.yaml` to remove stale contexts
2. Or upgrade to L2 (automated cleanup via git hooks)
3. Or upgrade to L3 (capability server with TTL expiration)

---

## Examples

### Example 1: Two Tabs, No Conflicts

**Scenario**: Tab 1 working on docs, Tab 2 working on scripts

```bash
# Tab 1
just work-context-register tab-1 tab tab1/docs/update "docs/**/*.md"

# Tab 2
just work-context-register tab-2 tab tab2/scripts/refactor "scripts/**/*.py"

# Check conflicts
just work-dashboard
# Output: 0 conflicts (separate domains)
```

---

### Example 2: Two Tabs, justfile Conflict

**Scenario**: Both tabs need to add recipes to justfile

```bash
# Tab 1
just work-context-register tab-1 tab tab1/feat/x "docs/**/*.md,justfile"

# Tab 2
just work-context-register tab-2 tab tab2/feat/y "scripts/**/*.py,justfile"

# Check conflicts
just work-dashboard
# Output: ⚠️ Conflict: justfile (tab-1 + tab-2)

# Coordination decision:
# Option A: Tab 1 edits justfile first, commits, Tab 2 pulls and edits
# Option B: Both defer justfile edits until features complete
# Option C: One tab handles all justfile updates (centralized)
```

---

### Example 3: Multi-Developer (Alice + Bob)

**Scenario**: Alice working on frontend, Bob on backend

```bash
# Alice's machine
just work-context-register alice dev alice/feat/ui "src/ui/**/*.tsx"

# Bob's machine
just work-context-register bob dev bob/feat/api "src/api/**/*.ts"

# Shared dashboard (if federated):
just work-dashboard
# Output:
#   alice (dev): src/ui/**/*.tsx
#   bob (dev): src/api/**/*.ts
#   0 conflicts (separate domains)
```

---

## Related Documentation

- [capability-charter.md](capability-charter.md) - Full problem/solution/ROI analysis
- [protocol-spec.md](protocol-spec.md) - API/CLI specifications
- **SAP-051**: Git Workflow Patterns (branch naming, conventional commits)
- **SAP-052**: Code Ownership (CODEOWNERS, ownership zones)
- **SAP-053**: Conflict Resolution (pre-merge detection, resolution guidance)

---

**Status**: Pilot (Lightweight implementation, no capability server)
**Next Phase**: Validate tab-as-dev pattern, gather feedback, decide on L3 upgrade
**Last Updated**: 2025-11-20
