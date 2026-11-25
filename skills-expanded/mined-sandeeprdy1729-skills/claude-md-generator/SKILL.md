---
name: claude-md-generator
description: >
  Self-healing CLAUDE.md generator and maintenance skill. Activates when the user
  wants to create, update, audit, or repair CLAUDE.md files for a project — or when
  Claude has just made a mistake that a CLAUDE.md entry could have prevented.
  Scans the codebase for build commands, test runners, file conventions, environment
  setup, and project-specific gotchas. Generates a root CLAUDE.md (≤50 lines) with
  progressive disclosure into subfolder CLAUDE.md files. Detects missing-context gaps
  and patches them automatically after each mistake.
  Use when user says: generate CLAUDE.md, create CLAUDE.md, update CLAUDE.md, fix
  CLAUDE.md, Claude keeps forgetting, re-teaching Claude, Claude made a mistake again,
  document my project for Claude, capture this pattern, add this to CLAUDE.md, Claude
  doesn't know about, write project context, persistent context, memory for Claude,
  project instructions.
  Do NOT activate for: general documentation requests unrelated to Claude context,
  README generation, API docs, code comments.
  First response: "CLAUDE.md Generator active. I'll scan your project and generate
  context files Claude actually needs. Share your project root or describe what
  Claude keeps getting wrong."
license: Apache 2.0
---

# Self-Healing CLAUDE.md Generator

Users on HN describe re-teaching Claude "how to curl" every morning. Every session,
the same build command, the same test runner flags, the same "don't use X, we use Y"
correction — over and over. This skill captures those patterns once, writes them to
disk, and patches the files automatically when a new gap is discovered.

The output is not a massive documentation dump. It is the minimal, highest-signal
context that prevents Claude from making the mistakes it actually makes in this project.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/scan [path]` | Scan a directory tree and extract all detectable patterns |
| `/generate` | Generate a full CLAUDE.md file set from scan results |
| `/patch "<what went wrong>"` | Given a mistake description, add the missing entry |
| `/audit` | Read existing CLAUDE.md files and identify gaps, bloat, and stale entries |
| `/diff` | Compare the current CLAUDE.md against what a fresh scan would generate |
| `/promote <subfolder>` | Move a buried subfolder entry up to the root if it's high-frequency |
| `/demote <entry>` | Move a root entry to the relevant subfolder to reduce root size |
| `/trim` | Remove entries that haven't prevented a mistake in ≥30 days (with confirmation) |
| `/explain <entry>` | Show why a specific entry was added (trace to the originating gap) |
| `/reset` | Regenerate the entire file set from a fresh scan, discarding manual edits |
| `/completeness` | Score context completeness 0–10; show what's missing and how much each gap costs |
| `/gaps-remaining` | Sorted list of remaining context gaps by mistake frequency (highest pain first) |
| `/drill <category>` | Deep-dive one gap category with exhaustive coverage — don't stop at the obvious |
| `/iterate` | Scan → patch → score → repeat until completeness ≥ 8/10 |

---

## HIGH-LEVEL WORKFLOW

```text
Trigger: user asks for CLAUDE.md, or Claude just made a mistake
    │
    ├─ Phase 1: Scan
    │     Walk the project tree; extract build, test, conventions, env, gotchas
    │
    ├─ Phase 2: Gap Detection
    │     Compare extracted patterns against existing CLAUDE.md content
    │     Identify what is missing, stale, or mis-placed
    │
    ├─ Phase 3: Structure Planning
    │     Assign each entry to root or a subfolder file
    │     Enforce root ≤50 lines, progressive disclosure rules
    │
    ├─ Phase 4: Generation / Patch
    │     Write new entries; preserve manually written content
    │     Add provenance comments for every generated entry
    │
    ├─ Phase 5: Validation
    │     Verify root line count, no duplicate entries, no dead references
    │     Confirm every subfolder file is reachable from root
    │
    └─ Phase 6: Completeness Score + Next Gap
          Score 0–10; surface the single highest-impact gap still open
          End every session with: "Completeness: X/10. Next gap to close: [gap]."
```

---

## PHASE 1 — SCAN

Walk the project tree and collect evidence for each pattern category. Do not require
the user to describe patterns — infer them from the files present.

### Pattern Categories

#### 1. Build & Run

Scan for build commands by reading (in order of confidence):

| Source | What to extract |
| --- | --- |
| `package.json` → `scripts` | `build`, `start`, `dev`, `preview` commands |
| `Makefile` | All targets with short descriptions |
| `Dockerfile` / `docker-compose.yml` | Service names, port mappings, build args |
| `Cargo.toml` | `[profile]` settings, workspace members |
| `pyproject.toml` / `setup.py` | Build backend, entry points |
| `build.gradle` / `pom.xml` | Main build targets |
| `.github/workflows/*.yml` | CI build steps (authoritative — CI always works) |
| `justfile` | All recipes |
| `README.md` → `## Getting Started` section | Manual fallback |

Output: a deduplicated list of `<command>: <what it does>` pairs.

#### 2. Test Patterns

| Source | What to extract |
| --- | --- |
| `package.json` → `scripts.test` | Test command and flags |
| `jest.config.*` / `vitest.config.*` | Test file patterns, timeout, coverage threshold |
| `pytest.ini` / `pyproject.toml [tool.pytest]` | Test directory, markers, fixture paths |
| `.github/workflows/` | Test job steps — captures the exact flags CI uses |
| `Makefile` target `test` | Command CI actually runs |
| `go.mod` presence | Assume `go test ./...` |

Special attention: extract **flags that are always passed** (e.g. `--run-in-band`,
`-p 1`, `--no-cache`). These are the flags users have to re-explain every session.

#### 3. File & Folder Conventions

| Signal | Pattern to record |
| --- | --- |
| Consistent casing in filenames | `kebab-case`, `PascalCase`, `snake_case` |
| Barrel files (`index.ts`) in component directories | Export pattern |
| Co-located test files (`*.test.ts` next to source) vs dedicated `__tests__/` | Test location rule |
| Migration files with timestamp prefix | Naming convention + how to create one |
| Feature-flag files | Where they live, how to add one |
| Generated files (`.generated.ts`, `*.g.dart`) | Do not edit these |
| Monorepo structure | Package names and their responsibilities |

#### 4. Environment & Setup

| Source | What to extract |
| --- | --- |
| `.env.example` | All required env vars and their purpose |
| `docker-compose.yml` | Local service dependencies (DB, cache, queue) |
| `README.md` → Prerequisites / Installation | Node/Python/Go version requirements |
| `.nvmrc` / `.python-version` / `rust-toolchain` | Exact runtime version |
| `scripts/setup.sh` or `scripts/bootstrap.sh` | One-time setup steps |

#### 5. Architecture & Gotchas

Infer from file structure and naming:

| Signal | Entry to generate |
| --- | --- |
| `src/api/` + `src/services/` + `src/repositories/` | Three-layer architecture note |
| `migrations/` present | Never hand-edit migrations; use `make migration name=X` |
| `generated/` or `__generated__/` directories | Auto-generated — do not edit |
| Multiple config files for same tool | Note which one is authoritative |
| `// @deprecated` comments in key files | Flag the deprecated path |
| Monorepo with shared packages | Cross-package import rules |
| Husky / lint-staged present | Pre-commit hook summary |
| `.cursorrules` or `.clinerules` already present | Parse these for existing project rules |

---

## PHASE 2 — GAP DETECTION

Run after a scan or when the user describes a mistake.

### Automated Gap Detection (post-scan)

Compare the scan output against the existing CLAUDE.md content:

1. For each detected pattern, search the existing CLAUDE.md for the key concept.
2. If absent → gap. If present but different → drift (stale entry).
3. Compute a **coverage score**: `patterns_covered / patterns_detected` (0–100%).

| Score | Status |
| --- | --- |
| ≥80% | Well-documented |
| 50–79% | Partially documented — gaps exist |
| <50% | Under-documented — high mistake risk |

### Mistake-Driven Gap Detection (triggered by `/patch`)

When the user describes a mistake Claude just made, extract the missing entry:

**Input:** natural language description of the mistake.

```
"Claude ran `npm test` with no flags and it hung because our test suite
requires --testTimeout=30000 for the integration tests."
```

**Extraction process:**

1. **Identify the mistake category** from the taxonomy below.
2. **Extract the correct behaviour** as a one-sentence imperative.
3. **Identify the scope** — is this a root-level entry (affects whole project) or
   a subfolder entry (affects one package or layer)?
4. **Write the patch entry** with provenance comment.

**Mistake category taxonomy:**

| Code | Category | Example mistake |
| --- | --- | --- |
| `M1` | Wrong command | Running `npm run build` when `make build` is correct |
| `M2` | Missing flag | Running `pytest` without `-x --tb=short` |
| `M3` | Wrong file | Editing a generated file instead of its source |
| `M4` | Wrong location | Creating a component in `src/` instead of `src/features/` |
| `M5` | Missing setup step | Forgetting `docker compose up -d` before running tests |
| `M6` | Deprecated path | Using the old `src/utils/api.ts` instead of `src/lib/client.ts` |
| `M7` | Convention violation | Using `snake_case` filenames in a `kebab-case` project |
| `M8` | Architecture violation | Calling a repository directly from a controller |
| `M9` | Env var assumption | Assuming `DATABASE_URL` exists without `.env.example` check |
| `M10` | Scope creep | Editing files in `packages/shared` when task is in `packages/app` |

---

## PHASE 3 — STRUCTURE PLANNING

Assign each entry to the correct file before writing anything.

### Progressive Disclosure Rules

**Root `CLAUDE.md`** (hard limit: 50 lines):

Include only:
- The single most important build command
- The single most important test command
- 3–5 project-wide gotchas that affect all work
- A reference list to all subfolder CLAUDE.md files

Never include in root:
- Per-package details
- Full env var lists (link to `.env.example` instead)
- Anything that only applies to one subfolder
- Explanations longer than 1 sentence

**Subfolder `CLAUDE.md` files**:

Create one per area where context differs meaningfully from the root:

| Subfolder | Typical content |
| --- | --- |
| `packages/<name>/CLAUDE.md` | Package-specific build, test, import rules |
| `src/api/CLAUDE.md` | API layer conventions, auth patterns, error handling |
| `src/db/CLAUDE.md` | Migration commands, ORM patterns, query conventions |
| `src/components/CLAUDE.md` | Component structure, styling conventions, a11y rules |
| `infra/CLAUDE.md` | Terraform/Pulumi commands, environment map, deploy flow |
| `scripts/CLAUDE.md` | What each script does, when to run it |
| `.github/CLAUDE.md` | CI pipeline structure, how to add a new workflow |

**Placement algorithm:**

```text
For each new entry:
  1. Does it affect every directory in the project?
     Yes → root, if root has room (< 50 lines after addition)
     Yes but root is full → root summary line + subfolder detail
  2. Does it affect only one subfolder?
     Yes → subfolder CLAUDE.md
  3. Does it affect 2–3 subfolders?
     Yes → create a shared parent CLAUDE.md or add to root if brief
```

### Root File Template

```markdown
# CLAUDE.md

## Build & Run
<one line: primary command to build/start the project>

## Test
<one line: exact test command including all required flags>

## Key Conventions
- <convention 1 — one sentence>
- <convention 2 — one sentence>
- <convention 3 — one sentence>

## Gotchas
- <gotcha 1 — one sentence: what to do instead of the wrong thing>
- <gotcha 2 — one sentence>

## Subfolders
- [src/api/](src/api/CLAUDE.md) — <one-line description>
- [src/db/](src/db/CLAUDE.md) — <one-line description>
- [packages/](packages/CLAUDE.md) — <one-line description>
```

---

## PHASE 4 — GENERATION / PATCH

### Writing New Files

When generating from scratch:

1. Write the root file first.
2. Write each subfolder file.
3. Add a provenance comment above every generated section:

```markdown
<!-- generated: claude-md-generator · scan · 2026-05-19 -->
```

4. Add an edit instruction at the top of every generated file:

```markdown
<!-- Manual edits are preserved on regeneration. To reset: /reset -->
```

### Patching Existing Files

When adding an entry to an existing file:

1. Search the file for the relevant section heading.
2. If the section exists, append the entry under it with a provenance comment.
3. If the section does not exist, add a new section at the bottom.
4. Never delete or reorder manually written content.
5. Never add duplicate entries (check before writing).

**Patch entry format:**

```markdown
<!-- patched: claude-md-generator · M2 missing-flag · 2026-05-19 -->
- Always run `pytest -x --tb=short --timeout=30` — the bare `pytest` command
  hangs on integration tests.
```

### Provenance Tracking

Every generated or patched entry carries a comment:

```
<!-- source: <how it was detected> · <category code> · <date> -->
```

| Source value | Meaning |
| --- | --- |
| `scan` | Detected automatically from project files |
| `patch` | Added after a reported mistake |
| `manual` | Written by the user directly (never overwrite) |
| `promoted` | Moved up from a subfolder via `/promote` |
| `demoted` | Moved down from root via `/demote` |

---

## PHASE 5 — VALIDATION

Before presenting the output, run these checks:

| Check | Condition | Fix |
| --- | --- | --- |
| Root line count | Root CLAUDE.md ≤ 50 lines | Move lowest-priority entries to subfolders |
| No duplicate entries | No two entries have >80% text overlap | Remove the less-specific one |
| No dead subfolder links | Every `[subfolder/](subfolder/CLAUDE.md)` link resolves | Remove or create the file |
| No stale commands | Detected commands match commands referenced in CLAUDE.md | Update diverged entries |
| No broken paths | All file paths mentioned exist | Flag with `[VERIFY]` tag |
| Provenance on every entry | Every generated/patched entry has a `<!-- ... -->` comment | Add missing comments |

### Validation Report Format

```text
CLAUDE.MD VALIDATION
────────────────────────────────────────────────────────────
  Root CLAUDE.md        : 34 / 50 lines  [PASS]
  Subfolder files       : 4 files
  Duplicate entries     : 0              [PASS]
  Dead links            : 1              [WARN] src/legacy/CLAUDE.md not found
  Stale commands        : 1              [WARN] build command diverges from Makefile
  Broken paths          : 0              [PASS]
  Entries with no source: 2              [INFO] manually written — preserved
────────────────────────────────────────────────────────────
  Coverage score        : 74%  (partially documented)
  Gaps detected         : 6
  Top gap               : test flags (--timeout, --run-in-band) not documented
────────────────────────────────────────────────────────────
```

---

## COVERAGE SCORING

Run `/audit` on any project to get:

```text
CLAUDE.MD COVERAGE AUDIT
────────────────────────────────────────────────────────────
  Patterns detected     : 31
  Patterns documented   : 23  (74%)
  ─────────────────────────────────────────────────────────
  DOCUMENTED
    ✓ Primary build command (package.json → scripts.build)
    ✓ Test runner (jest)
    ✓ Node version (.nvmrc → 20.11.0)
    ✓ Docker services (docker-compose.yml → postgres, redis)
    ✓ Migration command (Makefile → make migration)
    … 18 more

  GAPS (8)
    ✗ Test flags  — jest.config.js has testTimeout: 30000 but CLAUDE.md
                    says nothing about timeout
    ✗ Generated files — src/generated/ exists but no "do not edit" note
    ✗ Env var DATABASE_URL — in .env.example but not documented
    ✗ Pre-commit hook — husky installed, no mention in CLAUDE.md
    ✗ Barrel files — src/components/index.ts pattern undocumented
    ✗ Lint command — eslint script in package.json, no entry
    ✗ Feature flag location — src/flags/ detected, no convention note
    ✗ API versioning — src/api/v1/ and src/api/v2/ found, no routing note

  ACTION: run /generate to fill all 8 gaps
────────────────────────────────────────────────────────────
```

---

## SELF-HEALING MECHANISM

The "self-healing" loop works in four steps:

```text
Step 1: Claude makes a mistake in a project with CLAUDE.md
Step 2: User describes the mistake to this skill: /patch "Claude did X, should do Y"
Step 3: Skill extracts the missing entry, assigns it to the right file and section,
        writes the patch with a provenance comment
Step 4: On the next session, Claude reads the patched CLAUDE.md and does not repeat
        the mistake
```

This is not magic — it is a systematic pipeline from observed error to documented fix.
The skill does not auto-commit. Every patch is shown to the user for review before
writing. After confirmation, the file is updated in place.

### Patch Workflow

User input: `/patch "Claude ran npm test instead of make test and it failed"`

Skill output:

```text
PATCH PLAN
─────────────────────────────────────────────────────────
  Mistake category : M1 — wrong command
  Missing entry    : Test command is `make test`, not `npm test`
  Target file      : CLAUDE.md (root)
  Target section   : ## Test
  Current content  : (section absent)
  ─────────────────────────────────────────────────────
  PROPOSED PATCH

  ## Test
  <!-- patched: claude-md-generator · M1 wrong-command · 2026-05-19 -->
  Always use `make test` — the `npm test` script is a stub that exits 0
  without running anything.

  ─────────────────────────────────────────────────────
  Root after patch : 18 / 50 lines  [PASS]
  Confirm? [yes / no / edit]
─────────────────────────────────────────────────────
```

---

## `/diff` OUTPUT FORMAT

Shows what a fresh scan would change versus the current CLAUDE.md:

```text
CLAUDE.MD DIFF
────────────────────────────────────────────────────────────
  + ADDITIONS (6 entries the scan found, not in CLAUDE.md)
    + [root] Test: jest --testTimeout=30000 --runInBand
      Source: jest.config.js testTimeout + package.json scripts.test:ci
    + [root] Gotcha: src/generated/ is auto-generated — do not edit
      Source: src/generated/ directory + .gitattributes linguist-generated
    + [src/db/] Migration: make migration name=<description>
      Source: Makefile target 'migration' + migrations/ directory
    + [src/db/] ORM: Prisma — schema at prisma/schema.prisma
      Source: prisma/ directory + package.json dependency
    + [src/api/] Versioning: v1 is deprecated; new endpoints go in v2
      Source: src/api/v1/ has @deprecated JSDoc · src/api/v2/ is active
    + [.github/] CI: push to main triggers deploy-staging; PR only runs tests
      Source: .github/workflows/deploy.yml trigger conditions

  ~ DRIFTED (2 entries that exist but are out of date)
    ~ [root] Build: was `npm run build` → should be `make build`
      Source: package.json scripts.build removed; Makefile build target added
    ~ [root] Node version: was 18 → .nvmrc now specifies 20.11.0

  - REMOVALS (1 entry that no longer applies)
    - [root] Gotcha: avoid src/utils/api.ts (deprecated)
      Source: src/utils/api.ts deleted in codebase

────────────────────────────────────────────────────────────
  Run /generate to apply all changes.  Run /patch for individual entries.
```

---

## MULTI-PACKAGE MONOREPO SUPPORT

For monorepos (detected by presence of `packages/`, `apps/`, `libs/`, or
`pnpm-workspace.yaml`):

### File Structure

```text
CLAUDE.md                   ← root: workspace-level only (≤50 lines)
packages/
  CLAUDE.md                 ← package naming, cross-package import rules
  ui/
    CLAUDE.md               ← component conventions, storybook, a11y
  api/
    CLAUDE.md               ← endpoint conventions, auth, error handling
  shared/
    CLAUDE.md               ← what lives here, import rules, change policy
apps/
  web/
    CLAUDE.md               ← next.js specifics, env vars, deploy target
  mobile/
    CLAUDE.md               ← expo/rn specifics, native module notes
```

Root CLAUDE.md for a monorepo:

```markdown
# CLAUDE.md

## Workspace
pnpm monorepo. Install: `pnpm install`. Never use `npm` or `yarn`.

## Build
`pnpm build` — builds all packages in dependency order.
`pnpm --filter <name> build` — builds a single package.

## Test
`pnpm test` — runs all test suites.
`pnpm --filter <name> test` — single package.

## Key Conventions
- Cross-package imports must go through the package's public index, not deep paths.
- Changes to `packages/shared` affect all consumers — check dependents before merging.

## Subfolders
- [packages/](packages/CLAUDE.md) — package list, cross-package rules
- [apps/web/](apps/web/CLAUDE.md) — Next.js app specifics
- [apps/mobile/](apps/mobile/CLAUDE.md) — Expo app specifics
- [infra/](infra/CLAUDE.md) — deployment, environment map
```

---

## INTERACTION WITH EXISTING FILES

Users often have hand-written CLAUDE.md files. The skill never overwrites manual content.

### Merge Strategy

| Existing content type | Action |
| --- | --- |
| `<!-- manual -->` comment | Never touch — skip on regeneration |
| No provenance comment | Treat as manual — preserve, do not overwrite |
| `<!-- generated: ... -->` comment | Safe to update if scan detects drift |
| `<!-- patched: ... -->` comment | Safe to update if the underlying pattern changes |
| Empty file | Generate from scratch |
| File does not exist | Create with generated content |

### Conflict Resolution

If a generated entry contradicts an existing manual entry:

```text
CONFLICT DETECTED
─────────────────────────────────────────────────────────
  Entry    : Build command
  Existing : `npm run build`  (no provenance — treated as manual)
  Scanned  : `make build`  (from Makefile + CI workflow)
  ─────────────────────────────────────────────────────
  The scanned value differs from the existing entry.
  Since the existing entry has no provenance comment, it is treated as manual.

  Options:
  [1] Keep existing `npm run build` (skip this entry)
  [2] Replace with `make build` (add generated provenance)
  [3] Keep both with a note: "npm run build is deprecated; use make build"
─────────────────────────────────────────────────────────
```

---

## BEHAVIOUR RULES

- **Never exceed 50 lines in root `CLAUDE.md`.** If a new entry would push root over
  50 lines, automatically plan a demotion of the lowest-priority existing root entry.
- **Patch is not commit.** Every write to disk is shown for review first. The skill
  never silently modifies files.
- **Preserve all manual content.** Content without a generated/patched provenance
  comment is never deleted, moved, or rewritten.
- **One entry, one sentence.** Every entry in a CLAUDE.md must be actionable in a
  single sentence. Multi-sentence entries belong in a linked subfolder file.
- **Commands must be exact.** Never write a command entry with a placeholder unless
  the placeholder is clearly marked (e.g. `make migration name=<description>`).
- **Track the source.** Every entry must have a provenance comment. An undocumented
  entry cannot be validated, diffed, or pruned.
- **Always show coverage score.** Every `/scan`, `/audit`, and `/generate` must report
  the before/after coverage percentage.
- **Do not duplicate README content.** If the README already documents a pattern
  accurately, link to it from CLAUDE.md rather than copying the text.

---

## EXAMPLES

### Example: generating from scratch

> User: "I have a new Next.js monorepo. Generate CLAUDE.md for it."

```text
Scanning: package.json · pnpm-workspace.yaml · .nvmrc · Makefile ·
          .github/workflows/ · .env.example · packages/ · apps/

Detected 24 patterns across 6 categories.
Coverage score before: 0% (no existing CLAUDE.md)

Plan:
  root CLAUDE.md          → 31 lines (well under 50)
  packages/CLAUDE.md      → 18 lines
  apps/web/CLAUDE.md      → 22 lines
  apps/mobile/CLAUDE.md   → 14 lines

Generating…
  ✓ CLAUDE.md (31 lines)
  ✓ packages/CLAUDE.md
  ✓ apps/web/CLAUDE.md
  ✓ apps/mobile/CLAUDE.md

Coverage score after: 79% (19 / 24 patterns documented)
5 patterns require manual input to document — run /audit to see them.
```

### Example: `/patch` after a mistake

> User: `/patch "Claude edited prisma/migrations/ directly instead of running
> make migration name=add-user-roles"`

```text
Mistake category : M3 — wrong file (editing generated/managed file)
Target file      : src/db/CLAUDE.md  (prisma-related)
Target section   : ## Migrations

PROPOSED PATCH
<!-- patched: claude-md-generator · M3 wrong-file · 2026-05-19 -->
Never edit files in prisma/migrations/ directly.
To create a migration: `make migration name=<description>`
The Makefile target runs prisma migrate dev and names the file correctly.

Root impact: none (subfolder entry)
Confirm? [yes / no / edit]
```

### Example: `/trim` output

```text
TRIM CANDIDATES (entries with no confirmed mistake prevention in 30+ days)
────────────────────────────────────────────────────────────
  [root] "Use Node 18" — .nvmrc now specifies 20.11.0 (STALE)
  [src/api/] "v1 auth uses JWT, v2 uses sessions" — v1 deleted 14 days ago (STALE)
  [packages/] "lodash is banned, use native Array methods" — lodash removed from
               all package.json files 45 days ago (probably obsolete)
────────────────────────────────────────────────────────────
  Confirm removal of 3 entries? This cannot be undone without /reset.
  [yes / no / review-each]
```

---

## COMPLETENESS SCORING

Every `/scan`, `/audit`, `/generate`, and `/patch` must end with a completeness score.

```text
COMPLETENESS: 6/10
─────────────────────────────────────────────────────────
  HIGH IMPACT GAPS (fix these first)
    ✗ [score: 9] Test command — Claude will get this wrong on every session
    ✗ [score: 8] Env var setup — missing DATABASE_URL causes silent failures
    ✗ [score: 7] Generated file list — Claude will edit auto-generated files

  MEDIUM IMPACT GAPS
    ✗ [score: 5] Code style config — linting rules undocumented
    ✗ [score: 4] Feature flag location — guessable but not confirmed

  → Run /drill [category] to go deep on any gap.
  → Run /iterate to close all HIGH IMPACT gaps automatically.
─────────────────────────────────────────────────────────
```

**`/iterate` cycle:**

```
1. /completeness   → score the current state
2. /drill [top gap] → close the highest-impact gap with exhaustive coverage
3. /completeness   → re-score
4. repeat until score ≥ 8/10
```

Stop the cycle and report final score when 8/10 is reached or no high-impact gaps remain.
