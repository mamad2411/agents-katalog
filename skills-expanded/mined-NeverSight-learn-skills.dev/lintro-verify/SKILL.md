---
name: lintro-verify
description: Verify that a lintro tool implementation is complete and follows all project standards. Use after adding a new tool to lintro.
---

# Verify Lintro Tool Implementation

Use this skill to verify that a lintro tool implementation is complete and follows all
project standards.

## Usage

When asked to verify a tool (e.g., `/lintro-verify tsc`), run through all checklist
items below.

---

## 1. Core Implementation

### Plugin Definition

- [ ] `lintro/tools/definitions/<tool>.py` exists
- [ ] Uses `@register_tool` decorator from `lintro.plugins.registry`
- [ ] Inherits from `BaseToolPlugin`
- [ ] `ToolDefinition` includes:
  - `name` - tool identifier (lowercase)
  - `description` - clear description of what the tool does
  - `file_patterns` - list of glob patterns (e.g., `["*.ts", "*.tsx"]`)
  - `tool_type` - appropriate `ToolType` enum value
  - `can_fix` - boolean indicating if tool supports auto-fix
  - `native_configs` - list of config files the tool uses (e.g., `["tsconfig.json"]`)
  - `version_command` - command to check version (e.g., `["tsc", "--version"]`)
  - `priority` - execution priority (default 50)
- [ ] `check()` method implemented
- [ ] `fix()` method implemented (or raises `NotImplementedError` if `can_fix=False`)
- [ ] Options defined with proper types and defaults

### Parser

- [ ] `lintro/parsers/<tool>/` directory exists with:
  - `__init__.py` - exports parser and issue classes
  - `<tool>_parser.py` - parses tool output into issues
  - `<tool>_issue.py` - issue dataclass with `to_display_row()` method
- [ ] Parser handles all output formats the tool produces
- [ ] Parser handles edge cases (empty output, errors, warnings)

### Enums (if needed)

- [ ] Tool added to `lintro/enums/tool_name.py` if it has a `ToolName` enum

### Version Management

- [ ] Version added to `lintro/_tool_versions.py` (for external tools)
- [ ] Install hint added to `lintro/tools/core/version_checking.py`
      `get_install_hints()` templates
- [ ] Version is reasonably current (check latest: `npm view <tool> version` or `brew
info <tool>`)

### Version Consistency (CRITICAL)

- [ ] **All version sources are aligned:**
  - `lintro/_tool_versions.py` version
  - `package.json` version (for npm tools)
  - Plugin `min_version` in tool definition
  - `lintro/tools/manifest.json` version
- [ ] Renovate custom manager exists in `renovate.json` for `_tool_versions.py`
- [ ] `package.json` uses caret (^) prefix matching `_tool_versions.py` (e.g., ^0.27.0)
- [ ] Plugin `min_version` equals or is less than `_tool_versions.py` version

### Doctor Health Check

- [ ] Tool added to `TOOL_COMMANDS` in `lintro/cli_utils/commands/doctor.py`
- [ ] `lintro doctor` shows tool with correct version (no "No cmd defined")

### Command Builder (if needed)

- [ ] If tool needs special command building, added to
      `lintro/tools/core/command_builders.py`

### CLI Option Verification

- [ ] Run `<tool> --help` and compare against implemented `set_options()` parameters
- [ ] Verify each option is a real CLI flag (not config-file-only)
- [ ] Test `--tool-options` actually work: `lintro check . --tools <tool> --tool-options
"<tool>:option=value"`
- [ ] Document which settings are CLI-available vs config-file-only in docs

### Native Config Integration

- [ ] Run `<tool> --init` (if available) to see default config structure
- [ ] If tool has config file with useful settings, check if
      `lintro/utils/native_parsers.py` should parse it
- [ ] Verify `native_configs` in ToolDefinition lists all supported config files

---

## 2. Documentation

### README.md

- [ ] Tool added to **Supported Tools** table with badge, language, and fix support
- [ ] Tool added to **Optional External Tools** list (for external tools) with install
      commands

### docs/getting-started.md

- [ ] Tool added to **Optional External Tools** section with install instructions
- [ ] Usage example section added (if tool has unique features)

### docs/configuration.md

- [ ] Full configuration section added including:
  - Tool description
  - Installation instructions (all methods: brew, npm/bun, pip, etc.)
  - Native config file example
  - Available `--tool-options` table
  - Usage examples

### docs/tool-analysis/{tool}-analysis.md

- [ ] Tool analysis document created following the standard format:
  - Overview of what the tool does
  - Core Tool Capabilities (native features)
  - Lintro Implementation Analysis:
    - Preserved Features (what lintro exposes)
    - Limited / Missing (what's NOT available via lintro)
    - Enhancements (what lintro adds: timeout, normalization, etc.)
  - Usage Comparison (native vs lintro commands)
  - Configuration Strategy
  - Priority and Conflicts
  - Recommendations (when to use lintro vs native tool)

---

## 3. Tests

### Unit Tests

- [ ] `tests/unit/tools/<tool>/` directory with:
  - `test_options.py` - definition attributes, default options, set_options validation
  - `test_execution.py` - check/fix with mocked subprocess
- [ ] `tests/unit/parsers/test_<tool>_parser.py` - parser tests covering:
  - Single error/warning parsing
  - Multiple issues parsing
  - Empty output handling
  - Edge cases (different file extensions, paths, etc.)
  - `to_display_row()` output

### Integration Tests

- [ ] `tests/integration/tools/test_<tool>_integration.py` with:
  - `pytest.mark.skipif` for when tool not installed
  - Fixtures for test files (with issues and clean)
  - `test_definition_attributes` - name, can_fix
  - `test_definition_file_patterns` - correct patterns
  - `test_check_file_with_issues` - detects problems
  - `test_check_clean_file` - no false positives
  - `test_check_empty_directory` - handles gracefully
  - `test_set_options` - options work correctly

### Test Samples

- [ ] `test_samples/tools/<language>/<tool>/` directory with:
  - `<tool>_violations.<ext>` - file with deliberate issues (verify tool detects them)
  - `<tool>_clean.<ext>` - valid file without issues (verify no false positives)
- [ ] Violations file triggers actual tool errors when run directly: `<tool>
<violations_file>`

---

## 4. CI/CD & Docker

### Dockerfile.tools

- [ ] Tool version verification added (e.g., `tsc --version && \`)

### Dockerfile (runtime)

- [ ] Tool binary/wrapper copied from builder stage
- [ ] For Node.js tools: wrapper script created in `/usr/local/bin/`

### scripts/utils/install-tools.sh

- [ ] Tool added to help text description
- [ ] Installation block added with version from `_tool_versions.py`
- [ ] Tool added to "Installed tools" echo list
- [ ] Tool added to `tools_to_verify` array

### scripts/ci/tools-image-verify.sh

- [ ] Tool version check added

### .github/workflows/tools-image.yml

- [ ] Verify trigger paths include relevant files (usually automatic via
      Dockerfile.tools)

---

## 5. User Experience

### lintro list-tools

- [ ] Tool appears with correct name, language, actions, priority, config type

### Error Handling

- [ ] Graceful handling when tool not installed
- [ ] Clear error messages with install hints
- [ ] No crashes on malformed tool output

### Install Hints

- [ ] All common installation methods documented (brew, npm/bun, pip, cargo, etc.)
- [ ] Version placeholders work correctly in hints

---

## 6. Verification Commands

Run these to verify implementation:

```bash
# Unit tests
uv run pytest tests/unit/tools/<tool>/ tests/unit/parsers/test_<tool>_parser.py -v

# Integration tests (requires tool installed)
uv run pytest tests/integration/tools/test_<tool>_integration.py -v

# Test on sample files
uv run lintro check test_samples/tools/<language>/<tool>/ --tools <tool>

# Verify tool appears in list
uv run lintro list-tools | grep <tool>

# Full lint check
uv run lintro chk

# Full test suite
uv run pytest tests/ -v
```

### Version Consistency Verification

```bash
# Check all version sources are aligned (replace <tool> with actual name)
echo "=== _tool_versions.py ===" && grep "<tool>" lintro/_tool_versions.py
echo "=== manifest.json ===" && grep -A3 '"<tool>"' lintro/tools/manifest.json
echo "=== package.json ===" && grep "<tool>" package.json
echo "=== Plugin min_version ===" && grep "min_version" lintro/tools/definitions/<tool>.py
echo "=== Renovate manager ===" && grep -A5 '"<tool>"' renovate.json | head -10
echo "=== Doctor TOOL_COMMANDS ===" && grep "<tool>" lintro/cli_utils/commands/doctor.py
```

### CLI Option Verification Commands

```bash
# Compare native CLI options against lintro implementation
<tool> --help

# Check version currency
npm view <tool> version        # for npm packages
brew info <tool>               # for Homebrew packages
pip index versions <tool>      # for Python packages

# Test that tool-options actually work (should not error)
uv run lintro check test_samples/ --tools <tool> --tool-options "<tool>:timeout=60"

# Test each documented option (replace with actual options)
uv run lintro check . --tools <tool> --tool-options "<tool>:option_name=value"

# Generate default config to understand structure
<tool> --init  # if available
```

---

## 7. Common Issues to Check

- [ ] No "Missing install hints for tools" warning when running lintro
- [ ] Tool respects `--tool-options` passed via CLI
- [ ] Tool uses native config file when present
- [ ] Parser correctly maps severity levels
- [ ] File paths in issues are correct (relative vs absolute)
- [ ] Line/column numbers are 1-indexed (not 0-indexed)
- [ ] Tool timeout is configurable and has reasonable default
- [ ] **CLI options actually exist** - verify with `<tool> --help` (some tools only
      support options via config file)
- [ ] **Version is current** - check if pinned version is significantly outdated
- [ ] **Config-file-only options** are not exposed as `--tool-options` (will cause
      runtime errors)
- [ ] **Version consistency** - `_tool_versions.py`, `package.json`, and plugin
      `min_version` are aligned
- [ ] **Renovate manager** - custom regex manager exists in `renovate.json` for external
      tools

---

## Review Output Format

After reviewing, provide a summary:

```text
## Tool Review: <tool_name>

### Status: PASS / FAIL / PARTIAL

### Checklist Summary
- Core Implementation: X/Y items
- Documentation: X/Y items
- Tests: X/Y items
- CI/Docker: X/Y items
- User Experience: X/Y items

### Missing Items
1. [item description]
2. [item description]

### Recommendations
1. [recommendation]
2. [recommendation]
```
