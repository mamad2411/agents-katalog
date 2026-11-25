---
name: cli-cycle
metadata:
  author: clement
description: "Continuous improvement cycle — orchestrates all cli-* skills on the current project, synthesizes results, and proposes prioritized improvements. Use when the user wants a full project review, a health check, a weekly cycle, or says 'audit everything', 'review the project', 'health check', 'what should I improve', 'run all audits', 'cycle', 'improvement cycle'. Designed for recurring use with '/loop 7d /cli-cycle'."
argument-hint: "[project-path-or-scope-directory]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Agent
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.

> **Language rule:** Skill instructions are written in English. When generating user-facing output (reports, files, documentation), detect the project's primary language (from README, comments, docs, commit messages) and produce the output in that language. If the project is bilingual, ask the user which language to use before proceeding.

# Cycle — Phoenix Continuous Improvement

> *"The phoenix does not die — it burns what is impure and is reborn stronger.
> Each cycle consumes the flaws. When there is nothing left to burn, the project is born."*

Run every applicable `cli-*` skill on the current project, collect results, deliver the **complete** list of corrections in 3 tiers, and loop until clean.

## Core Principles

1. **You don't duplicate logic — you delegate.** Each sub-agent reads the real SKILL.md and follows its instructions. You orchestrate, collect, and judge.
2. **Show everything.** Never truncate the correction list. The user sees ALL issues, organized by severity.
3. **Phoenix loop.** Audit → user fixes → re-audit → repeat until convergence.
4. **Autonomous convergence.** When invoked with `--converge`, run the entire loop in an isolated worktree, then present a single unified plan. Read `references/convergence.md` for the full algorithm.
5. **Flow graph.** Skills form a DAG: audit detects → forge corrects → git commits → re-audit verifies. No cycles allowed. Read `references/skill-flow.md` for the complete trigger graph, deduplication rules, and cycle detection.

**Gotchas** — read `../gotchas.md` before producing output to avoid known mistakes.

## Workflow

### Step 0.5 — Determine scope

`$ARGUMENTS` can be:
- **Empty or project root** → full project audit (all directories, all skills)
- **A subdirectory** (e.g., `src/features/dlp/`) → **scoped audit** (vertical slice)

**Scoped audit rules:**
1. Only scan files within the scope directory (and its subdirectories)
2. Pass the scope directory as `$ARGUMENTS` to every sub-agent: `/cli-audit-code {scope}`, `/cli-audit-test {scope}`, etc.
3. Skills that don't accept a directory scope (e.g., `cli-forge-pipeline`, `cli-forge-github`) are **skipped** — they are project-wide by nature
4. The scorecard, triage, and report are titled with the scope: `# Cycle — {project} / {scope}`
5. Co-located tests are detected within the scope: `{scope}/**/test*`, `{scope}/**/*_test.*`, `{scope}/**/tests/`
6. Co-located docs are detected within the scope: `{scope}/**/*.md`, `{scope}/**/README*`

**Applicability in scoped mode:**

| Skill | Scoped? | Why |
|---|---|---|
| `cli-audit-code` | ✅ | Scans only the slice's code |
| `cli-audit-xray` | ✅ if scope has source code and optimization/dataflow signals | Scans semantic/resource-flow candidates within the slice |
| `cli-audit-data` | ✅ if scope has SQLx/PostgreSQL code or migrations | Audits persistent invariants, transactions, concurrency, and schema evolution |
| `cli-audit-doc` | ✅ | Scans only the slice's docs |
| `cli-audit-test` | ✅ | Scans only the slice's tests |
| `cli-audit-tangle` | ✅ | Analyzes call graph within the slice |
| `cli-audit-drift` | ✅ if scope has CONTRACTS.md entries | Checks contracts for functions in the slice |
| `cli-audit-review` | ✅ if scope contains an active diff or MR/PR review context | Reviews changed behavior as a merge gate |
| `cli-audit-sync` | ✅ | Checks doc-code coherence within the slice |
| `cli-audit-shell` | ✅ if scope has .sh files | Audits shell scripts in the slice |
| `cli-forge-readme` | ❌ | README is project-wide |
| `cli-forge-tree` | ✅ | Audits only the slice's structure |
| `cli-forge-pipeline` | ❌ | CI is project-wide |
| `cli-forge-schema` | ✅ | Audits diagrams referencing the slice |
| `cli-forge-infra` | ❌ | Infra is project-wide |
| `cli-forge-data` | ✅ only when explicitly requested or correcting a data-safety finding | Designs or implements the scoped database correction |
| `cli-forge-github` | ❌ | Repo config is project-wide |
| `cli-audit-wizard` | ❌ | Wizard UX is project-wide |
| `cli-audit-hanoi` | ✅ if scope has ordering-sensitive artifacts (Dockerfile, playbooks, manifests, workspace members) | Audits step ordering and blast radius within the slice |

### Step 1 — Discover available skills

```
Resolve SKILLS_ROOT:
  1. $CODEX_HOME/skills if set and exists
  2. ~/.codex/skills if it exists and contains cli-*/SKILL.md
  3. ~/.claude/skills if it exists and contains cli-*/SKILL.md

Glob: $SKILLS_ROOT/cli-*/SKILL.md
```

Parse each SKILL.md frontmatter to extract: `name`, `description`, `argument-hint`.

### Step 2 — Detect project context and language

1. **Detect output language** (MANDATORY): `git log --oneline -10` + `head -20 README.md`. Whatever language dominates the commits and README is the language all report output must use. Inject that language into every sub-agent prompt. No exceptions.
2. Read manifest (`Cargo.toml`, `package.json`, `go.mod`, etc.)
3. Check for docs: `README.md`, `docs/`, `*.md`
4. Check for schemas/diagrams: Mermaid blocks in `.md` files
5. Check for infra: `Dockerfile`, `docker-compose.yml`, `*.tf`, `helmfile.yaml`
6. Check for tests: `tests/`, `test/`, `spec/`, `e2e/`
7. Check for contracts: `CONTRACTS.md`
8. Check for CI: `.github/workflows/`, `.gitlab-ci.yml`
9. Get project size: file count, primary language(s)
10. Detect database signals: SQLx dependencies/macros, PostgreSQL URLs/types, migration directories,
    `.sql` files, repositories, transaction boundaries, and schema tools

### Step 3 — Decide which skills to run

Read `references/orchestration.md` for the full applicability matrix. Key rule: **don't run skills that don't apply** — no infra files = no infra audit.

### Step 4 — Execute in 2 waves

Read `references/orchestration.md` for execution order, prompt patterns, and wave rules.

**Wave 1 (foundation, parallel):** code, doc, test, tangle, tree, readme, shell, wizard — independent scans
**Wave 2 (cross-cutting + handoffs, parallel):** review, data, sync, drift, pipeline, schema, infra + skills recommended by Wave 1 handoffs
**Wave 3 (adaptive, if needed):** skills recommended by Wave 2 handoffs that haven't run yet

Wave 2 skills get Wave 1 summaries injected. Handoff-recommended skills get the caller's reason injected. Deduplication prevents duplicate runs (same skill + same scope = run once). See `references/orchestration.md` for the full adaptive handoff algorithm.

### Step 5 — Collect, classify, and present ALL corrections

Read `references/orchestration.md` for templates and the full Phoenix triage rules.

**Critical rule: show every correction found. Never truncate.**

Produce a unified report with:

1. **Score card** — all skill scores in one table
2. **Triage 3-2-1** — ALL corrections, classified in 3 tiers (see below)
3. **Strengths** — what the project does right
4. **Trends** — if previous audit exists in `docs/reviews/`, compare scores
5. **Phoenix status** — convergence indicator

#### Triage 3-2-1 (inspired by emergency medicine triage + immune system)

Every correction goes into exactly one tier. The tiers define **treatment order**, not importance:

| Tier | Name | Criteria | Action |
|------|------|----------|--------|
| **🔴 Tier 3** | **Critical** | Security flaws, broken functionality, data loss risk, hardcoded secrets, missing error handling that causes silent failure | Fix NOW — these block everything |
| **🟡 Tier 2** | **Major** | Architecture debt, missing tests, obsolete docs, non-pinned versions, code smells with real impact (god functions, duplication) | Fix NEXT — these degrade over time |
| **🟢 Tier 1** | **Minor** | Style, missing diagrams, nice-to-have docs, structural organization, cosmetic improvements | Fix LATER — these improve but don't protect |

**Display rules:**
- Show ALL items in each tier — no "top N" truncation
- Each item gets: `#`, description, effort (Low/Medium/High), source skill
- Count per tier shown in the tier header: `🔴 Tier 3 — Critical (4 items)`

### Step 6 — Phoenix Choice

After presenting the full triage, ask the user. Phrase the prompt in the project's detected language; the English version below is the canonical template:

```
Phoenix — Which tier should we tackle?
  [1] Fix everything (autonomous convergence, unified plan)
  [2] Fix 🔴 critical only (N items)
  [3] Fix 🟡 major only (N items)
  [4] Fix 🟢 minor only (N items)
  [5] Not now
```

**Option [1] = autonomous convergence.** The cycle runs in an isolated worktree, performs all passes autonomously with file-based tracking (so no items get forgotten), then presents ONE unified plan to approve or reject. No per-item "interactive" mode — that proved too fragile.

### Step 6b — Correction pipeline (audit → forge → commit → re-audit)

**Convention conservation law (read `../gotchas.md` section "Convention conservation")**:

Before ANY correction that touches a convention (file extension, naming, indentation, quoting, language), verify that a **concrete external force** justifies the change. Otherwise, preserve the project's current state. Consistency, best-practice, and aesthetics are NOT forces.

**File-based tracking is MANDATORY** (prevents the LLM from forgetting items):

```bash
mkdir -p .claude/cycle-progress
# Write the full triage as a checklist to current.md before starting
```

When the user chooses any correction option, follow this pipeline with **explicit per-item iteration**:

```
1. Write triage to .claude/cycle-progress/current.md (all items as [ ])

2. FOR EACH item in the selected tier (sequential, no batching):
   a. FIX: edit code/config directly OR trigger the forge skill
   b. GENERATE: if missing docs/diagrams → run the appropriate forge skill
   c. COMMIT: format with cli-git-conventional (ghostwriter, zero AI markers)
   d. MARK: update current.md from [ ] to [x]
   e. LOG: append to .claude/cycle-progress/log.txt with timestamp
   NEVER skip an item. NEVER mark multiple items as done in batch.

3. VERIFY: grep "\[ \]" current.md → must return 0 unfinished items
   If unfinished items remain → RESTART the loop, you forgot some

4. RE-AUDIT: re-run only the skills that sourced the fixed items
```

**Forge skills triggered automatically by audit findings:**

| Audit finding | Forge skill triggered | What it produces |
|--------------|----------------------|-----------------|
| Missing CONTRIBUTING.md, architecture docs | `cli-forge-doc` | CONTRIBUTING.md, docs/explanation/architecture.md |
| Missing or outdated README | `cli-forge-readme` | Updated README.md |
| Missing diagrams | `cli-forge-schema` | Mermaid diagrams in docs or README |
| CI/CD issues (missing stages, parallelism) | `cli-forge-pipeline` | Updated pipeline config |
| Code fixes, config fixes | Direct edit | Modified files |

**cli-git-conventional is ALWAYS used** — every correction commit goes through ghostwriter format. No exceptions, no AI trailers.

**Example correction sequence:**
```
Triage item #5: "Missing CONTRIBUTING.md" (source: cli-audit-doc)
  → cli-forge-doc generates CONTRIBUTING.md (absorbs CLAUDE.md content if present)
  → git add CONTRIBUTING.md
  → cli-git-conventional: "docs: add contributing guide with commit rules and git workflow"
  → cli-audit-doc re-runs → item resolved

Triage item #1: "Hardcoded password in Containerfile" (source: cli-audit-code)
  → Direct edit: remove hardcoded value, add env var
  → git add Containerfile entrypoint.sh
  → cli-git-conventional: "fix(security): externalize healthcheck password"
  → cli-audit-code re-runs → item resolved, may find cascade items
```

If the user chooses `[1]` Fix everything:
1. Read `references/convergence.md` for the full algorithm
2. Run in an isolated worktree, fully autonomous
3. Track cascades (issues that only appear after earlier fixes)
4. Present a single unified plan with the complete diff
5. User approves (apply all), selects (cherry-pick), or rejects (discard)

### Step 7 — Phoenix Convergence (self-stopping)

The cycle stops automatically when **any** of these conditions is met:

| Condition | Meaning |
|-----------|---------|
| No 🔴 Tier 3 and no 🟡 Tier 2 items remain | Project is healthy — only cosmetic items left |
| Re-audit finds 0 new issues vs. previous pass | Fixes didn't introduce regressions — stable |
| User chooses `[5]` | Explicit stop |

When the cycle converges, output (translated into the project's detected language; English template below):

```
🔥 Phoenix — Cycle complete

Passes performed: N
Issues resolved: X / Y
Score: before → after

The project has converged. No critical or major flaws remain.
```

### Step 8 — Output

- **Console** (always): full scorecard + complete 3-2-1 triage + phoenix choice
- **File** (if `docs/` exists): `docs/reviews/{YYYY-MM-DD}-audit.md` — includes full triage and convergence status

## Recurring Usage

```
/loop 7d /cli-cycle .
```

The skill automatically detects previous reports in `docs/reviews/` and shows progression.

## What this skill does NOT do

- **It does not generate from scratch.** It audits existing state
- **It does not run skills that don't apply.** No wasted tokens
- **It does not hide corrections.** Every finding is shown, classified, and actionable
