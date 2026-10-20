## 📖 Quick Reference

**New to SAP-027?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - Week -1: Pre-pilot discovery (select candidate from intention inventory)
- 📚 **Time Savings** - 6 weeks upfront validation → avoid 20-30 hours rework later, data-driven GO/NO-GO decisions
- 🎯 **Feature 1** - Structured phases (Research → Build → Validate → Decide → Formalize)
- 🔧 **Feature 2** - Objective decision framework (time ≥5x, satisfaction ≥85%, bugs = 0, adoption ≥2)
- 📊 **Feature 3** - ≥30% Level A citations (standards, peer-reviewed papers)
- 🔗 **Integration** - Works with SAP-000 (Framework)

This CLAUDE.md provides: Claude Code-specific workflows for implementing SAP-027.
s.

---

# Dogfooding Patterns (SAP-027) - Claude-Specific Awareness

**SAP ID**: SAP-027
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for running dogfooding pilots.

### First-Time Dogfooding

1. Read [AGENTS.md](AGENTS.md) for generic dogfooding workflows
2. Use this file for Claude Code tool integration
3. Follow 6-week pilot methodology (Week 0 research + 5-week pilot)

### Session Resumption

- Check pilot status in docs/project-docs/dogfooding-pilot/{pattern}/
- Read weekly metrics to understand current phase
- Use Claude Code tools for metrics collection and documentation

---

## Claude Code Dogfooding Workflows

### Workflow 1: Launching Pilot with Claude Code

```markdown
User: "Start dogfooding pilot for {new pattern}"

Claude (Phase 0: Research - Week 0):
1. Read docs/skilled-awareness/dogfooding-patterns/AGENTS.md
2. Execute research workflow:
   Bash: just research "{pattern-domain} best practices"
   # Uses WebSearch/WebFetch tools to generate research report
   # Time: 15-30 minutes
3. Review research output:
   Read docs/research/{pattern-domain}-research.md
   # Extract principles, decision playbooks, anti-patterns
4. Create pilot directory:
   Bash: mkdir -p docs/project-docs/dogfooding-pilot/{pattern-name}
5. Write pilot plan:
   Write docs/project-docs/dogfooding-pilot/{pattern-name}/pilot-plan.md
   # Content: Hypothesis, GO criteria, timeline, research insights

Claude (Phase 1: Setup - Week 0 continued):
6. Validate research evidence levels:
   # Check: Level A ≥30%, Level B ≥40%, Level C ≤30%
7. Extract research insights for build phase:
   # Cite research in design decision docs

Claude (Phase 2: Build - Weeks 1-3):
8. Build capability (Write/Edit tools)
9. Use research insights to inform design decisions
10. Track time spent (manual + note in metrics)

Claude (Phase 3: Validate - Week 4):
11. Use capability 2+ times
12. Collect metrics after each use:
   - Time tracking via Bash: time {command}
   - Satisfaction: Ask user for 1-5 rating
   - Log bugs: Write to metrics file
13. Write week-4-metrics.md with all data

Claude (Phase 4: Decision - Week 4 end):
14. Read week-4-metrics.md
15. Calculate: Time savings, satisfaction avg, bugs, adoption
16. Write go-no-go-decision.md with recommendation

Claude (Phase 5: Formalization - Week 5 if GO):
17. Edit protocol-spec.md (complete TODOs)
18. Edit ledger.md (add adoption tracking, cite research report)
19. Write final-summary.md
20. Commit changes

Result: Pattern validated and formalized (or deprecated if NO-GO)
```

---

### Workflow 2: Collecting Metrics with Claude Code

```markdown
User: "Use {pattern} for {task}"

Claude (Before use):
1. Note start time:
   Bash: date +%s > /tmp/dogfooding-start-time

Claude (During use):
2. Execute pattern/capability
3. Track any bugs encountered

Claude (After use):
4. Calculate elapsed time:
   Bash: echo "$(( $(date +%s) - $(cat /tmp/dogfooding-start-time) )) seconds"
5. Ask user for satisfaction rating (1-5)
6. Append to metrics file:
   Edit docs/project-docs/dogfooding-pilot/{pattern}/week-4-metrics.md
   # Add: Use {N}: Time={X}s, Satisfaction={Y}/5, Bugs={Z}

Result: Metrics captured for GO/NO-GO decision
```

---

### Workflow 3: Making GO/NO-GO Decision with Claude Code

```markdown
User: "Should we formalize {pattern}?" (Week 4 end)

Claude:
1. Read week-4-metrics.md:
   Read docs/project-docs/dogfooding-pilot/{pattern}/week-4-metrics.md
2. Calculate metrics:
   - Time savings = (baseline - new) / new * 100
   - Satisfaction avg = sum(ratings) / count(ratings)
   - Critical bugs count
   - Adoption cases count
3. Compare to GO criteria:
   | Criterion | Target | Actual | Met? |
   |-----------|--------|--------|------|
   | Time savings | ≥5x | {X}x | ✅/❌ |
   | Satisfaction | ≥85% | {Y}% | ✅/❌ |
   | Critical bugs | 0 | {Z} | ✅/❌ |
   | Adoption | ≥2 | {N} | ✅/❌ |
4. Write go-no-go-decision.md:
   Write docs/project-docs/dogfooding-pilot/{pattern}/go-no-go-decision.md
   # Content: Metrics table, decision (GO/NO-GO), rationale

Claude (response):
"✅ GO decision - All criteria met:
- Time savings: {X}x (target: ≥5x)
- Satisfaction: {Y}% (target: ≥85%)
- Critical bugs: 0 (target: 0)
- Adoption: {N} cases (target: ≥2)

Proceed with Week 5 formalization?"

Result: Clear GO/NO-GO decision with data-driven rationale
```

---

### Workflow 4: Formalizing Pattern (Week 5 if GO)

```markdown
User: "Formalize {pattern}" (after GO decision)

Claude:
1. Complete protocol-spec TODOs:
   Read docs/skilled-awareness/{sap-name}/protocol-spec.md
   Edit docs/skilled-awareness/{sap-name}/protocol-spec.md
   # Remove TODO comments, fill in actual specifications
2. Update ledger:
   Edit docs/skilled-awareness/{sap-name}/ledger.md
   # Add adoption tracking, metrics, version history
3. Update capability-charter (add metrics):
   Edit docs/skilled-awareness/{sap-name}/capability-charter.md
   # Add: "Evidence" section with pilot metrics
4. Write final summary:
   Write docs/project-docs/dogfooding-pilot/{pattern}/final-summary.md
   # Content: Overview, metrics, learnings, recommendation
5. Update status (if applicable):
   Edit docs/skilled-awareness/{sap-name}/capability-charter.md
   # Change: status: pilot → status: production
6. Commit:
   Bash: git add docs/
   Bash: git commit -m "feat({sap}): Formalize after dogfooding GO decision"

Result: Pattern formalized, production-ready
```

---

## Claude-Specific Tips

### Tip 1: Automate Time Tracking

**Pattern**:
```bash
# Before using pattern
echo "$(date +%s)" > /tmp/dogfooding-start

# After using pattern
echo "Elapsed: $(( $(date +%s) - $(cat /tmp/dogfooding-start) )) seconds"
```

**Why**: Accurate time tracking is critical for GO/NO-GO decision

---

### Tip 2: Prompt User for Satisfaction After Each Use

**Pattern**:
```markdown
Claude (after completing task with pattern):
"Task complete using {pattern}.

Please rate your satisfaction (1-5):
1 = Frustrating
2 = Problematic
3 = Acceptable
4 = Good
5 = Excellent

This helps determine if we should formalize {pattern}."
```

**Why**: Real-time satisfaction ratings are more accurate than retrospective

---

### Tip 3: Log Bugs Immediately

**Pattern**:
```markdown
Claude (when encountering bug):
"Bug encountered during {pattern} use:
- Description: {what happened}
- Severity: Critical (blocks use) / Non-critical (workaround available)
- Workaround: {if applicable}

Logging to metrics file..."

Edit docs/project-docs/dogfooding-pilot/{pattern}/week-4-metrics.md
# Add bug entry
```

**Why**: Immediate logging captures details before you forget

---

### Tip 4: Use Templates for Consistency

**Pattern**:
```bash
# On pilot start, copy templates
cp docs/skilled-awareness/dogfooding-patterns/templates/pilot-plan.md \
   docs/project-docs/dogfooding-pilot/{pattern}/

cp docs/skilled-awareness/dogfooding-patterns/templates/weekly-metrics.md \
   docs/project-docs/dogfooding-pilot/{pattern}/week-4-metrics.md

cp docs/skilled-awareness/dogfooding-patterns/templates/go-no-go-decision.md \
   docs/project-docs/dogfooding-pilot/{pattern}/
```

**Why**: Templates ensure all required data is collected

---

### Tip 5: Calculate ROI Automatically

**Pattern**:
```bash
# Calculate break-even
setup_time=10  # hours
per_use_savings=9.917  # hours
echo "Break-even: $(echo "scale=2; $setup_time / $per_use_savings" | bc) uses"

# Calculate net savings after N uses
uses=2
echo "Net savings after $uses uses: $(echo "scale=2; ($uses * $per_use_savings) - $setup_time" | bc) hours"
```

**Why**: Quantified ROI makes GO/NO-GO decision objective

---

## Common Pitfalls for Claude

### Pitfall 1: Not Using Pattern Enough (< 2 Cases)

**Problem**: Only 1 adoption case, can't meet ≥2 criterion

**Fix**:
```markdown
Claude (Week 4):
"Only 1 adoption case so far. Finding second use case...

Potential second case: {alternative use}

Attempting now to reach ≥2 adoption cases for GO decision."
```

---

### Pitfall 2: Forgetting to Track Time

**Problem**: No time data collected, can't calculate savings

**Fix**:
```bash
# Always start timer before pattern use
date +%s > /tmp/dogfooding-start

# Always calculate elapsed time after
echo "$(( $(date +%s) - $(cat /tmp/dogfooding-start) )) seconds" | \
  tee -a docs/project-docs/dogfooding-pilot/{pattern}/time-log.txt
```

---

### Pitfall 3: Classifying Non-Critical Bug as Critical

**Problem**: Minor formatting issue blocks GO decision

**Fix**:
```markdown
# Decision tree for bug severity
Is core functionality blocked? NO → Non-critical
Is there a workaround? YES → Non-critical
Does it prevent pattern use? NO → Non-critical

# Only mark as critical if:
- Core use case broken AND
- No workaround available
```

---

### Pitfall 4: Not Documenting GO Rationale

**Problem**: GO decision made but not explained

**Fix**:
```markdown
Claude (in go-no-go-decision.md):
"✅ GO Decision

**Rationale**:
- Time savings 24x over target (12000% vs 500% target)
- Perfect satisfaction (100% vs 85% target)
- Zero critical bugs (met requirement)
- 2 distinct adoption cases (met requirement)
- Break-even after 1.01 uses, already at 2 uses (9.8h net savings)

**Confidence**: 100% (exceeded all targets)

**Proceed to formalization**: Week 5"
```

---

### Pitfall 5: Skipping Final Summary

**Problem**: Pilot complete but learnings not captured

**Fix**:
```bash
# Always write final summary (even if NO-GO)
Write docs/project-docs/dogfooding-pilot/{pattern}/final-summary.md
# Content: Metrics, decision, learnings, next steps
```

---

## Example Claude Code Session (Full Pilot)

```markdown
User: "Let's dogfood SAP generation templates"

Claude (Week 0: Setup):
1. mkdir -p docs/project-docs/dogfooding-pilot/sap-generation
2. Write pilot-plan.md:
   - Hypothesis: Templates save 80% time
   - GO criteria: ≥5x savings, ≥85% satisfaction, 0 critical bugs, ≥2 cases
   - Timeline: Weeks 1-5 (Nov 1-Dec 5)

Claude (Weeks 1-3: Build):
3. Build SAP generation templates
4. Track setup time: 10 hours

Claude (Week 4: Validate):
5. Use 1: Generate SAP-029
   - time sap-generate → 5 minutes
   - Satisfaction: 5/5
   - Bugs: 0 critical
6. Use 2: Generate SAP-028
   - time sap-generate → 5 minutes
   - Satisfaction: 5/5
   - Bugs: 0 critical
7. Write week-4-metrics.md:
   - Time savings: (10h - 5min) / 5min * 100 = 11900% (119x)
   - Satisfaction: (5+5)/2 = 5/5 (100%)
   - Critical bugs: 0
   - Adoption: 2 cases

Claude (Week 4 end: Decision):
8. Read week-4-metrics.md
9. Calculate: 119x vs 5x target (24x over)
10. Write go-no-go-decision.md: ✅ GO

Claude (Week 5: Formalization):
11. Edit docs/skilled-awareness/sap-generation/protocol-spec.md (remove TODOs)
12. Edit docs/skilled-awareness/sap-generation/ledger.md (add metrics)
13. Write final-summary.md
14. git commit -m "feat(sap-029): Formalize after dogfooding GO decision (119x time savings)"

Result: SAP-029 validated and formalized
Time: 5 weeks (3 build + 1 validate + 1 formalize)
Outcome: Production-ready, 119x time savings proven
```

---

## Tool Usage Patterns

### Using Bash Tool for Metrics

```bash
# Time tracking
date +%s > /tmp/start
# ... do work ...
echo "$(( $(date +%s) - $(cat /tmp/start) ))s" >> metrics.txt

# ROI calculation
echo "scale=2; 10 / 9.917" | bc  # Break-even

# Counting adoption cases
grep -c "Use [0-9]:" week-4-metrics.md  # Count uses
```

---

### Using Write Tool for Documentation

```bash
# Pilot plan
Write docs/project-docs/dogfooding-pilot/{pattern}/pilot-plan.md

# Weekly metrics
Write docs/project-docs/dogfooding-pilot/{pattern}/week-4-metrics.md

# GO/NO-GO decision
Write docs/project-docs/dogfooding-pilot/{pattern}/go-no-go-decision.md

# Final summary
Write docs/project-docs/dogfooding-pilot/{pattern}/final-summary.md
```

---

### Using Edit Tool for Formalization

```bash
# Complete TODOs
Edit docs/skilled-awareness/{sap}/protocol-spec.md
# old_string: "<!-- TODO: ... -->"
# new_string: "{actual content}"

# Update ledger
Edit docs/skilled-awareness/{sap}/ledger.md
# Add adoption tracking, metrics

# Update status
Edit docs/skilled-awareness/{sap}/capability-charter.md
# old_string: "status: pilot"
# new_string: "status: production"
```

---

## Support & Resources

**SAP-027 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic dogfooding workflows
- [Capability Charter](capability-charter.md) - Problem and solution
- [Protocol Spec](protocol-spec.md) - Technical specification
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking

**Example Pilots**:
- docs/project-docs/dogfooding-pilot/sap-generation/ (SAP-029, 119x savings)
- docs/project-docs/dogfooding-pilot/publishing-automation/ (SAP-028)

**Templates** (in AGENTS.md):
- Pilot plan template
- Weekly metrics template
- GO/NO-GO decision template
- Final summary template

**Related SAPs**:
- [SAP-000 (sap-framework)](../sap-framework/) - Framework foundation
- [SAP-029 (sap-generation)](../sap-generation/) - Validated via SAP-027

---

## Version History

- **1.0.0** (2025-11-04): Initial CLAUDE.md for SAP-027
  - Claude Code dogfooding workflows
  - Tool usage patterns (Bash, Write, Edit)
  - Automated metrics collection
  - Common pitfalls and tips
  - Example full pilot session (SAP-029)

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic workflows
2. Start pilot: mkdir docs/project-docs/dogfooding-pilot/{pattern}/
3. Use templates for consistency
4. Automate time tracking with Bash
5. Document GO/NO-GO decision with data
