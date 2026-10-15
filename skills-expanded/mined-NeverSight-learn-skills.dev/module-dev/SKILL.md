---
name: module-dev
description: Spawn Verifier/Judge/Dev agents to fix DSP module quality issues
argument-hint: <module-name> [--auto]
---

# Module Dev Agent Loop for $ARGUMENTS

## Auto-Fix Mode

If `--auto` is passed, enable automatic fix application:
```
/module-dev ModuleName --auto
```

In auto mode:
1. Verifier detects issues
2. Judge classifies issues as auto-fixable or manual
3. AutoFixer applies template-based fixes automatically
4. Re-verify after fixes
5. If still failing after 3 auto-fixes, request manual intervention

## Workflow

Run this loop until module passes or 5 iterations:

### Step 1: Spawn Verifier

Use the Task tool:
- subagent_type: "module-dev:verifier"
- description: "Verify $ARGUMENTS"
- prompt: "Verify the $ARGUMENTS module. Return metrics and verdict."

### Step 2: Check Result

- If PASS: Done! Report success.
- If NEEDS_WORK/CRITICAL_ISSUES: Continue.

### Step 3: Spawn Judge

Use the Task tool:
- subagent_type: "module-dev:judge"
- description: "Judge $ARGUMENTS"
- prompt: "Evaluate these verification results and generate fix instructions:\n\n{VERIFIER_OUTPUT}"

### Step 4: Apply Fix

Either:
- Apply simple fixes yourself (edit test_config.json or .dsp file)
- Or spawn Dev agent for complex fixes:
  - subagent_type: "module-dev:dev"
  - description: "Fix $ARGUMENTS"
  - prompt: "Apply this fix to $ARGUMENTS:\n\n{JUDGE_OUTPUT}"

### Step 5: Loop

Go back to Step 1 until PASS or 5 iterations.

## Quick Reference - Just Commands

| Command | Purpose |
|---------|---------|
| `just build` | Build the plugin |
| `just validate-modules $ARGUMENTS` | Run module tests |
| `just validate-audio $ARGUMENTS` | Audio quality (THD, clipping) |
| `just test-ai-clap $ARGUMENTS` | CLAP embedding analysis |
| `just validate $ARGUMENTS` | Full validation suite |
| `just analyze-ranges $ARGUMENTS` | Parameter range analysis |
| `just install` | Install to VCV Rack |

## Common Fixes

| Issue | Fix Location | Solution |
|-------|--------------|----------|
| High THD (intentional) | test_config.json | Raise `thd_max_percent` |
| Clipping | .dsp file | Add `ma.tanh : *(0.7)` |
| DC offset | .dsp file | Add `fi.dcblocker` |
| Clicks | .dsp file | Add `si.smooth(0.995)` |
| Parameter no effect | test_config.json | Add to `parameter_sweeps.exclude` |

## Pass Thresholds

| Metric | Default Threshold | Notes |
|--------|-------------------|-------|
| Build | Must succeed | No errors |
| Clipping | <5% | Or module-specific in test_config.json |
| Quality Score | >=70 | Combined metric |
| THD | <15% | Higher OK for distortion effects |
| HNR | >0 dB | Harmonic-to-noise ratio |

## Key Files

- **DSP source:** `src/modules/$ARGUMENTS/{lowercase}.dsp`
- **Test config:** `src/modules/$ARGUMENTS/test_config.json`
- **C++ wrapper:** `src/modules/$ARGUMENTS/$ARGUMENTS.cpp`

## Auto-Fix Templates

The AutoFixer supports these template-based fixes:

| Fix Type | Target | What It Does |
|----------|--------|--------------|
| `add_limiter` | .dsp | Adds `ma.tanh` soft limiter before output |
| `reduce_gain` | .dsp | Reduces output gain by factor (default 0.7) |
| `add_dc_blocker` | .dsp | Adds `fi.dcblocker` to output |
| `smooth_gate` | .dsp | Adds `si.smooth(0.995)` to gate parameter |
| `adjust_threshold` | test_config.json | Raises THD/clipping thresholds |

To manually apply a fix:
```bash
just agent-fix-preview ModuleName add_limiter  # Preview
just agent-fix-apply ModuleName add_limiter    # Apply
```

## CI Quality Gates

Run fast CLAP-based validation (no API key needed):
```bash
just validate-ci                    # All modules
just validate-ci-module ModuleName  # Single module
```

CI thresholds are defined in `test/ci_config.json`.
