---
name: team-training
description: Executes recursive performance telemetry evaluation, prompt tuning, and regression-gated optimization loops.
---
# Training Skill Protocol

Use this skill to evaluate sub-agent execution performance, tune system prompts, and validate updates against zero-regression benchmark suites.

## Execution Workflow

1. **Telemetry Ingestion**: `performance-evaluator` audits execution logs, defect rates, and rework cycles.
2. **Prompt & Skill Tuning**: `prompt-optimizer` (or `rapid-prompt-tuner` for rapid mode) drafts updated system prompt instructions.
3. **Benchmark Creation**: `curriculum-builder` constructs synthetic evaluation test suites.
4. **Regression Gate**: `regression-guard` runs benchmarks to guarantee zero capability regressions before promoting prompt updates.
