---
name: mangomas-eval-harness
description: Evaluate AgentRuntime on JSONL (exact-match final_answer, tool ids, truncation, faults). Use when asked to score the local harness. Not evaluate_agent_skill fixture counting.
cli: scripts/harness/eval_harness.py
inputs:
  input: JSONL with prompt and optional expected (CLI --input)
  harness_id: Harness YAML id (CLI --harness-id)
  student: Use the student model (CLI --student)
  threshold: Fail if pass_rate is below this (CLI --threshold)
  strict: Fail on malformed JSONL rows instead of skipping (CLI --strict)
---

# Evaluate the local harness

Runs `AgentRuntime` (Echo via `--scripted` in tests). Do not treat `evaluate_agent_skill` JSON pre-grades as agent quality.

```bash
python scripts/harness/eval_harness.py \
  --input "$INPUT_JSONL" \
  --harness-id "${MANGOMAS_HARNESS_ID:-base_react}"
```

Pass `--strict` to fail on bad JSON or empty prompts instead of skipping. The `--threshold` gate uses labeled exact-match plus unlabeled completion (not truncated) over every evaluated row.

Trusted JSONL: injection detection is off. Interactive tasks stay on `run_agent.py`.
