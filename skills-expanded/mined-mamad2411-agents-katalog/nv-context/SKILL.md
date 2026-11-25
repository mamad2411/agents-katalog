---
name: nv-context
description: Set up state-of-the-art context engineering for any repository. Analyzes codebase, generates multi-level CLAUDE.md/AGENTS.md hierarchy, hooks, session management, and token budgets. Based on 200+ sources including ETH Zurich, Anthropic, Google DeepMind, and Manus production data. For engineers who ship with AI agents.
argument-hint: [path-to-repo]
user-invocable: true
---

# nv:context — Context Engineering for Engineers Who Ship

You are an expert context engineer. You set up the complete context engineering infrastructure for a repository so every AI coding agent — Claude Code, Cursor, Copilot, Windsurf, Aider, Gemini — works at maximum effectiveness.

## Core Laws

These are NON-NEGOTIABLE. Backed by ETH Zurich, Anthropic, Google DeepMind, Manus, and 200+ sources:

1. **LESS IS MORE.** Auto-generated configs REDUCE success by 3% and increase costs 20%+ (ETH Zurich). Every line must earn its place.
2. **LANDMINES, NOT MAPS.** "Can the agent discover this by reading code?" If yes, DELETE it. Agents need to know where the traps are.
3. **COMMANDS BEAT PROSE.** One executable command with full flags outperforms three paragraphs.
4. **CONTEXT IS FINITE.** LLMs follow ~150-200 instructions reliably. Target under 200 lines per root file.
5. **PROGRESSIVE DISCLOSURE.** Root file for orientation -> subdirectory files for scope -> skills for on-demand -> MCP for runtime.
6. **HOOKS FOR DETERMINISM.** LLMs follow instructions ~90-95%. Hooks follow them 100%. Use hooks for anything that MUST happen.
7. **NEGATIVE INSTRUCTIONS BACKFIRE.** "Don't use X" increases likelihood of X. Say "MUST use Y" instead. Only NEVER is safe.
8. **COMPACT PROACTIVELY.** 60% = safe zone. 70% = precision drops. 85% = hallucinations. Don't wait for auto-compact at 95%.

---

## Phase 0: Smart Discovery (Analyze First, Confirm Second)

DO NOT interrogate the user. Analyze the codebase FIRST, detect everything you can automatically, then present ONE confirmation with smart defaults. The user should only need to confirm or adjust — not fill out a form.

**AUTOMATED/BATCH MODE:** When no human is available to confirm (e.g., running as a subagent, in CI, or in batch mode), present your findings but DO NOT block on confirmation. Proceed with detected defaults after a 3-second pause. Write assumptions to `NV_CONTEXT_LOG.md` in the project root so the user can review what was auto-detected and auto-decided.

### Step 1: Silent Auto-Detection (No User Input Needed)

Run these checks in parallel using subagents BEFORE asking the user anything:

**Detect tools:** Check for `.claude/`, `.cursor/`, `.github/copilot-instructions.md`, `GEMINI.md`, `.windsurfrules`, `CONVENTIONS.md`
**Detect team:** Check git log for number of unique authors
**Detect existing configs:** Read any CLAUDE.md, AGENTS.md, .cursorrules content
**Detect commands:** Read package.json scripts, Makefile, CI configs for exact commands
**Detect linters/formatters:** Check for eslint, biome, prettier, ruff, black, pre-commit
**Detect landmines:** Use Explore agents to find deprecated code, complex files, fragile patterns, env coupling, dead code
**Detect MCP:** Check .mcp.json or claude settings for configured servers
**Detect hooks:** Check .claude/settings.local.json, .git/hooks/, .pre-commit-config.yaml

### Step 2: Present Findings + ONE Question

After auto-detection, present everything you found in a compact summary and ask the user ONE thing — the only thing you can't detect from code:

> **Here's what I found in your codebase:**
>
> **Tools detected:** [Claude Code, Cursor, etc.]
> **Team:** [Solo / N contributors based on git log]
> **Existing configs:** [CLAUDE.md (X lines), etc. — or "none"]
> **Commands:** [test: ..., lint: ..., build: ...]
> **Linters:** [eslint, black, etc. — will set up as hooks]
> **MCP servers:** [list or "none"]
> **Hooks:** [existing or "none"]
>
> **Landmines I found:** (the codebase exploration results)
> 1. [Specific landmine with file path]
> 2. [Specific landmine with file path]
> 3. [etc.]
>
> **I'll set up:** AGENTS.md, CLAUDE.md (multi-level), hooks (auto-format + PostCompact + branch protection), HANDOFF.md, .claudeignore, continuous sync
>
> **One question: anything I missed?** Any landmines, gotchas, or preferences I should know about that aren't visible in the code? (Or just say "go" and I'll proceed with what I found.)

That's it. ONE interaction. The user types "go" or adds context. Then proceed to Phase 1.

### Smart Defaults (Don't Ask What You Can Infer)

| Signal | Default | Don't Ask |
|--------|---------|-----------|
| Solo dev (1 git author) | High autonomy, CLAUDE.local.md | Team size, review process |
| Team (2+ authors) | Medium autonomy, AGENTS.md in git | -- |
| .cursor/ exists | Generate Cursor rules | "Do you use Cursor?" |
| eslint/prettier/biome exists | Set up auto-format hooks | "Want hooks?" |
| pre-commit config exists | Preserve + enhance | "Want pre-commit?" |
| CLAUDE.md exists | Improve, don't replace | "What's working?" |
| No CLAUDE.md | Generate fresh | -- |
| CI config exists | Extract exact commands | "What's your test command?" |
| MCP config exists | Preserve + recommend additions | "Use MCP?" |

### Fallback: Ask ONLY What You Can't Detect

If auto-detection finds NO tool-specific directories (.claude/, .cursor/, .github/copilot-instructions.md, etc.) AND no CLAUDE.md/AGENTS.md, then ask ONE multiple-choice question using AskUserQuestion:

> **I couldn't detect which AI tools you use. Which do you work with?**
> - Claude Code
> - Cursor
> - GitHub Copilot
> - Windsurf
> - Aider
> - Gemini CLI
> - Multiple (I'll generate for all major tools)

Use AskUserQuestion to present this as selectable options — NOT as a text prompt the user has to type into.

Similarly, if git log has zero commits or no authors detected:
> **Solo dev or team?**
> - Just me
> - Team (2-5)
> - Large team (6+)

ONLY ask what auto-detection genuinely could not determine. Every question you ask that could have been detected is a failure of the skill.

---

## Phase 1: Deep Codebase Analysis

Analyze the repository using Glob, Grep, Read, and Bash. For each item, focus on what's NON-OBVIOUS — skip anything agents can discover by reading code.

| Step | Check | Goal |
|------|-------|------|
| 1.1 Token Bombs | ANY file >200 lines referenced in CLAUDE.md or loaded at session start | **HIGHEST PRIORITY.** Split into slim current-state + archive. Production data: 440→67 lines (-85%), 805→59 lines (-93%, saved 15.8K tokens/session). This single step often has more impact than everything else combined. |
| 1.2 Tech Stack | package.json, pyproject.toml, Cargo.toml, go.mod | Non-obvious choices that would surprise a new dev |
| 1.3 Commands | scripts, Makefile, CI configs | Exact commands with FULL FLAGS |
| 1.4 Architecture | Imports, custom abstractions, middleware | Counterintuitive patterns differing from defaults |
| 1.5 Existing Configs | CLAUDE.md, AGENTS.md, .cursorrules, etc. | What exists, what's stale |
| 1.6 Landmines | Deprecated paths, fragile tests, env gotchas | Combine with engineer's Phase 0 answers |
| 1.7 Testing | Test files, config, CI commands, async patterns | Exact test commands, philosophy |
| 1.8 Style Tools | .eslintrc, biome.json, ruff.toml, pre-commit | What's deterministic → becomes hooks, NOT config lines |
| 1.9 Token Budget | Existing configs, skill descriptions, MCP tools | Estimate baseline token cost before conversation starts |
| 1.10 Negative Scan | All config files | Find "don't/avoid/do not" → rewrite as "MUST Y" (keep NEVER as-is) |

---

## Phase 2: Maturity & Leverage Scoring

### L0-L6 Maturity Score

| Level | Name | Criteria |
|-------|------|----------|
| L0 | Absent | No config file |
| L1 | Basic | File exists, may be /init boilerplate |
| L2 | Scoped | MUST/MUST NOT with RFC 2119 language |
| L3 | Structured | Multiple files organized by concern |
| L4 | Abstracted | Path-scoped rules per directory |
| L5 | Maintained | L4 + active upkeep, pruned regularly |
| L6 | Adaptive | Skills, MCP, hooks, dynamic loading, session management |

### Hierarchy of Leverage Score

Score EACH layer independently (0-10) using these concrete checklists:

```
Layer                          Score  Criteria
---------------------------------------------------------------------
Verification (tests/linters)   ?/10   0: No tests/linters
                                      3: Tests exist but no CI
                                      5: CI runs tests, no coverage gate
                                      7: CI + coverage gate + lint in CI
                                      9: CI + coverage + mutation/property tests
                                      10: All of 9 + pre-commit hooks enforced

CLAUDE.md / AGENTS.md quality  ?/10   0: No file
                                      3: File exists, mostly boilerplate/prose
                                      5: Has commands + some boundaries
                                      7: Commands w/ flags + 3-tier boundaries + landmines
                                      9: Under line limits + RFC 2119 + no soft negatives
                                      10: All of 9 + @imports + progressive disclosure

Hooks                          ?/10   0: No hooks
                                      3: Basic pre-commit (lint only)
                                      5: Auto-format on save/edit
                                      7: Format + branch protection + pre-commit test
                                      9: All of 7 + PostCompact re-injection
                                      10: All of 9 + custom project-specific hooks

Skills                         ?/10   0: No skills
                                      3: 1-2 generic skills
                                      5: Skills for main workflows with descriptions
                                      7: Scoped skills under 150 lines each
                                      9: Skills + argument hints + clear triggers
                                      10: All of 9 + eval coverage for skills

Subagent patterns              ?/10   0: No subagent usage
                                      3: Ad-hoc subagent calls
                                      5: Documented fan-out patterns
                                      7: Worktree isolation + parallel execution
                                      9: All of 7 + merge quality gates
                                      10: All of 9 + resource budgets per agent

Session management             ?/10   0: No session management
                                      3: HANDOFF.md exists but unused
                                      5: HANDOFF.md + .claudeignore
                                      7: Document-and-Clear workflow documented
                                      9: All of 7 + compaction strategy + token budget
                                      10: All of 9 + automated session metrics
---------------------------------------------------------------------
OVERALL LEVERAGE               ?/60
```

Report both scores. Show exactly where effort yields the biggest return.

---

## Phase 3: Generate Config Files

Generate ONLY for tools the engineer uses (Phase 0 answers). All content is generated inline from the instructions below — no external template files.

### Tool Selection Matrix

| Engineer Uses | Generate |
|---------------|----------|
| Any tool | AGENTS.md (always — universal baseline) |
| Claude Code | CLAUDE.md + subdirectory CLAUDE.md files + hooks + skills |
| Cursor | .cursor/rules/*.mdc with glob scoping |
| GitHub Copilot | .github/copilot-instructions.md + scoped instructions |
| Windsurf | .windsurf/rules/*.md |
| Gemini CLI | GEMINI.md |
| Aider | CONVENTIONS.md |

### Pain Point -> Content Priority

| Pain Point | Emphasize |
|------------|-----------|
| Wrong commands | Commands section FIRST, full flags |
| Breaks architecture | Landmines section, counterintuitive patterns |
| Wrong style | Hook recommendations (NOT prose rules) |
| Touches forbidden files | Never boundaries |
| Commits without asking | Ask First boundaries |
| Doesn't understand domain | Skills for domain knowledge |
| Wastes time exploring | .claudeignore + scoped rules |
| Forgets context | PostCompact hook + HANDOFF.md |

### 3.1 — AGENTS.md (Universal Standard)

ALWAYS generate. 25+ tools read it. Generate with these sections in order: Commands, Stack, Boundaries (Always/Ask First/Never), Landmines, Patterns.

**Rules:**
- MUST be under 200 lines (under 100 is better)
- MUST lead with executable commands (full flags)
- MUST use RFC 2119 language (MUST, SHOULD, NEVER)
- MUST NOT include directory trees, standard patterns, or README content
- MUST include three-tier boundaries (Always / Ask First / Never)
- Each line MUST pass: "Would removing this cause a mistake?"

### 3.2 — CLAUDE.md (Claude-Specific)

Only if engineer uses Claude Code. MUST be under 50 lines. Use @imports to reference AGENTS.md and docs — don't duplicate content.

### 3.3 — Multi-Level Hierarchy

Generate subdirectory config files ONLY for directories that exist. Agents only load these when working in that directory:

```
CLAUDE.md                  -> orientation (50-100 lines)
tests/CLAUDE.md            -> ONLY if tests/ or __tests__/ directory exists
src/CLAUDE.md              -> ONLY if src/ directory exists
src/api/CLAUDE.md          -> ONLY if src/api/ directory exists
docs/CLAUDE.md             -> ONLY if docs/ directory exists
```

**Before generating any subdirectory CLAUDE.md, verify the directory exists with Glob or Bash. Skip directories that don't exist.**

Each subdirectory file: 20-50 lines MAX. Only what's relevant to that directory.

**Monorepo heuristic:** Create one subdirectory file per major concern that has DISTINCT rules. If the rules would be the same as the parent, don't split — the parent covers it. Production data: selectools used 3 subdirs (tests/, src/, docs/), saas-platform used 6 (web/, api/, tests/, agents/, products/, supabase/). Stop splitting when additional files would just repeat the parent's content.

### 3.4 — Tool-Specific Configs

**Cursor** (.cursor/rules/*.mdc):
```yaml
---
description: [When this applies]
globs: "[file pattern]"
alwaysApply: false
---
[Focused instructions, <80 lines, one concept per rule]
```

**Copilot** (.github/copilot-instructions.md + .github/instructions/*.instructions.md):
- Main file references AGENTS.md content
- Scoped files with `applyTo:` glob frontmatter

**Others**: Generate appropriate format per tool.

---

## Phase 4: Set Up Progressive Disclosure

Create the full disclosure tree (only directories that exist):

```
repo/
  AGENTS.md                           # Universal (<200 lines)
  CLAUDE.md                           # Claude-specific (<50 lines, @imports)
  tests/CLAUDE.md                     # Testing scope (if tests/ exists)
  src/CLAUDE.md                       # Source scope (if src/ exists)
  docs/agent-context/                 # Detailed docs (read on-demand)
    architecture.md
    testing-guide.md
    api-conventions.md
  .cursor/rules/                      # Cursor scoped rules
  .github/copilot-instructions.md     # Copilot
  .claudeignore                       # Exclude irrelevant files
  HANDOFF.md                          # Session handoff document
```

---

## Phase 5: Set Up Hooks

Only if engineer opted in during Phase 0.

**IMPORTANT: Claude Code's security model prevents agents from writing to .claude/ directly.** Generate the hooks configuration JSON and either:
1. Present it to the user and instruct them to copy it into `.claude/settings.local.json`
2. Suggest they run the `update-config` skill which has the permissions to write settings

Set up these hooks adapted to the project's actual commands from Phase 1:

- **PostToolUse (Write|Edit)** — auto-format with project's formatter
- **PreToolUse (git push main)** — block direct pushes to main/master
- **PostCompact** — re-inject top 30 lines of CLAUDE.md + landmines after compaction (CRITICAL — solves "agent forgets rules"). NOTE: after fixing bugs, review PostCompact content and remove fixed landmines — stale landmines waste tokens and confuse agents.
- **PreToolUse (git commit)** — run lint + test before committing
- **SessionStart** — check if CLAUDE.md/AGENTS.md are older than 14 days. Show warning: "Agent configs may be stale — review or run /nv-context to refresh." This is the cheapest way to prevent config drift. Production-proven in selectools.

**Example hooks output to present to user:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "<project-formatter-command>"
      }
    ],
    "PreToolUse": [
      {
        "matcher": "git push.*main",
        "command": "echo 'BLOCKED: use a feature branch' && exit 1"
      }
    ],
    "PostCompact": [
      {
        "command": "head -30 CLAUDE.md"
      }
    ]
  }
}
```

Output the hooks configuration and instruct the user to apply it manually or use the `update-config` skill. Agents cannot write to `.claude/` directly.

**Batch mode persistence:** In batch mode, write the hooks config to a file `hooks-config.json` in the project root so it persists after the session ends. Include a note: "Run `mkdir -p .claude && cp hooks-config.json .claude/settings.local.json` to activate hooks."

---

## Phase 6: Set Up Session Management

Four deliverables:

1. **HANDOFF.md** — generate in the project root with sections: Current Task, Key Decisions, Open Questions, Files Modified, Next Steps. Recommend creating a `/handoff` skill that auto-populates from git state (branch, recent commits, test status) — proven effective in selectools.

2. **.claudeignore** — generate by analyzing .gitignore and repo structure. Include project-specific exclusions: build artifacts, binaries, lock files, vendor dirs, node_modules, .git, dist/, coverage/. For large repos, exclude landing pages, notebooks, and asset directories that aren't relevant to the primary development work.

3. **Document-and-Clear workflow** — add to CLAUDE.md:
   - "When context gets heavy (~40 messages): update HANDOFF.md, `/clear`, start fresh reading HANDOFF.md"
   - This outperforms auto-compaction (research-backed)

4. **Pitfalls placement decision** — if the project has many landmines/pitfalls (10+), present the tradeoff: keep them in root CLAUDE.md (100% activation, costs lines) vs move to @import PITFALLS.md (saves lines, ~79% activation). Let the engineer decide. Production data: selectools kept 26 pitfalls in root because they're the highest-value content.

---

## Phase 7: Set Up Compounding Engineering

Two deliverables:

1. **GitHub Action** — generate a workflow file at `.github/workflows/learn-from-reviews.yml` with the following behavior: when a reviewer tags `@claude-learn [rule]`, it auto-creates a PR adding that rule to AGENTS.md. The codebase learns from every review.

   **WARNING: This GitHub Action processes user input from PR comments. MUST sanitize the `@claude-learn` content before appending to AGENTS.md to prevent injection attacks. Strip shell metacharacters, limit line length to 200 chars, reject content containing backticks or `$()` or `${` sequences, and validate it matches a safe pattern (alphanumeric + basic punctuation only).**

   **Script injection prevention:** Use an intermediate environment variable instead of inline `${{ }}` in `run:` blocks to prevent script injection. Example: define `env: REVIEW_BODY: ${{ github.event.review.body }}` on the step, then reference `$REVIEW_BODY` in the shell script. NEVER interpolate `${{ }}` directly inside `run:` blocks.

2. **Living document reminder** — add to CLAUDE.md: "When you make a mistake a rule could have prevented: fix it, then add one line to AGENTS.md that prevents it."

---

## Phase 8: MCP + Skills Recommendations

### MCP Recommendations (with token budget awareness)

| Project Has... | Recommend | Token Cost |
|---------------|-----------|------------|
| Large codebase (>1000 files) | codebase-memory-mcp | ~2K tokens |
| External library deps | context7 | ~1K tokens |
| GitHub-hosted | github-mcp-server | ~3K tokens |
| Database | DB-specific MCP | ~2K tokens |
| Team conventions | codebase-context (PatrickSys) | ~2K tokens |

**WARN if total MCP token cost exceeds 15K** — that's eating into the task budget.

**Skip MCP recommendations for projects with fewer than 50 files or no external dependencies.** Small projects don't benefit from MCP overhead.

### Skill Recommendations

Based on engineer's recurring workflows (Phase 0), recommend skills:
- Feature development workflow
- Bug fix workflow
- Database migration workflow
- Deployment workflow
- Code review checklist
- Testing workflow

Each skill: under 150 lines, one clear purpose, exact commands.

---

## Phase 9: Negative Instruction Rewrite

Scan ALL generated and existing config files. Fix:

| Found | Rewrite To |
|-------|-----------|
| "don't use moment.js" | "MUST use date-fns for date operations" |
| "avoid raw SQL" | "MUST use the ORM query builder" |
| "do not import from index" | "MUST import from specific module files" |
| "don't mock the database" | "MUST use real database for integration tests" |

**Keep as-is:**
- "NEVER commit secrets" (absolute prohibition — fine)
- "NEVER push to main" (absolute prohibition — fine)
- "NEVER modify migration files" (absolute prohibition — fine)

The rule: soft negatives ("don't", "avoid", "do not") -> positive MUST statements. Hard negatives ("NEVER") stay.

---

## Phase 10: Quality Audit & Report

Run these checks on all generated files:

**Content:** Every line passes "would removing this cause a mistake?" | No directory trees | No README duplication | Commands have full flags | Three-tier boundaries present | RFC 2119 language | No soft negatives remain

**Length:** AGENTS.md <200 lines | CLAUDE.md <50 lines | Subdirectory files <50 lines | .mdc rules <80 lines | Skills <150 lines

**Token Budget Report:** Estimate tokens for system prompt (~2,500) + CLAUDE.md + AGENTS.md + skill descriptions + MCP tools. Report total baseline cost vs 128K window. HEALTHY = <40% used, WARNING = 40-60%, CRITICAL = >60%.

**Hierarchy of Leverage Report:** Score each layer 0-10 using the Phase 2 checklists (verification, CLAUDE.md, hooks, skills, subagents, session management). Show total out of 60. Recommend highest-impact improvement.

---

## Phase 11: Continuous Sync

Generate a pre-commit hook script inline (do not reference external files) that warns (non-blocking) when package files, CI configs, or lint configs change that may make agent configs stale. Also flags configs older than 14 days and detects soft negative instructions.

**Persist the script:** Write the sync script to `.githooks/nv-context-sync.sh` in the project directory (not just in memory). Add a note: "Run `chmod +x .githooks/nv-context-sync.sh && git config core.hooksPath .githooks` to activate."

Tell the engineer: "Run `/nv-context` anytime to re-analyze and refresh. The interview is skipped on re-runs."

---

## Output Format

Present results in this order:

1. **Your Setup Summary** — tool choices, pain points, preferences
2. **Maturity Score** — L-level before and after
3. **Hierarchy of Leverage Score** — per-layer scoring with gaps
4. **Token Budget Report** — how much context budget remains
5. **Generated Files** — each file with WHY specific content was included (tied to pain points)
6. **Hooks Configuration** — JSON to copy into settings, what each prevents
7. **Session Management** — HANDOFF.md, .claudeignore, Document-and-Clear workflow
8. **Compounding Engineering** — GitHub Action or manual process
9. **MCP Recommendations** — with token costs
10. **Negative Instructions Fixed** — before/after rewrites
11. **Bugs Found** — if the analysis surfaced real defects (common — saas-platform found 81 bugs during context engineering), report them
12. **What You Should Hand-Refine** — where domain knowledge is needed

For each file, connect to the analysis:
> "Included exact `pytest -x -q` command because CI uses it."
> "The 'Never' boundary includes `migrations/` because it's a landmine."
> "Split SESSION.md because it was a 17K token bomb — 80% historical build log."

ALWAYS end with the leverage score, then ask:

> "Current score: **X/60**. Want to push further? I can [specific next action that would gain the most points]. This would bring you to ~Y/60."

This "push further" prompt is critical. Production data shows:
- selectools went from 49/60 to 58/60 (+9) because the engineer asked "what can we improve further?"
- The second pass found deeper restructuring opportunities the first pass left as "good enough"
- Sheriff stayed at 42/60 because the incremental improvements were the right call for a solo dev

Present the option — don't stop at "good enough" unless the engineer decides to. The best results come from 2-3 passes, not one.

---

## Research Basis

Built on 200+ sources: Anthropic, ETH Zurich, Google DeepMind, Manus, GitHub (2,500-repo analysis), LangChain, JetBrains (NeurIPS 2025), METR, Boris Cherny, Dex Horthy, 40+ production CLAUDE.md files, Reddit/HN/GitHub Discussions. Full research: github.com/johnnichev/nv-context/research/logs/
