---
name: agentic-legibility-score
description: "Score any code repository 0-100 on Agentic Legibility — how effectively autonomous AI agents can navigate, understand, build, test, and contribute to the codebase. Use when the user asks to score, evaluate, audit, or assess a repo for agent readiness, agentic legibility, AI-friendliness, or wants to know how well their codebase supports autonomous AI development."
---

# Agentic Legibility Score

Score a repository 0-100 on how effectively AI agents can autonomously operate within it.

Agent failures are almost always environment failures. This skill evaluates the scaffolding, not the code.

## Evaluation Workflow

This is a **two-pass** process. The scanner catches common mechanical signals, but it uses hardcoded keywords and patterns that won't match every ecosystem. The second pass — your qualitative assessment — is where you actually read the repo and score what the scanner cannot see.

### Step 1: Mechanical Scan (Baseline)

Execute the scanner script against the target repository. Use whichever invocation matches your setup:

```bash
# If installed as a Claude/Copilot skill
python3 <skill-directory>/scripts/scan_repo.py /path/to/repo

# If cloned as a standalone repo
python3 scripts/scan_repo.py /path/to/repo

# If pip-installed
agentic-legibility-score /path/to/repo
```

If no specific repo is given, scan the current workspace root.

Capture the JSON output. Treat this as a **starting signal**, not a final score. The scanner checks for common file names, config patterns, and directory conventions — it will miss non-standard setups, custom build systems, alternative tools, and anything that doesn't match its hardcoded patterns.

### Step 2: Qualitative Assessment (You Read the Repo)

This is the critical step. For each category, actually read the relevant files and assess what the scanner missed or misjudged.

**What to read per category:**

| Category | Read These | What You're Looking For |
|---|---|---|
| 1. Bootstrap | README, Makefile/Justfile, any setup script | Are there clear setup instructions even if the tool names are non-standard? |
| 2. Entry Points | README, build configs, CI files, task runners | Can you identify how to build/test/lint even if it's not npm/make/pytest? |
| 3. Documentation | README, AGENTS.md, docs/, top-level .md files | Is the content *useful* or just boilerplate? Is there a real map? |
| 4. Architecture | ARCHITECTURE.md, ADRs, source tree structure | Does the code organization make sense? Are decisions explained? |
| 5. Testing | Test dirs, CI configs, test framework configs | Are tests meaningful and runnable, not just present? |
| 6. Code Quality | Linter/formatter configs, pre-commit hooks, CI | Are quality gates actually enforced, not just configured? |
| 7. Security | .gitignore, CI security steps, dependency management | Is the repo secure by default? |

**Adjustment rules for the second pass:**

- **Upgrade** a category if the scanner missed signals due to non-standard tooling but the capability exists (e.g., `build.zig` instead of `Makefile`, `deno.json` instead of `package.json`, a custom `run.sh` with clear build/test/lint targets)
- **Upgrade** if file *contents* show quality the scanner can't see (e.g., README has excellent setup docs but uses unfamiliar commands, CI runs extensive checks via a custom script)
- **Downgrade** if the scanner found files that are actually empty, boilerplate, stale, or misleading (e.g., `CONTRIBUTING.md` that just says "TBD", test files with no assertions, CI that's disabled)
- **Downgrade** if critical knowledge lives outside the repo (referenced Notion pages, "ask #team-platform on Slack", undocumented env vars)

### Step 3: Compute Final Scores

Read the detailed rubric at `references/scoring-rubric.md` for point breakdowns per sub-criterion.

For each category, combine the mechanical signals (Step 1) with your qualitative assessment (Step 2) to arrive at a final score:

| # | Category | Max | What It Measures |
|---|---|---|---|
| 1 | Bootstrap & Environment | 15 | Can an agent set up and run the project cold? |
| 2 | Entry Points & Commands | 15 | Can it find build/test/lint without guessing? |
| 3 | Documentation & Navigation | 20 | Is there a map? Can the agent find its way? |
| 4 | Architecture & Structure | 15 | Does it understand why things are where they are? |
| 5 | Testing & Validation | 15 | Can it verify changes without a human? |
| 6 | Code Quality Enforcement | 10 | Are quality gates automated and discoverable? |
| 7 | Security & Governance | 10 | Will it avoid introducing vulnerabilities? |

For each category, note where and why you adjusted from the scanner baseline. Transparency matters — the user should understand what was detected mechanically vs. what you assessed by reading the repo.

### Step 4: Generate the Scorecard

Present findings using this exact format:

```
╔══════════════════════════════════════════════════════════════════╗
║                  AGENTIC LEGIBILITY SCORECARD                   ║
║                     {repo_name}                                 ║
╚══════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────┬───────┬───────┬──────────┐
│ Category                            │ Score │  Max  │  Grade   │
├─────────────────────────────────────┼───────┼───────┼──────────┤
│ 1. Bootstrap & Environment          │  XX   │  15   │  ▓▓▓▓░░  │
│ 2. Entry Points & Commands          │  XX   │  15   │  ▓▓▓░░░  │
│ 3. Documentation & Navigation       │  XX   │  20   │  ▓▓▓▓▓░  │
│ 4. Architecture & Structure         │  XX   │  15   │  ▓▓░░░░  │
│ 5. Testing & Validation             │  XX   │  15   │  ▓▓▓▓░░  │
│ 6. Code Quality Enforcement         │  XX   │  10   │  ▓▓▓▓▓▓  │
│ 7. Security & Governance            │  XX   │  10   │  ▓▓▓░░░  │
╞═════════════════════════════════════╪═══════╪═══════╪══════════╡
│ TOTAL                               │  XX   │  100  │    ?     │
└─────────────────────────────────────┴───────┴───────┴──────────┘

GRADE: [A+/A/B/C/D/F/F-]  —  "{one-line verdict}"
```

Use 6-char progress bars: each ▓ = ~17% of category max. Round to nearest block.

### Step 5: Category Deep-Dives

For each category, output a findings block showing both mechanical and qualitative signals:

```
### {N}. {Category Name} — {score}/{max}

🔍 Scanner detected:
  • {signal from scan_repo.py output}
  • {signal from scan_repo.py output}

🧠 Qualitative assessment:
  • {what you found by reading the actual files}
  • {adjustments made and why — e.g. "Scanner missed build.zig but it clearly documents build/test/lint targets (+3)"}

✅ What's working:
  • {strength}

❌ What's missing:
  • {gap identified} — {why it matters for agents}

💡 Quick wins:
  • {specific actionable fix} (est. +X pts)
```

### Step 6: Executive Summary

Close with:

```
## Agentic Legibility Summary

**Score: XX/100 ({Grade})**

**What this means:** {2-3 sentence interpretation of what agents can/cannot
do in this repo based on the grade.}

**Top 3 Improvements (highest leverage):**
1. {action} → expected impact: +X pts
2. {action} → expected impact: +X pts
3. {action} → expected impact: +X pts

**Bottom line:** {One punchy sentence. Channel the spirit of
"None of this is glamorous. That is exactly why it matters."}
```

## Grade Scale Reference

| Score | Grade | Agent Capability |
|---|---|---|
| 90-100 | A+ | Full autonomous operation |
| 80-89 | A | High autonomy, minimal guidance needed |
| 70-79 | B | Moderate autonomy, guidance for complex tasks |
| 60-69 | C | Limited autonomy, basic maintenance only |
| 40-59 | D | Minimal autonomy, frequent stalling |
| 20-39 | F | Mostly unable to operate |
| 0-19 | F- | Opaque to agents |

## Sources

- [Agent Legibility Scoring](https://seand.ai/blog/agent-legibility-scoring/) — seand.ai (2026)
- [Harness Engineering](https://openai.com/index/harness-engineering/) — OpenAI (2025)
