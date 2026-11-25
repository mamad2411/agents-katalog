---
name: sync-project-docs
description: >
  Keep project documentation truthful and consistent. Use when about to commit code that
  adds, removes, or renames files, changes API endpoints, modifies service boundaries, or
  alters architectural structure. Also when concept renamed, metric changed, findings need
  propagation, or consistency check needed. Triggers: "update docs", "sync docs",
  "commit", "提交", "更新文档", "同步文档", "文档一致性".
---

# Sync Project Docs

**Core principle:** Structural commits and terminology changes must leave documentation truthful. Stale docs mislead agents and humans alike.

Three-phase loop: **Discover → Verify → Update**. Two entry points: **commit-driven** (git diff) or **concept-driven** (terminology/consistency check).

## When to Sync

| Trigger | Mode | Example |
|---------|------|---------|
| About to commit structural changes | commit-driven | File added/removed/renamed, endpoints changed, new services, dependency direction changed, new DB tables |
| User says "update docs" / "sync docs" / "提交" | commit-driven | Check last commit's diff |
| Concept renamed or metric changed | concept-driven | API name changed, threshold updated, module repurposed |
| Consistency check needed | concept-driven | "文档一致性", "sync documentation" |
| Pure bugfix, typo, comment-only | **Skip** | No structural impact |

## Phase 1 — Discover

Don't assume which docs exist. Scan every time.

### Step 1: Find All Documentation

```bash
find . -maxdepth 4 -type f \( -name "AGENTS.md" -o -name "CLAUDE.md" -o -name "GEMINI.md" -o -name "README.md" -o -name "ARCHITECTURE.md" -o -name "*.drawio" -o -name "*.puml" -o -name "*mermaid*" -o -name "*diagram*" -o -name "RELEASE_NOTES*" -o -name "CHANGELOG*" -o -name "CHANGE_LOG*" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/.venv/*" | sort
```

Also scan for other doc formats if the project uses them:

```bash
find . -type f \( -name "*.rst" -o -name "*.adoc" -o -name "*.texi" -o -name "*.org" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/.venv/*" | sort
```

### Step 2: Classify Dynamically

For each file found, assign a role based on **actual content and location**, not a hardcoded list:

| Path/name signal | Likely role | Update caution |
|-----------------|-------------|----------------|
| `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` | Agent instructions | Agents act on stale info immediately — high priority |
| `README.md` | Entry point | High visibility |
| `CHANGELOG*`, `RELEASE_NOTES*` | Change history | Usually append-only |
| `docs/`, `doc/` | Reference docs | Check all that mention the topic |
| `SPEC*`, `DESIGN*`, `ARCHITECTURE*` | Contracts | Changes here affect implementations |
| `DECISION*`, `decision*` | Decision records | Historical entries stay; add new ones |
| `output/`, `results/`, `reports/` | Generated artifacts | Check if auto-generated before editing |
| `archive/`, `attic/`, `legacy/` | Historical | Only update if explicitly requested |

**Key rule:** If a file exists in the inventory and mentions the relevant concept, it's in scope. No file gets skipped just because it wasn't in a predefined list.

### Step 2A: Audit the Root Documentation Surface

Treat the repository root as a small public interface, not a storage location for every Markdown note.

- Read the project-level `AGENTS.md` or equivalent and derive the allowed root-document set from its explicit conventions. Do not impose one universal filename list across repositories.
- Keep only discovery files, human entry points, and explicitly canonical project records at root. Put research plans, method notes, terminology reviews, literature evidence, report-design notes, and other topic material under `docs/<domain>/` or the project's existing documentation directory.
- Maintain one documentation index such as `docs/README.md`. Every topic document must be reachable from that index; supporting evidence may sit behind a canonical topic page when that keeps the index smaller.
- Before creating a new root-level Markdown file, classify its role. If it is not part of the project's root contract, place it in the documentation directory and register it in the index.
- When relocating documents, update current entry points and live references. Preserve historical `CHANGELOG*` and `DECISION*` text, and append a migration entry instead of rewriting old paths.

### Step 3: Determine Scope

**Commit-driven** — map the diff to affected docs:

```bash
git diff --name-only HEAD~1
```

| Code changed | Docs likely affected |
|---|---|
| Routes / handlers / tools | Transport-layer AGENTS.md, API reference in README |
| Services / modules (new/removed) | Module AGENTS.md + parent AGENTS.md, architecture doc |
| Database / ORM models | ER diagram, data-layer docs |
| Config / settings | CLAUDE.md / GEMINI.md facts, README setup section |
| Composition root / DI | Architecture doc, diagrams |
| New directory | Parent-level file tree listings |
| Schema / entity files | Data contract docs, architecture doc |

**Concept-driven** — search all variants of the concept (proceed to Step 4).

If the change affects many files, confirm with user:
- "Found {n} docs mentioning this concept. Update all, or limit to specific categories?"
- "These files appear auto-generated — edit them directly, or update their source?"

## Phase 2 — Verify

Before changing anything, compare current state across all discovered documents.

### Step 4: Search All Variants (concept-driven mode)

Grep for every reasonable variant of the concept/term:

```
Grep pattern="variant1|variant2|variant3" glob="*.md" output_mode="content" -n
```

Include:
- Exact term and common misspellings/typos
- Abbreviations and full forms
- Translated equivalents (if multilingual project)
- Hyphenated / spaced / camelCase variants

### Step 5: Cross-Reference Check

For each file in the hit list, verify:

1. **Terminology** — same concept, same name across files?
2. **Facts** — do numbers, dates, paths, commands match?
3. **References** — do file paths and cross-references still exist on disk?
4. **Contradictions** — does one doc say X while another says Y about the same thing?
5. **Completeness** — do counts (endpoints, services, modules) match `ls` / `grep` reality?

Output a verification report:

```
一致性检查:
✅ 一致: {concept} 在 {n} 个文件中使用相同表述
⚠️ 不一致: {file_A} 用 "{term_A}", {file_B} 用 "{term_B}" (行 {line_A}, {line_B})
❌ 矛盾: {file_A}:{line_A} 说 X, {file_B}:{line_B} 说 Y
❓ 失效引用: {file}:{line} 引用了 {path}, 该路径不存在
```

### Step 6: Present Findings — Confirmation Gate

Show the verification report. Ask user to confirm:
- Which inconsistencies to fix
- How to resolve contradictions
- Which references to update vs remove
- Any files to exclude

**Do not start editing until the user confirms.**

## Phase 3 — Update

### Step 7: Edit

**Order:** high-visibility files first (agent configs, entry points), reference docs second, generated artifacts and history last.

For each affected doc, apply doc-type-specific checks:

#### Agent Instruction Files (AGENTS.md / CLAUDE.md / GEMINI.md)

Three major agent systems share overlapping instruction file conventions:

| File | Agent System | Scope |
|------|-------------|-------|
| `CLAUDE.md` | Claude Code | Project instructions, key facts, commands |
| `AGENTS.md` | Claude Code, OpenCode, Codex | Module knowledge, cascading per directory |
| `GEMINI.md` | Gemini CLI | Project instructions |

Check:
- File tree / directory listing — lists all current files?
- Quick-location table — references new modules/services?
- Interface / endpoint counts — still accurate?
- Dependency lists — still accurate?
- **Update BOTH the changed module's doc AND its parent.**

#### Architecture Doc

Check:
- Layer diagram / dependency table — current layers and allowed dependencies
- Module descriptions — all modules listed with accurate responsibilities
- Service descriptions — all services listed with accurate dependencies
- Boundary / prohibition rules — still complete and correct

#### Diagrams (mermaid / drawio / puml / excalidraw)

Check:
- Architecture diagrams — nodes for all components, edges for all dependencies
- ER diagrams — all tables, new columns, changed relationships
- Flow / sequence diagrams — new steps or changed sequences
- **Always bump the "last updated" date in diagram headers**

#### README

Check:
- Directory tree in overview — current
- Feature list — includes new features
- Setup / install instructions — still valid
- Architecture summary — matches current state

#### Changelog / Release Notes

- Add entry for structural or user-visible changes
- Date + concise description of what changed

#### Editing principles

1. **Remove duplication before adding text** — if two docs say the same thing, keep it in the canonical one and add a pointer in the other
2. **Prefer pointers to canonical docs over copied detail** — "See `docs/ARCHITECTURE.md` for details" beats copying the full table
3. **Keep root-level docs readable in one screen** — if a section grows into a manual, move it deeper
4. Apply minimal, precise changes — don't rewrite entire sections for a single fact update
5. Use `replace_all: true` for mechanical replacements across a file
6. For nuanced changes, edit specific sections to preserve context

**Hard exclusions — never edit these without explicit user approval:**
- `DECISION*`, `CHANGELOG*`, `RELEASE_NOTES*` — historical records; terminology in past entries is part of the historical record, not an error to fix
- `archive/`, `attic/`, `legacy/` — retained for provenance
- Auto-generated output files (`output/`, `results/`) — edit the pipeline, not the artifact

When verification finds inconsistencies in these files, **report them but do not fix them**. Mark as "skipped (historical)" or "skipped (auto-generated)" in the report.

### Step 8: Verify

After updating, spot-check:

1. **File references exist** — extract file paths from docs, verify each exists on disk
2. **Counts match reality** — endpoint counts, service counts, module counts match `ls` / `grep`
3. **No orphan mentions** — docs don't reference deleted/renamed files
4. **Diagram completeness** — every service/module in code has a corresponding diagram node
5. **Old terms removed** — re-run grep from Step 4, confirm old terms only remain in exception zones
6. **No collateral damage** — spot-check 3 changed files for unintended changes
7. **Root surface is intentional** — root-level Markdown matches the project-defined allowlist
8. **Topic docs are discoverable** — every maintained document under `docs/` is reachable from the documentation index

```bash
# Verify old terms are gone (outside exception zones)
grep -rn "old_term" --include="*.md" . | grep -v "archive/" | grep -v "CHANGELOG"
```

### Step 9: Report

```
文档同步报告:
- 触发模式: {commit-driven / concept-driven}
- 变更类型: {what changed}
- 扫描文件: {n} 个
- 涉及更新: {n} 个文件
  - 已编辑: {list}
  - 跳过(自动生成): {list}
  - 跳过(历史记录): {list}
  - 跳过(用户排除): {list}
- 验证: {pass/fail — if fail, list remaining issues}
- 各关注点的规范文档: {which doc is now canonical for each concern}
```

## Project-Specific Customization

If the project has a local `repo-docs` skill or project-level documentation conventions in `AGENTS.md`, **those conventions take precedence** over this generic skill. Specifically:

- If the project defines a canonical split (which doc owns what), follow it strictly
- If the project says "root AGENTS.md stays under N lines", respect that limit
- If the project has specific file naming or section ordering, match it
- Always check `AGENTS.md` for project-specific documentation rules before editing

## Red Flags — Check Before Declaring Done

- File path in doc doesn't exist on disk
- Number/metric in doc doesn't match actual value
- Same concept described differently in two files
- Doc says "current" or "latest" but the value has changed
- File tree in docs shows a file that doesn't exist (or missing one that does)
- Architecture doc mentions a module not in the codebase
- Diagram missing a node for a component that exists
- README setup commands fail when run fresh

**Any of these = docs are misleading. Fix before moving on.**
