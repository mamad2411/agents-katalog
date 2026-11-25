---
name: python-script-generation
description: Standards for generating "Ultra-Lean Industrial" Python scripts, ensuring type safety, modularity, and pedagogical documentation.
category: Scripting
---

# Python Script Generation Skill

This document defines the craftsmanship standards for generating Python scripts. Adhering to these protocols ensures that all scripts are professional, maintainable, and pedagogical.

***

## 1. Scope & Context

This skill mandates a strictly disciplined approach to Python scripting. It prioritizes:

- **Zero Noise**: No introductory fluff or unnecessary comments.
- **Type Safety**: Mandatory use of the `typing` module.
- **Modularity**: Multi-repository logic sharing via base engines and thin wrappers.
- **Documentation**: Mandatory adjacent explainers using the **Code Explanation** skill.

***

## 2. Industrial Standards & Formatting

All generated Python scripts MUST adhere to the following standards:

- **Shebang**: MUST start with `#!/usr/bin/env python3`.
- **Encoding**: Explicitly declare encoding if special characters are used: `# -*- coding: utf-8 -*-`.
- **Linting**: MUST be compliant with `ruff` and `pylint`.
- **Formatting**: Adhere to PEP 8 standards. Use `ruff format` if available.

### 2.1 Structural Hierarchy (Skill-First Compliance)

All scripts MUST follow a predictable, industrialized structure:

- **H1 Header**: Matches the YAML title in documentation.
- **Scope Statement**: A brief paragraph in the docstring defining *why* the script exists.
- **Docstrings**: MUST use triple-double quotes `"""..."""` and follow Googley style.

### 2.2 Interpreter Invocation

Scripts MUST use `#!/usr/bin/env python3` shebang (see §2 above).  For runtime
resolution — which interpreter to invoke when `python3` on PATH is
unavailable, outdated, or blocked by mise cascade — see
[`mise-tool-management §3.3`](../mise-tool-management/SKILL.md#33-runtime-tool-resolution).

For **documentation** of invocation commands in skill files, the simplified
`python3` form MUST be used; do NOT embed fragile path-resolution commands
like `PY=~/.local/share/mise/installs/python/$(ls …)/bin/python` in docs.
See [skill-factory mandate #7](../skill-factory/SKILL.md#2211-universal-script-mandates).

***

## 3. Type Safety & Defensive Programming

Python's flexibility must be constrained by strict type safety and defensive logic.

- **Mandatory Type Hints**: Every function signature MUST include type hints for all parameters and return values using the `typing` module (e.g., `List`, `Dict`, `Optional`, `Union`, `Any`).
- **Defensive I/O**:
    - Always verify file/directory existence before operations using `os.path.exists()` or `pathlib.Path.exists()`.
    - Use `try-except` blocks for all network, filesystem, and external process logic.
    - Implement robust error logging rather than silent failures.
- **Runtime Validation**: Use `isinstance()` or schema validation for complex data structures to ensure runtime safety.

***

## 4. Core Design Philosophy: The "Industrial Standard"

All script generation MUST prioritize:

- **Extensible**: Logic must be modular and designed to accommodate future parameters or requirements without refactoring the core engine.
- **Maintainable**: Code must be clean, dry, and pedagogical.
- **Portable**: Scripts must use relative paths or environment variables to function across different local filesystems.
- **Modular**: Logic must be separated into distinct engines and wrappers.

***

## 5. Prototypical Scenario: Modular "Base Sync" Logic

To ensure industrially portable toolsets, follow this pattern for synchronization or complex automation:

### 5.1 The Modular Engine (`base_sync.py`)

Create a parameter-driven core class (e.g., `SyncManager`) that encapsulates the primary logic.

- **Mandatory Parameters**: `rules_dir`, `skills_dir`, `templates_dir`, `readme_template`, `index_template`, `readme_output`, `index_output`.
- **Flexible Initialization**: Allow flags like `index_template` and `index_output` to default to `None`.
- **Conditional Execution**: Process logic only for provided directories (e.g., "Process rules if `rules_dir` is provided; process skills if `skills_dir` is provided").

### 5.2 Thin Wrapper Architecture

Create lightweight scripts that instantiate and run the modular engine with specific configurations:

- **Example `sync_rules.py`**: Configure with `rules_dir="."` and `skills_dir=None`.
- **Example `sync_skills.py`**: Configure with `rules_dir=None` and `skills_dir=".agents/skills"`.

***

## 6. Documentation & Explainer Integration

The script itself is only half of the implementation.

- **Adjacent Explainers**: Every generated script MUST have an adjacent explainer file following the **[Code Explanation](../code-explanation/SKILL.md)** skill.
- **Industrial Explainer Pattern (1.4)**: Use the `[filename].[extension].md` naming convention (e.g., `my_script.py.md`).
- **Pedagogical Comments**: Use block comments *before* logic to explain the "Why" behind implementation choices.

***

## 7. Environment & Dependencies

Every implementation MUST include a dedicated section or comment block listing dependencies.

- **Verification Logic**: Provide logic to autonomously verify required tools (e.g., Python version, `ruff`).
- **Installation Logic**: Provide standard package manager commands (e.g., `pip install ruff pylint`).

***

## 8. Status Traceability & Performance

- **Atomic Commits**: Script changes must be committed atomically following **[Git Atomic Commit Construction Rules](../../../ai-agent-rules/git-atomic-commit-construction-rules.md)**.
- **Performance**: Mandate efficient I/O operations (e.g., batching file reads) to ensure responsiveness.
