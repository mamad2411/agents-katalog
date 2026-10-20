# Discoverability-Based Enforcement (SAP-031) - Claude-Specific Awareness

**SAP ID**: SAP-031
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-08

---

## 📖 Quick Reference

**New to SAP-031?** → Read **[README.md](README.md)** first (19-min read)

The README provides:
- 🚀 **Quick Start** - 5-minute setup (root AGENTS.md reminder → domain AGENTS.md patterns → template files)
- 📚 **5-Layer Architecture** - Discoverability (70%), Pre-Commit (20%), CI/CD (9%), Documentation, Review (1%)
- 🎯 **90%+ Prevention Rate** - Achieve through strategic pattern placement (Layer 1) + automation (Layers 2-3)
- 🔧 **Integration with SAP-009** - Nested awareness hierarchy for strategic pattern placement
- 📊 **Self-Service Tools** - Validation scripts, auto-fix tools, educational error messages
- 🔗 **Integration** - Works with SAP-009 (Awareness), SAP-006 (Quality Gates), SAP-005 (CI/CD)

This CLAUDE.md provides: Claude Code tool integration for enforcement (Read, Write, Edit, Bash), pattern placement workflows, and validation troubleshooting.

---

## Claude Code Enforcement Workflows

### Workflow 1: Setting Up Layer 1 (Discoverability)

```markdown
User: "Set up cross-platform enforcement for this project"

Claude (Phase 1: Layer 1 Setup - Root AGENTS.md):
1. Read root AGENTS.md to understand existing structure
2. Edit root AGENTS.md to add enforcement reminder:
   ## 🔴 CROSS-PLATFORM REMINDER

   **ALL code MUST run on Windows, macOS, and Linux without modification.**

   Before writing scripts or file I/O, read: **[scripts/AGENTS.md](scripts/AGENTS.md)** for cross-platform patterns.

   **Quick Template**: Copy [templates/cross-platform-script.py](templates/cross-platform-script.py)

Claude (Phase 2: Layer 1 Setup - Domain AGENTS.md):
3. Create scripts/AGENTS.md with patterns:
   Write scripts/AGENTS.md
   # Content: 3-5 core patterns with examples (UTF-8 console, file I/O encoding, pathlib)

Claude (Phase 3: Layer 1 Setup - Template File):
4. Create templates/cross-platform-script.py:
   Write templates/cross-platform-script.py
   # Content: Production-ready template with patterns pre-implemented

Claude (Phase 4: Validation):
5. Test discovery workflow:
   - Read root AGENTS.md (see reminder)
   - Read scripts/AGENTS.md (see patterns)
   - Read templates/cross-platform-script.py (see implementation)
   - Confirm all components accessible within 3 minutes

Result: Layer 1 (discoverability) set up, 70% prevention expected
```

---

### Workflow 2: Writing Code with Enforcement

```markdown
User: "Write a Python script to process config files"

Claude (Before writing - Discovery):
1. Read root AGENTS.md at session start
2. See 🔴 CROSS-PLATFORM REMINDER
3. Navigate to scripts/AGENTS.md (read patterns)
4. Copy templates/cross-platform-script.py (production-ready starting point)

Claude (During writing - Implementation):
5. Use template as starting point:
   - UTF-8 console output already configured
   - File I/O with encoding='utf-8' already implemented
   - Path handling with pathlib already implemented
6. Add domain-specific logic to template structure

Result: Code follows all cross-platform patterns (patterns pre-implemented from template)
```

---

### Workflow 3: Validating Code Before Commit

```markdown
User: "Check if my code follows cross-platform patterns"

Claude:
1. Run validation script:
   Bash: python scripts/validate-cross-platform.py

2. If violations found:
   - Review educational error messages
   - Option 1: Fix manually (Edit tool to fix files)
   - Option 2: Auto-fix (Bash: python scripts/fix-cross-platform-issues.py)
   - Option 3: Override (git commit --no-verify, not recommended)

3. Re-run validation after fixes:
   Bash: python scripts/validate-cross-platform.py
   # Expected: ✅ All files comply

4. Commit changes:
   Bash: git add . && git commit -m "Fix cross-platform issues"
   # Pre-commit hook runs validation automatically

Result: Code validated before commit, violations prevented
```

---

## Claude-Specific Tips

### Tip 1: Always Read Root AGENTS.md at Session Start

**Pattern**:
```markdown
Claude (at session start):
1. Read AGENTS.md (project root)
2. Look for 🔴 emoji (enforcement reminders)
3. Navigate to linked domain AGENTS.md files
4. Copy linked template files when writing new code
```

**Why**: 70% of violations prevented through discoverability (Layer 1)

---

### Tip 2: Use Templates as Starting Points

**Pattern**:
```markdown
Claude (when writing new file):
1. Check if template exists for file type
2. Copy template using Write tool
3. Customize domain-specific logic (patterns already implemented)
4. No need to remember all patterns (pre-implemented in template)
```

**Why**: Templates have all patterns pre-implemented, eliminating pattern omission errors

---

### Tip 3: Run Validation Before Committing

**Pattern**:
```markdown
Claude (before git commit):
1. Run validation: Bash: python scripts/validate-[domain].py
2. If violations: Auto-fix: Bash: python scripts/fix-[domain]-issues.py
3. Re-validate: Bash: python scripts/validate-[domain].py
4. Commit: Bash: git commit -m "message"
```

**Why**: Catch violations before commit (avoid pre-commit hook blocking)

---

### Tip 4: Use Educational Error Messages

**Pattern**:
```markdown
Claude (when validation fails):
1. Read error message:
   ❌ file.py:42: open() without explicit encoding
   Why: Default encoding varies by platform (utf-8 on Linux/macOS, cp1252 on Windows)
   Fix: Add encoding='utf-8' parameter
   Auto-fix: python scripts/fix-cross-platform-issues.py --add-encoding

2. Understand "Why" (explains rationale)
3. Apply "Fix" (specific action)
4. Or use "Auto-fix" (one-command fix)
```

**Why**: Educational messages explain rationale + how to fix (not just "invalid")

---

### Tip 5: Track Prevention Rates

**Pattern**:
```markdown
Claude (biweekly measurement):
1. Measure baseline violations (Week 0):
   Bash: python scripts/validate-[domain].py --count-violations
   # Output: violations_baseline = 100

2. Measure current violations (Week 2, 4, 6):
   Bash: python scripts/validate-[domain].py --count-violations
   # Output: violations_current = 8

3. Calculate prevention rate:
   prevention_rate = (100 - 8) / 100 = 92%

4. Target: ≥ 90% (violations_current / violations_baseline ≤ 10%)
```

**Why**: Measure effectiveness objectively (data-driven improvement)

---

## Common Pitfalls for Claude

### Pitfall 1: Not Reading Root AGENTS.md at Session Start

**Problem**: Claude writes code without discovering enforcement patterns

**Fix**:
```markdown
Claude (at session start):
ALWAYS read root AGENTS.md first
Look for 🔴 emoji (enforcement reminders)
Navigate to linked domain AGENTS.md before writing code
```

---

### Pitfall 2: Starting from Scratch Instead of Using Templates

**Problem**: Claude writes code from scratch, omits patterns

**Fix**:
```markdown
Claude (when writing new file):
CHECK for template first
COPY template using Write tool
CUSTOMIZE domain-specific logic (patterns already implemented)
```

---

### Pitfall 3: Not Running Validation Before Commit

**Problem**: Pre-commit hook blocks commit, requires rework

**Fix**:
```markdown
Claude (before git commit):
ALWAYS run validation: python scripts/validate-[domain].py
FIX violations before commit (manual or auto-fix)
COMMIT after validation passes
```

---

## Support & Resources

**SAP-031 Documentation**:
- [README.md](README.md) - Complete enforcement guide (19-min read)
- [AGENTS.md](AGENTS.md) - Generic agent patterns (15-min read)
- [Protocol Spec](protocol-spec.md) - Technical specification (23-min read)
- [Adoption Blueprint](adoption-blueprint.md) - 3-level setup guide (25-min read)

**Example Implementations**:
- [scripts/AGENTS.md](../../scripts/AGENTS.md) - Cross-platform patterns
- [scripts/validate-cross-platform.py](../../scripts/validate-cross-platform.py) - Validation script
- [templates/cross-platform-script.py](../../templates/cross-platform-script.py) - Template file

**Related SAPs**:
- [SAP-009 (Agent Awareness)](../agent-awareness/) - Nested awareness hierarchy
- [SAP-006 (Quality Gates)](../quality-gates/) - Pre-commit hooks
- [SAP-005 (CI/CD)](../ci-cd-workflows/) - GitHub Actions validation

---

## Version History

- **1.0.0** (2025-11-08): Initial CLAUDE.md for SAP-031
  - Claude Code enforcement workflows
  - Tool usage patterns (Read, Write, Edit, Bash)
  - Discovery and validation patterns
  - Common pitfalls and tips
  - Prevention rate tracking

---

**Next Steps**:
1. Read [README.md](README.md) for complete enforcement guide
2. Start with Layer 1 (discoverability): root AGENTS.md → domain AGENTS.md → templates
3. Use templates as starting points when writing new code
4. Run validation before committing
5. Track prevention rates biweekly (target ≥ 90%)
