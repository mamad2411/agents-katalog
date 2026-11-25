---
name: product-management-os-builder
description: Advanced operational skill for product-management-os-builder.
read_when:
  - When working in launch-systems workflows
  - When user asks for product management os builder
  - When a structured artifact must be generated
  - When reusable documentation is required
metadata: {"codex": {"level": "advanced", "category": "launch-systems", "runtime": "markdown+python", "requires": {"files": ["templates/", "scripts/", "examples/"]}}}
---

# Product Management Os Builder

    Advanced operational skill for product-management-os-builder.

    ## Activation trigger

    Use this skill when the user requests **product management os builder** and needs a high-confidence, decision-ready outcome in **launch-systems**.

    ## Required inputs

    - User objective and constraints.
- Repository context.
- Expected output format.

    ## Optional inputs

    - Previous outputs from this skill family.
    - Team ownership map and delivery timeline.
    - Explicit constraints for cost, risk, or compliance.

    ## Files to inspect

    - `concept/`, `templates/`, `examples/`, `scripts/` in this skill folder.
    - User-referenced repository files and related modules.
    - Prior artifacts that constrain or inform this decision.

    ## Execution workflow

    1. Clarify scope.
2. Inspect context.
3. Generate structured output.
4. Validate result.
5. Return actionable deliverable.

    ## Generated artifacts

    - `outputs/result.md`

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
    $product-management-os-builder "Run product management os builder on my current project context"
    python scripts/run.py --input examples/input-example.md
    python scripts/validate.py --file examples/output-example.md
    ```

    ## Advanced usage

    - Run in phased mode: discovery -> draft -> validation -> final.
    - Compare two decision branches and include tradeoff table.
    - Enforce stricter gates for production/release-critical use.
