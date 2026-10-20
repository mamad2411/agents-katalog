# Feedback Processor Skill

Process Carmen's bug feedback for Pipeline 1. Generates and applies code fixes.

## When to Use

Activate this skill when:
- User says "process feedback FB-XXX"
- User says "fix projection XXX"
- User mentions a feedback JSON file
- User asks to validate or fix a projection bug
- Working with `feedback/` directory files

## Quick Commands

| User Says | Action |
|-----------|--------|
| "Process feedback FB-001" | Full workflow: validate → analyze → fix → commit |
| "Fix projection aegonai__locked" | Analyze failure → generate fix → apply |
| "Validate FB-001" | Check feedback JSON without processing |
| "List failed projections" | Show projections with issues |
| "Show report FB-001" | Display generated report |

---

## Complete Workflow

### Phase 1: Validate Feedback

**Command:**
```bash
uv run python main.py validate feedback/FB-XXX.json
```

**Critical Checks:**
- `validated_by` MUST equal "Miquel" → Block if missing!
- `validation_date` format: YYYY-MM-DD
- Minimum 2 user addresses for testing
- Debank URL and expected_values required

**On Failure:** Tell Carmen exactly what's missing. Do NOT proceed.

### Phase 2: Analyze Projection Failure

**Parse projection:**
```bash
uv run python src/scripts/feedback_tool/projection_parser.py projections/{name}
```

**Read failure details:**
- `projections/{name}/pool_1/final_output.json` - What P1 produced
- `projections/{name}/pool_1/discovery_process/input_selected.json` - Expected values

**Compare:**
```
Expected (from Debank):
- Supply tokens: {from input_selected.json}
- Unlock at: {from input_selected.json}

Actual (P1 output):
- Supply tokens: {from final_output.json}
- Discovery rate: {from final_output.json}
```

### Phase 3: Read P1 Source Code

Based on module type, read relevant files:

| Module | Files to Read |
|--------|---------------|
| locked/vesting | `src/generators/pattern_detector.py`, `pattern_utils.py` |
| staking | `src/generators/pattern_utils.py` |
| lending | `src/generators/formula_engine.py` |
| yield/farming | `src/pipeline/stages/stage_05_watcher.py` |
| dex | `src/generators/pool_gen.py` |

Also check:
- `src/llm/prompts/context.py` - LLM context building
- `src/llm/prompts/templates.py` - Prompt templates

### Phase 4: Identify Bug

Common bug types:

| Symptom | Bug Type | Fix Location |
|---------|----------|--------------|
| `discovery_rate: 0%` | Pattern not detected | `pattern_detector.py` |
| `unlock_at: null` | Unlock not found | `pattern_utils.py` |
| `supply_token_list: []` | Token not discovered | `stage_05_watcher.py` |
| Wrong values | Formula wrong | `formula_engine.py` |

### Phase 5: Generate & Apply Fix

1. **Create branch:**
```bash
git checkout -b fix/FB-XXX-{protocol}-{module}
```

2. **Edit the file(s)** using Edit tool

3. **Commit:**
```bash
git add -A
git commit -m "fix(FB-XXX): Description of the fix"
```

### Phase 6: Report to Carmen

```
=== FIX COMPLETE ===

Branch: fix/FB-XXX-{protocol}-{module}

Changes:
- File: src/generators/{file}.py
- Fix: {description}

NEXT STEPS:
1. Send this branch to Miquel
2. Miquel runs Pipeline 1 with the fix
3. Check new output matches Debank
4. If all good, merge to main
```

---

## P1 Source Code Reference

### Pattern Detection
```
src/generators/
├── pattern_detector.py    ← Main pattern detection class
├── pattern_utils.py       ← Helper functions (token coverage, unlock_at)
└── pattern_types.py       ← Pattern type definitions
```

### Formula Engine
```
src/generators/
└── formula_engine.py      ← JSON to TypeScript translation
```

### Pipeline Stages
```
src/pipeline/stages/
├── stage_00_input.py      ← Input validation
├── stage_05_watcher.py    ← Watcher generation (token discovery)
└── stage_06_optimization/ ← LLM optimization loop
```

### LLM Prompts
```
src/llm/prompts/
├── context.py             ← Context building for LLM
└── templates.py           ← Jinja2 templates
```

---

## CLI Reference

```bash
# Parse projection
uv run python src/scripts/feedback_tool/projection_parser.py projections/{name}

# List failed projections
uv run python src/scripts/feedback_tool/projection_parser.py

# Validate feedback
uv run python main.py validate feedback/FB-XXX.json

# Process feedback
uv run python main.py process feedback/FB-XXX.json

# Run tests
uv run pytest tests/test_feedback_tool.py -v
```

---

## Safety Rules

### NEVER:
- Process without Miquel validation
- Commit directly to main
- Skip reading the source code before fixing
- Make up data - always read from files

### STOP If:
- Validation fails
- Can't identify the bug clearly
- Fix requires major architectural changes
- Multiple files need complex changes

---

## File Locations

| What | Where |
|------|-------|
| Projections | `projections/{protocol}__{module}/` |
| P1 Source | `src/generators/`, `src/pipeline/` |
| Feedback | `feedback/FB-XXX.json` |
| Reports | `feedback_reports/` |
| Parser | `src/scripts/feedback_tool/projection_parser.py` |

---

## Carmen's 3-Step Process

1. **Create:** Run `/new-feedback` → Answer questions → Get Miquel validation
2. **Fix:** Run `/process-feedback FB-XXX` or `/fix-projection {name}`
3. **Verify:** Send branch to Miquel → Check new output → Merge if good
