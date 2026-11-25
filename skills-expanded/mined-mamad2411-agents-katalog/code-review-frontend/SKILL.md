---
name: code-review-frontend
description: |
  Multi-agent PR review orchestrator. Discovers codebase quality standards first (lint, format, build,
  CI), then spawns specialized agents in parallel to surface real issues in the git diff.
  Agents report findings only — no fixes. Every finding is VERIFIED or tagged [ASSUMPTION].
  Use when: "review this PR", "code review", "check my diff", "/review"
---

# Multi-Agent Pre-Landing PR Review

**Core contract:** Surface real issues. Never invent. Every finding must be traceable to
the diff, a config file, or declared as an [ASSUMPTION]. This skill does not fix code.

## Guardrails

- Review only the changed behavior and its direct integration points.
- Do not recommend broad rewrites, abstractions, or style churn unless they prevent a verified bug.
- If evidence is weak, label the assumption or omit the finding.
- Prefer findings with a concrete repro, failing test, config violation, or line-level reasoning.

---

## Skill Directory

```
SKILL_DIR=./
```

Sub-skill paths (read when relevant):

- `$SKILL_DIR/checklist.md` — base review checklist
- `$SKILL_DIR/typescript-react-reviewer/SKILL.md` — TypeScript + React 19 reviewer
- `$SKILL_DIR/typescript-react-reviewer/references/` — antipatterns, react19-patterns, checklist
- `$SKILL_DIR/frontend-patterns/SKILL.md` — React component & state patterns
- `$SKILL_DIR/jest-react-testing/SKILL.md` — Jest + RTL testing quality
- `$SKILL_DIR/jest-react-testing/EXAMPLES.md` — test examples reference
- `$SKILL_DIR/vercel-react-best-practices/SKILL.md` — Vercel perf rules (70 rules, 8 categories)
- `$SKILL_DIR/vercel-react-best-practices/AGENTS.md` — full compiled rules doc
- `$SKILL_DIR/vercel-react-best-practices/rules/` — individual rule files
- `$SKILL_DIR/TODOS-format.md` — TODO item format reference

---

## Step 0: Codebase Context Discovery

**Before anything else**, check whether the codebase has been mapped and its conventions are known.
Without this, agents cannot distinguish a real violation from a project-specific pattern.

### 0a. Check `.planning/` for existing docs

```bash
ls .planning/ 2>/dev/null && find .planning -name "*.md" | head -20
```

Read any files that describe:

- Architecture, conventions, coding standards
- Tech stack, frameworks in use
- CI/CD pipeline or quality enforcement

**If `.planning/` has sufficient context** → proceed to Step 0b.

**If `.planning/` is empty or missing codebase context** → stop and run:

```
/gsd-map-codebase
```

After mapping completes, if enterprise work style / team conventions are still unclear:

```
/interrogate-me
```

**Do not proceed to review until codebase context is sufficient.** Assumptions without any
context produce noise, not signal.

---

### 0b. Discover Quality Tooling (Source of Truth)

Run these commands to find the project's actual quality standards. These become the ground
truth that agents cite in findings.

```bash
# Lint config
find . -maxdepth 3 \( -name ".eslintrc*" -o -name "eslint.config.*" \) 2>/dev/null | head -10

# Format config
find . -maxdepth 3 \( -name ".prettierrc*" -o -name "prettier.config.*" \) 2>/dev/null | head -10

# TypeScript config
find . -maxdepth 3 -name "tsconfig*.json" 2>/dev/null | head -10

# Build / quality scripts
cat package.json 2>/dev/null | grep -A 30 '"scripts"'

# CI quality gates
find . -path "./.git" -prune -o -name "*.yml" -path "*/.github/workflows/*" -print 2>/dev/null | head -10

# Stylelint, commitlint, husky, lint-staged
find . -maxdepth 3 \( -name ".stylelintrc*" -o -name ".commitlintrc*" -o -name ".lintstagedrc*" \) 2>/dev/null | head -10
```

Read each config file found. Extract:

- Lint rules enforced (eslint rules/plugins active)
- Format rules (printWidth, semi, quotes, trailing commas)
- TypeScript strictness (strict, noUncheckedIndexedAccess, etc.)
- Pre-commit hooks (what runs before every commit)
- CI quality gates (what must pass in CI)

Record findings as **QUALITY_CONTEXT** — agents will reference this, not invent rules.

**If no quality tooling found at all** → every agent finding for that category must be
tagged `[ASSUMPTION — no config found]`.

---

## Step 1: Branch + Diff Check

```bash
git branch --show-current
```

If on base branch → **"Nothing to review — on base branch."** → stop.

```bash
git fetch origin <base> --quiet && git diff origin/<base> --stat
```

No diff → same message → stop.

```bash
git log origin/<base>..HEAD --oneline
git diff origin/<base>
```

Read `.planning/tasks/TODOS.md` if it exists.

---

## Step 2: Scope Detection

Based on files in the diff, decide which specialist agents to spawn:

| Files changed                                  | Agent                       |
| ---------------------------------------------- | --------------------------- |
| Any file (always)                              | `base-checklist`            |
| `.ts`, `.tsx`                                  | `typescript-react-reviewer` |
| React components, hooks, context, state        | `frontend-patterns`         |
| `.test.*`, `.spec.*`, `__tests__/`             | `jest-react-testing`        |
| Any `.ts`, `.tsx`, `.js`, `.jsx` frontend file | `vercel-perf`               |

Agents are additive. A `.test.tsx` change spawns `jest-react-testing` + `typescript-react-reviewer` + `vercel-perf` + `base-checklist`.

---

## Step 3: Spawn Sub-Agents in Parallel

Spawn all applicable agents in **one message** (parallel execution). Pass each agent:

1. The QUALITY_CONTEXT discovered in Step 0b
2. The base branch name
3. The skill files to read

**Agents do not fix code. They report findings only.**

---

### Agent: base-checklist

**Always spawn.**

```
You are a code security and correctness reviewer. Your job is to find real issues — not invent them.

QUALITY CONTEXT (from main agent's discovery):
<paste QUALITY_CONTEXT here>

YOUR TASK:
1. Run: git diff origin/<base>
2. Read: ./checklist.md
3. Review diff against every checklist category.
4. Do NOT fix anything. Report findings only.

EVIDENCE RULES (critical — follow exactly):
- VERIFIED: You can point to the exact diff line or config line that proves the issue.
- [ASSUMPTION]: You believe there is an issue but cannot trace it to a specific line or config rule.
  State what you assumed and why. The human will validate.
- If you cannot verify AND the assumption is too weak → do not include the finding at all.
  It is better to miss a finding than to invent one.

REPORT FORMAT (use exactly):

## [AGENT: base-checklist]
Model: claude-sonnet-4-6
Skill: checklist.md

### Quality Config Used
<list which config files were referenced, or "None found — all findings are assumptions">

### Findings

| # | Severity | File:Line | Evidence | Issue | What to Check |
|---|----------|-----------|----------|-------|---------------|
| 1 | CRITICAL | src/foo.rb:42 | VERIFIED (diff +42) | Direct SQL interpolation | Use parameterized query |
| 2 | HIGH | src/bar.rb:18 | [ASSUMPTION] no DB schema found | Possible N+1 in loop | Verify association has .includes |

### Verdict
BLOCK | WARN | PASS

### Top Finding
<the single most important finding, or "None">

VERDICT RULES:
- BLOCK = CRITICAL finding that is VERIFIED
- WARN = HIGH findings, or CRITICAL that is only [ASSUMPTION]
- PASS = no findings
```

---

### Agent: typescript-react-reviewer

**Spawn when `.ts` or `.tsx` files changed.**

```
You are a TypeScript + React 19 code reviewer. Your job is to surface real issues — not invent them.

QUALITY CONTEXT (from main agent's discovery):
<paste QUALITY_CONTEXT here — especially tsconfig strictness and eslint rules>

YOUR TASK:
1. Run: git diff origin/<base>
2. Read in order:
   ./typescript-react-reviewer/SKILL.md
   ./typescript-react-reviewer/references/antipatterns.md
   ./typescript-react-reviewer/references/react19-patterns.md
   ./typescript-react-reviewer/references/checklist.md
3. Cross-check findings against the QUALITY CONTEXT — if the project's tsconfig/eslint already
   catches the issue automatically, note that instead of flagging it as a human-action item.
4. Do NOT fix anything. Report findings only.

EVIDENCE RULES:
- VERIFIED: Traceable to a specific diff line or to a tsconfig/eslint rule that confirms the pattern is wrong.
- [ASSUMPTION]: You recognize the pattern as problematic based on skill knowledge, but the project
  config does not explicitly address it. State what framework knowledge you're drawing from.
- Weak assumptions = omit the finding entirely.

REPORT FORMAT (use exactly):

## [AGENT: typescript-react-reviewer]
Model: claude-sonnet-4-6
Skill: typescript-react-reviewer/SKILL.md + references/

### Quality Config Used
<tsconfig strictness level found, eslint plugins active, or "None found">

### Findings

| # | Severity | File:Line | Evidence | Issue | What to Check |
|---|----------|-----------|----------|-------|---------------|

### Verdict
BLOCK | WARN | PASS

### Top Finding
<the single most important finding, or "None">

VERDICT RULES:
- BLOCK = VERIFIED critical React/TS issue (hook rules violation, memory leak, React 19 specific bug,
  type unsafety that will cause runtime errors)
- WARN = [ASSUMPTION] critical issues, or verified high-priority issues
- PASS = no findings
```

---

### Agent: frontend-patterns

**Spawn when React component, hook, context, or UI state files changed.**

```
You are a React frontend patterns reviewer. Your job is to surface real issues — not invent them.

QUALITY CONTEXT (from main agent's discovery):
<paste QUALITY_CONTEXT here>

YOUR TASK:
1. Run: git diff origin/<base>
2. Read: ./frontend-patterns/SKILL.md
3. Focus on: component composition, state colocation, custom hook design, form handling,
   accessibility, error boundaries. Skip React 19 hook correctness (typescript-react-reviewer covers that).
4. Do NOT fix anything. Report findings only.

EVIDENCE RULES:
- VERIFIED: Traceable to the diff. You can describe exactly what line introduces the problem.
- [ASSUMPTION]: You believe the pattern is problematic but need more context about component
  usage, routing, or data flow to be certain. State what additional info would confirm it.
- If you'd need to see files not in the diff to be certain → tag as [ASSUMPTION] and say which
  files would clarify.

REPORT FORMAT (use exactly):

## [AGENT: frontend-patterns]
Model: claude-haiku-4-5-20251001
Skill: frontend-patterns/SKILL.md

### Quality Config Used
<any relevant config, or "None found">

### Findings

| # | Severity | File:Line | Evidence | Issue | What to Check |
|---|----------|-----------|----------|-------|---------------|

### Verdict
BLOCK | WARN | PASS

### Top Finding
<the single most important finding, or "None">
```

---

### Agent: jest-react-testing

**Spawn when test files changed (`.test.*`, `.spec.*`, `__tests__/`).**

```
You are a Jest + React Testing Library reviewer. Your job is to surface real issues — not invent them.

QUALITY CONTEXT (from main agent's discovery):
<paste QUALITY_CONTEXT here — especially jest config, coverage thresholds>

YOUR TASK:
1. Run: git diff origin/<base>
2. Read:
   ./jest-react-testing/SKILL.md
   ./jest-react-testing/EXAMPLES.md
3. Look for the jest config file in the repo (jest.config.*, jest section in package.json).
   Read it — this tells you the actual test environment and setup. Cross-reference with findings.
4. Also check: does production code in the diff lack test coverage that the QUALITY CONTEXT
   says is required (coverage thresholds)?
5. Do NOT fix anything. Report findings only.

EVIDENCE RULES:
- VERIFIED: You can point to the test file line that demonstrates the issue (wrong query type,
  missing cleanup, etc.) OR to a jest config rule that the test violates.
- [ASSUMPTION]: You believe there is a testing gap, but haven't confirmed whether other test
  files cover the missing case. State which files you'd need to check.

REPORT FORMAT (use exactly):

## [AGENT: jest-react-testing]
Model: claude-haiku-4-5-20251001
Skill: jest-react-testing/SKILL.md

### Quality Config Used
<jest config found, coverage thresholds, or "None found">

### Findings

| # | Severity | File:Line | Evidence | Issue | What to Check |
|---|----------|-----------|----------|-------|---------------|

### Verdict
BLOCK | WARN | PASS

### Top Finding
<the single most important finding, or "None">

VERDICT RULES:
- BLOCK = VERIFIED test that actively gives false confidence (wrong async pattern causing silent pass,
  test pollution via missing cleanup, testing implementation not behavior)
- WARN = [ASSUMPTION] gaps, or verified maintainability anti-patterns
- PASS = no findings
```

---

### Agent: vercel-perf

**Spawn when any frontend file (`.ts`, `.tsx`, `.js`, `.jsx`) changed.**

```
You are a React + Next.js performance reviewer using Vercel engineering best practices.
Your job is to surface real issues — not invent them.

QUALITY CONTEXT (from main agent's discovery):
<paste QUALITY_CONTEXT here — especially Next.js config, bundle analyzer setup>

YOUR TASK:
1. Run: git diff origin/<base>
2. Read: ./vercel-react-best-practices/SKILL.md
3. For any rule that seems violated, read the specific rule file before reporting:
   ./vercel-react-best-practices/rules/<rule-name>.md
   Do not report a violation without reading the full rule — partial knowledge produces noise.
4. Prioritize: CRITICAL categories first (waterfalls, bundle), then HIGH, then MEDIUM.
5. Do NOT fix anything. Report findings only.

EVIDENCE RULES:
- VERIFIED: You read the specific rule file AND can point to the diff line that violates it.
  Cite both the rule file name and the diff line.
- [ASSUMPTION]: You believe a rule might apply but the diff alone is not enough to confirm —
  e.g., you'd need to see the component's parent or the Next.js config. Say what you need.
- If you haven't read the specific rule file for a potential violation → do not report it.

REPORT FORMAT (use exactly):

## [AGENT: vercel-perf]
Model: claude-sonnet-4-6
Skill: vercel-react-best-practices/SKILL.md

### Quality Config Used
<Next.js version found, bundle analyzer, or "None found">

### Findings

| # | Severity | File:Line | Evidence | Rule | Issue | What to Check |
|---|----------|-----------|----------|------|-------|---------------|
| 1 | CRITICAL | src/Page.tsx:14 | VERIFIED (diff +14, rule: async-parallel.md) | async-parallel | Sequential awaits for independent fetches | Wrap in Promise.all |

### Verdict
BLOCK | WARN | PASS

### Top Finding
<the single most important finding, or "None">

VERDICT RULES:
- BLOCK = VERIFIED CRITICAL rule violation (waterfall, bundle bloat introduced)
- WARN = VERIFIED HIGH/MEDIUM, or CRITICAL [ASSUMPTION]
- PASS = no findings
```

---

## Step 4: Collect Reports

Wait for all agents. Collect all reports. Count totals by severity and evidence type.

---

## Step 5: Synthesize — Main Agent Review

Read every agent report. Cross-check: if an agent cites `file:line`, verify that line exists
in the diff. If it doesn't match → drop the finding and note it was unverifiable.

**De-duplicate:** Same file:line flagged by multiple agents → merge into one finding, list
all agents that caught it.

**Never introduce new findings here** that weren't in an agent report. Your job is to
organize and verify, not add.

**Output format:**

```
# Pre-Landing Review

Branch: <branch>
Base: <base>
Files changed: <N files, +X -Y lines>
Agents run: <list>
Codebase context: <from .planning/ | mapped via /gsd-map-codebase | [ASSUMPTION — no map found]>

---

## Quality Config Summary

| Tool | Config Found | Key Rules Active |
|------|-------------|-----------------|
| ESLint | .eslintrc.js | react-hooks/exhaustive-deps, @typescript-eslint/strict |
| Prettier | .prettierrc | semi: false, printWidth: 100 |
| TypeScript | tsconfig.json | strict: true, noUncheckedIndexedAccess: false |
| CI | .github/workflows/ci.yml | lint + typecheck + test required |

---

## Agent Summary

| Agent | Model | Verdict | Verified | Assumptions |
|-------|-------|---------|----------|-------------|
| base-checklist | claude-sonnet-4-6 | BLOCK/WARN/PASS | N | N |
| typescript-react-reviewer | claude-sonnet-4-6 | BLOCK/WARN/PASS | N | N |
| frontend-patterns | claude-haiku-4-5-20251001 | BLOCK/WARN/PASS | N | N |
| jest-react-testing | claude-haiku-4-5-20251001 | BLOCK/WARN/PASS | N | N |
| vercel-perf | claude-sonnet-4-6 | BLOCK/WARN/PASS | N | N |

**Overall: BLOCK / WARN / PASS**

---

## CRITICAL — Must Address Before Merge

### 1. [CRITICAL · VERIFIED] file:line
Found by: <agent(s)>
Evidence: <config rule or diff line that proves it>
Issue: <description>
What to check: <what the developer should look at>

---

## HIGH PRIORITY

### 1. [HIGH · VERIFIED] file:line
...

---

## INFORMATIONAL

### 1. [INFO · VERIFIED] file:line
...

---

## Assumptions — Needs Human Validation

These were flagged but could not be fully verified from the diff alone.
The developer should check each one — they may be non-issues.

### 1. [ASSUMPTION] file:line (if known)
Found by: <agent>
What was assumed: <the reasoning>
What would confirm it: <specific file, line, or config to check>

---

## Scope Check

Intent:   <from commit messages / TODOS>
Delivered: <what the diff shows>
Status:   CLEAN / DRIFT / MISSING
```

---

## Important Rules

- Read full diff before reviewing
- Spawn agents in ONE parallel message — never wait for one before spawning others
- Pass QUALITY_CONTEXT to every agent — without it, agents make worse assumptions
- Never claim a finding is real without pointing to the diff line or config that proves it
- Never claim something is safe — safety claims require the same evidence standard as findings
- Do not commit, push, or modify any files
- If codebase context is inadequate → gate on `/gsd-map-codebase` and `/interrogate-me`
  before proceeding; a review without context is worse than no review
---

> **Install:** ``npx skills add ChristopherAlphonse/calphonse-skills --skill code-review-frontend``
