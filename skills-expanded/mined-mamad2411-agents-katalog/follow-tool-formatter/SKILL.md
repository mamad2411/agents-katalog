---
name: follow-tool-formatter
description: Use a code formatter in the project to keep style consistent
argument-hint: "[scope]"
related:
  - follow-tool-linter
  - follow-tool-data-validation
  - follow-tool-biome
  - follow-tool-dprint
  - run-verify
  - update-references
  - run-lint
  - run-format

---

## Goal

Use a code formatter in the project to format code consistently per the style guide

## Scope

Use for projects needing a formatter supporting TypeScript, JavaScript, Rust, Python, Go, per tech stack

- Boundary: this skill helps select and wire a formatter into the repo/CI — after choosing a tool use its dedicated skill (`/follow-tool-biome`, `/follow-tool-dprint`) for detailed config; linting lives in `/follow-tool-linter`
- Latest: `prettier@3.9.9` / `dprint@0.57.4` / `@biomejs/biome@2.5.14` (verified 2026-09-26)
- References: [cli](references/cli.md) | [apis](references/apis.md) 
## Execute

### 1. Select Formatter

> Goal: pick the formatter by tech stack

1. Check the project's tech stack
2. Pick a formatter by fit:
   - TypeScript/JavaScript: biome, prettier, dprint
   - Rust: rustfmt
   - Python: ruff format, black
   - Go: gofmt
3. If the project already has a formatter → keep using it

### 2. Configure Formatter

> Goal: configure the formatter to match the style guide

1. Create the config file per formatter, e.g. `biome.json`, `.prettierrc`, `rustfmt.toml`
2. Set quote, semicolon, tab width, line width per project convention
3. Use `ignore`/`exclude` for generated files, vendored files, lock files
4. Keep the config at the root or in `.config/` per project structure
5. If `package.json` scripts exist, add a `format` script

### 3. Run Formatter

> Goal: format all code

1. Run the formatter over every relevant file
2. Review the diff for unintended changes
3. Unintended changes → adjust the config and re-format
4. Run `format:check` or the equivalent to verify in CI

### 4. Integrate With Lint And CI

> Goal: the formatter works with lint and CI

1. Keep `format` separate from `lint` (format may fix files; lint only checks)
2. Use `format --check` or `fmt --check` in CI
3. Git hooks for format (fix): repos with `.moon/workspace.yml` → add `moon run :format --affected --status=staged` to moon's `vcs.hooks`; other repos → an hk/lefthook `pre-commit` step
4. Run `/run-verify` to verify format + lint + typecheck

### 5. Editor And Onboarding

> Goal: the team uses the formatter consistently

1. Add editor integration (VS Code settings, .editorconfig)
2. Document how to format before commit
3. If using `formatOnSave` → state it in the editor config
4. Confirm CI catches unformatted code

## Rules

### 1. Format Separate From Lint

- the formatter handles style (spacing, quote, semicolon)
- the linter handles code quality (unused, errors, patterns)
- never let the linter be the primary formatter

### 2. Config In Version Control

- the config file must live in the repo
- do not commit personal/IDE-specific format settings
- use root-level config for consistency

### 3. Fast And Deterministic

- the formatter must be fast enough for pre-commit
- deterministic output (re-running yields the same result)
- do not format generated or vendored files

### 4. No Manual Formatting Battles

- never commit unformatted code
- do not switch formatters often
- changing formatter → run `/update-references` and note it in the CHANGELOG

- Use `/follow-tool-linter` if needed
- Use `/follow-tool-data-validation` if needed
- Use `/follow-tool-biome` if needed
- Use `/follow-tool-dprint` if needed
- Use `/run-verify` to verify format + lint + typecheck
- Use `/update-references` when changing formatter
- Use `/run-lint` if needed
- Use `/run-format` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Formatter selected and configured correctly
- `format` and `format:check` scripts work
- CI catches unformatted code
- Editor settings support format on save
- Code style stays consistent across the project
