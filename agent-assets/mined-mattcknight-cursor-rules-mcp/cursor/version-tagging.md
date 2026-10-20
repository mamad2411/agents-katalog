---
description: Version Tagging Rule - Git tags after phase completion following gitflow versioning
alwaysApply: false
tags: [git, versioning, gitflow, tagging]
priority: 2
version: 1.0.0
---

# Version Tagging Rule

## 🔴 MANDATORY: Version Tagging After Phase Completion

**Git tags MUST be created after major phase completions following gitflow versioning conventions.**

---

## Core Requirements

### When to Tag

**Tags are created:**
1. **After Phase Completion**: When a major phase is completed (Phase 0.1, 0.2, 0.3, etc.)
2. **Explicit User Request**: When user explicitly requests a tag
3. **Rule Trigger**: When a rule explicitly triggers tagging

**Tags are NOT created:**
- Automatically after every commit
- After minor updates or fixes
- Without explicit trigger or user request

---

## Version Format

### Gitflow Versioning Convention

**Format:** `v{MAJOR}.{MINOR}.{PATCH}`

**Examples:**
- `v0.1.0` - Phase 0.1 completion (Solution Architecture Document)
- `v0.2.0` - Phase 0.2 completion (Technical Design Document)
- `v0.3.0` - Phase 0.3 completion (Implementation Specification)
- `v0.4.0` - Phase 0.4 completion (Data Evaluation & Test Strategy)
- `v0.5.0` - Phase 0.5 completion (Documentation Review & Approval)
- `v1.0.0` - Phase 1 completion (Foundation Setup)
- `v1.1.0` - Phase 2 completion (Core Matching Service)
- `v1.2.0` - Phase 3 completion (Review Workflow)
- etc.

### Version Increment Rules

- **MAJOR**: Incremented for major milestones or breaking changes
- **MINOR**: Incremented for phase completions (Phase 0.1 → 0.2 → 0.3)
- **PATCH**: Incremented for bug fixes or minor updates within a phase

---

## Tagging Process

### Step 1: Determine Version

**Check existing tags:**
```bash
git tag -l "v*" | sort -V
```

**Determine next version:**
- If last tag is `v0.2.0` and Phase 0.3 completed → `v0.3.0`
- If last tag is `v0.3.0` and Phase 0.4 completed → `v0.4.0`
- Follow semantic versioning increment rules

### Step 2: Create Tag

**Tag format:**
```bash
git tag -a v{MAJOR}.{MINOR}.{PATCH} -m "Phase {PHASE}: {DESCRIPTION}

- {List of deliverables}
- {Key achievements}
- {Completion date}

---
Produced By AI: Composer and Cursor IDE"
```

**Example:**
```bash
git tag -a v0.3.0 -m "Phase 0.3: Implementation Specification Complete

- Complete project structure specified
- All service interfaces and implementations defined
- Docker configuration specified
- Database migrations defined
- Configuration files specified
- Embedding service implementation specified
- Completion date: 2025-11-12

---
Produced By AI: Composer and Cursor IDE"
```

### Step 3: Push Tag (ONLY if explicitly requested)

**CRITICAL: DO NOT push tags automatically. Only push if user explicitly requests.**

**Push tag to remote (only if requested):**
```bash
git push origin v{MAJOR}.{MINOR}.{PATCH}
```

**Default behavior:** Tags are created locally only. User must explicitly request push.

---

## Phase-to-Version Mapping

| Phase | Version | Description |
|-------|---------|-------------|
| Phase 0.1 | v0.1.0 | Solution Architecture Document |
| Phase 0.2 | v0.2.0 | Technical Design Document |
| Phase 0.3 | v0.3.0 | Implementation Specification |
| Phase 0.4 | v0.4.0 | Data Evaluation & Test Strategy |
| Phase 0.5 | v0.5.0 | Documentation Review & Approval |
| Phase 1 | v1.0.0 | Foundation Setup |
| Phase 2 | v1.1.0 | Core Matching Service |
| Phase 3 | v1.2.0 | Review Workflow |
| Phase 4 | v1.3.0 | Vector DB Population |
| Phase 5 | v1.4.0 | Testing & Validation |
| Phase 6 | v1.5.0 | Documentation & Deployment |

---

## Tag Message Format

**Standard tag message structure:**

```
Phase {PHASE}: {TITLE}

- {Deliverable 1}
- {Deliverable 2}
- {Key achievement}
- Completion date: {YYYY-MM-DD}

---
Produced By AI: Composer and Cursor IDE
```

---

## Workflow

### Automatic Tagging (Rule Trigger)

**When:** After phase completion, if rule explicitly triggers tagging

**Process:**
1. Check current phase completion status
2. Determine next version number
3. Create annotated tag with phase details (LOCAL ONLY)
4. Report tag creation to user
5. DO NOT push tag unless user explicitly requests

### Manual Tagging (User Request)

**When:** User explicitly requests tagging

**Process:**
1. User requests tag (e.g., "add tag for phase completion")
2. Determine version number
3. Create annotated tag (LOCAL ONLY)
4. Confirm tag creation
5. DO NOT push tag unless user explicitly requests push

---

## Tag Naming Conventions

### Annotated Tags

**Use annotated tags** (not lightweight tags):
- `-a` flag for annotated tags
- Include message with phase details
- Include completion date
- Include AI attribution

### Tag Names

**Format:** `v{MAJOR}.{MINOR}.{PATCH}`

**Examples:**
- `v0.1.0`
- `v0.2.0`
- `v0.3.0`
- `v1.0.0`

**Never use:**
- `phase-0.3` (use version format)
- `v0.3` (include patch version)
- `release-0.3` (use version format)

---

## Verification

### Check Tags

**List all tags:**
```bash
git tag -l "v*" | sort -V
```

**View tag details:**
```bash
git show v0.3.0
```

**Verify tag pushed:**
```bash
git ls-remote --tags origin
```

---

## Remember

✅ **ALWAYS use annotated tags** (`-a` flag)  
✅ **ALWAYS follow version format** `v{MAJOR}.{MINOR}.{PATCH}`  
✅ **ALWAYS include phase details** in tag message  
✅ **ONLY tag** when rule triggers or user explicitly requests  
✅ **CREATE tags locally only** (do not push automatically)  
✅ **NEVER tag** automatically after every commit  
✅ **NEVER push tags** unless user explicitly requests  
✅ **NEVER use** lightweight tags for phase completions

---

**Last Updated:** 2025-11-12  
**Version:** 1.0.0  
**Status:** MANDATORY  
**Priority:** HIGH
