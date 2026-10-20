---
description: "Use when starting work in a new project, detecting project stack, or adapting to an existing codebase. Covers language detection, test framework discovery, linter/formatter/build system detection, and convention matching. Trigger phrases: analyze project, detect framework, project setup, what language, what test framework, legacy project."
---

# Project Detection

Analyze any project to discover its language, test framework, linter, formatter, build system,
and conventions. Always run this before starting ATDD in a new repository.

## What to Detect

1. **Language**: Check for `package.json`, `pyproject.toml`, `*.csproj`, `go.mod`, `Cargo.toml`, `Gemfile`, `pom.xml`, `build.gradle`, `composer.json`, `mix.exs`, `pubspec.yaml`
2. **Test framework**: Check deps, config files, and existing test files for patterns
3. **Linter**: ESLint, Biome, Ruff, Flake8, Pylint, RuboCop, golangci-lint, Clippy
4. **Formatter**: Prettier, Biome, Black, Ruff, rustfmt, gofmt
5. **Type checker**: TypeScript, mypy, pyright
6. **Build system**: npm scripts, Make, dotnet, go, cargo, gradle, maven
7. **CI/CD**: GitHub Actions, GitLab CI, Jenkins, CircleCI, Azure Pipelines
8. **Conventions**: Test file naming, directory structure, import style, code style

## Adapting to Existing Projects

- Match existing test file naming patterns (`.test.ts` vs `.spec.ts` vs `test_*.py`)
- Use existing test directory structure
- Use existing linter/formatter config — don't create new ones
- Follow existing import conventions and code style
- Co-locate or separate acceptance tests based on project preference

## Greenfield Projects

- Ask the user what language/framework to use
- Set up minimal test framework config
- Create standard directory structure

Full reference: `docs/atdd/project-detection.md`
