---
name: benchmark-models
description: Compare model behavior for a repeated prompt or workflow across available Codex-accessible model paths.
---

# Benchmark Models

Use this skill when the user asks which model is best for a prompt, skill, task, or workflow.

Upstream GStack can run Claude, GPT, and Gemini side by side. This Codex port preserves the benchmarking discipline and uses only model paths that are actually available in the current environment.

## Workflow

1. Define the benchmark:
   - prompt or task
   - expected output shape
   - quality criteria
   - latency, cost, or token constraints
2. Identify available runners:
   - current Codex model
   - `codex exec` or CLI paths if available
   - external model CLIs only when already configured
3. Run the same prompt unchanged for each candidate.
4. Compare:
   - correctness
   - completeness
   - instruction following
   - latency
   - token/cost estimate when observable
5. Report a recommendation and the evidence behind it.

## Guardrails

- Do not invent benchmark numbers.
- Do not call unavailable model providers.
- Keep the original prompt stable across candidates.
