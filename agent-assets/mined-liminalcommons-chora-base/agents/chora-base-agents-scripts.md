# Scripts - Agent Awareness

**Domain**: Automation Scripts
**Purpose**: Python scripts for chora-base development and operations
**Cross-Platform**: Windows, Mac, Linux (CRITICAL requirement)

---

## ⚠️ BEFORE Writing ANY New Script

**STOP**: chora-base supports Windows, Mac, and Linux. Follow these patterns:

### Quick Checklist

- [ ] Copy [templates/cross-platform/python-script-template.py](../templates/cross-platform/python-script-template.py)
- [ ] Add UTF-8 reconfiguration if using emojis
- [ ] Use `encoding='utf-8'` for all file I/O
- [ ] Use `pathlib.Path` for all file paths
- [ ] NO bash scripts (Python only)
- [ ] Validate: `python scripts/validate-windows-compat.py --file your-script.py`

---

## Pattern 1: UTF-8 Console Output (Emojis/Unicode)

**When**: Script uses emojis (✅, ❌, ⚠️, etc.) or Unicode characters

**Pattern**:
```python
import sys

# Configure UTF-8 output for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
```

**Where**: Place immediately after imports, before any output

**Why**: Windows console defaults to cp1252, causing `UnicodeEncodeError` on emojis

**Reference**: [create-model-mcp-server.py:46-49](create-model-mcp-server.py#L46-L49)

---

## Pattern 2: File I/O with Encoding

**When**: Reading or writing ANY text file

**Pattern**:
```python
# Reading files
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Writing files
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Using pathlib (preferred)
from pathlib import Path
content = Path(file_path).read_text(encoding='utf-8')
Path(file_path).write_text(content, encoding='utf-8')
```

**Why**: Windows defaults to cp1252, causing silent data corruption

**Reference**: [generate-sap.py:24](generate-sap.py#L24)

---

## Pattern 3: Path Handling

**When**: ANY file path manipulation

**Pattern**:
```python
from pathlib import Path

# GOOD: Cross-platform path building
output_dir = Path(args.output)
file_path = output_dir / "subdir" / "file.txt"

# GOOD: Home directory
home = Path.home()

# GOOD: Current directory
current = Path.cwd()

# BAD: String concatenation (Unix-only)
# file_path = f"{args.output}/subdir/file.txt"  # ❌ Breaks on Windows

# BAD: Hardcoded home (Unix-only)
# home = Path("~/")  # ❌ Doesn't expand on Windows
```

**Why**: Windows uses backslashes (\), Unix uses forward slashes (/)

**Reference**: [create-model-mcp-server.py](create-model-mcp-server.py) (throughout)

---

## Pattern 4: Platform Detection

**When**: Need platform-specific behavior

**Pattern**:
```python
import sys

if sys.platform == 'win32':
    # Windows-specific code
    pass
elif sys.platform == 'darwin':
    # macOS-specific code
    pass
elif sys.platform.startswith('linux'):
    # Linux-specific code
    pass
```

**Reference**: [platform-info.py:66](platform-info.py#L66)

---

## Pattern 5: Environment Variables

**When**: Accessing environment variables (especially paths)

**Pattern**:
```python
import os
from pathlib import Path

# GOOD: Cross-platform home directory
home = os.environ.get("HOME") or os.environ.get("USERPROFILE", "")

# BETTER: Use pathlib
home = Path.home()

# GOOD: Check existence
if "PYTHONIOENCODING" in os.environ:
    print(f"Encoding: {os.environ['PYTHONIOENCODING']}")
```

**Reference**: [platform-info.py:66](platform-info.py#L66)

---

## Template: New Script

**Start here**: Copy this template and modify

```bash
cp templates/cross-platform/python-script-template.py scripts/your-new-script.py
```

**Template includes**:
- ✅ UTF-8 console reconfiguration
- ✅ File I/O with encoding
- ✅ Pathlib usage throughout
- ✅ Cross-platform path building
- ✅ Proper error handling
- ✅ Argument parsing with pathlib
- ✅ Exit codes
- ✅ Documentation

**See**: [templates/cross-platform/python-script-template.py](../templates/cross-platform/python-script-template.py)

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Missing Encoding

```python
# BAD
with open("file.txt") as f:
    content = f.read()

# GOOD
with open("file.txt", encoding='utf-8') as f:
    content = f.read()
```

**Impact**: Silent data corruption on Windows

---

### ❌ Mistake 2: String Path Concatenation

```python
# BAD
path = f"{base_dir}/subdir/file.txt"

# GOOD
from pathlib import Path
path = Path(base_dir) / "subdir" / "file.txt"
```

**Impact**: Breaks on Windows (uses backslashes)

---

### ❌ Mistake 3: Hardcoded Home Directory

```python
# BAD
home = Path("~/projects")

# GOOD
from pathlib import Path
home = Path.home() / "projects"
```

**Impact**: `~/` doesn't expand on Windows

---

### ❌ Mistake 4: Bash Scripts

```bash
#!/bin/bash
# BAD: Don't create new bash scripts
```

**Why**: Requires WSL/Git Bash on Windows

**Solution**: Use Python instead (cross-platform by default)

**See**: [BASH_SCRIPTS_README.md](BASH_SCRIPTS_README.md)

---

## Validation Workflow

### Before Committing

```bash
# 1. Validate your script
python scripts/validate-windows-compat.py --file scripts/your-script.py

# Expected output:
# ✅ No Windows compatibility issues found!
```

### Pre-Commit Hook (Recommended)

```bash
# Install hook (one-time setup)
git config core.hooksPath .githooks

# Hook automatically validates before commit
git commit -m "feat: add new script"
# 🔍 Running Windows compatibility checks...
# ✅ All Windows compatibility checks passed
```

---

## Example Scripts to Study

### Excellent Examples (Copy These Patterns)

| Script | Pattern | Lines |
|--------|---------|-------|
| [create-model-mcp-server.py](create-model-mcp-server.py) | ⭐ Complete reference | All patterns |
| [generate-sap.py](generate-sap.py) | File I/O encoding | 24 |
| [install-sap.py](install-sap.py) | UTF-8 console + paths | 42-49 |
| [platform-info.py](platform-info.py) | Platform detection | 66 |
| [validate-windows-compat.py](validate-windows-compat.py) | Validation patterns | Throughout |

---

## Automation Tools

### 1. Validation Script

**Purpose**: Detect Windows compatibility issues

```bash
# Validate entire scripts directory
python scripts/validate-windows-compat.py --scripts-only

# Validate specific file
python scripts/validate-windows-compat.py --file scripts/your-script.py

# JSON output for CI/CD
python scripts/validate-windows-compat.py --format json
```

**Checks**:
- ✅ Emojis without UTF-8 reconfiguration
- ✅ File I/O without encoding parameter
- ✅ Hardcoded Unix paths

---

### 2. Fix Script (Automated)

**Purpose**: Automatically fix common issues

```bash
# Dry run (show what would be fixed)
python scripts/fix-encoding-issues.py --dry-run --file your-script.py

# Apply fixes
python scripts/fix-encoding-issues.py --apply --file your-script.py
```

**Fixes**:
- ✅ Adds UTF-8 console reconfiguration
- ✅ Adds `encoding='utf-8'` to file I/O
- ✅ Ensures stderr is configured

---

## Directory Structure

```
scripts/
├── AGENTS.md                          ← You are here
├── BASH_SCRIPTS_README.md             ← Bash migration status
├── validate-windows-compat.py         ← Validation tool
├── fix-encoding-issues.py             ← Automated fixes
├── create-model-mcp-server.py         ← ⭐ Reference implementation
├── generate-sap.py                    ← ⭐ Good file I/O example
├── install-sap.py                     ← ⭐ Good UTF-8 example
├── platform-info.py                   ← ⭐ Platform detection example
├── deprecated/                        ← Old bash scripts
│   ├── README.md
│   └── *.sh                           ← Don't use these
└── [50+ other Python scripts]         ← All follow patterns above
```

---

## Related Documentation

### Detailed Guides

- **Complete Patterns**: [SAP-030: Cross-Platform Fundamentals](../docs/skilled-awareness/cross-platform-fundamentals/)
- **Migration Guide**: [Bash to Python Migration](../docs/user-docs/how-to/bash-to-python-migration.md)
- **Testing Checklist**: [Windows Testing Checklist](../docs/dev-docs/testing/windows-testing-checklist.md)
- **Enforcement Strategy**: [Cross-Platform Enforcement](../docs/project-docs/cross-platform-enforcement-strategy.md)

### Quick Links

- **Template**: [python-script-template.py](../templates/cross-platform/python-script-template.py)
- **Validation**: [validate-windows-compat.py](validate-windows-compat.py)
- **Pre-Commit Hook**: [../.githooks/pre-commit-windows-compat](../.githooks/pre-commit-windows-compat)
- **Summary**: [Windows Compatibility Summary](../docs/project-docs/windows-compatibility-summary.md)

---

## Development Policy

### New Scripts MUST

1. ✅ Be Python 3.8+ (NO bash)
2. ✅ Use `pathlib.Path` for all paths
3. ✅ Use `encoding='utf-8'` for all text file I/O
4. ✅ Add UTF-8 reconfiguration if using emojis
5. ✅ Pass `validate-windows-compat.py`
6. ✅ Follow template structure

### Pre-Commit Hook Will Block

1. ❌ New bash scripts (`.sh` files)
2. ❌ Scripts with critical Windows issues
3. ❌ Missing UTF-8 encoding (errors)

### CI/CD Will Validate

1. ✅ All scripts run on Windows runner
2. ✅ No encoding errors
3. ✅ Emojis display (or degrade gracefully)

---

## FAQ

### Q: Why Python instead of bash?

**A**: Bash requires WSL/Git Bash on Windows. Python is cross-platform by default.

### Q: What if I don't have a Windows machine to test?

**A**: Use the validation script (`validate-windows-compat.py`) and rely on CI/CD.

### Q: Can I use bash for quick one-offs?

**A**: No. Even "quick" scripts become long-lived. Use Python.

### Q: What about PowerShell for Windows-specific tasks?

**A**: Avoid. Use Python with platform detection (`sys.platform == 'win32'`).

### Q: Do I really need `encoding='utf-8'` everywhere?

**A**: YES. Windows defaults to cp1252. Silent corruption is worse than crashes.

### Q: What if my emoji doesn't display on Windows?

**A**: That's OK (font limitation). Important: no crashes. Windows Terminal supports emojis.

---

## Support

### Issues or Questions

- **Windows Compatibility Issues**: Open issue with `windows-compatibility` label
- **Pre-Commit Hook Problems**: See [../.githooks/pre-commit-windows-compat](../.githooks/pre-commit-windows-compat)
- **CI/CD Failures**: Check GitHub Actions logs + [Windows Testing Checklist](../docs/dev-docs/testing/windows-testing-checklist.md)

### Quick Fixes

```bash
# Script won't run on Windows?
python scripts/fix-encoding-issues.py --apply --file your-script.py

# Pre-commit hook failing?
python scripts/validate-windows-compat.py --file your-script.py

# Want to bypass hook (not recommended)?
git commit --no-verify
```

---

**Version**: 1.0.0
**Last Updated**: 2025-11-08
**Maintained By**: Chora-base contributors
**Cross-Platform Score**: 85/100 (target: 95/100)
