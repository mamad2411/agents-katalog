---
name: rs-plan
description: >
  Plan improvements to an assessed skillset. Reads the quality
  assessment, selects the highest-impact issues, designs specific
  changes to skillset artifacts, and produces an improvement plan
  with clear acceptance criteria. The plan constrains rs-iterate
  to targeted, verifiable changes.
metadata:
  author: monkeypants
  version: "0.1"
  skillset: refine-skillset
  stage: "2"
  freedom: medium
---

# Improvement Planning

You are planning specific improvements to an existing skillset based
on an agreed quality assessment. Every change must be targeted,
verifiable, and leave the skillset measurably better.

## Prerequisites

Check that the project directory contains:
- `assessment.agreed.md` (stage 1 gate)

If missing, tell the operator to complete `rs-assess` first.

Read the assessment thoroughly. Understand which issues are critical,
important, and minor.

## Step 1: Select improvement scope

Not all issues need fixing in one cycle. Select based on:

### Selection criteria

1. **Impact**: Fixes that improve the most operator/client interactions
2. **Independence**: Changes that don't cascade into other changes
3. **Verifiability**: Changes with clear before/after tests
4. **Effort proportionality**: Benefit must exceed cost

### Typical scope per cycle

- 1-2 critical issues (always include these)
- 2-3 important issues (if they don't conflict)
- Minor issues only if they're trivial to fix alongside others

Write the selected scope to `plan/scope.md` with reasoning for each
inclusion and exclusion.

## Step 2: Design changes

For each selected issue, specify the exact changes:

```markdown
### {Issue title}

**Assessment reference**: {link to issue in assessment.agreed.md}

#### Current state

{What exists now — quote the relevant artifact}

#### Target state

{What it should look like after the change}

#### Files to modify

- `{path}`: {what changes and why}

#### Acceptance criteria

- [ ] {Testable property that proves the issue is fixed}
- [ ] {Another testable property}
- [ ] Conformance tests pass after change

#### Risks

{What could go wrong? What else might break?}
```

### Change categories

Changes typically fall into these categories:

**Skill file updates**: Revised methodology, clearer instructions,
better progressive disclosure. Verify by re-reading and checking
that the domain model is honoured.

**Bytecode updates**: Revised semantic bytecode levels. Verify by
checking token budgets and progressive disclosure property.

**Pipeline adjustments**: Reordered stages, revised gates, new
stages. Verify by running `pytest -m doctrine` to confirm pipeline
coherence.

**Presenter fixes**: Improved rendering of workspace artifacts.
Verify by running presenter tests and checking site output.

**Infrastructure changes**: New usecases, repositories, CLI
commands. Verify by running the full test suite.

## Step 3: Define verification plan

Specify how you will verify each change:

```markdown
## Verification Plan

### Automated checks

- [ ] `uv run ruff check .` passes
- [ ] `uv run ruff format --check .` passes
- [ ] `uv run pytest -m doctrine` passes (N tests)
- [ ] `uv run pytest` passes (N tests)

### Manual checks

- [ ] {Specific thing to verify by inspection}
- [ ] {Specific thing to verify by running a skill}

### Regression checks

- [ ] {Existing behaviour that must not change}
```

## Step 4: Estimate and sequence

Order the changes so that:
1. Independent changes come first (easy wins, build confidence)
2. Dependent changes are sequenced correctly
3. The highest-impact change is not last (in case the cycle is cut short)

For each change, note whether it can be done in isolation or requires
other changes to land first.

## Step 5: Present to operator

Present the improvement plan. Show:
1. Selected scope with inclusion/exclusion reasoning
2. Designed changes with acceptance criteria
3. Verification plan
4. Execution sequence

Ask:

1. "Is the scope right? Too ambitious? Not ambitious enough?"
2. "Do the acceptance criteria capture what you care about?"
3. "Are there constraints I should know about before making changes?"
4. "Should any changes be deferred to a future cycle?"

## Step 6: Iterate and agree

Based on operator feedback, update the plan. When agreed:
1. Write `plan.agreed.md`
2. Record the decision:
   ```
   skillset_engineering/skills/rs-plan/scripts/record-plan-agreed.sh \
     --client {org} --engagement {engagement} --project {slug} \
     --field "Changes={count}" \
     --field "Critical fixes={count}" \
     --field "Sequence={summary}"
   ```

## Completion

When `plan.agreed.md` is written, tell the operator the next step
is `rs-iterate` to execute the planned improvements.
