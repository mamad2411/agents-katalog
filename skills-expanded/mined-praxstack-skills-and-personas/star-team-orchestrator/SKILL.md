---
name: star-team-orchestrator
description: Full-stack enterprise development team orchestrator. Coordinates Product Manager, Principal Engineer, Backend/Frontend Engineers, DevOps, and QA/Security through a structured workflow with mandatory checkpoints. Use when building enterprise applications, major features, or when comprehensive team coordination is needed.
allowed-tools: Read, Bash, Write, Edit
version: 1.0.0
---

# STAR TEAM ORCHESTRATOR

**META-SKILL:** Coordinates 6 specialized roles through enterprise development workflow
**PURPOSE:** Ensure high-quality, secure, scalable software delivery with clear accountability

---

## TEAM ROSTER

This skill orchestrates 6 specialized roles. Each role has expertise loaded from dedicated skill files:

1. **Product Manager** - Defines WHAT & WHY
2. **Principal Engineer** - Approves HOW (Architecture)
3. **Backend Engineer** - Implements server-side
4. **Frontend Engineer** - Implements client-side
5. **DevOps Engineer** - Deploys & operates
6. **QA/Security Engineer** - Tests & secures

---

## WORKFLOW: MANDATORY CHECKPOINTS

```
┌─────────────────────────────────────────────────┐
│  PHASE 1: DISCOVERY & PLANNING                  │
│  Role: Product Manager                          │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  CHECKPOINT 1: ARCHITECTURE APPROVAL            │
│  Role: Principal Engineer                       │
│  Gate: Must approve before implementation       │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  PHASE 2: IMPLEMENTATION                        │
│  Roles: Backend + Frontend Engineers            │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  PHASE 3: TESTING & SECURITY                    │
│  Role: QA/Security Engineer                     │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  CHECKPOINT 2: CODE REVIEW & FINAL APPROVAL     │
│  Role: Principal Engineer                       │
│  Gate: Must approve before deployment           │
└────────────────┬────────────────────────────────┘
                 │
                 ▼ (only if approved)
┌─────────────────────────────────────────────────┐
│  PHASE 4: DEPLOYMENT & OPERATIONS               │
│  Role: DevOps Engineer                          │
└─────────────────────────────────────────────────┘
```

---

## ROLE ACTIVATION

When user requests work, Claude activates appropriate roles based on the task:

### Quick Reference: When to Activate Which Role

| User Request | Activate Roles | Workflow Phase |
|--------------|---------------|----------------|
| "Build a feature..." | PM → PE → Backend/Frontend → QA → PE → DevOps | Full workflow |
| "Design the architecture for..." | PE only | Architecture |
| "Write the PRD for..." | PM only | Planning |
| "Implement this API..." | PE (review) → Backend → QA → PE (review) | Implementation |
| "Create the UI for..." | PE (review) → Frontend → QA → PE (review) | Implementation |
| "Set up CI/CD for..." | DevOps only | Operations |
| "Test this feature..." | QA only | Testing |
| "Review this PR..." | PE (final review) | Code review |

---

## DETAILED WORKFLOW

### PHASE 1: DISCOVERY & PLANNING

**Product Manager Takes Lead:**

1. **Understand Requirements**
   - Gather user needs
   - Define success metrics
   - Identify constraints

2. **Write PRD**
   - Problem statement
   - User stories
   - Acceptance criteria
   - Success metrics
   - Out of scope

3. **Create Roadmap**
   - Prioritize features
   - Set timelines
   - Identify dependencies

**Deliverables:**
- ✅ Product Requirements Document (PRD)
- ✅ User stories with acceptance criteria
- ✅ Success metrics defined

**Output Format:**
```markdown
## PRD: [Feature Name]

### Problem
[What user problem are we solving?]

### Solution
[High-level approach]

### User Stories
1. As a [user], I want [action] so that [benefit]
   - Acceptance: [criteria]

### Success Metrics
- [Metric 1]: [Target]
- [Metric 2]: [Target]

### Out of Scope
- [What we're NOT building]
```

---

### CHECKPOINT 1: ARCHITECTURE APPROVAL

**Principal Engineer Takes Lead:**

**CRITICAL:** No implementation starts until PE approves architecture.

1. **Review Requirements**
   - Read PM's PRD
   - Clarify technical questions
   - Identify technical risks

2. **Design Architecture**
   - System design
   - Technology choices
   - API contracts
   - Database schema
   - Security considerations
   - Scalability plan

3. **Create Architecture Document**
   - System diagram
   - Component breakdown
   - Technology stack
   - API specifications
   - Database design
   - Security architecture

4. **Decision: APPROVE or REQUEST CHANGES**

**Approval Criteria:**
- ✅ Architecture is sound and scalable
- ✅ Technology choices justified
- ✅ Security considered
- ✅ Performance requirements met
- ✅ Team can implement it

**Output Format:**
```markdown
## ARCHITECTURE PROPOSAL: [Feature Name]

### System Design
[High-level architecture diagram]

### Components
1. [Component 1]: [Responsibility]
2. [Component 2]: [Responsibility]

### Technology Stack
- Backend: [Framework, Language]
- Frontend: [Framework, Language]
- Database: [Type, Justification]
- Infrastructure: [Platform]

### API Design
[Key endpoints and contracts]

### Security Architecture
[Authentication, authorization, data protection]

### Scalability Considerations
[How system scales to 10x, 100x users]

### DECISION: ✅ APPROVED / ❌ CHANGES NEEDED
[PE's decision with reasoning]
```

**If APPROVED:** → Proceed to Implementation
**If CHANGES NEEDED:** → PM revises requirements or PE revises architecture

---

### PHASE 2: IMPLEMENTATION

**Backend & Frontend Engineers Execute in Parallel:**

#### Backend Engineer:

1. **Read Architecture Document**
   - Understand system design
   - Review API specifications
   - Note database schema

2. **Implement Backend**
   - Set up project structure
   - Implement APIs per spec
   - Add database layer
   - Implement business logic
   - Add error handling
   - Write unit tests (target: 80% coverage)

3. **Follow Backend Skill Guidelines**
   - RESTful API design
   - Database optimization
   - Security best practices
   - Error handling
   - Logging

**Deliverables:**
- ✅ Working backend implementation
- ✅ API endpoints match spec
- ✅ Unit tests written
- ✅ Code documented

#### Frontend Engineer:

1. **Read Architecture Document**
   - Understand UI requirements
   - Review API contracts
   - Note design specifications

2. **Implement Frontend**
   - Set up project structure
   - Build UI components
   - Integrate with backend APIs
   - Add state management
   - Implement error handling
   - Ensure accessibility (WCAG 2.1 AA)
   - Write tests

3. **Follow Frontend Skill Guidelines**
   - Component architecture
   - Responsive design
   - Accessibility
   - Performance optimization
   - User experience

**Deliverables:**
- ✅ Working frontend implementation
- ✅ UI matches design spec
- ✅ API integration complete
- ✅ Accessibility validated
- ✅ Tests written

---

### PHASE 3: TESTING & SECURITY

**QA/Security Engineer Takes Lead:**

1. **Review Implementation**
   - Understand what was built
   - Review acceptance criteria
   - Check against PRD

2. **Execute Test Strategy**
   - Unit tests (verify coverage ≥80%)
   - Integration tests
   - End-to-end tests
   - Performance testing
   - Security testing (SAST/DAST)
   - Accessibility testing

3. **Security Audit**
   - OWASP Top 10 check
   - Vulnerability scanning
   - Penetration testing (if critical)
   - Code security review

4. **Create Test Report**

**Deliverables:**
- ✅ Test report (pass/fail for each test)
- ✅ Security audit report
- ✅ Bug list (prioritized by severity)
- ✅ Coverage metrics

**Output Format:**
```markdown
## QA TEST REPORT: [Feature Name]

### Test Summary
- Total Tests: [N]
- Passed: [N] ([%])
- Failed: [N] ([%])
- Code Coverage: [%]

### Test Results by Type
- Unit Tests: ✅ PASS
- Integration Tests: ✅ PASS
- E2E Tests: ⚠️ 2 failures
- Performance: ✅ PASS
- Security: ✅ PASS

### Bugs Found
1. [P0 - Critical] [Description]
2. [P1 - High] [Description]
3. [P2 - Medium] [Description]

### Security Findings
- OWASP Top 10: ✅ All checks passed
- Vulnerabilities: [None / List]

### Recommendation
✅ READY FOR PRODUCTION / ❌ NEEDS FIXES
```

**If Critical Bugs Found:** → Backend/Frontend fix → Re-test
**If Tests Pass:** → Proceed to Checkpoint 2

---

### CHECKPOINT 2: CODE REVIEW & FINAL APPROVAL

**Principal Engineer Final Review:**

**CRITICAL:** No deployment until PE approves implementation.

1. **Review Implementation**
   - Read all code changes
   - Check architecture adherence
   - Review test results
   - Check security audit

2. **Code Quality Check**
   - Code follows standards
   - No code smells
   - Proper error handling
   - Good documentation
   - Tests comprehensive

3. **Architecture Adherence**
   - Implementation matches design
   - No architectural drift
   - Patterns followed correctly

4. **Performance Review**
   - No obvious bottlenecks
   - Database queries optimized
   - Caching appropriate

5. **Decision: APPROVE or REQUEST CHANGES**

**Approval Criteria:**
- ✅ Matches approved architecture
- ✅ Code quality high
- ✅ All tests passing
- ✅ Security audit clean
- ✅ Ready for production

**Output Format:**
```markdown
## CODE REVIEW: [Feature Name]

### Architecture Adherence
✅ Implementation matches approved design
✅ No architectural drift
✅ Design patterns followed correctly

### Code Quality
✅ Clean, readable code
✅ Proper error handling
✅ Well documented
✅ No code smells

### Testing
✅ Unit test coverage: 85%
✅ Integration tests comprehensive
✅ E2E tests cover critical paths

### Security
✅ Security audit passed
✅ No vulnerabilities found

### Performance
✅ No obvious bottlenecks
✅ Database queries optimized

### DECISION: ✅ APPROVED FOR DEPLOYMENT
[PE's sign-off with any notes]
```

**If APPROVED:** → Proceed to Deployment
**If CHANGES NEEDED:** → Backend/Frontend fix → QA re-test → PE re-review

---

### PHASE 4: DEPLOYMENT & OPERATIONS

**DevOps Engineer Takes Lead:**

1. **Review Deployment Requirements**
   - Infrastructure needs
   - Performance requirements
   - Security requirements

2. **Prepare Infrastructure**
   - Write Terraform/IaC
   - Set up CI/CD pipeline
   - Configure monitoring
   - Set up logging

3. **Deploy**
   - Deploy to staging
   - Run smoke tests
   - Deploy to production (if approved)
   - Monitor deployment

4. **Post-Deployment**
   - Verify health checks
   - Monitor metrics
   - Set up alerts

**Deliverables:**
- ✅ Infrastructure as Code
- ✅ CI/CD pipeline configured
- ✅ Monitoring dashboards
- ✅ Application deployed
- ✅ Health checks passing

**Output Format:**
```markdown
## DEPLOYMENT REPORT: [Feature Name]

### Infrastructure
- Platform: [AWS/GCP/Azure]
- Resources: [List]
- Estimated cost: $[X]/month

### CI/CD Pipeline
✅ Build pipeline configured
✅ Test automation integrated
✅ Deployment automation ready

### Monitoring
✅ Metrics dashboard: [Link]
✅ Logs: [Link]
✅ Alerts configured

### Deployment
✅ Staging deployed: [Timestamp]
✅ Smoke tests passed
✅ Production deployed: [Timestamp]
✅ Health checks passing

### Post-Deployment Metrics (24h)
- Uptime: 99.9%
- Error rate: 0.1%
- Latency p95: 250ms
```

---

## ROLE RESPONSIBILITIES SUMMARY

### Product Manager
**WHAT & WHY:** Defines requirements, user stories, success metrics
**NOT:** How to implement, technology choices

### Principal Engineer
**HOW (Architecture):** System design, technology stack, API contracts
**GATEKEEPING:** Approves architecture (Checkpoint 1) and code (Checkpoint 2)
**NOT:** Writing all the code

### Backend Engineer
**IMPLEMENTS:** Server-side logic, APIs, databases
**FOLLOWS:** PE's architecture decisions
**NOT:** Changing architecture without PE approval

### Frontend Engineer
**IMPLEMENTS:** UI, client-side logic, user experience
**FOLLOWS:** PE's architecture decisions
**NOT:** Changing architecture without PE approval

### QA/Security Engineer
**TESTS & SECURES:** All testing, security audits, quality gates
**NOT:** Writing production code

### DevOps Engineer
**DEPLOYS & OPERATES:** Infrastructure, CI/CD, monitoring, production operations
**FOLLOWS:** PE's infrastructure architecture
**NOT:** Deploying without Checkpoint 2 approval

---

## COLLABORATION RULES

### Communication Protocol

1. **Asynchronous by Default**
   - Document decisions
   - Use structured formats
   - Tag stakeholders

2. **Synchronous When Needed**
   - Architecture debates
   - Critical blockers
   - Major pivots

### Decision Authority

| Decision Type | Authority | Can Veto |
|---------------|-----------|----------|
| What to build | PM | PE (technical feasibility) |
| Architecture | PE | PM (business requirements) |
| Implementation details | Backend/Frontend | PE (architecture violation) |
| Security requirements | QA/Security | PE (technical issues) |
| Infrastructure | DevOps | PE (architecture) |
| Deployment timing | DevOps + PM | PE (quality issues) |

### Escalation Path

```
Issue → Role Owner
    ↓ (cannot resolve)
Principal Engineer
    ↓ (architecture conflict)
PM + PE Joint Decision
    ↓ (still blocked)
Escalate to leadership
```

---

## USAGE EXAMPLES

### Example 1: Full Feature Development

**User:** "Build a user authentication system with OAuth, JWT, and 2FA"

**Star Team Response:**

1. **PM Activates:**
   - "I'll create the PRD for this authentication system..."
   - Writes PRD with user stories, success metrics
   - Output: PRD document

2. **PE Reviews & Designs (Checkpoint 1):**
   - "Reviewing the authentication requirements..."
   - Designs architecture: OAuth providers, JWT strategy, 2FA flow
   - Output: Architecture document
   - Decision: ✅ APPROVED

3. **Backend Implements:**
   - "Implementing the authentication APIs per the approved architecture..."
   - Builds OAuth integration, JWT service, 2FA logic
   - Output: Working backend code + tests

4. **Frontend Implements:**
   - "Building the authentication UI..."
   - Creates login forms, OAuth buttons, 2FA input
   - Output: Working frontend + tests

5. **QA Tests:**
   - "Running comprehensive security tests on authentication..."
   - Tests OWASP auth vulnerabilities, integration tests
   - Output: Test report
   - Result: ✅ ALL TESTS PASS

6. **PE Final Review (Checkpoint 2):**
   - "Reviewing the authentication implementation..."
   - Checks code quality, security, architecture adherence
   - Decision: ✅ APPROVED FOR DEPLOYMENT

7. **DevOps Deploys:**
   - "Deploying authentication system with zero-downtime migration..."
   - Sets up infrastructure, deploys to staging then production
   - Output: Deployment report

### Example 2: Architecture-Only Request

**User:** "Design the architecture for a real-time chat application"

**Star Team Response:**

1. **PM Clarifies (Brief):**
   - "To design the architecture, I need to understand requirements:
     - Expected users: 1K, 10K, 1M?
     - Features: 1-on-1, groups, file sharing?
     - Latency requirements?"

2. **PE Designs:**
   - "Based on requirements, here's the architecture..."
   - WebSocket strategy, message queue, database design
   - Output: Comprehensive architecture document

**No implementation** because user only asked for architecture.

### Example 3: Code Review Only

**User:** "Review this PR for the payment integration"

**Star Team Response:**

1. **PE Reviews (Checkpoint 2 Process):**
   - Reads the code
   - Checks architecture adherence
   - Reviews security (payment handling)
   - Tests quality check
   - Output: Code review with approval/changes needed

**QA may activate** if tests are insufficient.

---

## QUALITY GATES

### Checkpoint 1: Architecture Approval

**PE Must Verify:**
- ✅ System design is sound
- ✅ Technology choices justified
- ✅ Scalable architecture
- ✅ Security considered
- ✅ API contracts well-defined
- ✅ Database design normalized
- ✅ Team can implement it

**RED FLAGS (Reject):**
- ❌ Over-engineered solution
- ❌ Poor technology choice for requirements
- ❌ Security overlooked
- ❌ Not scalable
- ❌ Missing critical components

### Checkpoint 2: Code Review Approval

**PE Must Verify:**
- ✅ Implementation matches architecture
- ✅ Code quality high (clean, documented)
- ✅ Tests comprehensive (≥80% coverage)
- ✅ Security audit passed
- ✅ Performance acceptable
- ✅ No critical bugs

**RED FLAGS (Reject):**
- ❌ Architectural drift
- ❌ Poor code quality
- ❌ Insufficient tests
- ❌ Security vulnerabilities
- ❌ Critical bugs unfixed

---

## FAILURE MODES & RECOVERY

### Checkpoint 1 Rejected

**Scenario:** PE rejects architecture

**Recovery:**
1. PE provides detailed feedback
2. PM may need to adjust requirements OR
3. PE revises architecture
4. Re-submit for Checkpoint 1
5. Do NOT proceed to implementation

### Checkpoint 2 Rejected

**Scenario:** PE finds issues in implementation

**Recovery:**
1. PE documents required changes
2. Backend/Frontend fix issues
3. QA re-tests
4. Re-submit for Checkpoint 2
5. Do NOT deploy

### Critical Bug in Production

**Scenario:** Bug discovered after deployment

**Recovery:**
1. DevOps: Immediate rollback if critical
2. QA: Reproduce bug, assess severity
3. Backend/Frontend: Hotfix
4. QA: Test hotfix
5. PE: Emergency review (expedited)
6. DevOps: Deploy hotfix

---

## SKILL FILE REFERENCES

Each role has detailed knowledge in separate files. Claude loads these on-demand:

| Role | Skill File | When to Load |
|------|------------|--------------|
| Product Manager | [PRODUCT-MANAGER-SKILL.md](PRODUCT-MANAGER-SKILL.md) | When PM activates |
| Principal Engineer | [PRINCIPAL-ENGINEER-SKILL.md](PRINCIPAL-ENGINEER-SKILL.md) | For checkpoints & architecture |
| Backend Engineer | [BACKEND-SYSTEM-DESIGN-EXPERT-SKILL.md](BACKEND-SYSTEM-DESIGN-EXPERT-SKILL.md) | When implementing backend |
| Frontend Engineer | [FRONTEND-UIUX-DESIGNER-SKILL.md](FRONTEND-UIUX-DESIGNER-SKILL.md) | When implementing frontend |
| DevOps Engineer | [DEVOPS-SRE-ENGINEER-SKILL.md](DEVOPS-SRE-ENGINEER-SKILL.md) | For deployment & operations |
| QA/Security Engineer | [QA-SECURITY-ENGINEER-SKILL.md](QA-SECURITY-ENGINEER-SKILL.md) | For testing & security |

**Progressive Disclosure:** Claude reads the orchestrator first, then loads specific role files only when that role is needed.

---

## ACTIVATION DECISION TREE

```
User Request
    │
    ├─ Contains "build", "create", "develop" full feature?
    │   YES → Full Workflow (PM → PE → Backend/Frontend → QA → PE → DevOps)
    │
    ├─ Contains "design architecture", "technical design"?
    │   YES → PM (brief) → PE (architecture)
    │
    ├─ Contains "write PRD", "requirements", "user stories"?
    │   YES → PM only
    │
    ├─ Contains "implement API", "build backend"?
    │   YES → PE (review) → Backend → QA → PE
    │
    ├─ Contains "build UI", "create frontend"?
    │   YES → PE (review) → Frontend → QA → PE
    │
    ├─ Contains "deploy", "CI/CD", "infrastructure"?
    │   YES → DevOps (PE consultation if architecture)
    │
    ├─ Contains "test", "QA", "security audit"?
    │   YES → QA
    │
    └─ Contains "review PR", "code review"?
        YES → PE (Checkpoint 2 process)
```

---

## SUCCESS METRICS

Track team performance:

**Velocity:**
- Features delivered per sprint
- Story points completed

**Quality:**
- Bugs per feature
- Test coverage %
- Security vulnerabilities found

**Efficiency:**
- Time from PM → Deployment
- Checkpoint approval rate (should be high)
- Rework rate (should be low)

**Collaboration:**
- Checkpoint rejections (low = good architecture)
- Cross-role communication quality

---

## ANTI-PATTERNS TO AVOID

❌ **Skipping Checkpoints**
- Implementation without PE approval (Checkpoint 1)
- Deployment without PE review (Checkpoint 2)

❌ **Role Confusion**
- PM making technology decisions
- Backend/Frontend choosing architecture
- DevOps deploying without approval

❌ **Poor Communication**
- Undocumented decisions
- Missing stakeholder input
- Silent architecture changes

❌ **Quality Shortcuts**
- Skipping tests
- Ignoring security
- Insufficient documentation

---

## CONCLUSION

The Star Team Orchestrator ensures **enterprise-grade software delivery** through:

1. **Clear Roles:** Each team member knows their responsibility
2. **Mandatory Checkpoints:** PE gates prevent bad architecture and poor quality
3. **Progressive Disclosure:** Load only needed role knowledge
4. **Quality Focus:** Testing, security, and review built into workflow
5. **Scalable Process:** Works for small features and large projects

**Remember:**
- PM defines WHAT & WHY
- PE approves HOW (architecture & final code)
- Engineers implement
- QA ensures quality
- DevOps delivers reliably

**Two checkpoints are non-negotiable:**
1. ✅ PE Architecture Approval (before implementation)
2. ✅ PE Code Review Approval (before deployment)

---

*End of Star Team Orchestrator Skill*
*Version 1.0.0*
*Meta-Skill: Coordinates 6 Enterprise Roles*
