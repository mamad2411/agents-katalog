---
name: competitive-landscape-mapper
description: Advanced operational skill for competitive-landscape-mapper.
read_when:
  - When working in idea-validation workflows
  - When user asks for competitive landscape mapper
  - When planning and sequencing work
  - When scope and decisions must be explicit
metadata: {"codex": {"level": "advanced", "category": "idea-validation", "runtime": "markdown+python", "requires": {"files": ["templates/", "scripts/", "examples/"]}}}
---

# Competitive Landscape Mapper

    Advanced operational skill for competitive-landscape-mapper.

    ## Activation trigger

    Use this skill when the user requests **competitive landscape mapper** and needs a high-confidence, decision-ready outcome in **idea-validation**.

    ## Required inputs

    - Target user segment and context.
- Current problem statement and assumptions.
- Existing evidence (calls, notes, metrics, market signals).
- Decision to make after this analysis.

    ## Optional inputs

    - Previous outputs from this skill family.
    - Team ownership map and delivery timeline.
    - Explicit constraints for cost, risk, or compliance.

    ## Files to inspect

    - `concept/`, `templates/`, `examples/`, `scripts/` in this skill folder.
    - User-referenced repository files and related modules.
    - Prior artifacts that constrain or inform this decision.

    ## Execution workflow

    1. Normalize the request into falsifiable hypotheses and explicit assumptions.
2. Build a confidence map per assumption (evidence strength, recency, bias risk).
3. Identify evidence gaps and design the minimum validation loop.
4. Generate ranked validation actions by learning-per-effort.
5. Produce a go/no-go recommendation with clear conditions to revisit.

    ## Generated artifacts

    - `outputs/hypothesis.md`
- `outputs/assumption-map.md`
- `outputs/validation-plan.md`

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
    $competitive-landscape-mapper "Run competitive landscape mapper on my current project context"
    python scripts/run.py --input examples/input-example.md
    python scripts/validate.py --file examples/output-example.md
    ```

    ## Advanced usage

    - Run in phased mode: discovery -> draft -> validation -> final.
    - Compare two decision branches and include tradeoff table.
    - Enforce stricter gates for production/release-critical use.
