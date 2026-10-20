## 📖 Quick Reference

**New to SAP-027?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - Week -1: Pre-pilot discovery (select candidate from intention inventory)
- 📚 **Time Savings** - 6 weeks upfront validation → avoid 20-30 hours rework later, data-driven GO/NO-GO decisions
- 🎯 **Feature 1** - Structured phases (Research → Build → Validate → Decide → Formalize)
- 🔧 **Feature 2** - Objective decision framework (time ≥5x, satisfaction ≥85%, bugs = 0, adoption ≥2)
- 📊 **Feature 3** - ≥30% Level A citations (standards, peer-reviewed papers)
- 🔗 **Integration** - Works with SAP-000 (Framework)

This AGENTS.md provides: Agent-specific patterns for implementing SAP-027.
s.

---

# Dogfooding Patterns (SAP-027) - Agent Awareness

**SAP ID**: SAP-027
**Version**: 1.0.0
**Status**: Production
**Last Updated**: 2025-11-04

---

## Quick Reference

### What is Dogfooding?

**Dogfooding** = Testing patterns/capabilities through internal use before recommending to ecosystem

SAP-027 provides a formalized **6-week pilot methodology** for validating patterns with:
- 4-phase design (research, build, validate, decide)
- Week 0 research phase using evidence-based research prompt template
- GO/NO-GO criteria (time savings, satisfaction, bugs, adoption)
- ROI analysis with break-even calculation
- Metrics templates and pilot documentation structure

### When to Use Dogfooding

✅ **Use SAP-027 for**:
- New SAP validation before ecosystem recommendation
- Pattern/workflow validation (e.g., "Should we adopt X tool?")
- Efficiency claim verification (e.g., "Tool Y saves 5x time - true?")
- Breaking changes risk assessment

❌ **Don't use for**:
- One-off experiments (too structured for ad-hoc testing)
- Already-validated patterns (SAP-027 is for NEW patterns)
- Quick prototypes (5-week commitment required)

---

## Common Workflows

### Workflow 1: Launching Dogfooding Pilot

**Steps**:
0. Research phase (Week 0): Evidence gathering before building
1. Define hypothesis (e.g., "SAP generation templates save 80% time")
2. Set GO/NO-GO criteria (time savings ≥5x, satisfaction ≥85%, bugs = 0)
3. Build capability (Weeks 1-3)
4. Validate through dogfooding (Week 4)
5. GO/NO-GO decision (Week 4 end)
6. Formalize if GO (Week 5)

**Example (SAP-029 pilot with research)**:
```markdown
Week 0: Research SAP generation best practices
  - Topic: "Template automation for code generation, ROI patterns, anti-patterns"
  - Output: docs/research/sap-generation-research.md (15 pages)
  - Extract: Template patterns (Level A: Yeoman docs), ROI models (Level B: GitHub case studies)

Week 1-3: Build SAP generation templates
  - Use research insights for template structure
  - Cite research decision playbooks for integration patterns

Week 4: Generate 2 SAPs (SAP-029, SAP-028)
  - Metrics: 120x time savings (vs 5x target)
  - Satisfaction: 5/5 (100%)
  - Bugs: 0 critical

Week 4 end: GO decision (24x over target)
Week 5: Formalize as SAP-029
```

**Outcome**: SAP-029 validated, recommended to ecosystem

---

### Workflow 2: Week 0 Research Phase

**Purpose**: Gather evidence-based insights before building capability

**Steps**:
1. Fill research prompt template with SAP domain context
   - Organization/team: "Open-source framework, 1 core maintainer"
   - Domain: "SAP capability domain" (e.g., "database migrations for Python")
   - Tech stack: Relevant technologies
   - Constraints: Open-source, budget, compliance
   - Time horizon: 6-12 months

2. Execute research prompt
   - Use Claude Code WebSearch/WebFetch tools
   - Or: `just research "{topic}"`
   - Time: 15-30 minutes research execution

3. Review research output
   - Validate evidence levels: Level A ≥30%, Level B ≥40%, Level C ≤30%
   - Extract principles for capability charter
   - Extract decision playbooks for protocol spec
   - Extract anti-patterns for awareness guide

4. Save research report
   - Location: `docs/research/{sap-name}-research.md`
   - Cite in Week 1-3 build phase design decisions

**Example (SAP-030 database-migrations research)**:
```bash
# Step 1: Fill template parameters
just research "database migration best practices for Python projects"

# Step 2: Execute (15-30min)
# Claude Code WebSearch generates 15-page report

# Step 3: Review output
# - Level A: 35% (Flyway docs, Alembic specs, PEP standards)
# - Level B: 45% (Netflix case studies, Stripe postmortems)
# - Level C: 20% (Expert blogs)
# ✅ Evidence levels valid

# Step 4: Extract insights
# Principles → capability-charter.md Section 1 (Problem Statement)
#   - "Rollback strategies critical for production safety (Level A: Flyway docs)"
#   - "State tracking prevents drift (Level B: Netflix case study)"
#
# Decision playbooks → protocol-spec.md Section 5 (Integration)
#   - "Choose SQL-based migrations when: team SQL expertise high, schema complex"
#   - "Choose ORM migrations when: rapid prototyping, simple schema"
#
# Anti-patterns → awareness-guide.md Section 5 (Error Patterns)
#   - "Don't run migrations without rollback plan (causes downtime)"
#   - "Don't skip migration testing (causes data loss)"

# Step 5: Use in Week 1-3 build
# Build SAP-030 with research-backed design decisions
```

**Outcome**: Week 1-3 build phase informed by evidence (reduces pilot failure risk)

---

### Workflow 3: Collecting Dogfooding Metrics

**Steps**:
1. Track time: Setup time vs per-use time
2. Measure satisfaction: 1-5 rating after each use
3. Log bugs: Critical vs non-critical
4. Count adoption cases: ≥2 required for GO
5. Calculate ROI: Break-even point = setup / (per-use savings)

**Metrics Template**:
```markdown
## Dogfooding Metrics (Week 4)

**Time Tracking**:
- Setup time: X hours
- Per-use time: Y minutes
- Baseline time: Z hours
- Time savings: (Z - Y/60) / Y * 100 = W%
- Target: ≥5x (500%)

**Satisfaction**:
- Use 1: 5/5
- Use 2: 4/5
- Average: 4.5/5 (90%)
- Target: ≥85%

**Quality**:
- Critical bugs: 0
- Non-critical bugs: 2
- Target: 0 critical

**Adoption**:
- Case 1: SAP-029 generation
- Case 2: SAP-028 generation
- Total: 2 cases
- Target: ≥2

**GO/NO-GO**: ✅ GO (all criteria met)
```

---

### Workflow 4: Making GO/NO-GO Decision

**Steps**:
1. Review metrics at Week 4 end
2. Check each GO criterion:
   - Time savings ≥5x? (500%+)
   - Satisfaction ≥85%?
   - Critical bugs = 0?
   - Adoption cases ≥2?
3. If all YES → GO (proceed to formalization)
4. If any NO → NO-GO (document learnings, deprecate)

**Decision Matrix**:
```markdown
| Criterion | Target | Actual | Met? |
|-----------|--------|--------|------|
| Time savings | ≥5x (500%) | 120x (12000%) | ✅ |
| Satisfaction | ≥85% | 100% (5/5) | ✅ |
| Critical bugs | 0 | 0 | ✅ |
| Adoption cases | ≥2 | 2 (SAP-029, SAP-028) | ✅ |

**Decision**: ✅ GO (all criteria met, 24x over target)
```

---

### Workflow 5: Formalizing After GO Decision

**Steps**:
1. Complete TODOs in protocol-spec.md (P0/P1 priority)
2. Fill adoption tracking in ledger.md
3. Document pilot metrics and results
4. Update status: pilot → production
5. Announce to ecosystem (if applicable)

**Example (SAP-029 formalization)**:
```markdown
Week 5 tasks:
- ✅ Complete protocol-spec TODOs
- ✅ Fill ledger adoption tracking
- ✅ Document 120x time savings in capability-charter
- ✅ Update status: pilot → production
- ✅ Add to chora-base v4.2.0 release notes
```

---

## GO/NO-GO Criteria

### Criterion 1: Time Savings ≥5x (500%)

**Definition**: Pattern saves ≥5x time vs baseline approach

**Measurement**:
```
Time savings = (Baseline time - New time) / New time * 100
Example: (10 hours - 5 minutes) / (5 minutes / 60) * 100 = 11900%
```

**Why 5x?**: Below 5x, setup cost may not justify adoption

---

### Criterion 2: Satisfaction ≥85%

**Definition**: Average satisfaction rating ≥4.25/5 across all uses

**Measurement**:
```
Satisfaction = (Σ ratings) / (# of ratings)
Example: (5 + 5 + 4 + 4) / 4 = 4.5/5 = 90%
```

**Why 85%?**: Ensures positive developer experience, encourages adoption

---

### Criterion 3: Critical Bugs = 0

**Definition**: Zero bugs that block core functionality

**Measurement**:
- Critical: Blocks core use case, no workaround
- Non-critical: Minor issues, workarounds available

**Why 0?**: Critical bugs erode ecosystem trust, delay adoption

---

### Criterion 4: Adoption Cases ≥2

**Definition**: Pattern used successfully in ≥2 distinct cases

**Measurement**:
- Case = distinct use of pattern (e.g., generating different SAPs)
- Must be successful (not failed attempts)

**Why 2?**: Single case may be fluke, ≥2 demonstrates repeatability

---

## ROI Analysis

### Break-Even Calculation

**Formula**:
```
Break-even = Setup time / Per-use savings

Example (SAP-029):
- Setup time: 10 hours
- Baseline time: 10 hours/SAP
- New time: 5 minutes/SAP = 0.083 hours/SAP
- Per-use savings: 10 - 0.083 = 9.917 hours
- Break-even: 10 / 9.917 = 1.01 uses

After 2 uses: ROI = 2 * 9.917 - 10 = 9.834 hours saved
```

**Interpretation**:
- Break-even < 2 uses: Excellent ROI (GO)
- Break-even 2-5 uses: Good ROI (GO if other criteria met)
- Break-even > 5 uses: Poor ROI (NO-GO unless strategic value)

---

## Integration with Other SAPs

### Integration with SAP-029 (SAP Generation)

**Pattern**: SAP-027 validates SAP-029's effectiveness

**Workflow**:
1. SAP-029 pilot: Use templates to generate SAPs
2. Measure time savings (120x actual vs 5x target)
3. Collect satisfaction (5/5 rating)
4. Count adoption cases (2 SAPs generated)
5. GO decision: Formalize SAP-029

**Outcome**: SAP-029 validated via SAP-027 methodology

---

### Integration with SAP-000 (SAP Framework)

**Pattern**: SAP-027 defines how to validate new SAPs

**Workflow**:
1. New SAP proposed
2. Apply SAP-027 methodology (5-week pilot)
3. Collect metrics (time, satisfaction, bugs, adoption)
4. GO/NO-GO decision
5. If GO: Add to SAP catalog, recommend to ecosystem

**Outcome**: All new SAPs validated before ecosystem recommendation

---

## Pilot Documentation Structure

### Weekly Metrics Template

```markdown
# Dogfooding Pilot: [Pattern Name]

## Week 1-3: Build Phase
- **Goal**: Build capability to minimum viable state
- **Status**: [In Progress / Complete]
- **Blockers**: [None / List blockers]

## Week 4: Validation Phase
- **Use 1**: [Date, description, time, satisfaction]
- **Use 2**: [Date, description, time, satisfaction]
- **Metrics Summary**: [Time savings, satisfaction, bugs, adoption]

## Week 4 End: GO/NO-GO Decision
- **Time savings**: Actual vs target
- **Satisfaction**: Actual vs target
- **Critical bugs**: Actual vs target
- **Adoption cases**: Actual vs target
- **Decision**: GO / NO-GO
- **Rationale**: [Why]

## Week 5: Formalization (if GO)
- **TODOs completed**: [List]
- **Ledger updated**: [Yes/No]
- **Status change**: pilot → production
- **Announcement**: [Link to release notes / ecosystem notification]
```

---

### Final Summary Template

```markdown
# Dogfooding Pilot Summary: [Pattern Name]

## Overview
- **Pattern**: [Name and description]
- **Hypothesis**: [What you wanted to validate]
- **Timeline**: [Start date] - [End date] (5 weeks)
- **Outcome**: GO / NO-GO

## Metrics
| Criterion | Target | Actual | Met? |
|-----------|--------|--------|------|
| Time savings | ≥5x | [X]x | ✅/❌ |
| Satisfaction | ≥85% | [Y]% | ✅/❌ |
| Critical bugs | 0 | [Z] | ✅/❌ |
| Adoption cases | ≥2 | [N] | ✅/❌ |

## ROI Analysis
- **Setup time**: X hours
- **Per-use savings**: Y hours
- **Break-even**: Z uses
- **Actual uses**: N
- **Net savings**: (N * Y) - X = W hours

## Learnings
- **What worked well**: [List]
- **What didn't work**: [List]
- **Improvements for next pilot**: [List]

## Recommendation
- **Decision**: GO / NO-GO
- **Rationale**: [Why]
- **Next steps**: [If GO: formalization tasks / If NO-GO: deprecation plan]
```

---

## Troubleshooting

### Issue: Metrics don't meet GO criteria

**Solution**:
1. Identify which criterion failed
2. If close to target (e.g., 4.5x vs 5x): Consider strategic value, extend pilot 1 week
3. If far from target (e.g., 2x vs 5x): NO-GO, document learnings
4. Document rationale in ledger, deprecate if NO-GO

---

### Issue: Unclear if bug is critical

**Solution**:
- **Critical**: Blocks core use case, no workaround → Counts as critical bug
- **Non-critical**: Workaround available OR minor feature → Doesn't block GO
- **Example**: Template generates invalid syntax (critical) vs template formatting off (non-critical)

---

### Issue: Only 1 adoption case

**Solution**:
1. Find second use case (different context)
2. If no second use case available: Extend pilot 1 week
3. If still only 1 case: NO-GO (insufficient validation)
4. Document in ledger: "Pattern may be too narrow for ecosystem"

---

## Key Commands

```bash
# Start pilot
mkdir docs/project-docs/dogfooding-pilot/{pattern-name}
vim docs/project-docs/dogfooding-pilot/{pattern-name}/pilot-plan.md

# Track metrics weekly
vim docs/project-docs/dogfooding-pilot/{pattern-name}/week-{N}-metrics.md

# Make GO/NO-GO decision
vim docs/project-docs/dogfooding-pilot/{pattern-name}/go-no-go-decision.md

# Formalize (if GO)
vim docs/skilled-awareness/{sap-name}/protocol-spec.md  # Complete TODOs
vim docs/skilled-awareness/{sap-name}/ledger.md  # Add adoption tracking
vim docs/skilled-awareness/{sap-name}/capability-charter.md  # Add metrics

# Document summary
vim docs/project-docs/dogfooding-pilot/{pattern-name}/final-summary.md
```

---

## Support & Resources

**SAP-027 Documentation**:
- [Capability Charter](capability-charter.md) - Problem, solution, scope
- [Protocol Spec](protocol-spec.md) - Technical specification
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking and version history

**Example Pilots**:
- SAP-029 pilot (docs/project-docs/dogfooding-pilot/sap-generation/)
- SAP-028 pilot (docs/project-docs/dogfooding-pilot/publishing-automation/)

**Related SAPs**:
- [SAP-000 (sap-framework)](../sap-framework/) - Framework foundation
- [SAP-029 (sap-generation)](../sap-generation/) - Validated via SAP-027

**Templates**:
- Weekly metrics template (see above)
- Final summary template (see above)
- GO/NO-GO decision matrix (see above)

---

## Version History

- **1.0.0** (2025-11-04): Initial AGENTS.md for SAP-027
  - Common workflows (launch, metrics, GO/NO-GO, formalization)
  - GO/NO-GO criteria (time savings, satisfaction, bugs, adoption)
  - ROI analysis and break-even calculation
  - Pilot documentation structure
  - Integration with SAP-029 and SAP-000

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude-specific dogfooding patterns
2. Review [capability-charter.md](capability-charter.md) for design rationale
3. Check example pilots in docs/project-docs/dogfooding-pilot/
4. Start your first pilot using the templates above
