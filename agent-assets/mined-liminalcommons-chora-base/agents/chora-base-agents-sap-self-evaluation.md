---
sap_id: SAP-019
version: 1.0.0
status: active
last_updated: 2025-11-04
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 10
progressive_loading:
  phase_1: "lines 1-120"    # Quick Reference + Status Check Workflow
  phase_2: "lines 121-250"  # Deep Dive + Strategic Analysis Workflows
  phase_3: "full"           # Complete including troubleshooting and integration
phase_1_token_estimate: 3500
phase_2_token_estimate: 7500
phase_3_token_estimate: 10000
---

# SAP Self-Evaluation (SAP-019) - Agent Awareness

**SAP ID**: SAP-019
**Capability**: sap-self-evaluation
**Last Updated**: 2025-11-04

---

## 📖 Quick Reference

**New to SAP-019?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - Quick check: Is SAP-004 installed and functional? (30 seconds)
- 📚 **Time Savings** - 15-20 min/sprint automated evaluation vs manual assessment, evidence-based decisions
- 🎯 **Feature 1** - Three depth levels (30s quick check, 5min deep dive, 30min strategic analysis) adapt to available time
- 🔧 **Feature 2** - Quick check validates file existence, command execution, and exit codes without LLM overhead
- 📊 **Feature 3** - Deep dive analyzes actual content quality, integration depth, and usage patterns beyond automated checks
- 🔗 **Integration** - Works with SAP-000 (Framework)

This AGENTS.md provides: Agent-specific patterns for implementing SAP-019.
n.

---

## Quick Reference

This file provides **agent-executable workflows** for self-evaluating SAP adoption depth across projects.

### What is SAP Self-Evaluation?

A **progressive assessment framework** enabling agents to:
1. **Assess** SAP adoption maturity (Level 0/1/2/3 per SAP)
2. **Identify** prioritized gaps blocking value (P1/P2/P3 with effort estimates)
3. **Generate** actionable roadmaps for continuous improvement

### When to Use

**Trigger Signals**:

| User Signal | Workflow | Evaluation Mode |
|-------------|----------|-----------------|
| "How are we doing with SAPs?" | Workflow 1 | Quick Check (30s) |
| "Show me SAP adoption status" | Workflow 1 | Quick Check (30s) |
| "How can we improve SAP-004?" | Workflow 2 | Deep Dive (5min) |
| "What gaps are blocking us?" | Workflow 2 | Deep Dive (5min) |
| "Generate SAP roadmap" | Workflow 3 | Strategic Analysis (30min) |
| "What should we prioritize next?" | Workflow 3 | Strategic Analysis (30min) |
| "Track SAP adoption progress" | Workflow 4 | Timeline Analysis |
| "Validate SAP-011 installation" | Workflow 5 | Quick Check (single SAP) |

**Do NOT Use For**:
- SAP installation (use `install-sap.py` instead)
- Generating new SAPs (use SAP-029 sap-generation)
- Bug fixing or debugging

### Core Files

```
scripts/
├── sap-evaluator.py           # CLI tool (primary interface)
└── batch-evaluate-saps.py     # Batch evaluation across all SAPs

utils/
├── sap_evaluation.py          # Core evaluation engine
└── awareness_validation.py    # AGENTS.md/CLAUDE.md validation

docs/skilled-awareness/sap-self-evaluation/
├── capability-charter.md      # Problem statement, ROI
├── protocol-spec.md           # Evaluation logic, data models
├── awareness-guide.md         # Detailed agent workflows
├── adoption-blueprint.md      # Installation guide
└── ledger.md                  # Adoption tracking, version history
```

---

## Common Workflows

### Workflow 1: Quick Status Check (30 seconds)

**User Signal**: "How are we doing with SAPs?" or "Show adoption status"

**Context**: User wants high-level overview of SAP adoption across the project.

**Steps**:

1. **Run quick check** on all SAPs:
   ```bash
   python scripts/sap-evaluator.py --quick
   ```

2. **Parse output** for key metrics:
   - Total SAPs installed (e.g., 12/18 = 67%)
   - Adoption level distribution (Level 0/1/2/3 counts)
   - Health status (✅/❌/🟡 indicators)

3. **Identify top priority** (highest impact gap):
   - Look for P1 gaps in strategic SAPs (SAP-003, SAP-004, SAP-006, SAP-008)

4. **Summarize for user**:
   ```markdown
   ## SAP Adoption Status

   **Coverage**: 12/30 SAPs installed (40%)
   **Maturity**: 8/12 at Level 2+ (67%)
   **Health**: 🟢 Strong adoption

   **Top Priority**: SAP-004 (Testing Framework)
   - Current: Level 1 (basic tests only)
   - Gap: No coverage tracking → blocks CI/CD quality gates
   - Action: Enable pytest-cov (30 minutes, see deep dive)

   Run deep dive for details:
   `python scripts/sap-evaluator.py --deep SAP-004`
   ```

5. **Offer next action**: "Would you like me to run a deep dive on SAP-004?"

**Expected Output**: Terminal summary with color-coded status and top 1-3 priorities.

---

### Workflow 2: Deep Dive Gap Analysis (5 minutes)

**User Signal**: "How can we improve SAP-004?" or "What gaps are blocking us?"

**Context**: User wants detailed analysis of specific SAP with actionable next steps.

**Steps**:

1. **Run deep dive** on target SAP:
   ```bash
   python scripts/sap-evaluator.py --deep SAP-004
   ```

2. **Read evaluation output** (printed to terminal):
   - Current adoption level (0/1/2/3)
   - Completion percentage toward next level
   - Validation results (which checks passed/failed)
   - Gap list with priorities (P1/P2/P3)

3. **Analyze gaps** for prioritization:
   - **P1 gaps**: Blockers preventing adoption (missing files, broken validation)
   - **P2 gaps**: Quality issues reducing value (incomplete integration)
   - **P3 gaps**: Nice-to-have improvements

4. **Extract actionable tasks**:
   - For each P1 gap:
     - What needs to be done (specific action)
     - Estimated effort (hours)
     - Validation command (how to verify fix)

5. **Present prioritized roadmap** to user:
   ```markdown
   ## SAP-004 Deep Dive Results

   **Current**: Level 1 (75% toward Level 2)
   **Blockers**: 2 P1 gaps

   ### Immediate Actions (P1)

   1. **Enable coverage tracking** (30 minutes)
      - Install: `pip install pytest-cov`
      - Configure: Add `addopts = --cov=src` to `pyproject.toml`
      - Validate: `pytest --cov=src --cov-report=term`

   2. **Add coverage badge** (15 minutes)
      - Generate: `pytest --cov=src --cov-report=html`
      - Add badge to README.md
      - Validate: Check badge displays correctly

   **Impact**: Unlocks Level 2 → enables SAP-006 (Quality Gates) integration
   **Total Effort**: 45 minutes
   ```

6. **Ask for approval**: "Should I proceed with these changes?"

**Expected Output**: Detailed gap analysis with prioritized, sprint-ready action items.

---

### Workflow 3: Strategic Roadmap Generation (30 minutes)

**User Signal**: "Generate SAP roadmap" or "What should we prioritize next quarter?"

**Context**: User wants multi-sprint roadmap for SAP adoption improvements.

**Steps**:

1. **Run strategic analysis**:
   ```bash
   python scripts/sap-evaluator.py --strategic --output sap-roadmap.yaml
   ```

2. **Wait for analysis** (may take 15-30 minutes):
   - Evaluates all SAPs (quick + deep dive)
   - Analyzes dependencies between SAPs
   - Groups gaps into sprint themes
   - Generates quarterly roadmap

3. **Read generated roadmap** (`sap-roadmap.yaml`):
   - **Quarterly goals** (high-level objectives)
   - **Sprint breakdown** (2-week chunks)
   - **Dependency ordering** (which SAPs to adopt first)
   - **Effort estimates** (total hours per sprint)

4. **Parse roadmap structure**:
   ```yaml
   roadmap:
     quarter: Q1 2026
     goals:
       - Achieve 80% SAP coverage (24/30 SAPs)
       - Reach Level 2+ for all core SAPs
     sprints:
       - sprint: 1
         theme: Testing & Quality Foundation
         saps:
           - SAP-004: Enable coverage tracking
           - SAP-006: Add quality gates to CI
         estimated_hours: 12
   ```

5. **Integrate with planning**:
   - Option A: Update `ECOSYSTEM_STATUS.yaml` (if exists)
   - Option B: Create sprint plans in `docs/project-docs/sprints/`
   - Option C: Create coordination request in `inbox/active/`

6. **Present roadmap to user**:
   ```markdown
   ## Q1 2026 SAP Adoption Roadmap

   **Goal**: 80% coverage (24/30 SAPs), all core SAPs at Level 2+

   ### Sprint 1 (Weeks 1-2): Testing & Quality Foundation
   - SAP-004: Coverage tracking (3 hours)
   - SAP-006: Quality gates (4 hours)
   - **Outcome**: Automated quality enforcement in CI

   ### Sprint 2 (Weeks 3-4): Docker & Automation
   - SAP-011: Containerize app (5 hours)
   - SAP-008: Add automation scripts (3 hours)
   - **Outcome**: One-command dev environment setup

   **Total**: 4 sprints, 38 hours estimated

   Roadmap saved to: `sap-roadmap.yaml`
   ```

7. **Offer to create sprint plans**: "Should I create sprint plans in `docs/project-docs/sprints/`?"

**Expected Output**: YAML roadmap file + markdown summary for user.

---

### Workflow 4: Batch Evaluation Across All SAPs (2 minutes)

**User Signal**: "Evaluate all SAPs" or "Generate comprehensive adoption report"

**Context**: User wants complete picture of SAP adoption across entire catalog.

**Steps**:

1. **Run batch evaluation**:
   ```bash
   python scripts/batch-evaluate-saps.py --output /tmp/sap-eval-results.json
   ```

2. **Wait for completion** (evaluates all 30 SAPs):
   - Runs deep dive on each SAP
   - Checks awareness file coverage (AGENTS.md/CLAUDE.md)
   - Aggregates gaps by priority

3. **Read results** from JSON output:
   ```json
   {
     "summary": {
       "awareness_coverage": {
         "both_files": ["SAP-004", "SAP-011", "SAP-012"],
         "agents_only": ["SAP-001", "SAP-009"],
         "neither": ["SAP-003", "SAP-006", "SAP-008"]
       },
       "total_gaps": 77,
       "p1_gaps": 53,
       "p2_gaps": 23
     }
   }
   ```

4. **Analyze coverage patterns**:
   - Which SAPs have both awareness files? (✅ best practice)
   - Which SAPs missing awareness files? (⚠️ needs documentation)
   - Distribution of adoption levels (how many at Level 2+?)

5. **Identify strategic priorities**:
   - SAPs missing awareness files but at Level 2 (need docs)
   - SAPs with P1 gaps (blockers preventing adoption)

6. **Present comprehensive report**:
   ```markdown
   ## Comprehensive SAP Evaluation Results

   **Coverage**:
   - 8/30 SAPs have both AGENTS.md and CLAUDE.md ✅
   - 20/30 SAPs missing awareness files ⚠️

   **Gaps**:
   - 53 P1 gaps (blockers)
   - 23 P2 gaps (quality)

   **Strategic Priorities**:
   1. SAP-003 (project-bootstrap) - No awareness files, Level 2
   2. SAP-008 (automation-scripts) - No awareness files, Level 2
   3. SAP-019 (sap-self-evaluation) - No awareness files, Level 2

   **Recommendation**: Create awareness files for top 3 strategic SAPs
   ```

**Expected Output**: JSON file + terminal summary with strategic recommendations.

---

### Workflow 5: Validate Single SAP Installation (30 seconds)

**User Signal**: "Check if SAP-011 is installed correctly" or "Validate Docker SAP"

**Context**: After installing a SAP, verify it's working correctly.

**Steps**:

1. **Run quick check** on specific SAP:
   ```bash
   python scripts/sap-evaluator.py --quick SAP-011
   ```

2. **Review validation results**:
   - ✅ `artifacts_complete`: All required files present
   - ✅ `installed`: Validation commands pass
   - ✅ `awareness_files`: AGENTS.md and CLAUDE.md exist with valid YAML

3. **Check adoption level**:
   - Level 0: Installed but not configured
   - Level 1: Basic usage
   - Level 2: Integrated with project
   - Level 3: Full mastery

4. **If validation fails**, identify missing pieces:
   - Missing files (check protocol-spec.md for required artifacts)
   - Failed validation commands (check adoption-blueprint.md for setup)
   - Missing awareness files (check SAP-009 for documentation requirements)

5. **Report status to user**:
   ```markdown
   ## SAP-011 Validation Results

   ✅ Installation: Complete
   ✅ Artifacts: All 5 files present (Dockerfile, docker-compose.yml, etc.)
   ✅ Awareness: Both AGENTS.md and CLAUDE.md with valid YAML

   **Adoption Level**: Level 1 (basic usage)
   **Next Step**: Add CI integration to reach Level 2 (see deep dive)
   ```

**Expected Output**: Quick validation status with next steps for improvement.

---

## Best Practices

### Practice 1: Run Quick Check Regularly

**Pattern**: Add quick check to weekly or sprint reviews.

```bash
# In sprint review script
python scripts/sap-evaluator.py --quick > sap-status.txt
cat sap-status.txt
```

**Why**: Proactive visibility into adoption health prevents drift.

---

### Practice 2: Deep Dive Before Sprints

**Pattern**: Run deep dive on target SAP before planning sprint work.

```bash
# Before sprint planning
python scripts/sap-evaluator.py --deep SAP-004 > sap-004-analysis.md
# Review analysis, extract P1 gaps → add to sprint plan
```

**Why**: Ensures sprint work is prioritized (focus on P1 gaps first).

---

### Practice 3: Strategic Analysis Quarterly

**Pattern**: Generate roadmap at start of each quarter.

```bash
# Q1 planning
python scripts/sap-evaluator.py --strategic --output q1-sap-roadmap.yaml
# Review roadmap → integrate with OKRs
```

**Why**: Aligns SAP adoption with strategic goals, tracks progress over time.

---

### Practice 4: Validate After Installation

**Pattern**: Always run quick check after installing new SAP.

```bash
# After: python scripts/install-sap.py SAP-011
python scripts/sap-evaluator.py --quick SAP-011
```

**Why**: Catches installation issues early (missing files, broken commands).

---

### Practice 5: Track Gaps in Ledger

**Pattern**: Update SAP ledgers with evaluation results.

```bash
# After deep dive SAP-011:
# 1. Read: docs/skilled-awareness/docker-operations/ledger.md
# 2. Add: Section with evaluation date, gaps identified, actions taken
```

**Why**: Creates historical record of improvement journey.

---

## Common Pitfalls

### Pitfall 1: Running Strategic Analysis Too Frequently

**Problem**: Strategic analysis takes 30 minutes and generates large roadmaps. Running it weekly creates noise.

**Fix**: Use appropriate evaluation mode for context:
- **Daily/Weekly**: Quick check (30s)
- **Sprint planning**: Deep dive (5min)
- **Quarterly**: Strategic analysis (30min)

---

### Pitfall 2: Ignoring P1 Gaps

**Problem**: Focusing on P2/P3 improvements while P1 blockers prevent adoption.

**Fix**: Always address P1 gaps first:
```bash
# Read gap priority in output
# Priority: P1 → blocker (fix immediately)
# Priority: P2 → quality issue (fix in next sprint)
# Priority: P3 → nice-to-have (defer if low impact)
```

---

### Pitfall 3: Not Validating Fixes

**Problem**: Marking gap as resolved without running validation command.

**Fix**: Every gap has a validation command - always run it:
```bash
# Gap: "Coverage tracking not enabled"
# Validation: pytest --cov=src --cov-report=term

# After fix:
pytest --cov=src --cov-report=term  # Must pass ✅
```

---

### Pitfall 4: Forgetting Dependency Order

**Problem**: Trying to adopt SAP-006 (Quality Gates) before SAP-004 (Testing Framework).

**Fix**: Check protocol-spec.md for dependencies:
```markdown
# SAP-006 protocol-spec.md
Dependencies:
- SAP-004 (testing-framework) - REQUIRED
- SAP-005 (ci-cd-workflows) - REQUIRED
```

Adopt dependencies first, then dependent SAPs.

---

### Pitfall 5: Not Creating Awareness Files After Adoption

**Problem**: SAP reaches Level 2 but no AGENTS.md/CLAUDE.md to document workflows.

**Fix**: After reaching Level 2, create awareness files:
1. Read capability-charter.md, protocol-spec.md
2. Write AGENTS.md (generic workflows)
3. Write CLAUDE.md (Claude Code patterns)
4. Add Section 9.5 to protocol-spec.md (validation criteria)

---

## Integration with Other SAPs

**SAP-004** (testing-framework):
- Self-evaluation checks test coverage metrics
- Gap analysis identifies missing test types

**SAP-006** (quality-gates):
- Self-evaluation validates quality gate configuration
- Checks if gates are enforced in CI

**SAP-009** (agent-awareness):
- Self-evaluation validates AGENTS.md/CLAUDE.md presence
- Checks YAML frontmatter structure, progressive loading

**SAP-013** (metrics-framework):
- Self-evaluation generates adoption metrics
- Tracks improvement velocity over time

**SAP-029** (sap-generation):
- After generating new SAP, validate installation with SAP-019
- Ensure new SAP has both AGENTS.md and CLAUDE.md

---

## Support & Resources

**SAP-019 Documentation**:
- [Capability Charter](capability-charter.md) - Problem statement, impact analysis
- [Protocol Spec](protocol-spec.md) - Evaluation logic, data models, APIs
- [Awareness Guide](awareness-guide.md) - Detailed agent workflows (this file's sibling)
- [Adoption Blueprint](adoption-blueprint.md) - Installation instructions
- [Ledger](ledger.md) - Adoption tracking, version history

**Scripts**:
- [sap-evaluator.py](../../../scripts/sap-evaluator.py) - CLI tool (primary interface)
- [batch-evaluate-saps.py](../../../scripts/batch-evaluate-saps.py) - Batch evaluation
- [sap_evaluation.py](../../../utils/sap_evaluation.py) - Core engine (import in Python)
- [awareness_validation.py](../../../utils/awareness_validation.py) - AGENTS.md/CLAUDE.md validator

**Related SAPs**:
- [SAP-009 (agent-awareness)](../agent-awareness/) - Awareness file protocol
- [SAP-013 (metrics-framework)](../metrics-framework/) - Metrics collection
- [SAP-029 (sap-generation)](../sap-generation/) - SAP generation from prompts

---

## Version History

- **1.0.0** (2025-11-04): Initial AGENTS.md for SAP-019
  - 5 core workflows (Quick Check, Deep Dive, Strategic Analysis, Batch Evaluation, Validation)
  - User signal pattern table (8 signals → workflows)
  - 5 best practices (regular checks, pre-sprint deep dives, quarterly strategic, validate installs, track in ledgers)
  - 5 common pitfalls (frequency, P1 priority, validation, dependencies, awareness files)
  - Integration with SAP-004, SAP-006, SAP-009, SAP-013, SAP-029

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific tool usage patterns
2. Review [protocol-spec.md](protocol-spec.md) for evaluation algorithms and data models
3. Try Workflow 1: Run quick check to assess current SAP adoption
4. Try Workflow 2: Deep dive on one strategic SAP to identify prioritized gaps
