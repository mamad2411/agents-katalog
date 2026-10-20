---
description: "Orchestrator post-run suggester: prepare candidates, call scorer tool, apply gates"
globs: ["**/*"]
alwaysApply: false
---

# Behavior
- After any agent completes, summarize context (state, gates, latest outputs).
- Build candidate list (mix of NATURAL_STEP and COMMAND_TRIGGER) with metrics in [0,1].
- Call local scorer tool (see decision_scoring_tool.mdc).
- Emit a JSON block with decision result and short rationale.
- Log outputs to logs/decisions/YYYYMMDD_HHMMSS.json.

# Inputs (expected to be available)
- workflow_state.json, gate_results.json, handoff_log.json
- recent outputs (memory-bank/*, reports/*, test logs)

# Outputs
- One JSON per run with decision & candidates, stored under logs/decisions/.
