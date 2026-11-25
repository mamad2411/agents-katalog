---
name: markdown-lint-workflow
description: Three-step pipeline for fixing markdown lint issues — markdownlint-cli2 --fix, companion scripts, manual fix + audit.
category: General
---

# Markdown Lint Workflow (v1)

This skill provides the three-step pipeline protocol for fixing markdown lint
issues in any project. It is consumed by:

- **`markdown-generation`** — post-generation linting
- **`skill-factory` §3** — post-drafting linting
- **Any skill that edits `.md` files** — pre-submission lint verification

The companion scripts under [`scripts/`](scripts/) handle patterns that
`markdownlint-cli2 --fix` does not resolve (line length, table alignment, fence
language tags, list style, heading spacing, etc.).

-

## 1. The 3-Step Pipeline

Before finalizing ANY markdown file, run these steps in order:

### Step 1: Auto-Fix

```bash
markdownlint-cli2 --fix <file_path>
```

- Run from the project root where `.markdownlint.jsonc` lives.
- Use paths **relative** to the project root — absolute paths can cause the
  tool to silently find 0 files (`Linting: 0 file(s)`) and do nothing.

**Caveat:** `markdownlint-cli2 --fix` corrupts bare closing fences for MD040.
Do NOT rely on `--fix` for MD040 — Step 2 handles it correctly. See §2.2.

### Step 2: Companion Scripts

Run ALL companion scripts from [§2](#2-companion-scripts) in the
[required execution order](#21-execution-order). Each script accepts
`--check` for a dry-run preview; omit `--check` to apply changes in-place.

```bash
# Quick overview of available scripts:
python3 .agents/skills/general/markdown-lint-workflow/scripts/fix-table-separators.py file.md
python3 .agents/skills/general/markdown-lint-workflow/scripts/fix-fenced-code-language.py file.md
python3 .agents/skills/general/markdown-lint-workflow/scripts/fix-container-fence.py file.md
python3 .agents/skills/general/markdown-lint-workflow/scripts/wrap-long-lines.py --max 120 file.md
python3 .agents/skills/general/markdown-lint-workflow/scripts/fix-emphasis-as-heading.py file.md
python3 .agents/skills/general/markdown-lint-workflow/scripts/fix-list-style.py file.md
python3 .agents/skills/general/markdown-lint-workflow/scripts/fix-heading-spacing.py file.md
```

For a single automated invocation, see the
[Convenience Pipeline Script](#3-convenience-pipeline-script).

### Step 3: Manual Fix + Final Audit

Fix any remaining semantic or structural errors (e.g., heading increments,
broken cross-references, anchor mismatches). Then verify:

```bash
markdownlint-cli2 <file_path>
```

Zero errors means the file is lint-compliant.

-

## 2. Companion Scripts

This skill ships seven helper scripts under
[`scripts/`](scripts/) for one-shot lint fixes:

- [`fix-table-separators.py`](scripts/fix-table-separators.py) — scans for
  compact table separators (`|---|---|`) and rewrites them with proper spacing
  (`| --- | --- |`) to satisfy MD060. Use `--check` for dry-run.
- [`wrap-long-lines.py`](scripts/wrap-long-lines.py) — wraps prose lines
  exceeding the configured `--max` width (default 120) while preserving code
  blocks, tables, YAML frontmatter, and list structure. Use `--check` for
  dry-run.
- [`fix-fenced-code-language.py`](scripts/fix-fenced-code-language.py) — adds
  a default language tag (default `text`) to bare opening fenced code blocks
  to satisfy MD040. Properly undoes `markdownlint-cli2 --fix` damage that
  attaches `text` to closing fences. Use `--default <lang>` to override the
  language (default: `text`). Use `--check` for dry-run.
- [`fix-emphasis-as-heading.py`](scripts/fix-emphasis-as-heading.py) — strips
  emphasis markers (`*...*`, `_..._`) from lines that are standalone
  emphasis-as-heading paragraphs to satisfy MD036. Use `--check` for dry-run.
- [`fix-list-style.py`](scripts/fix-list-style.py) — converts asterisk
  unordered list markers (`*`) to dash style (`-`) to satisfy MD004.
  Use `--check` for dry-run.
- [`fix-heading-spacing.py`](scripts/fix-heading-spacing.py) — inserts a blank
  line before headings that lack one to satisfy MD022. Skips YAML frontmatter
  and code blocks. Use `--check` for dry-run.
- [`fix-container-fence.py`](scripts/fix-container-fence.py) — detects fenced
  code blocks whose outer fence uses 4+ backtick markers with content containing
  inner ``` fences (markdown-syntax examples). Adds a `text` language tag to
  the opening fence to satisfy MD040 without breaking the inner fences. Use
  `--check` for dry-run.

### 2.1 Execution Order

When running multiple fix scripts, the following order is **REQUIRED** to avoid
re-introducing lint errors:

1. `fix-table-separators.py`
2. `fix-fenced-code-language.py` (MUST run BEFORE `wrap-long-lines.py` — fence
   lines may exceed the width limit and wrapping a fence line before its
   language tag has been added produces a broken fence)
3. `fix-container-fence.py`
4. `wrap-long-lines.py`
5. `fix-emphasis-as-heading.py`
6. `fix-list-style.py`
7. `fix-heading-spacing.py`

> **Indent drift after editing / lint-fix.** After running the §2.1 pipeline,
> verify that continuation-line indent in edited regions matches the original
> file's siblings. The fix scripts and `markdownlint-cli2 --fix` can leave
> whitespace drift on adjacent lines. Delegate detection and repair to the
> [`list-indent-consistency`](../list-indent-consistency/SKILL.md)
> base skill, then re-run the audit before staging.

### 2.2 Known `markdownlint-cli2 --fix` Caveats

**`markdownlint-cli2 --fix` corrupts bare closing fences.** When it encounters
a fenced code block without a language tag (\`\`\`), the built-in `MD040` fix
attaches a `text` language tag to **every** \`\`\` line — including the
closing fence — producing a broken construct:

```text
text
code here
text
```

**Resolution:** Do NOT use `markdownlint-cli2 --fix` for MD040. Instead, run
`fix-fenced-code-language.py` which correctly tracks open/close fence state
and strips any language tag from closing fences. If `--fix` has already been
applied, `fix-fenced-code-language.py` will repair the damage.

-

## 3. Convenience Pipeline Script

This skill ships
[`scripts/fix-markdown-pipeline.py`](scripts/fix-markdown-pipeline.py) which
wraps the entire 3-step pipeline into a single invocation:

```bash
python3 .agents/skills/general/markdown-lint-workflow/scripts/fix-markdown-pipeline.py <file.md> [<file.md> ...]
```

The script:

1. Runs `markdownlint-cli2 --fix` (Step 1)
2. Runs all companion scripts in §2.1 order (Step 2)
3. Runs final `markdownlint-cli2` audit (Step 3 verification)
4. Exits 0 if clean, non-zero with remaining-error report

This is equivalent to executing the full manual workflow but guarantees
correct script ordering and avoids the `--check` per-script overhead.

-

## 4. Cross-References

- [`markdown-generation`](../markdown-generation/SKILL.md) — consumes this
  skill for post-generation linting
- [`skill-factory`](../skill-factory/SKILL.md) §3 — Post-Drafting Checklist
  references this skill for linting; its Header Blockquote Audit (via
  `scripts/audit-normalize-skill-headers.py`) delegates library-wide header
  normalization here
- [`list-indent-consistency`](../list-indent-consistency/SKILL.md) — detect
  and repair indent drift after fix scripts
- [`markdown-generation` §1.6](../../markdown-generation/SKILL.md#16-blockquote-metadata-headers) — SSOT for the
  `> **Label:**` header-blockquote rendering convention; the 7 companion-script variants above do NOT cover header
  rendering, so blockquote-header fixes delegate to `markdown-generation`'s base primitive
- [`markdownlint-cli2`](https://github.com/DavidAnson/markdownlint-cli2) —
  the underlying lint tool

## 5. Validation Rules (markdownlint-cli2)

### 5.0 Execution Strategy

To ensure consistent and efficient validation:

1. **Direct Execution (NO NPX)**: Prefer the standalone binary (installed via `brew`
   or system package manager) over `npm` wrappers to avoid dependency overhead.
   - **Command**: `markdownlint-cli2`
   - **Forbidden**: NEVER use `npx markdownlint-cli2`. Relying on `npx` introduces
     unnecessary overhead and bypasses the globally managed system tool. You must
     use the bare executable.

2. **Auto-Fix First (MANDATORY)**: The agent MUST NOT use manual string
   replacements (e.g., `multi_replace_file_content`) to fix standard lint
   violations like list indentation (`MD007`), alignment, or line-length
   (`MD013`). The agent MUST run the auto-fix command first.
   - **Command**: `markdownlint-cli2 --fix "**/*.md"`
   - Manual fixes are strictly reserved for semantic structural errors or when
     the auto-fix explicitly fails to resolve the issue. Do NOT start manually
     wrapping lines before attempting the auto-fix.

3. **Project Root Execution (CRITICAL)**: ALWAYS run `markdownlint-cli2` from
   the project root directory where `.markdownlint.jsonc` is located. Running
   from subdirectories will use default settings (80-char line length) instead
   of the project's 120-char standard, causing false errors.
   - **Correct**: `cd /path/to/project && markdownlint-cli2 "ai-agent-rules/file.md"`
   - **Incorrect**: `cd /path/to/project/ai-agent-rules && markdownlint-cli2 "file.md"`

4. **Cross-Platform Compatibility**:
   - Ensure shell commands are compatible with **macOS, Linux, and Windows**.
   - Use forward slashes (`/`) for paths and globs, as they are universally
     supported by `markdownlint-cli2`.
   - Verify commands in the target shell environment (e.g., `bash`, `zsh`,
     `PowerShell`) if generic syntax is not erroneous.

5. **IDE Synchronization (CRITICAL)**:
   - To ensure the VS Code `markdownlint` extension (DavidAnson) respects the
     workspace's Industrial standards, the agent MUST verify that the
     `.vscode/settings.json` file explicitly references the config.
   - **Protocol**: Add `"markdownlint.configFile": ".markdownlint.jsonc"` to
     the workspace settings.
   - **Rationale**: Extensions often ignore `.jsonc` files or use default
     (80-char) rules unless explicitly pointed to the workspace configuration.
     Parity between the IDE (real-time) and CLI (CI/CD) is mandatory.

### 5.1 Common Rules & Aliases

| Rule | Alias | Description |
| :--- | :--- | :--- |
| **MD001** | `heading-increment` | Heading levels should only increment by one level at a time |
| **MD003** | `heading-style` | Consistent heading style (ATX/Setext) |
| **MD004** | `ul-style` | Unordered list style consistency |
| **MD007** | `ul-indent` | Unordered list indentation |
| **MD009** | `no-trailing-spaces` | No trailing spaces |
| **MD010** | `no-hard-tabs` | No hard tabs |
| **MD012** | `no-multiple-blanks` | No multiple consecutive blank lines |
| **MD013** | `line-length` | Line length management |
| **MD022** | `blanks-around-headings` | Headings surrounded by blank lines |
| **MD031** | `blanks-around-fences` | Spacing around code blocks |
| **MD032** | `blanks-around-lists` | Spacing around lists |
| **MD033** | `no-inline-html` | Inline HTML management |
| **MD040** | `fenced-code-language` | Fenced code blocks must have a language |
| **MD041** | `first-line-h1` | First line in a file should be a top-level heading |
| **MD047** | `single-trailing-newline` | Files must end with a single newline |
| **MD060** | `table-column-style` | Table columns must be consistently aligned |

### 5.2 Category Tags

Use these tags to enable/disable groups of rules:

- **`accessibility`**: `MD045` (alt text), `MD059` (descriptive link text)
- **`blank_lines`**: `MD012`, `MD022`, `MD031`, `MD032`, `MD047`
- **`code`**: `MD014`, `MD031`, `MD038`, `MD040`, `MD046`, `MD048`
- **`headings`**: `MD001`, `MD003`, `MD018`, `MD019`, `MD020`, `MD021`, `MD022`, `MD023`, `MD024`, `MD025`, `MD026`,
`MD036`, `MD041`, `MD043`
- **`links`**: `MD011`, `MD034`, `MD039`, `MD042`, `MD051`, `MD052`, `MD053`, `MD054`, `MD059`
- **`whitespace`**: `MD009`, `MD010`, `MD012`, `MD027`, `MD028`, `MD030`, `MD037`, `MD038`, `MD039`

See the full [Rules documentation](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md) for a complete
list of MD001-MD060.

### 5.3 Sub-Repository Configuration Strategy

For repositories nested within the parent monorepo:

- **Inheritance**: Sub-repos MUST have their own `.markdownlint.jsonc` that
  extends the parent configuration or replicates it to ensure standard
  consistency.
- **Local Ignores**: Sub-repos MUST have a corresponding `.markdownlintignore`
  generated by combining:
  1. Parent `.markdownlintignore` rules.
  2. Parent `.gitignore` rules (relevant to the sub-repo).
  3. Sub-repo root `.gitignore` rules.
  4. Nested `.gitignore` rules (e.g., in `sync/`, `samples/cra-project/`)
     incorporated via relative paths.
- **Independence**: This ensures sub-repos can be linted independently while
  maintaining adherence to global standards.
