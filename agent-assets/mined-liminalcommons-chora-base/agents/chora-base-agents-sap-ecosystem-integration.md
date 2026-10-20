# SAP Ecosystem Integration (SAP-061) - Agent Awareness

**SAP ID**: SAP-061
**Version**: 1.0.0
**Status**: Draft
**Last Updated**: 2025-11-20

---

## 📖 Quick Reference

**New to SAP-061?** → Read **[capability-charter.md](capability-charter.md)** first (10-min read)

The capability charter provides:
- 🚀 **Problem Statement** - Integration gaps discovered too late (SAP-053 INDEX.md omission)
- 📚 **Solution Overview** - 5 integration points validated automatically
- 🎯 **Core Capability** - Automated ecosystem integration validation
- 🔧 **Integration Points** - INDEX.md, sap-catalog.json, copier.yml, adoption paths, dependencies
- 📊 **Performance** - <2s for full ecosystem validation (all 48 SAPs)
- 🔗 **Pre-commit Hook** - Prevents incomplete integrations from being committed

This AGENTS.md provides: Agent-specific patterns for implementing SAP-061.

---

## Common Workflows

### Workflow 1: Validating a Single SAP

**When to use**: After completing SAP development, before final commit

**Steps**:
1. Run validator: `python scripts/validate-ecosystem-integration.py SAP-XXX`
2. Review output (5 integration points checked)
3. Fix any failures reported
4. Re-run until validation passes

**Example (SAP-053 validation)**:
```bash
$ python scripts/validate-ecosystem-integration.py SAP-053

✅ Validating SAP-053 Ecosystem Integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ INDEX.md: SAP-053 found in domain section
✅ sap-catalog.json: SAP-053 metadata exists
✅ copier.yml: SAP-053 available for distribution (status=pilot)
✅ Dependencies: All referenced SAPs exist (SAP-000, SAP-009, SAP-056)
⚠️  Progressive Adoption Path: Not checked (status=pilot, not active)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Result: PASS (4/4 required checks, 1 skipped)
Exit code: 0
```

**Outcome**: SAP-053 fully integrated, ready for commit

---

### Workflow 2: Validating All SAPs

**When to use**: Weekly health check, before releases, after bulk updates

**Steps**:
1. Run full validation: `python scripts/validate-ecosystem-integration.py --all`
2. Review summary (number of SAPs passed/failed)
3. Identify gaps with detailed output
4. Fix failures systematically (highest priority first)
5. Re-run until all SAPs pass

**Example (full ecosystem validation)**:
```bash
$ python scripts/validate-ecosystem-integration.py --all

✅ Validating All SAPs in Ecosystem
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Validated 48 SAPs in 1.4s
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ PASSED: 47 SAPs
❌ FAILED: 1 SAP
  - SAP-029: Missing from INDEX.md

Performance: 1.4s total (target: <2s)
Exit code: 1
```

**Outcome**: Ecosystem health report, actionable gap list

---

### Workflow 3: Installing Pre-Commit Hook

**When to use**: One-time setup for SAP development workflow

**Steps**:
1. Copy hook to git hooks directory:
   ```bash
   cp scripts/git-hooks/pre-commit-ecosystem .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   ```
2. Test hook manually:
   ```bash
   .git/hooks/pre-commit
   ```
3. Commit changes (hook runs automatically)
4. If validation fails, fix gaps before committing

**Example (hook preventing incomplete integration)**:
```bash
$ git commit -m "Add SAP-062"

Running SAP Ecosystem Integration Check...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ SAP-062: Missing from sap-catalog.json

Cannot commit: SAP integration incomplete.
Fix gaps and try again, or use --no-verify to skip (not recommended).

Exit code: 2
```

**Outcome**: Prevents committing incomplete SAP integrations

---

### Workflow 4: Fixing Integration Gaps

**When to use**: After validation identifies failures

**Steps**:
1. Read validator output (exit code indicates failure type)
2. Fix based on integration point:
   - **Exit code 1 (INDEX.md)**: Add SAP entry to appropriate domain section
   - **Exit code 2 (sap-catalog.json)**: Add SAP metadata to catalog
   - **Exit code 3 (copier.yml)**: Add SAP to Copier template questions
   - **Exit code 4 (Dependencies)**: Fix broken SAP references or add missing SAPs
   - **Exit code 5 (Multiple)**: Fix all failures in order
3. Re-run validation: `python scripts/validate-ecosystem-integration.py SAP-XXX`
4. Repeat until exit code 0

**Example (fixing INDEX.md gap)**:
```bash
# Step 1: Validator identifies gap
$ python scripts/validate-ecosystem-integration.py SAP-062
❌ INDEX.md: SAP-062 not found in INDEX.md
Exit code: 1

# Step 2: Add SAP-062 to INDEX.md
# (Edit docs/skilled-awareness/INDEX.md, add entry under appropriate domain)

# Step 3: Re-validate
$ python scripts/validate-ecosystem-integration.py SAP-062
✅ INDEX.md: SAP-062 found in domain section
✅ All checks passed
Exit code: 0
```

**Outcome**: All integration gaps fixed, SAP ready for commit

---

### Workflow 5: Running Validation in CI/CD

**When to use**: Automated validation in GitHub Actions or other CI/CD

**Steps**:
1. Add validation step to CI workflow:
   ```yaml
   - name: Validate SAP Ecosystem Integration
     run: python scripts/validate-ecosystem-integration.py --all --json
   ```
2. Parse JSON output for failures:
   ```bash
   # JSON output structure:
   # {
   #   "total_saps": 48,
   #   "passed": 47,
   #   "failed": 1,
   #   "failures": [
   #     {
   #       "sap_id": "SAP-029",
   #       "failed_checks": [
   #         {"integration_point": "INDEX.md", "message": "..."}
   #       ]
   #     }
   #   ],
   #   "exit_code": 1
   # }
   ```
3. Fail CI build if exit code non-zero
4. Report failures in PR comments or Slack

**Example (GitHub Actions integration)**:
```yaml
name: SAP Validation

on: [push, pull_request]

jobs:
  validate-ecosystem:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Validate SAP Ecosystem Integration
        run: |
          python scripts/validate-ecosystem-integration.py --all --json > validation.json
          exit_code=$?
          if [ $exit_code -ne 0 ]; then
            echo "❌ SAP ecosystem validation failed"
            cat validation.json | jq '.failures'
            exit $exit_code
          fi
          echo "✅ All SAPs fully integrated"
```

**Outcome**: Automated validation on every commit/PR

---

## Integration with Other SAPs

### SAP-000 (sap-framework)
- **Relationship**: SAP-061 validates SAP-000's 5-artifact pattern compliance
- **Integration**: Validator checks for required artifacts (capability-charter.md presence)
- **Pattern**: Use SAP-000 protocol-spec.md to understand artifact requirements

### SAP-050 (sap-catalog)
- **Relationship**: SAP-061 validates sap-catalog.json completeness
- **Integration**: Checks metadata presence (id, name, status, version, dependencies)
- **Pattern**: sap-catalog.json is the source of truth for SAP metadata

### SAP-056 (lifecycle-traceability)
- **Relationship**: SAP-061 validates dependency references (integration point 5)
- **Integration**: Ensures all referenced SAPs exist and are valid
- **Pattern**: Broken dependency detection prevents invalid SAP references

### SAP-029 (sap-generation)
- **Relationship**: SAP-061 validation should run after SAP-029 generates artifacts
- **Integration**: Post-generation validation ensures complete ecosystem integration
- **Pattern**: Generate → Validate → Fix gaps → Re-validate

---

## Performance Metrics

### Validation Speed

| Metric | Target | Typical | Notes |
|--------|--------|---------|-------|
| **Single SAP validation** | <100ms | 50-80ms | 5 integration points checked |
| **All SAPs validation (48)** | <2s | 1.4-1.8s | Parallel processing |
| **INDEX.md parsing** | <50ms | 20-30ms | Cached after first read |
| **sap-catalog.json parsing** | <50ms | 10-20ms | Single JSON read |
| **Dependency resolution** | <200ms | 100-150ms | Recursive checks |

### Exit Code Distribution (Typical)

| Exit Code | Meaning | Frequency | Fix Time |
|-----------|---------|-----------|----------|
| **0 (PASS)** | All checks passed | 95%+ | N/A |
| **1 (INDEX.md)** | Missing from INDEX.md | 3% | 2-5 min |
| **2 (catalog)** | Missing from sap-catalog.json | 1% | 3-5 min |
| **3 (copier)** | Missing from copier.yml | <1% | 5-10 min |
| **4 (deps)** | Broken dependencies | <1% | 5-15 min |
| **5 (multiple)** | Multiple failures | <1% | 10-20 min |

---

## Common Patterns

### Pattern 1: Pre-Release Validation Checklist

**Context**: Before marking a SAP as "active" or creating a release

**Steps**:
1. Complete all 5 SAP artifacts
2. Run `python scripts/validate-ecosystem-integration.py SAP-XXX`
3. Fix all integration gaps (exit code 0 required)
4. Run full ecosystem validation: `--all`
5. Ensure no regressions (all SAPs still pass)
6. Update SAP status to "active" in capability-charter.md and sap-catalog.json
7. Re-validate (adoption path check now applies)
8. Commit with pre-commit hook enabled

**Outcome**: SAP ready for production use

---

### Pattern 2: Bulk SAP Update Workflow

**Context**: Updating multiple SAPs simultaneously (e.g., status changes, dependency updates)

**Steps**:
1. Create feature branch: `git checkout -b bulk-sap-updates`
2. Make changes to SAPs
3. Run validation after each SAP: `python scripts/validate-ecosystem-integration.py SAP-XXX`
4. After all changes, run full validation: `--all`
5. Fix any integration gaps discovered
6. Re-run `--all` until exit code 0
7. Commit (pre-commit hook validates)
8. Create PR with validation report

**Outcome**: Bulk updates with ecosystem consistency guaranteed

---

### Pattern 3: New SAP Development Workflow

**Context**: Creating a new SAP from scratch

**Steps**:
1. Generate SAP artifacts (via SAP-029 or manually)
2. Add SAP to sap-catalog.json immediately (prevents exit code 2)
3. Add SAP to INDEX.md immediately (prevents exit code 1)
4. If status=active/pilot, add to copier.yml (prevents exit code 3)
5. Run validation: `python scripts/validate-ecosystem-integration.py SAP-XXX`
6. Fix any dependency issues (exit code 4)
7. Complete SAP content (fill TODOs, write docs)
8. Re-validate before final commit
9. Commit with pre-commit hook

**Outcome**: SAP integrated from day 1, no post-completion gaps

---

## Troubleshooting

### Issue 1: Validation Fails with "SAP directory not found"

**Symptom**: `SAP-XXX directory not found in docs/skilled-awareness/`

**Cause**: capability-charter.md missing or doesn't contain SAP ID

**Fix**:
1. Verify capability-charter.md exists: `ls docs/skilled-awareness/{sap-name}/capability-charter.md`
2. Check SAP ID in charter:
   ```bash
   grep "SAP ID" docs/skilled-awareness/{sap-name}/capability-charter.md
   ```
3. Ensure format matches: `**SAP ID**: SAP-XXX` or `SAP ID: SAP-XXX`

---

### Issue 2: INDEX.md Check Fails but SAP is Present

**Symptom**: Exit code 1, but SAP visible in INDEX.md

**Cause**: Entry format doesn't match expected pattern `### SAP-XXX: Name`

**Fix**:
1. Check INDEX.md entry format:
   ```markdown
   ### SAP-053: Multi-Interface Conformance
   ```
2. Ensure no extra spaces, correct heading level (###), colon after SAP ID

---

### Issue 3: Copier.yml Check False Positive

**Symptom**: Exit code 3 for SAP with status=draft

**Cause**: Copier check only applies to status=active or pilot

**Fix**: No action needed. Draft SAPs are not required to be in copier.yml.

---

### Issue 4: Dependency Check Fails for Valid SAP

**Symptom**: Exit code 4, "SAP-XXX not found" but SAP exists

**Cause**: Referenced SAP's capability-charter.md missing or invalid

**Fix**:
1. Run validation on referenced SAP: `python scripts/validate-ecosystem-integration.py SAP-XXX`
2. Fix referenced SAP first
3. Re-validate original SAP

---

### Issue 5: Slow Validation Performance (>2s)

**Symptom**: `--all` validation takes >2s

**Cause**: Large number of SAPs or I/O bottleneck

**Fix**:
1. Check SAP count: `ls docs/skilled-awareness/ | wc -l`
2. Profile validation: `python scripts/validate-ecosystem-integration.py --all --verbose`
3. If >60 SAPs, consider caching or parallel processing enhancements

---

## Best Practices

### For SAP Developers

1. **Add to catalog and INDEX.md immediately** when creating new SAP (prevents most common failures)
2. **Run validation after every major change** (status update, dependency change, etc.)
3. **Enable pre-commit hook** to catch gaps before commit
4. **Use `--json` output in CI/CD** for automated reporting
5. **Validate dependencies before referencing** (run validation on referenced SAP first)

### For Ecosystem Maintainers

1. **Run `--all` validation weekly** to catch drift
2. **Review exit code distribution** to identify systemic issues
3. **Update adoption paths** when SAPs reach "active" status
4. **Use validation in release gates** (no release unless all SAPs pass)
5. **Monitor performance metrics** (<2s target for full validation)

### For AI Agents

1. **Always validate after SAP creation** (part of standard workflow)
2. **Parse `--json` output** for programmatic integration
3. **Fix gaps in priority order** (INDEX.md → catalog → copier → deps)
4. **Re-validate after fixes** (don't assume fix worked)
5. **Update AGENTS.md** to reflect SAP-061 adoption

---

## Quick Commands Reference

```bash
# Validate single SAP
python scripts/validate-ecosystem-integration.py SAP-053

# Validate all SAPs
python scripts/validate-ecosystem-integration.py --all

# JSON output (for automation)
python scripts/validate-ecosystem-integration.py SAP-053 --json

# Verbose output (debugging)
python scripts/validate-ecosystem-integration.py SAP-053 --verbose

# Install pre-commit hook
cp scripts/git-hooks/pre-commit-ecosystem .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Test pre-commit hook manually
.git/hooks/pre-commit

# Check validator version
python scripts/validate-ecosystem-integration.py --version
```

---

## Exit Code Reference

| Code | Meaning | Priority | Fix Action |
|------|---------|----------|------------|
| 0 | All checks passed | N/A | None needed |
| 1 | Missing from INDEX.md | High | Add SAP entry to appropriate domain |
| 2 | Missing from sap-catalog.json | High | Add SAP metadata to catalog |
| 3 | Missing from copier.yml | Medium | Add SAP to Copier questions (if distributable) |
| 4 | Broken dependencies | Medium | Fix SAP references or add missing SAPs |
| 5 | Multiple failures | High | Fix all gaps, prioritize INDEX.md and catalog |
| 6 | Usage error or invalid SAP ID | N/A | Check SAP ID format (SAP-XXX) |

---

## Integration Point Details

### 1. INDEX.md
- **Location**: `docs/skilled-awareness/INDEX.md`
- **Required Format**: `### SAP-XXX: Name`
- **Required For**: All SAPs (draft, pilot, active)
- **Validation**: Pattern matching for SAP ID entry

### 2. sap-catalog.json
- **Location**: `sap-catalog.json` (repo root)
- **Required Fields**: id, name, status, version, dependencies
- **Required For**: All SAPs (draft, pilot, active)
- **Validation**: JSON parsing + field presence

### 3. copier.yml
- **Location**: `copier.yml` (repo root)
- **Required For**: SAPs with status=active or pilot
- **Validation**: YAML parsing + SAP reference check
- **Skipped**: Draft SAPs (not distributable)

### 4. Progressive Adoption Path
- **Location**: `docs/user-docs/adoption-paths/*.md` (depends on domain)
- **Required For**: SAPs with status=active
- **Validation**: Markdown search for SAP mention
- **Skipped**: Draft and pilot SAPs (not recommended for adoption yet)

### 5. Dependencies
- **Source**: capability-charter.md (Dependencies field)
- **Required For**: All SAPs (draft, pilot, active)
- **Validation**: Recursive existence check for all referenced SAPs
- **Failure**: If any referenced SAP doesn't exist or is invalid

---

## Version History

- **1.0.0** (2025-11-20): Initial AGENTS.md for SAP-061
  - 5 common workflows (validate single, validate all, install hook, fix gaps, CI/CD)
  - Integration patterns with SAP-000, SAP-050, SAP-056, SAP-029
  - Performance metrics (<2s for 48 SAPs)
  - 3 development patterns (pre-release, bulk updates, new SAP workflow)
  - 5 troubleshooting scenarios with fixes
  - Quick commands reference + exit code reference
  - Integration point details (5 points documented)

---

**Next Steps**:
1. Read [capability-charter.md](capability-charter.md) for problem/solution design
2. Review [protocol-spec.md](protocol-spec.md) for complete validator specification
3. Check [adoption-blueprint.md](adoption-blueprint.md) for installation guide
4. Run first validation: `python scripts/validate-ecosystem-integration.py --all`
