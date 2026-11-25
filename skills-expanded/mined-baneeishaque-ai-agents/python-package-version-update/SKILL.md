---
name: python-package-version-update
description: Industrial protocol for updating Python package versions in requirements files, installing updated packages in virtual environments, and verifying compatibility with existing codebase.
category: Package Management & Dependencies
---

# Python Package Version Update Skill

> **Skill ID:** `python-package-version-update`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Update Python package versions in requirements files (requirements.txt, local.txt, production.txt, etc.), install the updated packages in virtual environments, and verify compatibility with existing codebase usage patterns.

This skill addresses common scenarios where:
- Old package versions cause compilation failures (e.g., quickfix 1.15.1 failing on macOS ARM64)
- Newer versions provide better compatibility or bug fixes
- Teams need to upgrade packages while ensuring no breaking changes in their code

## Source Rules

This skill operationalizes best practices for:

- **Version Compatibility Analysis**: Scan codebase for package usage patterns before upgrading
- **Requirements File Updates**: Precise editing of version specifications
- **Virtual Environment Management**: Proper installation in isolated environments
- **Post-Installation Verification**: Ensure packages work correctly after upgrade

## Prerequisites

| Requirement | Minimum |
|---|---|
| Python | 3.8+ |
| pip | 20.0+ |
| Virtual Environment | Active venv with requirements files |
| Git | 2.x+ (for version control) |

## When to Apply

Apply this skill when:
- User asks: "update package version" or "upgrade [package] to [version]"
- Package installation fails due to version incompatibility
- Newer package versions provide better platform support (e.g., ARM64 wheels)
- Security updates or bug fixes are available in newer versions
- User wants to verify compatibility before committing version changes

Do NOT apply when:
- Package has breaking API changes that would require code modifications
- Project is in production and stability is critical
- User explicitly requests to keep current version
- No virtual environment is active

## Operational Logic

### Phase 1: Compatibility Analysis

1. **Codebase Usage Scan**
   ```bash
   # Search for package imports and usage patterns
   grep -r "import $PACKAGE_NAME\|from $PACKAGE_NAME" --include="*.py" .
   grep -r "$PACKAGE_NAME\." --include="*.py" .
   ```

2. **API Usage Assessment**
   - Identify classes, methods, and constants used from the package
   - Check for deprecated API usage that might break in newer versions
   - Review error handling patterns that depend on specific exceptions

3. **Version Compatibility Check**
   - Research changelog between current and target versions
   - Identify breaking changes or deprecated features
   - Assess migration complexity

### Phase 2: Requirements File Update

1. **File Location Identification**
   ```bash
   # Find requirements files
   find . -name "requirements*.txt" -o -name "*requirements.txt" | head -10
   ```

2. **Version Specification Update**
   - Locate the exact line with current version
   - Replace with new version specification
   - Preserve formatting and surrounding context

3. **Backup Creation**
   ```bash
   # Create backup before modification
   cp requirements/local.txt requirements/local.txt.backup
   ```

### Phase 3: Package Installation

1. **Virtual Environment Activation**
   ```bash
   # Ensure venv is active
   source .venv/bin/activate  # or appropriate activation command
   ```

2. **Package Installation**
   ```bash
   # Install updated package
   pip install $PACKAGE_NAME==$NEW_VERSION
   ```

3. **Dependency Resolution**
   - Handle any dependency conflicts
   - Update lock files if present (requirements-lock.txt, etc.)

### Phase 4: Verification & Testing

1. **Import Verification**
   ```python
   # Test basic import
   python -c "import $PACKAGE_NAME; print('Import successful')"
   ```

2. **Basic Functionality Test**
   - Run simple operations using the package
   - Verify no import errors or basic API changes

3. **Codebase Integration Check**
   - Run existing tests if available
   - Check for any runtime errors in package usage

## Environment & Dependencies

### Required Tools
- **Python**: 3.8+ with virtual environment support
- **pip**: 20.0+ for package management
- **grep**: For codebase analysis (standard on Unix systems)
- **find**: For file discovery (standard on Unix systems)

### Verification Commands
```bash
# Check Python version
python --version

# Check pip version
pip --version

# Verify virtual environment
which python  # Should point to venv/bin/python
echo $VIRTUAL_ENV  # Should show venv path
```

## Script Implementation

The implementation script is maintained as a separate executable file for editing, testing, and debugging.

- **Script file**: [scripts/update-package-version.ps1](scripts/update-package-version.ps1)

Run example (PowerShell):
```powershell
pwsh ./scripts/update-package-version.ps1 -PackageName quickfix -NewVersion 1.16.0
```

## Traceability & Related Conversations

This skill was created based on the following operational patterns:

- **Package Version Updates**: Handling version compatibility issues (e.g., quickfix 1.15.1 → 1.16.0 for ARM64 support)
- **Virtual Environment Management**: Proper installation in isolated Python environments
- **Codebase Compatibility Analysis**: Scanning for package usage patterns before upgrades
- **Requirements File Management**: Precise editing of version specifications in txt files

## Composition Rationale

This skill operates as a **composer skill** that leverages existing base skills:

- **Base Skills Used**:
  - [git-atomic-commit-construction](../git-atomic-commit-construction/SKILL.md) - For committing version updates
  - [python-venv-repair](../python-venv-repair/SKILL.md) - For virtual environment validation
 
- **Why Composer Pattern**: Package updates involve multiple concerns (file editing, environment management, compatibility analysis) that are domain-specific to Python package management, while delegating atomic operations to specialized base skills.