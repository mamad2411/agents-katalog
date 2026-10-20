---
sap_id: SAP-056
version: 1.0.0
status: draft
last_updated: 2025-11-20
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 12
progressive_loading:
  phase_1: "lines 1-200"   # Quick Start + Core Workflows
  phase_2: "lines 201-400" # Advanced Operations + Tool Patterns
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 4000
phase_2_token_estimate: 8000
phase_3_token_estimate: 12000
---

# Lifecycle Traceability (SAP-056) - Claude-Specific Awareness

**SAP ID**: SAP-056
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-20

---

## 📖 Quick Reference

**New to SAP-056?** → Read **[capability-charter.md](capability-charter.md)** first (10-min read)

The capability charter provides:
- 🎯 **Problem Statement** - Accountability gap where artifacts exist in isolation (40% traceability coverage today)
- 💡 **Solution Design** - Umbrella SAP governing linkage across 10 artifact types via feature-manifest.yaml
- 📊 **Success Criteria** - 80% of adopters achieve L2+ traceability, <1 min context restoration (vs 15-30 min)
- 🔧 **Key Artifacts** - feature-manifest.yaml, validation scripts, traceability markers (REQ-XXX, FEAT-XXX)
- 📈 **ROI** - ~93 hours saved annually per project, 6-8 month break-even

This CLAUDE.md provides: Claude Code-specific workflows using Read for manifest queries, Edit for adding markers, Bash for validation, and progressive loading patterns for efficient traceability operations.

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for working with lifecycle traceability (SAP-056).

### First-Time Session

1. Read [AGENTS.md](AGENTS.md) for generic traceability patterns
2. Use this file for Claude Code tool integration (Read for manifest, Edit for markers, Bash for validation)
3. **Always read feature-manifest.yaml** before making changes to features

### Key Files for Claude

- **feature-manifest.yaml**: Single source of truth for feature linkages (Read tool)
- **schemas/feature-manifest.yaml**: JSON Schema for validation (Read for structure)
- **scripts/validate-traceability.py**: 10-rule validation suite (Bash tool)
- **scripts/generate-feature-manifest.py**: Auto-generation from git log (Bash tool)

---

## Claude Code Traceability Workflows

### Workflow 1: Querying Feature Manifest with Read Tool

```markdown
User: "Show me all artifacts for FEAT-056-001"

Claude (Phase 1: Read Manifest - 0-5k tokens):
1. Read feature manifest:
   Read feature-manifest.yaml

2. Search for feature ID:
   # Use yq or grep to extract feature entry
   # Example output:
   # - id: FEAT-056-001
   #   name: "Feature manifest schema"
   #   code: ["schemas/feature-manifest.yaml"]
   #   tests: ["tests/test_feature_manifest.py"]
   #   documentation: ["docs/skilled-awareness/lifecycle-traceability/protocol-spec.md"]

Claude (Phase 2: Load Artifacts - 5-15k tokens):
3. Read linked artifacts progressively:
   Read schemas/feature-manifest.yaml  # Code implementation
   Read tests/test_feature_manifest.py  # Test coverage
   Read docs/skilled-awareness/lifecycle-traceability/protocol-spec.md  # Documentation

Claude (response to user):
"✅ FEAT-056-001 artifacts loaded:
   - Code: schemas/feature-manifest.yaml (150 lines)
   - Tests: tests/test_feature_manifest.py (45 lines, 3 test cases)
   - Docs: protocol-spec.md section 4.1

   Context restored in 1 minute (vs 15-30 min manual search)
   Token usage: 12k/200k"

Result: Complete feature context loaded efficiently
```

**Key Pattern**: Read manifest first → Extract file paths → Read only relevant artifacts (progressive loading)

---

### Workflow 2: Adding Traceability Markers with Edit Tool

```markdown
User: "Add traceability markers to validate_manifest() function"

Claude (Phase 1: Understand Context - 0-5k tokens):
1. Read feature manifest to find feature/requirement IDs:
   Read feature-manifest.yaml
   # Find FEAT-056-001 and REQ-056-001 references

2. Read target code file:
   Read src/traceability/validator.py
   # Locate validate_manifest() function

Claude (Phase 2: Add Markers - 5-10k tokens):
3. Edit code file to add docstring markers:
   Edit src/traceability/validator.py

   # Old:
   def validate_manifest(manifest_path: str) -> bool:
       """Validate feature manifest against JSON Schema."""
       # Implementation...

   # New:
   def validate_manifest(manifest_path: str) -> bool:
       """
       Validate feature manifest against JSON Schema.

       Traceability:
           - REQ-056-001: Single source of truth validation
           - REQ-056-006: Schema compliance enforcement
           - FEAT-056-001: Feature manifest schema
       """
       # Implementation...

4. Add inline markers for specific logic:
   Edit src/traceability/validator.py

   # Old:
   schema = load_schema("schemas/feature-manifest.yaml")

   # New:
   # REQ-056-006: Load JSON Schema for validation
   schema = load_schema("schemas/feature-manifest.yaml")

Claude (Phase 3: Update Manifest - 10-15k tokens):
5. Update feature-manifest.yaml with code reference:
   Edit feature-manifest.yaml

   # Add to FEAT-056-001 code array:
   code:
     - path: "src/traceability/validator.py"
       lines: "10-50"
       commit: "current"  # Will update with actual SHA after commit

Claude (Phase 4: Validate - 15-18k tokens):
6. Run validation to ensure markers are correct:
   Bash: python scripts/validate-traceability.py --check-markers

Claude (response to user):
"✅ Traceability markers added:
   - Docstring: 3 markers (REQ-056-001, REQ-056-006, FEAT-056-001)
   - Inline: 1 marker (REQ-056-006)
   - Manifest updated: code array for FEAT-056-001
   - Validation: PASS (all markers reference valid IDs)

   Files modified:
   - src/traceability/validator.py (markers added)
   - feature-manifest.yaml (code reference updated)"

Result: Code properly linked to requirements and features
```

**Key Pattern**: Read manifest for IDs → Read code → Edit markers → Update manifest → Validate

---

### Workflow 3: Validating Traceability with Bash Tool

```markdown
User: "Check traceability compliance for this project"

Claude (Phase 1: Run Validation - 0-5k tokens):
1. Execute validation script:
   Bash: python scripts/validate-traceability.py

2. Capture output:
   # Example output:
   # ✅ Rule 1: Forward Linkage - 12/12 vision outcomes linked
   # ✅ Rule 2: Bidirectional Linkage - 45/45 docs have code references
   # ❌ Rule 3: Evidence Requirement - 8/10 features have tests (FAIL)
   # ✅ Rule 4: Closed Loop - 25/25 commits linked to tasks
   # ⚠️  Rule 5: Orphan Detection - 3 orphaned code files (WARNING)
   # ...
   # Compliance Level: L2 (Substantial) - 70% coverage

Claude (Phase 2: Analyze Failures - 5-10k tokens):
3. Read feature-manifest.yaml to identify failing features:
   Read feature-manifest.yaml
   # Find features without tests (Rule 3 failure)

4. Determine fixes needed:
   # FEAT-056-003: Missing tests
   # FEAT-056-007: Missing tests
   # 3 orphaned code files: src/utils/helper.py, src/deprecated/old.py, src/temp/debug.py

Claude (Phase 3: Fix Violations - 10-30k tokens):
5. Create missing tests:
   Write tests/test_feat_056_003.py
   Write tests/test_feat_056_007.py

6. Update manifest with test linkage:
   Edit feature-manifest.yaml
   # Add tests array for FEAT-056-003 and FEAT-056-007

7. Link orphaned files or mark as infrastructure:
   Edit feature-manifest.yaml
   # Add src/utils/helper.py to FEAT-056-005 (utility feature)
   # Add deprecated files to FEAT-056-999 (infrastructure/deprecated)

Claude (Phase 4: Re-Validate - 30-35k tokens):
8. Run validation again:
   Bash: python scripts/validate-traceability.py

9. Verify all rules pass:
   # ✅ All 10 rules passing
   # Compliance Level: L3 (Complete) - 100% coverage

Claude (Phase 5: Generate Report - 35-40k tokens):
10. Create compliance report:
    Bash: python scripts/validate-traceability.py --report > traceability-report.md

Claude (response to user):
"✅ Traceability compliance achieved:
   - Compliance Level: L3 (Complete) - 100% coverage
   - Fixed: 2 features missing tests
   - Fixed: 3 orphaned code files linked
   - Validation: All 10 rules passing

   Report generated: traceability-report.md
   Token usage: 38k/200k"

Result: Complete traceability compliance with automated validation
```

**Key Pattern**: Bash validation → Read manifest → Fix violations → Re-validate → Generate report

---

### Workflow 4: Creating Feature Entry with Write/Edit Tools

```markdown
User: "Create feature entry for new authentication module"

Claude (Phase 1: Understand Feature - 0-5k tokens):
1. Gather feature information from user:
   # Feature: Authentication module (OAuth2 + JWT)
   # Requirements: REQ-AUTH-001 (OAuth2), REQ-AUTH-002 (JWT validation)
   # Vision: docs/vision/security-vision.md

Claude (Phase 2: Check Manifest Structure - 5-10k tokens):
2. Read existing manifest for structure:
   Read feature-manifest.yaml
   # Learn YAML structure and ID numbering

3. Determine next feature ID:
   # Last feature: FEAT-056-007
   # Next ID: FEAT-AUTH-001 (domain-specific numbering)

Claude (Phase 3: Create Feature Entry - 10-15k tokens):
4. Edit manifest to add new feature:
   Edit feature-manifest.yaml

   # Add to features array:
   - id: FEAT-AUTH-001
     name: "OAuth2 + JWT Authentication"
     description: "Implement OAuth2 authorization flow with JWT token validation"
     status: draft
     created: "2025-11-20"
     vision_ref: "docs/vision/security-vision.md"
     requirements:
       - id: REQ-AUTH-001
         description: "OAuth2 authorization flow (authorization code grant)"
         status: draft
       - id: REQ-AUTH-002
         description: "JWT token validation with RS256 signature"
         status: draft
     code: []  # Will populate after implementation
     tests: []  # Will populate after writing tests
     documentation: []  # Will populate after writing docs
     git_commits: []  # Will populate after first commit

Claude (Phase 4: Validate Entry - 15-20k tokens):
5. Validate manifest schema:
   Bash: python -c "import yaml, jsonschema; manifest = yaml.safe_load(open('feature-manifest.yaml')); schema = yaml.safe_load(open('schemas/feature-manifest.yaml')); jsonschema.validate(manifest, schema)"

6. Check feature-specific validation:
   Bash: python scripts/validate-traceability.py --feature FEAT-AUTH-001

Claude (response to user):
"✅ Feature entry created:
   - Feature ID: FEAT-AUTH-001
   - Status: draft
   - Requirements: 2 (REQ-AUTH-001, REQ-AUTH-002)
   - Vision link: docs/vision/security-vision.md
   - Schema validation: PASS

   Next steps:
   1. Implement code (add to code array)
   2. Write tests (add to tests array with pytest markers)
   3. Write docs (add to documentation array with frontmatter)
   4. Update status: draft → in_progress → implemented

   File modified: feature-manifest.yaml"

Result: Feature entry created with complete metadata, ready for implementation
```

**Key Pattern**: Read manifest structure → Edit to add entry → Bash validation → Guide next steps

---

### Workflow 5: Impact Analysis with Grep and Read Tools

```markdown
User: "What would break if I change FEAT-056-001?"

Claude (Phase 1: Query Manifest Dependencies - 0-5k tokens):
1. Read feature manifest:
   Read feature-manifest.yaml

2. Search for features depending on FEAT-056-001:
   # Grep for requirements that reference this feature
   # (In this case, FEAT-056-001 defines the manifest schema itself)

Claude (Phase 2: Find Code Dependencies - 5-10k tokens):
3. Search for code markers:
   Bash: grep -r "FEAT-056-001" src/ tests/ --include="*.py"

   # Output:
   # src/traceability/validator.py:        - FEAT-056-001: Feature manifest schema
   # tests/test_feature_manifest.py:@pytest.mark.feature("FEAT-056-001")

4. Find test dependencies:
   Bash: grep -r "@pytest.mark.feature(\"FEAT-056-001\")" tests/

   # Output:
   # tests/test_feature_manifest.py:@pytest.mark.feature("FEAT-056-001")

Claude (Phase 3: Find Documentation Dependencies - 10-15k tokens):
5. Search docs for references:
   Bash: grep -r "FEAT-056-001" docs/ --include="*.md"

   # Output:
   # docs/skilled-awareness/lifecycle-traceability/protocol-spec.md:feature_refs: [FEAT-056-001]
   # docs/skilled-awareness/lifecycle-traceability/capability-charter.md:Example: FEAT-056-001

Claude (Phase 4: Find Features Using This Feature's Requirements - 15-20k tokens):
6. Check if other features depend on requirements from FEAT-056-001:
   # Read manifest to find features referencing REQ-056-001 or REQ-056-006

   Read feature-manifest.yaml
   # Search for requirement references in other features

Claude (Phase 5: Generate Impact Report - 20-25k tokens):
7. Compile impact analysis:
   # Direct dependencies:
   # - Code: src/traceability/validator.py (uses schema)
   # - Tests: tests/test_feature_manifest.py (validates schema)
   # - Docs: protocol-spec.md, capability-charter.md (document schema)
   #
   # Indirect dependencies:
   # - FEAT-056-002 depends on REQ-056-001 (which FEAT-056-001 implements)
   # - All features using feature-manifest.yaml depend on schema structure

Claude (response to user):
"⚠️ FEAT-056-001 Impact Analysis:

Direct dependencies (WILL break):
- src/traceability/validator.py (schema validation logic)
- tests/test_feature_manifest.py (schema validation tests)
- docs/skilled-awareness/lifecycle-traceability/protocol-spec.md (schema docs)

Indirect dependencies (MIGHT break):
- All 7 features in manifest (depend on schema structure)
- FEAT-056-002 (validation rules - uses schema constraints)
- Scripts: validate-traceability.py, generate-feature-manifest.py

Recommendation:
- Schema changes are HIGH RISK (affects all features)
- Create migration plan for schema updates
- Add deprecation warnings before removing fields
- Test all 7 features after schema changes

Token usage: 22k/200k"

Result: Complete impact analysis preventing breaking changes
```

**Key Pattern**: Read manifest → Grep code/tests/docs → Analyze dependencies → Report impact + recommendations

---

## Claude-Specific Tool Patterns

### Read Tool: Querying feature-manifest.yaml

**Pattern 1: Read entire manifest**
```markdown
Read feature-manifest.yaml
# Use when: Need to understand all features or analyze structure
# Token cost: ~5-10k tokens (depending on manifest size)
```

**Pattern 2: Read specific feature section**
```markdown
Read feature-manifest.yaml
# Then parse in memory for specific feature ID
# Alternatively: Use Bash with yq/grep for targeted extraction
# Use when: Only need one feature's data
# Token cost: 5k tokens (manifest) vs 1k tokens (Bash extraction)
```

**Pattern 3: Validate manifest schema**
```markdown
Read schemas/feature-manifest.yaml
# Understand schema structure before creating entries
# Use when: Creating new feature entries or updating structure
# Token cost: ~2-3k tokens
```

---

### Edit Tool: Adding Traceability Markers

**Pattern 1: Add docstring markers**
```markdown
Edit src/module/file.py

# Old:
def my_function():
    """Function description."""
    pass

# New:
def my_function():
    """
    Function description.

    Traceability:
        - REQ-XXX-001: Requirement description
        - FEAT-XXX-001: Feature this implements
    """
    pass
```

**Pattern 2: Add inline markers**
```markdown
Edit src/module/file.py

# Old:
if condition:
    do_something()

# New:
# REQ-XXX-001: Implementation of requirement 1
if condition:
    # FEAT-XXX-001: Feature-specific logic
    do_something()
```

**Pattern 3: Update feature-manifest.yaml**
```markdown
Edit feature-manifest.yaml

# Add code reference to existing feature:
code:
  - path: "src/module/file.py"
    lines: "10-50"
    commit: "abc123def"  # Git SHA
```

---

### Bash Tool: Validation and Queries

**Pattern 1: Run full validation**
```bash
Bash: python scripts/validate-traceability.py
# Output: 10-rule validation report with compliance level
```

**Pattern 2: Validate specific feature**
```bash
Bash: python scripts/validate-traceability.py --feature FEAT-XXX-001
# Output: Validation results for single feature
```

**Pattern 3: Check markers only**
```bash
Bash: python scripts/validate-traceability.py --check-markers
# Output: Marker integrity report (all markers reference valid IDs)
```

**Pattern 4: Generate compliance report**
```bash
Bash: python scripts/validate-traceability.py --report > report.md
# Output: Markdown report with detailed findings
```

**Pattern 5: Auto-generate manifest**
```bash
Bash: python scripts/generate-feature-manifest.py --from-git --output feature-manifest-draft.yaml
# Output: Draft manifest generated from git log and beads tasks
```

**Pattern 6: Query manifest with yq**
```bash
# Find all code files for feature
Bash: yq eval '.features[] | select(.id == "FEAT-XXX-001") | .code[].path' feature-manifest.yaml

# Find all tests for feature
Bash: yq eval '.features[] | select(.id == "FEAT-XXX-001") | .tests[].path' feature-manifest.yaml

# Find features with status=draft
Bash: yq eval '.features[] | select(.status == "draft") | .id' feature-manifest.yaml
```

**Pattern 7: Search for markers**
```bash
# Find all requirement markers
Bash: grep -r "REQ-" src/ tests/ --include="*.py"

# Find all feature markers
Bash: grep -r "FEAT-" src/ tests/ docs/ --include="*.py" --include="*.md"
```

---

## Progressive Loading for Traceability

### Phase 1: Essential Context (0-10k tokens)

**Use when**: Quick queries, single feature context, validation runs

**Load**:
- feature-manifest.yaml (5-10k tokens)
- Target feature entry only (extract with yq/grep)
- Validation output (1-2k tokens)

**Example**:
```markdown
User: "Show me FEAT-056-001"
Claude: Read feature-manifest.yaml (10k tokens)
Claude: Extract feature entry (0 additional tokens, in-memory)
Result: 10k tokens total
```

---

### Phase 2: Standard Context (10-30k tokens)

**Use when**: Implementing features, adding markers, updating manifest

**Load**:
- feature-manifest.yaml (5-10k tokens)
- Target code files (5-10k tokens)
- Related test files (3-5k tokens)
- Validation results (1-2k tokens)

**Example**:
```markdown
User: "Add traceability to validator.py"
Claude: Read feature-manifest.yaml (10k tokens)
Claude: Read src/traceability/validator.py (5k tokens)
Claude: Read tests/test_validator.py (3k tokens)
Claude: Bash validate-traceability.py (2k tokens)
Result: 20k tokens total
```

---

### Phase 3: Comprehensive Context (30-50k+ tokens)

**Use when**: Impact analysis, compliance audits, architecture changes

**Load**:
- feature-manifest.yaml (5-10k tokens)
- All code files for feature(s) (10-20k tokens)
- All test files for feature(s) (5-10k tokens)
- All documentation for feature(s) (5-10k tokens)
- Validation report (2-5k tokens)
- Related features (5-10k tokens)

**Example**:
```markdown
User: "Impact analysis for FEAT-056-001"
Claude: Read feature-manifest.yaml (10k tokens)
Claude: Read all code files (15k tokens)
Claude: Read all test files (8k tokens)
Claude: Read all docs (7k tokens)
Claude: Grep dependencies (2k tokens)
Result: 42k tokens total
```

---

## Claude-Specific Tips

### Tip 1: Use yq/grep for Targeted Manifest Queries

**Pattern**:
```markdown
# ❌ BAD: Read entire manifest for one feature (10k tokens)
Read feature-manifest.yaml
# Parse in memory for FEAT-XXX-001

# ✅ GOOD: Extract feature with Bash (1k tokens)
Bash: yq eval '.features[] | select(.id == "FEAT-XXX-001")' feature-manifest.yaml
# Or: grep -A 30 "id: FEAT-XXX-001" feature-manifest.yaml
```

**Why**: Save 9k tokens per query when manifest grows large

---

### Tip 2: Validate Before Committing

**Pattern**:
```markdown
# After making traceability changes:
1. Edit code/manifest files
2. Bash: python scripts/validate-traceability.py
3. Fix violations immediately
4. Re-run validation until passing
5. Commit

# Don't commit without validation (creates tech debt)
```

**Why**: Easier to fix violations immediately than retroactively

---

### Tip 3: Use Edit Tool for Markers, Not Write

**Pattern**:
```markdown
# ✅ GOOD: Edit existing code file
Edit src/module/file.py
# Add markers to existing function

# ❌ BAD: Write entire file (risky, loses comments/formatting)
Write src/module/file.py
# Recreate entire file just to add markers
```

**Why**: Edit tool preserves existing code structure and formatting

---

### Tip 4: Read Schema Before Creating Entries

**Pattern**:
```markdown
# Before creating feature entry:
1. Read schemas/feature-manifest.yaml (understand structure)
2. Read feature-manifest.yaml (see examples)
3. Edit feature-manifest.yaml (add new entry)
4. Bash validate (check schema compliance)
```

**Why**: Schema defines required fields and validation rules

---

### Tip 5: Use Progressive Loading for Impact Analysis

**Pattern**:
```markdown
# Phase 1: Read manifest only (10k tokens)
Read feature-manifest.yaml
# Identify dependencies

# Phase 2: Grep for code markers (2k tokens)
Bash: grep -r "FEAT-XXX-001" src/ tests/
# Find direct code dependencies

# Phase 3: Read dependent files only if needed (10-20k tokens)
Read src/dependent/file1.py
Read tests/dependent/test1.py
# Only load files that actually depend on feature

# Don't load all code upfront (wasteful)
```

**Why**: Most impact analyses need manifest + grep, not full codebase

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Reading Manifest Before Edits

**Problem**: Edit code or add markers without checking manifest for feature/requirement IDs

**Fix**: ALWAYS read feature-manifest.yaml first
```markdown
# ✅ GOOD workflow:
1. Read feature-manifest.yaml (find IDs)
2. Edit code (add markers with correct IDs)
3. Edit manifest (update code array)
4. Bash validate

# ❌ BAD workflow:
1. Edit code (guess marker IDs)
2. Markers reference non-existent features
3. Validation fails
```

**Why**: Manifest is single source of truth for IDs

---

### Pitfall 2: Forgetting Bidirectional Linkage

**Problem**: Edit code to add manifest reference, but forget to update manifest with code reference

**Fix**: Update BOTH sides when creating linkage
```markdown
# ✅ GOOD:
1. Edit code (add # FEAT-XXX-001 marker)
2. Edit feature-manifest.yaml (add code path to FEAT-XXX-001)
3. Validate bidirectional linkage

# ❌ BAD:
1. Edit code (add marker)
2. Forget to update manifest
3. Rule 2 (Bidirectional Linkage) fails
```

**Why**: Rule 2 enforces consistency between code and manifest

---

### Pitfall 3: Not Validating After Changes

**Problem**: Make traceability changes, commit without validation

**Fix**: ALWAYS run validation before committing
```markdown
# ✅ GOOD:
1. Edit code/manifest
2. Bash: python scripts/validate-traceability.py
3. Fix violations
4. Re-validate
5. Commit

# ❌ BAD:
1. Edit code/manifest
2. Commit without validation
3. CI/CD fails (validation errors)
```

**Why**: Validation catches errors immediately, before code review

---

### Pitfall 4: Loading Full Codebase for Single Feature

**Problem**: Read all code files when analyzing single feature

**Fix**: Use manifest to target specific files
```markdown
# ✅ GOOD:
1. Read feature-manifest.yaml
2. Extract FEAT-XXX-001 code paths
3. Read only those files (targeted loading)

# ❌ BAD:
1. Read src/**/*.py (all code, 100k tokens)
2. Search for feature references manually
3. Token budget exhausted
```

**Why**: Manifest provides file paths, eliminates blind search

---

### Pitfall 5: Creating Features Without Requirements

**Problem**: Add feature entry with empty requirements array

**Fix**: Define requirements before implementation
```markdown
# ✅ GOOD:
1. Create feature entry with ≥1 requirement
2. Implement code referencing requirements
3. Write tests validating requirements
4. Rule 8 (Requirement Coverage) passes

# ❌ BAD:
1. Create feature with requirements: []
2. Implement code without markers
3. Rule 8 fails (no requirement coverage)
```

**Why**: Requirements drive implementation and testing

---

## Support & Resources

**SAP-056 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic traceability patterns
- [capability-charter.md](capability-charter.md) - Problem statement, solution design
- [protocol-spec.md](protocol-spec.md) - Traceability schemas, validation rules
- [adoption-blueprint.md](adoption-blueprint.md) - L0→L3 adoption steps
- [ledger.md](ledger.md) - Adoption tracking, version history

**Key Files**:
- feature-manifest.yaml - Single source of truth for features
- schemas/feature-manifest.yaml - JSON Schema for manifest
- scripts/validate-traceability.py - 10-rule validation suite
- scripts/generate-feature-manifest.py - Auto-generation tool

**Related SAPs**:
- [SAP-004 (testing-framework)](../testing-framework/) - pytest markers for requirements
- [SAP-007 (documentation-framework)](../documentation-framework/) - Frontmatter for doc↔code linkage
- [SAP-010 (memory-system)](../memory-system/) - A-MEM events with feature_id
- [SAP-015 (task-tracking)](../task-tracking/) - Beads tasks with feature references

---

## Example Claude Code Session

```markdown
User: "Add traceability for the new authentication feature"

Claude (Phase 1: Read Context - 0-10k tokens):
1. Read feature-manifest.yaml
   # Find FEAT-AUTH-001 entry
   # Extract requirement IDs: REQ-AUTH-001, REQ-AUTH-002

2. Read code file:
   Read src/auth/oauth2.py
   # Locate functions to annotate

Claude (Phase 2: Add Markers - 10-15k tokens):
3. Edit code with traceability markers:
   Edit src/auth/oauth2.py

   # Add docstring markers:
   def authorize():
       """
       Implement OAuth2 authorization flow.

       Traceability:
           - REQ-AUTH-001: OAuth2 authorization code grant
           - FEAT-AUTH-001: Authentication module
       """

4. Edit manifest with code reference:
   Edit feature-manifest.yaml

   # Update FEAT-AUTH-001:
   code:
     - path: "src/auth/oauth2.py"
       lines: "10-150"
       commit: "pending"

Claude (Phase 3: Validate - 15-20k tokens):
5. Run validation:
   Bash: python scripts/validate-traceability.py --feature FEAT-AUTH-001

6. Check output:
   # ✅ All rules passing for FEAT-AUTH-001

Claude (response):
"✅ Traceability added for FEAT-AUTH-001:
   - Code markers: 5 functions annotated
   - Manifest updated: 1 code file linked
   - Validation: PASS

   Files modified:
   - src/auth/oauth2.py (markers)
   - feature-manifest.yaml (linkage)

   Token usage: 18k/200k"

Result: Feature properly linked with validated traceability
Time: 5 minutes (vs 30 min manual)
```

---

## Version History

- **1.0.0** (2025-11-20): Initial CLAUDE.md for lifecycle traceability
  - 5 workflows: Query manifest, add markers, validate, create feature, impact analysis
  - Tool patterns: Read for manifest, Edit for markers, Bash for validation
  - Progressive loading phases (0-10k, 10-30k, 30-50k+ tokens)
  - 5 Claude-specific tips, 5 common pitfalls
  - Example session demonstrating end-to-end traceability workflow

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic traceability patterns
2. Review [protocol-spec.md](protocol-spec.md) for validation rules and schemas
3. Check [capability-charter.md](capability-charter.md) for design rationale
4. Explore feature-manifest.yaml to understand structure
