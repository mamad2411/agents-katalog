---
name: pwrl-testing
description: Comprehensive testing framework for micro-skill pipeline architecture validation, including unit, integration, compatibility tests, and consolidation audit.
status: specification
created: "2026-06-12"
phases_covered: "6"
---

# pwrl-testing Orchestrator

**Phase 6: Testing & Validation**

Comprehensive testing and validation framework for micro-skill pipeline architecture.

## Interaction Method

- Use platform's `ask_user_question`, `ask_user`, `ask_user_input`, `vscode/askQuestions` or any available extension/tool for user interaction for all decisions
- Ask one question at a time
- Use multiple-choice questions when possible
- If input is empty, ask: "What should be tested? Provide a test scope, files to test, or a skill to validate."
- Provide clear recovery suggestions when errors occur

## Overview

Phase 6 ensures quality of the entire refactored architecture through comprehensive testing and validation.

## Architecture

Pure 4-phase testing pipeline:

```
Code Ready for Testing
  ↓
Phase 1: Micro-Skill Unit Tests (U6.1)
├─ Test each of 17 micro-skills
├─ 40-50 test cases per skill
├─ 8-10 test suites per skill
├─ Happy path + errors + edge cases
├─ Output: Unit test results + coverage
  ↓
Phase 2: Orchestration Integration Tests (U6.2)
├─ Test 4 complete orchestrators
├─ Test phase-to-phase data flow
├─ Test error recovery paths
├─ Test performance benchmarks
├─ Output: Integration test results
  ↓
Phase 3: Backward Compatibility Tests (U6.3)
├─ Verify no breaking changes
├─ Compare old vs. new behavior
├─ Test real-world scenarios
├─ Verify API compatibility
├─ Output: Compatibility report
  ↓
Phase 4: Consolidation Audit (U6.4)
├─ Measure duplication reduction
├─ Verify shared utility adoption
├─ Calculate consolidation metrics
├─ Verify 40%+ reduction achieved
├─ Output: Audit report + metrics
  ↓
Quality Validation Complete
```

## Testing Units

### U6.1: Micro-Skill Unit Tests

**Protocol:** [Micro-Skill Unit Tests Protocol](pwrl-testing/references/micro-skill-unit-tests-protocol.md)

**Scope:**

- Unit tests for each micro-skill
- Multiple test suites per skill (happy path, input validation, error handling, edge cases, performance, integration, recovery, dependencies)
- GIVEN-WHEN-THEN format
- Comprehensive scenario coverage
- Performance benchmarks

### U6.2: Orchestration Integration Tests

**Protocol:** [Orchestration Tests Protocol](pwrl-testing/references/orchestration-tests-protocol.md)

**Scope:**

- Integration tests across all orchestrators
- Full pipeline execution scenarios
- Phase-to-phase data flow verification
- Error recovery path validation
- Performance benchmarking

### U6.3: Backward Compatibility Tests

**Protocol:** [Compatibility Test Protocol](pwrl-testing/references/compatibility-tests-protocol.md)

**Scope:**

- Backward compatibility validation
- Old vs. new behavior verification
- Real-world scenario workflows
- API compatibility verification
- Output format verification
- Error message compatibility

### U6.4: Consolidation & Duplication Audit

**Protocol:** [Consolidation Audit Protocol](pwrl-testing/references/consolidation-audit-protocol.md)

**Scope:**

- Measure code duplication reduction
- Verify shared utility adoption
- Calculate consolidation metrics
- Code quality analysis
- Test consolidation metrics

**Focus Areas:**

- Code duplication reduction measurement
- Shared utility adoption tracking
- Code coverage assessment
- Dependency cycle detection
- Performance overhead analysis

## Test Organization

```
tests/
├── lib/                                    (Shared utilities - Phase 5)
│   ├── context-extraction.test.ts         (10 cases)
│   ├── github-integration.test.ts         (10 cases)
│   ├── artifact-io.test.ts                (10 cases)
│   ├── errors.test.ts                     (10 cases)
│   └── recovery-suggestions.test.ts       (5 cases)
│
├── pwrl-plan/                              (Unit tests for all 4 micro-skills)
│   ├── scope.test.ts                      (40 cases)
│   ├── research.test.ts                   (40 cases)
│   ├── design.test.ts                     (40 cases)
│   └── generate.test.ts                   (35 cases)
│
├── pwrl-work/                              (Unit tests for all 5 micro-skills)
│   ├── triage.test.ts                     (40 cases)
│   ├── prepare.test.ts                    (40 cases)
│   ├── execute.test.ts                    (40 cases)
│   ├── review.test.ts                     (35 cases)
│   └── ship.test.ts                       (35 cases)
│
├── pwrl-review/                            (Unit tests for all 4 micro-skills)
│   ├── scope.test.ts                      (40 cases)
│   ├── prepare.test.ts                    (40 cases)
│   ├── analyze.test.ts                    (45 cases)
│   └── report.test.ts                     (35 cases)
│
├── pwrl-learnings/                         (Unit tests for all 5 micro-skills)
│   ├── extract.test.ts                    (50 cases)  ✓ EXISTS
│   ├── classify.test.ts                   (50 cases)  ✓ EXISTS
│   ├── structure.test.ts                  (45 cases)  ✓ EXISTS
│   ├── dedup.test.ts                      (50 cases)  ✓ EXISTS
│   └── save.test.ts                       (45 cases)  ✓ EXISTS
│
├── integration/                            (Cross-orchestrator tests)
│   ├── pwrl-plan-orchestration.test.ts    (20 cases)
│   ├── pwrl-work-orchestration.test.ts    (20 cases)
│   ├── pwrl-review-orchestration.test.ts  (20 cases)
│   ├── pwrl-learnings-orchestration.test.ts (20 cases)
│   └── cross-orchestrator.test.ts         (20 cases)
│
├── compatibility/                          (Backward compatibility tests)
│   ├── pwrl-plan-compat.test.ts           (15 cases)
│   ├── pwrl-work-compat.test.ts           (15 cases)
│   ├── pwrl-review-compat.test.ts         (15 cases)
│   ├── pwrl-learnings-compat.test.ts      (15 cases)
│   └── real-world-scenarios.test.ts       (20 cases)
│
└── audit/                                  (Consolidation audit verification)
    ├── consolidation-metrics.audit.ts     (Duplication measurement)
    ├── shared-utility-adoption.audit.ts   (Usage verification)
    └── code-quality.audit.ts              (Metrics validation)
```

## Test Statistics

| Category                | Count    | Coverage              |
| ----------------------- | -------- | --------------------- |
| **Unit Tests**          | 150+     | 80%+ of micro-skills  |
| **Integration Tests**   | 100+     | All orchestrators     |
| **Compatibility Tests** | 60+      | 100% API compat       |
| **Audit Tests**         | 10+      | Consolidation metrics |
| **TOTAL**               | **320+** | **Comprehensive**     |

## Quality Gates

**All Must Pass Before Merge:**

- [ ] All 320+ tests passing
- [ ] No flaky tests
- [ ] Code coverage ≥80%
- [ ] Performance <5% overhead
- [ ] 40%+ duplication reduction
- [ ] Backward compatibility 100%
- [ ] Shared utilities adopted by 15+ skills
- [ ] No breaking changes detected

## Performance Targets

| Metric                     | Target | Status     |
| -------------------------- | ------ | ---------- |
| Micro-skill execution      | <100ms | ✓ Baseline |
| Full pipeline (4-5 phases) | <2-3s  | ✓ Target   |
| Test suite runtime         | <30s   | ✓ Target   |
| Code overhead              | <5%    | ✓ Target   |

## Output Artifacts

After Phase 6 completion:

1. **Unit Test Results** — Coverage report showing 80%+ coverage
2. **Integration Test Results** — All 100+ tests passing
3. **Compatibility Report** — 100% backward compatible verified
4. **Consolidation Audit** — Duplication reduction metrics (≥40%)
5. **Quality Metrics** — Code quality scores for all skills

## Success Criteria

✓ All 320+ tests passing
✓ No failing tests
✓ Code coverage ≥80% across all skills
✓ Performance within 5% of baseline
✓ 40%+ code duplication reduction measured
✓ 100% backward compatibility verified
✓ Ready for Phase 7 (documentation) and production

## Related Documents

- [Phase 6 Testing Protocols](pwrl-testing/references/)
  - [Micro-Skill Unit Tests Protocol](pwrl-testing/references/micro-skill-unit-tests-protocol.md)
  - [Orchestration Tests Protocol](pwrl-testing/references/orchestration-tests-protocol.md)
  - [Compatibility Tests Protocol](pwrl-testing/references/compatibility-tests-protocol.md)
  - [Consolidation Audit Protocol](pwrl-testing/references/consolidation-audit-protocol.md)
- [Phase 7: Documentation & Migration](../pwrl-documentation/)
