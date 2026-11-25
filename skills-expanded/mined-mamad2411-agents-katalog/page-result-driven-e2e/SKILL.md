---
name: page-result-driven-e2e
description: Standardized screenshot-first browser E2E loop for Industry-AI-Flow modules. Uses agent-browser automation, compares page evidence against expected behavior, prioritizes P0/P1 defects, applies fixes, and reruns until gate conditions are met.
---

# Page Result-Driven E2E Skill

Use this skill when you need a repeatable workflow of:

1. Run page automation with `agent-browser`
2. Capture key screenshots as evidence
3. Compare observed UI/output with design expectations
4. Triage and fix defects (P0/P1 first)
5. Rerun until the module passes gate conditions

This skill is designed for continuous use in demo-oriented QA across core modules.

## Supported Modules

- `data_dashboard`
- `cost_estimation`
- `rag`

Module runners already available in this repo:

- `scripts/testing/run_data_dashboard_agent_browser_e2e.py`
- `scripts/testing/run_cost_estimation_agent_browser_e2e.py`
- `scripts/testing/run_rag_agent_browser_e2e.py`

Unified gate orchestrator:

- `scripts/testing/run_page_result_driven_gate.py`

## Inputs

- `module`: one of `data_dashboard | cost_estimation | rag`
- `frontend_url`: default `http://127.0.0.1:3001`
- `login_email` / `login_password`
- `max_cycles`: rerun limit, default `3`
- Optional `repair_command`: shell command executed between failed cycles

## Core Loop

1. **Execute module E2E script**
   - Drive UI flows with `agent-browser`.
   - Capture full-page screenshots for key steps.
   - Save JSON report + case index.

2. **Evidence-based evaluation**
   - Parse module report.
   - Evaluate success rate and case-level failures.
   - Validate screenshot artifacts exist and are complete enough for review.

3. **Defect triage (P0/P1 first)**
   - P0: Core workflow blocked or incorrect (cannot demo feature).
   - P1: Major UX/functional incompleteness (feature appears unreliable).
   - Ignore P2/P3 until P0/P1 are closed.

4. **Fix and regression**
   - Apply minimal, targeted code changes.
   - Re-run the same module test.
   - Repeat until gate passes or cycle limit reached.

5. **Output delivery**
   - Return gate report path, module report path, screenshot directory.
   - Include unresolved failures (if any) with exact evidence.

## Execution Commands

### A) Direct one-shot gate run

```bash
python3 scripts/testing/run_page_result_driven_gate.py \
  --module data_dashboard \
  --frontend-url http://127.0.0.1:3001 \
  --login-email "${RAG_E2E_LOGIN_EMAIL:-demo@example.com}" \
  --login-password "${RAG_E2E_LOGIN_PASSWORD:-demo123}" \
  --max-cycles 1
```

### B) Multi-cycle run with automatic repair hook

```bash
python3 scripts/testing/run_page_result_driven_gate.py \
  --module cost_estimation \
  --frontend-url http://127.0.0.1:3001 \
  --login-email "${RAG_E2E_LOGIN_EMAIL:-demo@example.com}" \
  --login-password "${RAG_E2E_LOGIN_PASSWORD:-demo123}" \
  --max-cycles 3 \
  --repair-command "pytest tests/unit -q"
```

### C) RAG gate run

```bash
python3 scripts/testing/run_page_result_driven_gate.py \
  --module rag \
  --frontend-url http://127.0.0.1:3001 \
  --rag-csv docs/testing/rag_question_bank_180.csv \
  --rag-max-questions 30 \
  --max-cycles 2
```

## Gate Criteria

- `data_dashboard`: all cases pass (`success_cases == total_cases`)
- `cost_estimation`: all cases pass + clear-queue validation passes
- `rag`: success rate meets threshold (default `0.7`, configurable)

## Evidence Requirements

For each cycle, preserve:

- Module native report JSON
- Case index (`CASE_INDEX.md`) when available
- Screenshot files for each case/turn
- Unified gate report:
  - `temp/page_result_driven/<module>_<timestamp>/<module>_gate_report.json`
  - `temp/page_result_driven/<module>_<timestamp>/<module>_gate_summary.md`

## Output Contract

Always provide:

1. Pass/fail status with cycle count
2. Success metrics (count/rate)
3. Paths to screenshots and reports
4. P0/P1 findings with concise fix status
5. Next rerun decision (continue loop or stop)

## Notes

- Keep screenshot readability stable: ensure question + answer (or input + output) are both visible.
- Prefer simple/stable demo cases first, then expand coverage.
- If a cycle fails and no repair hook is supplied, stop and perform manual fix before rerun.
