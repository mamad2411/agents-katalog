---
name: test-framework
allowed-tools: Bash, Read, Glob, Grep
description: >
  Four-layer test framework for Claude Code plugin skills. Use when validating
  plugin structure, testing trigger accuracy of skill descriptions, running
  multi-turn session scenarios, or comparing skill value (with vs without).
  Also use when creating new trigger evals, session scenarios, or debugging
  why a skill fires for the wrong prompts. NOT for writing unit tests, running
  pytest, or testing application code — this is for testing AI plugin skills only.
---

# Skill Test Framework

Test framework for validating Claude Code plugin skills across four layers:
structure, trigger accuracy, session behavior, and skill value.

## Why AI plugins need different testing

Traditional testing verifies deterministic behavior. AI plugin skills are
probabilistic — the same prompt can trigger different skills across runs,
routing is inferred not explicit, quality degrades silently, and models
improve over time (making skills redundant). This framework addresses all
four failure modes.

## Four-Layer Testing Model

| Layer | What it tests | Speed | Script |
|-------|--------------|-------|--------|
| **L1 Structure** | Plugin spec compliance, naming, cross-refs | ~0.1s | `validate.py` |
| **L2 Triggers** | Skill description accuracy (precision/recall) | ~30s/query | `run_trigger_eval.py` |
| **L3 Sessions** | Multi-turn routing, context, boundaries | 2-3 min | `session_test.py` |
| **L4 Value** | Does the skill actually help? (with vs without) | 5+ min | `compare_skill.py` |

## Quick Start

All scripts live in `skills/test-framework/scripts/` and accept a `--root`
flag pointing to the plugin directory being tested (defaults to cwd).

```bash
# L1: Validate plugin structure
uv run skills/test-framework/scripts/validate.py --root .

# L1: Validate a specific skill
uv run skills/test-framework/scripts/validate.py --root . skills/my-skill/

# L2: Dry-run trigger eval (validate eval set structure)
uv run skills/test-framework/scripts/run_trigger_eval.py \
    --eval-set tests/evals/triggers/my-skill.json \
    --skill-path skills/my-skill \
    --dry-run

# L2: Run trigger eval against claude
uv run skills/test-framework/scripts/run_trigger_eval.py \
    --eval-set tests/evals/triggers/my-skill.json \
    --skill-path skills/my-skill \
    --runs-per-query 3

# L3: Run a session scenario
uv run skills/test-framework/scripts/session_test.py \
    --scenario tests/evals/scenarios/my-workflow.json \
    --verbose

# L4: Compare skill value (with vs without)
uv run skills/test-framework/scripts/compare_skill.py \
    --skill my-skill \
    --scenario tests/evals/scenarios/my-workflow.json \
    --runs 3 --verbose

# All layers for one skill
uv run skills/test-framework/scripts/test_skill.py my-skill

# Test inventory
uv run skills/test-framework/scripts/test_skill.py --inventory
```

## L1: Structure Validation

Validates `.claude-plugin/plugin.json`, agents, skills, commands, MCP config,
and cross-references.

**What it checks:**
- `.claude-plugin/plugin.json` — required fields, semver, agent path references
- `.mcp.json` — server configs have command/url (optional)
- `CLAUDE.md` — exists with meaningful content (optional but recommended)
- **Agents** — frontmatter has name + description, names are lowercase
- **Skills** — SKILL.md exists, name matches directory, description 20-1024 chars
- **Commands** — files are non-empty, have description in frontmatter
- **Cross-references** — agents in plugin.json exist, no name collisions
- **Orphans** — skill directories without SKILL.md

```bash
uv run skills/test-framework/scripts/validate.py --root . --json
```

## L2: Trigger Accuracy

Tests whether a skill's description causes Claude to activate for the right
prompts. See [eval-schemas.md](reference/eval-schemas.md) for JSON format.

### Creating trigger evals

Create `tests/evals/triggers/{skill-name}.json`:

```json
{
  "skill_name": "my-skill",
  "evals": [
    {"query": "realistic prompt that should trigger this skill", "should_trigger": true},
    {"query": "near-miss prompt that should NOT trigger", "should_trigger": false}
  ]
}
```

**Guidelines:**
- 8-10 should-trigger queries (different phrasings, edge cases)
- 8-10 should-NOT-trigger queries (near-misses, adjacent domains)
- Queries must be realistic and specific (min 10 chars)

### Interpreting results

| Metric | Meaning |
|--------|---------|
| **Precision** | When the skill triggers, how often is it correct? |
| **Recall** | When the skill should trigger, how often does it? |
| **Accuracy** | Overall correct rate |

Low recall = description too narrow. Low precision = description too broad.

## L3: Session Scenarios

Tests multi-turn context, routing accuracy, and skill boundaries.

### Creating scenarios

Create `tests/evals/scenarios/{name}-workflow.json`:

```json
{
  "name": "my-skill-workflow",
  "description": "Test my-skill routing and context",
  "ready_pattern": "❯|\\$|>",
  "steps": [
    {
      "name": "basic-query",
      "prompt": "what does my-skill handle?",
      "timeout": 90,
      "pause_after": 3,
      "assertions": [
        {"pattern": "expected-keyword", "type": "contains", "description": "Routes correctly"},
        {"pattern": "wrong-skill-keyword", "type": "not_contains", "description": "Does NOT invoke wrong skill"}
      ]
    }
  ]
}
```

**Assertion types:** `contains`, `regex`, `not_contains`

**Safety:** Prompts must be read-only. Action verbs (create, delete, push, deploy)
are blocked automatically when running with `--dangerously-skip-permissions`.

## L4: Skill Value Comparison

Measures whether a skill actually helps by running the same scenario with and
without the skill loaded.

### Verdicts

| Verdict | Delta | Action |
|---------|-------|--------|
| **VALUABLE** | >+10% | Keep the skill |
| **MARGINAL** | +1-10% | Review if context cost is worth it |
| **REDUNDANT** | ~0% (both high) | Model already knows this — consider removing |
| **INEFFECTIVE** | ~0% (both low) | Rewrite — skill isn't helping |
| **HARMFUL** | Negative | Remove or rewrite — skill makes things worse |

### When to run comparisons

- After editing a skill's instructions
- When upgrading the underlying model
- Quarterly to prune redundant skills
- Before adding a new skill (baseline first)

## Using the Makefile

Copy the Makefile to your plugin root or use ROOT to point at your plugin:

```bash
make test                              # L1 + L2 (fast)
make lint ROOT=/path/to/plugin         # L1 only
make integration S=my-skill            # L3 for one skill
make benchmark S=my-skill              # L4 for one skill
make report ROOT=/path/to/plugin       # Test inventory
make test-skill S=my-skill             # All layers
```

## Adding Tests for a New Skill

1. Create the skill (`skills/{name}/SKILL.md`)
2. Run `validate.py` to check structure
3. Create trigger evals (`tests/evals/triggers/{name}.json`) — 8+ positive, 8+ negative
4. Run trigger eval dry-run to validate the eval set
5. Create a session scenario (`tests/evals/scenarios/{name}-workflow.json`)
6. Run `test_skill.py {name}` to verify all layers

## Reference

- [eval-schemas.md](reference/eval-schemas.md) — JSON schemas for trigger evals, scenarios, benchmarks
