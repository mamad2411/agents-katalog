---
name: harness-audit
version: 2.0.0
description: |
  Scan a codebase to detect the five most common harness self-deceptions,
  generate a narrative diagnostic report, and optionally auto-fix findings.
  Based on the 4-Layer Harness Model.
  
  Trigger: /harness-audit, "audit my harness", "scan my project",
  "harness 审计", "检查我的 harness", or when user wants an automated
  assessment of their AI agent project setup.
---

# Harness Audit

Automatically scan a codebase for the five most common harness self-deceptions. For each one found, explain what's wrong, why it matters, and offer to fix it.

## Framework: Five Self-Deceptions

| # | Self-Deception | What you think | What's actually true | Layer |
|---|---------------|----------------|---------------------|-------|
| 1 | **The Stale Goal** | "I have a goal" | Your goal doc is months old and doesn't match what you're building | L1 |
| 2 | **The Monolith** | "I have instructions" | Everything is in one file with no priority structure | L2 |
| 3 | **The Paper Rule** | "I have checks" | Your checks are generic defaults, not project-specific constraints | L3 |
| 4 | **The Gut Review** | "I review everything" | No systematic quality criteria; review quality varies by how busy you are | L4 |
| 5 | **The Frozen Harness** | "I set up my harness" | Nothing harness-related has changed in 30+ days | L4 |

---

## Audit Procedure

### Step 1: Identify Domain & Gather Data

Determine project type. Load domain-specific reference if available:

- **Software engineering** → read `docs/software-engineering.md` for additional checks
- **Other domains** → use generic checks below

Run all data gathering commands. Store results — you'll reference them in the diagnosis.

```bash
# === Goal documents ===
# Check for goal/spec/PRD files
find docs/ -maxdepth 2 \( -name "PRD*" -o -name "spec*" -o -name "requirements*" -o -name "features*" \) 2>/dev/null
ls README.md docs/PRD.md docs/product-spec.md docs/requirements.md docs/features.md docs/decisions/*.md 2>/dev/null

# Check if instruction file references goal documents
grep -i -E "(goal|objective|spec|prd|requirement|feature|docs/)" CLAUDE.md .cursorrules 2>/dev/null

# Goal freshness: last modified date vs project activity
stat -c '%Y' docs/PRD.md docs/requirements.md docs/features.md 2>/dev/null
git log -1 --format='%at' 2>/dev/null

# === Instruction files ===
# Line count of main instruction file
wc -l CLAUDE.md .cursorrules .github/copilot-instructions.md AGENTS.md 2>/dev/null

# Check for progressive disclosure (links to other docs)
grep -c "\[.*\](.*\.md)" CLAUDE.md 2>/dev/null
grep -c "see \|refer to \|详见\|参考" CLAUDE.md 2>/dev/null

# Check for package/module-level instruction files
find . -name "CLAUDE.md" -not -path "./CLAUDE.md" -not -path "*/node_modules/*" 2>/dev/null

# Count "must/never/always" rules vs total rules
grep -c -i -E "must|never|always|绝对|必须|不得" CLAUDE.md 2>/dev/null
grep -c "^-\|^[0-9]\." CLAUDE.md 2>/dev/null

# === Automated checks ===
# CI/CD
ls .github/workflows/*.yml .gitlab-ci.yml 2>/dev/null

# Pre-commit hooks
ls .husky/pre-commit .git/hooks/pre-commit 2>/dev/null
cat .husky/pre-commit 2>/dev/null

# Custom check scripts (project-specific, not framework defaults)
find scripts/ -name "*harness*" -o -name "*check*" -o -name "*lint*" 2>/dev/null
find . -name "*.arch.*" -o -name "*architecture*test*" -not -path "*/node_modules/*" 2>/dev/null | head -5

# Count custom rules vs framework defaults
# (Read CI config to see if there are project-specific checks beyond standard lint/typecheck)

# === Quality signals ===
ls docs/QUALITY_SCORE.md 2>/dev/null
ls jest.config.* vitest.config.* coverage/ 2>/dev/null

# === Harness evolution ===
# Harness-related commits in last 30 days
git log --since="30 days ago" --oneline -- \
  CLAUDE.md .cursorrules AGENTS.md docs/ scripts/harness-checks.sh \
  .eslintrc* commitlint.config.* .husky/ 2>/dev/null | wc -l

# Total commits for context
echo "Total commits (30d):"
git log --since="30 days ago" --oneline 2>/dev/null | wc -l

# Last modified date of instruction file
git log -1 --format='%ar' -- CLAUDE.md 2>/dev/null
```

Also read these files if they exist:

```
CLAUDE.md / .cursorrules / AGENTS.md
README.md
docs/PRD.md or equivalent
docs/QUALITY_SCORE.md
.github/workflows/*.yml (scan for custom vs default checks)
```

### Step 2: Diagnose Each Self-Deception

For each of the five, determine: **detected / not detected / inconclusive.**

Use the evidence from Step 1. Be specific — cite file names, line counts, dates.

#### Self-Deception 1: The Stale Goal

**Detected if ANY of:**
- No goal/spec/PRD document exists at all
- Goal document exists but CLAUDE.md doesn't reference it (agent can't find it)
- Goal document's last modification is 60+ days older than the most recent project commit
- Goal document exists but contains no verifiable acceptance criteria (only vague descriptions)

**Severity:** 🔴 Critical — all other layers optimize the wrong direction.

**Auto-fix options:**
- If goal doc exists but isn't referenced → add reference line to CLAUDE.md
- If goal doc is stale → flag it and ask user to review/update (can't auto-fix content)
- If no goal doc exists → create a template and ask user to fill it in

#### Self-Deception 2: The Monolith

**Detected if ANY of:**
- Main instruction file > 100 lines with no links to external docs
- No package/module-level instruction files exist
- "Must/never/always" ratio > 50% of all rules (everything is "critical" = nothing is)
- Zero progressive disclosure (no links, no "see X for details", no file references)

**Severity:** 🟡 Medium — agent is making unpredictable priority judgments.

**Auto-fix options:**
- Split instruction file into index (top 60 lines: build commands + critical rules) + linked detail docs
- Create package-level CLAUDE.md stubs for each major module
- Restructure rules into "Critical Rules" and "Preferences" sections

#### Self-Deception 3: The Paper Rule

**Detected if ANY of:**
- CLAUDE.md contains "don't do X" / "never do X" rules that have no corresponding automated check
- CI only runs framework defaults (lint, typecheck) with zero project-specific checks
- No pre-commit hooks, or pre-commit hooks only run formatting
- No architecture tests or custom check scripts exist

**Detection method:** Extract "don't/never/must not" rules from CLAUDE.md. For each, search CI config and hook scripts for a corresponding automated check. The gap count = paper rules.

**Severity:** 🟡 Medium — known errors slip through because enforcement is verbal, not mechanical.

**Auto-fix options:**
- For each paper rule: generate a grep-based check script that detects violations
- Create `scripts/harness-checks.sh` if it doesn't exist
- Add harness-checks to CI pipeline or pre-commit hook
- Ask user which paper rules to convert first (prioritize by how often agent violates them)

#### Self-Deception 4: The Gut Review

**Detected if ANY of:**
- No quality scorecard / QUALITY_SCORE.md exists
- No test coverage configuration found
- No review automation (no review workflows, no quality gates beyond CI pass/fail)
- No evidence of systematic review criteria anywhere in docs

**Severity:** 🟡 Medium — quality depends on reviewer's attention on any given day.

**Auto-fix options:**
- Create a QUALITY_SCORE.md template with module-level grading
- Add test coverage thresholds to CI config
- Create a review checklist template

#### Self-Deception 5: The Frozen Harness

**Detected if ANY of:**
- Zero harness-related commits in last 30 days
- Instruction file last modified 60+ days ago
- No evidence of error→rule conversion (no new check rules added recently)

**Severity:** 🟡 Medium — harness is decaying, symptoms will be misdiagnosed as model problems.

**Auto-fix options:**
- No auto-fix for this — it's a process problem, not a file problem
- Recommend: schedule a monthly 30-minute harness review
- Show the user their "harness vitality" metric and explain what it means

---

### Step 3: Generate Report

Output format — **narrative first, scores second:**

```markdown
# Harness Audit Report

**Project**: {name}
**Date**: {date}
**Instruction file**: {filename}, {line count} lines

---

## Findings

### ⚠️ Self-Deception 1: The Stale Goal — DETECTED
{Specific evidence: "Your docs/PRD.md was last modified 94 days ago. 
Your most recent commit was 2 hours ago. CLAUDE.md does not reference 
this file — your agent doesn't know it exists."}

**Why this matters:** Your agent is solving a problem you defined three 
months ago. The project has moved on. Every hour of agent work is 
potentially optimizing the wrong direction.

**Fix:** Add a reference to docs/PRD.md in CLAUDE.md, then review and 
update the PRD to match current direction.

**Want me to add the reference now?** (I'll add one line to CLAUDE.md. 
You'll still need to update the PRD content yourself.)

---

### ✅ Self-Deception 2: The Monolith — NOT DETECTED
{Evidence: "CLAUDE.md is 72 lines, links to 4 sub-documents, has 
package-level files in 3 modules. Emphasis ratio: 23% (healthy)."}

---

### ⚠️ Self-Deception 3: The Paper Rule — DETECTED
{Evidence: "Found 5 'don't do X' rules in CLAUDE.md. Of these, 
2 have corresponding CI checks. 3 are paper-only:
- 'Never import from internal/ directly' — no automated check
- 'Always use the repository pattern for DB access' — no automated check  
- 'Don't commit console.log statements' — no automated check"}

**Why this matters:** These 3 rules exist only as suggestions. Your 
agent understands them but will violate them when context is long 
or reasoning drifts. You'll catch the violation days later — if at all.

**Fix:** Convert the top paper rule into an automated check.

**Want me to create a check script for these?** (I'll generate 
scripts/harness-checks.sh with grep-based rules for all 3.)

---

[...continue for each self-deception...]

---

## Summary

| # | Self-Deception | Status | Severity |
|---|---------------|--------|----------|
| 1 | The Stale Goal | ⚠️ Detected | 🔴 Critical |
| 2 | The Monolith | ✅ Clean | — |
| 3 | The Paper Rule | ⚠️ Detected | 🟡 Medium |
| 4 | The Gut Review | ⚠️ Detected | 🟡 Medium |
| 5 | The Frozen Harness | ⚠️ Detected | 🟡 Medium |

**Self-deceptions found: 4/5**

## Top 3 Fixes (by impact)

1. **[🔴 Now] Fix the stale goal** — update docs/PRD.md and add 
   reference in CLAUDE.md. ~1 hour. Everything else is pointless 
   until the goal is current.
2. **[🟡 This week] Convert paper rules** — create harness-checks.sh 
   for the 3 unenforced rules. ~2 hours. Stops the most common 
   recurring errors.
3. **[🟡 This week] Create quality scorecard** — QUALITY_SCORE.md 
   with module grades. ~1 hour. Gives you a reference point for 
   review instead of gut feel.

**Estimated total effort: ~4 hours to go from 4/5 self-deceptions to 1/5.**
```

### Step 4: Execute Fixes (if user approves)

After presenting the report, ask:

> "I found {N} self-deceptions. Want me to fix what I can automatically? I'll show you each change before making it."

If yes, execute fixes **one at a time**, showing diff before applying:

1. Show the proposed change
2. Explain what it does
3. Wait for explicit approval
4. Apply the change
5. Move to next fix

**What CAN be auto-fixed:**
- Adding goal doc references to CLAUDE.md
- Restructuring CLAUDE.md (split into sections, add links)
- Creating harness-checks.sh with grep-based rules from paper rules
- Creating QUALITY_SCORE.md template
- Creating package-level CLAUDE.md stubs
- Adding harness-checks to pre-commit hook or CI

**What CANNOT be auto-fixed (flag for user):**
- Stale goal content — only the user knows what the current goal is
- Missing acceptance criteria — requires domain knowledge
- Frozen harness — process change, not file change
- Review standards — requires team agreement

---

## Operating Principles

1. **Narrative before numbers.** Lead with "here's what I found and why it matters," not "D1: 2/5." Scores are supplementary, not primary.

2. **Evidence, not opinion.** Every finding must cite specific files, line counts, dates, or command outputs. "Your instruction file seems long" → "Your CLAUDE.md is 187 lines with 0 links to sub-documents."

3. **One fix at a time.** Never batch auto-fixes. Show each change, explain it, wait for approval.

4. **Stale goal trumps everything.** If Self-Deception 1 is detected, say explicitly: "Fix this first. Everything else is optimizing the wrong direction."

5. **Don't create work that won't be maintained.** If the harness is frozen (Self-Deception 5), creating a bunch of new files will just add more things to go stale. Address the process first.

6. **Respect the domain adapter pattern.** Generic detection logic lives here. Domain-specific file paths, commands, and scoring examples live in `docs/software-engineering.md` (or other domain files). Load the right adapter before running checks.

## Response Language

Match the user's language. Chinese project → Chinese report. English project → English report. Self-deception names stay consistent in both languages.

## Domain Adapters

For domain-specific checks, file paths, and scoring examples:
- **Software engineering** → `docs/software-engineering.md`
- Other domains: create `docs/{domain}.md` following the same pattern
