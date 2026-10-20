# Agent Workflow Examples

This guide provides practical examples of how to use the Claude Command Suite agents together for common development scenarios.

## 🚀 Complete Feature Development Workflow

### Scenario: Adding a User Dashboard Feature

```bash
# 1. Strategic Planning
"Use strategic-analyst to model scenarios for adding a user analytics dashboard to our SaaS product"

# 2. Architecture Design  
"Have project-architect design the dashboard module structure with React and TypeScript"

# 3. Implementation
"Create the dashboard components following our design"

# 4. Code Review
"Use code-auditor to review the dashboard implementation"

# 5. Security Check
"Have security-auditor specifically check the data access patterns in the dashboard"

# 6. Test Generation
"Use test-engineer to create comprehensive tests for the dashboard components"

# 7. Performance Analysis
"Have performance-auditor analyze the dashboard rendering performance"

# 8. Integration Setup
"Use integration-manager to create Linear tasks for remaining dashboard work"

# 9. Release Preparation
"Have release-manager prepare the dashboard feature for deployment"
```

## 🐛 Bug Fix Workflow

### Scenario: Critical Production Bug

```bash
# 1. Issue Sync
"Use integration-manager to sync GitHub issue #456 about the login bug to Linear"

# 2. Code Analysis
"Have code-auditor analyze the authentication module for potential issues"

# 3. Security Review
"Use security-auditor to check if this is a security vulnerability"

# 4. Fix Implementation
"Fix the authentication bug in the login handler"

# 5. Test Creation
"Have test-engineer create regression tests for this bug"

# 6. Hotfix Release
"Use release-manager to prepare and deploy a hotfix"
```

## 🏗️ New Project Setup Workflow

### Scenario: Starting a New Microservice

```bash
# 1. Strategic Analysis
"Use strategic-analyst to evaluate microservice vs monolith for our inventory system"

# 2. Project Setup
"Have project-architect create a new Node.js microservice for inventory management"

# 3. Integration Planning
"Use integration-manager to set up GitHub-Linear sync for the new project"

# 4. Architecture Review
"Have architecture-auditor review the microservice boundaries and API design"

# 5. Test Infrastructure
"Use test-engineer to set up the testing framework and initial tests"

# 6. CI/CD Setup
"Have release-manager configure the deployment pipeline"
```

## 🔍 Code Quality Improvement Workflow

### Scenario: Technical Debt Reduction

```bash
# 1. Full Audit
"Run all code auditors on the legacy payments module"

# Agent Chain Activation:
- code-auditor → Identifies general issues
- architecture-auditor → Finds design problems  
- performance-auditor → Discovers bottlenecks
- security-auditor → Uncovers vulnerabilities

# 2. Prioritization
"Use strategic-analyst to prioritize which technical debt to address first"

# 3. Task Creation
"Have integration-manager create Linear tasks for each improvement"

# 4. Implementation
"Refactor the payment processing based on architecture-auditor recommendations"

# 5. Testing
"Use test-engineer to ensure refactoring didn't break functionality"
```

## 🚢 Release Preparation Workflow

### Scenario: Major Version Release

```bash
# 1. Pre-Release Analysis
"Have code-auditor do a complete review of all changes for v2.0"

# 2. Security Audit
"Use security-auditor to do a final security check before release"

# 3. Performance Baseline
"Have performance-auditor establish performance metrics for v2.0"

# 4. Test Coverage
"Use test-engineer to ensure we have >90% test coverage"

# 5. Release Preparation
"Have release-manager prepare the v2.0 release with changelog and migration guide"

# 6. Deployment Planning
"Use strategic-analyst to model rollout strategies for v2.0"
```

## 🔄 Integration Sync Workflow

### Scenario: Bi-directional GitHub-Linear Sync

```bash
# 1. Initial Setup
"Use integration-manager to set up bidirectional sync between GitHub and Linear"

# 2. Bulk Import
"Have integration-manager import all open GitHub issues to Linear"

# 3. Workflow Creation
"Create an automated workflow where:
- New GitHub issues → integration-manager → Linear tasks
- Linear status updates → integration-manager → GitHub issue updates
- PR merges → integration-manager → Linear task completion"

# 4. Monitoring
"Set up integration-manager to report daily sync status"
```

## 🎯 Performance Optimization Workflow

### Scenario: Slow API Response Times

```bash
# 1. Performance Analysis
"Use performance-auditor to analyze the user API endpoints"

# 2. Database Review
"Have performance-auditor specifically check database queries in the user service"

# 3. Architecture Assessment
"Use architecture-auditor to evaluate if the service architecture is causing bottlenecks"

# 4. Implementation
"Implement the caching strategy recommended by performance-auditor"

# 5. Testing
"Have test-engineer create performance tests to verify improvements"

# 6. Monitoring Setup
"Use project-architect to add performance monitoring"
```

## 🛡️ Security Incident Response Workflow

### Scenario: Potential Security Vulnerability Reported

```bash
# 1. Immediate Assessment
"Use security-auditor to investigate the reported XSS vulnerability in comments"

# 2. Impact Analysis
"Have strategic-analyst model the potential impact of this vulnerability"

# 3. Fix Development
"Implement security-auditor's recommended fixes immediately"

# 4. Testing
"Use test-engineer to create security-specific tests"

# 5. Emergency Release
"Have release-manager prepare an emergency security patch"

# 6. Post-Mortem
"Use integration-manager to create tasks for security improvements"
```

## 📊 Strategic Planning Workflow

### Scenario: Evaluating Technology Migration

```bash
# 1. Current State Analysis
"Use architecture-auditor to document our current monolith architecture"

# 2. Scenario Modeling
"Have strategic-analyst model scenarios for migrating to microservices over 18 months"

# 3. Risk Assessment
"Use strategic-analyst to identify risks and mitigation strategies"

# 4. Implementation Planning
"Have project-architect create a phased migration plan"

# 5. Task Breakdown
"Use integration-manager to create an epic with all migration tasks in Linear"
```

## 🔗 Agent Chaining Patterns

### Pattern 1: Sequential Analysis
```
code-auditor → security-auditor → performance-auditor → test-engineer
```
Use when: Doing comprehensive code review

### Pattern 2: Parallel Analysis
```
        ┌→ security-auditor ─┐
Issue ──┼→ performance-auditor ├→ Report
        └→ architecture-auditor ┘
```
Use when: Investigating complex problems

### Pattern 3: Iterative Improvement
```
code-auditor → Fix Issues → code-auditor → test-engineer → release-manager
```
Use when: Ensuring high code quality

### Pattern 4: Strategic to Tactical
```
strategic-analyst → project-architect → integration-manager → development
```
Use when: Planning new features or projects

## 💡 Pro Tips

1. **Batch Operations**: When reviewing multiple modules, invoke all auditors at once
2. **Context Sharing**: Mention findings from one agent when invoking another
3. **Explicit Chaining**: Tell Claude to use specific agents in sequence
4. **Parallel Execution**: Request multiple agents for faster results

## 🎪 Advanced Scenarios

### Multi-Project Coordination
```bash
"Use strategic-analyst to plan the API versioning strategy across our 5 microservices, 
then have project-architect create a consistent structure for each service, 
and finally use integration-manager to create coordinated Linear tasks for all teams"
```

### Continuous Quality Monitoring
```bash
"Set up a workflow where code-auditor reviews every PR, 
test-engineer ensures test coverage doesn't drop, 
and release-manager maintains a rolling changelog"
```

### Architecture Evolution
```bash
"Have architecture-auditor analyze our system monthly, 
strategic-analyst model the impact of suggested changes, 
and project-architect implement approved improvements"
```

Remember: Agents work best when given clear, specific objectives. Combine their expertise to tackle complex challenges efficiently.