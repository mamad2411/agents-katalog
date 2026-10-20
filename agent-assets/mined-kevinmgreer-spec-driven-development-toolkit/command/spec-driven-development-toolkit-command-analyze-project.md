---
description: Analyze the project to detect its language, test framework, linter, formatter, build system, and conventions. Writes docs/project-profile.md. Run before starting ATDD in a new or existing project.
argument-hint: "[optional path to the project root]"
---

Analyze this project and produce a project profile. Target: $ARGUMENTS (defaults to the workspace root).

Full procedure: `docs/atdd/project-detection.md` (authoritative — read it if any step below is unclear).

## Steps

1. **Language and package manager**: Search for `package.json`, `pyproject.toml`, `*.csproj`,
   `go.mod`, `Cargo.toml`, `Gemfile`, `pom.xml`, `build.gradle`, `composer.json`, `mix.exs`,
   `pubspec.yaml`, `Package.swift`. Check for lock files (`yarn.lock`, `pnpm-lock.yaml`,
   `poetry.lock`, `bun.lockb`).

2. **Test framework**: Check package dependencies, config files, and scan for existing test files
   to detect the framework AND the directory/naming conventions being used.

3. **Linter**: Check for ESLint, Biome, Ruff, Flake8, RuboCop, golangci-lint, Clippy configs.

4. **Formatter**: Check for Prettier, Black, Ruff format, rustfmt, gofmt configs.

5. **Type checker**: Check for `tsconfig.json`, mypy, pyright configs.

6. **Build system**: Check `scripts.build` in `package.json`, `Makefile`, `*.csproj`, `go.mod`,
   `Cargo.toml`, `pom.xml`, `build.gradle`.

7. **CI/CD**: Check for `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`,
   `.circleci/config.yml`, `azure-pipelines.yml`.

8. **Directory structure**: Identify `src/`, `lib/`, `test/`, `tests/`, `__tests__/`, `spec/`
   directories and any existing `specs/` directory.

9. **Git**: Check default branch, `.gitignore`, conventional commits config (`commitlint.*`,
   `.czrc`), and recent commit messages (look at the last 5–10 commits to detect prefix style).

10. **Existing project documentation** (mandatory if any docs exist). Read the project's own
    docs before drawing conclusions — they often carry intent and vocabulary the code alone
    does not reveal. Check and, when present, read: `README.md` (and variants),
    `CONTRIBUTING.md`, `ARCHITECTURE.md` / `docs/architecture.md`, `docs/adr/` or
    `docs/decisions/`, other `docs/`, `.github/PULL_REQUEST_TEMPLATE.md`, `STYLE.md` /
    `STYLEGUIDE.md` / `CODING_STANDARDS.md`, `SECURITY.md`.

    Precedence rules when docs and code disagree:
    - README commands **override** inferred commands (use the command in the README verbatim).
    - ADRs / `ARCHITECTURE.md` **override** architecture patterns guessed from samples.
    - `CONTRIBUTING.md` **overrides** commit/branch conventions guessed from git history.
    - Domain terms in README/docs **must** be used in specs and tests (not generic substitutes).
    - If docs and code genuinely conflict, record both and flag under a `Known inconsistencies`
      subsection in the profile. Do not silently pick one.

    Record every file you read under `Sources consulted` in the profile output. If no docs
    exist, record `none detected` — do not invent rationale.

11. **Code conventions** (mandatory unless greenfield). Using any hints from step 10 to
    identify canonical examples, pick **2–4 representative source files** that span layers
    (e.g., one controller/handler, one service, one repository, one test) and read them in
    full. From those files only, extract: architecture style, module layout, dependency
    wiring, error handling, validation, async/cancellation patterns, logging, configuration
    loading, naming, public API style, persistence, and comment/doc style.

    Record only what you actually observe — do not guess. For each item the value is either
    the pattern or "none detected."

12. **Greenfield detection**: If no project files are found (empty repo or docs only), prompt
    the user for their tooling preferences in a **single prompt** — required: language/runtime,
    test framework, package manager; optional: linter, formatter, directory structure, CI/CD.
    If the user says "pick defaults," choose the most common tooling for the language and
    record the choices. Do NOT set up config files or install packages yet — that happens
    after the spec is approved.

## Output

**Step 1 — Write the file.** Use the Write tool to persist the profile to
**`docs/project-profile.md`** (create `docs/` if needed; overwrite any existing version), using
the template in `docs/atdd/project-detection.md` § Detection Output Format. The file must
contain the required sections — `Tooling`, `Quality Gates Available`, `Conventions`,
`Reference Files`, `Sources consulted` — plus optional `Anti-patterns to avoid in this repo`
and `Known inconsistencies`. Do not stop at "I would write…" — actually persist the file.

**Step 2 — Verify the file landed.** Re-read `docs/project-profile.md` to confirm contents.

**Step 3 — Confirm to the user.** Print verbatim:

> ✓ Wrote `docs/project-profile.md` (Tooling: N rows, Conventions: N rows, Reference Files: N
> entries). Future prompts will read this instead of re-detecting.

Then print the profile contents so the user can review.

If you cannot write the file (permissions, sandbox, etc.), **stop** and tell the user — do not
silently continue. The whole toolkit relies on this file existing.

For each `Conventions` row, write the actual observed pattern or **"none detected"** — never
invent a convention that isn't present in the sampled files.
