---
name: codex-session-planner
description: Advanced operational skill for codex-session-planner.
read_when:
  - When working in mvp-build workflows
  - When user asks for codex session planner
  - When planning and sequencing work
  - When scope and decisions must be explicit
metadata: {"codex": {"level": "advanced", "category": "mvp-build", "runtime": "markdown+python", "requires": {"files": ["templates/", "scripts/", "examples/"]}}}
---

# Codex Session Planner

    Advanced operational skill for codex-session-planner.

    ## Activation trigger

    Use this skill when the user requests **codex session planner** and needs a high-confidence, decision-ready outcome in **mvp-build**.

    ## Required inputs

    - Strategic objective and decision horizon.
- Current constraints and bottlenecks.
- Existing workflows, cadences, and ownership map.
- Required outputs and success conditions.

    ## Optional inputs

    - Previous outputs from this skill family.
    - Team ownership map and delivery timeline.
    - Explicit constraints for cost, risk, or compliance.

    ## Files to inspect

    - `concept/`, `templates/`, `examples/`, `scripts/` in this skill folder.
    - User-referenced repository files and related modules.
    - Prior artifacts that constrain or inform this decision.

    ## Execution workflow

    1. Convert broad objective into decision-ready workstreams.
2. Define cadence, ownership, and measurable checkpoints.
3. Generate an execution plan with dependencies and risk gates.
4. Create artifacts for continuity (logs, briefs, review templates).
5. Validate feasibility against timeline and resource limits.

    ## Generated artifacts

    - `outputs/execution-plan.md`
- `outputs/decision-log.md`
- `outputs/review-cadence.md`

    ## Output contract

    Final response must include:

    - Objective and scope boundaries.
    - Inputs and assumptions used.
    - Analysis and decision rationale.
    - Artifact paths and summary.
    - Validation result and residual risks.
    - Next actions ordered by priority.

    ## Validation checklist

    - Required sections are complete and non-empty.
- No placeholder content (`TODO`, `TBD`, `lorem`, `placeholder`).
- Claims are traceable to provided inputs or inspected files.
- Output includes explicit decisions, risks, and next steps.

    ## Safety / failure rules

    - Pause and ask for clarification if required inputs are missing or contradictory.
- Do not invent metrics, user evidence, or repository facts.
- Do not modify unrelated files or broaden scope silently.
- If high-risk uncertainty remains, return a gated recommendation instead of false precision.

    ## Example commands

    ```shell
    $codex-session-planner "Run codex session planner on my current project context"
    python scripts/run.py --input examples/input-example.md
    python scripts/validate.py --file examples/output-example.md
    ```

    ## Advanced usage

    - Run in phased mode: discovery -> draft -> validation -> final.
    - Compare two decision branches and include tradeoff table.
    - Enforce stricter gates for production/release-critical use.
