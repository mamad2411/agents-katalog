---
name: comprehensive-toolkit
description: Consolidated toolkit for comprehensive. Covers comprehensive-review-full-review, comprehensive-review-pr-enhance
---
# Comprehensive Toolkit

## Use this skill when
- Needing guidance, best practices, or checklists for comprehensive review full review
- Organizing tests, risks, and rollout notes
- Reducing PR size or improving reviewability
- Summarizing changes for faster reviews
- Working on comprehensive review full review tasks or workflows
- Writing or improving PR descriptions

## Do not use this skill when
- The task is unrelated to comprehensive review full review
- The task is unrelated to software delivery
- There is no PR or change list to summarize
- You need a different domain or tool outside this scope
- You need a full code review instead of PR polishing

## Core Capabilities
# Comprehensive Toolkit

## Review Configuration Options

- **--security-focus**: Prioritize security vulnerabilities and OWASP compliance
- **--performance-critical**: Emphasize performance bottlenecks and scalability issues
- **--tdd-review**: Include TDD compliance and test-first verification
- **--ai-assisted**: Enable AI-powered review tools (Copilot, Codium, Bito)
- **--strict-mode**: Fail review on any critical issues found
- **--metrics-report**: Generate detailed quality metrics dashboard
- **--framework [name]**: Apply framework-specific best practices (React, Spring, Django, etc.)

## Phase 1: Code Quality & Architecture Review

Use Task tool to orchestrate quality and architecture agents in parallel:

### 1A. Code Quality Analysis
- Use Task tool with subagent_type="code-reviewer"
- Prompt: "Perform comprehensive code quality review for: $ARGUMENTS. Analyze code complexity, maintainability index, technical debt, code duplication, naming conventions, and adherence to Clean Code principles. Integrate with SonarQube, CodeQL, and Semgrep for static analysis. Check for code smells, anti-patterns, and violations of SOLID principles. Generate cyclomatic complexity metrics and identify refactoring opportunities."
- Expected output: Quality metrics, code smell inventory, refactoring recommendations
- Context: Initial codebase analysis, no dependencies on other phases

### 1B. Architecture & Design Review
- Use Task tool with subagent_type="architect-review"
- Prompt: "Review architectural design patterns and structural integrity in: $ARGUMENTS. Evaluate microservices boundaries, API design, database schema, dependency management, and adherence to Domain-Driven Design principles. Check for circular dependencies, inappropriate coupling, missing abstractions, and architectural drift. Verify compliance with enterprise architecture standards and cloud-native patterns."
- Expected output: Architecture assessment, design pattern analysis, structural recommendations
- Context: Runs parallel with code quality analysis

## Phase 2: Security & Performance Review

Use Task tool with security and performance agents, incorporating Phase 1 findings:

### 2A. Security Vulnerability Assessment
- Use Task tool with subagent_type="security-auditor"
- Prompt: "Execute comprehensive security audit on: $ARGUMENTS. Perform OWASP Top 10 analysis, dependency vulnerability scanning with Snyk/Trivy, secrets detection with GitLeaks, input validation review, authentication/authorization assessment, and cryptographic implementation review. Include findings from Phase 1 architecture review: {phase1_architecture_context}. Check for SQL injection, XSS, CSRF, insecure deserialization, and configuration security issues."
- Expected output: Vulnerability report, CVE list, security risk matrix, remediation steps
- Context: Incorporates architectural vulnerabilities identified in Phase 1B

### 2B. Performance & Scalability Analysis
- Use Task tool with subagent_type="application-performance::performance-engineer"
- Prompt: "Conduct performance analysis and scalability assessment for: $ARGUMENTS. Profile code for CPU/memory hotspots, analyze database query performance, review caching strategies, identify N+1 problems, assess connection pooling, and evaluate asynchronous processing patterns. Consider architectural findings from Phase 1: {phase1_architecture_context}. Check for memory leaks, resource contention, and bottlenecks under load."
- Expected output: Performance metrics, bottleneck analysis, optimization recommendations
- Context: Uses architecture insights to identify systemic performance issues

## Phase 3: Testing & Documentation Review

Use Task tool for test and documentation quality assessment:

### 3A. Test Coverage & Quality Analysis
- Use Task tool with subagent_type="unit-testing::test-automator"
- Prompt: "Evaluate testing strategy and implementation for: $ARGUMENTS. Analyze unit test coverage, integration test completeness, end-to-end test scenarios, test pyramid adherence, and test maintainability. Review test quality metrics including assertion density, test isolation, mock usage, and flakiness. Consider security and performance test requirements from Phase 2: {phase2_security_context}, {phase2_performance_context}. Verify TDD practices if --tdd-review flag is set."
- Expected output: Coverage report, test quality metrics, testing gap analysis
- Context: Incorporates security and performance testing requirements from Phase 2

### 3B. Documentation & API Specification Review
- Use Task tool with subagent_type="code-documentation::docs-architect"
- Prompt: "Review documentation completeness and quality for: $ARGUMENTS. Assess inline code documentation, API documentation (OpenAPI/Swagger), architecture decision records (ADRs), README completeness, deployment guides, and runbooks. Verify documentation reflects actual implementation based on all previous phase findings: {phase1_context}, {phase2_context}. Check for outdated documentation, missing examples, and unclear explanations."
- Expected output: Documentation coverage report, inconsistency list, improvement recommendations
- Context: Cross-references all previous findings to ensure documentation accuracy

## Phase 4: Best Practices & Standards Compliance

Use Task tool to verify framework-specific and industry best practices:

### 4A. Framework & Language Best Practices
- Use Task tool with subagent_type="framework-migration::legacy-modernizer"
- Prompt: "Verify adherence to framework and language best practices for: $ARGUMENTS. Check modern JavaScript/TypeScript patterns, React hooks best practices, Python PEP compliance, Java enterprise patterns, Go idiomatic code, or framework-specific conventions (based on --framework flag). Review package management, build configuration, environment handling, and deployment practices. Include all quality issues from previous phases: {all_previous_contexts}."
- Expected output: Best practices compliance report, modernization recommendations
- Context: Synthesizes all previous findings for framework-specific guidance

### 4B. CI/CD & DevOps Practices Review
- Use Task tool with subagent_type="cicd-automation::deployment-engineer"
- Prompt: "Review CI/CD pipeline and DevOps practices for: $ARGUMENTS. Evaluate build automation, test automation integration, deployment strategies (blue-green, canary), infrastructure as code, monitoring/observability setup, and incident response procedures. Assess pipeline security, artifact management, and rollback capabilities. Consider all issues identified in previous phases that impact deployment: {all_critical_issues}."
- Expected output: Pipeline assessment, DevOps maturity evaluation, automation recommendations
- Context: Focuses on operationalizing fixes for all identified issues

## Consolidated Report Generation

Compile all phase outputs into comprehensive review report:

### Critical Issues (P0 - Must Fix Immediately)
- Security vulnerabilities with CVSS > 7.0
- Data loss or corruption risks
- Authentication/authorization bypasses
- Production stability threats
- Compliance violations (GDPR, PCI DSS, SOC2)

### High Priority (P1 - Fix Before Next Release)
- Performance bottlenecks impacting user experience
- Missing critical test coverage
- Architectural anti-patterns causing technical debt
- Outdated dependencies with known vulnerabilities
- Code quality issues affecting maintainability

### Medium Priority (P2 - Plan for Next Sprint)
- Non-critical performance optimizations
- Documentation gaps and inconsistencies
- Code refactoring opportunities
- Test quality improvements
- DevOps automation enhancements

### Low Priority (P3 - Track in Backlog)
- Style guide violations
- Minor code smell issues
- Nice-to-have documentation updates
- Cosmetic improvements

## Success Criteria

Review is considered successful when:
- All critical security vulnerabilities are identified and documented
- Performance bottlenecks are profiled with remediation paths
- Test coverage gaps are mapped with priority recommendations
- Architecture risks are assessed with mitigation strategies
- Documentation reflects actual implementation state
- Framework best practices compliance is verified
- CI/CD pipeline supports safe deployment of reviewed code
- Clear, actionable feedback is provided for all findings
- Metrics dashboard shows improvement trends
- Team has clear prioritized action plan for remediation

Target: $ARGUMENTS

---

# Pull Request Enhancement

You are a PR optimization expert specializing in creating high-quality pull requests that facilitate efficient code reviews. Generate comprehensive PR descriptions, automate review processes, and ensure PRs follow best practices for clarity, size, and reviewability.

## Context
The user needs to create or improve pull requests with detailed descriptions, proper documentation, test coverage analysis, and review facilitation. Focus on making PRs that are easy to review, well-documented, and include all necessary context.

## Requirements
$ARGUMENTS

## Output Format

- PR summary and scope
- What changed and why
- Tests performed and results
- Risks, rollbacks, and reviewer notes

## Resources

- `resources/implementation-playbook.md` for detailed templates and examples.

---
