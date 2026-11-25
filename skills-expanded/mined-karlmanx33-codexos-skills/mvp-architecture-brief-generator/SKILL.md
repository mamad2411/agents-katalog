---
name: mvp-architecture-brief-generator
description: Advanced operational skill for mvp-architecture-brief-generator.
read_when:
  - When working in mvp-build workflows
  - When user asks for mvp architecture brief generator
  - When a structured artifact must be generated
  - When reusable documentation is required
metadata: {"codex": {"level": "advanced", "category": "mvp-build", "runtime": "markdown+python", "requires": {"files": ["templates/", "scripts/", "examples/"]}}}
---

# Mvp Architecture Brief Generator

    Advanced operational skill for mvp-architecture-brief-generator.

    ## Activation trigger

    Use this skill when the user requests **mvp architecture brief generator** and needs a high-confidence, decision-ready outcome in **mvp-build**.

    ## Required inputs

    - Product objective and bounded scope.
- Technical constraints (stack, infra, compliance).
- Non-functional requirements (security, latency, reliability).
- Dependencies and integration points.

    ## Optional inputs

    - Previous outputs from this skill family.
    - Team ownership map and delivery timeline.
    - Explicit constraints for cost, risk, or compliance.

    ## Files to inspect

    - `concept/`, `templates/`, `examples/`, `scripts/` in this skill folder.
    - User-referenced repository files and related modules.
    - Prior artifacts that constrain or inform this decision.

    ## Execution workflow

    1. Translate product goals into architecture/spec decisions with explicit tradeoffs.
2. Map components, boundaries, data contracts, and failure paths.
3. Define execution slices (MVP-now vs later) and risk controls.
4. Generate implementation-ready artifacts and acceptance criteria.
5. Validate internal consistency across scope, architecture, and delivery plan.

    ## Generated artifacts

    - `outputs/brief.md`
- `outputs/component-boundaries.md`
- `outputs/acceptance-criteria.md`

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
    $mvp-architecture-brief-generator "Run mvp architecture brief generator on my current project context"
    python scripts/run.py --input examples/input-example.md
    python scripts/validate.py --file examples/output-example.md
    ```

    ## Advanced usage

    - Run in phased mode: discovery -> draft -> validation -> final.
    - Compare two decision branches and include tradeoff table.
    - Enforce stricter gates for production/release-critical use.
