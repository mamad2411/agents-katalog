# Awareness Guide: Discoverability-Based Enforcement

**SAP ID**: SAP-031
**Version**: 1.0.0
**For**: AI Agents, LLM-Based Assistants
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

This AGENTS.md provides: Agent-specific enforcement workflows, layer-by-layer adoption patterns, and prevention rate measurement for AI coding assistants.

---

## 1. Core Concepts for Agents

### Key Concepts

**Concept 1**: 5-Layer Defense in Depth
- **Description**: Each layer provides incremental prevention (70% → 90% → 99% → support → 100%), allowing agents/developers to catch issues earlier in the workflow
- **When to use**: Configure all 5 layers for critical quality domains (security, cross-platform), start with Layer 1 for new domains
- **Example**: Cross-platform enforcement uses discoverability (root + domain AGENTS.md), pre-commit hooks (validation), CI/CD (Windows/Mac/Linux testing), documentation (CONTRIBUTING.md), and review (PR checklist)

**Concept 2**: Discoverability via SAP-009 Integration
- **Description**: Leverage nested awareness hierarchy (root AGENTS.md → domain AGENTS.md → templates) to place patterns where agents naturally look during workflow
- **When to use**: Always start with Layer 1 (discoverability) before adding validation layers
- **Example**: Session start → read root AGENTS.md (see cross-platform reminder) → navigate to scripts/AGENTS.md (find patterns) → copy template (pre-implemented patterns)

**Concept 3**: Progressive Enforcement (Warn → Educate → Block)
- **Description**: Start with warnings to collect false positives, refine rules, then promote to blocking
- **When to use**: New validation rules should start as warnings (Layer 2: pre-commit warn-only), promote to blocking after false-positive refinement
- **Example**: Week 1: Pre-commit warns about missing UTF-8 encoding → Week 2: Refine to exclude binary files → Week 3: Promote to blocking

**Concept 4**: Self-Service Remediation
- **Description**: Provide one-command fix tools to reduce friction when validation fails
- **When to use**: For automatable fixes (encoding, formatting, simple refactoring), not for complex logic changes
- **Example**: `python scripts/fix-encoding-issues.py --apply` automatically adds `encoding='utf-8'` to all `open()` calls

### Decision Tree

```
User asks to enforce quality standard
   │
   ├─ SAP-009 adopted?
   │   │
   │   ├─ YES → Proceed with SAP-031 (use nested awareness)
   │   └─ NO → Adopt SAP-009 first (foundation for discoverability)
   │
   ├─ Patterns automatable?
   │   │
   │   ├─ YES (70%+) → Full 5-layer enforcement
   │   ├─ PARTIAL (30-70%) → Layers 1, 4, 5 (discoverability + docs + review)
   │   └─ NO (<30%) → Documentation-only (SAP-031 not applicable)
   │
   ├─ Prevention rate target?
   │   │
   │   ├─ ≥90% → Implement all 5 layers
   │   ├─ 70-90% → Layers 1-3 (skip Layer 4 docs if time-constrained)
   │   └─ <70% → Layers 1-2 (discoverability + pre-commit)
   │
   └─ Existing validation tools?
       │
       ├─ YES → Integrate with Layer 2 (pre-commit) + Layer 3 (CI/CD)
       └─ NO → Create validation scripts, then integrate
```

---

## 2. Common Agent Workflows

### Workflow 1: Implementing Enforcement for New Quality Domain

**User Request**: "Enforce [quality domain] standards (e.g., accessibility, security, testing)"

**Agent Actions**:

1. **Verify SAP-009 adoption** (prerequisite):
   ```bash
   # Check for root AGENTS.md and domain AGENTS.md structure
   test -f AGENTS.md && test -d docs/skilled-awareness/
   ```

2. **Layer 1 (Discoverability)** - Add reminder to root AGENTS.md:
   ```markdown
   ## 🔴 [QUALITY DOMAIN] REMINDER

   **ALL code MUST [quality requirement].**

   Before [activity], read: **[domain AGENTS.md path]** for [quality domain] patterns.

   **Quick Template**: Copy [template file path]
   ```

3. **Layer 1 (Discoverability)** - Create domain AGENTS.md with patterns:
   ```bash
   # Create or update domain AGENTS.md
   # Include: Pattern 1, Pattern 2, Pattern 3, Template link
   # Max 200 lines for quick reference
   ```

4. **Layer 1 (Discoverability)** - Create template file:
   ```bash
   # Copy similar template or create from scratch
   # Pre-implement all patterns (production-ready)
   # Location: templates/[domain]/[template-name].[ext]
   ```

5. **Layer 2 (Pre-Commit)** - Create validation hook:
   ```python
   # .githooks/pre-commit-[quality-domain]
   # Validate Pattern 1, Pattern 2, Pattern 3
   # Educational error messages
   # Self-service fix tool reference
   ```

6. **Layer 2 (Pre-Commit)** - Install hook:
   ```bash
   git config core.hooksPath .githooks
   chmod +x .githooks/pre-commit-[quality-domain]
   ```

7. **Layer 3 (CI/CD)** - Create validation workflow:
   ```yaml
   # .github/workflows/[quality-domain]-validation.yml
   # Matrix testing on target platforms/environments
   # Artifact upload for validation reports
   ```

8. **Layer 4 (Documentation)** - Update CONTRIBUTING.md:
   ```markdown
   ## [Quality Domain] Requirements

   - [ ] Pattern 1
   - [ ] Pattern 2
   - [ ] Pattern 3
   - [ ] Run: python scripts/validate-[domain].py
   ```

9. **Layer 4 (Documentation)** - Update PR template:
   ```markdown
   ### [Quality Domain] Checklist

   - [ ] Patterns validated via pre-commit hook
   - [ ] CI/CD validation passing
   - [ ] Template used (if applicable)
   ```

10. **Measure prevention rate**:
    ```bash
    # Baseline: Count existing violations
    python scripts/validate-[domain].py

    # After 2 weeks: Count new violations
    git log --since="2 weeks ago" --oneline | wc -l  # Total commits
    # Compare: violations / commits
    # Target: ≥90% prevention
    ```

**Validation**:
```bash
# Verify all layers installed
test -f AGENTS.md && grep "[QUALITY DOMAIN] REMINDER" AGENTS.md  # Layer 1
test -f .githooks/pre-commit-[quality-domain]  # Layer 2
test -f .github/workflows/[quality-domain]-validation.yml  # Layer 3
grep "[Quality Domain]" CONTRIBUTING.md  # Layer 4
```

**Expected Output**:
```
✅ Layer 1 (Discoverability): Reminder in AGENTS.md, patterns in domain AGENTS.md, template file
✅ Layer 2 (Pre-Commit): Hook installed, validation working
✅ Layer 3 (CI/CD): Workflow created, first run passing
✅ Layer 4 (Documentation): CONTRIBUTING.md + PR template updated
✅ Prevention rate: [X]% → target ≥90%
```

**Common Variations**:
- **Variation 1**: If no CI/CD platform, skip Layer 3 (rely on Layers 1-2 + manual review)
- **Variation 2**: If patterns not automatable, implement Layers 1 + 4 only (discoverability + docs)
- **Variation 3**: If low false-positive confidence, start Layer 2 in warn-only mode (don't block commits)

---

### Workflow 2: Integrating Existing Validation Tools

**User Request**: "We have validation scripts but they're not consistently run"

**Agent Actions**:

1. **Identify existing validation tools**:
   ```bash
   # Find validation scripts
   find scripts/ -name "validate-*.py" -o -name "check-*.py"
   ```

2. **Create pre-commit hook wrapper**:
   ```python
   # .githooks/pre-commit-[quality-domain]
   import subprocess

   def main():
       result = subprocess.run(['python', 'scripts/validate-[domain].py'])
       if result.returncode != 0:
           print("❌ ERROR: [Quality Domain] validation failed!")
           print("\nRequired action:")
           print("  1. Run: python scripts/validate-[domain].py")
           print("  2. Fix issues")
           print("  3. Try commit again")
           return 1
       return 0
   ```

3. **Add CI/CD integration**:
   ```yaml
   # .github/workflows/[quality-domain]-validation.yml
   - name: Run [Quality Domain] validation
     run: python scripts/validate-[domain].py
   ```

4. **Add discoverability layer**:
   ```bash
   # Update root AGENTS.md with reminder
   # Update domain AGENTS.md with validation command
   ```

**Validation**:
```bash
# Test pre-commit hook
git commit -m "test" --dry-run  # Should run validation

# Test CI/CD workflow
gh workflow run [quality-domain]-validation.yml
```

---

### Workflow 3: Measuring and Improving Prevention Rate

**User Request**: "How effective is our enforcement? Can we improve it?"

**Agent Actions**:

1. **Establish baseline metrics**:
   ```bash
   # Count violations before enforcement
   python scripts/validate-[domain].py > baseline-report.txt
   VIOLATIONS_BEFORE=$(grep "ERROR" baseline-report.txt | wc -l)
   ```

2. **Implement enforcement (Workflow 1)**

3. **Measure prevention after 2 weeks**:
   ```bash
   # Count new violations since enforcement
   git log --since="2 weeks ago" --name-only | grep "\.py$" | sort -u > recent-files.txt
   python scripts/validate-[domain].py --file-list recent-files.txt > current-report.txt
   VIOLATIONS_AFTER=$(grep "ERROR" current-report.txt | wc -l)

   # Calculate prevention rate
   PREVENTION_RATE=$(echo "scale=2; (1 - $VIOLATIONS_AFTER / $VIOLATIONS_BEFORE) * 100" | bc)
   echo "Prevention Rate: ${PREVENTION_RATE}%"
   ```

4. **Identify gaps** (if prevention rate <90%):
   ```bash
   # Analyze where violations still occur
   grep "ERROR" current-report.txt | awk '{print $1}' | sort | uniq -c | sort -nr

   # Common gaps:
   # - Pattern not in domain AGENTS.md (discoverability gap)
   # - Pre-commit hook not catching pattern (validation gap)
   # - Developers using --no-verify (bypass)
   ```

5. **Improve enforcement**:
   - **Gap 1 (Discoverability)**: Add missing pattern to domain AGENTS.md, update template
   - **Gap 2 (Validation)**: Enhance pre-commit hook to catch pattern
   - **Gap 3 (Bypass)**: Add CI/CD as second line of defense, educate on --no-verify usage

**Validation**:
```bash
# Target: ≥90% prevention rate
# Measure: violations_after / violations_before ≤ 10%
```

---

## 3. Quick Reference for Agents

### Key Commands

```bash
# Install enforcement framework
git config core.hooksPath .githooks  # Enable pre-commit hooks

# Validate enforcement setup
python scripts/validate-enforcement.py

# Validate specific quality domain
python scripts/validate-[domain].py

# Self-service fix (if available)
python scripts/fix-[domain]-issues.py --apply

# Measure prevention rate
# 1. Baseline: python scripts/validate-[domain].py > baseline.txt
# 2. After 2 weeks: python scripts/validate-[domain].py > current.txt
# 3. Compare: diff baseline.txt current.txt

# CI/CD workflow trigger
gh workflow run [quality-domain]-validation.yml

# Bypass pre-commit (use sparingly)
git commit --no-verify  # Document reason in commit message
```

### Important File Paths

| File | Purpose | Agent Action |
|------|---------|--------------|
| `AGENTS.md` (root) | Session-start awareness | Add enforcement reminder with link to domain AGENTS.md |
| `[domain]/AGENTS.md` | Task-start patterns | Add 5 core patterns (max 200 lines) + template link |
| `templates/[domain]/[template].[ext]` | Production-ready starting point | Create with patterns pre-implemented |
| `.githooks/pre-commit-[domain]` | Pre-commit validation | Create hook with educational error messages |
| `.github/workflows/[domain]-validation.yml` | CI/CD validation | Create workflow with matrix testing |
| `CONTRIBUTING.md` | Contribution guidelines | Add quality domain checklist |
| `.github/pull_request_template.md` | PR checklist | Add quality domain verification |
| `scripts/validate-[domain].py` | Validation tool | Reference in hooks + CI/CD |
| `scripts/fix-[domain]-issues.py` | Self-service fix tool | Provide one-command remediation |
| `.chora/enforcement.yaml` | Enforcement config | Configure layers per domain |

### Configuration Snippets

**Configuration 1**: Enable enforcement for quality domain

```yaml
# .chora/enforcement.yaml
enforcement:
  enabled: true

  domains:
    [quality-domain]:
      enabled: true
      severity: critical  # block | warn | info

      # Layer 1: Discoverability
      discoverability:
        root_agents_reminder: true
        domain_agents_patterns: true
        templates_enabled: true

      # Layer 2: Pre-Commit
      pre_commit:
        enabled: true
        performance_target_seconds: 10

      # Layer 3: CI/CD
      ci_cd:
        enabled: true
        platforms: [ubuntu-latest, macos-latest, windows-latest]

      # Patterns to enforce
      patterns:
        - [pattern-1-identifier]
        - [pattern-2-identifier]
        - [pattern-3-identifier]
```

**Configuration 2**: Pre-commit hook template

```python
#!/usr/bin/env python3
"""Pre-commit hook: Validate [Quality Domain]"""

import sys
from pathlib import Path

# UTF-8 console (cross-platform)
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def validate_pattern(file_path: Path) -> list[str]:
    """Validate pattern - return list of errors"""
    errors = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Validation logic
    return errors

def main():
    print("🔍 Running [Quality Domain] validation...")
    # Get staged files, validate, report errors
    return 0  # or 1 if errors

if __name__ == '__main__':
    sys.exit(main())
```

### Common Patterns

**Pattern 1**: Layer 1 Discoverability (Root AGENTS.md)

```markdown
## 🔴 [QUALITY DOMAIN] REMINDER

**ALL code MUST [quality requirement].**

Before [activity], read: **[scripts/AGENTS.md](scripts/AGENTS.md)** for [quality domain] patterns.

**Quick Template**: Copy [templates/[domain]/template.py](templates/[domain]/template.py)
```

**Pattern 2**: Layer 1 Discoverability (Domain AGENTS.md)

```markdown
# [Domain] AGENTS.md

## [Quality Domain] Patterns

### Pattern 1: [Name]
**Description**: [What this enforces]

**Example**:
```[language]
[Code showing correct pattern]
```

**Template**: [templates/[domain]/template.[ext]](templates/[domain]/template.[ext])
```

**Pattern 3**: Layer 2 Educational Error Message

```python
if violation_detected:
    print("❌ ERROR: [Quality Domain] issue found!\n")
    print(f"  File: {file_path}")
    print(f"  Issue: [Specific violation]\n")
    print("Why this matters: [Explanation]")
    print("How to fix: [Step-by-step]\n")
    print("Quick fix: python scripts/fix-[domain]-issues.py --apply\n")
    print("See: [domain AGENTS.md path]")
    print("Bypass (not recommended): git commit --no-verify")
```

**Pattern 4**: Layer 3 CI/CD Matrix Testing

```yaml
strategy:
  fail-fast: false
  matrix:
    platform: [ubuntu-latest, macos-latest, windows-latest]
    version: ['3.8', '3.11']  # or Node.js versions, etc.

steps:
  - name: Run validation on ${{ matrix.platform }} - Version ${{ matrix.version }}
    run: python scripts/validate-[domain].py
```

---

## 4. Integration with Other SAPs

### Required Dependencies

#### SAP-009 (agent-awareness)

**Integration Point**: Nested awareness hierarchy (root + domain AGENTS.md)

**Agent Workflow**:
1. Session start → read root AGENTS.md (SAP-009)
2. See enforcement reminder (SAP-031 Layer 1)
3. Navigate to domain AGENTS.md (SAP-009 pattern)
4. Find quality domain patterns (SAP-031 Layer 1)
5. Copy template (SAP-031 Layer 1)

**Configuration**:
```markdown
# Root AGENTS.md (SAP-009 structure)
## Navigation Tree
- Domain 1: [docs/skilled-awareness/AGENTS.md]
- Domain 2: [scripts/AGENTS.md]  ← Add SAP-031 enforcement reminder

## 🔴 CROSS-PLATFORM REMINDER  ← SAP-031 Layer 1
**ALL code MUST work on Windows, Mac, and Linux.**
Before writing Python scripts, read: **[scripts/AGENTS.md](scripts/AGENTS.md)**
**Quick Template**: Copy [templates/cross-platform/python-script-template.py]
```

**When to Use**: Always - SAP-031 requires SAP-009 for discoverability layer

---

### Optional Dependencies

#### SAP-006 (quality-gates)

**Integration Point**: Pre-commit hook framework

**Agent Workflow**:
1. SAP-006 provides pre-commit infrastructure (.pre-commit-config.yaml)
2. SAP-031 adds domain-specific validation hooks (.githooks/pre-commit-[domain])
3. Both frameworks coexist (SAP-006 for linting/type-checking, SAP-031 for quality domains)

**Configuration**:
```yaml
# .pre-commit-config.yaml (SAP-006)
repos:
  - repo: local
    hooks:
      - id: ruff  # SAP-006
        name: Ruff Linting
        entry: ruff check
        language: system

      - id: [quality-domain]-validation  # SAP-031
        name: [Quality Domain] Validation
        entry: .githooks/pre-commit-[quality-domain]
        language: python
        pass_filenames: false
```

**When to Use**: If SAP-006 already adopted (unified hook management)

---

#### SAP-005 (ci-cd-workflows)

**Integration Point**: CI/CD automation framework

**Agent Workflow**:
1. SAP-005 provides GitHub Actions infrastructure
2. SAP-031 adds domain-specific validation workflows
3. Workflows run in parallel (SAP-005 for tests/linting, SAP-031 for quality domains)

**Configuration**:
```yaml
# .github/workflows/[quality-domain]-validation.yml (SAP-031)
# Uses SAP-005 patterns: matrix testing, artifact upload, status badges

name: [Quality Domain] Validation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ${{ matrix.platform }}
    strategy:
      matrix:
        platform: [ubuntu-latest, macos-latest, windows-latest]  # SAP-005 pattern
```

**When to Use**: If CI/CD platform available (Layer 3 enforcement)

---

#### SAP-030 (cross-platform-fundamentals)

**Integration Point**: Reference implementation of SAP-031 enforcement

**Agent Workflow**:
1. User asks: "How do I implement enforcement for [quality domain]?"
2. Agent references SAP-030 cross-platform enforcement as example
3. Adapt patterns to new quality domain

**When to Use**: As reference when implementing enforcement for new quality domains

---

## 5. Common Mistakes and How to Avoid Them

### Mistake 1: Skipping Layer 1 (Discoverability)

**Symptom**: Pre-commit hooks catch issues, but agents/developers don't know how to fix them

**Why It Happens**: Jumped straight to Layer 2 (validation) without establishing discoverability

**Fix**:
```markdown
# Always start with Layer 1
1. Add reminder to root AGENTS.md
2. Create domain AGENTS.md with patterns
3. Create template file
4. THEN add validation (Layer 2)
```

**Prevention**: Follow Workflow 1 in order (Layers 1 → 2 → 3 → 4 → 5)

---

### Mistake 2: Over-Enforcement (Too Many Rules)

**Symptom**: Developers frequently use --no-verify, prevention rate stagnates <70%

**Why It Happens**: Added all validation rules at once (too strict too fast)

**Fix**:
```bash
# Start with critical-only rules (warn-only mode)
# Week 1: Enable warnings
# Week 2: Collect false-positive reports
# Week 3: Refine rules, promote to blocking
```

**Prevention**: Use progressive enforcement (warn → educate → block)

---

### Mistake 3: Poor Error Messages

**Symptom**: Validation fails but agents/developers don't know how to fix

**Why It Happens**: Error messages only say "what" failed, not "why" or "how to fix"

**Fix**:
```python
# Educational error message template:
print("❌ ERROR: [What failed]")
print("Why: [Business reason]")
print("How to fix: [Step-by-step]")
print("Quick fix: [One-command remediation]")
print("Learn more: [Link to domain AGENTS.md]")
```

**Prevention**: Always include "Why" + "How to fix" in error messages

---

### Mistake 4: Template Files Out of Sync

**Symptom**: Template file doesn't match patterns in domain AGENTS.md

**Why It Happens**: Updated patterns but forgot to update template

**Fix**:
```bash
# Diff patterns vs template
# Update template to match current patterns
# Version template with SAP version (e.g., template-v1.1.0)
```

**Prevention**: Update template alongside domain AGENTS.md, version both together

---

### Mistake 5: No Prevention Rate Measurement

**Symptom**: Don't know if enforcement is effective

**Why It Happens**: Implemented layers but never measured baseline vs current violations

**Fix**:
```bash
# Establish baseline
python scripts/validate-[domain].py > baseline.txt

# Measure after 2 weeks
python scripts/validate-[domain].py > current.txt

# Calculate prevention rate
# Target: ≥90%
```

**Prevention**: Always measure baseline before enforcement, re-measure after 2 weeks

---

## 6. Performance Considerations for Agents

### Pre-Commit Hook Performance

**Target**: <10 seconds execution time

**Optimization Strategies**:
- Validate only staged files (not entire repository)
- Use compiled regex patterns (cache)
- Parallel validation for independent checks
- Early exit on first critical error (fail-fast)

**Example**:
```python
import subprocess

# Get staged files only
result = subprocess.run(['git', 'diff', '--cached', '--name-only'], capture_output=True, text=True)
staged_files = result.stdout.strip().split('\n')

# Validate only staged files
for file_path in staged_files:
    if file_path.endswith('.py'):  # Filter by extension
        validate(file_path)  # Skip non-Python files
```

---

### Pattern Discovery Performance

**Target**: <30 seconds from session start to finding pattern

**Optimization Strategies**:
- Root AGENTS.md reminder points directly to domain AGENTS.md (1 click)
- Domain AGENTS.md max 200 lines (quick scan)
- Template link at top of domain AGENTS.md (no scrolling)

**Example**:
```markdown
# scripts/AGENTS.md (domain AGENTS.md)

**Quick Template**: [templates/cross-platform/python-script-template.py](templates/cross-platform/python-script-template.py) ← Top of file

## Cross-Platform Patterns
[Patterns below, max 200 lines]
```

---

## 7. Troubleshooting for Agents

### Problem: Pre-commit hook blocking legitimate code

**Symptom**: Validation fails but code is correct (false positive)

**Diagnosis**:
```bash
# Check what pattern failed
.githooks/pre-commit-[quality-domain] --verbose

# Review validation logic
cat .githooks/pre-commit-[quality-domain] | grep "def validate"
```

**Solution**:
1. If legitimate edge case, bypass with `git commit --no-verify` and document reason
2. File issue to refine validation rule (reduce false positives)
3. Quarterly review of false-positive rate

---

### Problem: CI/CD validation passing locally but failing in CI

**Symptom**: Pre-commit hook passes, but CI/CD fails

**Diagnosis**:
```bash
# Download validation report artifact from failed CI run
gh run download [run-id] --name validation-report

# Check for platform-specific differences
cat validation-report.md | grep "ERROR"
```

**Solution**:
1. Reproduce locally on target platform (or use Docker container)
2. Fix platform-specific issue (e.g., Windows vs Linux path separators)
3. Use cross-platform patterns (SAP-030) to avoid future issues

---

### Problem: Prevention rate <90% despite enforcement

**Symptom**: Enforcement installed but violations still occurring

**Diagnosis**:
```bash
# Identify where violations occur
python scripts/validate-[domain].py > current-violations.txt
grep "ERROR" current-violations.txt | awk '{print $1}' | sort | uniq -c | sort -nr

# Check if --no-verify being used
git log --all --grep="--no-verify" --oneline
```

**Solution**:
1. **Gap 1 (Discoverability)**: Pattern not in domain AGENTS.md → add pattern + update template
2. **Gap 2 (Validation)**: Pre-commit hook not catching pattern → enhance validation logic
3. **Gap 3 (Bypass)**: Frequent --no-verify usage → educate on proper use, add CI/CD as second line of defense

---

## 8. Reference: Cross-Platform Enforcement (Case Study)

### Problem

chora-base had 142 cross-platform issues (38 critical, 104 high priority), 65/100 Windows compatibility score

### SAP-031 Implementation

**Layer 1 (Discoverability)**:
- Root AGENTS.md: "🔴 CROSS-PLATFORM REMINDER" → link to scripts/AGENTS.md
- scripts/AGENTS.md: 5 patterns (UTF-8 console, file I/O encoding, pathlib, etc.)
- templates/cross-platform/python-script-template.py: Production-ready template

**Layer 2 (Pre-Commit)**:
- .githooks/pre-commit-windows-compat: Validates emoji → UTF-8, encoding parameter, path patterns
- scripts/fix-encoding-issues.py: One-command fix tool

**Layer 3 (CI/CD)**:
- .github/workflows/cross-platform-test.yml: Windows/Mac/Linux matrix testing

**Layer 4 (Documentation)**:
- CONTRIBUTING.md: Cross-platform checklist
- .github/pull_request_template.md: PR checklist with cross-platform verification

**Layer 5 (Review)**:
- Human verification: At least one platform manual testing

### Results

- **Prevention Rate**: 99%+ (0 critical issues after enforcement)
- **Pattern Discovery**: <30 sec (scripts/AGENTS.md quick reference)
- **Fix Time**: 1-command (`python scripts/fix-encoding-issues.py --apply`)
- **Review Overhead**: <5% (checklist verification only)
- **Compatibility Score**: 65/100 → 95/100

### Lessons Learned

1. **Discoverability is 70% of success** - Most issues prevented by making patterns easy to find
2. **Educational error messages reduce support burden** - Developers self-serve instead of asking for help
3. **Templates > Documentation** - Easier to copy correct template than write from scratch
4. **Progressive enforcement reduces friction** - Warn first, block after refinement
5. **Measure prevention rate** - Can't improve what you don't measure

---

**Version History**:
- **1.0.0** (2025-11-08): Initial awareness guide for Discoverability-Based Enforcement
  - 3 common workflows (implement enforcement, integrate tools, measure prevention)
  - Quick reference (commands, file paths, patterns)
  - Integration with SAP-009 (discoverability), SAP-006 (pre-commit), SAP-005 (CI/CD)
  - Cross-platform reference implementation (case study)
  - 5 common mistakes and troubleshooting guide
