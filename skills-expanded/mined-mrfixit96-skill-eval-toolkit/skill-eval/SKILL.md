---
name: skill-eval
description: >
  Reference knowledge about the skill evaluation framework — tiers, scoring rubrics, judge
  criteria, and improvement methodology. Use when the user asks about "skill eval", "evaluation
  tiers", "how skills are scored", "lint score", "trigger coverage", "A/B judge", "effectiveness
  eval", "skill quality", "eval framework", "improvement cycle", "diagnose research fix validate",
  "skill testing", or "content depth scorecard".
---

# Skill Evaluation Framework

A 3-tier evaluation system for measuring Copilot CLI skill quality, from free structural checks to LLM A/B judging.

## Architecture

- **Tier 1 (Free)**: Structural lint + content depth scoring + trigger keyword coverage — runs on every push
- **Tier 2 (Light API)**: Semantic trigger evaluation — LLM judges whether skill descriptions activate correctly
- **Tier 3 (Heavy API)**: A/B effectiveness comparison — LLM judges skill-augmented responses vs baseline
- **Results**: All stored in `results/` as versioned JSON; improvement docs as `improve-{skill}-v{N}.md`
- **CI**: GitHub Agentic Workflows (`gh aw`) run Tier 1 on push/PR, full 3-tier eval weekly or on-demand
- **Orchestrator**: `skill-eval-orchestrator` evaluates the fleet and dispatches `skill-improver` workers
- **GEPA**: Evolutionary optimizer uses LLM reflection on judge reasoning (ASI) to evolve skills

## Tier 1: Structural Quality

### Lint (`scripts/lint-skills.py`)

Checks every skill for structural correctness:
- YAML frontmatter between `---` fences with `name` and `description` fields
- `description` contains trigger keywords (quoted phrases users would say)
- Body content exists and is substantial
- References to `references/` files resolve correctly
- No orphaned files

**Pass/fail**: Binary per skill. All must pass.

### Content Depth Score (`scripts/score-skills.py`)

Scores each skill 0–100 across 8 dimensions:

| Dimension | Max | What It Measures |
|-----------|-----|-----------------|
| Frontmatter (FM) | 10 | Valid YAML, name, description present |
| Triggers (Trig) | 15 | Keyword density and specificity in description |
| Body (Body) | 15 | Word count, section coverage, depth |
| Code (Code) | 15 | Number and quality of code examples |
| References (Refs) | 15 | Links to reference modules, external sources |
| Examples (Ex) | 10 | Worked examples with context |
| Sources (Src) | 10 | Citations to official documentation |
| Clean (Clean) | 10 | No TODOs, no placeholder text, consistent style |

**Thresholds**: ≥50 = pass, ≥80 = good, 100 = excellent. Fleet average target: ≥95.

### Trigger Coverage (`scripts/trigger-coverage.py`)

Tests skill descriptions against curated query sets in `tests/trigger-coverage.json`:
- Each skill has mapped test queries (positive triggers)
- Checks that skill description keywords would match
- Reports coverage percentage per skill

## Tier 2: Semantic Trigger Evaluation

**Script**: `scripts/eval-trigger-semantic.py`
**Cost**: ~7 API calls per run
**Requires**: `MODELS_PAT` environment variable

An LLM judges: "Given this user query, would this skill's description cause it to be selected?"

- Tests each skill against its positive queries AND cross-skill negative queries
- Measures precision (no false activations) and recall (no missed activations)
- Catches subtle description issues that keyword matching misses

## Tier 3: LLM A/B Effectiveness

### Quality Judge (`scripts/eval-skill-quality.py`)
Scores individual skill content quality on a rubric.

### Effectiveness Comparison (`scripts/eval-skill-effectiveness.py`)
**Cost**: ~75+ API calls (3 per skill × 25 skills)
**Requires**: `MODELS_PAT` environment variable

Side-by-side A/B test:
- **Response A**: LLM answers a query with the skill injected as context
- **Response B**: LLM answers the same query with no skill (baseline)
- **Judge**: Third LLM rates which response is more helpful, accurate, and complete

**Outcomes per skill**: Win (skill helped), Loss (skill hurt), Tie
**Target**: ≥80% win rate across the fleet

## The Improvement Cycle

When a skill fails Tier 3, follow this process:

### 1. Diagnose
- Read `results/effectiveness-*.json` for judge reasoning
- Classify failure: inaccuracy (HIGH), missing content (HIGH), insufficient depth (MEDIUM), poor examples (MEDIUM)
- Identify specific SKILL.md sections affected

### 2. Research
- Fetch official documentation for the technology
- Verify every fact before editing
- Save notes to `results/research-{topic}.md`

### 3. Fix
- Surgical edits only — change what the diagnosis identified
- Add content near related existing content
- Code examples must be complete and runnable
- Preserve all working content

### 4. Validate
- Run Tier 1: `python scripts/lint-skills.py && python scripts/score-skills.py`
- Confirm lint passes and score maintained/improved
- Commit with descriptive message

## Common Pitfalls

- **Guessing instead of researching**: Never add technical content without verifying against official docs first
- **Over-editing**: Only fix what the judge criticized — don't reorganize or rewrite working sections
- **Incomplete code examples**: Fragments that can't run hurt more than help — always provide complete, annotated examples
- **Ignoring the judge quote**: The verbatim judge reasoning is the most important diagnostic signal — read it carefully

## Success Criteria

- [ ] All 25 skills pass Tier 1 lint
- [ ] Fleet average score ≥ 95/100
- [ ] Tier 3 win rate ≥ 80% (ideally ≥90%)
- [ ] No HIGH-severity inaccuracies in any skill
- [ ] Every improvement is backed by research documentation

## Agentic Workflows (CI/CD)

The eval framework runs autonomously via GitHub Agentic Workflows (`gh aw`):

| Workflow | Trigger | What It Does |
|----------|---------|-------------|
| `skill-lint` | push, PR, manual | Tier 1 lint + score + triggers, comments on PRs |
| `skill-eval` | weekly, manual | Full 3-tier eval, creates issue report |
| `skill-improver` | issue label, manual | Autonomous diagnose → research → fix → validate, creates PR |
| `skill-eval-orchestrator` | weekly, manual | Fleet-wide eval, dispatches `skill-improver` per failing skill |
| `gepa-evaluator` | manual | GEPA fitness function — wraps eval scripts with ASI extraction |
| `gepa-optimizer` | manual | Evolutionary search — evolves SKILL.md via Pareto selection |

### GEPA (Genetic-Pareto Optimization)

GEPA replaces the manual improvement cycle with automated evolution:
- **ASI (Actionable Side Information)**: Judge reasoning from Tier 3 eval — tells the LLM exactly what to fix
- **Mutation**: LLM reads ASI and proposes targeted edits (not random changes)
- **Selection**: Multi-objective Pareto dominance across score, triggers, win rate, lint
- **Stop condition**: score ≥95, lint pass, 100% triggers, ≥90% win rate

## Key Files

- `scripts/lint-skills.py` — Tier 1 structural lint
- `scripts/score-skills.py` — Tier 1 content depth scoring
- `scripts/trigger-coverage.py` — Tier 1 trigger keyword coverage
- `scripts/eval-trigger-semantic.py` — Tier 2 semantic trigger eval
- `scripts/eval-skill-quality.py` — Tier 3 quality judge
- `scripts/eval-skill-effectiveness.py` — Tier 3 A/B effectiveness
- `tests/trigger-coverage.json` — Test queries (dict keyed by skill name)
- `results/effectiveness-*.json` — Eval result history
- `results/improve-*.md` — Improvement documentation
- `results/research-*.md` — Research notes
- `.github/workflows/skill-*.md` — Agentic workflow definitions
- `.github/workflows/gepa-*.md` — GEPA evolutionary workflows
- `.github/workflows/shared/` — Shared imports (tools, knowledge, config)
- `SKILL_TEMPLATE.md` — Reference skill template
- `SKILL_TEMPLATE_TASK.md` — Task skill template
