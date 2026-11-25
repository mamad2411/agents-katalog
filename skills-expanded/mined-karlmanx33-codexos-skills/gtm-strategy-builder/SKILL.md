---
name: gtm-strategy-builder
description: Advanced operational skill for gtm-strategy-builder.
read_when:
  - When working in gtm-growth workflows
  - When user asks for gtm strategy builder
  - When a structured artifact must be generated
  - When reusable documentation is required
metadata: {"codex": {"level": "advanced", "category": "gtm-growth", "runtime": "markdown+python", "requires": {"files": ["templates/", "scripts/", "examples/"]}}}
---

# Gtm Strategy Builder

    Advanced operational skill for gtm-strategy-builder.

    ## Activation trigger

    Use this skill when the user requests **gtm strategy builder** and needs a high-confidence, decision-ready outcome in **gtm-growth**.

    ## Required inputs

    - ICP segments and current traction data.
- Positioning hypotheses and pricing assumptions.
- Channel constraints (budget, team bandwidth, timelines).
- Success metrics (CAC, payback, activation, retention).

    ## Optional inputs

    - Previous outputs from this skill family.
    - Team ownership map and delivery timeline.
    - Explicit constraints for cost, risk, or compliance.

    ## Files to inspect

    - `concept/`, `templates/`, `examples/`, `scripts/` in this skill folder.
    - User-referenced repository files and related modules.
    - Prior artifacts that constrain or inform this decision.

    ## Execution workflow

    1. Prioritize segments/channels using evidence-weighted scoring.
2. Build positioning/messaging assets mapped to ICP pain and value proof.
3. Design measurable GTM experiments with clear stop/scale rules.
4. Quantify unit economics assumptions and sensitivity ranges.
5. Produce execution roadmap and weekly review cadence.

    ## Generated artifacts

    - `outputs/gtm-strategy.md`
- `outputs/experiment-matrix.md`
- `outputs/metrics-dashboard-spec.md`

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
    $gtm-strategy-builder "Run gtm strategy builder on my current project context"
    python scripts/run.py --input examples/input-example.md
    python scripts/validate.py --file examples/output-example.md
    ```

    ## Advanced usage

    - Run in phased mode: discovery -> draft -> validation -> final.
    - Compare two decision branches and include tradeoff table.
    - Enforce stricter gates for production/release-critical use.
