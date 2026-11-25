---
name: open-testing-plan
description:       Generate comprehensive test plans, schedules, resource allocation, environment setup, and test data strategies.
  Use this when you need to develop master test plans, level-specific test plans, allocate resources and environments,
  plan non-functional testing, define end-to-end testing chains, or establish test data management strategies.
---

<!-- Tip: Use /open-testing-plan in chat to generate content with agent assistance -->

# Open Testing Plan

The **open-testing-plan** skill generates test plans, schedules, resource allocation, environment setup, and test data strategies using a 7-agent PLANNED pipeline that transforms test strategies into executable test plans.

## PLANNED Agent Pipeline

The PLANNED mnemonic orchestrates seven specialized agents:

1. **P_plan** - Plan Agent
2. **L_levels** - Levels Agent
3. **A_allocation** - Allocation Agent
4. **N_nonfunctional** - Non-Functional Agent
5. **N_network** - Network/E2E Agent
6. **E_environment** - Environment Agent
7. **D_data** - Data Agent

## Agent Specifications

### P_plan: Plan Agent

**Purpose**: Generate master test plans and level-specific test plans following ISO 29119-3 and TMap templates.

**Inputs**:
- Test strategy from `open-testing-design` skill
- Scope and test objects
- Timeline and release gates
- Stakeholder requirements

**Outputs**:
- Master Test Plan (MTP)
- Level Test Plans (LTP) for each level
- Test Plan Change Request procedure
- Test Plan Approval Sign-Off document

**Knowledge Base Files**:
- `standards/iso-29119.json` - ISO/IEC 29119-3 Master Test Plan structure
- `standards/tmap.json` - TMap test planning templates
- `template-analysis.json` - 108 plan templates with field definitions
- `terminology.json` - standardized terminology

**Master Test Plan (MTP) Structure**:

1. **Scope and Objectives**
   - Testing objectives aligned with business goals
   - Scope: what is/isn't tested
   - Success criteria

2. **Test Approach**
   - Test strategy reference (from design skill)
   - Technique selections and intensities
   - Risk-based allocation approach

3. **Test Schedule and Milestones**
   - Planning, preparation, execution, closing phases
   - Key milestones and gates
   - Dependencies and critical path

4. **Resources and Roles**
   - Test team structure
   - Skills and competencies required
   - Tool and environment requirements

5. **Entry and Exit Criteria**
   - Phase-level entry criteria (e.g., "Requirements approved")
   - Phase-level exit criteria (e.g., "Test cases reviewed and approved")

6. **Risk Management**
   - Testing risks (schedule, resource, technical)
   - Mitigation strategies
   - Contingency plans

7. **Deliverables and Reporting**
   - Test artifacts (cases, data, scripts)
   - Status and metrics reporting cadence
   - Escalation procedures

---

### L_levels: Levels Agent

**Purpose**: Define test levels with entry/exit criteria, scope, and techniques for each level.

**Inputs**:
- Master Test Plan
- Quality characteristics and risk classes
- Organizational testing standards
- Component architecture

**Outputs**:
- Level Test Plans (LTP) for:
  - Unit Testing
  - Component Testing
  - Integration Testing
  - System Testing
  - System Integration Testing (SIT)
  - User Acceptance Testing (UAT)
- Level-to-Technique Mapping
- Level-Specific Entry/Exit Criteria Document

**Knowledge Base Files**:
- `standards/iso-29119.json` - level definitions per ISO 29119
- `standards/tmap.json` - TMap level frameworks
- `technique-patterns.json` - technique applicability by level
- `template-analysis.json` - level test plan templates

**Level Definitions and Scope**:

| Level | Focus | Techniques | Entry Criteria | Exit Criteria |
|---|---|---|---|---|
| Unit | Individual units/modules | Code inspection, unit test frameworks, TDD | Code ready, test framework configured | 100% statement coverage, all tests pass |
| Component | Component functionality | Component testing, API testing, mocking | Component code complete, test env ready | Functional coverage 90%+, defects fixed |
| Integration | Component interactions | Integration testing, API contract testing | Components tested individually, integration env ready | All interfaces verified, integration smoke tests pass |
| System | Full system functionality | End-to-end testing, scenario testing, business process | Integration complete, system env ready | All requirements tested, performance benchmarks met |
| SIT | System + external integrations | Integration testing, data mapping | System tested, external systems available | External interfaces verified, data integrity confirmed |
| UAT | Business requirements validation | User scenario testing, exploratory, acceptance testing | System SIT complete, UAT env ready | Business acceptance sign-off, all priority requirements met |

**Technique Selection by Level**:
- **Unit**: TDD, code inspection, branch coverage analysis
- **Component**: Black-box testing (BVA, equivalence partitioning), API contract testing
- **Integration**: Integration scenarios, state transition testing, data flow testing
- **System**: End-to-end scenarios, user journey testing, performance/security testing
- **SIT**: System integration with external APIs, data migration testing
- **UAT**: Business scenario testing, usability testing, exploratory testing

---

### A_allocation: Allocation Agent

**Purpose**: Allocate resources, roles, environments, tools, and budget across test activities.

**Inputs**:
- Test effort estimate from design skill
- Resource availability
- Tool portfolio (licensed, open-source)
- Budget constraints
- Team structure and competencies

**Outputs**:
- Resource Allocation Matrix
- Role Definitions and RACI
- Tool and Environment Allocation
- Budget Breakdown by Phase
- Skills Gap Analysis
- Staffing Timeline

**Knowledge Base Files**:
- `standards/iso-29119.json` - resource frameworks
- `standards/tmap.json` - role definitions
- `terminology.json` - role standardization

**Resource Allocation Matrix Format**:
| Role | Responsibility | % Allocation | Timeline | Skills Required | Reporting To |
|---|---|---|---|---|---|
| QA Lead | Test planning, execution oversight | 80% | Full project | 10 yrs QA exp, risk analysis | Test Manager |
| Test Automation Engineer | Automation infrastructure, scripts | 100% | Full project | Python, Selenium, CI/CD | QA Lead |
| Manual Tester | Test execution, exploratory | 100% | Execution phase | Test design, domain knowledge | QA Lead |

**Tool Allocation by Activity**:
- Test Management: [tool selection]
- Test Automation: [framework selection]
- Performance Testing: [load testing tool]
- Security Testing: [SAST/DAST tools]
- Reporting: [dashboarding tool]

---

### N_nonfunctional: Non-Functional Agent

**Purpose**: Plan non-functional testing (NFT) across performance, security, usability, accessibility, scalability.

**Inputs**:
- Non-functional requirements from strategy
- Business-critical quality attributes
- Performance benchmarks and SLAs
- Security and compliance requirements

**Outputs**:
- Non-Functional Test Matrix (NFR × Test Type)
- Performance Test Plan (load, stress, endurance)
- Security Test Plan (SAST, DAST, penetration, compliance scanning)
- Usability Test Plan
- Accessibility Test Plan
- Scalability Test Plan

**Knowledge Base Files**:
- `standards/iso-29119.json` - NFT frameworks
- `standards/tmap.json` - non-functional testing patterns
- `technique-patterns.json` - NFT technique definitions

**Non-Functional Test Matrix Format**:
| Quality Attribute | NFR | Test Type | Technique | Success Criteria | Owner |
|---|---|---|---|---|---|
| Performance | Response time < 2 sec | Load testing | JMeter scenarios | P99 < 2 sec at 1000 users | Perf Engineer |
| Security | PCI DSS compliance | Penetration testing | OWASP Top 10 | Zero critical vulnerabilities | Security Lead |
| Usability | Task completion > 80% | Usability testing | User study (5 users) | 80%+ task completion | UX Researcher |
| Accessibility | WCAG 2.1 AA | Accessibility testing | Axe/lighthouse | Zero violations | QA Lead |

**Performance Test Scenarios**:
- **Baseline**: Establish current performance metrics
- **Load Test**: Normal production load + headroom
- **Stress Test**: Beyond expected load until failure point
- **Endurance Test**: Sustained load over extended period
- **Spike Test**: Sudden traffic spikes

**Security Test Coverage**:
- OWASP Top 10: Injection, broken auth, XSS, CSRF, etc.
- PCI DSS requirements (if payment processing)
- API security (authentication, authorization, data encryption)
- Dependency vulnerability scanning
- Code security scanning (SAST)

---

### N_network: Network/E2E Agent

**Purpose**: Plan end-to-end and chain testing across system components and external integrations.

**Inputs**:
- System architecture and data flow
- External system integrations
- User journeys and business processes
- System dependencies

**Outputs**:
- End-to-End (E2E) Test Scenarios
- E2E Chain Cards (swimlane diagrams)
- Integration Test Matrix (system × system)
- Data Flow Test Mapping
- Dependency and Critical Path Analysis

**Knowledge Base Files**:
- `standards/iso-29119.json` - integration testing frameworks
- `standards/tmap.json` - chain testing patterns
- `template-analysis.json` - E2E scenario templates

**E2E Chain Card Format**:

**Chain**: Customer Registration and First Purchase
```
Actor: New Customer
Steps:
1. Web Portal: Submit registration form
   → Data validation: Email format, unique check
   → Output: User record created in CRM
2. CRM System: Send welcome email via Email Service
   → Integration: Email Service API call
   → Output: Email sent, delivery confirmed
3. Web Portal: Redirect to product catalog
   → Integration: Product API call
   → Output: Catalog loaded with personalized recommendations
4. Web Portal: Checkout process
   → Integration: Payment Gateway API
   → CRM: Update customer purchase history
   → Inventory: Decrement stock
   → Fulfillment: Create order
   → Output: Order confirmation email
5. Email Service: Shipment notification
   → Integration: Tracking system API
   → Output: Tracking link sent to customer

Critical Data Points:
- Customer ID consistency across systems
- Email delivery confirmation
- Payment transaction integrity
- Inventory accuracy
```

**Integration Test Matrix**:
| System 1 | System 2 | Interface Type | Test Type | Success Criteria |
|---|---|---|---|---|
| Web Portal | CRM | REST API | Contract testing | API response schema matches |
| CRM | Email Service | SMTP | Data integrity | Email delivered within 5 min |
| Web Portal | Payment Gateway | HTTPS | Security | TLS 1.2+, no man-in-middle |
| Fulfillment | Inventory | Database | Data consistency | Stock counts match bidirectionally |

---

### E_environment: Environment Agent

**Purpose**: Generate environment specifications and infrastructure requirements for all test levels.

**Inputs**:
- Test levels and scope
- Performance requirements
- Integration dependencies
- Tool requirements
- Data volume and complexity

**Outputs**:
- Environment Specification Document
- Infrastructure Requirements (compute, storage, network)
- Environment Provisioning Checklist
- Data Seeding and Refresh Procedures
- Environment Maintenance Plan

**Knowledge Base Files**:
- `standards/iso-29119.json` - environment frameworks
- `template-analysis.json` - environment specification templates

**Environment Specification Structure**:

**1. Environment Topology**
```
Dev Environment:
  - 2x Web servers (load balanced)
  - 1x API server
  - 1x PostgreSQL (single instance)
  - 1x Redis cache
  - Mock external services: Payment Gateway, Email Service

QA/Test Environment:
  - 4x Web servers (load balanced)
  - 2x API servers
  - 1x PostgreSQL (with replication)
  - 2x Redis cache (replicated)
  - Real external service connections (sandbox)

Performance Test Environment:
  - 8x Web servers
  - 4x API servers
  - 1x PostgreSQL optimized (dedicated storage)
  - Load balancer with auto-scaling
  - Monitoring: Prometheus, Grafana

UAT Environment:
  - Production-like configuration
  - All external services in production sandbox
  - Data masking applied
```

**2. Resource Requirements**:
- CPU/Memory/Storage specifications
- Network bandwidth and latency constraints
- Database size and backup requirements
- Third-party service sandboxes/accounts

**3. Configuration Management**:
- Environment variables and secrets management
- Version control for environment definitions
- Infrastructure-as-Code (Terraform, CloudFormation) templates
- Environment consistency verification

**4. Data Seeding**:
- Base dataset size and refresh frequency
- Synthetic data generation rules
- Realistic data distribution
- Compliance-aware masking (PII, PCI)

---

### D_data: Data Agent

**Purpose**: Plan test data strategy, data masking, synthetic data generation, and data lifecycle management.

**Inputs**:
- Data types and volume from scope
- Privacy and compliance requirements
- Performance testing data needs
- Test level data requirements

**Outputs**:
- Test Data Master Sheet
- Data Masking Policy
- Synthetic Data Generation Rules
- Data Refresh and Cleanup Procedures
- Data Traceability and Audit Log

**Knowledge Base Files**:
- `standards/iso-29119.json` - test data frameworks
- `template-analysis.json` - data management templates
- `terminology.json` - data classification terms

**Test Data Master Sheet Format**:
| Data Type | Volume | Source | Generation Method | Masking Rules | Refresh Frequency | Owner |
|---|---|---|---|---|---|---|
| Customer Records | 100K | Production (masked) | Subset + synthetic | Hash PII, mask email | Weekly | Data Eng |
| Transactions | 1M | Production (anonymized) | Subset + replay | Remove cardholder name | Weekly | Finance |
| Product Catalog | 10K | Source system | Direct sync | No masking | Daily | Catalog Mgmt |
| Test-Only Records | N/A | Synthetic | Faker library (Python) | N/A | On-demand | QA Lead |

**Data Masking Policy**:

**PII Classification**:
- **Level 1 (High Risk)**: Payment card numbers, SSN, bank accounts
  - Masking: Hash (SHA-256), never store plaintext
- **Level 2 (Medium Risk)**: Names, emails, phone numbers
  - Masking: Partial mask (first 2 chars), character substitution
- **Level 3 (Low Risk)**: Job title, company, location
  - Masking: No masking required

**Data Generation Rules**:
```
Customer Names: faker.name()
Email Addresses: faker.email() with domain mapping
Phone Numbers: Valid format (555-XXX-XXXX for test)
Credit Cards: Valid Luhn checksum, non-functional (4532 test range)
Addresses: Realistic distributions by geography
Dates: Relative to current date, realistic ranges
Product IDs: Existing IDs from product system
```

**Data Refresh Cycle**:
- **Development**: Refresh on-demand (manual)
- **QA/Test**: Refresh weekly (automated)
- **Performance**: Refresh before performance test run
- **UAT**: Refresh before each UAT cycle
- **Production**: Never use production data in lower environments

**Compliance & Audit**:
- Data access logging (who accessed what when)
- Audit trail for data modifications
- Retention policy (delete after X days)
- GDPR/CCPA compliance (right to deletion)

---

## Output Templates

### 1. Master Test Plan (MTP)
- Project identification
- Test objectives aligned to business goals
- Scope statement (in/out of scope)
- Test approach and strategy reference
- Schedule and milestones
- Resource plan with roles
- Risk and contingency plan
- Entry and exit criteria (organizational)
- Deliverables list
- Metrics and reporting

### 2. Level Test Plans (LTP)
One LTP per level (Unit, Component, Integration, System, SIT, UAT):
- Level scope and objectives
- Techniques and coverage targets
- Entry criteria (level-specific)
- Exit criteria (level-specific)
- Test case inventory
- Schedule and resource allocation
- Environment requirements
- Risk mitigation for level

### 3. Non-Functional Test Matrix
Spreadsheet with quality attributes, NFR mappings, test types, success criteria, and resource allocation.

### 4. E2E Chain Cards
Swimlane diagrams (text or visio) showing:
- Actors and systems involved
- Step-by-step data flow
- Integration points
- Critical data validation points

### 5. Environment Specification
Technical document with topology, resource specs, configuration, and data seeding procedures.

### 6. Test Data Master Sheet
Spreadsheet with data types, volumes, generation methods, masking rules, refresh schedules, and ownership.

---

## Knowledge Base Files Reference

All KB files located at `/sessions/trusting-pensive-ptolemy/mnt/Open-Testing/knowledge-base/`:

- **terminology.json** (1105 terms): Standardized testing terminology
- **technique-patterns.json** (106 patterns): Technique applicability by level and context
- **template-analysis.json** (108 templates): MTP, LTP, NFT, E2E, environment, and data templates
- **standards/iso-29119.json**: ISO/IEC 29119 testing standard structures and definitions
- **standards/ieee-standards.json**: IEEE standard references (830 for requirements, 1012 for testing)
- **standards/tmap.json**: TMap methodologies, best practices, and frameworks
- **ontology.json**: Testing domain classification and relationships

---

## Invocation Examples

### Example 1: Generate Complete Test Plan from Strategy

**User Input**:
```
Create a test plan for our payment module project:
- From the test strategy generated previously
- 3-week timeline
- 8 developers, 3 QA testers
- Need performance testing (< 2 sec response time)
- PCI DSS compliance required
- Production-like QA environment
```

**Agent Pipeline**:
1. **P_plan** creates MTP with 3-week schedule, alignment to strategy objectives
2. **L_levels** defines 6 level test plans (unit through UAT) with entry/exit criteria
3. **A_allocation** distributes 8 developers and 3 QA across levels, allocates tools (Selenium, JMeter)
4. **N_nonfunctional** plans performance testing (load scenarios), security testing (OWASP scanning)
5. **N_network** defines E2E chains: registration, payment processing, refund scenarios
6. **E_environment** specifies 3 environments (dev, QA, perf test) with load balancer setup
7. **D_data** creates test data strategy with 100K masked customer records, synthetic transaction data

**Output**:
- Master Test Plan (20 pages)
- 6 Level Test Plans
- Performance Test Plan with JMeter scenarios
- Security Test Plan with OWASP Top 10 coverage
- E2E Chain Cards (8 critical paths)
- Environment Specification (infrastructure-as-code templates)
- Test Data Master Sheet (data generation rules, masking policy)

### Example 2: Plan Non-Functional Testing for Performance-Critical System

**User Input**:
```
Our API must handle 10K requests/second during peak load.
E-commerce platform with payment processing.
SLA: 99.99% uptime, p99 response time < 500ms.
Generate the non-functional test plan.
```

**Agent Pipeline**:
1. **N_nonfunctional** creates NFT matrix with performance, security, and scalability testing
2. **N_network** identifies integration bottlenecks (payment gateway, inventory, analytics)
3. **E_environment** specifies perf test environment with auto-scaling infrastructure
4. **A_allocation** allocates performance engineer and infrastructure resources
5. **D_data** plans synthetic transaction dataset (1M records) for realistic load simulation

**Output**:
- Performance Test Plan with load/stress/endurance/spike scenarios
- Load test data (1M+ synthetic transactions)
- Infrastructure scaling policy
- SLA monitoring and alerting setup

---

## Integration with Other Skills

**Inputs from `open-testing-design`**:
- Test Strategy Table (techniques, intensities, risk classes)
- Quality Engineering Strategy Table (preventive/static/dynamic measures)
- Exit criteria and coverage targets

**Integration Points**:
- Test levels use techniques selected in design skill
- Risk classes determine level intensity and resource allocation
- Exit criteria from design become acceptance gates in plan

**Output for Other Skills**:
- Test plans feed into `opentestai` skill for test case generation
- Environment specs inform CI/CD pipeline setup
- E2E chain cards inform test automation script structure

**For Document Generation**: Use `docx` skill to create formatted MTP and LTP documents
**For Spreadsheet Output**: Use `xlsx` skill to create resource matrices, NFT matrix, and test data master sheet

---

## Algorithm Summary

### Level Planning Algorithm
```
FOR EACH test_level (unit, component, integration, system, sit, uat):
  1. Look up level definition in standards/iso-29119.json
  2. Identify techniques applicable to level (from technique-patterns.json)
  3. Determine risk-based intensity (from strategy):
     - Class A risks: thorough coverage at this level
     - Class B risks: standard coverage at this level
     - Class C risks: light coverage or coverage only
  4. Set entry criteria: prerequisites from previous level + env readiness
  5. Set exit criteria: technique coverage + defect/quality metrics
  6. Calculate effort for level using technique factors
  7. Allocate resources proportional to effort
  8. Create LTP with templates from template-analysis.json
```

### Environment Specification Algorithm
```
FOR EACH test_level:
  1. Identify external system integrations needed
  2. Determine data volume requirements (from scope)
  3. Select environment tier (minimal/standard/full):
     - Unit/Component: lightweight, local or containerized
     - Integration/System: full topology with mocks or sandboxes
     - SIT: production-like, real external systems (sandbox)
     - UAT: production-equivalent with masked data
  4. Allocate infrastructure resources (compute, storage, network)
  5. Define environment provisioning (IaC templates, Docker, Kubernetes)
  6. Create data seeding procedures
  7. Set refresh frequency based on test execution rate
  8. Document maintenance and troubleshooting procedures
```

### Test Data Generation Algorithm
```
FOR EACH data_type:
  1. Classify by privacy/sensitivity level (PII/confidential/public)
  2. Determine required volume and distribution
  3. Select generation method:
     - Production subset (masked)
     - Synthetic generation (Faker, data factories)
     - Combination (seed + synthetic variants)
  4. Apply masking rules per classification level
  5. Validate generated data (Luhn checksum, format rules)
  6. Create refresh procedures (weekly, per-execution, on-demand)
  7. Document audit trail and compliance adherence
  8. Test data traceability (which dataset used in which test run)
```

---

## Quality Assurance

The PLANNED pipeline ensures:
- Test plans align with test strategies from design skill
- All test levels have clear entry/exit criteria
- Resources are appropriately allocated to risk-based priorities
- Environments support all test level requirements
- Test data is realistic, compliant, and managed
- Non-functional testing covers SLA/performance/security requirements
- E2E testing validates complete business processes

**Plan Quality Validation**:
- All levels reference applicable techniques from strategy
- Entry criteria are measurable and achievable
- Exit criteria are specific and objectively verifiable
- Resource allocation totals match availability
- Environment specifications include all external system integrations
- Data masking policy covers all PII classifications
- Non-functional test matrix covers business-critical quality attributes
