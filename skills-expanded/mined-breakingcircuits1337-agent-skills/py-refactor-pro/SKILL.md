---
name: py-refactor-pro
description: Analyzes Python code for complexity, security vulnerabilities, and maintainability issues. Use when you need to audit a codebase, identify refactoring candidates, or get a health report on Python projects.
---

# Python Refactor Pro

## Overview
This skill provides deep analysis of Python codebases, leveraging "Big Pickle" logic to identify complexity hotspots, security risks, and maintainability issues.

## Usage

### 1. Run Analysis
To generate a JSON report of metrics and vulnerabilities for a file or directory:

```bash
python3 scripts/code_analyzer.py <path>
```

**Example Output:**
```json
[
  {
    "file_path": "main.py",
    "complexity": 15,
    "score": 85.5,
    "vulnerabilities": []
  }
]
```

### 2. Interpret Results
- **Complexity**: Sum of decision points. Aim for < 10 per function.
- **Maintainability Index**: 0-100 scale. > 80 is good, < 50 requires attention.
- **Vulnerabilities**: Critical issues like hardcoded secrets or `eval()` usage.

### 3. Refactoring Guidance
Consult `references/rules.md` for specific actions based on the analysis findings.

## Resources
- `scripts/code_analyzer.py`: The core analysis engine.
- `references/rules.md`: Dictionary of refactoring rules and thresholds.