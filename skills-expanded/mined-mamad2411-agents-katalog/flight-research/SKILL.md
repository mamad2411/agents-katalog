---
name: flight-research
description: Temporal research for dependencies and domain skill validation. Validates package versions, discovers issues, updates landmines. Also validates .claude/skills/ domain files against current API documentation. Use for existing projects, mid-project dependency additions, domain skill validation, or periodic maintenance.
---

## ⚠️ EXECUTION RULES (MANDATORY)

1. **EXECUTE EACH STEP** - Do not skip steps based on "prior context"
2. **USE TOOLS** - You MUST call Read/Bash tools, not recall from memory
3. **SHOW WORK** - Each step must produce visible tool output
4. **NO SHORTCUTS** - "I already read this" is NOT acceptable

### Anti-Patterns (DO NOT DO THESE)
- ❌ "I already read the domain files earlier"
- ❌ "From earlier analysis..."
- ❌ Summarizing steps without executing them
- ❌ Claiming knowledge from "this conversation"

---

# /flight-research

Temporal research with **input-aware routing**. Handles three input types:

1. **Package Research** - Validates versions, discovers breaking changes, updates landmines
2. **Domain Skill Validation** - Validates .claude/skills/*/skill.md domain files against current API documentation
3. **General Questions** - Research any topic

## Input Detection (Step 0)

**BEFORE doing anything else**, classify the input:

| Input Pattern | Route To | Example |
|---------------|----------|---------|
| Bare skill name (matches `.claude/skills/<name>/`) | Domain Skill Validation | `/flight-research supabase` |
| `.claude/skills/*/skill.md` file path | Domain Skill Validation | `/flight-research .claude/skills/supabase/skill.md` |
| `*.flight` file path | Domain Skill Validation | `/flight-research api.flight` |
| Package names with optional versions | Package Research | `/flight-research express@5 react@19` |
| Question or topic | General Research | `/flight-research "REST API best practices 2026"` |
| `--validate-all` | Domain Skill Validation (all files) | `/flight-research --validate-all` |
| No arguments | Package Research (auto-detect) | `/flight-research` |

**Classification Rules:**
1. If argument ends in `.md` and path contains `skills/` → Domain Skill Validation mode
2. If argument matches a directory name in `.claude/skills/` → Domain Skill Validation mode (resolve to `.claude/skills/<name>/skill.md`)
3. If argument ends in `.flight` → Domain Skill Validation mode
4. If argument is `--validate-all` → Validate all domain skill files in `.claude/skills/`
5. If argument looks like `package@version` or known package name → Package Research mode
6. If argument is quoted or contains question words → General Research mode
7. If no arguments → Package Research with auto-detection

---

## Usage

```
/flight-research [input...] [flags]
```

## Flags

| Flag | Behavior | Modes |
|------|----------|-------|
| (none) | Standard research depth | All |
| `--quick` | Check staleness only, no new searches | Package, Domain |
| `--deep` | Thorough research with Firecrawl | All |
| `--include-all` | Include tooling deps (eslint, prettier, @types) | Package |
| `--validate-all` | Validate all domain rule files | Domain |

---

# ROUTE A: Package Research

Use this route when researching npm packages, dependencies, or version compatibility.

## Process

### Step 0: Date Anchor (MANDATORY)

**BEFORE ANY TOOL CALLS**, output:

```
📅 Research Date: {CURRENT_DATE}
🔍 Research Window: {YEAR-1}-01-01 to {CURRENT_DATE}
```

This anchors ALL subsequent searches. Without this, queries will return stale results.

---

### Step 1: Identify Dependencies

Detect dependencies in priority order:

1. **$ARGUMENTS** (if provided) - Use exactly what user specified
2. **package.json** - Parse `dependencies` + `devDependencies`
3. **PRD.md** - Extract tech stack from "## Tech Stack" or similar
4. **tasks/*.md** - Grep for `npm install` commands

#### Skip Patterns (Default)

Skip tooling deps unless `--include-all`:

```
@types/*
eslint*
prettier*
*-loader
*-plugin
typescript  (unless explicitly requested)
```

**Heuristic:** If a breaking change would require CODE changes (not just config), research it.

#### Output Step 1:

```markdown
## Dependencies to Research

**Source:** {package.json|PRD.md|args}

| Package | Current | Category |
|---------|---------|----------|
| express | ^5.0.0 | Backend |
| react | ^19.0.0 | Frontend |
```

---

### Step 2: Check Existing Landmines

If `.flight/known-landmines.md` or `.claude/known-landmines.md` exists:

1. **Read the "Last Full Review" date**
2. **If >3 months old:** Mark ALL entries as NEEDS_VERIFICATION
3. **Check each entry against dependencies being researched**
4. **Use entries as research STARTING POINTS, not facts**

If no landmines file exists, note: "No existing landmines file. Will create."

---

### Step 3: Research Each Dependency

For each dependency, run date-anchored searches.

#### 3a. Breaking Changes (GitHub)

```
"{library} breaking changes {YEAR-1}-{YEAR}" site:github.com
```

#### 3b. Migration Guide

```
"{library} v{X} migration guide after:{YEAR-1}-01-01"
```

#### 3c. Integration Issues (if using scaffold tools)

```
"vite {library} {YEAR}" OR "create-react-app {library} {YEAR}"
```

#### 3d. Stack Overflow

```
"{library} {framework} after:{YEAR-1}-01-01" site:stackoverflow.com
```

---

### Step 4: Update Landmines File

Update or create `.claude/known-landmines.md`:

#### New Issues → Add Entry

```markdown
### {Issue Title}
**Discovered:** {CURRENT_DATE}
**Status:** ACTIVE
**Re-verify After:** {CURRENT_DATE + 6 months}
**Issue:** {description}
**Solution (if active):** {workaround or version pin}
```

#### Existing Issues → Update Status

- Still valid → Keep as ACTIVE, update "Last Verified"
- Fixed → Change to RESOLVED, note which version fixed it
- Uncertain → Keep as NEEDS_VERIFICATION

---

### Step 5: Update Existing Files (if they exist)

**Principle:** Update what exists, don't create new artifacts.

#### If `tasks/*.md` exist with `npm install`:

Update version pins with comments explaining why.

#### If `PRD.md` exists:

Append to "Known Technical Issues" section (create section if missing).

---

### Step 6: Output Summary

```markdown
## Research Summary

📅 **Research Date:** {CURRENT_DATE}
📦 **Dependencies Researched:** {count}

### Version Recommendations

| Package | Latest | Recommended | Reason |
|---------|--------|-------------|--------|
| express | 5.1.0 | 4.21.0 | v5.x middleware hang |
| react | 19.0.0 | 19.0.0 | Stable |

### Landmines Discovered/Updated
- {list}

### Files Updated
- {list}
```

---

# ROUTE B: Domain Skill Validation

Use this route when validating `.claude/skills/*/skill.md` domain files against current API documentation.

**Purpose:** Validates that domain skills are still accurate by researching the external APIs, frameworks, or standards they reference.

**When to use:**
- Periodic maintenance (every 3-6 months)
- After major version releases of referenced APIs
- Before trusting domain skills for a new project
- When CC produces code that contradicts a domain skill

## Process (Domain Validation)

### Step D0: Date Anchor (MANDATORY)

**BEFORE ANY TOOL CALLS**, output:

```
📅 Validation Date: {CURRENT_DATE}
🔍 Research Window: {YEAR-1}-01-01 to {CURRENT_DATE}
📄 Domain File: {file_path}
```

---

### Step D1: Parse Domain Skill

Read and analyze the `skill.md` file:

1. **Read the file** using Read tool
2. **Extract structure**: frontmatter (name, description), domain name
3. **Parse rule sections**: NEVER, MUST, SHOULD, GUIDANCE
4. **Identify external references**: APIs, RFCs, frameworks, libraries, specific function names, import paths
5. **Flag temporal content**: version numbers, specific package names, dated examples

#### Output Step D1:

```markdown
## Domain Analysis

**File:** {file_path}
**Domain:** {domain_name}

### Rules to Validate

| # | Section | Title | Has External Refs | Temporal Risk |
|---|---------|-------|-------------------|---------------|
| 1 | NEVER | No raw createClient | @supabase/ssr | High |
| 2 | MUST | Use RLS policies | Supabase RLS docs | Medium |
| 3 | GUIDANCE | Auth hierarchy | getClaims/getUser | High |

### External References Detected

| Reference | Type | Rules Using |
|-----------|------|-------------|
| @supabase/ssr | Package API | N2, N3 |
| RFC 9457 | Standard | M3 |
| Supabase RLS | Platform feature | M1, G2 |
```

---

### Step D2: Research External References

For each external reference, verify current accuracy:

#### 2a. Package APIs

```
"{package} API changes {YEAR}"
"{package} latest version {YEAR}"
"{package} migration guide {YEAR}"
```

Check for: renamed functions, removed APIs, new recommended patterns.

#### 2b. RFCs and Standards

```
"{RFC number} current status {YEAR}"
"{standard name} latest version {YEAR}"
```

Check for: superseded standards, errata, new versions.

#### 2c. Platform Features

```
"{platform} {feature} changes {YEAR}"
"{platform} documentation {feature}"
```

Check for: deprecated features, renamed concepts, new alternatives.

---

### Step D3: Validate Each Rule

For each rule with external references, verify:

1. **Is the rule still accurate?** Does current documentation support it?
2. **Are import paths still correct?** Have packages restructured?
3. **Are function names still current?** Have APIs been renamed?
4. **Are examples still valid?** Do good/bad examples reflect current reality?
5. **Is there new information?** Updates that should modify the rule?

#### Output Step D3:

```markdown
## Rule Validation Results

### NEVER #2: Use @supabase/ssr
**Status:** ✅ VERIFIED
**Notes:** @supabase/ssr remains the current recommended package.

### GUIDANCE #3: Auth validation hierarchy
**Status:** ⚠️ UPDATE RECOMMENDED
**Notes:** getClaims() renamed to getTokenClaims() in supabase-js v3.
**Recommended Change:** Update function name in guidance section.

### NEVER #5: Sensitive data in query strings
**Status:** 🔄 NEEDS UPDATE
**Notes:** OWASP API Security Top 10 2025 now covers additional patterns.
**Required Change:** Add new patterns to examples.
```

---

### Step D4: Update Domain Skill

Apply verified changes directly to the `.claude/skills/*/skill.md` file:

1. **Fix stale content** — update function names, import paths, package names
2. **Preserve timeless principles** — never remove the underlying rule, only update the specifics
3. **Add validation timestamp** at the top of the file:

```markdown
<!-- Last validated: {CURRENT_DATE} | Next review: {CURRENT_DATE + 6 months} -->
```

4. **Do NOT add version numbers** — keep content timeless per Flight's temporal hygiene principle

---

### Step D5: Output Summary (Domain Validation)

```markdown
## Domain Validation Summary

📅 **Validation Date:** {CURRENT_DATE}
📄 **Domain:** {domain_name}
📊 **Rules Validated:** {count}

### Results

| Status | Count | Rules |
|--------|-------|-------|
| ✅ Verified | 18 | N1, N2, N3, M1, ... |
| ⚠️ Updated | 3 | N5, G3, G12 |
| 🔄 Needs Manual Review | 1 | M8 |

### Changes Made
- {list of changes applied}

### Next Validation Due
- {CURRENT_DATE + 6 months}
```

---

### --validate-all Mode

When `--validate-all` is passed:

1. List all `skill.md` files in `.claude/skills/*/`
2. Check each for a `<!-- Last validated: -->` comment
3. Prioritize files with no validation date or dates older than 6 months
4. Run Steps D0-D5 for each file that needs validation
5. Output a combined summary

```markdown
## Full Validation Summary

📅 **Date:** {CURRENT_DATE}
📊 **Files Scanned:** {count}

| Skill | Last Validated | Status | Action |
|-------|---------------|--------|--------|
| supabase | 2025-09-01 | Stale (>6mo) | Validated ✅ |
| typescript | Never | New | Validated ✅ |
| clerk | 2025-08-01 | Stale (>6mo) | Validated ⚠️ 2 updates |
```

---

# ROUTE C: General Research

Use this route for general research questions.

## Process (General Research)

### Step G0: Date Anchor (MANDATORY)

```
📅 Research Date: {CURRENT_DATE}
🔍 Research Window: {YEAR-1}-01-01 to {CURRENT_DATE}
❓ Topic: {quoted question or topic}
```

### Step G1: Research Topic

Use appropriate tools based on topic:

| Topic Type | Primary Tool | Query Format |
|------------|--------------|--------------|
| Best practices | Web Search | `"{topic} best practices {YEAR}"` |
| API standards | Web Search | `"{standard} specification"` |
| Framework patterns | Web Search | `"{framework} {pattern} {YEAR}"` |
| Security | Web Search | `"{topic} security" site:owasp.org` |

### Step G2: Synthesize Findings

Output findings with:
- **Date context** - When was this information published?
- **Source quality** - Official docs > RFCs > guides > blog posts
- **Applicability** - How does this apply to domain rules?

### Step G3: Recommend Domain Updates

If research reveals information relevant to existing domains:

```markdown
## Domain Impact

| Domain | Potential Update | Priority |
|--------|------------------|----------|
| api.md | New status code guidance | Medium |
| supabase.md | Updated auth patterns | High |
```

---

## Critical Rules

1. **DATE ANCHOR IS MANDATORY** - Step 0 must happen BEFORE any searches
2. **LANDMINES ARE STARTING POINTS** - Never trust without re-verification
3. **PRESERVE TIMELESS PRINCIPLES** - When updating domain files, keep the rule, update the specifics
4. **NO VERSION NUMBERS IN RULES** - Keep domain files temporally clean
5. **PREFER OFFICIAL SOURCES** - GitHub releases > official docs > Stack Overflow > blog posts
6. **UPDATE, DON'T CREATE** - Only modify existing files unless creating landmines for the first time

---

## When to Use

| Situation | Use This? |
|-----------|-----------|
| Periodic maintenance (every 3-6 months) | Yes — `--validate-all` |
| Major dependency version release | Yes — specific package or skill file |
| Adding new dependencies mid-project | Yes — package names |
| CC produces code contradicting a domain skill | Yes — validate that specific skill file |
| Skill file has no validation timestamp | Yes — validate it |
| Starting a new project | Yes — `--validate-all` then start work |
| Writing new code (daily work) | No — Flight handles this |

---

## Integration with Flight

Rules in `.claude/rules/` provide universal calibration. Skills in `.claude/skills/` provide domain knowledge on demand. This research skill is the **maintenance layer** — it ensures calibration stays accurate over time.

```
Daily work:   rules always loaded + skills loaded on demand → CC calibrated → hooks verify
Maintenance:  /flight-research --validate-all → skills updated → calibration stays current
```

Flight handles the present. This skill handles temporal drift.
