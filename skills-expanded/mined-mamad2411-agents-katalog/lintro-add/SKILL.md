---
name: lintro-add
description: Guide for adding new linting/formatting tools to lintro. Use when implementing shellcheck, shfmt, sqlfluff, taplo, semgrep, gitleaks, or any new tool plugin.
---

# Adding a New Tool to Lintro

Lintro is a unified CLI for code linting/formatting with a plugin architecture:
tools are defined in `lintro/tools/definitions/<tool>.py` (via `@register_tool`),
parsed by `lintro/parsers/<tool>/`, tested in `tests/unit/`, with sample violation
files in `test_samples/tools/`.

## Related Skills

- `stand-py`: Python coding standards (type hints, docstrings, trailing commas)
- `test`: pytest best practices (no classes, use fixtures, parametrize)
- `commit`: semantic commit format when committing changes

## How to Implement: Copy a Reference, Don't Write From Scratch

Do NOT write plugin/parser/test code from a template. Pick the closest existing
implementation, read all of its files (definition, issue class, parser, parser
`__init__.py`, sample violation file, parser tests, plugin tests), and mirror
that structure exactly for the new tool:

- **Simple tool (no fix)**: `lintro/tools/definitions/actionlint.py`, `hadolint.py`
- **Tool with fix support**: `lintro/tools/definitions/ruff.py`, `black.py`
- **Security scanner**: `lintro/tools/definitions/bandit.py`, `semgrep.py`
- **Shell tools**: `lintro/tools/definitions/shellcheck.py`, `shfmt.py`

The parser lives in `lintro/parsers/<reference-tool>/` and its tests in
`tests/unit/parsers/` and `tests/unit/tools/<reference-tool>/` — copy the pattern
from the same reference tool so imports, mocking, and naming stay consistent.

## Quick Reference

### New files (paths)

```text
lintro/parsers/<tool>/__init__.py
lintro/parsers/<tool>/<tool>_issue.py
lintro/parsers/<tool>/<tool>_parser.py
lintro/tools/definitions/<tool>.py
test_samples/tools/<category>/<tool>/<tool>_violations.<ext>
tests/unit/parsers/test_<tool>_parser.py
tests/unit/tools/<tool>/__init__.py
tests/unit/tools/<tool>/test_<tool>_plugin.py
```

### Updated files (paths)

```text
lintro/enums/tool_name.py              # Add to ToolName enum (alphabetical)
lintro/tools/core/version_parsing.py   # Add to TOOLS_WITH_SIMPLE_VERSION_PATTERN
lintro/tools/core/version_checking.py  # Add install hints in get_install_hints()
lintro/_tool_versions.py               # Add version (external tools only)
lintro/tools/manifest.json             # Add tool entry (version MUST match _tool_versions.py)
lintro/cli_utils/commands/doctor.py    # Add to TOOL_COMMANDS for health check
package.json                           # Add version for npm tools (must match _tool_versions.py)
renovate.json                          # Add custom managers for BOTH _tool_versions.py AND manifest.json
pyproject.toml                         # Add parser package + [tool.lintro.versions] entry
Dockerfile                             # Add to verification steps (root AND non-root blocks)
Dockerfile.tools                       # Add to verification step (tool --version)
scripts/utils/install-tools.sh         # Add installation command (external tools)
scripts/ci/homebrew/templates/lintro.rb.template  # Add depends_on + update caveats (if Homebrew-installable)
```

For every updated file, find an existing tool's entry in that file and add the new
tool the same way (alphabetical order where the file is ordered).

### Version Consistency (CRITICAL for external tools)

For external tools (not bundled Python packages), versions must be consistent across:

1. **`lintro/_tool_versions.py`** — source of truth for install-tools.sh
2. **`lintro/tools/manifest.json`** — must match `_tool_versions.py` for
   binary/cargo/rustup tools
3. **`package.json`** — for npm tools, must match `_tool_versions.py`
4. **Plugin `min_version`** — in the tool definition, should match or be <=
   `_tool_versions.py`
5. **`renovate.json`** — must have custom regex managers updating BOTH
   `_tool_versions.py` AND `manifest.json` (copy an existing tool's pair of
   entries and adjust the package name and datasource)

CI enforces manifest/version sync with the manifest generator run in `--check`
mode (the generate-with---check pattern from `stand-ci` — no separate verify
script). **PRs fail if versions drift between these files.** Run the generator
with `--check` locally before pushing.

### Homebrew Formula (for Homebrew-installable tools)

- Add `depends_on "<tool>"` to `scripts/ci/homebrew/templates/lintro.rb.template`
  and list the tool in the caveats under the appropriate category.
- Bundled Python tools (ruff, black, mypy, bandit, yamllint) are excluded from the
  Homebrew venv via `generate_resources.py --exclude`; they install as separate
  Homebrew formulae and are discovered via PATH (`shutil.which`), NOT `python -m`.
  `PythonBundledBuilder` in `command_builders.py` handles this automatically.

## ToolType Options

```python
ToolType.LINTER          # Code quality checker
ToolType.FORMATTER       # Code formatter
ToolType.TYPE_CHECKER    # Type checking (mypy)
ToolType.DOCUMENTATION   # Doc checker (darglint)
ToolType.SECURITY        # Security scanner (bandit, semgrep, gitleaks)
ToolType.INFRASTRUCTURE  # IaC linter (hadolint, actionlint)
ToolType.TEST_RUNNER     # Test framework (pytest)
```

Can be combined: `ToolType.LINTER | ToolType.FORMATTER`

## Common Gotchas

1. **Version command variations**: some tools use `version` instead of `--version`
   (e.g., `gitleaks version`). Check the tool's CLI.
2. **ToolResult invariant for fix operations**:
   `initial_issues_count = fixed_issues_count + remaining_issues_count`.
3. **Test mocking**: mock the version check with
   `patch("lintro.plugins.execution_preparation.verify_tool_version", return_value=None)`
   and subprocess calls with `patch.object(plugin, "_run_subprocess", ...)` — copy
   the patterns from a reference tool's plugin tests.
4. **File discovery**: `_prepare_execution()` handles filtering by `file_patterns`;
   use `ctx.rel_files` for the filtered list.
5. **Subprocess safety**: always use list args, never `shell=True`; add
   `# nosec B404` on the subprocess import.
6. **Return early**: if `ctx.should_skip` is True, return `ctx.early_result`.
7. **Parser function naming**: must be
   `parse_<tool>_output(output: str | None) -> list[<Tool>Issue]`.
8. **Issue class**: must inherit from `BaseIssue`; use `DISPLAY_FIELD_MAP` for
   custom field name mappings.

## Deprecated Patterns to Avoid

- Do NOT create tool-specific formatters (use the unified formatter)
- Do NOT modify `lintro/tools/tool_enum.py` (deleted — registry is automatic)
- Do NOT modify `lintro/tools/core/tool_base.py` (deleted — use BaseToolPlugin)

## Verification Checklist

- [ ] `uv run lintro tools` shows the new tool
- [ ] `uv run lintro check --tools <tool> .` runs without error — single-tool runs are
      normally banned by the `lint` skill; this is the explicit sanctioned
      exception for verifying a tool under development. Still finish with a full
      `uv run lintro chk`.
- [ ] `uv run lintro doctor` shows the tool with correct version (no "No cmd defined")
- [ ] Tool detects violations in the sample file
- [ ] Parser unit tests pass: `pytest tests/unit/parsers/test_<tool>_parser.py -v`
- [ ] Plugin unit tests pass: `pytest tests/unit/tools/<tool>/ -v`
- [ ] Coverage >80% on new code
- [ ] No linting errors: `uv run lintro fmt && uv run lintro chk`
- [ ] Manifest generator passes in `--check` mode (no version drift)
- [ ] Tool added to `Dockerfile` (root and non-root blocks) and `Dockerfile.tools`
- [ ] Tool added to `install-tools.sh` (external tools only)
- [ ] Tool added to `lintro/tools/manifest.json` (version matches `_tool_versions.py`)
- [ ] Renovate managers added for BOTH `_tool_versions.py` and `manifest.json`
- [ ] Homebrew template updated with `depends_on` + caveats (if Homebrew-installable)
- [ ] Docker image builds: `docker build -t py-lintro:test .`

Use the `lintro-verify` skill for the full post-implementation review.
