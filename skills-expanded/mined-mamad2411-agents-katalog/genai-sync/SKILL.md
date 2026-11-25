---
name: genai-sync
description: "Inject managed sections into existing CLAUDE.md and AGENTS.md after a North Starr GenAI plugin update without re-bootstrapping. Preserves all project-specific content."
---

# Sync — Inject Managed Sections After Plugin Update

## Purpose

After updating the North Starr GenAI plugin, inject any new or updated managed sections into your existing CLAUDE.md and AGENTS.md without re-running `/genai-bootstrap`. This preserves all your project-specific content (architecture, module map, vocabulary, etc.) while adding new North Starr GenAI sections.

**This skill is for Claude Code plugin users only.** If you installed via Homebrew, run `north-starr-genai update` from the terminal instead — it does the same thing without using AI tokens.

## When to Use

- After updating the North Starr GenAI plugin in Claude Code
- When you see new features in the skills (like auto-learn) but your CLAUDE.md and AGENTS.md don't have them
- As a lightweight alternative to re-running `/genai-bootstrap` when only managed sections need updating

## How It Works

Managed sections are wrapped in marker comments:
```markdown
<!-- [NORTH-STARR-GENAI:section-name v1.2] -->
## Section Content
...
<!-- [/NORTH-STARR-GENAI:section-name] -->
```

The open marker includes an optional version tag (e.g., `v1.2`). When syncing, the version in the canonical section is compared to the version in the file. If versions match, the content is assumed current and skipped. If versions differ (or no version exists), content comparison is used as fallback.

The sync process:
1. Reads your existing CLAUDE.md and AGENTS.md
2. For each managed section defined below, checks the target file
3. If the section exists (has markers) → **replaces it in place** with the latest version
4. If the section is missing → **appends it** at the end
5. If the heading exists without markers (pre-v2.3.9 file) → **skips it** and tells you
6. **Reorders sections** so managed sections (instructions) appear BEFORE project context (Tech Stack, Architecture, etc.)
7. All project-specific content outside managed sections is **never touched**

## Workflow

### Step 0: Check Plugin Freshness

Before syncing, check whether the installed plugin is stale. This prevents syncing against outdated templates that silently serve old content.

1. **Locate the marketplace cache:** Check if `~/.claude/plugins/marketplaces/north-starr-genai/` exists (this is where Claude Code caches the plugin repo).

2. **Fetch and compare:** Run these commands via Bash:
   ```bash
   cd ~/.claude/plugins/marketplaces/north-starr-genai && git fetch origin 2>/dev/null && git rev-parse HEAD && git rev-parse origin/main
   ```

3. **Evaluate freshness:**
   - If the directory doesn't exist → skip this check (user may have installed differently)
   - If `HEAD` equals `origin/main` → plugin is current, proceed to Step 1
   - If `HEAD` is behind `origin/main` → the plugin cache is stale

4. **If stale**, auto-update the cache and continue:
   ```bash
   cd ~/.claude/plugins/marketplaces/north-starr-genai && git reset --hard origin/main && cd -
   rm -rf ~/.claude/plugins/cache/north-starr-genai
   ```

   Then present a brief notice (not a blocker):
   ```
   ⚠ Plugin cache was stale (HEAD: <old> → <new>). Auto-updated. Continuing sync with latest templates.
   ```

   Proceed to Step 1 — do NOT stop or ask the user to restart. The sync will now read from the updated marketplace directory, which has the latest templates. A full Claude Code restart is not required for `/genai-sync` to work correctly since it reads templates directly from the filesystem.

5. **Version cross-check (optional):** If `.claude-plugin/marketplace.json` is readable, compare its `metadata.version` with the version in the marketplace cache's `marketplace.json`. Log the versions in the sync preview for transparency:
   ```
   Plugin version: 4.4.0 (installed) vs 4.5.0 (latest) — STALE
   Plugin version: 4.5.0 (installed) vs 4.5.0 (latest) — current
   ```

### Step 1: Read Existing Files

Read the root context files in the project:
- `CLAUDE.md` — always (if it exists)
- `AGENTS.md` — always (if it exists)

If a file doesn't exist, skip it.

### Step 2: Sync Each Managed Section

For each managed section defined in the **Canonical Sections** below, apply the sync logic to all context files found in Step 1:

**Decision logic for each section:**

| Current state of target file | Action |
|------------------------------|--------|
| Section exists with markers AND content is **identical** to canonical | **Skip** — already up to date, no write needed |
| Section exists with markers AND content **differs** from canonical | **Replace** everything between the open and close markers (inclusive) with the canonical version below |
| Section heading (e.g. `## How to Approach Tasks`) exists but WITHOUT markers | **Skip** — tell the user: "Section exists without markers. Run `/genai-bootstrap` to get marker support, or manually wrap the section with markers." |
| Section is completely absent | **Append** the canonical version at the end of the file |

**Comparison:** Compare the existing content (between markers) with the canonical version. Normalize whitespace before comparing — trailing newlines and minor formatting differences should not trigger an unnecessary rewrite.

**Dry-run preview:** Before writing any changes, collect all planned actions (replace, append, skip) and present them as a summary:

```
Sync preview:
  CLAUDE.md:
    how-to-approach-tasks — UPDATE (content differs)
    auto-learn — SKIP (already current)
  AGENTS.md:
    how-to-approach-tasks — APPEND (section missing)
    auto-learn — APPEND (section missing)
  Agents:
    chief-ai-po.md — ADD (new)
    genai-layoutplan.md — SKIP (identical)

Apply changes? (y/n)
```

Wait for user confirmation before writing. If the user runs `/genai-sync` with `--force` or says "just do it", skip the preview.

### Step 3: Reorder Sections

After syncing content, check if managed sections appear AFTER project context headings (`## Tech Stack`, `## Architecture`, `## Grain`, `## Module Map`, `## Conventions`). If so, move them:

1. Extract all managed sections (between their markers)
2. Remove them from their current positions
3. Re-insert them immediately after the first heading (`# Project Name`) and its description line, BEFORE any project context headings
4. Preserve all other content and ordering

**Correct order:**
```
# Project Name
[description]

<!-- [NORTH-STARR-GENAI:how-to-approach-tasks] -->
## How to Approach Tasks
...
<!-- [/NORTH-STARR-GENAI:how-to-approach-tasks] -->

<!-- [NORTH-STARR-GENAI:auto-learn] -->
## When to Learn Automatically
...
<!-- [/NORTH-STARR-GENAI:auto-learn] -->

## Tech Stack
## Architecture
## Grain
## Module Map
```

If sections are already in the correct order, skip this step.

### Step 4: Sync Agents

Sync agent definitions for each enabled tool:

**Claude Code** — from `templates/claude/agents/` into `.claude/agents/`:
1. List all `.md` files in `templates/claude/agents/`
2. For each agent, copy to `.claude/agents/` — create if missing, update if content differs, skip if identical
3. Create `.claude/agents/` if it doesn't exist

**VS Code Copilot** — from `templates/github/agents/` into `.github/agents/` (only if `.github/agents/` exists or AGENTS.md references Copilot):
1. List all `.agent.md` files in `templates/github/agents/`
2. For each agent, copy to `.github/agents/` — create if missing, update if content differs, skip if identical
3. Create `.github/agents/` if it doesn't exist

**Do not hardcode the agent list.** Dynamically list all files in the template directories. This ensures new agents added in future plugin versions are automatically synced. Current agents as of v4.3.0: `genai-layoutplan`, `genai-storymap`, `chief-ai-po`.

### Step 4b: Validate Sync Results

After syncing, verify the files weren't corrupted:

1. **Marker integrity** — Every `<!-- [NORTH-STARR-GENAI:name] -->` open marker must have a matching `<!-- [/NORTH-STARR-GENAI:name] -->` close marker. If any are orphaned, warn the user.
2. **No duplicate headings** — Check that no `##` heading appears more than once in the file. Duplicates indicate a botched append.
3. **Line limit check** — CLAUDE.md and AGENTS.md should stay under 125 lines total. If syncing pushed a file over, warn the user: "File is [N] lines (recommended max: 125). Consider moving project-specific content to module-level CLAUDE.md files."
4. **Section order** — Verify managed sections appear before project context sections (confirmed by Step 3).

If any check fails, present the issue before the summary so the user can fix it.

### Step 5: Present Summary

```
## Sync Complete

**Files updated:**
- CLAUDE.md — [added: section-name, section-name] [updated: section-name] [skipped: section-name (no markers)]
- AGENTS.md — [added: section-name, section-name] [updated: section-name] [skipped: section-name (no markers)]

**Agents:**
- .claude/agents/<name>.md — [added / updated / already current]
[...repeat for each agent found in templates/claude/agents/]

**No changes needed:**
- [file] — all managed sections are up to date
```

---

## Canonical Sections

These are the managed sections that `/genai-sync` injects. CLAUDE.md and AGENTS.md get **different variants** of the `how-to-approach-tasks` section — CLAUDE.md uses plain text prompts while AGENTS.md uses `vscode_askQuestions`.

### Section: `how-to-approach-tasks` (CLAUDE.md variant)

Use this version when syncing `CLAUDE.md`:

```markdown
<!-- [NORTH-STARR-GENAI:how-to-approach-tasks v3.0] -->
## How to Approach Tasks

Before ANY code change, print this assessment:

| # | Question | Answer |
|---|----------|--------|
| Q0 | Is current behavior covered by evals? | Yes / No |
| Q1 | Does this touch a production prompt or model config? | Yes / No |
| Q2 | Does this change what data the model sees? (RAG sources, context window, tool definitions) | Yes / No |
| Q3 | Does this affect a client-facing output? | Yes / No |
| Q4 | Could this change cost at scale? (new model, more tokens, removed caching) | Yes / No |

**Gate Rules (MANDATORY — not advisory):**
- **Fast-path**: Q0 = Yes, all others No → state the file and proceed. Declare "FAST-PATH" when the routing hook asks.
- Q0 = No → MUST invoke `baseline-capturer` agent (via `/baseline`) to capture current behavior FIRST.
- Q1 or Q2 = Yes → MUST invoke `ai-invert-analyst` agent (via `/ai-invert`). The PreToolUse hook surfaces a reminder when Write/Edit targets `.plans/PROMPTS-*`, `.plans/RAG-*`, `.plans/EVAL-*`, or `.plans/GUARDRAILS-*` — route to the specialist instead of writing directly. Once inversion is ready, ask "Proceed with layout plan?" before spawning `genai-layoutplan`. Do not proceed without approval.
- Q3 = Yes → MUST invoke `baseline-capturer` agent (via `/baseline`) before any change.
- Q4 = Yes → MUST invoke `cost-estimator` agent (via `/cost-estimate`) before proceeding.
- Two or more of Q1–Q4 = Yes → Spawn `genai-layoutplan` agent for structured planning.
- All Low → State files and wait for confirmation.

## Delegation Policy (MUST)

When the task touches one of these domains, you MUST invoke the matching specialist agent via the Agent tool (`subagent_type: "north-starr-genai:<name>"`) on a separate thread, cite its output path in your response's `Cross-Consult Log`, and NOT write to its owned `.plans/` directory directly:

| Domain | Specialist Agent | Owned `.plans/` paths |
|---|---|---|
| Prompt design, few-shot, CoT, system messages | `prompt-engineer` | `PROMPTS-*/` |
| Eval design, golden sets, rubrics, regression tests | `eval-designer` | `EVAL-*/` |
| Baseline capture (pre-change snapshot) | `baseline-capturer` | `BASELINE-*.md` |
| RAG, retrieval, embedding, chunking, re-rank | `rag-advisor` | `RAG-*.md` |
| Guardrails, injection defense, PII, content filter, compliance | `guardrails-designer` | `GUARDRAILS-*.md`, `GUARDRAILS-REPORT-*.md` |
| Red-teaming, adversarial prompts | `prompt-adversary` | `ADVERSARY-*.md` |
| Cost estimation, token budget, model-tier routing | `cost-estimator` | `COST-*.md` |
| Architecture, model selection, ADRs, topology | `ai-architect` | `ADR-*.md` |
| Monitoring, observability, telemetry, drift, SLA, alerts | `ai-ops` | `OPS-*.md` |
| External APIs, credentials, webhooks, auth, retry strategy | `integration-planner` | `INTEGRATION-*.md` |
| Risk analysis, inversion, failure modes | `ai-invert-analyst` | `INVERT-*.md` |
| UI/UX for AI interfaces | `agentic-designer` | `UI-*.md` |
| Implementation plan from inversion | `genai-layoutplan` | `PLAN-*.md` |
| Story decomposition (PRD → stories) | `genai-storymap` or `chief-ai-po` | `STORIES-*.md`, `STORIES-AI-*.md` |
| Story refinement (TRIAGE mode) | `chief-ai-po` | `REFINED-*.md` |

**Exceptions — when delegation is NOT required:**
- True fast-path changes (config, docs, typo, trivial one-line fix) — declare "FAST-PATH" in your response.
- The user explicitly says "handle it yourself" or "no agents" — follow the user.
- You are the specialist agent writing your own output file.

**Peer consultation is mandatory inside specialist threads:** Every specialist report ends with a `## Cross-Consult Log` section citing peer agents consulted. Missing log → orchestrator flags the report incomplete at HARDEN → DELIVER and routes back for rework. See each specialist's `## Required Peer Consultations` section for the specific MUST-cite list.

**Workflow — 5 phases executed in order:**

**1. ASSESS** — Run the gate above. Capture baseline if needed (via `baseline-capturer`). Run `/ai-invert` (dispatches `ai-invert-analyst`) → `genai-layoutplan` for complex tasks.

**2. BUILD** — Implement the plan. Spawn specialist agents based on what the plan involves:
- Plan includes prompt design or prompt changes → spawn `prompt-engineer` agent (designs/versions prompts, writes to `.plans/PROMPTS-<name>/`)
- Plan includes RAG pipeline work → spawn `rag-advisor` agent (designs chunking, embeddings, retrieval)
- Plan includes external system integration → spawn `integration-planner` agent (maps API contracts, auth, retry strategies)
- Plan is pure application code with no AI-specific design → code directly, no specialist needed
- Specialists run on separate threads. Once they produce their outputs (prompt files, RAG configs, API specs), implement the code to wire everything together. Write tests/evals first (RED), then implement (GREEN).

**3. HARDEN** — After code is working, validate automatically:
- Spawn `eval-designer` agent — runs the eval suite (`.plans/EVAL-<name>/`), scores outputs against rubric, compares to baseline. If no eval suite exists, it creates one from the acceptance criteria.
- Spawn `guardrails-designer` agent — tests input/output guardrails, PII filtering, prompt injection defenses, audit logging.
- **Both must pass AND both must have populated Cross-Consult Logs** to proceed. If any of these fail:
  - Eval failure → review the failing criteria, fix the prompt or code, re-run eval
  - Guardrail failure → fix the gap, re-run validation
  - Missing Cross-Consult Log → route back to the specialist with feedback "cite the peers in your Required Peer Consultations section"
  - If the same validation fails twice → stop and ask the user for guidance

**4. COMPLETE** — Present a summary listing files modified, eval scores, guardrail status. Ask the user: "What would you like to do next?" with options: Generate commit message, Generate PR description, Run /learn (capture learnings), or Done. Do not run any of these automatically — wait for the user's choice.

**5. LEARN** — If the user chooses /learn, capture prompt patterns, model quirks, cost insights, and eval calibrations discovered during this task.

**Todo discipline:** Never create a todo item for verification steps like "run tests", "run evals", "build project", or "verify changes". Testing, evaluation, and building are implicit parts of the implementation workflow, not standalone tasks.

**Skip the full workflow for:** config changes, docs, CI, trivial one-line fixes — use the fast-path instead.
If more files are affected than estimated mid-implementation, STOP and run `/ai-invert`.
Always check `.plans/` for active plans before starting new work.
<!-- [/NORTH-STARR-GENAI:how-to-approach-tasks] -->
```

### Section: `how-to-approach-tasks` (AGENTS.md variant)

Use this version when syncing `AGENTS.md`:

```markdown
<!-- [NORTH-STARR-GENAI:how-to-approach-tasks v3.0] -->
## How to Approach Tasks

Before ANY code change, print this assessment:

| # | Question | Answer |
|---|----------|--------|
| Q0 | Is current behavior covered by evals? | Yes / No |
| Q1 | Does this touch a production prompt or model config? | Yes / No |
| Q2 | Does this change what data the model sees? (RAG sources, context window, tool definitions) | Yes / No |
| Q3 | Does this affect a client-facing output? | Yes / No |
| Q4 | Could this change cost at scale? (new model, more tokens, removed caching) | Yes / No |

**Gate Rules (MANDATORY — not advisory):**
- **Fast-path**: Q0 = Yes, all others No → state the file and proceed. Declare "FAST-PATH" when the routing hook asks.
- Q0 = No → MUST invoke `baseline-capturer` agent (via `/baseline`) to capture current behavior FIRST.
- Q1 or Q2 = Yes → MUST invoke `ai-invert-analyst` agent (via `/ai-invert`). The PreToolUse hook surfaces a reminder when Write/Edit targets `.plans/PROMPTS-*`, `.plans/RAG-*`, `.plans/EVAL-*`, or `.plans/GUARDRAILS-*` — route to the specialist instead of writing directly. Once inversion is ready, use `vscode_askQuestions` to ask "Proceed with layout plan?" (options: "Yes, run genai-layoutplan", "No, let me review first"). Once the plan is ready, ask again with `vscode_askQuestions`: "Plan is ready. Start implementation?" (options: "Yes, start coding", "No, I want to adjust the plan"). Do not proceed without approval at each gate.
- Q3 = Yes → MUST invoke `baseline-capturer` agent (via `/baseline`) before any change.
- Q4 = Yes → MUST invoke `cost-estimator` agent (via `/cost-estimate`) before proceeding.
- Two or more of Q1–Q4 = Yes → Spawn `genai-layoutplan` agent for structured planning.
- All Low → State files and wait for confirmation.

## Delegation Policy (MUST)

When the task touches one of these domains, you MUST invoke the matching specialist agent via the Agent tool (`subagent_type: "north-starr-genai:<name>"`) on a separate thread, cite its output path in your response's `Cross-Consult Log`, and NOT write to its owned `.plans/` directory directly:

| Domain | Specialist Agent | Owned `.plans/` paths |
|---|---|---|
| Prompt design, few-shot, CoT, system messages | `prompt-engineer` | `PROMPTS-*/` |
| Eval design, golden sets, rubrics, regression tests | `eval-designer` | `EVAL-*/` |
| Baseline capture (pre-change snapshot) | `baseline-capturer` | `BASELINE-*.md` |
| RAG, retrieval, embedding, chunking, re-rank | `rag-advisor` | `RAG-*.md` |
| Guardrails, injection defense, PII, content filter, compliance | `guardrails-designer` | `GUARDRAILS-*.md`, `GUARDRAILS-REPORT-*.md` |
| Red-teaming, adversarial prompts | `prompt-adversary` | `ADVERSARY-*.md` |
| Cost estimation, token budget, model-tier routing | `cost-estimator` | `COST-*.md` |
| Architecture, model selection, ADRs, topology | `ai-architect` | `ADR-*.md` |
| Monitoring, observability, telemetry, drift, SLA, alerts | `ai-ops` | `OPS-*.md` |
| External APIs, credentials, webhooks, auth, retry strategy | `integration-planner` | `INTEGRATION-*.md` |
| Risk analysis, inversion, failure modes | `ai-invert-analyst` | `INVERT-*.md` |
| UI/UX for AI interfaces | `agentic-designer` | `UI-*.md` |
| Implementation plan from inversion | `genai-layoutplan` | `PLAN-*.md` |
| Story decomposition (PRD → stories) | `genai-storymap` or `chief-ai-po` | `STORIES-*.md`, `STORIES-AI-*.md` |
| Story refinement (TRIAGE mode) | `chief-ai-po` | `REFINED-*.md` |

**Exceptions — when delegation is NOT required:**
- True fast-path changes (config, docs, typo, trivial one-line fix) — declare "FAST-PATH" in your response.
- The user explicitly says "handle it yourself" or "no agents" — follow the user.
- You are the specialist agent writing your own output file.

**Peer consultation is mandatory inside specialist threads:** Every specialist report ends with a `## Cross-Consult Log` section citing peer agents consulted. Missing log → orchestrator flags the report incomplete at HARDEN → DELIVER and routes back for rework. See each specialist's `## Required Peer Consultations` section for the specific MUST-cite list.

**Workflow — 5 phases executed in order:**

**1. ASSESS** — Run the gate above. Capture baseline if needed (via `baseline-capturer`). Run `/ai-invert` (dispatches `ai-invert-analyst`) → `genai-layoutplan` for complex tasks.

**2. BUILD** — Implement the plan. Spawn specialist agents based on what the plan involves:
- Plan includes prompt design or prompt changes → spawn `prompt-engineer` agent (designs/versions prompts, writes to `.plans/PROMPTS-<name>/`)
- Plan includes RAG pipeline work → spawn `rag-advisor` agent (designs chunking, embeddings, retrieval)
- Plan includes external system integration → spawn `integration-planner` agent (maps API contracts, auth, retry strategies)
- Plan is pure application code with no AI-specific design → code directly, no specialist needed
- Specialists run on separate threads. Once they produce their outputs (prompt files, RAG configs, API specs), implement the code to wire everything together. Write tests/evals first (RED), then implement (GREEN).

**3. HARDEN** — After code is working, validate automatically:
- Spawn `eval-designer` agent — runs the eval suite (`.plans/EVAL-<name>/`), scores outputs against rubric, compares to baseline. If no eval suite exists, it creates one from the acceptance criteria.
- Spawn `guardrails-designer` agent — tests input/output guardrails, PII filtering, prompt injection defenses, audit logging.
- **Both must pass AND both must have populated Cross-Consult Logs** to proceed. If any of these fail:
  - Eval failure → review the failing criteria, fix the prompt or code, re-run eval
  - Guardrail failure → fix the gap, re-run validation
  - Missing Cross-Consult Log → route back to the specialist with feedback "cite the peers in your Required Peer Consultations section"
  - If the same validation fails twice → stop and ask the user for guidance

**4. COMPLETE** — Present a summary listing files modified, eval scores, guardrail status. Use `vscode_askQuestions` to prompt the developer with options: "Generate commit message", "Generate PR description", "Run /learn (capture learnings)", "Done". Do not run any of these automatically — wait for the developer's choice. If the developer chooses "Generate commit message", generate it, then use `vscode_askQuestions` again with options: "Generate PR description", "Run /learn (capture learnings)", "Done".

**5. LEARN** — If the user chooses /learn, capture prompt patterns, model quirks, cost insights, and eval calibrations discovered during this task.

**Todo discipline:** Never create a todo item for verification steps like "run tests", "run evals", "build project", or "verify changes". Testing, evaluation, and building are implicit parts of the implementation workflow, not standalone tasks.

**Skip the full workflow for:** config changes, docs, CI, trivial one-line fixes — use the fast-path instead.
If more files are affected than estimated mid-implementation, STOP and run `/ai-invert`.
Always check `.plans/` for active plans before starting new work.
<!-- [/NORTH-STARR-GENAI:how-to-approach-tasks] -->
```

### Section: `auto-learn` (same for both files)

```markdown
<!-- [NORTH-STARR-GENAI:auto-learn v1.0] -->
## When to Learn Automatically

Run `/learn` automatically when: user corrects your approach, same fix requested twice, your change breaks something, user rejects generated code, you discover an undocumented convention, you hit a trap not in any landmine rule, prompt change causes unexpected regression, model-specific behavior discovered (works on one model, fails on another), cost optimization found (caching, batching, model selection), eval threshold adjusted (too strict or too loose), guardrail gap discovered in production, hallucination pattern identified, or data pipeline quirk encountered. Finish the immediate fix first, then capture the insight.
<!-- [/NORTH-STARR-GENAI:auto-learn] -->
```

## Notes

- This skill is Claude Code plugin-only (`tool: claude`)
- Brew/CLI users should run `north-starr-genai update` instead — same result, no AI tokens
- Only managed sections (wrapped in `<!-- [NORTH-STARR-GENAI:...] -->` markers) are touched
- All project-specific content is preserved
- When new managed sections are added in future versions, they'll be included in this skill's Canonical Sections — running `/genai-sync` after a plugin update will pick them up
- If you want full marker support on a pre-v2.3.9 file, run `/genai-bootstrap` once to regenerate with markers
