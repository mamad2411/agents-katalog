---
name: claude-md-audit
description: >
  Audit and improve CLAUDE.md files in the current project. Use when the user asks to
  check, audit, update, improve, or fix CLAUDE.md files; wants a quality report on
  project memory; says "review my CLAUDE.md", "is my CLAUDE.md good?", "improve my
  project memory", or "/claude-md-audit". Scans for all CLAUDE.md files, scores quality
  against standard criteria, outputs a report, then makes targeted improvements after
  confirmation. Safe to run on any project at any time.
argument-hint: [path] — audit a specific directory instead of the current one
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# Skill: claude-md-audit

Audit, score, and improve CLAUDE.md files in the current project. Generates a quality
report before making any changes, then applies targeted improvements after confirmation.

---

## Phase 1: Discovery

Find all CLAUDE.md files under the target directory (default: current working directory,
or the path given in `$ARGUMENTS`):

```bash
find . -name "CLAUDE.md" -o -name ".claude.local.md" 2>/dev/null | sort
```

**File types and their roles:**

| Type | Location | Purpose |
|---|---|---|
| Project root | `./CLAUDE.md` | Primary project context — shared with team via git |
| Local overrides | `./.claude.local.md` | Personal settings — gitignored, not shared |
| Global defaults | `~/.claude/CLAUDE.md` | User-wide defaults across all projects |
| Package-specific | `./packages/*/CLAUDE.md` | Module-level context in monorepos |
| Subdirectory | Any nested path | Feature or domain-specific context |

Note: Claude auto-discovers CLAUDE.md files in parent directories, so monorepo setups
work without duplication.

---

## Phase 2: Quality assessment

For each file found, score it against the criteria in
`${CLAUDE_PLUGIN_ROOT}/references/quality-criteria.md`.

**Quick scoring summary (full rubric in reference):**

| Criterion | Weight | Question |
|---|---|---|
| Commands/workflows | High | Are build, test, run, and lint commands present? |
| Architecture clarity | High | Can Claude understand the directory structure and key files? |
| Non-obvious patterns | Medium | Are gotchas, quirks, and project-specific rules documented? |
| Conciseness | Medium | Is it free of verbose explanations and obvious filler? |
| Currency | High | Does the content reflect the current codebase state? |
| Actionability | High | Are instructions copy-paste ready — not vague? |

**Grade scale:**
- **A (90–100)**: Comprehensive, current, actionable
- **B (70–89)**: Good coverage, minor gaps
- **C (50–69)**: Basic info, missing key sections
- **D (30–49)**: Sparse or outdated
- **F (0–29)**: Missing or severely outdated

---

## Phase 3: Quality report

**Always output the report before making any changes.**

```
## CLAUDE.md Quality Report

### Summary
- Files found: X
- Average score: X/100
- Files needing update: X

### File-by-File Assessment

#### 1. ./CLAUDE.md (Project Root)
**Score: XX/100 (Grade: X)**

| Criterion | Score | Notes |
|---|---|---|
| Commands/workflows | X/20 | ... |
| Architecture clarity | X/20 | ... |
| Non-obvious patterns | X/15 | ... |
| Conciseness | X/15 | ... |
| Currency | X/15 | ... |
| Actionability | X/15 | ... |

**Issues:**
- [specific problems]

**Recommended additions:**
- [what should be added]
```

After printing the report, ask: **"Shall I apply the recommended improvements?"**

---

## Phase 4: Targeted updates

After the user confirms, apply improvements using these guidelines:

**Only add genuinely useful information:**
- Commands or workflows discovered during analysis
- Non-obvious patterns and gotchas found in the code
- Package relationships not otherwise clear
- Configuration quirks

**Never add:**
- Content that restates what is obvious from the code
- Generic best practices not specific to this project
- One-off fixes unlikely to recur
- Verbose explanations when a one-liner suffices

**Show a diff for each proposed change** before writing:

```
### Update: ./CLAUDE.md

**Why:** Build command was missing — sessions couldn't run the project.

```diff
+ ## Quick Start
+
+ ```bash
+ npm install
+ npm run dev   # dev server on port 3000
+ ```
```
```

For CLAUDE.md templates appropriate to the detected project type, load the matching
reference from `${CLAUDE_PLUGIN_ROOT}/../references/project-types/`.

---

## Phase 5: Apply updates

Write approved changes using the Edit tool. Preserve existing content structure —
only add or update the specific sections identified in Phase 4.

---

## Structural notes to share with the user

After completing the audit, mention these practices if they aren't already in use:

1. **`<important>` tags** — wrap critical rules that must not be ignored:
   ```markdown
   <important>Never edit files outside src/ without explicit confirmation.</important>
   ```

2. **200-line limit** — CLAUDE.md content after ~200 lines may be truncated. Split
   domain-specific sections into `.claude/rules/` files and import with `@path`.

3. **`#` key shortcut** — during any Claude session, pressing `#` prompts Claude to
   incorporate session learnings into CLAUDE.md automatically.

4. **`.claude.local.md`** — personal preferences not shared with the team (add to
   `.gitignore`); put user-wide preferences in `~/.claude/CLAUDE.md`.

---

## Constraints

- Never modify any CLAUDE.md without showing the diff and receiving confirmation.
- Never add generic advice that isn't specific to the project.
- Always complete the quality report (Phase 3) before offering to apply changes.
- Do not modify source files, package manifests, or any non-CLAUDE.md file.
