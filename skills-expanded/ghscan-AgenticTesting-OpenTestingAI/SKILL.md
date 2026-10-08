---
name: open-testing-management
description:       Test management, defect management, process evaluation, and maturity assessment using the MANAGES agent pipeline. Use this skill whenever the user mentions test management, defect management, process improvement, TMMi, maturity assessment, ARCI matrix, quality policy, test policy, process evaluation, defect lifecycle, triage, test process, roles and responsibilities, QAM, QPM, GTA, generic test agreements, process maturity, test improvement, or wants to evaluate and improve their testing practices. Also trigger for defect tracking, anomaly management, process compliance, test governance, or organizational testing capability. MANDATORY TRIGGERS: test management, defect management, TMMi, maturity, ARCI, process improvement, quality policy, defect lifecycle, process evaluation, test governance.
---

<!-- Tip: Use /open-testing-management in chat to generate content with agent assistance -->

# Open Testing Management (MANAGES)

Assess, govern, and improve test processes using TMMi maturity models, TMap organizing topics, and ISO 29119 process standards. The MANAGES pipeline evaluates current testing practices, identifies gaps, and generates improvement roadmaps.

## Agent Pipeline

### Agent 1: M_maturity — Maturity Assessor

**Purpose:** Assess test process maturity using the TMMi (Test Maturity Model integration) framework.

**TMMi Levels:**

| Level | Name | Process Areas | Focus |
|---|---|---|---|
| 1 | Initial | — | Ad hoc, chaotic testing |
| 2 | Managed | Test Policy & Strategy, Test Planning, Test Monitoring & Control, Test Design & Execution, Test Environment | Basic test management |
| 3 | Defined | Test Organization, Test Training, Test Lifecycle & Integration, Non-Functional Testing, Peer Reviews | Standardized processes |
| 4 | Measured | Test Measurement, Product Quality Evaluation, Advanced Peer Reviews, Quality Control | Quantitative management |
| 5 | Optimization | Defect Prevention, Test Process Optimization, Quality Optimization | Continuous improvement |

**Assessment Procedure:**
1. Load TMMi process areas from `standards/tmmi.json` (16 process areas, 113 practices)
2. For each process area, evaluate specific goals and specific practices
3. Rate each practice: Not Performed / Partially Performed / Largely Performed / Fully Performed
4. Calculate process area satisfaction (all specific goals must be satisfied)
5. Determine overall maturity level (all PAs at that level must be satisfied)
6. Generate gap analysis showing practices that need improvement

**Output:** TMMi Assessment Report (xlsx) with:
- Executive Summary and overall maturity level
- Per-process-area scoring with evidence
- Gap analysis with specific improvement actions
- Radar chart showing capability per process area
- Improvement roadmap with timeline

**KB Files:** `standards/tmmi.json` — 5 levels, 16 process areas, specific goals, specific practices

### Agent 2: A_anomaly — Defect Lifecycle Manager

**Purpose:** Manage the complete defect lifecycle from logging through closure.

**Defect Lifecycle States:**
```
New → Assigned → In Progress → Resolved → Verified → Closed
                     ↓                        ↓
                 Deferred              Reopened → Assigned
```

**Anomaly Administration Template (per IEEE 1044.1-1995):**

| Field | Description |
|---|---|
| Anomaly ID | Unique identifier |
| Title | Brief description |
| Severity | Critical / Major / Minor / Trivial |
| Priority | Immediate / High / Medium / Low |
| Status | Current lifecycle state |
| Found By | Tester name/ID |
| Found Date | Discovery date |
| Found In | Test level, build, environment |
| Assigned To | Developer/team responsible |
| Root Cause | Logic / Computation / Interface / Data / Documentation |
| Resolution | Fix description |
| Verified By | Tester who verified fix |
| Closed Date | Closure date |

**Triage Process:**
1. Review new anomalies daily
2. Classify by severity and priority using IEEE 1044.1 classification scheme
3. Assign to appropriate developer/team
4. Set target resolution date based on priority
5. Track aging — escalate overdue anomalies

### Agent 3: N_norming — Process Compliance Evaluator

**Purpose:** Evaluate test processes against recognized standards and generate compliance checklists.

**Standards Evaluated:**
- **ISO/IEC/IEEE 29119-2**: Test processes (organizational, management, fundamental)
- **TMMi**: Process areas and practices
- **TMap**: Organizing and performing topics
- **IEEE 730-2014**: SQA processes (16 activities in 3 groups)
- **IEEE 1028-2008**: Reviews and audits (5 types)

**Process Evaluation Checklist Generation:**
For each standard, generate a checklist with:
- Process/Practice/Activity name
- Description of expected practice
- Evidence required
- Current status (Conformant / Partially Conformant / Non-Conformant / Not Applicable)
- Gap description and remediation action

**KB Files:** `standards/iso-29119.json`, `standards/tmmi.json`, `standards/tmap.json`, `standards/ieee-standards.json`

### Agent 4: A_accountability_mgmt — Accountability Agent

**Purpose:** Define roles, responsibilities, and accountability using ARCI matrices and quality mappings.

**ARCI Matrix (Accountable, Responsible, Consulted, Informed):**

| Activity | QA Manager | Test Lead | Test Analyst | Developer | Product Owner |
|---|---|---|---|---|---|
| Test Strategy | A | R | C | I | C |
| Test Planning | I | A | R | C | I |
| Test Design | I | C | A/R | C | I |
| Test Execution | I | C | A/R | I | I |
| Defect Triage | C | A | R | R | I |
| Release Advice | A | R | C | C | I |

**Quality Activity Matrix (QAM):** Maps quality measures to activities
**Quality People Matrix (QPM):** Maps quality measures to roles/people

Generate these matrices populated with project-specific context from user input.

### Agent 5: G_governance_mgmt — Governance Agent

**Purpose:** Generate quality and test policies, generic test agreements (GTA), and process documentation.

**Documents Generated:**

1. **Quality & Test Policy** — Organization-level document defining testing principles, scope, objectives, and standards adherence. Aligned with TMap quality & test policy template.

2. **Generic Test Agreements (GTA)** — Standardized agreements defining:
   - Test levels and their boundaries
   - Entry and exit criteria per level
   - Defect severity/priority definitions
   - Communication protocols
   - Escalation procedures
   - Environment requirements

3. **Test Process Description** — Detailed process documentation aligned with ISO 29119-2:
   - Organizational test process
   - Test management process
   - Dynamic test processes (design, implementation, execution, completion)

### Agent 6: E_efficiency — Efficiency Analyzer

**Purpose:** Analyze test process efficiency using quantitative metrics.

**Efficiency Metrics:**

| Metric | Formula | Target | Interpretation |
|---|---|---|---|
| Defect Detection Effectiveness | (Defects found in testing / Total defects) × 100 | >85% | Higher = better testing |
| Defect Removal Efficiency | (Defects removed before release / Total defects) × 100 | >90% | Higher = fewer escapes |
| Test Execution Velocity | Test cases executed per tester per day | Varies | Higher = more efficient |
| Cost per Defect Found | Total test cost / Defects found | <$500 | Lower = more efficient |
| Automation ROI | (Manual cost saved - Automation cost) / Automation cost | >200% | Higher = better ROI |
| Defect Leakage | (Post-release defects / Total defects) × 100 | <10% | Lower = better |
| Test Case Effectiveness | Defects found per test case | >0.1 | Higher = better test design |
| Review Effectiveness | Defects found per review hour | >1.0 | Higher = more efficient |

**IEEE 982.2-1988 Measures Applied:** Fault density (A1), Defect density (A2), Test coverage (A25), Defect removal efficiency (A39)

### Agent 7: S_improvement — Improvement Planner

**Purpose:** Generate process improvement plans using TMMi improvement vectors.

**Improvement Planning Procedure:**
1. Start from M_maturity assessment results (current level and gaps)
2. Identify improvement actions for each unsatisfied practice
3. Prioritize using impact/effort matrix:
   - **Quick Wins**: High impact, low effort — implement immediately
   - **Strategic**: High impact, high effort — plan for next quarter
   - **Fill-ins**: Low impact, low effort — do when convenient
   - **Deprioritize**: Low impact, high effort — defer or skip
4. Create improvement roadmap with milestones and owners
5. Define success metrics for each improvement action

**Improvement Roadmap Template:**

| # | Improvement Action | TMMi PA | Current State | Target State | Priority | Owner | Timeline | Success Metric |
|---|---|---|---|---|---|---|---|---|
| 1 | Implement test policy | Test Policy & Strategy | Not performed | Fully performed | Quick Win | QA Mgr | 2 weeks | Policy approved |
| 2 | Standardize test design | Test Design & Execution | Partially | Largely | Strategic | Test Lead | 3 months | 80% techniques applied |
| 3 | Establish peer reviews | Peer Reviews | Not performed | Largely | Strategic | QA Mgr | 2 months | 100% deliverables reviewed |

## Knowledge Base

Located at `/sessions/trusting-pensive-ptolemy/mnt/Open-Testing/knowledge-base/`:
- `terminology.json` — 1105 terms including management terminology
- `standards/tmmi.json` — 5 maturity levels, 16 process areas, 113 practices
- `standards/tmap.json` — 11 organizing topics, 9 performing topics
- `standards/iso-29119.json` — Testing processes and documentation
- `standards/ieee-standards.json` — IEEE 730 (SQA), 829 (documentation), 1028 (reviews), 1044.1 (anomaly classification)
- `supporting-materials.json` — 20 course knowledge domains and exercise patterns

Read the xlsx skill at `/sessions/trusting-pensive-ptolemy/mnt/.claude/skills/xlsx/SKILL.md` before generating spreadsheets.
Read the docx skill at `/sessions/trusting-pensive-ptolemy/mnt/.claude/skills/docx/SKILL.md` before generating documents.

## Example Invocations

**"Assess our testing maturity"**
→ M_maturity TMMi assessment → N_norming standards compliance → E_efficiency metrics → S_improvement roadmap

**"Set up defect management for our project"**
→ A_anomaly lifecycle definition → G_governance GTA with severity/priority definitions → A_accountability ARCI matrix

**"Help us improve our test process"**
→ M_maturity current state → E_efficiency bottleneck analysis → S_improvement prioritized roadmap

**"Create a quality policy for our organization"**
→ G_governance quality & test policy → A_accountability roles/ARCI → N_norming standards alignment

## Integration

- **open-testing-design**: Governance agent outputs feed into strategy design
- **open-testing-reporting**: Efficiency metrics feed into trend reports
- **open-testing-coverage**: Coverage data informs maturity assessment
- **TMMi**: Primary framework for maturity assessment (5 levels, 16 PAs)
- **TMap**: Organizing topics align with management activities
