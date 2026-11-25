---
name: harness-optimizer
description: "Diagnose and improve Claude Code harness configurations based on Anthropic's harness design principles. Analyzes skills/, agents/, commands/, hooks/, plugin.json, CLAUDE.md, .mcp.json, and settings.json for 8 design principles: evaluator separation, context management, task decomposition, evaluation criteria, structured handoff, harness simplification, sprint contract, and feedback loop. Supports both plugin projects (with plugin.json) and non-plugin projects (CLAUDE.md + .claude/ only). Uses 2-layer diagnostics: Layer 1 signal collection via Grep/Glob, Layer 2 semantic judgment by LLM. Outputs PASS/FAIL/PARTIAL checklist with per-principle scores, health grade, and auto-fix suggestions. Triggers: 'harness optimizer', 'harness 진단', 'optimize harness', 'diagnose harness', 'harness health', 'check my harness', 'harness design', 'improve harness', '하네스 최적화', '하네스 점검', '하네스 개선', 'check harness', 'harness check', 'harness review', '하네스 리뷰'. Use this skill whenever the user mentions harness quality, agent pipeline improvement, or wants to evaluate their multi-agent setup, even if they don't explicitly say 'harness'."
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion]
---

# Harness Optimizer

Diagnose and improve your Claude Code harness configuration based on 8 design principles from Anthropic's "Harness design for long-running application development." This skill scans your project's plugin components, grades each principle with a 2-layer diagnostic (signal collection + semantic judgment), and offers tiered auto-fixes.

## Flag Parsing

Parse `$ARGUMENTS` for these flags:

| Flag | Effect |
|------|--------|
| `--dry-run` | Analyze and show proposed changes without modifying any files |
| `--report-only` | Output diagnostic report only, skip auto-fix phases |
| `--path <path>` | Target project path (defaults to current working directory) |
| `--help` | Display usage information and exit |

## Workflow

### Phase 0: Setup

1. **Detect language** from user message or system locale (Korean/English)
2. **Resolve target path** from `--path` flag or current working directory
3. **Check minimum requirements:**
   - Look for `CLAUDE.md` OR `.claude/` directory in the target path
   - If neither exists, display an informative message (not an error) and exit gracefully:
     > "This project doesn't appear to have a Claude Code configuration (no CLAUDE.md or .claude/ directory found). Create a CLAUDE.md to get started, then run this diagnostic again."
4. **Scan components** using `scripts/scan-components.mjs`:
   ```bash
   node "$(dirname "$SKILL_PATH")/scripts/scan-components.mjs" "<target_path>"
   ```
   If Node.js is unavailable, fall back to manual scanning with Glob:
   - `Glob("skills/*/SKILL.md")` and `Glob(".claude/skills/*/SKILL.md")`
   - `Glob("agents/*.md")` and `Glob(".claude/agents/*.md")`
   - `Glob("commands/*.md")` and `Glob(".claude/commands/*.md")`
   - `Glob("hooks/*")` and check for `hooks.json`
   - Check existence of `plugin.json`, `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`
5. **Determine project type:** `isPlugin = true` if `plugin.json` exists
6. If `--help` flag is present, display usage and exit

### Phase 1: Component Discovery

Present the scan results to the user:

```
## Project Scan Results

| Component | Count | Detected |
|-----------|-------|----------|
| Skills | {n} | {paths} |
| Agents | {n} | {paths} |
| Commands | {n} | {paths} |
| Hooks | {n} | {paths} |
| plugin.json | {yes/no} | |
| CLAUDE.md | {yes/no} | {line count} |
| .mcp.json | {yes/no} | |
| settings.json | {yes/no} | |

**Project type:** {Plugin / Non-plugin (CLAUDE.md + .claude/)}
**Total components:** {n}
```

If `isPlugin=false`, note that plugin-specific diagnostics (plugin.json analysis) will be skipped.

### Phase 2: Principle Diagnostics (2-Layer)

For each of the 8 principles, perform a 2-layer diagnostic. Read `references/principles-checklist.md` for the detailed check logic for each principle.

**Layer 1 — Signal Collection:**
- Run the Grep/Glob patterns specified in `references/principles-checklist.md` for the current principle
- Record all matches as a signal list (file path, line number, matched content)
- DO NOT make any PASS/FAIL/PARTIAL judgment at this layer — collect signals only

**Layer 2 — Semantic Judgment:**
- Read the actual content of files identified in Layer 1 signals
- Apply the Layer 2 judgment guidelines from `references/principles-checklist.md`
- Determine: PASS (7-10), PARTIAL (3-6), or FAIL (0-2) with specific evidence
- A keyword match alone is never sufficient for PASS. The principle must be meaningfully implemented.

**The 8 Principles:**

| # | Principle | Weight | Key Question |
|---|-----------|--------|-------------|
| 1 | Evaluator Separation | 20% | Are generator and evaluator agents separated? |
| 2 | Context Management | 15% | Is there a context reset/compaction strategy? |
| 3 | Task Decomposition | 15% | Are complex tasks broken into manageable units? |
| 4 | Evaluation Criteria Design | 10% | Are subjective qualities converted to measurable criteria? |
| 5 | Structured Handoff | 10% | Is agent context transfer via files/artifacts? |
| 6 | Harness Simplification | 7% | Is unnecessary scaffolding removed? |
| 7 | Sprint Contract | 8% | Are "done" criteria defined before work starts? |
| 8 | Feedback Loop | 15% | Do evaluation results feed back to the generator? |

### Phase 3: Health Report

Present the diagnostic results:

```
## Harness Health Report

| # | Principle | Status | Score | Weight | Weighted | Evidence |
|---|-----------|--------|-------|--------|----------|----------|
| 1 | Evaluator Separation | {PASS/FAIL/PARTIAL} | {0-10} | 20% | {s*w} | {brief evidence} |
| ... | ... | ... | ... | ... | ... | ... |
| | **Health Score** | | | | **{total}/100** | |
| | **Grade** | | | | **{grade}** | |

Grade scale: Excellent (80-100), Good (60-79), Fair (40-59), Poor (20-39), Critical (0-19)
```

**Calculate health score inline:**
```
Health Score = (P1×0.20 + P2×0.15 + P3×0.15 + P4×0.10 + P5×0.10 + P6×0.07 + P7×0.08 + P8×0.15) × 10
```

Refer to `references/scoring-system.md` for score ranges and grade definitions.

**Save a Before snapshot in memory** (do not write to file):
```json
{
  "timestamp": "<ISO 8601>",
  "scores": [{"principle": "<id>", "status": "<PASS|FAIL|PARTIAL>", "score": 8, "evidence": ["..."]}],
  "healthScore": 72.5,
  "grade": "Good",
  "componentCount": 12,
  "isPlugin": true
}
```

If `--report-only` flag is set, stop here.

### Phase 4: Auto-Fix Tier 1 (Existing File Modifications)

Read `references/autofix-catalog.md` for the specific Tier 1 fixes for each FAIL/PARTIAL principle.

Tier 1 fixes modify existing files only (prompts, settings, configuration). They do not create new files.

1. Collect all applicable Tier 1 fixes based on FAIL/PARTIAL results
2. Present them to the user with `AskUserQuestion`:
   > "Found {n} Tier 1 improvements (existing file modifications). Apply all / Select individually / Skip?"
3. If `--dry-run`, show proposed diffs without applying
4. Apply approved changes using Edit tool

### Phase 5: Auto-Fix Tier 2 (New File Creation)

Read `references/autofix-catalog.md` for Tier 2 fixes.

Tier 2 fixes create new files (agents, hooks, skill templates). These always require explicit user confirmation.

1. Collect applicable Tier 2 fixes
2. Present each with a preview of what will be created:
   > "Tier 2: Create evaluator agent template at agents/evaluator.md? [Preview below]"
3. If `--dry-run`, show file contents that would be created without creating them
4. Create approved files using Write tool
5. For complex skill creation, suggest: "For a full-featured skill, consider using `/skill-creator`"

### Phase 6: Verification

1. Re-run a lightweight Phase 2 diagnostic (only for principles that had fixes applied)
2. Generate an After snapshot in the same schema as Phase 3
3. Present Before/After comparison:

```
## Before/After Comparison

| Principle | Before | After | Change |
|-----------|--------|-------|--------|
| Evaluator Separation | FAIL (2) | PARTIAL (5) | +3 |
| ... | ... | ... | ... |
| **Health Score** | **{before}** | **{after}** | **{delta}** |
| **Grade** | **{before}** | **{after}** | |
```

## Reference Files

- **`references/principles-checklist.md`** — Detailed 2-layer diagnostic logic for each principle: Layer 1 Grep/Glob patterns and Layer 2 semantic judgment guidelines. Read the relevant principle section during Phase 2.
- **`references/scoring-system.md`** — Score ranges (PASS 7-10, PARTIAL 3-6, FAIL 0-2), weight table, health score formula, and grade definitions.
- **`references/autofix-catalog.md`** — Tier 1 and Tier 2 fix catalog with Before/After examples for each principle. Read during Phase 4/5.
- **`references/harness-article-summary.md`** — Key insights from the original Anthropic article, organized by principle. Useful for explaining WHY each principle matters to the user.
