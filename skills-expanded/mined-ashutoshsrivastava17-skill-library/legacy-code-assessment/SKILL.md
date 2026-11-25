---
name: legacy-code-assessment
description: >
  Assess legacy codebases — code health metrics, dependency mapping,
  risk areas, technical debt quantification, and modernization roadmap.
  TRIGGER when: user says /legacy-code-assessment, needs to evaluate an old
  codebase, or asks about modernizing or understanding legacy systems.
argument-hint: "[codebase or system to assess]"
user-invocable: true
---

# Legacy Code Assessment

You are a software architect. Systematically assess a legacy codebase to inform modernization decisions.

## Process

### Step 1: Gather Overview

| Dimension | Assessment |
|-----------|-----------|
| Age | When was it written? Last major update? |
| Language/framework | What versions? Still supported? |
| Size | Lines of code, number of files, modules |
| Team | Original authors still available? Current maintainers? |
| Documentation | Architecture docs, README, inline comments? |
| Tests | Test coverage? Do tests pass? Are they trusted? |
| Deployment | How is it deployed? CI/CD or manual? |

### Step 2: Assess Code Health

| Metric | Tool | What It Reveals |
|--------|------|----------------|
| Cyclomatic complexity | SonarQube, radon | Functions that are too complex |
| Code duplication | SonarQube, jscpd | Copy-paste patterns |
| Dependency freshness | Dependabot, npm audit | Outdated/vulnerable dependencies |
| Test coverage | Coverage tools | Untested risk areas |
| Dead code | Coverage + static analysis | Code that can be safely removed |
| Churn rate | `git log` analysis | Files changed most often (hotspots) |
| Coupling | Structure analysis | Modules with too many dependencies |

### Step 3: Map Dependencies

| Dependency Type | Risk |
|----------------|------|
| EOL frameworks | No security patches, forced migration |
| Unmaintained libraries | No bug fixes, growing CVE exposure |
| Tightly coupled modules | Can't change one without breaking others |
| External services | API deprecation, vendor lock-in |
| Database schema | Migration complexity |
| Build tools | Outdated toolchain, CI compatibility |

### Step 4: Identify Risk Areas

| Risk | Indicator | Severity |
|------|-----------|----------|
| Security | Vulnerable dependencies, no input validation | Critical |
| Reliability | No tests, no monitoring, crash-prone code | High |
| Maintainability | High complexity, no docs, original team gone | High |
| Performance | Known bottlenecks, no profiling data | Medium |
| Scalability | Hardcoded limits, monolithic design | Medium |
| Compliance | Missing audit trails, data handling issues | Variable |

### Step 5: Quantify Technical Debt

| Category | Estimated Effort to Fix | Business Impact if Ignored |
|----------|----------------------|---------------------------|
| Security vulnerabilities | X person-weeks | Data breach risk |
| Framework upgrade | X person-weeks | No security patches after [date] |
| Test coverage gaps | X person-weeks | Regressions in production |
| Documentation gaps | X person-weeks | Onboarding takes X weeks instead of X days |
| Performance issues | X person-weeks | User churn, SLA violations |

### Step 6: Recommend Modernization Path

| Strategy | When | Risk | Investment |
|----------|------|------|-----------|
| Maintain as-is | Low business criticality, stable | Low | Low |
| Incremental refactor | High value, team knows the code | Medium | Medium |
| Strangler fig | Need to modernize without downtime | Medium | High |
| Rewrite | Fundamentally broken, small codebase | High | Very high |
| Replace (buy) | Commodity functionality, SaaS available | Low | Variable |

## Output Format

```markdown
## Legacy Assessment: [System]

### Overview: [Age, size, language, team]
### Health Metrics: [Complexity, coverage, dependencies]
### Risk Areas: [Prioritized risks]
### Technical Debt: [Quantified by category]
### Recommendation: [Modernization strategy with rationale]
### Roadmap: [Phased plan if modernizing]
```

## Quality Checklist

- [ ] Codebase actually explored (not just discussed)
- [ ] Health metrics are data-driven
- [ ] Dependencies assessed for EOL and vulnerabilities
- [ ] Risk areas prioritized by business impact
- [ ] Technical debt is quantified in effort, not just listed
- [ ] Recommendation matches business context (not always "rewrite")
- [ ] Team knowledge and availability factored in

## Edge Cases

- If original team is gone, budget extra time for code archaeology
- If the system "works fine," focus assessment on risk, not functionality
- For systems with no tests, add characterization tests before any changes
- If the business wants a rewrite, present incremental alternatives first
- For compliance-critical systems, prioritize audit trail and access control gaps
