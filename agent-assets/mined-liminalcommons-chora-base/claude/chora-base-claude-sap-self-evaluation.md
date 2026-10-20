---
sap_id: SAP-019
version: 1.0.0
status: active
last_updated: 2025-11-04
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 11
progressive_loading:
  phase_1: "lines 1-100"    # Quick Start + Quick Check Workflow
  phase_2: "lines 101-240"  # Deep Dive + Strategic Workflows
  phase_3: "full"           # Complete including tips and pitfalls
phase_1_token_estimate: 3000
phase_2_token_estimate: 7000
phase_3_token_estimate: 11000
---

# SAP Self-Evaluation (SAP-019) - Claude-Specific Awareness

**SAP ID**: SAP-019
**Claude Compatibility**: Sonnet 4.5+
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

This CLAUDE.md provides: Claude Code-specific workflows for implementing SAP-019.
).

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for self-evaluating SAP adoption using Claude's tool suite (Bash, Read, Edit, Write).

### First-Time Evaluation

1. Read [AGENTS.md](AGENTS.md) for generic self-evaluation workflows
2. Use this file for Claude Code tool integration (Bash for evaluation, Read for analysis, Edit for updates)
3. Run quick check → deep dive → update ledgers with results

### Session Resumption

- Use Bash tool to run `python scripts/sap-evaluator.py --quick`
- Use Read tool to view evaluation reports
- Use Edit tool to update ledgers with findings
- Use Glob tool to find SAP directories needing evaluation

---

## Claude Code Self-Evaluation Workflows

### Workflow 1: Running Quick Status Check with Claude Code

```markdown
User: "How are we doing with SAP adoption?"

Claude (Phase 1: Run Quick Check - 0-5k tokens):
1. Execute quick check via Bash:
   Bash: python scripts/sap-evaluator.py --quick
2. Capture output showing all SAPs status

Claude (Phase 2: Parse Results - 5-10k tokens):
3. Parse Bash output for key metrics:
   - Total SAPs: 30
   - Installed: count ✅ indicators
   - Adoption levels: count Level 0/1/2/3
   - Top priorities: identify P1 gaps

Claude (Phase 3: Summarize for User - 10-15k tokens):
4. Present summary to user:

"## SAP Adoption Status

**Coverage**: 12/30 SAPs installed (40%)
**Maturity**: 8/12 at Level 2+ (67%)

**Strategic Gaps** (P1):
1. SAP-003 (project-bootstrap) - Missing awareness files
2. SAP-008 (automation-scripts) - Missing awareness files
3. SAP-019 (sap-self-evaluation) - Missing awareness files

**Recommendation**: Create awareness files for top 3 SAPs (6-9 hours total)

Would you like me to run a deep dive on SAP-003 to identify specific actions?"

Result: User has clear visibility, knows next step
```

---

### Workflow 2: Deep Dive with Gap Analysis Using Claude Code

```markdown
User: "Run deep dive on SAP-004 and tell me what to fix"

Claude (Phase 1: Execute Deep Dive - 0-5k tokens):
1. Run deep dive via Bash:
   Bash: python scripts/sap-evaluator.py --deep SAP-004
2. Capture detailed evaluation output

Claude (Phase 2: Parse Gap Analysis - 5-15k tokens):
3. Extract from Bash output:
   - Current level (e.g., Level 1)
   - Completion % (e.g., 75% toward Level 2)
   - Gap list with priorities:
     - Gap 1: P1, impact=high, effort=medium, 2 hours
     - Gap 2: P1, impact=medium, effort=low, 30 minutes
     - Gap 3: P2, impact=low, effort=medium, 1 hour

4. Identify P1 gaps (blockers):
   - Filter gaps where priority == "P1"
   - Sort by impact (high → medium → low)

Claude (Phase 3: Generate Action Plan - 15-30k tokens):
5. Create actionable task list:

"## SAP-004 Deep Dive: Action Plan

**Current**: Level 1 (75% toward Level 2)
**Blockers**: 2 P1 gaps

### Immediate Actions

#### 1. Enable Coverage Tracking (P1, 30 minutes)
**Why**: Blocks CI/CD quality gates (SAP-006 dependency)
**Steps**:
1. Install pytest-cov:
   ```bash
   pip install pytest-cov
   ```
2. Configure in pyproject.toml:
   ```toml
   [tool.pytest.ini_options]
   addopts = "--cov=src --cov-report=term --cov-fail-under=85"
   ```
3. Validate:
   ```bash
   pytest --cov=src
   ```

**Validation**: Should see coverage report ≥85%

#### 2. Add Coverage Badge (P1, 15 minutes)
**Why**: Visibility for stakeholders, completes Level 2
**Steps**:
1. Generate HTML report:
   ```bash
   pytest --cov=src --cov-report=html
   ```
2. Add badge to README.md
3. Commit changes

**Total Effort**: 45 minutes to reach Level 2
**Impact**: Unlocks SAP-006 (Quality Gates) adoption

Should I proceed with these changes?"

Result: User has sprint-ready task list with validation commands
```

---

### Workflow 3: Strategic Roadmap Generation with Claude Code

```markdown
User: "Generate a SAP adoption roadmap for next quarter"

Claude (Phase 1: Run Strategic Analysis - 0-5k tokens):
1. Execute strategic analysis:
   Bash: python scripts/sap-evaluator.py --strategic --output /tmp/sap-roadmap.yaml

2. Wait for completion (may take 15-30 minutes):
   # This runs deep dive on all SAPs, analyzes dependencies, generates roadmap

Claude (Phase 2: Read Generated Roadmap - 5-20k tokens):
3. Read roadmap file:
   Read /tmp/sap-roadmap.yaml

4. Parse YAML structure:
   - Quarter and goals
   - Sprint breakdown (2-week iterations)
   - SAP priorities per sprint
   - Effort estimates

Example roadmap structure:
```yaml
roadmap:
  quarter: Q1 2026
  goals:
    - "Achieve 80% SAP coverage (24/30 SAPs)"
    - "Reach Level 2+ for all core SAPs"

  sprints:
    - sprint: 1
      theme: "Testing & Quality Foundation"
      saps:
        - sap_id: SAP-004
          actions: ["Enable coverage", "Add badge"]
          hours: 3
        - sap_id: SAP-006
          actions: ["Configure quality gates", "Add CI integration"]
          hours: 4
      total_hours: 7

    - sprint: 2
      theme: "Docker & Automation"
      saps:
        - sap_id: SAP-011
          actions: ["Create Dockerfile", "Add docker-compose"]
          hours: 5
        - sap_id: SAP-008
          actions: ["Add justfile", "Document commands"]
          hours: 3
      total_hours: 8
```

Claude (Phase 3: Integrate with Project Planning - 20-40k tokens):
5. Determine integration strategy:
   Option A: Update ECOSYSTEM_STATUS.yaml (if exists)
   Option B: Create sprint plans in docs/project-docs/sprints/
   Option C: Create coordination request in inbox/active/

6. For Option B (create sprint plans):
   - Read sprint template:
     Read docs/project-docs/templates/SPRINT_PLAN_TEMPLATE.md

   - Create Sprint 1 plan:
     Write docs/project-docs/sprints/sprint-005.md
     # Copy template, populate with SAP-004 + SAP-006 tasks

   - Create Sprint 2 plan:
     Write docs/project-docs/sprints/sprint-006.md
     # Copy template, populate with SAP-011 + SAP-008 tasks

Claude (Phase 4: Present to User - 40-50k tokens):
7. Summarize roadmap for user:

"## Q1 2026 SAP Adoption Roadmap

**Goal**: 80% coverage (24/30 SAPs), all core SAPs at Level 2+

### Sprint 1 (Weeks 1-2): Testing & Quality Foundation
- SAP-004: Coverage tracking + badge (3 hours)
- SAP-006: Quality gates + CI integration (4 hours)
- **Outcome**: Automated quality enforcement

### Sprint 2 (Weeks 3-4): Docker & Automation
- SAP-011: Containerize application (5 hours)
- SAP-008: Add automation scripts (3 hours)
- **Outcome**: One-command dev environment

### Sprint 3 (Weeks 5-6): Documentation & Awareness
- SAP-003: Add awareness files (3 hours)
- SAP-019: Add awareness files (3 hours)
- **Outcome**: Agent-friendly documentation

### Sprint 4 (Weeks 7-8): React Foundation
- SAP-020: React setup (4 hours)
- SAP-021: React testing (3 hours)
- **Outcome**: Modern frontend stack

**Total**: 4 sprints, 30 hours estimated

Roadmap saved to: `/tmp/sap-roadmap.yaml`
Sprint plans created: `sprint-005.md` through `sprint-008.md`

Should I create coordination requests for approval?"

Result: Quarterly roadmap integrated into project planning system
```

---

## Claude-Specific Tips

### Tip 1: Use Bash Tool for All Evaluation Commands

**Pattern**:
```bash
# ALWAYS use Bash tool to run sap-evaluator.py
Bash: python scripts/sap-evaluator.py --quick
Bash: python scripts/sap-evaluator.py --deep SAP-004
Bash: python scripts/batch-evaluate-saps.py --output /tmp/results.json

# DON'T try to evaluate manually - use the provided tools
```

**Why**: Evaluation logic is complex (LLM analysis, dependency checks, scoring) - delegating to tool ensures correct results.

---

### Tip 2: Use Read Tool to Analyze Evaluation Outputs

**Pattern**:
```bash
# If evaluation writes to file (--output flag):
Read /tmp/sap-roadmap.yaml
Read /tmp/sap-eval-results.json

# Parse YAML/JSON in memory, extract key metrics
```

**Why**: Evaluation outputs are structured (YAML/JSON) - Read tool provides full content for analysis.

---

### Tip 3: Use Edit Tool to Update Ledgers with Findings

**Pattern**:
```bash
# After running deep dive on SAP-011:
Read docs/skilled-awareness/docker-operations/ledger.md

# Add evaluation results to changelog
Edit docs/skilled-awareness/docker-operations/ledger.md
# old_string: ## 12. Changelog\n\n(empty)
# new_string: ## 12. Changelog\n\n### 2025-11-04 - Deep Dive Evaluation\n\n**Gaps Identified**:\n- Missing CI integration (P1, 2 hours)\n- Image size > 500MB (P2, 1 hour)\n\n**Actions Taken**:\n- Added buildx cache to CI (resolved P1)\n```

**Why**: Ledgers track SAP evolution over time - documenting evaluation results creates historical record.

---

### Tip 4: Use Glob Tool to Find SAPs Needing Evaluation

**Pattern**:
```bash
# Find all SAP directories without awareness files:
Glob docs/skilled-awareness/*/

# For each directory, check:
# - Does AGENTS.md exist?
# - Does CLAUDE.md exist?
# - If both missing → add to evaluation priority list
```

**Why**: Systematic discovery of SAPs needing attention - Glob is faster than manual ls.

---

### Tip 5: Batch Evaluation for Comprehensive Analysis

**Pattern**:
```bash
# When user asks "evaluate everything":
Bash: python scripts/batch-evaluate-saps.py --output /tmp/batch-results.json

# Then read results:
Read /tmp/batch-results.json

# Parse JSON for summary:
# - total_gaps, p1_gaps, p2_gaps
# - awareness_coverage (both_files, neither, etc.)
# - strategic priorities
```

**Why**: Batch script handles iteration, aggregation, and prioritization - Claude focuses on analysis and presentation.

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Using Bash Tool for Evaluation

**Problem**: Trying to implement evaluation logic manually instead of using `sap-evaluator.py`.

**Fix**: ALWAYS delegate to evaluation tool:

```bash
# BAD: Try to evaluate manually
Read docs/skilled-awareness/testing-framework/protocol-spec.md
# Try to parse and score manually ❌

# GOOD: Use evaluation tool
Bash: python scripts/sap-evaluator.py --deep SAP-004 ✅
# Parse structured output
```

**Why**: Evaluation tool encapsulates complex logic (LLM analysis, dependency resolution, scoring algorithms) - manual implementation is error-prone.

---

### Pitfall 2: Not Reading Evaluation Output Before Responding

**Problem**: Running evaluation but not reading the output before presenting to user.

**Fix**: ALWAYS capture and analyze Bash output:

```bash
# Run evaluation
Bash: python scripts/sap-evaluator.py --deep SAP-004

# Output is returned immediately - parse it for:
# - Current level
# - Gap list (priority, impact, effort)
# - Validation commands

# Then present structured summary to user
```

**Why**: Evaluation output contains all the data needed - skipping Read step means losing critical information.

---

### Pitfall 3: Not Updating Ledgers After Evaluation

**Problem**: Running deep dive but not documenting findings in SAP ledger.

**Fix**: After every deep dive, update ledger:

```bash
# After: Bash: python scripts/sap-evaluator.py --deep SAP-011

# Read current ledger:
Read docs/skilled-awareness/docker-operations/ledger.md

# Add evaluation results:
Edit docs/skilled-awareness/docker-operations/ledger.md
# Add section: "### YYYY-MM-DD - Evaluation Results"
# List gaps, actions, resolution status
```

**Why**: Ledgers are the historical record - evaluation findings should be preserved for future reference.

---

### Pitfall 4: Running Strategic Analysis Too Frequently

**Problem**: Running `--strategic` flag on every evaluation (30 minute runtime, heavy analysis).

**Fix**: Use appropriate evaluation mode:

```bash
# Quick status (30 seconds):
Bash: python scripts/sap-evaluator.py --quick

# Detailed gap analysis (5 minutes):
Bash: python scripts/sap-evaluator.py --deep SAP-004

# Quarterly roadmap (30 minutes):
Bash: python scripts/sap-evaluator.py --strategic --output roadmap.yaml
# Only run at start of quarter or major milestone
```

**Why**: Strategic analysis is expensive (evaluates all SAPs, analyzes dependencies) - reserve for quarterly planning.

---

### Pitfall 5: Not Validating Gap Fixes

**Problem**: Implementing gap fix but not running validation command to verify.

**Fix**: Every gap has validation command - always run it:

```bash
# Gap from evaluation:
# "Coverage tracking not enabled"
# Validation: pytest --cov=src --cov-report=term

# After implementing fix (pip install pytest-cov, configure pyproject.toml):
Bash: pytest --cov=src --cov-report=term

# Verify: Should see coverage report ✅
# If fails: Fix is incomplete, investigate further
```

**Why**: Validation commands are the acceptance criteria - gap isn't resolved until validation passes.

---

## Support & Resources

**SAP-019 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic self-evaluation workflows (5 workflows, user signal patterns)
- [Capability Charter](capability-charter.md) - Problem statement, impact analysis
- [Protocol Spec](protocol-spec.md) - Evaluation algorithms, data models, APIs
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking, version history

**Scripts**:
- [sap-evaluator.py](../../../scripts/sap-evaluator.py) - CLI tool (use via Bash)
- [batch-evaluate-saps.py](../../../scripts/batch-evaluate-saps.py) - Batch evaluation
- [sap_evaluation.py](../../../utils/sap_evaluation.py) - Core engine (Python import)
- [awareness_validation.py](../../../utils/awareness_validation.py) - AGENTS.md/CLAUDE.md validator

**Related SAPs**:
- [SAP-009 (agent-awareness)](../agent-awareness/) - Awareness file protocol (YAML frontmatter, progressive loading)
- [SAP-013 (metrics-framework)](../metrics-framework/) - Metrics collection and analysis
- [SAP-029 (sap-generation)](../sap-generation/) - SAP generation from prompts

**External Resources**:
- [YAML Specification](https://yaml.org/spec/1.2/spec.html) - For parsing roadmap.yaml
- [JSON Schema](https://json-schema.org/) - For validation of evaluation outputs

---

## Version History

- **1.0.0** (2025-11-04): Initial CLAUDE.md for SAP-019
  - 3 Claude Code workflows (Quick Check, Deep Dive, Strategic Roadmap)
  - Tool usage patterns (Bash for evaluation, Read for outputs, Edit for ledgers, Glob for discovery)
  - 5 Claude-specific tips (Bash for evaluation, Read outputs, Edit ledgers, Glob for SAPs, batch for comprehensive)
  - 5 common pitfalls (manual evaluation, skip Read, skip ledger updates, excessive strategic, skip validation)
  - Integration with AGENTS.md, SAP-009, SAP-013, SAP-029

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic self-evaluation workflows and best practices
2. Review [protocol-spec.md](protocol-spec.md) for evaluation algorithms and data structures
3. Try Workflow 1: Run quick check to assess current SAP adoption
4. Try Workflow 2: Deep dive on SAP-019 to dogfood self-evaluation capability
