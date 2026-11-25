---
name: setup-repo
description: "Fully configure this repo for a specific project. Asks 3 targeted questions, reads the codebase, then writes all agent instruction files in place — replacing every [FILL:] marker across all 32 files. Run immediately after cloning the template."
---

# Setup Repo

## Overview

This skill produces a fully configured repo with zero remaining `[FILL:]` markers. It covers all 32 files that contain markers — not just the primary instruction files — and writes them directly when run in Claude Code.

**Announce at start:** "I'm using the setup-repo skill. I'll ask you 3 quick questions, then read the codebase and write all instruction files."

## When to Use

- Immediately after cloning this template into a new project
- When basic fills were done manually but deeper fills remain
- When onboarding an existing codebase onto this template

## When NOT to Use

- Repo already fully set up (verify: `grep -rn "\[FILL:" . --include="*.md"` returns nothing outside docs)
- You only need to update one specific file — edit it directly instead

---

## Execution Modes

### Mode A — Claude Code (preferred)

Claude Code has direct file access. The skill reads files, gathers facts, writes every file in place, activates git hooks, and validates. No copy-pasting required.

### Mode B — Other agents

Generate a repo bundle first:

```bash
npx repomix   # produces repomix-output.xml (already configured)
```

Attach `repomix-output.xml` to your chat. The skill outputs filled content tiered by priority — paste and apply Tier 1 before proceeding to Tier 2.

---

## Phase 0 — Ask 3 Questions

Before reading a single file, ask the user these questions. Their answers fill things no codebase analysis can determine:

**Question 1 — Users & deployment context:**
> "Who are the primary users of this project and what is the deployment environment?"
> *(e.g. "Internal logistics staff via a React dashboard", "Public API consumers", "iOS/Android WebView")*

**Question 2 — Immutable contract:**
> "Are there any externally-bound IDs, stored data schemas, or API versions that MUST NEVER change — even across refactors?"
> *(If yes, list them. If no, answer "none" — the Immutable Contract section will be deleted.)*

**Question 3 — Extra prohibitions:**
> "Is there anything agents should never do that won't be obvious from reading the code?"
> *(e.g. "Never modify the payments module without a second review", "Never add browser APIs — this runs in a Node.js CLI")*

Wait for all three answers before proceeding.

---

## Phase 1 — Gather Project Facts

Read the codebase to establish these values:

| Fact | Where to look |
| --- | --- |
| Project name | `package.json` `name`, directory name, `README.md` H1 |
| Description | `package.json` `description`, `README.md` intro paragraph |
| Tech stack | `package.json` `dependencies`/`devDependencies`, file extensions, import patterns |
| Test command | `package.json` `scripts.test`, `Makefile`, `pyproject.toml`, `Cargo.toml` |
| Lint command | `package.json` `scripts.lint`, `.eslintrc*`, `.pre-commit-config.yaml` |
| Build command | `package.json` `scripts.build`, `Makefile`, `Dockerfile` |
| Architectural constraints | `.githooks/`, CI workflows, patterns repeated across source files |
| Prohibitions | ESLint/linter rules, code comments flagging bad patterns |
| File structure | Top-level dirs, entry points, key config files agents need to navigate |
| Primary source file | Entry point (used in qa-audit and doc-audit skills) |
| Immutable IDs | Cross-referenced values, stored schemas (supplement with Question 2 answer) |

Also run:

```bash
grep -rn "\[FILL:" . --include="*.md" --include="*.yaml" --include="*.yml" --include="*.cursorrules" | grep -v ".git/"
```

This gives you the exact list of files and line numbers to process.

---

## Phase 2 — Generate and Write (Tiered)

Process files in tier order. In **Mode A**, write each file in place using Edit/Write tools. In **Mode B**, output each tier's content before starting the next.

### Fill quality rules — apply to every marker

| Rule | Pass condition |
| --- | --- |
| **Specific** | Includes file paths, function names, or exact patterns — never vague intent |
| **Evidence-based** | Only write what you found in the repo or user answers — never guess |
| **Actionable** | An agent can follow this rule without further clarification |
| **Not code-inferable** | Only constraints that agents cannot figure out by reading source |

**Good:** `"No ORM — all DB queries in src/db/query.ts via raw SQL"`
**Bad:** `"Use the database correctly"`

**Section deletion rule:** If a section has no applicable content, delete it entirely. Key conditional sections:
- `## Immutable Contract` → delete if Question 2 answer was "none"
- `## Layout Constraints` → delete if not a UI/mobile project
- `## [FILL: Language/Framework-Specific Rules]` → replace heading + add stack-specific rules, or delete section if none apply

---

### Tier 1 — Essential (agents read these every session)

These 5 files are loaded on every agent conversation. Fill them first.

**1. `CLAUDE.md`**
Fill: project name + description + tech stack (one line), 2 constraints, 2 prohibitions, test/lint/build commands, after-every-change steps.

**2. `AGENTS.md`**
Fill: project overview, 3 architectural constraints, file structure block (generate from actual top-level dirs and entry points — use `text` code block), 2 coding rules, immutable contract (or delete section), test command, verification steps, any project-specific doc links.

**3. `GEMINI.md`**
Same structure as CLAUDE.md — fill identically.

**4. `.github/copilot-instructions.md`**
Fill: project name + description + tech stack + deployment context (from Question 1), 2 always-do rules, 3 never-do prohibitions (include user answer from Question 3), key files table (3–5 rows: entry point, main config, test entry, key utility), any doc links.

**5. `.cursorrules`**
Fill: test command (one line).

---

### Tier 2 — Important (quality gates, PR reviews, prompts)

**6. `.claude/agents/qa-reviewer.md`**
Fill: 2 project-specific review rules (derive from linting config, architectural constraints, or user answers).

**7. `.claude/rules/coding-standards.md`**
Fill: 3 architectural constraints, language/framework-specific rules section heading + 2–4 rules derived from stack, 2 project rules, immutable contract reference (or delete).
Then copy this file's content verbatim to:
- `.agent/rules/coding-standards.md` (change frontmatter `trigger: always` — keep it)
- `.kilocode/rules/coding-standards.md`

**8–9. `.agent/rules/coding-standards.md` and `.kilocode/rules/coding-standards.md`**
Apply the copy from step 7.

**10. `.github/pull_request_template.md`**
Fill: doc paths section (list the 2–3 key docs agents should verify are up to date after every change).

**11. `.github/prompts/new-feature.prompt.md`**
Fill: 2 planning constraints (derive from tech stack constraints — e.g. "This is achievable with [stack] — no [forbidden pattern]").

**12. `.github/prompts/review-changes.prompt.md`**
Fill: 2 project-specific review checks (derive from linting rules, architectural constraints).

**13. `.github/instructions/docs.instructions.md`**
Fill: additional doc paths relevant to the project (entry point docs, API docs, engineering playbook if present).

**14. `.github/instructions/qa-audit.instructions.md`**
Fill: main source file path (entry point), 3 project-specific audit checks (security, rule compliance, robustness — derive from codebase patterns).

---

### Tier 3 — Skill files (fill once, sync to 3 directories)

Generate filled content for `.claude/skills/qa-audit/SKILL.md` and `.claude/skills/doc-audit/SKILL.md`, then copy each to the parallel directories.

**15. `.claude/skills/qa-audit/SKILL.md`**
Fill: main source file name, 1 project-specific security check, 2 rule compliance checks (from linting/architecture), 1 race condition check, 1 error propagation check, 1 key value that must match across rule files, any additional rule files beyond the defaults.
Then copy to:
- `.agents/skills/qa-audit/SKILL.md`
- `.agent/skills/qa-audit/SKILL.md`

**16. `.claude/skills/doc-audit/SKILL.md`**
Fill: project-specific doc references, key values to verify for drift, any custom audit scripts.
Then copy to:
- `.agents/skills/doc-audit/SKILL.md`
- `.agent/skills/doc-audit/SKILL.md`

---

### Tier 4 — Workflows (complex — fill best-effort, flag unclear markers)

These workflows have deep project-specific content. Fill what can be determined from the codebase; flag any marker you cannot fill confidently with `[REVIEW: <reason>]` instead of leaving `[FILL:]`.

**17. `.agent/workflows/qa-audit.md`** (35 markers)
Fill: test command, main source file, zone definitions (derive from file structure), rule checks (from architecture), config file list, security checks, robustness checks, drift checks.

**18. `.agent/workflows/pr-analysis.md`** (17 markers)
Fill: project-specific PR checks, rule file references, security patterns to scan for.

**19. `.agent/workflows/feature-delivery.md`** (7 markers)
Fill: implementation rules, platform constraints, docs to update after every feature.

**20. `.agent/workflows/doc-audit.md`** (6 markers)
Fill: doc structure, content descriptions, key drift points, any custom audit scripts.

**21. `.agent/workflows/architecture-change.md`** (6 markers)
Fill: runtime baseline, environment checks, docs affected by architecture changes.

**22. `.agent/workflows/release-readiness.md`** (5 markers)
Fill: baseline validation steps, compatibility checks, docs to verify before release.

**23. `.agent/workflows/post-merge-analysis.md`** (3 markers)
Fill: syntax checks, config reference doc path.

---

## Phase 3 — Activate Git Hooks (Mode A only)

```bash
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit .githooks/commit-msg
```

---

## Phase 4 — Validate

Run:

```bash
grep -rn "\[FILL:" . --include="*.md" --include="*.yaml" --include="*.yml" --include="*.cursorrules" \
  | grep -v ".git/" \
  | grep -v "README.md" \
  | grep -v "CHANGELOG.md" \
  | grep -v "docs/CUSTOMIZATION-GUIDE.md" \
  | grep -v "docs/SKILLS-CATALOG.md"
```

**If output is empty** — setup is complete. Commit with:
```bash
git add -A && git commit -m "chore: configure repo from template via /setup-repo"
```

**If markers remain** — list each with file + line. For each:
- If it can be filled from codebase facts: fill it now
- If it requires user input: ask the user directly
- If it is in a section that doesn't apply: delete the section

Repeat validation until clean.

---

## Summary Output

After completing all phases, output:

```
## Setup Complete

- Files written: <count>
- [FILL:] markers resolved: <count>
- [REVIEW:] markers flagged for manual review: <count> (list them)
- Sections deleted (not applicable): <list>
- Git hooks: activated ✓ / skipped (Mode B — activate manually)
```
