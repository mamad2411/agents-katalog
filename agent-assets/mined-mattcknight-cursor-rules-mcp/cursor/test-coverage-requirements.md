---
description: Test coverage requirements and quality gates
alwaysApply: false
tags: [development, testing, coverage, quality]
priority: 2
version: 1.0.0
---

# Test Coverage Requirements

## Core Principle

**ALL projects MUST achieve minimum 80% code coverage for unit tests.**

---

## Coverage Requirements

### Minimum Coverage Target

**Unit Tests:**
- **Minimum**: 80% code coverage
- **Target**: 90%+ code coverage (ideal)
- **Critical Paths**: 100% coverage required

**Coverage Metrics:**
- Line coverage: Percentage of code lines executed
- Branch coverage: Percentage of decision branches tested
- Function coverage: Percentage of functions called

---

## Test Requirements by Type

### Unit Tests
- **Coverage Target**: Minimum 80% code coverage
- **Scope**: All services, controllers, models, utilities
- **Focus**: Individual functions and methods
- **Dependencies**: Mock all external dependencies

### Integration Tests
- **Coverage Target**: All critical paths
- **Scope**: API endpoints, database operations, external service calls
- **Focus**: Component interactions
- **Dependencies**: Use test containers or test databases

### Performance Tests
- **Coverage Target**: All performance-critical paths
- **Scope**: High-traffic endpoints, data processing operations
- **Focus**: Response times, throughput, resource usage

---

## Coverage Validation

### Pre-Commit Requirements
- [ ] All new code has unit tests
- [ ] Coverage report generated
- [ ] Minimum 80% coverage verified
- [ ] Coverage gaps identified and documented

### Continuous Integration
- [ ] Coverage reports generated automatically
- [ ] Coverage thresholds enforced in CI pipeline
- [ ] Coverage trends tracked over time
- [ ] Coverage gaps reported in build failures

---

## Critical Rules

### ALWAYS
- ✅ Achieve minimum 80% code coverage for unit tests
- ✅ Generate coverage reports before committing
- ✅ Test all public methods and critical paths
- ✅ Mock external dependencies in unit tests
- ✅ Document coverage gaps if <80%

### NEVER
- ❌ Commit code with <80% coverage (without documented exception)
- ❌ Skip unit tests for new code
- ❌ Skip coverage validation
- ❌ Accept coverage gaps without documentation

---

**Last Updated:** 2025-01-22  
**Version:** 1.0.0  
**Rule Type:** Development - Testing  
**Priority:** HIGH
