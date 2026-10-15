---
name: feature-decompose
description: Decompose large features into small, reviewable PRs with dependency analysis. Use when implementing features that touch 10+ files or multiple components.
---

# Feature Decomposition

Break down large features into small, focused PRs with clear dependencies.

## Instructions

### Step 1: Analyze the Feature

Understand the full scope:

```markdown
## Feature Analysis

### Feature: [Name]

**Goal:** [What this feature accomplishes]

**Affected Areas:**
- [ ] Database/Schema
- [ ] Types/Interfaces
- [ ] Backend Services
- [ ] API Endpoints
- [ ] Frontend Components
- [ ] Tests
- [ ] Documentation

**Estimated Total Changes:**
- Files: ~[N] files
- Lines: ~[N] lines
```

### Step 2: Identify Natural Boundaries

Look for these splitting points:

| Boundary Type | Description | Example |
|---------------|-------------|---------|
| **Layer** | DB → Service → API → UI | Types PR, then API PR, then UI PR |
| **Component** | Independent UI components | SearchBar PR, FilterPanel PR |
| **Feature** | Independent sub-features | Keyword search PR, Location filter PR |
| **Risk** | Safe vs risky changes | Add new code PR, Remove old code PR |

### Step 3: Map Dependencies

Create a dependency graph:

```markdown
## Dependency Graph

### PRs

1. **PR1: [Name]** - Base, no dependencies
2. **PR2: [Name]** - Depends on: PR1
3. **PR3: [Name]** - Depends on: PR1 (parallel with PR2)
4. **PR4: [Name]** - Depends on: PR2, PR3

### Visualization

PR1 (types)
 ├── PR2 (api) ──┐
 └── PR3 (ui) ───┼── PR4 (integration)
```

### Step 4: Define Each PR

For each PR, specify:

```markdown
## PR1: [Title]

**Type:** base | stacked | parallel

**Branch:** feat/feature-name-part1

**Dependencies:** None | PR#

**Files:**
- path/to/file1.ts
- path/to/file2.ts

**Changes:**
- [Specific change 1]
- [Specific change 2]

**Size Estimate:** ~[N] lines

**Reviewability:** [Easy | Medium | Hard]
```

### Step 5: Determine Execution Strategy

Choose based on dependencies:

```markdown
## Execution Strategy

### Stacked (Sequential)
- PR1 → PR2 → PR4

### Parallel (Can run simultaneously)
- PR2 and PR3 (after PR1 merged)

### Recommended Order
1. Create and merge PR1 (base types)
2. Start PR2 (api) and PR3 (ui) in parallel
3. After PR2 and PR3 merged, create PR4 (integration)
```

## Output Format

Produce a complete decomposition document:

```markdown
# Feature Decomposition: [Feature Name]

## Overview

- **Total PRs:** [N]
- **Estimated Time:** [N] hours/days
- **Parallelizable:** [Yes/No, how many]
- **Risk Level:** [Low/Medium/High]

## Dependency Graph

[ASCII diagram]

## PR Breakdown

### PR1: [Title]
- **Branch:** feat/...
- **Base:** develop
- **Type:** base
- **Files:** [list]
- **Size:** ~N lines
- **Description:** [what and why]

### PR2: [Title]
- **Branch:** feat/...
- **Base:** feat/... (PR1's branch)
- **Type:** stacked
- **Files:** [list]
- **Size:** ~N lines
- **Description:** [what and why]

[Continue for all PRs...]

## Execution Plan

### Phase 1: Foundation
1. Create PR1
2. Get review and merge

### Phase 2: Parallel Development
1. Create PR2 (api) - Agent 1
2. Create PR3 (ui) - Agent 2
3. Coordinate on shared types

### Phase 3: Integration
1. Wait for PR2 and PR3 to merge
2. Create PR4 (integration)
3. Final review and merge

## Coordination Notes

### Shared Files
- [file]: Owned by [PR#], others read-only

### Communication Points
- After PR1 merged: Both agents can start
- Before modifying shared types: Coordinate

## Rollback Plan

If issues found:
1. [Step to rollback]
2. [Alternative approach]
```

## Examples

### Example 1: User Authentication Feature

```markdown
# Feature Decomposition: User Authentication

## Overview
- **Total PRs:** 4
- **Estimated Time:** 3 days
- **Parallelizable:** Partially (PR2 and PR3)
- **Risk Level:** Medium

## Dependency Graph

PR1 (auth types)
 ├── PR2 (auth service) ──┐
 └── PR3 (login ui) ──────┼── PR4 (integration)

## PR Breakdown

### PR1: Auth Types and Interfaces
- **Branch:** feat/auth-types
- **Base:** develop
- **Type:** base
- **Files:** 
  - types/auth.ts
  - types/user.ts
- **Size:** ~80 lines

### PR2: Auth Service Implementation
- **Branch:** feat/auth-service
- **Base:** feat/auth-types
- **Type:** stacked
- **Files:**
  - services/authService.ts
  - api/routes/auth.ts
  - middleware/auth.ts
- **Size:** ~300 lines

### PR3: Login UI Components
- **Branch:** feat/auth-ui
- **Base:** feat/auth-types
- **Type:** parallel (with PR2)
- **Files:**
  - components/LoginForm.tsx
  - components/RegisterForm.tsx
  - hooks/useAuth.ts
- **Size:** ~250 lines

### PR4: Auth Integration
- **Branch:** feat/auth-integration
- **Base:** develop (after PR2, PR3 merged)
- **Type:** final
- **Files:**
  - pages/LoginPage.tsx
  - pages/RegisterPage.tsx
  - App.tsx (add auth provider)
- **Size:** ~150 lines
```

### Example 2: Database Migration

```markdown
# Feature Decomposition: Add Soft Delete

## Overview
- **Total PRs:** 3
- **Strategy:** By Risk (safe first)

## PR Breakdown

### PR1: Add deleted_at Column (Safe, Additive)
- Add nullable deleted_at column
- No behavior change yet

### PR2: Update Queries (Behind Flag)
- Add feature flag for soft delete
- Update queries to filter by deleted_at
- Both paths work (flag on/off)

### PR3: Enable and Cleanup
- Enable flag by default
- Remove old code path
- Add hard delete for admin
```

## Tips

1. **Target PR Size:** 200-400 lines of logic
2. **Reviewability:** Each PR should be reviewable in <30 minutes
3. **Independence:** Maximize parallel PRs to reduce total time
4. **Clear Boundaries:** Each PR should have a clear, single purpose
5. **Test Inclusion:** Include relevant tests in each PR, not separate

## Anti-patterns

- **Too Large:** PRs with 1000+ lines
- **Too Granular:** 20 PRs for a simple feature
- **Circular Dependencies:** PR1 needs PR2, PR2 needs PR1
- **Unclear Scope:** "Misc changes" or "Part 1"
