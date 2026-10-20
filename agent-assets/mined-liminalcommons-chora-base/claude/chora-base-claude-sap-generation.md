# SAP Generation Automation (SAP-029) - Claude-Specific Awareness

**SAP ID**: SAP-029
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

---

## 📖 Quick Reference

**New to SAP-029?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - Step 1: Add SAP to catalog (sap-catalog.json)
- 📚 **Time Savings** - 70-80% SAP creation time reduction (1-2 hours vs 8-10 hours manual)
- 🎯 **Feature 1** - 10 hours → 2 hours (automated boilerplate + focused manual fill)
- 🔧 **Feature 2** - 5 templates for 5 artifacts (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger)
- 📊 **Feature 3** - 9 fields capture essential metadata (problem, solution, principles, scope, summary)
- 🔗 **Integration** - Works with SAP-000, SAP-004, SAP-005, SAP-007, SAP-016, SAP-027

This CLAUDE.md provides: Claude Code-specific workflows for implementing SAP-029.
s.

---

## Claude Code SAP Generation Workflows

### Workflow 1: Generating a New SAP with Claude Code

```markdown
User: "Create SAP-030 for database migrations"

Claude (Phase 0: Research - 0-5k tokens):
1. Execute research workflow:
   Bash: just research "database migration best practices for Python projects"
   # Uses WebSearch to generate research report (15-30min)
2. Read research output:
   Read: docs/research/database-migrations-research.md
   # Extract principles, anti-patterns, decision playbooks
3. Synthesize research for SAP metadata:
   # Problem ← anti-patterns section
   # Evidence ← case studies, metrics
   # Solution ← decision playbooks
   # Principles ← Level A evidence
   # In-scope/out-scope ← trade-off tables

Claude (Phase 1: Metadata - 5-10k tokens):
4. Read sap-catalog.json (understand schema)
5. Draft SAP-030 metadata (9 MVP fields, informed by research):
   {
     "id": "SAP-030",
     "name": "database-migrations",
     "owner": "Victor",
     "created_date": "2025-11-04",
     "problem": "No standardized approach to database schema evolution across environments",
     "evidence": ["Manual migrations prone to human error", "20+ migration files without clear structure", "Production incidents due to missing rollback plans"],
     "impact": "Development velocity reduced by 30%, production deployment risk, inconsistent database state across environments",
     "solution": "Standardized migration framework with version control, rollback support, and automated state tracking",
     "principles": ["Version-controlled migrations", "Rollback safety guarantees", "Automated state tracking", "Environment parity"],
     "in_scope": ["Migration file templates", "Rollback scripts", "State validation tools", "CLI commands"],
     "out_of_scope": ["ORM-specific migrations", "Multi-database vendor support", "Schema diffing tools"],
     "one_sentence_summary": "Standardized database migration framework with rollback support and state tracking"
   }
6. Edit sap-catalog.json to add SAP-030 entry

Claude (Phase 2: Generation - 10-15k tokens):
7. Run generation via Bash tool:
   Bash: python scripts/generate-sap.py SAP-030
8. Verify output:
   ✅ 5 artifacts created
   ✅ INDEX.md updated

Claude (Phase 3: Review - 15-25k tokens):
9. Read generated capability-charter.md
10. Identify TODO comments (15-20 per artifact)
11. Create plan: Fill critical TODOs (Core Contracts in protocol-spec.md, Level 1 adoption in adoption-blueprint.md)
12. Cite research report in capability-charter.md evidence section

Claude (Phase 4: Fill Content - 25-55k tokens):
13. Edit protocol-spec.md:
   - Fill Core Contracts section (migration file format, CLI API)
   - Use research decision playbooks for integration patterns
14. Edit adoption-blueprint.md:
    - Fill Level 1 installation steps (install CLI, create first migration)
15. Edit awareness-guide.md:
    - Add common workflows (create migration, run migration, rollback)
    - Include anti-patterns from research

Claude (Phase 5: Validation - 55-60k tokens):
16. Run validation via Bash tool:
    Bash: python scripts/sap-evaluator.py SAP-030
17. Fix any validation errors (broken links, missing sections)
18. Re-validate until PASS

Claude (response to user):
"I've created SAP-030 (database-migrations) with 5 artifacts:

✅ capability-charter.md - Problem, solution, scope defined
✅ protocol-spec.md - Core contracts filled (migration format, CLI API)
✅ awareness-guide.md - Common workflows added
✅ adoption-blueprint.md - Level 1 installation complete
✅ ledger.md - Adoption tracking baseline

⏳ TODOs remaining: 8 (Level 2/3 adoption, advanced integration patterns)

Validation: PASS (all 5 artifacts present, structure valid)

Total time: ~2 hours (vs 10 hours manual)"

Result: SAP-030 generated, 80% complete, validated
```

---

### Workflow 2: Filling Generated TODOs with Claude Code

```markdown
User: "Fill remaining TODOs in SAP-030"

Claude (Phase 1: Scan - 0-5k tokens):
1. Grep for TODO comments across all 5 artifacts:
   Bash: grep -r "<!-- TODO:" docs/skilled-awareness/database-migrations/
2. Identify 8 TODOs:
   - protocol-spec.md: 3 TODOs (Integration Patterns, Configuration, Error Handling)
   - adoption-blueprint.md: 3 TODOs (Level 2, Level 3, Troubleshooting)
   - ledger.md: 2 TODOs (Performance Metrics, Stakeholder Feedback)

Claude (Phase 2: Fill TODOs - 5-30k tokens):
3. Edit protocol-spec.md (Integration Patterns section):
   Read protocol-spec.md
   Edit protocol-spec.md
   # old_string: "<!-- TODO: Describe how this SAP integrates with other SAPs -->"
   # new_string: Actual integration patterns (SAP-011 docker-operations, SAP-004 testing)

4. Edit adoption-blueprint.md (Level 2 section):
   Read adoption-blueprint.md
   Edit adoption-blueprint.md
   # Fill Level 2 adoption steps (multi-environment setup, CI/CD integration)

5. Edit ledger.md (Performance Metrics section):
   Read ledger.md
   Edit ledger.md
   # Add baseline metrics (migration time, rollback success rate)

Claude (Phase 3: Validate - 30-35k tokens):
6. Bash: python scripts/sap-evaluator.py SAP-030
7. Verify no TODOs remaining:
   Bash: grep -r "<!-- TODO:" docs/skilled-awareness/database-migrations/ | wc -l
   # Output: 0 (all TODOs filled)

Claude (response):
"All 8 TODOs filled in SAP-030:

✅ protocol-spec.md: Integration patterns + configuration + error handling
✅ adoption-blueprint.md: Level 2/3 adoption steps + troubleshooting
✅ ledger.md: Performance metrics + stakeholder feedback baseline

Validation: PASS (no TODOs remaining, structure valid)

SAP-030 is now 100% complete and ready for commit."

Result: SAP-030 fully complete, no TODOs, validated
```

---

### Workflow 3: Validating Generated SAP with Claude Code

```markdown
User: "Validate SAP-030"

Claude:
1. Run validation via Bash tool:
   Bash: python scripts/sap-evaluator.py SAP-030

2. Parse validation output:
   ✅ Artifacts: 5/5 present
   ✅ Structure: All required sections found
   ⚠️  Links: 2 broken links found:
       - capability-charter.md:335 → ../docker-operations/ (404)
       - protocol-spec.md:89 → ../testing-framework/ (404)
   ✅ TODOs: 0 remaining

   Overall: FAIL (broken links)

3. Fix broken links:
   Read capability-charter.md (line 335)
   Edit capability-charter.md
   # old_string: "../docker-operations/"
   # new_string: "../docker-operations-sap/" (correct directory name)

   Read protocol-spec.md (line 89)
   Edit protocol-spec.md
   # old_string: "../testing-framework/"
   # new_string: "../testing-framework-sap/"

4. Re-validate:
   Bash: python scripts/sap-evaluator.py SAP-030
   ✅ All checks passed (5/5 artifacts, structure valid, 12/12 links valid, 0 TODOs)

Claude (response):
"SAP-030 validation complete:

✅ Fixed 2 broken links (docker-operations, testing-framework)
✅ All 5 artifacts present and valid
✅ All 12 internal links working
✅ No TODOs remaining

SAP-030 is production-ready."

Result: SAP-030 validated, ready for commit
```

---

### Workflow 4: Extending Generation Schema with Claude Code

```markdown
User: "Add 'risks' field to SAP generation schema"

Claude (Phase 1: Extend Schema - 0-10k tokens):
1. Read sap-catalog.json (understand current schema)
2. Read docs/skilled-awareness/templates/capability-charter.jinja2 (current template)
3. Draft schema extension:
   - Add "risks" array to sap-catalog.json schema
   - Each risk: {name, likelihood, impact, mitigation}

Claude (Phase 2: Update Template - 10-20k tokens):
4. Edit docs/skilled-awareness/templates/capability-charter.jinja2:
   Read capability-charter.jinja2 (section 8: Risks & Mitigations)
   Edit capability-charter.jinja2
   # old_string: Template TODO section for risks
   # new_string: Jinja2 loop over risks array:
   ```jinja2
   ## 8. Risks & Mitigations

   {% for risk in risks %}
   ### Risk {{ loop.index }}: {{ risk.name }}
   **Risk**: {{ risk.description }}
   **Likelihood**: {{ risk.likelihood }}
   **Impact**: {{ risk.impact }}
   **Mitigation**:
   {% for step in risk.mitigation %}
   - {{ step }}
   {% endfor %}
   {% endfor %}
   ```

Claude (Phase 3: Test Extension - 20-40k tokens):
5. Edit sap-catalog.json (add risks to SAP-030):
   "risks": [
     {
       "name": "Data loss during migration",
       "likelihood": "Medium",
       "impact": "High",
       "mitigation": ["Backup before migrate", "Rollback testing", "Dry-run validation"]
     }
   ]

6. Re-generate SAP-030 to test:
   Bash: python scripts/generate-sap.py SAP-030 --force
7. Read generated capability-charter.md (verify risks section)
8. Validate:
   Bash: python scripts/sap-evaluator.py SAP-030

Claude (Phase 4: Document - 40-50k tokens):
9. Edit protocol-spec.md (document new schema field):
   Add "risks" to schema documentation

Claude (response):
"Extended SAP generation schema with 'risks' field:

✅ Updated capability-charter.jinja2 template (Jinja2 loop over risks)
✅ Tested with SAP-030 (1 risk entry)
✅ Regenerated SAP-030 successfully
✅ Documented in protocol-spec.md

Schema now supports: 10 fields (was 9: +risks)

Re-generate existing SAPs with --force to incorporate new field (optional)."

Result: Schema extended, template updated, tested
```

---

## Claude-Specific Tips

### Tip 1: Use Bash Tool for Generation Commands

**Pattern**:
```bash
# Always use Bash tool for generation, not Write tool
# Write tool would overwrite, Bash tool runs generator script

# Generate new SAP
Bash: python scripts/generate-sap.py SAP-XXX

# Validate SAP
Bash: python scripts/sap-evaluator.py SAP-XXX

# Check INDEX.md stats
Bash: cat docs/skilled-awareness/INDEX.md | grep "Total SAPs"
```

**Why**: Generator script handles 5-file creation, INDEX.md update, directory structure automatically

---

### Tip 2: Read Generated Artifacts Before Editing

**Pattern**:
```bash
# After generation, ALWAYS read artifacts before editing
# Understand TODO placement and context

# Read all 5 artifacts
Read docs/skilled-awareness/{sap-name}/capability-charter.md
Read docs/skilled-awareness/{sap-name}/protocol-spec.md
Read docs/skilled-awareness/{sap-name}/awareness-guide.md
Read docs/skilled-awareness/{sap-name}/adoption-blueprint.md
Read docs/skilled-awareness/{sap-name}/ledger.md

# Then edit with context
Edit docs/skilled-awareness/{sap-name}/protocol-spec.md
```

**Why**: Edit tool requires exact old_string, reading first ensures accuracy

---

### Tip 3: Search for TODOs Systematically

**Pattern**:
```bash
# Find all TODOs in generated SAP
Bash: grep -r "<!-- TODO:" docs/skilled-awareness/{sap-name}/ --line-number

# Count TODOs per file
Bash: grep -c "<!-- TODO:" docs/skilled-awareness/{sap-name}/*.md

# Track progress (TODOs remaining)
Bash: grep -r "<!-- TODO:" docs/skilled-awareness/{sap-name}/ | wc -l
```

**Why**: Systematic TODO tracking ensures nothing is missed

---

### Tip 4: Validate Early and Often

**Pattern**:
```bash
# After generating (before filling TODOs)
Bash: python scripts/sap-evaluator.py SAP-XXX
# Expect: Structure valid, TODOs present (expected)

# After filling 50% of TODOs
Bash: python scripts/sap-evaluator.py SAP-XXX
# Check: No broken links introduced

# After filling 100% of TODOs
Bash: python scripts/sap-evaluator.py SAP-XXX
# Expect: All checks pass, 0 TODOs remaining
```

**Why**: Early validation catches structure issues before investing time in content

---

### Tip 5: Use Edit Tool for TODO Completion, Not Write Tool

**Pattern**:
```bash
# Don't: Overwrite entire file with Write tool
Write docs/skilled-awareness/{sap-name}/protocol-spec.md
# (Loses other TODOs, breaks structure)

# Do: Edit specific TODO sections with Edit tool
Read docs/skilled-awareness/{sap-name}/protocol-spec.md
Edit docs/skilled-awareness/{sap-name}/protocol-spec.md
# old_string: "<!-- TODO: Describe integration with SAP-000 -->"
# new_string: "Actual integration pattern content"
```

**Why**: Edit tool preserves generated structure, only updates targeted TODOs

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Adding to sap-catalog.json Before Generation

**Problem**: Running `generate-sap.py SAP-XXX` without SAP-XXX entry in sap-catalog.json

**Fix**:
```bash
# Always check sap-catalog.json first
Read sap-catalog.json | grep "SAP-XXX"

# If not found, add entry with 9 MVP fields
Edit sap-catalog.json
# Add SAP-XXX entry

# Then generate
Bash: python scripts/generate-sap.py SAP-XXX
```

---

### Pitfall 2: Using Write Tool Instead of Bash Tool for Generation

**Problem**: Trying to create 5 artifacts manually with Write tool instead of using generator

**Fix**:
```bash
# Don't: Write each artifact manually
Write docs/skilled-awareness/{sap-name}/capability-charter.md
Write docs/skilled-awareness/{sap-name}/protocol-spec.md
# (Inconsistent structure, missing navigation, INDEX.md not updated)

# Do: Use generator script via Bash tool
Bash: python scripts/generate-sap.py SAP-XXX
# (Consistent structure, navigation links, INDEX.md auto-updated)
```

---

### Pitfall 3: Overwriting Generated TODOs Without Reading Context

**Problem**: Using Edit tool to replace TODO without understanding surrounding context

**Fix**:
```bash
# Always read artifact first to understand context
Read docs/skilled-awareness/{sap-name}/protocol-spec.md

# Locate TODO context (e.g., section 2.3, related to configuration)
# Then edit with full context
Edit docs/skilled-awareness/{sap-name}/protocol-spec.md
# old_string includes surrounding text for unique match
```

---

### Pitfall 4: Not Validating After Each Major Fill Session

**Problem**: Filling 10+ TODOs without validation, then finding 5 broken links at end

**Fix**:
```bash
# After filling 3-5 TODOs, validate
Bash: python scripts/sap-evaluator.py SAP-XXX

# Fix any issues immediately (broken links, malformed sections)
# Then continue filling TODOs
```

---

### Pitfall 5: Forgetting to Update INDEX.md After Manual SAP Edits

**Problem**: Editing SAP metadata (status, version) without updating INDEX.md

**Fix**:
```bash
# Generator auto-updates INDEX.md on generation
# But manual metadata changes require manual INDEX.md update

# After changing SAP status in capability-charter.md:
Edit docs/skilled-awareness/INDEX.md
# Update SAP-XXX row with new status
```

---

## Tool Usage Patterns

### Using Bash Tool for SAP Generation

```bash
# Generate new SAP
python scripts/generate-sap.py SAP-XXX

# Regenerate existing SAP (use with caution, overwrites)
python scripts/generate-sap.py SAP-XXX --force

# Validate single SAP
python scripts/sap-evaluator.py SAP-XXX

# Validate all SAPs
python scripts/sap-evaluator.py --all

# Count TODOs remaining
grep -r "<!-- TODO:" docs/skilled-awareness/{sap-name}/ | wc -l

# Check generation schema
cat sap-catalog.json | jq '.[] | select(.id=="SAP-XXX")'
```

---

### Using Edit Tool for TODO Completion

```bash
# Read artifact first
Read docs/skilled-awareness/{sap-name}/protocol-spec.md

# Edit specific TODO section
Edit docs/skilled-awareness/{sap-name}/protocol-spec.md
# old_string: "<!-- TODO: Define configuration schema -->\n\n### Configuration Schema\n\n```yaml\n# Example configuration\n```"
# new_string: "### Configuration Schema\n\n```yaml\nsap-030:\n  enabled: true\n  backup_path: /var/backups/migrations\n  rollback_enabled: true\n```"
```

---

### Using Read Tool for Generated Artifact Review

```bash
# Read all 5 artifacts in order (recommended sequence)
Read docs/skilled-awareness/{sap-name}/capability-charter.md
# Understand: Problem, solution, scope, metrics

Read docs/skilled-awareness/{sap-name}/protocol-spec.md
# Identify: Core Contracts TODOs (most critical)

Read docs/skilled-awareness/{sap-name}/awareness-guide.md
# Check: Common workflows TODOs

Read docs/skilled-awareness/{sap-name}/adoption-blueprint.md
# Plan: Level 1/2/3 adoption steps

Read docs/skilled-awareness/{sap-name}/ledger.md
# Note: Adoption tracking baseline
```

---

## Example Claude Code Session (Complete SAP Generation)

```markdown
User: "Generate SAP-030 for database migrations"

Claude (thinking):
- User wants new SAP (SAP-030)
- Need to follow: Add to catalog → Generate → Fill → Validate
- SAP generation = SAP-029 patterns

Claude (Phase 1: Metadata - 0-5k tokens):
1. Read sap-catalog.json (understand schema)
2. Draft SAP-030 metadata (9 fields)
3. Edit sap-catalog.json (add SAP-030 entry)

Claude (Phase 2: Generation - 5-10k tokens):
4. Bash: python scripts/generate-sap.py SAP-030
   Output: ✅ 5 artifacts generated, INDEX.md updated

Claude (Phase 3: Review - 10-30k tokens):
5. Read capability-charter.md (problem, solution clear)
6. Read protocol-spec.md (18 TODOs identified)
7. Read adoption-blueprint.md (12 TODOs identified)

Claude (Phase 4: Fill Critical TODOs - 30-100k tokens):
8. Edit protocol-spec.md (Core Contracts section):
   - Migration file format specification
   - CLI API contracts (create, run, rollback commands)
   - Error handling codes
9. Edit adoption-blueprint.md (Level 1 section):
   - Installation steps (pip install chora-migrations)
   - First migration creation
   - Validation commands
10. Edit awareness-guide.md (Common Workflows):
    - Create migration workflow
    - Run migration workflow
    - Rollback workflow

Claude (Phase 5: Validation - 100-105k tokens):
11. Bash: python scripts/sap-evaluator.py SAP-030
    Output: ✅ PASS (5/5 artifacts, structure valid, 0 critical TODOs, 8 minor TODOs remaining)

Claude (response to user):
"I've generated SAP-030 (database-migrations):

✅ 5 artifacts created and validated
✅ Critical sections filled (Core Contracts, Level 1 adoption)
✅ 18 TODOs completed (protocol-spec, adoption-blueprint, awareness-guide)

⏳ 8 minor TODOs remaining (Level 2/3 adoption, advanced patterns)

Time spent: ~2 hours
Time saved: 8 hours (vs 10 hours manual)

SAP-030 is 80% complete and ready for review. Would you like me to fill the remaining 8 TODOs?"

Result: SAP-030 generated, validated, 80% complete
Total tokens: ~105k (within Phase 2-3 range for implementation)
```

---

## Support & Resources

**SAP-029 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic SAP generation workflows
- [Capability Charter](capability-charter.md) - Problem and solution design
- [Protocol Spec](protocol-spec.md) - Templates, schema, technical contracts
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking, metrics, version history

**Generator Scripts**:
- `scripts/generate-sap.py` - Main generator script (Jinja2 + sap-catalog.json)
- `scripts/sap-evaluator.py` - Validation script (structure, links, TODOs)

**Templates (Jinja2)**:
- `docs/skilled-awareness/templates/capability-charter.jinja2`
- `docs/skilled-awareness/templates/protocol-spec.jinja2`
- `docs/skilled-awareness/templates/awareness-guide.jinja2`
- `docs/skilled-awareness/templates/adoption-blueprint.jinja2`
- `docs/skilled-awareness/templates/ledger.jinja2`

**Related SAPs**:
- [SAP-000 (sap-framework)](../sap-framework/) - 5-artifact pattern foundation
- [SAP-027 (dogfooding-patterns)](../dogfooding-patterns/) - Validation methodology used for SAP-029
- [SAP-004 (testing-framework)](../testing-framework/) - Validation integration

**Example Generated SAPs**:
- SAP-029 (self) - First SAP generated with templates (119x time savings)
- SAP-028 (publishing-automation) - Second SAP, proved repeatability

---

## Version History

- **1.0.0** (2025-11-04): Initial CLAUDE.md for SAP-029
  - Claude Code workflows (generate, fill TODOs, validate, extend schema)
  - Tool usage patterns (Bash for generation, Edit for TODOs, Read for review)
  - Claude-specific tips (validation timing, TODO tracking, Edit vs Write)
  - Common pitfalls (sap-catalog.json first, Bash vs Write, validation frequency)
  - Example complete SAP generation session (SAP-030, ~105k tokens)

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic SAP generation workflows
2. Review [adoption-blueprint.md](adoption-blueprint.md) for installation (Python 3.9+, Jinja2 library)
3. Check [protocol-spec.md](protocol-spec.md) for MVP schema (9 fields) and template structure
4. Generate your first SAP: Edit sap-catalog.json → Bash: generate-sap.py → Fill TODOs → Validate
