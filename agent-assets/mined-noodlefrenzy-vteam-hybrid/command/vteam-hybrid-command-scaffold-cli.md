<!-- agent-notes: { ctx: "CLI project scaffold workflow", deps: [CLAUDE.md], state: active, last: "sato@2026-02-12" } -->
Scaffold a CLI project: $ARGUMENTS

You are setting up this repository as a CLI tool. Follow these steps:

## 0. Template Setup

Swap the storefront README for the project placeholder, move scaffolds into place, and clean up template-only files:

```bash
# Swap README: replace storefront with project placeholder
if [ -f README-template.md ]; then
  mv README-template.md README.md
fi

# Move stub docs from scaffolds/ to docs/ root
mv docs/scaffolds/*.md docs/ 2>/dev/null
rmdir docs/scaffolds 2>/dev/null

# Remove samples directory (only useful on the template repo itself)
rm -rf samples/ 2>/dev/null

# Remove template-specific ADRs (not relevant to inheriting projects)
rm -rf docs/adrs/template/

# Remove template research/comparison docs
rm -f docs/research/how-we-compare-*.md docs/research/agent-teams-comparison.md
rm -f docs/research/squad-vs-vteam-*.md docs/research/ux-gap-analysis-*.md
rm -f docs/research/what-*-can-learn-from-*.md docs/research/what-we-learn-from-*.md
```

## 1. Gather Requirements

Ask the user to choose their tech stack. Present these options:

**Language / Framework:**
- **Python + Click** — Mature, great for rapid prototyping, huge ecosystem (Recommended for most CLI tools)
- **Python + Typer** — Modern, type-hint-driven, auto-generates help text
- **Rust + Clap** — Fast binaries, strong typing, great for distributable tools
- **Other** — Let the user specify

**Package / Build tooling (language-dependent):**
- Python: **uv** (Recommended — fast, modern) or **poetry** or **pip + setuptools**
- Rust: **cargo** (standard)

**Testing framework:**
- Python: **pytest** (Recommended) or **unittest**
- Rust: **built-in cargo test** (standard), optionally with **assert_cmd** + **predicates** for integration tests

**Additional options to ask about:**
- Do they want a CI pipeline (GitHub Actions)?
- Do they want pre-commit hooks (linting, formatting)?
- Do they want shell completions scaffolded?

## 2. Create an ADR

Once choices are made, create an ADR at `docs/adrs/` (find the next number) documenting:
- The chosen language, framework, and tooling
- Why these were selected (capture the user's reasoning)
- Trade-offs acknowledged

## 3. Scaffold the Project

Based on the choices, create the project structure. General shape:

### Python CLI
```
src/<project_name>/
    __init__.py
    cli.py          # Entry point with CLI group/command definitions
    commands/       # Subcommand modules (if applicable)
        __init__.py
tests/
    __init__.py
    test_cli.py     # Starter test for the CLI entry point
pyproject.toml      # Project metadata, dependencies, scripts entry point
```

### Rust CLI
```
src/
    main.rs         # Entry point
    cli.rs          # Clap argument definitions
    commands/       # Subcommand modules (if applicable)
        mod.rs
tests/
    cli_tests.rs    # Integration tests using assert_cmd
Cargo.toml
```

### In all cases, also:
- Update `CLAUDE.md` with the chosen tech stack, how to run tests, how to build, and any conventions
- Update `README.md` with project description, setup instructions, and usage
- Add a `.gitignore` appropriate for the language
- Create a starter test that invokes the CLI `--help` and asserts success
- If CI was requested, create `.github/workflows/ci.yml`
- If pre-commit hooks were requested, configure them (ruff/black for Python, clippy/rustfmt for Rust)
- Add agent-notes to all new files per `docs/methodology/agent-notes.md`

## 4. Verify

Run the test suite to confirm the scaffold works. Fix any issues before declaring done.

## 5. Summary

Tell the user what was created and what commands to run to get started (install deps, run tests, build, etc.).
