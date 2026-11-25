---
name: intel
description: "Generate or refresh the project context scaffold in .claude/context/ (architecture, decisions, conventions, patterns)."
disable-model-invocation: true
---

# Skill: Architecture Intel

## Overview
Extract and maintain a persistent architectural context scaffold in `.claude/context/`. Eliminates cold-start context loss across sessions by documenting stack, decisions, patterns, constraints, and conventions — each in its own file so agents load only what's relevant per task.

For backwards compatibility, `.claude/architecture.md` is maintained as a slimmed summary pointing to the full scaffold.

## When to Use
- First session on a new-to-you project
- After major refactors, dependency upgrades, or architectural shifts
- Periodically (every few weeks) to keep context files current
- When onboarding a new stack or sub-project

Do NOT use for: small bug fixes, routine feature work where context files already exist and are current.

## Process

### Step 1: Detect Mode

Check the state of `.claude/context/`:

- **`.claude/context/ROUTER.md` does not exist** → First Run mode (full analysis, generate entire scaffold)
- **ROUTER.md exists but is still an unfilled template** → also First Run mode. The installer pre-seeds `.claude/context/` with blank templates, so existence alone doesn't mean the scaffold is populated. Telltales: the `Last updated` header comment still reads `YYYY-MM-DD`, or the Context Files table shows Status "Template" for every file.
- **ROUTER.md is populated** → read the `Last updated` date from each context file's header comment
  - If user passed `--full` → Full Refresh mode
  - Otherwise → Incremental mode

**Backwards compatibility:** If `.claude/architecture.md` exists but `.claude/context/` does not, treat as First Run mode. The monolithic file will be preserved as a reference during migration.

### Step 2: Check Axon Availability

Run `axon_list_repos` to check if the current repo is indexed.

- **Axon available** → use the Axon analysis path (faster, more structural)
- **Axon unavailable** → use the file-read analysis path (still effective, just more manual)

Inform the user which path you're taking.

### Step 3: Analyze the Codebase

**With Axon:**
1. `axon_query` with broad concept terms — "authentication", "error handling", "data models", "routing", "middleware" — to identify the major patterns in use
2. `axon_context` on key entry points (main URL conf, root app component, main router, etc.) to map the layer structure
3. `axon_cypher` for structural queries when needed — find all classes following a pattern, identify service layers, locate middleware chains
4. Read package manifests (requirements.txt, package.json, pubspec.yaml, go.mod) for stack and decision data

**Without Axon:**
1. Read CLAUDE.md and any existing project documentation for documented conventions
2. Read package manifests to identify stack and key dependencies
3. Identify entry points — glob for urls.py, app/layout.tsx, main.dart, main.go, index.ts, etc.
4. Read entry point files to understand the top-level structure
5. Glob for structural patterns: `**/services.py`, `**/repositories.py`, `**/middleware.*`, `**/serializers.py`, `**/hooks/use*.ts`
6. Read 2-3 representative examples of each discovered pattern
7. Infer decisions from dependency choices and configuration files

**Incremental mode — both paths:**
1. Run `git log --since="[last-updated-date]" --stat --pretty=format:"%H %s"` to identify what changed
2. If Axon available, run `axon_detect_changes` on the range for structural impact
3. Classify changed files to determine which context files need updating:
   - Config/manifest changes → `architecture.md` + `decisions.md`
   - New directories or apps → `architecture.md` + `conventions.md`
   - New service/pattern files → suggest adding a pattern to `patterns/`
   - New middleware, validators, exception handlers → `architecture.md` (constraints) + suggest pattern
   - Dependency additions/removals → `decisions.md`
4. Re-analyze only the code relevant to affected files
5. Skip context files whose underlying code did not change

### Step 4: Extract Architecture

For each category, extract concrete, specific findings — not generic descriptions. Every bullet should be grounded in what the code actually does.

**For `architecture.md` (`.claude/context/architecture.md`):**

| Category | What to capture | Example |
|----------|----------------|---------|
| **Stack** | Technology, version, directory | `Django 5.2 + DRF (server/)` |
| **Architecture Overview** | Layer map, boundaries, data flow | "Three-layer: views → services → models. All external API calls isolated in clients/" |
| **Constraints** | Non-negotiable rules | "All list endpoints paginated (PageNumberPagination, default 20)" |
| **Key Entry Points** | 3-5 files to understand first | `server/config/urls.py`, `web/app/layout.tsx` |

**For `decisions.md` (`.claude/context/decisions.md`):**

| What to capture | Example |
|----------------|---------|
| Technology/pattern choice + rationale + date | "JWT over sessions: stateless auth for mobile client support" |
| Status: Active or Superseded | If superseded, link to the replacement decision |

**For `conventions.md` (`.claude/context/conventions.md`):**

| Category | What to capture | Example |
|----------|----------------|---------|
| **Naming** | Naming conventions with examples | "Tests: apps/[domain]/tests/test_[module].py" |
| **File Organization** | Directory structure rules | "One service file per Django app" |
| **Error Handling** | Error handling norms | "All API errors go through custom exception handler" |
| **Testing** | Testing conventions | "Integration tests use factory_boy, unit tests use mocks" |
| **Project-Specific Rules** | Anything else specific to this project | "Never import from another app's models directly" |

**For `patterns/` (`.claude/context/patterns/`):**

When a recurring structural pattern is discovered, create a pattern file following the format in `patterns/README.md`. Only create pattern files for significant, reusable patterns — not every code convention.

**Multi-stack projects:** Detect multiple sub-projects (look for multiple package manifests at different directory levels, or sub-project directories in CLAUDE.md). Keep Decisions flat (project-wide). Give Conventions and Patterns per-stack subsections:

```markdown
## Naming
### Backend (server/)
- ...
### Frontend (web/)
- ...
```

### Step 5: Write or Update Context Files

**First Run:**
1. Ensure the `.claude/context/` structure exists. The installer usually pre-seeds it with blank templates (ROUTER.md, decisions.md, conventions.md, patterns/README.md) — fill those in place. If a file is missing, create it using the formats in Step 4 with a `<!-- Generated by /intel. Last updated: YYYY-MM-DD -->` header comment and a `## Manual Notes` section at the bottom.
   - Create `architecture.md` with extracted Stack, Architecture Overview, Constraints, Key Entry Points
   - Fill `decisions.md` with extracted decisions (replace placeholder entries)
   - Fill `conventions.md` with extracted conventions by category
   - Create any `patterns/*.md` files for significant patterns discovered
2. Set the `Last updated` date to today in each file's header comment
3. Generate `ROUTER.md` (see Step 5b)
4. Write `.claude/architecture.md` as a slimmed summary — same Stack/Overview/Constraints/Entry Points sections plus a pointer to `context/` — this maintains backwards compatibility

**Full Refresh (`--full`):**
1. Re-analyze the entire codebase (same as First Run analysis)
2. Rewrite all context files with fresh findings
3. **Preserve the `## Manual Notes` section** and everything below it in each file that has one
4. Regenerate `ROUTER.md` (see Step 5b)
5. Update `.claude/architecture.md` summary
6. Update `Last updated` dates

**Incremental:**
1. Read all existing context files in `.claude/context/`
2. Update only the files identified in Step 3 as affected by recent changes
3. Do NOT rewrite files whose underlying code hasn't changed
4. NEVER modify `## Manual Notes` sections or anything below them
5. If a new pattern is discovered, create a new `patterns/*.md` file and regenerate ROUTER.md
6. Update `Last updated` dates only on files that were modified
7. Update `.claude/architecture.md` if the architecture summary changed

### Step 5b: Generate ROUTER.md

After writing or updating context files, rebuild ROUTER.md:

1. Read the current `ROUTER.md` (or use the template for first run)
2. Update the **Context Files** table:
   - List every file in `.claude/context/` (except ROUTER.md itself)
   - List every `patterns/*.md` file individually
   - Set Status to "Populated" for files with content, "Template" for empty ones
3. Update the **Task Routing** table if new pattern files warrant specific routing (e.g., a "Testing Pattern" file should be listed under Debugging/Fixing tasks)
4. Keep ROUTER.md under 50 lines — it's a dispatch table, not a knowledge base

### Step 6: Wrap Up

After writing/updating the files:
1. Summarize what was found or changed, listing which context files were created/updated
2. Note if anything looks unusual or worth the user's attention
3. Mention the drift detector: *"You can check recent changes against these conventions by loading `agents/drift-detector.md` as a subagent."*
4. Mention memory commands: *"Use `/remember` to capture additional decisions, conventions, or patterns. Use `/recall` at the start of future sessions to load relevant context."*

## Quick Reference

| Mode | Trigger | Scope | Manual Notes |
|------|---------|-------|--------------|
| First Run | Scaffold missing, or only unfilled templates | Full analysis, all context files | N/A |
| Incremental | Context exists (default) | Changed files only | Preserved |
| Full Refresh | User passes `--full` | Full re-analysis, all files | Preserved |

| Axon Available | Analysis Approach |
|----------------|-------------------|
| Yes | axon_query → axon_context → axon_cypher + manifest reads |
| No | Entry point reads → glob for patterns → representative file reads |

| Context File | Contains | Size Target |
|-------------|----------|-------------|
| `architecture.md` | Stack, overview, constraints, entry points | Under 80 lines |
| `decisions.md` | Lightweight ADRs with rationale | Under 60 lines |
| `conventions.md` | Naming, file org, error handling, testing norms | Under 60 lines |
| `patterns/*.md` | One file per significant reusable pattern | Under 40 lines each |
| `ROUTER.md` | Navigation hub — dispatch table | Under 50 lines |

**Total token budget:** The scaffold should be smaller in aggregate than the old monolithic architecture.md when only relevant files are loaded per task. ROUTER.md + one context file should be under 100 lines.

## Common Mistakes

- **Overwriting Manual Notes** — never modify content after the `## Manual Notes` heading in any context file
- **Rewriting unchanged files** — in incremental mode, only touch files affected by recent changes
- **Generic descriptions** — "uses a service layer" is useless. "Business logic in `apps/*/services.py`, views call service functions, never access ORM directly" is useful
- **Too long** — if any single context file exceeds its size target, trim aggressively. The point of the scaffold is to load less, not more
- **Missing rationale in Decisions** — "uses JWT" isn't a decision. "JWT over sessions: needed stateless auth for mobile clients" is
- **Forgetting backwards compat** — always update `.claude/architecture.md` alongside the scaffold so projects that haven't migrated still get a useful summary
- **Bloated ROUTER.md** — the router is a dispatch table. If it exceeds 50 lines, you're putting content in it that belongs in the context files
