---
name: open-testing-templates
description:       Generate 108 context-specific test templates: decision tables, state transition matrices, test case logs, test plans, exploratory charters, ARCI matrices, traceability sheets, and quality hunting documents. Use this skill whenever the user needs: test design worksheets, test execution logs, test strategy tables, quality engineering templates, defect tracking forms, estimation worksheets, checklists, or any test artifact. Triggers include: 'template', 'worksheet', 'form', 'test document', 'test plan', 'test case log', 'decision table', 'charter', 'matrix', 'checklist', 'strategy table', 'ARCI', or requests to 'generate a [template type]'.
---

<!-- Tip: Use /open-testing-templates in chat to generate content with agent assistance -->


# open-testing-templates — Test Template Generator (TEMPLATE Agents)

## What This Skill Does

This skill generates any of **108 output templates** organized into 10 categories, populated with context-specific data. It uses 8 specialized agents (TEMPLATE mnemonic) to route user requests to the right template agent, extract requirements, populate the template with real data, and export in the correct format (XLSX, DOCX, or HTML).

## 108 Templates Organized by Category

### 1. Technique Templates (5 templates)
Agent: **T_technique** — Generate test design technique worksheets

- **Decision Table** — Decision table testing with binary condition-outcome matrices
- **State Transition** — State transition testing with state tables and transition paths
- **MCDC** — Modified Condition/Decision Coverage truth tables with boolean independence
- **Path Testing** — Path testing with decision point graphs and test depth levels
- **Classification Tree** — Classification Tree Method with hierarchical data combinations

**Output format:** XLSX with multiple sheets (template + examples)

### 2. Execution Templates (11 templates)
Agent: **E_execution** — Generate test case logs, test scripts, and test scenarios

- **Test Case Log** — Multi-run test case and execution log with pass/fail tracking
- **Test Log Sheet** — Single-run test log with inputs, expected results, anomaly links
- **Test Script** — Detailed test script with 371+ rows of step-by-step actions
- **Test Scenario** — Test scenario definition with requisites, preconditions, system config
- **Test Script Document** — Word document format test script with preparation and controls
- **Traceability Matrix** — BRD → FRS → TRS → Test Case traceability
- **Coverage Matrix** — Test-to-requirement coverage mapping
- **Non-Functional Matrix** — Non-functional characteristics mapped to test phases
- **Requirements Validation** — Requirements validation criteria and review results
- **Gherkin Acceptance** — BDD-format acceptance criteria with Given/When/Then
- **Specification by Example** — Workshop cards for specification by example mapping

**Output format:** XLSX (9 templates) or DOCX (2 templates)

### 3. Exploratory Testing Templates (7 templates)
Agent: **E_exploratory** — Generate exploratory testing charters, session logs, debriefing

- **Charter (Full)** — Comprehensive exploratory testing charter with charter, log, debriefing
- **Charter (Simple)** — Simplified Word document charter with test log and defects
- **Charter (PDF)** — PDF format charter with testers, timebox, mission, tactics, test ideas
- **Quality Hunting Debriefing** — Quality hunting findings and insights sheet
- **Session Log** — Multi-run session tracking with test ideas and observations
- **Risk-Based Charter** — Risk-focused exploratory charter with risk-to-test mapping
- **Capacity Planning** — Exploratory testing timebox and capacity planning

**Output format:** XLSX (4 templates), DOCX (2 templates), PDF (1 template)

### 4. Defect Management Templates (4 templates)
Agent: **M_management** — Generate anomaly administration, defect tracking, JIRA logs

- **Anomaly Administration** — Defect tracking with 14 columns (ID, status, severity, priority, progress)
- **Defect Process Document** — Defect management process workflow definition
- **JIRA Issue Log** — JIRA-aligned issue tracking spreadsheet
- **JIRA Process Document** — JIRA management workflow and escalation process

**Output format:** XLSX (2 templates) or DOCX (2 templates)

### 5. Checklist Templates (18 templates)
Agent: **T_technique** (routing) + **Landscape** (content) — Generate quality and risk checklists

- **Test Design Techniques Checklist** — Technique selection guidance for 11 techniques
- **Quality Characteristics Checklist** — Assessment checklists for quality attributes
- **Risk Factors Checklist** — Risk factor identification per quality characteristic
- **Test Environment Checklist** — Environment readiness assessment
- **Generic Checklist** — 7-sheet customizable checklist (functional, non-functional, code review)
- **Compliance Checklist** — Regulatory and compliance requirement verification
- **Security Checklist** — Security testing checklist (OWASP, injection, XSS, etc.)
- **Performance Checklist** — Performance characteristic assessment
- **Usability Checklist** — UI/UX and usability testing checklist
- **Accessibility Checklist** — WCAG and accessibility compliance checklist
- **Mobile Testing Checklist** — Mobile-specific device, OS, and interaction testing
- **API Testing Checklist** — REST/GraphQL API and integration testing
- **Database Checklist** — Database integrity and data testing
- **Automation Checklist** — Test automation framework and tool readiness
- **Test Data Checklist** — Test data preparation and masking checklist
- **Regression Testing Checklist** — Regression scope and baseline validation
- **UAT Readiness Checklist** — User acceptance testing readiness criteria
- **Go-Live Checklist** — Production readiness and deployment checklist

**Output format:** DOCX (12 checklists) or XLSX (6 checklists)

### 6. Strategy & Planning Templates (12 templates)
Agent: **P_planning** + **L_landscape** — Generate test plans, strategy tables, estimation

- **Test Strategy Table** — TMap test strategy with quality characteristics, risk class, intensity
- **Quality Engineering Strategy** — Preventive/detective/corrective measures per quality attribute
- **Test Intensity Table** — Maps 4 coverage groups to technique intensity (low/medium/high)
- **Quality and Test Policy** — Organizational quality and test policies (10 sections)
- **Master Test Plan** — IEEE 29119-3 aligned master test plan (Word document)
- **System & Acceptance Test Plan** — SIT/UAT test plan template
- **Agile Test Plan** — Kanban-format test plan with delivery items and task tracking
- **WSJF Prioritization** — Weighted Shortest Job First scoring (business value, time criticality, risk, size)
- **Estimation Worksheet** — Test estimation using story points, ideal hours, or T-shirt sizes
- **Risk Assessment Matrix** — Risk probability × impact mapping
- **Release Planning** — Release readiness and go-no-go decision template
- **Test Metrics Dashboard** — KPI tracking (pass rate, coverage, defect density, velocity)

**Output format:** XLSX (10 templates) or DOCX (2 templates)

### 7. Accountability & Governance Templates (4 templates)
Agent: **A_accountability** — Generate ARCI matrices, QAM/QPM mappings, policies

- **ARCI Matrix** — Accountability assignment (Accountable/Responsible/Consulted/Informed)
- **QAM (Quality to Activity Mapping)** — Quality measures mapped to DevOps pipeline stages
- **QPM (Quality to People Mapping)** — Quality measures mapped to roles (PO, Test, Dev, Ops)
- **Quality Governance Matrix** — Governance roles, responsibilities, escalation paths

**Output format:** XLSX

### 8. Traceability & Coverage Templates (6 templates)
Agent: **T_traceability** — Generate traceability matrices, coverage matrices, requirements validation

- **Requirements Traceability Matrix (RTM)** — Multi-level traceability (BRD → FRS → Test)
- **Test Coverage Map** — Test case-to-requirement coverage
- **Risk-to-Test Traceability** — Risk items linked to test cases and test conditions
- **Coverage Heatmap** — Visual coverage by requirement type and test phase
- **Compliance Traceability** — Standard/regulation items linked to test cases
- **Bidirectional Traceability** — Forward and reverse traceability with gap analysis

**Output format:** XLSX (5 templates) or HTML (1 template)

### 9. Reporting & Metrics Templates (8 templates)
Agent: **E_execution** (routing) — Generate test reporting and metrics

- **Test Execution Report** — Executive summary with pass rate, defects, coverage
- **Daily Status Report** — Daily test execution status and blockers
- **Test Metrics Summary** — Test count, execution rate, defect rate, coverage %
- **Defect Summary Report** — Defects by severity, status, component
- **Quality Trends** — Trend analysis over sprints/cycles (pass rate, defect escape, velocity)
- **Test Burndown Chart** — Sprint burndown data for test cases executed
- **Effort & Cost Analysis** — Effort tracking and cost-per-defect analysis
- **Risk Realization Report** — Risks realized, impact, mitigation status

**Output format:** XLSX (7 templates) with data visualization ready

### 10. E2E & Integration Templates (3 templates)
Agent: **L_landscape** — Generate end-to-end chain testing templates

- **E2E Chain Test Design** — End-to-end scenario chains with business process flow
- **Integration Test Matrix** — Component-to-component integration mapping
- **API Chain Testing** — API call sequences and dependency chains

**Output format:** XLSX

### 11. Estimation & Capacity Templates (5 templates)
Agent: **P_planning** — Generate estimation worksheets

- **3-Point Estimation** — Optimistic/Expected/Pessimistic for story point calculation
- **Capacity Planning** — Resource availability × effort = capacity buffer
- **T-Shirt Sizing** — XS/S/M/L/XL for quick estimation
- **Effort Distribution** — Effort by phase (design, execution, reporting, automation)
- **Velocity Tracking** — Sprint velocity and burndown for capacity forecasting

**Output format:** XLSX

### 12. AI & Prompt Templates (2 templates)
Agent: **Exploratory** (routing) — Generate AI testing prompts

- **Test Generation Prompt** — Prompt template for AI model to generate test cases
- **Quality Hunting Prompt** — Prompt template for exploratory test mission generation

**Output format:** DOCX or plaintext

## Template Routing Logic

User request → Category → Agent → Output format

```
User: "Generate a test strategy table for my login feature"
  ↓
Category: strategy_templates
  ↓
Agent: P_planning (Planning Template Agent)
  ↓
Template: test-strategy-table
  ↓
Output: XLSX with populated quality characteristics, risk classes, intensities
```

## The 8 TEMPLATE Agents

### T_technique — Technique Template Agent
**Domain:** Test design technique worksheets
**Handles:** Decision tables, state transition tables, MCDC truth tables, path testing, classification trees
**Load KB:** technique-patterns.json → technique_name → pattern.procedure
**Output:** XLSX with populated conditions, values, test situations, coverage calculations

**Example invocation:**
```
"Generate a decision table for the password validation rule:
 length 8-20, requires uppercase, requires digit, special char optional"
```

### E_execution — Execution Template Agent
**Domain:** Test execution artifacts (logs, scripts, scenarios)
**Handles:** Test case logs, test scripts, test scenarios, Gherkin acceptance criteria
**Load KB:** terminology.json → test_term → definition (for standard field names)
**Output:** XLSX or DOCX with test case ID, preconditions, steps, expected results, post-conditions

**Example invocation:**
```
"Create a test script for the payment checkout flow with 5 test cases"
```

### E_exploratory — Exploratory Template Agent
**Domain:** Exploratory testing charters and debriefing
**Handles:** Exploratory testing charters, session logs, debriefing sheets, quality hunting
**Load KB:** terminology.json → exploratory_testing → definition
**Output:** XLSX or DOCX with mission, test ideas, findings, insights

**Example invocation:**
```
"Generate an exploratory testing charter for the mobile app login feature
 with 90-minute timebox and security focus"
```

### M_management — Management Template Agent
**Domain:** Defect management and issue tracking
**Handles:** Anomaly administration, defect tracking, JIRA logs
**Load KB:** quality-to-technique.json → defect_attributes → severity, priority, status values
**Output:** XLSX with defect fields pre-configured (ID, status, severity, priority, due date)

**Example invocation:**
```
"Create a defect tracking log for the sprint with links to test case IDs"
```

### P_planning — Planning Template Agent
**Domain:** Test planning, strategy, and estimation
**Handles:** Test plans, test strategy tables, WSJF prioritization, estimation worksheets
**Load KB:** template-analysis.json → strategy_templates → strategy structure
**Output:** XLSX or DOCX with populated quality characteristics, technique recommendations, estimates

**Example invocation:**
```
"Generate a master test plan for the Q3 2026 release with work breakdown structure"
```

### L_landscape — Landscape Template Agent
**Domain:** Test strategy, quality engineering strategy, technique selection
**Handles:** Test strategy tables, quality engineering strategy, technique selection matrices
**Load KB:** quality-to-technique.json → quality_characteristic → recommended_techniques
**Output:** XLSX with quality attributes, recommended techniques, intensity levels

**Example invocation:**
```
"Create a quality engineering strategy table for an e-commerce platform
 with security, performance, and usability as primary characteristics"
```

### A_accountability — Accountability Template Agent
**Domain:** Governance, roles, responsibilities, accountability
**Handles:** ARCI matrices, QAM/QPM mappings, quality governance, role definitions
**Load KB:** terminology.json → roles → (PO, Test, Dev, Ops, QA Manager, etc.)
**Output:** XLSX with roles, responsibilities, accountability assignments

**Example invocation:**
```
"Generate an ARCI matrix for the testing team with 8 key activities"
```

### T_traceability — Traceability Template Agent
**Domain:** Traceability matrices, coverage reporting, requirements validation
**Handles:** Traceability matrices, coverage matrices, requirements validation sheets
**Load KB:** template-analysis.json → traceability_templates → traceability structure
**Output:** XLSX or HTML with multi-level traceability and coverage heatmap

**Example invocation:**
```
"Create a requirements traceability matrix linking business requirements to test cases
 with coverage gaps highlighted"
```

## Output Formats by Template Type

| Category | Format | Skill Dependency |
|----------|--------|------------------|
| Technique templates | XLSX | xlsx skill |
| Execution templates | XLSX, DOCX | xlsx, docx skills |
| Exploratory templates | XLSX, DOCX, PDF | xlsx, docx, pdf skills |
| Defect templates | XLSX, DOCX | xlsx, docx skills |
| Checklist templates | DOCX, XLSX | docx, xlsx skills |
| Strategy templates | XLSX, DOCX | xlsx, docx skills |
| Accountability templates | XLSX | xlsx skill |
| Traceability templates | XLSX, HTML | xlsx skill |
| Reporting templates | XLSX | xlsx skill |
| E2E templates | XLSX | xlsx skill |
| Estimation templates | XLSX | xlsx skill |
| AI templates | DOCX, plaintext | docx skill |

## Examples of Use

### Example 1: Decision Table Template
```
User: "Create a decision table for the age validation rule (18-65, must be integer)"

Flow:
  T_technique agent routes to decision-table template
  Load technique pattern: decision table testing
  Enumerate conditions:
    - Condition A: age < 18
    - Condition B: age > 65
    - Condition C: age is not integer
  Generate test situations:
    TS 01: F, F, F → VALID
    TS 02: T, F, F → INVALID (too young)
    TS 03: F, T, F → INVALID (too old)
    TS 04: F, F, T → INVALID (not integer)
  Output: XLSX with 4 test situations + expected outcomes
```

### Example 2: Test Strategy Table
```
User: "Generate a test strategy for a payment processing system"

Flow:
  P_planning agent routes to test-strategy-table template
  Load quality characteristics:
    - Security (functional correctness)
    - Performance (response time < 2s)
    - Availability (99.9% uptime)
  Load risk assessment:
    - Security: Class A (High risk)
    - Performance: Class B (Medium risk)
    - Availability: Class A (High risk)
  Recommend intensity:
    - Security: ●●● (high) → recommend: penetration testing, threat modeling
    - Performance: ●● (medium) → recommend: load testing, profiling
    - Availability: ●●● (high) → recommend: failover testing, chaos engineering
  Output: XLSX with 3 quality characteristics, risk classes, techniques, measures
```

### Example 3: ARCI Matrix
```
User: "Create an ARCI matrix for test team with activities: planning, design, execution,
        reporting, automation, defect management"

Flow:
  A_accountability agent routes to arci-matrix template
  Load roles from KB: Test Manager, QA Engineer, QA Automation, Business Analyst
  Create matrix:
    Activity | Test Manager | QA Engineer | QA Automation | Business Analyst
    ---------|--------------|-------------|---------------|------------------
    Planning | A            | R           | C             | C
    Design   | C            | R           | C             | I
    Execute  | I            | R           | R             | I
    Report   | A            | R           | I             | I
    Automate | C            | C           | A             | I
    Defects  | R            | R           | C             | C
  Output: XLSX with color coding (A=red, R=yellow, C=green, I=gray)
```

### Example 4: Exploratory Testing Charter
```
User: "Generate a 2-hour exploratory charter for mobile app payment flow with focus on edge cases"

Flow:
  E_exploratory agent routes to charter-full template
  Generate charter header:
    Mission: "Find edge cases and data validation issues in payment checkout"
    Duration: 120 minutes
    Scope: Payment form, validation, API integration
  Generate test ideas:
    - Test with expired card
    - Test with international characters in name
    - Test with max/min amount
    - Test with network interruption during submit
    - Test with rapid submission (double-click)
  Output: XLSX with charter, session log, debriefing sheets
```

## Knowledge Base Files Referenced

- **terminology.json** (1,105 terms) — Standard test terminology and definitions
- **technique-patterns.json** (106 patterns) — Test technique procedures and patterns
- **template-analysis.json** (108 templates) — Template structure, fields, output format
- **quality-to-technique.json** — Quality characteristics mapped to recommended techniques
- **All standards files** (IEEE 829, ISO 29119, ISTQB) — Standard structures

## Key Design Principles

1. **Template-First:** Every template has a pre-defined structure in template-analysis.json
2. **Agent Routing:** User request → category keyword → agent → template lookup
3. **KB Population:** Populate template fields from user context, load patterns from KB
4. **Format Automation:** XLSX for data-heavy, DOCX for narrative, PDF for distribution
5. **Reusable:** Generate once, customize many times — all outputs are editable

## Skill Dependencies

This skill depends on the following:
- **xlsx skill** — For generating and populating XLSX templates
- **docx skill** — For generating and populating DOCX templates
- **pdf skill** — For generating PDF templates (export)

---

*Version 1.0 | Open Testing Ecosystem | Generated 2026-04-05*
