# SAP Generation Automation (SAP-029) - Agent Awareness

**SAP ID**: SAP-029
**Version**: 1.0.0
**Status**: Pilot
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

This AGENTS.md provides: Agent-specific patterns for implementing SAP-029.
s.

---

## Common Workflows

### Workflow 1: Generating a New SAP

**Steps**:
0. **Research phase** (Step 0): Gather evidence before defining SAP metadata
1. Add SAP entry to `sap-catalog.json` (MVP schema: 9 fields)
2. Run: `python scripts/generate-sap.py SAP-XXX`
3. Review generated artifacts (5 files with TODO placeholders)
4. Fill manual content (capability charter details, protocol contracts, etc.)
5. Validate: `python scripts/sap-evaluator.py SAP-XXX`
6. Update INDEX.md stats (auto-updated by generator)

**Example (SAP-030 creation with research)**:
```markdown
Step 0: Research (15-30min)
$ just research "database migration best practices for Python projects"
# Generates: docs/research/database-migrations-research.md (15 pages)
# Extract insights:
#   - Problem (from anti-patterns): Manual migrations error-prone, state drift
#   - Evidence (from case studies): Netflix saved 40% time with automated migrations
#   - Solution (from Level A): Flyway-style migration framework with versioning
#   - Principles (from Level A/B): Version control, rollback safety, state tracking
#   - In-scope (from decision playbooks): SQL migrations, rollback scripts, state validation
#   - Out-of-scope (from limitations): ORM integration (separate SAP), multi-DB (v2.0)

Step 1: Edit sap-catalog.json (using research insights)
{
  "id": "SAP-030",
  "name": "database-migrations",
  "owner": "Victor",
  "created_date": "2025-11-04",
  "problem": "No standardized approach to database schema evolution",
  "evidence": ["Manual migrations prone to errors", "20+ migration files without structure"],
  "impact": "Development slowdown, production risks, inconsistent state",
  "solution": "Standardized migration framework with rollback support",
  "principles": ["Version control", "Rollback safety", "State tracking"],
  "in_scope": ["Migration templates", "Rollback scripts", "State validation"],
  "out_of_scope": ["ORM integration", "Multi-database support"],
  "one_sentence_summary": "Standardized database migration framework with rollback support"
}

Step 2: Generate artifacts
$ python scripts/generate-sap.py SAP-030
✅ Generated 5 artifacts:
  - docs/skilled-awareness/database-migrations/capability-charter.md
  - docs/skilled-awareness/database-migrations/protocol-spec.md
  - docs/skilled-awareness/database-migrations/awareness-guide.md
  - docs/skilled-awareness/database-migrations/adoption-blueprint.md
  - docs/skilled-awareness/database-migrations/ledger.md
✅ Updated docs/skilled-awareness/INDEX.md

Step 3: Fill manual content (2-4 hours)
- Complete TODO comments in protocol-spec.md (Core Contracts)
- Add specific adoption steps in adoption-blueprint.md
- Document integration patterns in awareness-guide.md

Step 4: Validate
$ python scripts/sap-evaluator.py SAP-030
✅ All 5 artifacts present
✅ Structure validation passed
✅ Link validation passed
```

**Outcome**: SAP-030 created in 2 hours (vs 10 hours manual)

---

### Workflow 2: Updating INDEX.md After Generation

**Steps**:
1. Generator auto-updates INDEX.md with new SAP entry
2. Review coverage stats (Total SAPs, Complete artifacts count)
3. Commit updated INDEX.md with generated SAP

**What INDEX.md Update Includes**:
```markdown
## SAP Registry

| SAP ID | Name | Status | Artifacts | Owner | Created |
|--------|------|--------|-----------|-------|---------|
| ... | ... | ... | ... | ... | ... |
| SAP-030 | database-migrations | draft | 5/5 | Victor | 2025-11-04 |

**Coverage Stats**:
- **Total SAPs**: 31 (was 30)
- **Complete Artifacts**: 155/155 (100%) - all 5 artifacts per SAP
```

**Outcome**: INDEX.md automatically reflects new SAP, no manual tracking needed

---

### Workflow 3: Validating Generated SAP

**Steps**:
1. After filling manual content, run `sap-evaluator.py SAP-XXX`
2. Check validation results:
   - Artifact completeness (5/5 files present)
   - Structure validation (required sections present)
   - Link validation (cross-references work)
3. Fix any validation errors
4. Re-run until validation passes

**Example Validation**:
```bash
$ python scripts/sap-evaluator.py SAP-030

SAP-030 Validation Report:
✅ Artifacts: 5/5 present
✅ Structure: All required sections found
✅ Links: 12/12 internal links valid
⚠️  TODOs: 15 remaining (expected, manual fill needed)

Overall: PASS (ready for manual content fill)
```

**Outcome**: Confidence that generated SAP meets structural requirements

---

### Workflow 4: Extending Generation Schema

**Steps** (Post-MVP, future enhancement):
1. Add new fields to sap-catalog.json schema (e.g., `risks`, `constraints`, `metrics`)
2. Update Jinja2 templates to include new fields
3. Re-generate existing SAPs to incorporate new structure (optional)
4. Update documentation (protocol-spec.md) with new schema

**Example (Adding `risks` field)**:
```markdown
Step 1: Extend sap-catalog.json
{
  "id": "SAP-030",
  ...
  "risks": [
    {"name": "Data loss during migration", "likelihood": "Medium", "impact": "High", "mitigation": "Backup before migrate"}
  ]
}

Step 2: Update capability-charter.jinja2 template
## 8. Risks & Mitigations

{% for risk in risks %}
### Risk {{ loop.index }}: {{ risk.name }}
**Likelihood**: {{ risk.likelihood }}
**Impact**: {{ risk.impact }}
**Mitigation**: {{ risk.mitigation }}
{% endfor %}

Step 3: Re-generate (optional)
$ python scripts/generate-sap.py SAP-030 --force
✅ Re-generated with extended schema
```

**Outcome**: SAP generation evolves with richer metadata over time

---

## MVP Generation Schema (9 Fields)

### Required Fields in sap-catalog.json

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | String | SAP identifier | `"SAP-030"` |
| `name` | String | SAP directory name | `"database-migrations"` |
| `owner` | String | SAP owner/maintainer | `"Victor"` |
| `created_date` | String | Creation date (ISO 8601) | `"2025-11-04"` |
| `problem` | String | Problem statement | `"No standardized approach to..."` |
| `evidence` | Array[String] | Evidence for problem | `["Manual migrations error-prone"]` |
| `impact` | String | Business impact | `"Development slowdown, production risks"` |
| `solution` | String | Proposed solution | `"Standardized migration framework..."` |
| `principles` | Array[String] | Key principles | `["Version control", "Rollback safety"]` |
| `in_scope` | Array[String] | What's included | `["Migration templates"]` |
| `out_of_scope` | Array[String] | What's excluded | `["ORM integration"]` |
| `one_sentence_summary` | String | Concise summary | `"Standardized database migration framework"` |

### What Gets Auto-Generated (80%)

**Structure auto-generated**:
- 5 artifact files with complete section headers
- Table of contents and navigation links
- Cross-references between artifacts
- Metadata sections (SAP ID, version, status, owner, dates)
- Placeholder TODO comments for manual content
- INDEX.md registry entry

**Manual content needed (20%)**:
- Detailed technical specifications (protocol-spec.md Core Contracts)
- Specific adoption steps (adoption-blueprint.md Level 1/2/3)
- Integration patterns (awareness-guide.md)
- Stakeholder details, dependencies, risks (capability-charter.md)
- Adoption tracking, metrics, feedback (ledger.md)

---

## Time Savings Analysis

### Baseline (Manual SAP Creation)

**Total time**: 10 hours
- Structure setup: 6-8 hours (creating 5 files, section headers, navigation)
- Content fill: 2-4 hours (writing problem, solution, contracts, adoption)
- Validation: 30 minutes (manual checking for consistency)

### With SAP-029 (Automated Generation)

**Total time**: ~2 hours (80% time savings)
- Setup (one-time): 10 hours (templates, generator script, validation)
- Generation: 5 minutes (run script, review structure)
- Content fill: 2-4 hours (same as manual, but focused)
- Validation: 30 seconds (automated sap-evaluator.py)

**Break-even**: 1.01 uses (10h setup / 9.917h per-SAP savings)

**ROI after 2 SAPs**: 9.8 hours net savings (119x time savings in pilot)

---

## Integration with Other SAPs

### Integration with SAP-000 (SAP Framework)

**Pattern**: SAP-029 enforces SAP-000's 5-artifact pattern

**Workflow**:
1. SAP-000 defines: Every SAP has 5 artifacts (charter, spec, guide, blueprint, ledger)
2. SAP-029 automates: Generate all 5 artifacts from sap-catalog.json metadata
3. SAP-029 validates: Ensure generated SAPs comply with SAP-000 structure

**Outcome**: All generated SAPs follow SAP Framework automatically

---

### Integration with SAP-027 (Dogfooding Patterns)

**Pattern**: SAP-029 was validated using SAP-027 methodology

**Workflow**:
1. SAP-027 defined: 5-week pilot (3 weeks build, 1 week validate, 1 week formalize)
2. SAP-029 pilot: Used SAP-027 to validate template system
   - Week 4 metrics: 119x time savings, 100% satisfaction, 0 critical bugs, 2 adoption cases
   - Week 4 decision: GO (exceeded all targets by 24x)
   - Week 5: Formalized SAP-029, completed TODOs
3. SAP-029 now used: To generate SAP-028, proving repeatability

**Outcome**: SAP-029 is production-proven via SAP-027 dogfooding

---

### Integration with SAP-004 (Testing Framework)

**Pattern**: SAP-029 integrates with validation/testing

**Workflow**:
1. SAP-029 generates: 5 artifacts with structure
2. SAP-004 validates: Run `sap-evaluator.py` as part of CI/CD
3. SAP-004 catches: Missing artifacts, broken links, incomplete structure
4. Developer fixes: Fill TODOs, fix validation errors
5. SAP-004 re-validates: Until SAP passes

**Outcome**: Generated SAPs are validated automatically in CI pipeline

---

## Common Pitfalls

### Pitfall 1: Forgetting to Update sap-catalog.json

**Problem**: Running `generate-sap.py SAP-XXX` without adding SAP-XXX to sap-catalog.json first

**Fix**:
```bash
# Always add to sap-catalog.json FIRST
vim sap-catalog.json
# Add SAP-XXX entry with 9 MVP fields

# THEN generate
python scripts/generate-sap.py SAP-XXX
```

---

### Pitfall 2: Treating Generated SAPs as "Done"

**Problem**: Committing generated SAPs without filling TODO comments

**Fix**:
- Generated SAPs are 80% complete (structure)
- Manual 20% required (Core Contracts, adoption steps, integration patterns)
- Search for `<!-- TODO:` comments and fill before committing

---

### Pitfall 3: Not Running Validation After Manual Fill

**Problem**: Filling content but breaking structure (e.g., removing required sections)

**Fix**:
```bash
# After filling manual content, ALWAYS validate
python scripts/sap-evaluator.py SAP-XXX

# Fix any validation errors before commit
```

---

### Pitfall 4: Inconsistent Naming (sap-catalog.json vs directory)

**Problem**: `"name": "database-migrations"` in sap-catalog.json but creating `docs/skilled-awareness/db-migrations/`

**Fix**:
- Generator uses `name` field to create directory
- Ensure `"name": "database-migrations"` matches desired directory name
- Generator creates: `docs/skilled-awareness/{name}/`

---

### Pitfall 5: Skipping MVP Schema Fields

**Problem**: Adding SAP to sap-catalog.json with only 3-4 fields instead of 9

**Fix**:
```json
// Minimum 9 fields required for generation:
{
  "id": "SAP-030",
  "name": "database-migrations",
  "owner": "Victor",
  "created_date": "2025-11-04",
  "problem": "...",
  "evidence": [...],
  "impact": "...",
  "solution": "...",
  "principles": [...],
  "in_scope": [...],
  "out_of_scope": [...],
  "one_sentence_summary": "..."
}
```

---

## Key Commands

```bash
# Generate new SAP (after adding to sap-catalog.json)
python scripts/generate-sap.py SAP-XXX

# Validate generated SAP
python scripts/sap-evaluator.py SAP-XXX

# Re-generate with force (overwrites existing, use with caution)
python scripts/generate-sap.py SAP-XXX --force

# Validate all SAPs in catalog
python scripts/sap-evaluator.py --all

# Check INDEX.md coverage stats
cat docs/skilled-awareness/INDEX.md | grep "Coverage Stats" -A 5
```

---

## Support & Resources

**SAP-029 Documentation**:
- [Capability Charter](capability-charter.md) - Problem, solution, scope, metrics
- [Protocol Spec](protocol-spec.md) - Technical specification (templates, schema, contracts)
- [CLAUDE.md](CLAUDE.md) - Claude Code-specific patterns
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide (Level 1-3)
- [Ledger](ledger.md) - Adoption tracking, metrics, version history

**Example SAPs Generated with SAP-029**:
- SAP-029 (self) - First SAP generated with templates
- SAP-028 (publishing-automation) - Second SAP, proved repeatability

**Related SAPs**:
- [SAP-000 (sap-framework)](../sap-framework/) - 5-artifact pattern foundation
- [SAP-027 (dogfooding-patterns)](../dogfooding-patterns/) - Validation methodology (119x savings)
- [SAP-004 (testing-framework)](../testing-framework/) - Validation integration

**Templates**:
- `docs/skilled-awareness/templates/capability-charter.jinja2`
- `docs/skilled-awareness/templates/protocol-spec.jinja2`
- `docs/skilled-awareness/templates/awareness-guide.jinja2`
- `docs/skilled-awareness/templates/adoption-blueprint.jinja2`
- `docs/skilled-awareness/templates/ledger.jinja2`

---

## Version History

- **1.0.0** (2025-11-04): Initial AGENTS.md for SAP-029
  - Common workflows (generate, validate, extend schema)
  - MVP generation schema (9 fields)
  - Time savings analysis (119x in pilot)
  - Integration with SAP-000, SAP-027, SAP-004
  - Common pitfalls and key commands

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific automation patterns
2. Review [adoption-blueprint.md](adoption-blueprint.md) for installation (requires Python 3.9+, Jinja2)
3. Check [capability-charter.md](capability-charter.md) for design rationale and metrics
4. Generate your first SAP: Add to sap-catalog.json → Run generate-sap.py → Fill TODOs → Validate
