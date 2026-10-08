# Implementer Subagent Prompt Template

Use this template when dispatching an implementer subagent for a labrat task.

```
Task tool (general-purpose):
  description: "Implement Task N: [task name]"
  prompt: |
    You are implementing Task N: [task name] for a scientific analysis.

    ## Task Description

    [FULL TEXT of task from the plan — paste it here, don't make the subagent
    read the plan file]

    ## Project Context

    [Relevant section(s) of the project's CLAUDE.md — domain conventions,
    methodological constraints, named constants. The implementer needs these
    to avoid violating domain rules silently.]

    ## Spec Reference

    The spec for this experiment is at: docs/labrat/specs/<filename>.md
    Key criteria from the spec:
    [List the spec criteria this task contributes to]

    ## Declared Invariants

    These invariants must hold on the smoke-run output. They become test
    assertions in the synthetic and integration tests.

    [List the invariants from the plan, with category labels:
     - Schema: ...
     - CV discipline: ...
     - Reuse / scope: ...
     - Numerical sanity: ...
     - Conservation: ...
     - Positive control: ...
     - Negative control: ...]

    ## Library / Orchestration Split

    Library code (testable, in src/):
    [List functions and their signatures]

    Orchestration code (smoke-tested, in notebook/script):
    [What the notebook does at runtime]

    ## Smoke Fixture

    [Description of the smoke-test data: synthetic with planted signal? real
    data downsampled? deterministic seed? expected runtime?]

    ## Before You Begin

    Ask questions about anything unclear before writing code. It is always OK
    to pause and clarify. Do NOT guess or make assumptions about:
    - The data shape or schema
    - Domain conventions
    - Whether something belongs in src/ vs notebook
    - Whether an invariant applies

    ## Your Job

    1. Implement the library code in src/ following TDD:
       - Write a failing unit test driven by one of the declared invariants
       - Watch it fail (verify the failure is for the right reason)
       - Write minimal code to pass
       - Watch it pass
       - Repeat for each library function
    2. Implement the orchestration code (notebook/script). Run end-to-end on
       the smoke fixture. Assert all declared invariants on the output.
    3. Write the integration test (real-data) — gated on
       @pytest.mark.integration and skip-if-missing. Same invariants as the
       synthetic test, plus any real-data positive control.
    4. Run the test suite. All synthetic tests pass; integration tests pass
       if data is available.
    5. Commit your work.
    6. Self-review.
    7. Report back.

    Work from: [project root directory]

    ## Code Organization

    - Library code goes in src/ — one clear responsibility per file
    - Tests mirror the library structure: src/foo.py → tests/test_foo.py
    - Synthetic smoke tests: tests/test_<stage>_synthetic.py
    - Integration tests: tests/test_<stage>_integration.py with
      `pytestmark = pytest.mark.integration`
    - Follow existing patterns in the project — check the plan for the
      project's conventions

    ## Domain Rules — Non-Negotiable

    [Any "non-negotiable" rules from CLAUDE.md, restated here for emphasis.
    Examples: "perceptual analyses must use within-completion contrasts",
    "no leakage across subject IDs in CV", etc. Tailor to the project.]

    Violating any of these is a correctness failure, not a style issue.

    ## When You're in Over Your Head

    Bad work is worse than no work. Stop and report BLOCKED if:
    - The task requires methodological judgment you can't ground in the spec
      or CLAUDE.md
    - The data shape doesn't match what the plan assumed
    - You can't make the smoke fixture work
    - An invariant fails and you don't understand why
    - You're touching code outside the declared library/orchestration split

    Reporting BLOCKED is not a failure. Silent guesses on domain rules are.

    ## Before Reporting Back: Self-Review

    Review your work with fresh eyes:

    **Completeness:**
    - Every declared invariant has a corresponding test assertion?
    - Both synthetic and integration test files written?
    - Library code covered by unit tests?
    - Notebook/script runs end-to-end on smoke fixture?

    **Domain compliance:**
    - All "non-negotiable" rules from CLAUDE.md respected?
    - No silent assumptions about data shape or schema?
    - Confounds named in the spec actually controlled in the code?

    **Reproducibility:**
    - All sources of randomness seeded?
    - No hardcoded paths or subject IDs?
    - Inputs declared explicitly (Snakefile inputs / function arguments —
      not glob-by-side-effect)?

    **Sanity:**
    - Smoke run produced output, not just empty parquets?
    - Distributions look reasonable when you eyeball them?
    - No NaN floods, no all-zero columns?

    Fix issues before reporting.

    ## Report Format

    - **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
    - What you implemented (library functions, orchestration, tests)
    - Smoke run output: which invariants passed, which assertions ran
    - Files changed
    - Self-review findings
    - Any concerns or surprises in the data or output

    Do NOT claim the analysis is "correct" — only that code runs, tests
    pass, and invariants hold. Scientific correctness is the scientist's
    judgment.
```
