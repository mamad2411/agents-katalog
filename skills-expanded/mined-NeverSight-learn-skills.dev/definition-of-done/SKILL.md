---
name: definition-of-done
description: Generates per-milestone acceptance criteria from milestones.yaml and business-requirements.yaml. For each milestone, produces functional acceptance criteria, non-functional gates, testing requirements, documentation requirements, and an exit checklist. Outputs definition-of-done.yaml so teams know exactly when a milestone is complete.
---

# Definition of Done

Generates explicit, verifiable acceptance criteria for every milestone in `milestones.yaml`. Bridges the gap between "the plan says we're building X" and "we know for certain that X is done." Each milestone gets criteria derived directly from the requirements — not generic checklists.

## Prerequisites

- `milestones.yaml` (output from `/implementation-planner`, with `estimated_days` added by `/delivery-timeline`)
- `business-requirements.yaml` (output from `/business-requirements-interview`)
- Optional: `technical-requirements.yaml` for NFR-derived gates

## Usage

```
/definition-of-done path/to/milestones.yaml path/to/business-requirements.yaml
```

## Process

### Step 1: Load Artifacts

Read `milestones.yaml` and extract each milestone's `id`, `name`, `description`, and any `deliverables` or `tasks` references.

Read `business-requirements.yaml` and map each functional requirement to the milestone(s) most likely to deliver it. Use the milestone name and description to make this determination — do not guess at task-level details.

If `technical-requirements.yaml` exists in the same directory, read it to extract non-functional requirements (performance targets, security requirements, test coverage thresholds).

### Step 2: Derive Acceptance Criteria per Milestone

For each milestone, generate criteria in five categories:

**1. Functional Criteria**
Specific, observable behaviors that must be true when the milestone is done. Derive these from the business requirements mapped to this milestone. Each criterion must be:
- Verifiable without ambiguity ("users can log in with email and password" ✓ vs "login works" ✗)
- Tied to a requirement ID where possible
- Written as "Given/When/Then" or declarative present tense

**2. Non-Functional Criteria**
Performance, security, reliability, or accessibility requirements that apply to this milestone's output. Pull from `technical-requirements.yaml` NFRs if present. Only include NFRs that are *testable at this milestone's scope* — do not apply system-wide SLAs to early foundational milestones.

**3. Testing Requirements**
What test coverage must exist before this milestone is considered done:
- Unit test coverage for new modules/functions introduced
- Integration tests for any new service boundaries crossed
- E2E scenarios for any user-facing flows delivered
- Regression: confirm no existing tests are broken

**4. Documentation Requirements**
What documentation artifacts are expected from this milestone:
- Inline code comments for complex logic
- API documentation for any new endpoints
- README updates if setup/usage changes
- Architecture diagram updates if structure changes

**5. Exit Checklist**
A short, concrete checklist used at code review / milestone sign-off. This is the quick reference — summarize the above into yes/no checks.

### Step 3: Identify Cross-Milestone Gates

If any requirement spans multiple milestones (e.g., "end-to-end encryption" requires work in m1, m3, and m5), note it as a cross-milestone gate: the full requirement is only verifiable at the *last* milestone that contributes to it. Add a `cross_milestone_note` to each intermediate milestone.

### Step 4: Generate definition-of-done.yaml

Write `definition-of-done.yaml` in the same directory as `milestones.yaml`.

### Step 5: Gap Analysis

Report inline after generating the file:

```
## Definition of Done Gap Analysis

**Project:** [name]
**Milestones with DoD:** [n]/[n]
**Functional Requirements Mapped:** [n]/[n]

**Criteria Quality:**
[✓ / ✗] All functional criteria are verifiable (no vague language)
[✓ / ✗] NFR criteria tied to specific thresholds (not just "must be fast")
[✓ / ✗] Every milestone has at least one testing requirement
[✓ / ✗] Cross-milestone requirements identified

**Unmapped Requirements:** [none / list requirements not tied to any milestone]

**Recommendations:** [none / list]
```

## Output Format

### definition-of-done.yaml Schema

```yaml
version: "1.0.0"
project: [project name]
generated: "[ISO 8601 timestamp]"
sources:
  milestones: milestones.yaml
  business_requirements: business-requirements.yaml
  technical_requirements: technical-requirements.yaml  # if used

milestones:
  - id: [milestone id, e.g. m0]
    name: [milestone name]
    acceptance_criteria:
      functional:
        - criterion: "[verifiable statement of behavior]"
          requirement_ref: "[business requirement ID, if applicable]"
        - criterion: "..."

      non_functional:
        - criterion: "[measurable NFR threshold]"
          requirement_ref: "[NFR ID, if applicable]"
        # Omit this section if no NFRs apply to this milestone

      testing:
        unit: "[coverage expectation for new code in this milestone]"
        integration: "[integration test expectations, or 'N/A']"
        e2e: "[E2E scenario expectations, or 'N/A']"
        regression: "All existing tests pass"

      documentation:
        - "[specific documentation artifact expected]"
        # e.g. "README updated with local setup instructions"

      cross_milestone_notes:
        - "[note about a requirement that spans milestones, if any]"
        # Omit if none

    exit_checklist:
      - "[ ] [check 1]"
      - "[ ] [check 2]"
      - "[ ] All unit tests pass with [n]%+ coverage"
      - "[ ] PR approved by at least one reviewer"
      - "[ ] No open blocking issues"
```

## Example Output

See [examples/definition-of-done.yaml](./examples/definition-of-done.yaml) for a complete sample.
