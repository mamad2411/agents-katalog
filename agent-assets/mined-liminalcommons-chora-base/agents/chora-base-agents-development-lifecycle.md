# AGENTS.md - Development Lifecycle (SAP-012)

**Domain**: Development Lifecycle & Workflows
**SAP**: SAP-012 (development-lifecycle)
**Version**: 1.5.0
**Last Updated**: 2025-11-06

---

## Overview

This is the domain-specific AGENTS.md file for the development lifecycle (SAP-012). It provides context for agents working with the DDD→BDD→TDD workflow, sprint planning, and release management.

**Parent**: See [/AGENTS.md](/AGENTS.md) for project-level context

**Pattern**: "Nearest File Wins" - This file provides development-lifecycle-specific context

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

This AGENTS.md provides: Agent-specific patterns for implementing SAP-012.
e.

---

## User Signal Patterns

### Workflow Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "start new sprint" | create_sprint_plan() | Copy SPRINT_PLAN_TEMPLATE.md | Follow SAP-012 Phase 2 |
| "create change request" | create_ddd_change_request() | Copy CHANGE_REQUEST_TEMPLATE.md | DDD Phase 3 |
| "write scenarios" | create_bdd_scenarios() | Create .feature file | BDD Phase 4 |
| "implement feature" | tdd_implementation() | RED-GREEN-REFACTOR cycle | TDD Phase 5 |
| "run quality gates" | validate_quality_gates() | pytest --cov, ruff, mypy | Phase 6 |
| "create release" | create_release() | Update CHANGELOG, git tag | Phase 8 |

### Sprint Planning

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "plan next sprint" | create_sprint_plan() | Edit docs/project-docs/sprints/sprint-NN.md | Use template |
| "update sprint" | edit_sprint_plan() | Edit current sprint file | Track progress |
| "complete sprint" | complete_sprint() | Move to completed/, update ledger | Archive work |
| "show sprint status" | display_sprint_status() | Read current sprint file | Progress overview |

### DDD (Documentation Driven Design)

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "define contracts" | create_change_request() | Write change-request.md | Define interfaces |
| "approve change request" | approve_change_request() | Add approval signature | Move to Phase 4 |
| "update change request" | edit_change_request() | Edit change-request.md | Iterate on design |

### BDD (Behavior Driven Development)

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "write scenarios" | create_feature_file() | Write features/*.feature | Gherkin syntax |
| "add scenario" | add_bdd_scenario() | Edit .feature file | New test case |
| "write step definitions" | create_step_definitions() | Write features/steps/*.py | Implement steps |
| "run scenarios" | run_behave() | behave features/ | Validate scenarios |
| "check scenario status" | behave_dry_run() | behave --dry-run | Check RED/GREEN |

### TDD (Test Driven Development)

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "write failing test" | create_red_test() | Write test_*.py | RED state |
| "make test pass" | implement_green() | Write implementation | GREEN state |
| "refactor code" | refactor_implementation() | Improve while tests pass | REFACTOR state |
| "run TDD cycle" | run_red_green_refactor() | RED→GREEN→REFACTOR | Full cycle |

### Quality Gates

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "validate quality" | run_quality_gates() | pytest, ruff, mypy, behave | All gates |
| "check coverage" | validate_coverage() | pytest --cov --cov-fail-under=85 | ≥85% required |
| "check lint" | validate_lint() | ruff check . | 0 errors required |
| "check types" | validate_types() | mypy --strict . | 0 errors required |
| "check scenarios" | validate_scenarios() | behave features/ | All pass required |

### Release Management

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "update changelog" | edit_changelog() | Edit CHANGELOG.md | Semantic versioning |
| "bump version" | bump_version() | Update SAP artifacts | MAJOR.MINOR.PATCH |
| "create release" | create_github_release() | gh release create vX.Y.Z | GitHub release |
| "tag release" | tag_release() | git tag vX.Y.Z && git push --tags | Version tag |

### Common Variations

**Workflow Queries**:
- "start work" / "begin sprint" / "new iteration" → create_sprint_plan()
- "design first" / "define contracts" / "DDD" → create_change_request()
- "write tests" / "BDD" / "scenarios" → create_feature_file()
- "implement" / "TDD" / "make it work" → tdd_implementation()

**Quality Queries**:
- "validate" / "check quality" / "run gates" → run_quality_gates()
- "coverage?" / "how's coverage" / "test coverage" → validate_coverage()
- "lint clean?" / "any lint errors" → validate_lint()

**Release Queries**:
- "ship it" / "deploy" / "create release" → create_release()
- "update version" / "bump version" → bump_version()

---

## Development Lifecycle Quick Reference

### 8-Phase Workflow (SAP-012)

**Phase 1: Vision & Requirements**
- Define problem, goals, success criteria
- Identify stakeholders, constraints
- Artifact: Vision document (optional, can be in coordination request)

**Phase 2: Planning & Architecture**
- Create sprint plan (SPRINT_PLAN_TEMPLATE.md)
- Define phases, tasks, estimates
- Update governance docs (SAP ledger, ECOSYSTEM_STATUS.yaml)
- Artifact: Sprint plan (docs/project-docs/sprints/sprint-NN.md)

**Phase 3: DDD (Documentation Driven Design)**
- Write change request defining contracts
- Specify inputs, outputs, behaviors, error handling
- Get approval before implementation
- Artifact: change-request.md (inbox/active/coord-NNN/)

**Phase 4: BDD (Behavior Driven Development)**
- Write Gherkin scenarios (.feature files)
- Write step definitions (features/steps/*.py)
- Verify all scenarios RED (pre-implementation)
- Artifact: features/*.feature, features/steps/*.py

**Phase 5: TDD (Test Driven Development)**
- RED: Write failing test
- GREEN: Implement minimum code to pass
- REFACTOR: Improve code while maintaining GREEN
- Repeat until all scenarios GREEN
- Artifact: Implementation code + tests

**Phase 6: Testing & Quality Gates**
- Run full test suite (pytest, behave)
- Validate coverage ≥85%
- Check lint (ruff check, 0 errors)
- Check types (mypy --strict, 0 errors)
- Artifact: Quality gate results

**Phase 7: Review & Integration**
- Create pull request
- Code review and approval
- CI/CD validation
- Artifact: GitHub PR

**Phase 8: Release & Deployment**
- Update CHANGELOG.md
- Update SAP artifacts (version bump)
- Create GitHub release
- Archive completed work
- Artifact: GitHub release, updated docs

### DDD Change Request Structure

**Template**: `docs/project-docs/templates/CHANGE_REQUEST_TEMPLATE.md`

**Required Sections**:
1. **Overview**: Problem, goals, scope
2. **Technical Specifications**: Contracts, interfaces, data structures
3. **Implementation Plan**: Phases, tasks, estimates
4. **Acceptance Criteria**: Success conditions (must be testable)
5. **Dependencies**: Prerequisites, related work
6. **Risks & Mitigations**: Potential issues, solutions
7. **Quality Gates**: Coverage, lint, type checking, scenario pass rate
8. **Approval**: Signature section

**Example Contract**:
```python
class IntentMatch:
    """Contract for intent routing result."""
    action: str              # Formal action identifier
    confidence: float        # Match confidence 0.0-1.0
    parameters: dict         # Extracted parameters
    pattern_id: str          # Matching pattern ID
    clarification: str|None  # Clarification question if needed

    def __post_init__(self):
        assert 0.0 <= self.confidence <= 1.0
        assert self.action  # Non-empty string
```

### BDD Scenario Structure

**Template**: Gherkin syntax (Given-When-Then)

**Example**:
```gherkin
Feature: Intent Recognition
  As a user
  I want to use natural language
  So that I can interact conversationally

  Scenario: Recognize exact inbox status query
    Given the intent router is initialized
    When user input is "show inbox"
    Then intent should be "run_inbox_status"
    And confidence should be >= 0.70
    And clarification should be empty
```

**Step Definitions**:
```python
from behave import given, when, then

@given('the intent router is initialized')
def step_impl(context):
    from scripts.intent_router import IntentRouter
    context.router = IntentRouter()

@when('user input is "{text}"')
def step_impl(context, text):
    context.matches = context.router.route(text)

@then('intent should be "{action}"')
def step_impl(context, action):
    assert context.matches[0].action == action
```

### TDD Cycle

**RED State**: Write failing test
```python
def test_intent_recognition():
    router = IntentRouter()
    matches = router.route("show inbox")
    # This will FAIL because IntentRouter.route() doesn't exist yet
    assert matches[0].action == "run_inbox_status"
```

**GREEN State**: Implement minimum code
```python
class IntentRouter:
    def route(self, user_input: str) -> list[IntentMatch]:
        if "show inbox" in user_input.lower():
            return [IntentMatch(action="run_inbox_status", confidence=0.95)]
        return []
```

**REFACTOR State**: Improve implementation
```python
class IntentRouter:
    def __init__(self):
        self.patterns = self._load_patterns()

    def route(self, user_input: str) -> list[IntentMatch]:
        # Improved: Pattern matching instead of hardcoded
        matches = []
        for pattern in self.patterns:
            score = self._calculate_confidence(user_input, pattern)
            if score > 0.50:
                matches.append(IntentMatch(
                    action=pattern.action,
                    confidence=score,
                    pattern_id=pattern.id
                ))
        return sorted(matches, key=lambda m: m.confidence, reverse=True)
```

### Quality Gate Commands

**Run All Quality Gates**:
```bash
# Coverage (≥85%)
pytest --cov=scripts --cov=src --cov-report=term-missing --cov-fail-under=85

# Lint (0 errors)
ruff check .

# Type checking (0 errors)
mypy --strict scripts/ src/

# BDD scenarios (all pass)
behave features/

# All together (CI/CD)
pytest --cov --cov-fail-under=85 && ruff check . && mypy --strict . && behave features/
```

**Pre-Commit Checklist**:
- [ ] All tests passing
- [ ] Coverage ≥85%
- [ ] No lint errors
- [ ] No type errors
- [ ] All BDD scenarios GREEN

**Pre-PR Checklist**:
- [ ] All tests passing
- [ ] Coverage ≥85%
- [ ] All BDD scenarios GREEN
- [ ] Change request approved
- [ ] CHANGELOG.md updated
- [ ] Documentation updated

### Sprint Planning

**Create New Sprint**:
```bash
# 1. Copy template
cp docs/project-docs/templates/SPRINT_PLAN_TEMPLATE.md \
   docs/project-docs/sprints/sprint-05.md

# 2. Fill in details
# - Sprint ID, version, goal
# - Estimated effort
# - Phases and tasks
# - Dependencies, risks

# 3. Update governance
# - SAP ledger: Mark "In Progress"
# - ECOSYSTEM_STATUS.yaml: Add to active_work
# - Emit event: phase_started
```

**Track Progress**:
```bash
# Update sprint plan with progress
# Use checkboxes: - [ ] Task (pending), - [x] Task (complete)

# Example:
# Phase 4: TDD Implementation
# - [x] Task 4.1: Enhance protocol-spec.md
# - [x] Task 4.2: Enhance awareness-guide.md
# - [ ] Task 4.3: Update domain AGENTS.md files (3/5 complete)
```

**Complete Sprint**:
```bash
# 1. Mark all tasks complete in sprint plan
# 2. Update SAP ledger: "Completed" or new version
# 3. Update ECOSYSTEM_STATUS.yaml: Move to recent_completions
# 4. Archive sprint plan (optional): mv to completed/
# 5. Emit event: sprint_completed
```

### Release Management

**Semantic Versioning**:
- **MAJOR** (X.0.0): Breaking changes, incompatible API
- **MINOR** (x.Y.0): New features, backward compatible
- **PATCH** (x.y.Z): Bug fixes, backward compatible

**Version Bump Checklist**:
1. Update CHANGELOG.md (new version section)
2. Update SAP artifact versions (charter, protocol, awareness, blueprint, ledger)
3. Update SAP Index (docs/skilled-awareness/INDEX.md)
4. Create git tag: `git tag vX.Y.Z`
5. Push tag: `git push --tags`
6. Create GitHub release: `gh release create vX.Y.Z`

**CHANGELOG Entry Format**:
```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Enhancements to existing features

### Fixed
- Bug fixes

### Breaking Changes
- Incompatible changes (MAJOR version only)
```

---

## Integration with Bidirectional Translation Layer

This domain AGENTS.md file integrates with the bidirectional translation layer (SAP-009 v1.1.0):

**Discovery Flow**:
1. User says "start new sprint" (casual, conversational)
2. Intent router loads root AGENTS.md (discovers intent-router.py exists)
3. Intent router loads THIS FILE (domain-specific patterns)
4. Matches "start new sprint" → `create_sprint_plan` with high confidence
5. Agent copies SPRINT_PLAN_TEMPLATE.md and prompts for details
6. Agent updates governance docs (SAP ledger, ECOSYSTEM_STATUS.yaml)

**Context-Aware Suggestions**:
- If sprint plan exists but incomplete, suggest continuing current sprint
- If change request approved, suggest moving to BDD phase
- If all scenarios GREEN, suggest running quality gates
- If quality gates pass, suggest creating release
- Prioritizes next phase in workflow progression

**Progressive Formalization**:
- Week 1: "let's start working" → Agent explains 8-phase workflow
- Week 2-4: "create sprint plan" → Agent creates plan from template
- Month 2+: "Phase 2" → Agent recognizes phase number directly
- Month 3+: User navigates workflow phases independently

**See**: [/AGENTS.md lines 732-944](/AGENTS.md) for bidirectional translation layer overview

---

## Common Tasks

### Start New Sprint

**Goal**: Create sprint plan for new work

**Steps**:
1. Copy template: `cp docs/project-docs/templates/SPRINT_PLAN_TEMPLATE.md docs/project-docs/sprints/sprint-NN.md`
2. Fill in metadata (Sprint ID, version, goal, effort)
3. Define 8 phases with tasks and estimates
4. Update SAP ledger: Mark "In Progress"
5. Update ECOSYSTEM_STATUS.yaml: Add to active_work
6. Emit event: `phase_started` (Governance_Updates)

**Expected Output**: Sprint plan file with 8 phases, ≥10 tasks

### Create DDD Change Request

**Goal**: Define contracts before implementation

**Steps**:
1. Copy template: `cp docs/project-docs/templates/CHANGE_REQUEST_TEMPLATE.md inbox/active/coord-NNN/change-request.md`
2. Write overview (problem, goals, scope)
3. Define technical specifications (contracts, interfaces)
4. Create implementation plan (phases, tasks)
5. Define acceptance criteria (testable conditions)
6. Get approval: Add approval signature
7. Emit event: `change_request_approved`

**Expected Output**: Change request with contracts, acceptance criteria, approval

### Write BDD Scenarios

**Goal**: Define expected behaviors in Gherkin

**Steps**:
1. Create feature file: `features/my-feature.feature`
2. Write Feature description (As a... I want... So that...)
3. Write Scenario(s) (Given-When-Then format)
4. Create step definitions: `features/steps/my_steps.py`
5. Implement step functions (@given, @when, @then)
6. Run behave: `behave features/my-feature.feature --dry-run`
7. Verify all scenarios RED (pre-implementation)

**Expected Output**: .feature file + step definitions, all RED

### Run TDD Cycle

**Goal**: Implement feature using RED-GREEN-REFACTOR

**Steps**:
1. RED: Write failing test (assert not yet implemented)
2. Run test: `pytest test_my_feature.py` (should FAIL)
3. GREEN: Write minimum code to pass test
4. Run test: `pytest test_my_feature.py` (should PASS)
5. REFACTOR: Improve code while maintaining GREEN
6. Run test: `pytest test_my_feature.py` (should still PASS)
7. Repeat until all scenarios GREEN

**Expected Output**: Implemented feature + passing tests

### Validate Quality Gates

**Goal**: Ensure code meets quality standards

**Steps**:
1. Run coverage: `pytest --cov --cov-fail-under=85`
2. Run lint: `ruff check .`
3. Run type check: `mypy --strict .`
4. Run BDD: `behave features/`
5. Verify all gates pass (0 errors, ≥85% coverage, all scenarios GREEN)

**Expected Output**: All quality gates PASS

### Create Release

**Goal**: Version and release completed work

**Steps**:
1. Update CHANGELOG.md (new version section)
2. Update SAP artifacts (version bump)
3. Update SAP Index
4. Commit changes: `git add . && git commit -m "chore: Release vX.Y.Z"`
5. Create tag: `git tag vX.Y.Z`
6. Push tag: `git push --tags`
7. Create GitHub release: `gh release create vX.Y.Z --notes "$(cat CHANGELOG.md | head -20)"`

**Expected Output**: GitHub release, git tag, updated CHANGELOG

---

## Related SAPs

- **SAP-001** (inbox-protocol): Coordination request intake (Phase 1-2)
- **SAP-004** (testing-framework): pytest, behave integration (Phase 6)
- **SAP-005** (ci-cd-workflows): GitHub Actions automation (Phase 7)
- **SAP-006** (quality-gates): Coverage, lint, type checking enforcement (Phase 6)
- **SAP-009** (agent-awareness): Workflow discovery via bidirectional translation
- **SAP-012** (development-lifecycle): THIS SAP - 8-phase workflow
- **SAP-013** (documentation-framework): Documentation standards (DDD, BDD)

---

**Version History**:
- **1.2.0** (2025-10-31): Added bidirectional translation layer integration, user signal patterns
- **1.1.0** (2025-10-29): Enhanced with BDD/TDD examples
- **1.0.0** (2025-10-28): Initial domain AGENTS.md for development lifecycle

