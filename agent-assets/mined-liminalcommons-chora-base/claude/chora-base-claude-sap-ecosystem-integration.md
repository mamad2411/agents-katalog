# SAP Ecosystem Integration (SAP-061) - Claude-Specific Awareness

**SAP ID**: SAP-061
**Claude Compatibility**: Sonnet 4.5+
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

This CLAUDE.md provides: Claude Code-specific workflows for implementing SAP-061.

---

## Claude Code SAP Validation Workflows

### Workflow 1: Validating a SAP with Claude Code

```markdown
User: "Validate SAP-053 ecosystem integration"

Claude (Phase 1: Run Validation - 0-5k tokens):
1. Execute validation via Bash tool:
   Bash: python scripts/validate-ecosystem-integration.py SAP-053

2. Parse output (5 integration points):
   ✅ INDEX.md: Found in domain section
   ✅ sap-catalog.json: Metadata exists
   ✅ copier.yml: Available for distribution
   ✅ Dependencies: All valid (SAP-000, SAP-009, SAP-056)
   ⚠️  Progressive Adoption Path: Skipped (status=pilot)

   Result: PASS (4/4 required checks)
   Exit code: 0

Claude (response to user):
"SAP-053 ecosystem integration validated successfully:

✅ INDEX.md: Entry exists in appropriate domain
✅ sap-catalog.json: Metadata complete
✅ copier.yml: Available for Copier distribution
✅ Dependencies: All referenced SAPs exist and are valid

Progressive Adoption Path check skipped (pilot status).

SAP-053 is fully integrated and ready for commit."

Result: SAP-053 validated, no gaps found
Token usage: ~3-5k (Phase 1 only, no fixes needed)
```

---

### Workflow 2: Fixing Integration Gaps with Claude Code

```markdown
User: "Fix SAP-062 integration gaps"

Claude (Phase 1: Identify Gaps - 0-5k tokens):
1. Run validation via Bash tool:
   Bash: python scripts/validate-ecosystem-integration.py SAP-062

2. Parse failure output:
   ❌ INDEX.md: SAP-062 not found
   ✅ sap-catalog.json: Metadata exists
   ❌ copier.yml: SAP-062 not found (status=pilot, required)
   ✅ Dependencies: None (no deps)

   Result: FAIL (2 failures)
   Exit code: 1 (INDEX.md failure takes priority)

Claude (Phase 2: Fix INDEX.md - 5-20k tokens):
3. Read INDEX.md to find correct domain section:
   Read docs/skilled-awareness/INDEX.md

4. Identify domain for SAP-062 (e.g., "Specialized Domain")

5. Edit INDEX.md via Edit tool:
   Edit docs/skilled-awareness/INDEX.md
   # old_string: (Find appropriate location in Specialized Domain)
   # new_string: Add SAP-062 entry:
   ### SAP-062: SAP Lifecycle Documentation

   **Status**: Pilot
   **Description**: Automated documentation generation for SAP development lifecycle stages.
   **Key Features**:
   - Lifecycle stage templates
   - Documentation coverage tracking
   - Cross-SAP documentation links

Claude (Phase 3: Fix copier.yml - 20-35k tokens):
6. Read copier.yml to understand structure:
   Read copier.yml

7. Edit copier.yml via Edit tool:
   Edit copier.yml
   # old_string: (Find SAP checklist section)
   # new_string: Add SAP-062 to checklist:
   - SAP-062 (sap-lifecycle-documentation)

Claude (Phase 4: Re-validate - 35-40k tokens):
8. Run validation again via Bash tool:
   Bash: python scripts/validate-ecosystem-integration.py SAP-062

9. Verify all checks pass:
   ✅ INDEX.md: SAP-062 found in Specialized Domain
   ✅ sap-catalog.json: Metadata exists
   ✅ copier.yml: SAP-062 found
   ✅ Dependencies: None

   Result: PASS (4/4 checks)
   Exit code: 0

Claude (response to user):
"Fixed 2 integration gaps for SAP-062:

✅ Added to INDEX.md (Specialized Domain section)
✅ Added to copier.yml (SAP checklist)

Re-validation: PASS (all 4 checks passed)
Exit code: 0

SAP-062 is now fully integrated and ready for commit."

Result: SAP-062 integration gaps fixed and validated
Token usage: ~35-40k (Phase 1-4: identify → fix → re-validate)
```

---

### Workflow 3: Installing Pre-Commit Hook with Claude Code

```markdown
User: "Set up SAP ecosystem validation pre-commit hook"

Claude (Phase 1: Check Hook Existence - 0-5k tokens):
1. Check if hook script exists via Bash tool:
   Bash: ls -la scripts/git-hooks/pre-commit-ecosystem

2. If exists, proceed to installation
   If not, inform user hook script needs creation

Claude (Phase 2: Install Hook - 5-10k tokens):
3. Copy hook to .git/hooks via Bash tool:
   Bash: cp scripts/git-hooks/pre-commit-ecosystem .git/hooks/pre-commit

4. Make hook executable via Bash tool:
   Bash: chmod +x .git/hooks/pre-commit

5. Test hook manually via Bash tool:
   Bash: .git/hooks/pre-commit

Claude (Phase 3: Verify Installation - 10-15k tokens):
6. Check hook is executable:
   Bash: ls -la .git/hooks/pre-commit

7. Test hook runs on commit (dry run):
   Bash: git commit --dry-run -m "Test commit"
   # Hook should run validator before commit

Claude (response to user):
"Pre-commit hook installed successfully:

✅ Hook script copied to .git/hooks/pre-commit
✅ Made executable (chmod +x)
✅ Tested manually (validation runs)

From now on, every commit will:
1. Run SAP ecosystem integration validation
2. Prevent commits if any SAP has integration gaps
3. Show which SAP(s) failed and which integration points

Use --no-verify to skip (not recommended):
git commit -m 'message' --no-verify"

Result: Pre-commit hook installed and verified
Token usage: ~10-15k (Phase 1-3)
```

---

### Workflow 4: Validating All SAPs with Claude Code

```markdown
User: "Run full SAP ecosystem validation"

Claude (Phase 1: Run Full Validation - 0-5k tokens):
1. Execute validation for all SAPs via Bash tool:
   Bash: python scripts/validate-ecosystem-integration.py --all

2. Parse summary output:
   Validated 48 SAPs in 1.4s
   ✅ PASSED: 47 SAPs
   ❌ FAILED: 1 SAP
     - SAP-029: Missing from INDEX.md

   Performance: 1.4s total (target: <2s)
   Exit code: 1

Claude (Phase 2: Get Detailed Failure Info - 5-10k tokens):
3. If failures exist, run with --verbose for details:
   Bash: python scripts/validate-ecosystem-integration.py SAP-029 --verbose

4. Identify specific failure:
   ❌ INDEX.md: SAP-029 not found in any domain section

Claude (Phase 3: Provide Fix Guidance - 10-15k tokens):
5. Read INDEX.md to suggest fix location:
   Read docs/skilled-awareness/INDEX.md
   # Identify appropriate domain for SAP-029 (Specialized Domain)

6. Suggest fix to user or execute if authorized

Claude (response to user):
"Full ecosystem validation complete:

✅ 47/48 SAPs passed (97.9%)
❌ 1 SAP failed:
  - SAP-029 (sap-generation): Missing from INDEX.md

Validation performance: 1.4s (target: <2s) ✅

Recommended fix:
Add SAP-029 to INDEX.md under Specialized Domain:

### SAP-029: SAP Generation
**Status**: Pilot
**Description**: Template-based SAP generation (80% time savings)

Would you like me to fix this gap?"

Result: Full validation complete, gap identified, fix suggested
Token usage: ~10-15k (Phase 1-3)
```

---

### Workflow 5: Integrating Validation in New SAP Development

```markdown
User: "Create SAP-063 and ensure it's fully integrated"

Claude (Phase 0: Context - 0-5k tokens):
- User wants new SAP + validation from start
- SAP-061 pattern: integrate early, validate often

Claude (Phase 1: Create SAP Metadata - 5-15k tokens):
1. Read sap-catalog.json via Read tool:
   Read sap-catalog.json

2. Draft SAP-063 metadata (id, name, status, etc.)

3. Edit sap-catalog.json via Edit tool:
   Edit sap-catalog.json
   # Add SAP-063 entry with metadata

4. Validate catalog addition via Bash tool:
   Bash: python scripts/validate-ecosystem-integration.py SAP-063
   # Expect: catalog check passes, others fail (SAP not created yet)

Claude (Phase 2: Add to INDEX.md Early - 15-25k tokens):
5. Read INDEX.md via Read tool:
   Read docs/skilled-awareness/INDEX.md

6. Edit INDEX.md via Edit tool:
   Edit docs/skilled-awareness/INDEX.md
   # Add SAP-063 entry to appropriate domain

7. Re-validate via Bash tool:
   Bash: python scripts/validate-ecosystem-integration.py SAP-063
   # Expect: INDEX.md and catalog pass, copier/deps may fail

Claude (Phase 3: Create SAP Artifacts - 25-80k tokens):
8. Generate SAP artifacts (via SAP-029 or manually)
   # capability-charter.md, protocol-spec.md, etc.

9. If status=pilot, add to copier.yml:
   Edit copier.yml
   # Add SAP-063 to SAP checklist

Claude (Phase 4: Final Validation - 80-90k tokens):
10. Run final validation via Bash tool:
    Bash: python scripts/validate-ecosystem-integration.py SAP-063

11. Verify all checks pass:
    ✅ INDEX.md: SAP-063 found
    ✅ sap-catalog.json: Metadata exists
    ✅ copier.yml: SAP-063 found (status=pilot)
    ✅ Dependencies: All valid

    Result: PASS (4/4 checks)
    Exit code: 0

Claude (response to user):
"SAP-063 created and fully integrated:

✅ Added to sap-catalog.json (metadata complete)
✅ Added to INDEX.md (Specialized Domain)
✅ Added to copier.yml (distributable)
✅ All 5 SAP artifacts created
✅ Validation: PASS (all integration points)

SAP-063 is integrated from day 1 - no post-completion gaps!

Time saved: ~10-15 min (vs manual checklist)
Pattern used: SAP-061 (early integration)"

Result: SAP-063 created and validated, no gaps
Token usage: ~80-90k (full SAP creation + integration)
```

---

## Claude-Specific Tips

### Tip 1: Use Bash Tool for Validation, Not Read Tool

**Pattern**:
```bash
# Always run validator via Bash tool
Bash: python scripts/validate-ecosystem-integration.py SAP-053

# Don't try to manually check integration points via Read
# (Validator is faster and more accurate)
```

**Why**: Validator handles complex logic (dependency resolution, pattern matching) that would require multiple Read tool calls.

---

### Tip 2: Parse Exit Codes for Workflow Branching

**Pattern**:
```bash
# Exit code 0: No action needed
# Exit code 1: Fix INDEX.md first (highest priority)
# Exit code 2: Fix sap-catalog.json
# Exit code 3: Fix copier.yml
# Exit code 4: Fix dependencies
# Exit code 5: Multiple failures (fix all)

# Use exit code to determine next action
Bash: python scripts/validate-ecosystem-integration.py SAP-XXX
# Output: Exit code: 1
# → Next action: Edit INDEX.md
```

**Why**: Exit codes prioritize fixes (INDEX.md before copier.yml)

---

### Tip 3: Validate After Every Integration Point Fix

**Pattern**:
```bash
# Fix 1: Add to INDEX.md
Edit docs/skilled-awareness/INDEX.md

# Validate immediately
Bash: python scripts/validate-ecosystem-integration.py SAP-XXX
# Check: INDEX.md now passes?

# Fix 2: Add to copier.yml
Edit copier.yml

# Validate again
Bash: python scripts/validate-ecosystem-integration.py SAP-XXX
# Check: copier.yml now passes?
```

**Why**: Early validation catches mistakes before moving to next fix

---

### Tip 4: Use --json Output for Programmatic Workflows

**Pattern**:
```bash
# Get JSON output for parsing
Bash: python scripts/validate-ecosystem-integration.py SAP-053 --json

# Output structure:
# {
#   "sap_id": "SAP-053",
#   "passed": true,
#   "checks": [
#     {"integration_point": "INDEX.md", "passed": true, "message": "..."},
#     ...
#   ],
#   "exit_code": 0
# }

# Parse JSON in Claude Code for automated workflows
```

**Why**: JSON output is easier to parse than human-readable text

---

### Tip 5: Integrate Early in SAP Development Workflow

**Pattern**:
```bash
# Don't wait until end:
# ❌ Create SAP → Fill artifacts → Validate (gaps found late)

# Integrate early:
# ✅ Add to catalog → Add to INDEX.md → Create artifacts → Validate

# Order of operations:
# 1. Add SAP metadata to sap-catalog.json
# 2. Add SAP entry to INDEX.md
# 3. Generate/create SAP artifacts
# 4. Add to copier.yml (if applicable)
# 5. Final validation
```

**Why**: Prevents post-completion scramble to fix integration gaps (SAP-053 pattern)

---

## Tool Usage Patterns

### Using Bash Tool for SAP Validation

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

# Test hook manually
.git/hooks/pre-commit

# Combine with git commands
python scripts/validate-ecosystem-integration.py --all && git commit -m "Add SAP-063"
```

---

### Using Edit Tool for Integration Gap Fixes

```bash
# Read target file first
Read docs/skilled-awareness/INDEX.md

# Edit to add SAP entry
Edit docs/skilled-awareness/INDEX.md
# old_string: (Find appropriate section header)
### SAP-060: Previous SAP

# new_string: Add new SAP entry after appropriate location
### SAP-060: Previous SAP

### SAP-063: New SAP Name
**Status**: Pilot
**Description**: Brief description of SAP
**Key Features**:
- Feature 1
- Feature 2

# Same pattern for sap-catalog.json and copier.yml
```

---

### Using Read Tool for Context Before Fixes

```bash
# Before fixing INDEX.md, read to understand structure
Read docs/skilled-awareness/INDEX.md

# Identify:
# - Which domain section (Infrastructure, Developer Experience, etc.)
# - Appropriate location within domain (alphabetical? by SAP ID?)
# - Format of existing entries (heading level, metadata fields)

# Before fixing copier.yml, read to understand pattern
Read copier.yml

# Identify:
# - Where SAP checklist is located
# - Format of existing SAP entries
# - Any conditional logic (status-based inclusion)
```

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Validating After Each Fix

**Problem**: Fix INDEX.md and copier.yml, then validate once at end (might miss mistakes)

**Fix**:
```bash
# Validate after INDEX.md fix
Edit docs/skilled-awareness/INDEX.md
Bash: python scripts/validate-ecosystem-integration.py SAP-XXX
# Verify INDEX.md check now passes before moving to copier.yml

# Validate after copier.yml fix
Edit copier.yml
Bash: python scripts/validate-ecosystem-integration.py SAP-XXX
# Verify copier.yml check now passes
```

---

### Pitfall 2: Using Write Tool Instead of Edit Tool for INDEX.md/Catalog

**Problem**: Overwriting entire INDEX.md or sap-catalog.json with Write tool (loses other entries)

**Fix**:
```bash
# Don't: Write entire file
Write docs/skilled-awareness/INDEX.md
# (Loses all other SAP entries)

# Do: Edit specific section
Read docs/skilled-awareness/INDEX.md
Edit docs/skilled-awareness/INDEX.md
# old_string: (Specific section to update)
# new_string: (Add new SAP entry only)
```

---

### Pitfall 3: Not Checking SAP Status Before Copier.yml Fix

**Problem**: Adding draft SAPs to copier.yml (not required, causes clutter)

**Fix**:
```bash
# Check SAP status first
Read sap-catalog.json | grep -A 5 "SAP-XXX" | grep status

# Only add to copier.yml if status=active or pilot
# Skip if status=draft (validation won't fail)
```

---

### Pitfall 4: Not Understanding Exit Code Priority

**Problem**: Fixing copier.yml first when INDEX.md also failed (INDEX.md has higher priority)

**Fix**:
```bash
# Exit code 1 = INDEX.md failure (highest priority)
# Exit code 2 = catalog failure
# Exit code 3 = copier.yml failure
# Exit code 4 = dependency failure

# Always fix in priority order:
# 1. INDEX.md (exit code 1)
# 2. sap-catalog.json (exit code 2)
# 3. copier.yml (exit code 3)
# 4. Dependencies (exit code 4)
```

---

### Pitfall 5: Not Installing Pre-Commit Hook for SAP Development

**Problem**: Repeatedly committing with integration gaps, then scrambling to fix

**Fix**:
```bash
# Install hook once at start of SAP development workflow
cp scripts/git-hooks/pre-commit-ecosystem .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# From now on, hook prevents incomplete integrations
git commit -m "Add SAP-063"
# → Hook runs validator automatically
# → Commit blocked if validation fails
```

---

## Example Claude Code Session (Complete SAP Integration)

```markdown
User: "Validate SAP-053 and fix any integration gaps"

Claude (thinking):
- Task = validate + fix gaps
- SAP-061 validation pattern
- Progressive: Run validation → Parse output → Fix gaps → Re-validate

Claude (Phase 1: Initial Validation - 0-5k tokens):
1. Run validation via Bash tool:
   Bash: python scripts/validate-ecosystem-integration.py SAP-053

2. Parse output:
   ✅ INDEX.md: Found
   ✅ sap-catalog.json: Found
   ❌ copier.yml: SAP-053 not found (status=pilot, required)
   ✅ Dependencies: All valid

   Result: FAIL (1 failure)
   Exit code: 3 (copier.yml)

Claude (Phase 2: Fix copier.yml - 5-15k tokens):
3. Read copier.yml via Read tool:
   Read copier.yml

4. Locate SAP checklist section (line ~450)

5. Edit copier.yml via Edit tool:
   Edit copier.yml
   # old_string: (Find SAP-052 entry)
   - SAP-052 (ownership-tracking)

   # new_string: Add SAP-053 after SAP-052
   - SAP-052 (ownership-tracking)
   - SAP-053 (multi-interface-conformance)

Claude (Phase 3: Re-validate - 15-20k tokens):
6. Run validation again via Bash tool:
   Bash: python scripts/validate-ecosystem-integration.py SAP-053

7. Verify all checks pass:
   ✅ INDEX.md: Found
   ✅ sap-catalog.json: Found
   ✅ copier.yml: SAP-053 found
   ✅ Dependencies: All valid

   Result: PASS (4/4 checks)
   Exit code: 0

Claude (response to user):
"SAP-053 validation complete:

Initial validation: FAIL
  ❌ copier.yml: SAP-053 missing

Fix applied:
  ✅ Added SAP-053 to copier.yml (SAP checklist)

Re-validation: PASS
  ✅ All 4 integration points validated
  ✅ Exit code: 0

SAP-053 is now fully integrated and ready for commit.

Time spent: ~5 min
Pattern used: SAP-061 (automated validation + targeted fix)"

Result: SAP-053 validated and integrated
Token usage: ~15-20k (Phase 1-3)
Time saved: ~10 min (vs manual checklist)
```

**Key Points**:
- Phase 1: Identified gap in ~2 min (validator found copier.yml gap)
- Phase 2: Fixed gap in ~3 min (Edit tool, targeted change)
- Phase 3: Re-validated in ~1 min (confirmed fix worked)
- Skipped manual checks: No need to verify INDEX.md, catalog (validator confirms)
- Exit code guided workflow: Code 3 → Fix copier.yml first

---

## Integration with Claude Desktop vs Claude Code

### Claude Code (Recommended for SAP Validation)

**Strengths**:
- Direct file system access (Read, Edit tools)
- Shell command execution (Bash tool for validator)
- Git integration (commit after validation)
- Multi-file editing (INDEX.md, catalog, copier.yml)

**Best Workflows**:
- Workflow 2: Fixing integration gaps (Edit tool for targeted changes)
- Workflow 3: Installing pre-commit hook (Bash tool)
- Workflow 5: New SAP development (Edit catalog/INDEX early, validate often)

---

### Claude Desktop (Best for Exploration)

**Strengths**:
- Interactive guidance
- Understanding validation logic
- Explaining integration points
- Planning SAP development workflow

**Best Workflows**:
- Workflow 1: Understanding validation output (explain what each check does)
- Explaining exit codes and priorities
- Suggesting fix strategies for complex gaps
- Planning pre-commit hook adoption

---

## Support & Resources

**SAP-061 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic SAP validation workflows
- [Capability Charter](capability-charter.md) - Problem and solution design
- [Protocol Spec](protocol-spec.md) - Validator algorithm, integration point schemas
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking, metrics, version history

**Validator Script**:
- `scripts/validate-ecosystem-integration.py` - Main validator (5 integration points)

**Pre-Commit Hook**:
- `scripts/git-hooks/pre-commit-ecosystem` - Git hook wrapper (runs validator)

**Related SAPs**:
- [SAP-000 (sap-framework)](../sap-framework/) - 5-artifact pattern foundation
- [SAP-050 (sap-catalog)](../sap-catalog/) - Machine-readable SAP catalog
- [SAP-056 (lifecycle-traceability)](../lifecycle-traceability/) - Dependency tracking
- [SAP-029 (sap-generation)](../sap-generation/) - SAP artifact generation

**Integration Points**:
- `docs/skilled-awareness/INDEX.md` - SAP registry (human-readable)
- `sap-catalog.json` - SAP metadata (machine-readable)
- `copier.yml` - Copier template questions (distribution)
- `docs/user-docs/adoption-paths/*.md` - Progressive adoption paths

---

## Version History

- **1.0.0** (2025-11-20): Initial CLAUDE.md for SAP-061
  - Claude Code workflows (validate, fix gaps, install hook, full validation, new SAP)
  - Tool usage patterns (Bash for validation, Edit for fixes, Read for context)
  - Claude-specific tips (exit codes, early integration, validate after each fix)
  - Common pitfalls (Write vs Edit, status checking, exit code priority)
  - Example complete SAP integration session (SAP-053, ~15-20k tokens)

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic SAP validation workflows
2. Review [protocol-spec.md](protocol-spec.md) for validator specification (exit codes, integration points)
3. Check [adoption-blueprint.md](adoption-blueprint.md) for pre-commit hook installation
4. Run first validation: `python scripts/validate-ecosystem-integration.py --all`
5. Install pre-commit hook: `cp scripts/git-hooks/pre-commit-ecosystem .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit`
