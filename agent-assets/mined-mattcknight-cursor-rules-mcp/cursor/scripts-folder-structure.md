---
description: Scripts folder structure and Python script requirements for documentation conversion
alwaysApply: false
tags: [documentation, scripts, python, automation]
priority: 2
version: 1.0.0
---

# Scripts Folder Structure

## Purpose

The `scripts/` folder contains generic, reusable Python scripts for documentation conversion and validation. These scripts should be copied from template projects or created once and reused across all projects.

## Directory Structure

```
scripts/
├── convert_md_to_html_for_presentation.py  # Convert .presentation.md to HTML
├── validate_spec_file.py                    # Validate .spec.md files
└── README.md                                # Script usage documentation
```

## Script Requirements

### Script Location
- ✅ Scripts MUST be placed in `scripts/` folder at repository root
- ✅ Scripts MUST be generic and reusable across projects
- ✅ Scripts MUST support both Windows (PowerShell) and Unix/Linux paths

### Script Sources

**Option 1: Copy from Template Projects**
- Copy scripts from: `C:\Work\Repositories\OneInc\claimspay3\claimspay4_AI\Zero Payment\scripts`
- Or from other template projects that have proven scripts
- Ensure scripts are generic (no project-specific paths)

**Option 2: Create Generic Scripts**
- Create reusable scripts based on existing patterns
- Ensure cross-platform compatibility
- Document usage in `scripts/README.md`

## Required Scripts

### 1. convert_md_to_html_for_presentation.py

**Purpose**: Convert `.presentation.md` files to HTML

**Usage**:

**OS Detection:** Use `py` on Windows, `python` or `python3` on Unix/Linux/Mac

```bash
# Windows (PowerShell)
py scripts\convert_md_to_html_for_presentation.py docs\presentation\<input>.presentation.md docs\presentation\<output>.html

# Unix/Linux/Mac
python scripts/convert_md_to_html_for_presentation.py docs/presentation/<input>.presentation.md docs/presentation/<output>.html
# OR
python3 scripts/convert_md_to_html_for_presentation.py docs/presentation/<input>.presentation.md docs/presentation/<output>.html
```

**Requirements**:
- ✅ Accept input file path (must be `.presentation.md`)
- ✅ Accept output file path (should be `.html`)
- ✅ Generate HTML with Mermaid diagram support
- ✅ Include syntax highlighting for code blocks
- ✅ Responsive design
- ✅ Professional styling
- ✅ Warn if input is not `.presentation.md`
- ✅ Place output relative to input file (same directory)

### 2. validate_spec_file.py

**Purpose**: Validate that a file is a proper specification file

**Usage**:

**OS Detection:** Use `py` on Windows, `python` or `python3` on Unix/Linux/Mac

```bash
# Windows (PowerShell)
py scripts\validate_spec_file.py docs\specifications\<file>.spec.md

# Unix/Linux/Mac
python scripts/validate_spec_file.py docs/specifications/<file>.spec.md
# OR
python3 scripts/validate_spec_file.py docs/specifications/<file>.spec.md
```

**Requirements**:
- ✅ Confirm file is a spec file (ends with `.spec.md`)
- ✅ Provide guidance on using spec files
- ✅ Warn against HTML conversion
- ✅ Validate file structure and content

## Script Development Guidelines

### Python Version
- ✅ Support Python 3.8+
- ✅ Use standard library where possible
- ✅ Document required dependencies

### Cross-Platform Support
- ✅ Handle Windows paths (`\`) and Unix paths (`/`)
- ✅ Use `os.path` or `pathlib` for path operations
- ✅ Test on both Windows and Linux

### Error Handling
- ✅ Validate input file exists
- ✅ Validate file extensions match expected types
- ✅ Provide clear error messages
- ✅ Exit with appropriate error codes

### Output
- ✅ Generate clean, professional HTML
- ✅ No operational metadata visible to stakeholders
- ✅ No warning banners in generated documents
- ✅ Relative paths in output (for portability)

## Integration with Rules

### Related Rules
- **spec-vs-presentation-file-pattern.mdc**: Defines file naming and directory structure
- **documentation-workflow.mdc**: Defines when to generate HTML
- **mermaid-diagram-syntax-rules.mdc**: Defines Mermaid syntax requirements

### Rule Alignment
- Scripts MUST enforce directory structure rules (`/docs/presentation/`, `/docs/specifications/`)
- Scripts MUST validate file extensions (`.presentation.md`, `.spec.md`)
- Scripts MUST generate HTML relative to presentation files

## Examples

### Example: Converting Presentation File

```bash
# Create presentation file
# File: docs/presentation/solution-architecture.presentation.md

# Convert to HTML
py scripts\convert_md_to_html_for_presentation.py docs\presentation\solution-architecture.presentation.md docs\presentation\solution-architecture.html

# Output: docs/presentation/solution-architecture.html
```

### Example: Validating Spec File

```bash
# Validate spec file
py scripts\validate_spec_file.py docs\specifications\implementation-spec.spec.md

# Output: Validation results and guidance
```

## Critical Rules

### ALWAYS
- ✅ Place scripts in `scripts/` folder at repository root
- ✅ Use generic, reusable scripts
- ✅ Support cross-platform paths
- ✅ Generate HTML relative to presentation files
- ✅ Validate file extensions before processing

### NEVER
- ❌ Create project-specific scripts in `scripts/` folder
- ❌ Hardcode project paths in scripts
- ❌ Skip validation of file extensions
- ❌ Generate HTML with absolute paths
- ❌ Include operational metadata in generated HTML

---

**Last Updated:** 2025-01-22  
**Version:** 1.0.0  
**Rule Type:** Scripts and Automation  
**Priority:** MEDIUM
