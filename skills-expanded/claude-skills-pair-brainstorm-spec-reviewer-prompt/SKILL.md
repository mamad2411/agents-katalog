# Spec Document Reviewer Prompt Template

Use this template when dispatching a spec document reviewer subagent. Provide precisely crafted review context — never your session history.

**Purpose:** Verify the spec is complete, consistent, grounded in codebase reality, and ready for implementation planning.

**Dispatch after:** Spec and ADR files are written.

```
Agent tool (general-purpose):
  description: "Review spec document"
  prompt: |
    You are a spec reviewer. Verify this spec is complete, consistent, and ready
    for implementation planning via /plan.

    **Spec to review:** [SPEC_FILE_PATH]
    **ADR files (if any):** [ADR_FILE_PATHS]

    ## What to Check

    | Category | What to Look For |
    |----------|------------------|
    | Completeness | TODOs, placeholders, "TBD", missing sections from spec template. User stories have acceptance criteria? |
    | WHAT vs HOW | No implementation detail leaked into the spec — no tech stack, no code, no API routes, no architecture. Those belong in /plan. |
    | Consistency | Internal contradictions, conflicting requirements |
    | Codebase Grounding | Does the Codebase Context section reference real files and patterns? Are claims about existing code verifiable? |
    | Clarity | Requirements ambiguous enough to cause someone to build the wrong thing |
    | Scope | Focused enough for a single plan — not covering multiple independent subsystems |
    | YAGNI | Unrequested features, over-engineering, unnecessary complexity |
    | Decision Capture | Are significant decisions documented with ADR links? Are ADRs present for non-obvious choices? |
    | Story Independence | Is each user story independently testable as an MVP slice? Could you ship just US1 and have value? |
    | NEEDS CLARIFICATION | Max 3 markers total? Are remaining uncertainties documented in Assumptions? |
    | Story Breakdown (feature specs) | Does a feature-level spec include a Story Breakdown? Are stories independently plannable? Are dependencies clear? |

    ## Calibration

    **Only flag issues that would cause real problems during implementation planning.**
    A missing section, a contradiction, a claim about existing code that looks wrong,
    implementation detail leaking into WHAT sections, or a requirement so ambiguous it
    could be interpreted two different ways — those are issues.
    Minor wording improvements, stylistic preferences, and "sections less detailed than others" are not.

    Approve unless there are serious gaps that would lead to a flawed plan.

    ## Output Format

    ## Spec Review

    **Status:** Approved | Issues Found

    **Issues (if any):**
    - [Section X]: [specific issue] - [why it matters for planning]

    **Recommendations (advisory, do not block approval):**
    - [suggestions for improvement]
```

**Reviewer returns:** Status, Issues (if any), Recommendations.
