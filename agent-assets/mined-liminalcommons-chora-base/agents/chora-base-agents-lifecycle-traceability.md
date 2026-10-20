# AGENTS.md - Lifecycle Traceability (SAP-056)

**Domain**: Governance & Traceability
**SAP**: SAP-056 (lifecycle-traceability)
**Version**: 1.0.0
**Last Updated**: 2025-11-20

---

## 📖 Quick Reference

**New to SAP-056?** → Read **[capability-charter.md](capability-charter.md)** first (10-min read)

The capability charter provides:
- 🎯 **Problem Statement** - Accountability gap where artifacts exist in isolation (40% traceability coverage today)
- 💡 **Solution Design** - Umbrella SAP governing linkage across 10 artifact types (Vision → Features → Requirements → Code → Tests → Docs → Git → Tasks → Events → Knowledge)
- 📊 **Success Criteria** - 80% of adopters achieve L2+ traceability (substantial coverage), 15-30 min → <1 min context restoration
- 🔧 **Key Artifacts** - feature-manifest.yaml (single source of truth), validation scripts, traceability markers (REQ-XXX, FEAT-XXX)
- 📈 **ROI** - ~93 hours saved annually per project, break-even in 6-8 months for single project

This AGENTS.md provides: Agent-specific patterns for creating feature entries, adding traceability markers to code, querying the manifest, validating completeness, and performing impact analysis.

---

## Overview

This is the domain-specific AGENTS.md file for lifecycle traceability (SAP-056). It provides context for agents working with the feature manifest, traceability markers, validation scripts, and impact analysis tools.

**Parent**: See [/AGENTS.md](/AGENTS.md) for project-level context

**Pattern**: "Nearest File Wins" - This file provides traceability-specific context

---

## User Signal Patterns

### Feature Manifest Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "create feature entry" | add_feature_to_manifest() | Edit feature-manifest.yaml | Add new feature with linkages |
| "link code to feature" | add_code_reference() | Edit feature-manifest.yaml code array | Link implementation files |
| "show feature dependencies" | query_feature_manifest() | yq/grep on feature-manifest.yaml | Find all artifacts for feature |
| "validate traceability" | validate_traceability() | python scripts/validate-traceability.py | Run 10 validation rules |
| "what implements REQ-X" | find_requirement_implementation() | grep "REQ-X" in code + manifest | Trace requirement to code |

### Traceability Marker Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "add requirement marker" | add_requirement_marker() | Edit code file (add # REQ-XXX) | Link code to requirement |
| "add feature marker" | add_feature_marker() | Edit code file (add # FEAT-XXX) | Link code to feature |
| "find all markers" | search_traceability_markers() | grep -r "REQ-\|FEAT-" src/ | Discover existing markers |
| "validate markers" | validate_marker_references() | scripts/validate-traceability.py rule 8 | Check marker integrity |

### Impact Analysis Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "what depends on feature X" | analyze_feature_impact() | Query feature-manifest.yaml dependencies | Dependency graph |
| "what breaks if I change X" | analyze_change_impact() | grep feature in manifest + tests | Find dependent artifacts |
| "show feature coverage" | report_feature_coverage() | scripts/traceability-dashboard.py | HTML coverage report |
| "find orphaned code" | detect_orphan_artifacts() | validate-traceability.py rule 5 | Code without feature linkage |

### Compliance Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "check traceability level" | assess_compliance_level() | validate-traceability.py --level | L0-L3 scoring |
| "generate traceability report" | generate_compliance_report() | validate-traceability.py --report | Markdown output |
| "auto-generate manifest" | auto_generate_manifest() | scripts/generate-feature-manifest.py | Git log + beads queries |
| "check bidirectional links" | validate_bidirectional_linkage() | validate-traceability.py rule 2 | Doc↔Code consistency |

### Common Variations

**Manifest Queries**:
- "show feature X" / "what's in feature X" / "feature dependencies" → query_feature_manifest()
- "create feature" / "add feature" / "new feature" → add_feature_to_manifest()

**Marker Queries**:
- "add marker" / "link to requirement" / "tag code" → add_requirement_marker()
- "find markers" / "search markers" / "show linkages" → search_traceability_markers()

**Impact Analysis Queries**:
- "what depends on X" / "impact of changing X" / "what breaks" → analyze_feature_impact()
- "orphaned code" / "unlinked artifacts" / "coverage gaps" → detect_orphan_artifacts()

**Validation Queries**:
- "validate" / "check traceability" / "run validation" → validate_traceability()
- "compliance level" / "traceability status" / "coverage score" → assess_compliance_level()

---

## Lifecycle Traceability Quick Reference

### Feature Manifest (feature-manifest.yaml)

**Structure**:
```yaml
features:
  - id: FEAT-056-001
    name: "Feature manifest schema"
    description: "Machine-readable linkage between artifacts"
    status: active
    created: "2025-11-16"
    vision_ref: "docs/vision/traceability-vision.md"
    requirements:
      - id: REQ-056-001
        description: "Single source of truth for feature artifacts"
        status: implemented
    code:
      - path: "schemas/feature-manifest.yaml"
        lines: "1-150"
        commit: "abc123def"
    tests:
      - path: "tests/test_feature_manifest.py"
        markers: ["requirement:REQ-056-001"]
    documentation:
      - path: "docs/skilled-awareness/lifecycle-traceability/protocol-spec.md"
        section: "4.1 Feature Manifest Schema"
    git_commits:
      - sha: "abc123def"
        message: "feat: Add feature manifest schema"
```

**Key Fields**:
- `id`: Unique feature identifier (FEAT-XXX-NNN)
- `vision_ref`: Link to vision document (forward linkage)
- `requirements`: Array of requirements this feature satisfies
- `code`: Implementation files with line ranges and git commits
- `tests`: Test files with pytest markers
- `documentation`: Documentation files with section references

### Traceability Markers

**In Code** (Python example):
```python
def validate_manifest(manifest_path: str) -> bool:
    """
    Validate feature manifest against JSON Schema.

    Traceability:
        - REQ-056-001: Single source of truth validation
        - REQ-056-006: Schema compliance enforcement
        - FEAT-056-001: Feature manifest schema
    """
    # Implementation validates schema compliance
    # REQ-056-006: Load JSON Schema
    schema = load_schema("schemas/feature-manifest.yaml")

    # REQ-056-001: Parse manifest
    manifest = parse_yaml(manifest_path)

    # REQ-056-006: Validate against schema
    return validate_schema(manifest, schema)
```

**In Tests** (pytest markers):
```python
import pytest

@pytest.mark.requirement("REQ-056-001")
@pytest.mark.feature("FEAT-056-001")
def test_feature_manifest_validation():
    """Test that feature manifest validates against schema."""
    # FEAT-056-001: Manifest schema validation
    result = validate_manifest("feature-manifest.yaml")
    assert result is True
```

**In Documentation** (frontmatter):
```markdown
---
sap_id: SAP-056
feature_refs:
  - FEAT-056-001
  - FEAT-056-002
requirement_refs:
  - REQ-056-001
  - REQ-056-006
code_references:
  - path: "schemas/feature-manifest.yaml"
    description: "JSON Schema definition"
test_references:
  - path: "tests/test_feature_manifest.py"
    description: "Schema validation tests"
---

# Feature Manifest Schema

This document defines the schema for feature-manifest.yaml...
```

### Validation Rules (10 Core Rules)

1. **Forward Linkage**: Every vision outcome → ≥1 feature
2. **Bidirectional Linkage**: If doc references code, code manifest lists doc
3. **Evidence Requirement**: Every feature → ≥1 test AND ≥1 doc
4. **Closed Loop**: Every git commit closing task → links to feature
5. **Orphan Detection**: No artifact without parent linkage
6. **Schema Compliance**: feature-manifest.yaml passes JSON Schema validation
7. **Reference Integrity**: All vision_ref/code/docs/tests paths exist
8. **Requirement Coverage**: Every requirement → ≥1 test with marker
9. **Documentation Coverage**: Every feature → ≥1 doc in frontmatter
10. **Event Correlation**: Every task completion → A-MEM event with feature_id

### Compliance Levels (L0-L3)

- **L0 (No Traceability)**: No linkages defined
- **L1 (Partial)**: Vision→Features + Code→Tests linked (~40% coverage)
- **L2 (Substantial)**: L1 + Features→Requirements + Docs→Code (~70% coverage)
- **L3 (Complete)**: L2 + Git→Tasks + Tasks→Events + Events→Knowledge (100% coverage)

**Target**: 80% of adopters achieve L2+ within 6 months

---

## Common Workflows

### Workflow 1: Creating Feature Entry in feature-manifest.yaml

**Goal**: Add new feature to manifest with complete traceability linkage

**Steps**:
1. Open feature-manifest.yaml
2. Add new feature entry under `features` array:
   ```yaml
   - id: FEAT-XXX-NNN  # Sequential numbering
     name: "Short feature name"
     description: "Detailed description"
     status: draft  # draft|in_progress|implemented|deprecated
     created: "2025-11-20"
     vision_ref: "docs/vision/vision-doc.md"  # Link to vision
     requirements: []  # Add in step 3
     code: []  # Add in step 4
     tests: []  # Add in step 5
     documentation: []  # Add in step 6
   ```
3. Add requirements:
   ```yaml
   requirements:
     - id: REQ-XXX-001
       description: "Requirement description"
       status: draft  # draft|in_progress|implemented|deprecated
   ```
4. Link code files (after implementation):
   ```yaml
   code:
     - path: "src/module/file.py"
       lines: "10-50"
       commit: "abc123"  # Git commit SHA
   ```
5. Link tests:
   ```yaml
   tests:
     - path: "tests/test_module.py"
       markers: ["requirement:REQ-XXX-001", "feature:FEAT-XXX-NNN"]
   ```
6. Link documentation:
   ```yaml
   documentation:
     - path: "docs/how-to/feature-guide.md"
       section: "3.2 Using Feature X"
   ```
7. Validate: `python scripts/validate-traceability.py --feature FEAT-XXX-NNN`

**Expected Output**: Feature entry passes all 10 validation rules

**Quality Gate**: Bidirectional linkage verified (doc frontmatter references feature, feature references doc)

---

### Workflow 2: Adding Traceability Markers to Code

**Goal**: Link implementation code to requirements and features via inline markers

**Steps**:
1. Identify requirement(s) and feature(s) this code implements
2. Add docstring markers:
   ```python
   def my_function():
       """
       Function description.

       Traceability:
           - REQ-056-001: Requirement description
           - REQ-056-002: Another requirement
           - FEAT-056-001: Feature this supports
       """
   ```
3. Add inline markers for specific blocks:
   ```python
   # REQ-056-001: Implementation of requirement 1
   if condition:
       # FEAT-056-001: Feature-specific logic
       do_something()
   ```
4. Update feature-manifest.yaml code array (Workflow 1, step 4)
5. Validate marker integrity: `python scripts/validate-traceability.py --check-markers`

**Expected Output**: All markers reference valid requirements/features in manifest

**Anti-Pattern**: Avoid markers without manifest entries (orphaned markers)

---

### Workflow 3: Querying Feature Manifest for Context Restoration

**Goal**: Quickly restore context for a feature by finding all related artifacts

**Steps**:
1. Query by feature ID:
   ```bash
   # Using yq (recommended for structured parsing)
   yq eval '.features[] | select(.id == "FEAT-056-001")' feature-manifest.yaml

   # Using grep (quick but less structured)
   grep -A 30 "id: FEAT-056-001" feature-manifest.yaml
   ```
2. Extract specific artifact types:
   ```bash
   # Find all code files for feature
   yq eval '.features[] | select(.id == "FEAT-056-001") | .code[].path' feature-manifest.yaml

   # Find all tests for feature
   yq eval '.features[] | select(.id == "FEAT-056-001") | .tests[].path' feature-manifest.yaml

   # Find all docs for feature
   yq eval '.features[] | select(.id == "FEAT-056-001") | .documentation[].path' feature-manifest.yaml
   ```
3. Load artifacts progressively:
   - Phase 1 (0-10k tokens): Read feature entry + requirements
   - Phase 2 (10-30k tokens): Read code files + tests
   - Phase 3 (30-50k tokens): Read documentation + vision
4. Context restored in <1 minute (vs 15-30 min manual search)

**Expected Output**: Complete artifact list with paths for targeted file reading

**Time Saved**: 14-29 minutes per context restoration event

---

### Workflow 4: Validating Traceability Completeness

**Goal**: Run automated validation to ensure all features have complete traceability

**Steps**:
1. Run validation script:
   ```bash
   python scripts/validate-traceability.py
   ```
2. Review output (10 validation rules checked):
   ```
   ✅ Rule 1: Forward Linkage - 12/12 vision outcomes linked
   ✅ Rule 2: Bidirectional Linkage - 45/45 docs have code references
   ❌ Rule 3: Evidence Requirement - 8/10 features have tests (FAIL)
   ✅ Rule 4: Closed Loop - 25/25 commits linked to tasks
   ⚠️  Rule 5: Orphan Detection - 3 orphaned code files (WARNING)
   ...

   Compliance Level: L2 (Substantial) - 70% coverage
   ```
3. Fix violations:
   - Rule 3 failure: Add tests for FEAT-056-003 and FEAT-056-007
   - Rule 5 warning: Link orphaned files to features or mark as infrastructure
4. Re-run validation until all rules pass
5. Generate compliance report:
   ```bash
   python scripts/validate-traceability.py --report > traceability-report.md
   ```

**Expected Output**: L2+ compliance (≥70% coverage), markdown report generated

**Quality Gate**: All critical rules pass (1-4, 6-9), warnings acceptable for L2

---

### Workflow 5: Impact Analysis via Traceability Graph

**Goal**: Identify what artifacts depend on a feature before making changes

**Steps**:
1. Query feature dependencies:
   ```bash
   # Find all features that depend on FEAT-056-001
   yq eval '.features[] | select(.requirements[].id == "REQ-056-001") | .id' feature-manifest.yaml
   ```
2. Find dependent tests:
   ```bash
   # Tests that validate this feature
   grep -r "@pytest.mark.feature(\"FEAT-056-001\")" tests/
   ```
3. Find dependent documentation:
   ```bash
   # Docs that reference this feature
   grep -r "FEAT-056-001" docs/ --include="*.md"
   ```
4. Find code markers:
   ```bash
   # Code that implements this feature
   grep -r "# FEAT-056-001" src/
   ```
5. Generate impact report:
   ```bash
   python scripts/traceability-dashboard.py --feature FEAT-056-001 --output impact-report.html
   ```
6. Review HTML dashboard for visual dependency graph

**Expected Output**: Complete dependency graph showing what breaks if feature changes

**Time Saved**: 1-2 hours manual review → <5 minutes automated query

---

## Integration with Other SAPs

### SAP-000 (sap-framework)
- **Pattern**: SAP-056 uses 5-artifact structure (charter, spec, guide, blueprint, ledger)
- **Traceability**: All SAP artifacts reference features via frontmatter `feature_refs`

### SAP-004 (testing-framework)
- **Pattern**: pytest markers (`@pytest.mark.requirement`, `@pytest.mark.feature`)
- **Traceability**: Tests link to requirements/features via markers, manifest links to test files

### SAP-007 (documentation-framework)
- **Pattern**: YAML frontmatter with `requirement_refs`, `feature_refs`, `code_references`, `test_references`
- **Traceability**: Bidirectional doc↔code linkage enforced by Rule 2

### SAP-010 (memory-system)
- **Pattern**: A-MEM events include `feature_id` field for correlation
- **Traceability**: Task→Events→Knowledge linkage via wikilinks

### SAP-012 (development-lifecycle)
- **Pattern**: Documentation-First workflow (Requirements → Docs → Tests → Code)
- **Traceability**: Artifact creation order ensures forward linkage by default

### SAP-015 (task-tracking)
- **Pattern**: Beads tasks reference features via `feature_id` field
- **Traceability**: Git commits link to tasks via `[task-id]` suffix, tasks link to features

### SAP-016 (link-validation)
- **Pattern**: Validate traceability references are valid links
- **Traceability**: Reference integrity (Rule 7) uses link validation for paths

---

## Best Practices

### 1. Create Feature Entries Early
- Add feature to manifest when requirement is created (draft status)
- Update status as implementation progresses (draft → in_progress → implemented)
- Avoids orphaned code (code without feature linkage)

### 2. Use Markers Consistently
- Always add docstring traceability section for functions/classes
- Add inline markers for complex logic blocks
- Keep markers up-to-date when refactoring

### 3. Validate Before Commits
- Run `validate-traceability.py` before committing code
- Fix violations immediately (easier than retroactive linkage)
- Pre-commit hook enforces validation (optional, recommended for L3)

### 4. Bidirectional Linkage is Critical
- If doc references code, code manifest MUST list doc
- If test validates requirement, requirement manifest MUST list test
- Prevents drift between artifacts

### 5. Progressive Adoption
- Start with L1 (Vision→Features + Code→Tests) - 2-4 hours
- Add L2 (Features→Requirements + Docs→Code) - 1-2 days
- Achieve L3 (Git→Tasks + Events→Knowledge) - 1 week
- Don't try to implement all levels simultaneously

---

## Common Pitfalls

### Pitfall 1: Creating Code Without Manifest Entry
**Problem**: Implement code first, forget to add feature to manifest
**Fix**: Always create feature entry (draft status) before writing code
**Detection**: Rule 5 (Orphan Detection) flags unlinked code

### Pitfall 2: Broken References in Manifest
**Problem**: feature-manifest.yaml references code/docs/tests that don't exist
**Fix**: Run `validate-traceability.py --check-paths` to verify all references
**Detection**: Rule 7 (Reference Integrity) validates file paths

### Pitfall 3: One-Way Linkage
**Problem**: Doc references code in frontmatter, but code manifest doesn't list doc
**Fix**: Update both sides when creating linkage (bidirectional)
**Detection**: Rule 2 (Bidirectional Linkage) enforces consistency

### Pitfall 4: Missing Test Coverage
**Problem**: Feature has code and docs but no tests
**Fix**: Add test file and link via manifest tests array + pytest markers
**Detection**: Rule 3 (Evidence Requirement) requires ≥1 test per feature

### Pitfall 5: Manual Manifest Maintenance is Tedious
**Problem**: Updating manifest for every git commit is overhead
**Fix**: Use `scripts/generate-feature-manifest.py` to auto-generate from git log
**Mitigation**: Run auto-generation weekly, manually adjust as needed

---

## Quality Gates

### Before Commit (Traceability Changes)
- [ ] feature-manifest.yaml passes schema validation (Rule 6)
- [ ] All referenced files exist (Rule 7)
- [ ] Bidirectional linkage verified (Rule 2)
- [ ] No orphaned artifacts (Rule 5)
- [ ] Markers reference valid features/requirements

### Before PR (New Features)
- [ ] Feature entry exists in manifest with status
- [ ] ≥1 test linked with pytest markers (Rule 3)
- [ ] ≥1 doc linked in frontmatter (Rule 9)
- [ ] Requirements have coverage (Rule 8)
- [ ] Validation script passes for this feature

### CI/CD (Automated Validation)
- [ ] Full validation suite passes (10 rules)
- [ ] Compliance level ≥L2 (Substantial)
- [ ] No critical violations (Rules 1-4, 6-9)
- [ ] Traceability report generated and archived

---

## Related SAPs

- **SAP-000** (sap-framework): 5-artifact structure with frontmatter
- **SAP-004** (testing-framework): pytest markers for requirement linkage
- **SAP-007** (documentation-framework): Frontmatter for doc↔code linkage
- **SAP-010** (memory-system): A-MEM events with feature_id correlation
- **SAP-012** (development-lifecycle): Documentation-First workflow
- **SAP-015** (task-tracking): Beads tasks with feature references
- **SAP-016** (link-validation): Reference integrity validation
- **SAP-019** (sap-self-evaluation): Traceability compliance assessment

---

**Version History**:
- **1.0.0** (2025-11-20): Initial AGENTS.md for lifecycle traceability
  - 5 common workflows: Create feature entry, add markers, query manifest, validate completeness, impact analysis
  - User signal patterns for manifest, markers, impact, and compliance operations
  - Integration patterns with 8 related SAPs
  - Best practices and 5 common pitfalls
  - Quality gates for commit, PR, and CI/CD
