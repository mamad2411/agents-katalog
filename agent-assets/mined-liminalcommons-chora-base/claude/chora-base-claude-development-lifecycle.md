---
sap_id: SAP-012
version: 1.5.0
status: active
last_updated: 2025-11-06
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 13
progressive_loading:
  phase_1: "lines 1-100"    # Quick Start + Sprint Workflow
  phase_2: "lines 101-260"  # DDD + BDD Workflows
  phase_3: "full"           # Complete including tips and pitfalls
phase_1_token_estimate: 3000
phase_2_token_estimate: 7500
phase_3_token_estimate: 11000
---

# Development Lifecycle (SAP-012) - Claude-Specific Awareness

**SAP ID**: SAP-012
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

---

## 📖 Quick Reference

**New to SAP-012?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - Phase 2: Create sprint plan
- 📚 **Time Savings** - 40-80% defect reduction via Documentation-First + BDD + TDD, 60% debugging time reduction
- 🎯 **Feature 1** - Vision → Planning → Requirements → Development → Testing → Review → Release → Monitoring
- 🔧 **Feature 2** - Research-backed from BDD + TDD integration
- 📊 **Feature 3** - Write how-to guides → Extract BDD → Implement with TDD
- 🔗 **Integration** - Works with SAP-004, SAP-005, SAP-006, SAP-007, SAP-010, SAP-012

This CLAUDE.md provides: Claude Code-specific workflows for implementing SAP-012.
s.

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for the 8-phase development lifecycle (DDD→BDD→TDD).

### First-Time Sprint Setup

1. Read [AGENTS.md](AGENTS.md) for generic development lifecycle workflows
2. Use this file for Claude Code tool integration (Read templates, Edit sprint plans, Bash for testing)
3. Follow 8-phase process: Vision → Planning → DDD → BDD → TDD → Quality → Review → Release

### Session Resumption

- Check docs/project-docs/sprints/ for current sprint
- Use Bash tool for testing (pytest, behave, ruff, mypy)
- Use Edit tool to update sprint plans, change requests, scenarios
- Use Read tool to understand current phase and next steps

---

## Claude Code Development Lifecycle Workflows

### Workflow 1: Starting a New Sprint with Claude Code

```markdown
User: "Start a new sprint for feature X"

Claude (Phase 1: Check Current Sprint - 0-5k tokens):
1. List existing sprints:
   Bash: ls -la docs/project-docs/sprints/
2. Identify current sprint number:
   Bash: ls docs/project-docs/sprints/ | grep -E "sprint-[0-9]+" | sort -V | tail -1
   # Example output: sprint-003.md → Next is sprint-004
3. Read current sprint to understand status:
   Read docs/project-docs/sprints/sprint-003.md

Claude (Phase 2: Create Sprint Plan - 5-15k tokens):
4. Read sprint template:
   Read docs/project-docs/templates/SPRINT_PLAN_TEMPLATE.md
5. Create new sprint file:
   Write docs/project-docs/sprints/sprint-004.md
   # Copy template structure, customize for feature X
6. Edit sprint plan with feature details:
   Edit docs/project-docs/sprints/sprint-004.md
   # Update: Title, Goals, Phases, Tasks, Estimates

Claude (Phase 3: Update Governance - 15-25k tokens):
7. Read current ledger to check version:
   Read docs/skilled-awareness/development-lifecycle/ledger.md
8. Update ledger with new sprint:
   Edit docs/skilled-awareness/development-lifecycle/ledger.md
   # Add sprint-004 to active sprints section
9. If ECOSYSTEM_STATUS.yaml exists, update it:
   Read ECOSYSTEM_STATUS.yaml
   Edit ECOSYSTEM_STATUS.yaml
   # Add feature X to active work

Claude (response to user):
"Created Sprint 004 for feature X:

✅ Sprint plan created:
   - File: docs/project-docs/sprints/sprint-004.md
   - Goal: Implement feature X with DDD→BDD→TDD workflow
   - Phases: 8 phases defined (Vision → Release)
   - Estimate: 12-16 hours

✅ Governance updated:
   - Ledger: Sprint 004 added to active sprints
   - ECOSYSTEM_STATUS: Feature X marked as in-progress

Next: Phase 2 (Planning & Architecture) - Define technical contracts"

Result: Sprint 004 active, ready for DDD phase
```

---

### Workflow 2: Writing a DDD Change Request with Claude Code

```markdown
User: "Create a change request for the new validation module"

Claude (Phase 1: Check Template - 0-5k tokens):
1. Check if change request template exists:
   Bash: ls docs/project-docs/templates/CHANGE_REQUEST_TEMPLATE.md
2. If exists, read it:
   Read docs/project-docs/templates/CHANGE_REQUEST_TEMPLATE.md
3. Check inbox structure:
   Bash: ls -la inbox/active/

Claude (Phase 2: Create Coordination Request - 5-15k tokens):
4. Determine coordination request number:
   Bash: ls inbox/active/ | grep -E "coord-[0-9]+" | sort -V | tail -1
   # Example: coord-023 → Next is coord-024
5. Create coordination directory:
   Bash: mkdir -p inbox/active/coord-024
6. Write change request:
   Write inbox/active/coord-024/change-request.md
   # Copy template, customize for validation module

Claude (Phase 3: Define Contracts - 15-40k tokens):
7. Edit change request to add technical specifications:
   Edit inbox/active/coord-024/change-request.md
   # Add: Overview, Contracts, Interfaces, Data Structures

Example contract to add:
```python
class ValidationResult:
    """Contract for validation output."""
    is_valid: bool
    errors: list[ValidationError]
    warnings: list[ValidationWarning]
    metadata: dict[str, Any]

    def __post_init__(self):
        assert isinstance(self.is_valid, bool)
        assert isinstance(self.errors, list)
```

8. Add acceptance criteria:
   Edit inbox/active/coord-024/change-request.md
   # Section: Acceptance Criteria
   # List testable conditions (must be verifiable via scenarios)

Claude (Phase 4: Add Implementation Plan - 40-60k tokens):
9. Edit change request to add implementation plan:
   Edit inbox/active/coord-024/change-request.md
   # Add: Phases, Tasks, Time Estimates, Dependencies

10. Add quality gates:
    Edit inbox/active/coord-024/change-request.md
    # Add: Coverage ≥85%, Lint 0 errors, Type check 0 errors, All scenarios GREEN

Claude (response to user):
"Created DDD change request for validation module:

✅ Change request:
   - File: inbox/active/coord-024/change-request.md
   - Contracts defined: ValidationResult, ValidationError, ValidationWarning
   - Acceptance criteria: 8 testable conditions
   - Implementation plan: 4 phases, 12-16 hours estimated

✅ Quality gates:
   - Coverage: ≥85%
   - Lint: 0 errors (ruff)
   - Type check: 0 errors (mypy --strict)
   - Scenarios: All GREEN (behave)

Next: Get approval, then proceed to Phase 4 (BDD Scenarios)"

Result: coord-024 change request ready for approval
```

---

### Workflow 3: Writing BDD Scenarios with Claude Code

```markdown
User: "Write BDD scenarios for the validation module"

Claude (Phase 1: Verify Change Request Approved - 0-5k tokens):
1. Read change request to check approval:
   Read inbox/active/coord-024/change-request.md
   # Check: Approval section has signature
2. If not approved, remind user to approve first

Claude (Phase 2: Create Feature File - 5-15k tokens):
3. Check if features/ directory exists:
   Bash: ls -la features/
4. If not, create structure:
   Bash: mkdir -p features/steps
5. Write feature file:
   Write features/validation.feature
   # Gherkin syntax: Feature → Scenario → Given/When/Then

Example feature content:
```gherkin
Feature: Validation Module
  As a developer
  I want to validate data inputs
  So that I can catch errors early

  Scenario: Valid input passes validation
    Given I have a validation schema for email addresses
    When I validate "user@example.com"
    Then the validation should pass
    And the result should have 0 errors

  Scenario: Invalid input fails validation
    Given I have a validation schema for email addresses
    When I validate "invalid-email"
    Then the validation should fail
    And the result should have 1 error
    And the error message should contain "invalid email format"
```

Claude (Phase 3: Write Step Definitions - 15-40k tokens):
6. Write step definitions file:
   Write features/steps/validation_steps.py
   # Implement Given/When/Then step functions

Example step definitions:
```python
from behave import given, when, then
from validation_module import Validator, ValidationResult

@given('I have a validation schema for email addresses')
def step_impl(context):
    context.validator = Validator(schema='email')

@when('I validate "{input_value}"')
def step_impl(context, input_value):
    context.result = context.validator.validate(input_value)

@then('the validation should pass')
def step_impl(context):
    assert context.result.is_valid is True
```

Claude (Phase 4: Verify Scenarios RED - 40-50k tokens):
7. Run behave to verify all scenarios are RED (not implemented yet):
   Bash: behave features/validation.feature --dry-run
8. If scenarios not RED, check step definitions:
   Read features/steps/validation_steps.py
9. Run actual behave (should fail because no implementation):
   Bash: behave features/validation.feature
   # Expected: All scenarios FAIL (RED state)

Claude (response to user):
"Created BDD scenarios for validation module:

✅ Feature file created:
   - File: features/validation.feature
   - Scenarios: 2 (valid input, invalid input)
   - Steps: 7 Given/When/Then steps

✅ Step definitions created:
   - File: features/steps/validation_steps.py
   - Steps implemented: 7 step functions
   - Uses: @given, @when, @then decorators

✅ Scenarios verified RED:
   - behave features/validation.feature
   - Result: 2 scenarios, 2 failed ✅ (expected before implementation)
   - Status: Ready for TDD Phase 5

Next: Phase 5 (TDD) - RED→GREEN→REFACTOR cycle"

Result: BDD scenarios ready, all RED (pre-implementation)
```

---

## Claude-Specific Tips

### Tip 1: Use Read for Templates Before Creating

**Pattern**:
```bash
# ALWAYS read template before creating new files
Read docs/project-docs/templates/SPRINT_PLAN_TEMPLATE.md
Read docs/project-docs/templates/CHANGE_REQUEST_TEMPLATE.md

# Then create new file based on template
Write docs/project-docs/sprints/sprint-004.md
# Copy template structure, customize
```

**Why**: Templates provide standardized structure; Read ensures consistency

---

### Tip 2: Use Bash for Quality Gates

**Pattern**:
```bash
# Run all quality gates in sequence
Bash: pytest --cov=src --cov-fail-under=85
Bash: ruff check .
Bash: mypy --strict src/
Bash: behave features/

# Check exit codes (0 = pass, non-zero = fail)
```

**Why**: Quality gates must all pass before moving to next phase

---

### Tip 3: Update Ledger After Each Sprint

**Pattern**:
```bash
# After completing sprint, update ledger
Read docs/skilled-awareness/development-lifecycle/ledger.md
Edit docs/skilled-awareness/development-lifecycle/ledger.md
# Move sprint from active to completed section
# Add sprint metrics (time spent, quality gate results)
```

**Why**: Ledger tracks adoption metrics and sprint history

---

### Tip 4: Verify Scenarios RED Before Implementation

**Pattern**:
```bash
# After writing BDD scenarios, ALWAYS verify RED:
Bash: behave features/validation.feature

# Expected output: X scenarios, X failed
# If scenarios pass, implementation already exists (wrong phase)
```

**Why**: BDD workflow requires RED state before TDD Phase 5

---

### Tip 5: Use Edit for Incremental Sprint Updates

**Pattern**:
```bash
# Read sprint plan first
Read docs/project-docs/sprints/sprint-004.md

# Edit specific sections (not full rewrite)
Edit docs/project-docs/sprints/sprint-004.md
# old_string: Phase 3: DDD - Status: pending
# new_string: Phase 3: DDD - Status: ✅ completed (coord-024 approved)
```

**Why**: Edit preserves sprint structure, tracks progress incrementally

---

## Common Pitfalls for Claude Code

### Pitfall 1: Skipping DDD Phase (No Change Request)

**Problem**: User asks to implement feature, Claude jumps straight to code without writing change request

**Fix**: ALWAYS create change request first (DDD Phase 3)

```bash
# User: "Implement validation module"

# BAD: Jump to implementation
Write src/validation.py  # ❌ No contracts defined

# GOOD: Create change request first
Write inbox/active/coord-024/change-request.md  # ✅ Define contracts
# Wait for approval, THEN implement
```

**Why**: DDD defines contracts first, prevents rework and interface conflicts

---

### Pitfall 2: Not Verifying BDD Scenarios Are RED

**Problem**: Write BDD scenarios but don't run behave to verify RED state

**Fix**: ALWAYS run behave after writing scenarios

```bash
# After creating features/validation.feature:

# ALWAYS verify RED:
Bash: behave features/validation.feature
# Expected: X scenarios, X failed ✅

# If scenarios pass, something wrong (implementation exists or step defs incorrect)
```

**Why**: BDD workflow requires RED state before TDD; passing scenarios indicate wrong phase or incorrect step definitions

---

### Pitfall 3: Not Running Quality Gates Before Completion

**Problem**: Mark phase complete without running pytest, ruff, mypy, behave

**Fix**: Run ALL quality gates before marking complete

```bash
# Before marking Phase 6 complete:

# MUST run all 4 quality gates:
Bash: pytest --cov=src --cov-fail-under=85  # ≥85% coverage
Bash: ruff check .                          # 0 lint errors
Bash: mypy --strict src/                    # 0 type errors
Bash: behave features/                      # All scenarios GREEN

# If any fail, fix issues before proceeding
```

**Why**: Quality gates ensure production-ready code; skipping gates introduces bugs

---

### Pitfall 4: Not Updating Ledger After Sprint

**Problem**: Complete sprint but forget to update ledger with metrics

**Fix**: Update ledger immediately after sprint completion

```bash
# After sprint complete:

# Read ledger
Read docs/skilled-awareness/development-lifecycle/ledger.md

# Update with sprint metrics
Edit docs/skilled-awareness/development-lifecycle/ledger.md
# Add: Sprint 004 completed, time spent, quality gate results
```

**Why**: Ledger tracks adoption metrics and ROI; missing data breaks analytics

---

### Pitfall 5: Overwriting Sprint Plan Instead of Editing

**Problem**: Using Write tool to replace sprint plan, losing progress tracking

**Fix**: Use Edit tool for incremental updates

```bash
# BAD
Write docs/project-docs/sprints/sprint-004.md  # ❌ Loses progress

# GOOD
Read docs/project-docs/sprints/sprint-004.md  # Check current state
Edit docs/project-docs/sprints/sprint-004.md  # Update specific phases
```

**Why**: Sprint plans track progress over time; overwriting loses historical context

---

## Support & Resources

**SAP-012 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic development lifecycle workflows (8 phases)
- [Capability Charter](capability-charter.md) - Design principles, DDD→BDD→TDD rationale
- [Protocol Spec](protocol-spec.md) - Phase contracts, quality gates, templates
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Sprint tracking, metrics, version history

**External Resources**:
- [Behave Documentation](https://behave.readthedocs.io/) - BDD framework for Python
- [Gherkin Syntax](https://cucumber.io/docs/gherkin/) - Scenario writing guide
- [pytest Documentation](https://docs.pytest.org/) - Testing framework
- [ruff Documentation](https://docs.astral.sh/ruff/) - Linting and formatting

**Related SAPs**:
- [SAP-004 (testing-framework)](../testing-framework/) - pytest configuration, TDD patterns
- [SAP-005 (ci-cd-workflows)](../ci-cd-workflows/) - GitHub Actions for quality gates
- [SAP-006 (quality-gates)](../quality-gates/) - Coverage, lint, type checking standards
- [SAP-008 (automation-scripts)](../automation-scripts/) - `just` commands for testing

**Templates**:
- `docs/project-docs/templates/SPRINT_PLAN_TEMPLATE.md` - Sprint planning template
- `docs/project-docs/templates/CHANGE_REQUEST_TEMPLATE.md` - DDD change request template

---

## Version History

- **1.0.0** (2025-11-04): Initial CLAUDE.md for SAP-012
  - Claude Code workflows (Sprint start, DDD change request, BDD scenarios)
  - Tool usage patterns (Read templates, Edit sprint plans, Bash for quality gates)
  - Claude-specific tips (Read templates, run quality gates, update ledger, verify RED, incremental edits)
  - Common pitfalls (skip DDD, not verify RED, skip quality gates, forget ledger, overwrite sprint plan)

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic development lifecycle workflows
2. Review [protocol-spec.md](protocol-spec.md) for phase contracts and quality gates
3. Check [capability-charter.md](capability-charter.md) for DDD→BDD→TDD design rationale
4. Start sprint: Create plan → DDD → BDD → TDD → Quality → Review → Release
