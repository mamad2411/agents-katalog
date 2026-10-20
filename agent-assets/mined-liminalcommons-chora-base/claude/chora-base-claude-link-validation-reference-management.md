---
sap_id: SAP-016
version: 1.0.0
status: active
last_updated: 2025-11-04
type: reference
audience: claude_code
complexity: beginner
estimated_reading_time: 7
progressive_loading:
  phase_1: "lines 1-160"   # Quick Start + Core Workflows
  phase_2: "lines 161-280" # Advanced Operations
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 3000
phase_2_token_estimate: 6000
phase_3_token_estimate: 8000
---

# Link Validation & Reference Management (SAP-016) - Claude-Specific Awareness

**SAP ID**: SAP-016
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

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

This CLAUDE.md provides: Claude Code-specific workflows using Bash (validation), Read (reports), Edit (fix broken links).

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for validating markdown links.

### First-Time Session

1. Read [AGENTS.md](AGENTS.md) for generic link validation workflows
2. Use this file for Claude Code tool integration (Bash for validation, Read for reports, Edit for fixes)
3. Always validate links before committing documentation changes

### Validation Commands

```bash
# Validate all links
./scripts/validate-links.sh

# Validate specific directory
./scripts/validate-links.sh docs/skilled-awareness/sap-framework/

# Validate changed files only (fast)
./scripts/validate-links.sh --changed
```

---

## Claude Code Link Validation Workflows

### Workflow 1: Validating Links with Bash Before Commit

```markdown
User: "Validate links before committing"

Claude (Phase 1: Run Validation - 0-10k tokens):
1. Run validation script:
   Bash: ./scripts/validate-links.sh --changed
   # Validates only modified files (fast)

2. Capture output:
   Output:
   Validating changed files...

   Changed files (2):
   - docs/skilled-awareness/sap-framework/AGENTS.md
   - docs/skilled-awareness/sap-framework/CLAUDE.md

   ✅ docs/skilled-awareness/sap-framework/AGENTS.md (12 links checked)
   ❌ docs/skilled-awareness/sap-framework/CLAUDE.md (2 broken links)
     - Line 234: [Missing](../non-existent.md) (file not found)
     - Line 456: [Bad Anchor](#invalid-section) (anchor not found)

   Summary: 10/12 links valid (83.3%)

Claude (Phase 2: Fix Issues - 10-30k tokens):
3. Read file with broken links:
   Read docs/skilled-awareness/sap-framework/CLAUDE.md
   # Focus on lines 234 and 456

4. Fix broken links:
   Edit docs/skilled-awareness/sap-framework/CLAUDE.md
   # Line 234: Update path to correct file
   # Line 456: Update anchor to valid section

Claude (Phase 3: Re-validate - 30-40k tokens):
5. Verify fixes:
   Bash: ./scripts/validate-links.sh docs/skilled-awareness/sap-framework/CLAUDE.md

   Output:
   ✅ CLAUDE.md (12/12 links valid)

Claude (response to user):
"✅ Link validation complete:
   - Initial: 10/12 links valid (2 broken)
   - Fixed 2 broken links:
     • Line 234: Updated file path
     • Line 456: Corrected anchor reference
   - Final: 12/12 links valid ✅

   Ready to commit!"

Result: All links valid, safe to commit
```

---

### Workflow 2: Fixing Broken Links with Read and Edit

```markdown
User: "Fix broken links in SAP-003"

Claude (Phase 1: Identify Broken Links - 0-10k tokens):
1. Run validation on specific SAP:
   Bash: ./scripts/validate-links.sh docs/skilled-awareness/project-bootstrap/

   Output:
   ❌ docs/skilled-awareness/project-bootstrap/AGENTS.md (3 broken links)
     - Line 45: [Old File](../old-name.md) (file not found)
     - Line 78: [Moved Doc](../../dev-docs/old-location.md) (file not found)
     - Line 120: [Section](#removed-section) (anchor not found)

Claude (Phase 2: Read and Fix - 10-40k tokens):
2. Read file with broken links:
   Read docs/skilled-awareness/project-bootstrap/AGENTS.md

3. For each broken link, fix:
   # Fix 1: Renamed file
   Edit docs/skilled-awareness/project-bootstrap/AGENTS.md
   # old_string: [Old File](../old-name.md)
   # new_string: [Old File](../new-name.md)

   # Fix 2: Moved file (search for new location)
   Grep: pattern="old-location", path="dev-docs/", output_mode="files_with_matches"
   # Found in: dev-docs/guides/new-location.md

   Edit docs/skilled-awareness/project-bootstrap/AGENTS.md
   # old_string: [Moved Doc](../../dev-docs/old-location.md)
   # new_string: [Moved Doc](../../dev-docs/guides/new-location.md)

   # Fix 3: Updated anchor (check current sections)
   Read docs/skilled-awareness/project-bootstrap/AGENTS.md
   # Find current section headings
   # Anchor was "removed-section", now "updated-section"

   Edit docs/skilled-awareness/project-bootstrap/AGENTS.md
   # old_string: [Section](#removed-section)
   # new_string: [Section](#updated-section)

Claude (Phase 3: Validate Fixes - 40-50k tokens):
4. Re-validate:
   Bash: ./scripts/validate-links.sh docs/skilled-awareness/project-bootstrap/

   Output:
   ✅ All links valid (15/15)

Claude (response to user):
"✅ Fixed 3 broken links in SAP-003:
   1. Renamed file reference: old-name.md → new-name.md
   2. Updated moved file path: old-location.md → guides/new-location.md
   3. Corrected anchor: #removed-section → #updated-section

   Validation: ✅ All links now valid"

Result: Broken links fixed, validation passes
```

---

### Workflow 3: Validating After Refactoring with Bash

```markdown
User: "I renamed protocol-spec.md to spec.md, validate all links"

Claude (Phase 1: Validate Impact - 0-10k tokens):
1. Run full validation to find all broken references:
   Bash: ./scripts/validate-links.sh

   Output:
   ❌ 5 files with broken links to protocol-spec.md:
     - docs/skilled-awareness/sap-framework/AGENTS.md (line 123)
     - docs/skilled-awareness/inbox/CLAUDE.md (line 67)
     - docs/skilled-awareness/memory-system/awareness-guide.md (line 234)
     - docs/ARCHITECTURE.md (line 89)
     - README.md (line 45)

Claude (Phase 2: Batch Fix - 10-60k tokens):
2. For each broken reference, update:
   Read docs/skilled-awareness/sap-framework/AGENTS.md
   Edit docs/skilled-awareness/sap-framework/AGENTS.md
   # old_string: [Protocol Spec](protocol-spec.md)
   # new_string: [Protocol Spec](spec.md)

   # Repeat for other 4 files...

Claude (Phase 3: Re-validate - 60-70k tokens):
3. Verify all fixes:
   Bash: ./scripts/validate-links.sh

   Output:
   ✅ All links valid (127/127)

Claude (response to user):
"✅ Updated all references after renaming protocol-spec.md → spec.md:
   - Fixed 5 files with broken links
   - Validation: ✅ All 127 links valid

   Files updated:
   - docs/skilled-awareness/sap-framework/AGENTS.md
   - docs/skilled-awareness/inbox/CLAUDE.md
   - docs/skilled-awareness/memory-system/awareness-guide.md
   - docs/ARCHITECTURE.md
   - README.md

   Safe to commit!"

Result: All references updated, validation passes
```

---

## Claude-Specific Tips

### Tip 1: Use Bash for Validation, Not Manual Checks

**Pattern**:
```markdown
# ✅ GOOD: Automated validation
Bash: ./scripts/validate-links.sh --changed

# ❌ BAD: Manual link checking
Read every file, manually check each link
```

**Why**: Script validates hundreds of links in seconds, catches edge cases

---

### Tip 2: Use --changed for Pre-Commit Validation (Faster)

**Pattern**:
```markdown
# Fast validation before commit
Bash: ./scripts/validate-links.sh --changed
# Only checks modified files

# Full validation periodically
Bash: ./scripts/validate-links.sh
# Checks all files (slower)
```

**Why**: --changed flag 80% faster, sufficient for pre-commit checks

---

### Tip 3: Use Grep to Find New Location of Moved Files

**Pattern**:
```markdown
# When link points to moved file:
Bash: ./scripts/validate-links.sh
# Output: docs/old-location/file.md (file not found)

# Search for file by name
Grep: pattern="file.md", path="docs/", output_mode="files_with_matches"
# Found: docs/new-location/file.md

# Update link
Edit <file-with-broken-link>
# old_string: [Link](docs/old-location/file.md)
# new_string: [Link](docs/new-location/file.md)
```

**Why**: Grep quickly locates moved files across repository

---

### Tip 4: Read File to Check Current Section Headings for Anchors

**Pattern**:
```markdown
# When anchor link broken:
Bash: ./scripts/validate-links.sh
# Output: #old-section-name (anchor not found)

# Read target file to see current headings
Read <target-file.md>
# Scan for section headings (lines starting with ##)

# Update anchor to match current heading
Edit <file-with-broken-link>
# old_string: [Link](#old-section-name)
# new_string: [Link](#current-section-name)
```

**Why**: Anchors generated from heading text, must match exactly

---

### Tip 5: Validate Full Repository After Major Refactoring

**Pattern**:
```markdown
# After moving/renaming multiple files:
Bash: ./scripts/validate-links.sh
# Full scan (not --changed)

# Fix all broken links
# Then commit
```

**Why**: Refactoring breaks links across many files, full scan required

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Validating After Renaming Files

**Problem**: Rename file but forget to check for broken references

**Fix**: ALWAYS validate after rename

```markdown
# ❌ BAD: Rename and commit without validation
Bash: git mv old.md new.md
Bash: git commit -m "rename file"

# ✅ GOOD: Validate after rename
Bash: git mv old.md new.md
Bash: ./scripts/validate-links.sh
# Fix broken references, then commit
```

**Why**: Renaming breaks relative paths in other files

---

### Pitfall 2: Using Read to Validate Links (Too Slow)

**Problem**: Read every file and manually check links

**Fix**: Use validation script

```markdown
# ❌ BAD: Manual validation
Read file1.md
Read file2.md
# Manually check each link...

# ✅ GOOD: Automated validation
Bash: ./scripts/validate-links.sh
```

**Why**: Script validates 100+ files in seconds, catches all edge cases

---

### Pitfall 3: Fixing Broken Links Without Re-Validating

**Problem**: Fix broken link but don't verify fix works

**Fix**: Re-validate after fixes

```markdown
# After fixing broken links:
Edit <file-with-broken-link>

# ALWAYS re-validate
Bash: ./scripts/validate-links.sh <file>
```

**Why**: Ensure fix actually resolves issue, catch typos

---

### Pitfall 4: Not Using --changed for Fast Pre-Commit Checks

**Problem**: Run full validation every commit (slow, wastes time)

**Fix**: Use --changed flag

```markdown
# ❌ SLOW: Full validation every time
Bash: ./scripts/validate-links.sh

# ✅ FAST: Changed files only
Bash: ./scripts/validate-links.sh --changed
```

**Why**: --changed validates only modified files, 80% faster

---

### Pitfall 5: Not Searching for Moved Files Before Fixing

**Problem**: Link broken because file moved, but don't find new location

**Fix**: Use Grep to locate moved file

```markdown
# When file moved:
# ❌ BAD: Guess new location
Edit <file>
# Update link with guessed path (might be wrong)

# ✅ GOOD: Search for file
Grep: pattern="filename.md", path="docs/", output_mode="files_with_matches"
# Use actual location found
```

**Why**: Grep finds correct new location, avoids guessing errors

---

## Support & Resources

**SAP-016 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic link validation workflows
- [Capability Charter](capability-charter.md) - Link validation problem and scope
- [Protocol Spec](protocol-spec.md) - Technical contract and validation rules
- [Awareness Guide](awareness-guide.md) - Detailed workflows
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking

**Scripts**:
- `scripts/validate-links.sh` - Main validation script
- `scripts/validate-links.sh --changed` - Fast validation for changed files
- `scripts/validate-links.sh <path>` - Validate specific directory/file

**Related SAPs**:
- [SAP-000 (sap-framework)](../sap-framework/) - SAP artifacts validated
- [SAP-004 (quality-gates)](../quality-gates/) - Link validation as gate
- [SAP-007 (documentation-framework)](../documentation-framework/) - Diataxis references
- [SAP-012 (development-lifecycle)](../development-lifecycle/) - Pre-commit validation

---

## Version History

- **1.0.0** (2025-11-04): Initial CLAUDE.md for SAP-016
  - 3 workflows: Validate with Bash, Fix with Read/Edit, Validate After Refactoring
  - Tool patterns: Bash for validation, Read for inspection, Edit for fixes, Grep for searching
  - 5 Claude-specific tips, 5 common pitfalls
  - --changed flag pattern for fast validation

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic link validation workflows
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
4. Validate links: `./scripts/validate-links.sh --changed`
