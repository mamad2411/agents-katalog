---
name: devils-advocate-idea-reviewer
description: Advanced operational skill for devils-advocate-idea-reviewer.
read_when:
  - When working in idea-validation workflows
  - When user asks for devils advocate idea reviewer
  - When assessing risks or quality
  - When remediation priorities are needed
metadata: {"codex": {"level": "advanced", "category": "idea-validation", "runtime": "markdown+python", "requires": {"files": ["templates/", "scripts/", "examples/"]}}}
---

# Devils Advocate Idea Reviewer

    Advanced operational skill for devils-advocate-idea-reviewer.

    ## Activation trigger

    Use this skill when the user requests **devils advocate idea reviewer** and needs a high-confidence, decision-ready outcome in **idea-validation**.

    ## Required inputs

    - Audit target (repo/module/system) and risk appetite.
- Severity model (P0-P3) and remediation SLA expectations.
- Security or quality policies that must be enforced.
- Evidence sources (code, configs, logs, prior incidents).

    ## Optional inputs

    - Previous outputs from this skill family.
    - Team ownership map and delivery timeline.
    - Explicit constraints for cost, risk, or compliance.

    ## Files to inspect

    - `concept/`, `templates/`, `examples/`, `scripts/` in this skill folder.
    - User-referenced repository files and related modules.
    - Prior artifacts that constrain or inform this decision.

    ## Execution workflow

    1. Inspect the target and collect objective evidence per risk domain.
2. Classify findings by impact, exploitability/probability, and blast radius.
3. Produce remediation plan with sequencing, owners, and verification steps.
4. Flag quick wins vs structural fixes and quantify residual risk.
5. Deliver a release recommendation (blocker/warn/pass) with rationale.

    ## Generated artifacts

    - `outputs/audit-report.md`
- `outputs/remediation-plan.md`
- `outputs/retest-checklist.md`

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
    $devils-advocate-idea-reviewer "Run devils advocate idea reviewer on my current project context"
    python scripts/run.py --input examples/input-example.md
    python scripts/validate.py --file examples/output-example.md
    ```

    ## Advanced usage

    - Run in phased mode: discovery -> draft -> validation -> final.
    - Compare two decision branches and include tradeoff table.
    - Enforce stricter gates for production/release-critical use.
