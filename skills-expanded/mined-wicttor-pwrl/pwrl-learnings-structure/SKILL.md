---
name: pwrl-learnings-structure
description: "Structure classified learnings for persistent storage with metadata, indexing, and navigation."
argument-hint: "[classification artifact from pwrl-learnings-classify]"
---

# pwrl-learnings-structure — Learning Structuring

**Purpose:** Phase 3 of learnings workflow. Transforms classified learnings into standardized storage format with comprehensive metadata, full-text indexing, and navigation indexes. Enables efficient retrieval and discovery.

## Interaction Method

- Primarily automated transformation and formatting.
- Ask user only for storage strategy preference: "Organize by type or domain?"
- Show storage summary before proceeding.
- No approval gate; proceed to next skill.

## Input: Classification Artifact

Expects artifact from `pwrl-learnings-classify` with:

```yaml
classify_id: YYYY-MM-DD-NNN-classify
learnings: [array of classified learnings]
```

Each learning has: type, domain, priority, applicability, tags, title, problem, application.

## Output: Structure Artifact

Emit structure artifact (YAML + markdown):

```yaml
---
format: pwrl-learnings-structure-artifact
version: "1.0"
structure_id: YYYY-MM-DD-NNN-structure
created: ISO-8601-timestamp
---

# Learning Structure Results

## Summary
- **Learnings Stored:** [count]
- **Storage Path:** docs/learnings/
- **Organization Strategy:** by_type | by_domain | by_category

## Storage Structure

### By Type
```

docs/learnings/
├── gotcha/ [N files]
├── pattern/ [N files]
├── decision/ [N files]
├── technical_fix/ [N files]
└── workflow/ [N files]

```

### By Domain
```

docs/learnings/
├── backend/ [N files]
├── frontend/ [N files]
├── architecture/ [N files]
├── security/ [N files]
├── devops/ [N files]
└── ...

```

## Index Files Generated
- `INDEX.md` — Master index by type
- `BY_TYPE.md` — Organized by type
- `BY_DOMAIN.md` — Organized by domain
- `BY_PRIORITY.md` — Organized by priority
- `BY_APPLICABILITY.md` — Organized by applicability score
- `RECENT.md` — Recently added learnings
- `.index.json` — Machine-readable index

## Storage Details
- **Total Learnings:** [count]
- **Files Created:** [count]
- **Index Files:** [count]
- **Full-Text Index Entries:** [count]

## Format & Metadata
- **Storage Format:** markdown
- **Metadata Fields:** [list of fields per learning]
- **Slug Generation:** enabled (for URLs)
- **Full-Text Index:** enabled (for search)

## Ready for Deduplication
- **Status:** ready
- **Next Skill:** pwrl-learnings-dedup
- **Artifacts Passed:** This structure artifact + learning files
```

Artifact passed to `pwrl-learnings-dedup`.

## Detailed Workflow

For complete step-by-step instructions, see [structure-learnings-detailed-workflow.md](references/structure-learnings-detailed-workflow.md).

This SKILL.md provides an overview. The detailed workflow document contains:

- Format normalization with default values
- Slug generation and collision detection
- Fingerprint calculation (for Phase 4 dedup)
- Full-text index entry creation
- Storage path generation by strategy
- Markdown template formatting
- Index file generation examples

## Quality Gate Validation

After completing this phase, run quality gate validation:

```bash
/pwrl-phase-checkpoint learnings 3 [artifact-path]
```

See [pwrl-phase-checkpoint](../../pwrl-phase-checkpoint/SKILL.md) for validation rules.

---

1. Check that input artifact has:
   - Valid `classify_id`
   - `learnings` array populated with classified items
   - Each learning has: type, domain, priority, applicability, tags

2. **If verification fails:**
   - Return error: "Classification artifact invalid. Return to pwrl-learnings-classify."

### Step 2: Determine Storage Strategy

**Ask user for preference (if needed):**

```
How should learnings be organized?
- By Type: Gotchas, Patterns, Decisions, etc.
- By Domain: Backend, Frontend, Security, etc.
- By Category: By date (2026-06, 2026-07, etc.)
```

**Default:** By Type (most intuitive for browsing)

### Step 3: Normalize Learning Format

**Ensure all learnings have standard structure:**

```yaml
Learning Record:
  id: [Auto-generated UUID or slug]
  slug: [URL-safe identifier]
  type: [gotcha | pattern | decision | technical_fix | workflow]
  domain:
    [
      backend | frontend | architecture | devops | security | performance | process | testing,
    ]
  priority: [critical | important | nice_to_know]
  applicability:
    current_project: [0-10]
    general: [0-10]
  tags: [list of tags]

  title: [Learning title]
  problem: [Problem description]
  application: [How to apply]

  source:
    type: [code | commit | task | documentation | error | review]
    reference: [file:line | commit_hash | task_id]
    extracted_at: [ISO-8601 timestamp]

  metadata:
    created_at: [ISO-8601 timestamp]
    updated_at: [ISO-8601 timestamp]
    author: [User ID if known]
    confidence: [high | medium | low]
```

**Add defaults for missing fields:**

- If `id` missing: Generate from slug
- If `slug` missing: Generate from title
- If `applicability` missing: Auto-calculate from priority/domain

### Step 4: Generate Metadata

**For each learning, create/enhance metadata:**

1. **Generate slug:**
   - URL-safe, lowercase, hyphenated
   - Example: "race-condition-in-cache"
   - Collision detection: append -1, -2 if needed

2. **Generate fingerprints:**
   - Title hash (detect duplicates)
   - Content hash (detect modifications)
   - These enable dedup phase

3. **Generate full-text index entry:**
   - Extract searchable keywords: title + problem + tags
   - Create inverted index entry: keyword → learning ID

4. **Add relationships:**
   - References to complementary learnings
   - Backreferences from related learnings

### Step 5: Generate Storage Paths

**Based on strategy, determine file path:**

**If by_type:**

```
docs/learnings/TYPE/YYYY-MM-DD-SLUG.md
docs/learnings/gotcha/2026-06-12-race-condition-cache.md
```

**If by_domain:**

```
docs/learnings/DOMAIN/YYYY-MM-DD-SLUG.md
docs/learnings/backend/2026-06-12-race-condition-cache.md
```

**If by_category:**

```
docs/learnings/YYYY-MM/TYPE-SLUG.md
docs/learnings/2026-06/gotcha-race-condition-cache.md
```

### Step 6: Format Content

**Convert each learning to markdown format:**

```markdown
---
id: [UUID]
type: gotcha
domain: backend
priority: critical
applicability:
  current_project: 9
  general: 8
tags: [typescript, concurrency, cache, critical]
created_at: 2026-06-12T10:30:00Z
source:
  type: code
  reference: "src/cache.ts:42"
---

# Race Condition in Shared Cache

## Problem

Multiple threads can access and modify the cache simultaneously without locking,
causing data corruption and inconsistent state. This can happen when:

- Thread A reads cache value
- Thread B writes new value
- Thread A overwrites with stale value

## Symptom

- Intermittent data corruption
- Tests pass in isolation, fail under concurrency
- Non-deterministic failures (hard to debug)

## Root Cause

Cache object (`this.data`) is mutated without synchronization. JavaScript is
single-threaded, but in Node.js clusters or with workers, multiple processes
can share memory.

## Solution

Use a mutex or semaphore to serialize access:

\`\`\`typescript
import { Mutex } from 'async-lock';

class Cache {
private data = {};
private lock = new Mutex();

async get(key: string) {
return this.lock.acquire('cache', () => this.data[key]);
}

async set(key: string, value: any) {
return this.lock.acquire('cache', () => {
this.data[key] = value;
});
}
}
\`\`\`

## Prevention

1. Always use locking for shared mutable state
2. Prefer immutable data structures
3. Consider using a proper cache library (Redis, Memcached)
4. Test with concurrent operations (stress testing)
5. Use TypeScript strict mode + concurrency linter rules

## Related Learnings

- [Mutex Usage Pattern](mutex-usage-pattern.md)
- [Immutable Data Structure Benefits](immutable-structures.md)

## References

- https://nodejs.org/en/docs/guides/worker-threads/
- MDN: Race Condition
```

### Step 7: Create Index Files

**Generate navigation indexes in docs/learnings/ root:**

**INDEX.md - Master Index:**

```markdown
# Learnings Index

Browse learnings by type:

- [Gotchas](BY_TYPE.md#gotchas)
- [Patterns](BY_TYPE.md#patterns)
- [Decisions](BY_TYPE.md#decisions)
- [Technical Fixes](BY_TYPE.md#technical-fixes)
- [Workflows](BY_TYPE.md#workflows)

Or browse by:

- [Domain](BY_DOMAIN.md)
- [Priority](BY_PRIORITY.md)
- [Applicability](BY_APPLICABILITY.md)
- [Recently Added](RECENT.md)

Total learnings: [count]
```

**BY_TYPE.md - Type Organization:**

```markdown
# Learnings by Type

## Gotchas (20 learnings)

- [Race condition in shared cache](gotcha/2026-06-12-race-condition-cache.md)
- [Null pointer dereference](gotcha/2026-06-10-null-pointer.md)
  ...

## Patterns (30 learnings)

- [Memoization technique](pattern/2026-06-11-memoization.md)
- [Builder pattern for configuration](pattern/2026-06-09-builder-pattern.md)
  ...
```

**BY_DOMAIN.md - Domain Organization:**

```markdown
# Learnings by Domain

## Backend (40 learnings)

- Race Condition (Gotcha) - [link]
- API Rate Limiting (Pattern) - [link]
  ...

## Frontend (20 learnings)

- React Hook Dependencies (Gotcha) - [link]
- Component Composition (Pattern) - [link]
  ...

## Security (15 learnings)

...
```

**BY_PRIORITY.md - Priority Organization:**

```markdown
# Learnings by Priority

## Critical (8 learnings)

- Must know these before shipping
- [link] Race Condition
- [link] SQL Injection Prevention
  ...

## Important (25 learnings)

...

## Nice to Know (20 learnings)

...
```

**BY_APPLICABILITY.md - Relevance Scores:**

```markdown
# Learnings by Applicability

## Highly Relevant (9-10) - 12 learnings

- Current project uses these technologies frequently
- [link] React Hooks
- [link] TypeScript Generics
  ...

## Moderately Relevant (5-8) - 20 learnings

...

## Niche (0-4) - 5 learnings

...
```

**RECENT.md - Recently Added:**

```markdown
# Recently Added Learnings

## Last 30 days (8 new learnings)

- 2026-06-12: Race Condition in Shared Cache (Gotcha)
- 2026-06-11: Memoization Technique (Pattern)
- 2026-06-10: React Custom Hook Pattern (Pattern)
  ...

## Last 90 days

...
```

### Step 8: Generate Full-Text Index

**Create .index.json for programmatic search:**

```json
{
  "version": "1.0",
  "generated_at": "2026-06-12T10:30:00Z",
  "total_learnings": 80,

  "by_type": {
    "gotcha": 20,
    "pattern": 30,
    "decision": 15,
    "technical_fix": 10,
    "workflow": 5
  },

  "by_domain": {
    "backend": 40,
    "frontend": 20,
    "security": 15,
    "devops": 5
  },

  "learnings": [
    {
      "id": "uuid-1",
      "slug": "race-condition-cache",
      "type": "gotcha",
      "domain": "backend",
      "title": "Race Condition in Shared Cache",
      "priority": "critical",
      "applicability": { "current_project": 9, "general": 8 },
      "tags": ["typescript", "concurrency", "cache"],
      "keywords": ["race", "condition", "cache", "mutex", "lock"],
      "created_at": "2026-06-12T10:30:00Z",
      "path": "gotcha/2026-06-12-race-condition-cache.md"
    },
    ...
  ],

  "keywords": {
    "race": ["uuid-1", "uuid-5"],
    "cache": ["uuid-1", "uuid-3", "uuid-7"],
    "concurrency": ["uuid-1", "uuid-2"],
    ...
  }
}
```

### Step 9: Generate Structure Artifact

**Emit artifact with:**

- All learnings stored with metadata
- Storage paths and organization strategy
- Index files list
- Full-text index reference
- Navigation structure summary
- Ready flag for next skill

## Storage Organization Examples

### Example: By Type Organization

```
docs/learnings/
├── INDEX.md
├── BY_TYPE.md
├── BY_DOMAIN.md
├── BY_PRIORITY.md
├── BY_APPLICABILITY.md
├── RECENT.md
├── .index.json
│
├── gotcha/
│   ├── 2026-06-12-race-condition-cache.md
│   ├── 2026-06-10-null-pointer-dereference.md
│   └── 2026-06-08-async-callback-timing.md
│
├── pattern/
│   ├── 2026-06-11-memoization-technique.md
│   ├── 2026-06-09-builder-pattern.md
│   └── 2026-06-07-middleware-chain.md
│
└── ...
```

## Error Handling

| Error                           | Recovery                                        |
| ------------------------------- | ----------------------------------------------- |
| Classification artifact invalid | Return error; direct to pwrl-learnings-classify |
| Storage directory missing       | Create docs/learnings/ automatically            |
| Duplicate slug                  | Append -1, -2, etc. to slug; regenerate path    |
| Slug generation fails           | Use UUID as fallback                            |
| Index generation fails          | Create partial indexes; flag for manual review  |
