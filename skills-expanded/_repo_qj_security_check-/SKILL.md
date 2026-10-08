# ============================================================================
# PROJECT CONTEXT - _repo_qj_security_check
# ============================================================================

## THIS REPOSITORY
**Purpose:** [Describe what this project does]
**Stack:** 
**Status:** Active development

## REPOSITORY STRUCTURE





- _docs/            → Per-repo documentation (THIS PROJECT ONLY)
- _shared/          → Cross-repo knowledge (symlink to ../_CURSOR/)
- _PR/              → Session notes (Git-tracked)

## DEPLOYMENT (THIS PROJECT)


**Details:** See _docs/DEPLOYMENT.md

## KEY DOCUMENTATION
- Architecture: _docs/ARCHITECTURE.md
- Deployment: _docs/DEPLOYMENT.md
- Onboarding: _docs/ONBOARDING.md

## CRITICAL RULES (THIS PROJECT)

- All DB migrations via proper migration tool
- NO secrets in Git (use .env)
- NO emoji in documentation

## IMPLEMENTATION WORKFLOW
1. Analyze problem
2. **Propose solution (mention if there's a simpler alternative)**
3. Wait for user confirmation
4. Implement

## CODE QUALITY GUIDELINES
These guidelines reduce common LLM coding mistakes. Bias toward caution over speed.

### 1. Think Before Coding
Don't assume. Don't hide confusion. Surface tradeoffs.

**Before implementing:**
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First
Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.
- Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.
- Default to simple solutions - prefer 1 file over 3, prefer built-in over custom.
- Always ask: "Can this be done simpler?"

### 3. Surgical Changes
Touch only what you must. Clean up only your own mess.

**When editing existing code:**
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

**When your changes create orphans:**
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

**The test:** Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution
Define success criteria. Loop until verified.

**Transform tasks into verifiable goals:**
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

**For multi-step tasks, state a brief plan:**
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]

## DOCUMENTATION LEVELS
- **_shared/_SKILLS/** → Universal knowledge (all QJ projects)
- **_shared/_PLAYBOOKS/** → Universal procedures (all QJ projects)  
- **_docs/** → THIS repository specifics (structure, deployment, conventions)
- **_PR/** → Session notes (daily work in THIS repo)

# ============================================================================
# ============================================================================
# QUANTJOURNEY DOCUMENTATION SYSTEM
# ============================================================================
#
# CRITICAL RULE: NO EMOJI ALLOWED IN ANY DOCUMENTATION
# - Do not use emoji in PR notes, Skills, ADRs, Playbooks, or any other docs
# - Use clear text markers instead: [CRITICAL], [IMPORTANT], [NICE TO HAVE]
# - Templates are marked with \"NO EMOJI ALLOWED\" reminder
#
# ============================================================================

# === KNOWLEDGE BASE STRUCTURE ===
# 
# _shared/              → Symlink to ../_CURSOR/ (Git-ignored, local only)
#   ├── _SKILLS/        → Reusable technical patterns & solutions
#   ├── _DECISIONS/     → Architecture Decision Records (ADRs)
#   ├── _PLAYBOOKS/     → Step-by-step operational procedures
#   ├── _TEMPLATES/     → Document templates
#   └── README.md       → Index of all shared knowledge
#
# _PR/                  → Project-specific PR notes (IN Git, tracked)
#   └── PR_YYYY-MM-DD_N.md

# === WHEN TO CREATE WHAT ===

## 1. PR NOTES (Daily Work)
**Trigger:** End of every significant coding session (>30 min with meaningful changes)
**Location:** _PR/PR_YYYY-MM-DD_N.md (IN GIT)
**Process:**
  1. Check _PR/ for existing files today
  2. Determine next number (e.g., if PR_2026-01-27_1.md exists → create _2.md)
  3. Ask: \"Utworzyć PR note? [Y/n]\"
  4. Create file using template from _shared/_TEMPLATES/pr-note-template.md

**PR Note triggers:**
- New API endpoint/route created
- Database schema modified
- New data connector added
- Bug fix with non-obvious root cause
- Performance optimization
- Configuration changes
- Any session >30 min with meaningful code changes

## 2. SKILLS (Reusable Knowledge)
**Trigger:** When we solve a problem that will likely recur
**Location:** _shared/_SKILLS/[category]/[name].md (SHARED, not in Git)
**Process:**
  1. Ask: \"Czy to jest reusable skill? [Y/n]\"
  2. Suggest category: architecture/deployment/data-connectors/family-office/troubleshooting
  3. Create file using template from _shared/_TEMPLATES/skill-template.md
  4. Update _shared/_SKILLS/README.md index

**Skill categories:**
- architecture/ → System design patterns, multi-tenant strategies
- deployment/ → Docker, CI/CD, monitoring setup
- data-connectors/ → Patterns for integrating external data sources
- family-office/ → Enterprise requirements (compliance, SLA, security)
- troubleshooting/ → Common errors and debugging approaches

## 3. ARCHITECTURE DECISION RECORDS (ADRs)
**Trigger:** When choosing between 2+ viable technical approaches
**Location:** _shared/_DECISIONS/ADR-XXX-[slug].md (SHARED, not in Git)
**Process:**
  1. Ask: \"Czy to zasługuje na ADR? [Y/n]\"
  2. Determine next ADR number (check _shared/_DECISIONS/)
  3. Create file using template from _shared/_TEMPLATES/adr-template.md
  4. Update _shared/_DECISIONS/README.md index

**ADR triggers:**
- Choosing between databases (TimescaleDB vs ClickHouse)
- Selecting framework (FastAPI vs Flask)
- API design decisions (REST vs GraphQL vs Batch)
- Caching strategy (Redis patterns)
- Architecture patterns (monolith vs microservices)

## 4. PLAYBOOKS (Procedures)
**Trigger:** Multi-step process that others (or future you) will repeat
**Location:** _shared/_PLAYBOOKS/[process-name].md (SHARED, not in Git)
**Process:**
  1. Ask: \"Czy to powtarzalny proces? [Y/n]\"
  2. Create file using template from _shared/_TEMPLATES/playbook-template.md
  3. Update _shared/_PLAYBOOKS/README.md index

**Playbook examples:**
- onboarding-new-connector.md
- incident-response.md
- customer-onboarding.md
- release-checklist.md
- fundraising-demo-prep.md

## 5. RESEARCH SPIKES (Experiments)
**Trigger:** Starting a proof-of-concept or experiment
**Location:** _shared/_RESEARCH/spike-[topic]-YYYY-MM.md (SHARED, not in Git)
**Process:**
  1. Ask: \"Czy to jest research spike? [Y/n]\"
  2. Create file using template from _shared/_TEMPLATES/research-spike-template.md
  3. Update status regularly: In Progress / Completed / Abandoned
  4. If successful: convert to Skill or ADR when done

**Status tracking:**
- In Progress → actively researching
- Completed → findings documented, recommendation made
- Abandoned → not worth pursuing, reason documented

# === CROSS-REFERENCING ===
- PR notes should link to relevant ADRs, Skills, Playbooks
- Skills should link to related Skills
- ADRs should link to PRs where implemented
- Always use relative paths: [Skill](../_shared/_SKILLS/...)

# === IMPORTANT NOTES ===
- _shared/ is Git-ignored → changes there don't affect this repo
- _PR/ is tracked in Git → commit these files
- Never store secrets in documentation (use env vars)
- Keep code examples minimal and focused (<20 lines)
- Update indexes (README.md) when adding new docs
- NO EMOJI in any documentation - use text markers instead
- Always use templates - they include checklists and reminders
- For simple changes, fill only required sections (marked in templates)

# ============================================================================
