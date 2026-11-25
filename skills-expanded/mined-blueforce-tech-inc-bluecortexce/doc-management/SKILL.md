---
name: doc-management
description: Systematic documentation placement, archival, and lifecycle management for the project.
requires:
  bins:
    - find
metadata: {"openclaw": {"emoji": "📚"}}
---

# Documentation Management Skill

## Purpose

Every `.md` file has a clear home based on its lifecycle stage. This skill defines where docs go, when to archive them, and how to keep the project navigable.

## When to Activate

Activate this skill when the agent:
- Creates a new `.md` file anywhere in the project
- Moves, renames, or reorganizes documentation
- Completes a task that produced progress reports or test results
- Runs a documentation audit or health check
- Notices stale or duplicate documents
- Reviews a PR that adds or moves `.md` files
- Before `git commit` that includes `.md` changes

## Quick Reference

```
Component README?        → <component>/README.md
Project-essential file?  → Root (allowlist only — see Rule 5)
One-time snapshot?       → docs/archive/YYYY-MM-DD_<name>.md
Actively iterated?       → docs/drafts/<name>.md
Periodically updated?    → appropriate dir + purpose header (mandatory)
Stable reference?        → docs/<name>.md
```

## Directory Map

```
project-root/
├── docs/
│   ├── archive/              # Historical snapshots (read-only)
│   │   └── README.md         # Index: date, origin path, description
│   ├── drafts/               # Active design docs under iteration
│   └── *.md                  # Stable reference docs
├── *.md                      # Root: allowlist only (see Rule 5)
├── backend/README.md         # Component README (allowed)
├── proxy/README.md           # Component README (allowed)
├── examples/*/README.md      # Example project README (allowed)
├── go-sdk/*/README.md        # SDK README (allowed)
├── scripts/README.md         # Scripts README (allowed)
├── .agents/skills/*/SKILL.md # Project-local skill definitions (allowed)
├── openclaw-plugin/skills/*/SKILL.md  # Plugin skill (allowed)
└── memory/*.md               # Agent memory (.gitignored)
```

## Rules

### Rule 1: Classify Before Creating

Before creating ANY `.md` file, classify it:

| Type | Lifecycle | Location |
|------|-----------|----------|
| **Live** | Periodically overwritten | Appropriate dir + purpose header |
| **Historical** | Written once, never changed | `docs/archive/YYYY-MM-DD_<name>.md` |
| **Draft** | Actively iterated | `docs/drafts/<name>.md` |
| **Reference** | Stable, updated with releases | `docs/<name>.md` |
| **Component README** | Tied to a component | `<component>/README.md` |
| **Root** | Project-essential | `./<name>.md` |

### Rule 2: Live Documents Must Have a Purpose Header

Every document that gets periodically updated MUST include this header immediately after the title:

```markdown
# Title

> **Purpose**: What this document tracks.
> **Updated by**: Who/what updates it (cron ID, manual process, etc.).
> **Update rule**: How it changes (overwrite with latest / append entries).
```

This header is mandatory. No exceptions.

### Rule 3: Archive, Don't Delete

When a document's content becomes a historical record:

1. Identify the last-relevant date for the content
2. Copy to `docs/archive/YYYY-MM-DD_<descriptive-name>.md`
   - `YYYY-MM-DD` = last-relevant date (not today's date)
   - `<descriptive-name>` = lowercase, hyphens, clear description
3. Add a row to `docs/archive/README.md`:
   ```
   | `YYYY-MM-DD_<name>.md` | `<original-path>` | YYYY-MM-DD | <brief description> |
   ```
4. Remove the original file
5. Check if any remaining docs reference the archived file's path — update those references

**Archive size**: If `docs/archive/` exceeds 30 files, review whether any very old entries can be removed (they remain in git history regardless).

**When to archive a draft**: When the feature it describes is fully implemented AND the design is no longer referenced for active work. If the draft still contains design rationale useful for future reference, promote it to `docs/` instead of archiving.

### Rule 4: No Duplicate Purpose

Before creating a new file, ask: "Does a file already exist for this purpose?"
- **Yes** → Update it in place (live docs) or create a new archive entry (historical)
- **No** → Create the file in the correct location per Rule 1

Never have two files tracking the same thing.

### Rule 5: Root Directory Is Sacred

Only these files may live in the project root:

| File | Status | Notes |
|------|--------|-------|
| `README.md` | Required | Project overview |
| `README-zh-CN.md` | Optional | Chinese version |
| `CHANGELOG.md` | Required | Release history |
| `CONTRIBUTING.md` | Optional | Contribution guide |
| `CODE_OF_CONDUCT.md` | Optional | Community standards |
| `SECURITY.md` | Optional | Security policy |
| `RELEASE.md` | Optional | Release process |
| `DOCKER_README.md` | Optional | Docker quick-start (when docker-compose.yml at root) |
| `CLAUDE.md` | Optional | Claude Code config |
| `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `TOOLS.md` | OpenClaw | Agent config |
| `HEARTBEAT.md`, `MEMORY.md` | Agent | `.gitignored` memory |
| `docker-compose.yml`, `Dockerfile`, etc. | Infra | Non-`.md` files OK |

**Everything else** → `docs/`, `docs/drafts/`, or `docs/archive/`.

### Rule 6: Language Consistency

- Reference docs: Maintain paired versions — `<name>.md` (English) + `<name>-zh-CN.md` (Chinese)
- Updating a doc with only one language version: update it as-is; note in commit that counterpart is missing
- Drafts: Any language; clarity matters most
- Archive: Keep original language; do not translate
- Code comments: English preferred

### Rule 7: Draft Naming Convention

Draft filenames should describe their content, not their tracking function. Use one of these patterns:

| Pattern | When to use | Example |
|---------|-------------|---------|
| `<topic>-<type>.md` | General design/research | `go-sdk-design.md`, `mcp-transport-analysis.md` |
| `<phase>-<N>-<topic>.md` | Phased implementation | `phase-3-extraction-design.md` |
| `<component>-<topic>.md` | Component-specific | `spring-ai-integration-plan.md` |

Where `<type>` is: `design`, `analysis`, `research`, `plan`, `walkthrough`, `guide`, `review`.

| ❌ Bad | ✅ Good | Why |
|--------|---------|-----|
| `TASK_PROGRESS.md` | `go-sdk-implementation.md` | Describes content, not function |
| `NOTES.md` | `phase-3-extraction-design.md` | Specific, searchable |
| `TEMP.md` | `mcp-transport-analysis.md` | Has a clear subject |

### Rule 8: No Ephemeral Files in the Repo

Do not commit scratch notes, temporary debugging logs, or throwaway files. If it's worth writing down, it's worth placing correctly per Rule 1. If it's truly temporary, use commit messages or terminal output instead.

Agent memory files (`HEARTBEAT.md`, `MEMORY.md`, `memory/*.md`) are `.gitignored` by design. Never `.gitignore` anything under `docs/` — those are project artifacts.

## Principle: Findability

When placing a document, ask: "If someone needs this in 3 months, where would they look first?"
- API docs → `docs/API.md` (obvious)
- Deployment → `docs/DEPLOYMENT.md` (obvious)
- Performance results → `docs/performance-test-results.md` (with purpose header)
- Design for an in-progress feature → `docs/drafts/<feature>-design.md`

The correct location is the one that maximizes findability for future readers.

## Draft Lifecycle

```
Created → Iterated → Implemented → Decision point
                                           ├─ Still useful as reference? → Promote to docs/
                                           └─ No longer needed?          → Archive to docs/archive/
```

**Signs a draft should be archived or promoted**:
- Feature fully implemented and tested
- Design stable for 2+ weeks without changes
- New contributors would find the final `docs/` version more useful

## Real-World Example

**Before** (the problem this skill prevents):
```
./TASK_TRACKER.md                          # Completed 2026-02-13, forgotten
./performance-test-results.md              # Duplicate of docs/ version
./backend/TASK_PROGRESS.md                 # Completed 2026-02-12, forgotten
./backend/TEST_REPORT.md                   # Historical snapshot, not updated
./reviews/code-review-2026-02-12.md        # Old review, never cleaned up
./docs/drafts/TASK_PROGRESS.md             # Completed task in drafts
./docs/drafts/implementation-progress.md   # Completed, never archived
./RELEASE_DRAFT.md                         # Already released as v0.1.0
```

**After** (applying this skill):
```
./docs/archive/2026-02-12_code-review-v1.md
./docs/archive/2026-02-12_code-review-fix-progress.md
./docs/archive/2026-02-13_task-tracker-webui-complete.md
./docs/archive/2026-02-13_comprehensive-test-report.md
./docs/archive/2026-03-13_v0.1.0-beta-release-draft.md
./docs/archive/2026-03-17_evo-memory-implementation-progress.md
./docs/archive/2026-03-18_spring-ai-integration-progress.md
./docs/archive/2026-03-20_go-java-sdk-implementation-progress.md
./docs/archive/README.md                   # Index of all archived docs
./docs/performance-test-results.md         # Single live copy with purpose header
```

11 scattered files → 1 organized archive with index.

## Audit Checklist

Run before major commits, or when documentation feels disorganized.

**Step 1** — Scan:
```bash
find . -name "*.md" \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/target/*" \
  -not -path "*/.mvn/*" \
  -not -path "*/memory/*" \
  | sort
```

**Step 2** — Verify each file:

- [ ] Correct location per Rule 1?
- [ ] If live: has purpose header per Rule 2?
- [ ] No duplicate purpose file?
- [ ] If completed tracker in `docs/drafts/`: archived?
- [ ] `docs/archive/README.md` table current?
- [ ] If stale: has archive entry?
- [ ] If in root: on the Rule 5 allowlist?
- [ ] Draft filenames descriptive per Rule 7?

**Step 3** — Report:
- All pass → "Documentation health OK"
- Issues found → List each violation with its file path, then fix per Common Violations table

## Common Violations

| Violation | Correct Action |
|-----------|---------------|
| `backend/TASK_PROGRESS.md` for a new task | Use `docs/drafts/<descriptive-name>.md` |
| Test report in `backend/` or root | Archive to `docs/archive/YYYY-MM-DD_test-report.md` |
| Completed progress in `docs/drafts/` | Archive to `docs/archive/YYYY-MM-DD_<name>.md` |
| Duplicate file for same data | Keep one, delete/archive the other |
| Temporary notes in root | Move to `docs/drafts/` or delete |
| Live doc missing purpose header | Add header per Rule 2 |
| Root `.md` not in allowlist | Move to `docs/` |
| Draft never archived after completion | Archive or promote per Draft Lifecycle |
| Vague draft name (`NOTES.md`, `TEMP.md`) | Rename per Rule 7 |
| Archived file still referenced elsewhere | Update references per Rule 3 step 5 |
