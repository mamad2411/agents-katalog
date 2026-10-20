---
sap_id: SAP-016
version: 1.0.0
status: active
last_updated: 2025-11-04
type: reference
audience: agents
complexity: beginner
estimated_reading_time: 8
progressive_loading:
  phase_1: "lines 1-180"   # Quick Reference + Core Workflows
  phase_2: "lines 181-320" # Advanced Operations
  phase_3: "full"          # Complete including troubleshooting
phase_1_token_estimate: 3500
phase_2_token_estimate: 7000
phase_3_token_estimate: 9000
---

# Link Validation & Reference Management (SAP-016) - Agent Awareness

**SAP ID**: SAP-016
**Last Updated**: 2025-11-04
**Audience**: Generic AI Coding Agents

---

## 📖 Quick Reference

**New to SAP-016?** → Read **[README.md](README.md)** first (5-min read)

The README provides:
- 🚀 **Quick Start** - 2-minute setup with 5 validation commands (all, docs, path, CI, help)
- 📚 **Time Savings** - 5-10 min saved per refactoring session (automated link checking), <5s validation for 87 files with 342 links
- 🎯 **3 Validation Modes** - Full scan, changed files (git-aware), single file validation
- 🔧 **3 Link Types** - Internal relative paths, anchor links (#sections), external HTTP/HTTPS
- 📊 **4 Output Formats** - Human-readable, JSON, GitHub Actions annotations, JUnit XML
- 🔗 **Integration** - Works with SAP-006 (Quality Gates), SAP-005 (CI/CD), SAP-007 (Documentation), SAP-009 (Agent Awareness)

This AGENTS.md provides: Agent-specific patterns for link validation workflows, git-aware validation, and CI/CD integration.

---

## Detailed Quick Reference

### When to Use

**Use link validation (SAP-016) when**:
- Before committing documentation changes (validate changed files)
- After refactoring documentation structure (validate all links)
- Adding new markdown files with cross-references
- Updating external dependencies (check external links still valid)
- Before releasing new version (ensure documentation integrity)

**Don't use when**:
- Validating code comments (too noisy, often hypothetical)
- Checking commit message links (historical, immutable)
- Validating image assets (separate capability needed)
- Testing deep external link content (only checks reachability)

### Validation Script

```bash
# Validate all markdown files in repository
./scripts/validate-links.sh

# Validate specific directory
./scripts/validate-links.sh docs/skilled-awareness/sap-framework/

# Validate single file
./scripts/validate-links.sh docs/ARCHITECTURE.md

# Validate only changed files (faster)
./scripts/validate-links.sh --changed
```

### Link Types Validated

| Type | Example | Validated |
|------|---------|-----------|
| **Relative** | `../foo.md` | ✅ |
| **Absolute (repo)** | `/docs/foo.md` | ✅ |
| **Anchor** | `#section-name` | ✅ |
| **Cross-doc anchor** | `../foo.md#section` | ✅ |
| **External HTTP** | `https://example.com` | ✅ |

---

## User Signal Patterns

### Link Validation Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "validate links" | run_link_validation() | ./scripts/validate-links.sh | Full scan |
| "check broken links" | run_link_validation() | Same as above | Natural variation |
| "verify references" | run_link_validation() | Same intent | |
| "validate docs" | run_link_validation() | Implies link check | |
| "check links in SAP-003" | run_link_validation(path="sap-003") | Specific directory | |
| "validate changed files" | run_link_validation(mode="changed") | Git diff only | |

### Common Variations

**Validation Requests**:
- "validate links" / "check links" / "verify references" → run_link_validation()
- "check broken links" / "find broken links" / "any dead links?" → run_link_validation()

**Scoped Validation**:
- "validate links in X" / "check X references" → run_link_validation(path=X)
- "validate changed files" / "check my changes" → run_link_validation(mode="changed")

---

## Common Workflows

### Workflow 1: Validate All Links Before Commit (1-2 minutes)

**User signal**: "Validate links", "Check broken links", "Verify references"

**Purpose**: Ensure all markdown links are valid before committing changes

**Steps**:
1. Run validation script:
   ```bash
   ./scripts/validate-links.sh
   ```

2. Review output:
   ```
   Validating links in /path/to/repo...

   ✅ docs/ARCHITECTURE.md (10 links checked)
   ✅ docs/skilled-awareness/sap-framework/capability-charter.md (15 links checked)
   ❌ docs/skilled-awareness/inbox/AGENTS.md (2 broken links)
     - Line 34: ../non-existent-file.md (file not found)
     - Line 67: #invalid-anchor (anchor not found in target)

   Summary: 25/27 links valid (92.6%)
   ```

3. Fix broken links:
   ```markdown
   # Before (broken)
   [Protocol Spec](../non-existent-file.md)

   # After (fixed)
   [Protocol Spec](protocol-spec.md)
   ```

4. Re-validate to confirm fixes:
   ```bash
   ./scripts/validate-links.sh
   ```

**Expected outcome**: All links valid, ready to commit

---

### Workflow 2: Validate Specific Directory (30 seconds)

**User signal**: "Check links in SAP-016", "Validate docs/skilled-awareness/", "Verify references in X"

**Purpose**: Validate links in specific SAP or directory without full scan

**Steps**:
1. Run validation on specific path:
   ```bash
   ./scripts/validate-links.sh docs/skilled-awareness/link-validation-reference-management/
   ```

2. Review directory-specific results:
   ```
   Validating links in docs/skilled-awareness/link-validation-reference-management/...

   ✅ capability-charter.md (8 links checked)
   ✅ protocol-spec.md (12 links checked)
   ✅ awareness-guide.md (6 links checked)
   ✅ adoption-blueprint.md (4 links checked)
   ✅ ledger.md (2 links checked)

   Summary: 32/32 links valid (100%)
   ```

**Expected outcome**: Directory-scoped validation complete

---

### Workflow 3: Validate Only Changed Files (15 seconds)

**User signal**: "Validate changed files", "Check my changes", "Verify what I edited"

**Purpose**: Fast validation of only modified files (pre-commit optimization)

**Steps**:
1. Run changed-files validation:
   ```bash
   ./scripts/validate-links.sh --changed
   ```

2. Review changed files only:
   ```
   Validating changed files...

   Changed files (3):
   - docs/skilled-awareness/sap-framework/AGENTS.md
   - docs/skilled-awareness/sap-framework/CLAUDE.md
   - docs/skilled-awareness/sap-framework/protocol-spec.md

   ✅ All links in changed files valid (18/18)
   ```

**Expected outcome**: Fast validation, ready to commit

---

### Workflow 4: Fix Broken Links (2-5 minutes)

**User signal**: "Fix broken links", "Repair references", "Update dead links"

**Purpose**: Systematically fix all broken links reported by validator

**Steps**:
1. Run validation to identify broken links:
   ```bash
   ./scripts/validate-links.sh > validation-report.txt
   ```

2. Parse report for broken links:
   ```bash
   grep "❌" validation-report.txt
   # or
   grep "(file not found)" validation-report.txt
   ```

3. Fix each broken link:
   ```markdown
   # Pattern 1: Renamed file
   # Broken: [Charter](capability-charter.md)
   # Fixed:  [Charter](charter.md)

   # Pattern 2: Moved file
   # Broken: [Spec](../inbox/protocol-spec.md)
   # Fixed:  [Spec](../../inbox/protocol-spec.md)

   # Pattern 3: Invalid anchor
   # Broken: [Section](#nonexistent-section)
   # Fixed:  [Section](#correct-section-name)
   ```

4. Re-validate after fixes:
   ```bash
   ./scripts/validate-links.sh
   ```

**Expected outcome**: All broken links fixed, validation passes

---

### Workflow 5: Validate External Links (2-3 minutes)

**User signal**: "Check external links", "Verify HTTP links", "Test external references"

**Purpose**: Ensure external HTTP/HTTPS links are still reachable

**Steps**:
1. Run full validation (includes external links by default):
   ```bash
   ./scripts/validate-links.sh
   ```

2. Review external link results:
   ```
   External links validated:
   ✅ https://docs.anthropic.com (200 OK)
   ✅ https://github.com/anthropics/claude-code (200 OK)
   ❌ https://example.com/old-page (404 Not Found)
   ```

3. Update broken external links:
   ```markdown
   # Broken external link
   [Old Resource](https://example.com/old-page)

   # Updated to current URL
   [New Resource](https://example.com/new-page)
   ```

4. Re-validate:
   ```bash
   ./scripts/validate-links.sh
   ```

**Expected outcome**: External links valid or updated

---

## Best Practices

### Practice 1: Validate Before Every Commit

**Pattern**:
```bash
# ALWAYS validate before committing documentation changes
./scripts/validate-links.sh --changed
git add .
git commit -m "docs: ..."
```

**Why**: Catch broken links before they reach main branch

---

### Practice 2: Use Relative Paths for Internal Links

**Pattern**:
```markdown
# ✅ GOOD: Relative path
[Protocol Spec](../sap-framework/protocol-spec.md)

# ❌ BAD: Absolute path
[Protocol Spec](/Users/username/code/chora-base/docs/skilled-awareness/sap-framework/protocol-spec.md)
```

**Why**: Relative paths work across different environments, absolute paths break

---

### Practice 3: Include Anchor Links When Referencing Sections

**Pattern**:
```markdown
# ✅ GOOD: Anchor link to specific section
[See Installation](adoption-blueprint.md#installation-steps)

# ⚠️ LESS HELPFUL: Link to entire document
[See Installation](adoption-blueprint.md)
```

**Why**: Anchor links jump directly to relevant section, better UX

---

### Practice 4: Validate After Refactoring Documentation Structure

**Pattern**:
```bash
# After moving/renaming files:
git mv docs/old-name.md docs/new-name.md

# Validate ALL links (not just changed files)
./scripts/validate-links.sh

# Fix any broken references
# Then commit
```

**Why**: Refactoring breaks relative paths, full scan catches all issues

---

### Practice 5: Use CI/CD to Block Broken Links

**Pattern**:
```yaml
# .github/workflows/validate-links.yml
name: Validate Links
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate links
        run: ./scripts/validate-links.sh
```

**Why**: Prevent broken links from merging to main branch

---

## Common Pitfalls

### Pitfall 1: Not Validating After Renaming Files

**Problem**: Rename file but forget to update links pointing to it

**Fix**: Validate after every file rename

```bash
# After rename:
git mv docs/old-name.md docs/new-name.md

# ALWAYS validate
./scripts/validate-links.sh

# Fix broken references, then commit
```

**Why**: Renaming breaks relative paths in other files

---

### Pitfall 2: Using Absolute Paths Instead of Relative

**Problem**: Use absolute filesystem paths in markdown links

**Fix**: Use relative paths

```markdown
# ❌ BAD: Absolute path
[Link](/Users/username/code/chora-base/docs/foo.md)

# ✅ GOOD: Relative path
[Link](../foo.md)
```

**Why**: Absolute paths break for other users, relative paths portable

---

### Pitfall 3: Forgetting to Validate External Links

**Problem**: External links go stale (404) but not caught

**Fix**: Run full validation periodically

```bash
# Full validation includes external links
./scripts/validate-links.sh

# Review external link failures
grep "404" validation-report.txt
```

**Why**: External resources move/disappear over time

---

### Pitfall 4: Invalid Anchor Links After Section Renames

**Problem**: Rename section heading but anchor links still point to old name

**Fix**: Validate after section renames

```markdown
# Before:
## Old Section Name
[Link](#old-section-name)

# After renaming section:
## New Section Name
[Link](#new-section-name)  # Update anchor
```

**Why**: Anchors generated from heading text, must match exactly

---

### Pitfall 5: Not Using --changed for Fast Validation

**Problem**: Run full validation on every commit (slow)

**Fix**: Use --changed for pre-commit checks

```bash
# ❌ SLOW: Full validation every time
./scripts/validate-links.sh

# ✅ FAST: Changed files only
./scripts/validate-links.sh --changed
```

**Why**: Changed-files validation 80% faster, sufficient for pre-commit

---

## Integration with Other SAPs

### SAP-000 (sap-framework)
- All SAP artifacts validated for broken links
- Integration: Run validate-links.sh on docs/skilled-awareness/

### SAP-007 (documentation-framework)
- Link validation enforces Diataxis cross-references
- Integration: Validate documentation domain links

### SAP-004 (quality-gates)
- Link validation as quality gate criterion
- Integration: CI/CD blocks merges with broken links

### SAP-012 (development-lifecycle)
- Validation in pre-commit hook (DDD phase)
- Integration: Git hook runs validate-links.sh --changed

---

## Support & Resources

**SAP-016 Documentation**:
- [Capability Charter](capability-charter.md) - Link validation problem and scope
- [Protocol Spec](protocol-spec.md) - Technical contract and validation rules
- [Awareness Guide](awareness-guide.md) - Detailed workflows
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking

**Scripts**:
- `scripts/validate-links.sh` - Main validation script
- `scripts/validate-links.sh --changed` - Fast validation for changed files

**Related SAPs**:
- [SAP-000 (sap-framework)](../sap-framework/) - SAP artifacts validated
- [SAP-004 (quality-gates)](../quality-gates/) - Link validation as gate
- [SAP-007 (documentation-framework)](../documentation-framework/) - Diataxis references
- [SAP-012 (development-lifecycle)](../development-lifecycle/) - Pre-commit validation

---

## Version History

- **1.0.0** (2025-11-04): Initial AGENTS.md for SAP-016
  - 5 workflows: Validate All Links, Validate Directory, Validate Changed Files, Fix Broken Links, Validate External Links
  - 1 user signal pattern table (Link Validation Operations)
  - 5 best practices, 5 common pitfalls
  - Integration with SAP-000, SAP-004, SAP-007, SAP-012

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific patterns
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
4. Validate links: `./scripts/validate-links.sh`
