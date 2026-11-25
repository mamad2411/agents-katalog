---
name: cmd-lint
description: Command — Run the project's linter with sensible defaults for the detected stack
---

# /lint

Auto-detects the project's linter and runs it. Optional `--fix` to apply fixes where possible.

**Trust assumption:** the project's linter is invoked exactly as configured in the project. If `package.json` has a `"lint"` script, a `Makefile` has a `lint` target, or `.devkit.toml` defines one, it will be executed. Treat unfamiliar projects with caution — read the script before running if you don't recognize the codebase.

## Detection

```bash
# Decide which command to run based on what config files exist
if [[ -f "eslint.config.js" || -f "eslint.config.mjs" || -f ".eslintrc.json" || -f ".eslintrc.js" ]]; then
  CMD="pnpm eslint ."  # or bun/npm equivalent based on which package manager files exist
elif [[ -f "biome.json" ]]; then
  CMD="pnpm biome check ."
elif [[ -f "Cargo.toml" ]]; then
  CMD="cargo clippy -- -D warnings"
elif [[ -f "ruff.toml" ]] || grep -q '\[tool\.ruff\]' pyproject.toml 2>/dev/null; then
  CMD="ruff check ."
elif [[ -f ".golangci.yml" || -f ".golangci.yaml" ]]; then
  CMD="golangci-lint run"
else
  echo "No linter config detected. Looked for: eslint, biome, cargo/clippy, ruff, golangci."
  exit 1
fi
```

| Detected                              | Command                                 |
| ------------------------------------- | --------------------------------------- |
| `eslint.config.*` / `.eslintrc.*`     | `pnpm eslint .` (or bun/npm equivalent) |
| `biome.json`                          | `pnpm biome check .`                    |
| `Cargo.toml`                          | `cargo clippy -- -D warnings`           |
| `ruff.toml` / pyproject `[tool.ruff]` | `ruff check .`                          |
| `.golangci.yml`                       | `golangci-lint run`                     |

If `--fix` was passed, append the appropriate fix flag (`--fix`, `--apply`, `--write`) per the linter.

## devkit self-lint detection

In the devkit plugin source repo, additionally run the plugin's own validators. Detection criterion: the working directory contains all four of `agents/`, `commands/`, `hooks/`, `skills/`:

```bash
if [[ -d "agents" && -d "commands" && -d "hooks" && -d "skills" ]]; then
  bash scripts/validate-skills.sh
  bash scripts/test-validator.sh
  bash scripts/test-hooks.sh
fi
```

Run these AFTER the language linter (if any). They are additive.

## Arguments

`[--fix]`
