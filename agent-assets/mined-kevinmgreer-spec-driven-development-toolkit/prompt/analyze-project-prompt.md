---
description: "Analyze a project to detect its language, test framework, linter, formatter, build system, and conventions. Use before starting ATDD in a new or existing project."
agent: agent
tools: [read, search, execute, edit, edit/createFile, edit/editFiles]
argument-hint: "Optional: path to the project root (defaults to workspace root)"
---

Analyze this project and produce a project profile.

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
    does not reveal. Check and, when present, read:

    | File / location                                       | What to extract                                                |
    | ----------------------------------------------------- | -------------------------------------------------------------- |
    | `README.md` / `README.rst` / `README.adoc`            | Setup/run/test commands, project purpose, domain vocabulary    |
    | `CONTRIBUTING.md`                                     | Commit conventions, branch naming, PR process, local dev steps |
    | `ARCHITECTURE.md` / `docs/architecture.md`            | Architecture style, module boundaries, dependency direction    |
    | `docs/adr/` or `docs/decisions/` (ADRs)               | Authoritative architectural decisions — these beat inference   |
    | `docs/` (other docs)                                  | Dev setup, deployment, domain glossary, runbooks, style guides |
    | `.github/PULL_REQUEST_TEMPLATE.md` / `ISSUE_TEMPLATE` | PR/issue hygiene expectations                                  |
    | `STYLE.md` / `STYLEGUIDE.md` / `CODING_STANDARDS.md`  | Explicit conventions that override inferred ones               |
    | `SECURITY.md`                                         | Constraints the agent must respect (e.g., PII handling)        |

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
    full. From those files only, extract:
    - Architecture style (layered, hexagonal, MVC, vertical slice, modular monolith, etc.)
    - Module layout (folder-by-feature vs folder-by-layer; tests co-located vs separated)
    - Dependency wiring (constructor DI, container, factories, plain imports)
    - Error handling (exceptions vs Result; custom error classes; boundary mapping)
    - Validation library and where it lives
    - Async/cancellation patterns
    - Logging library and conventions
    - Configuration loading
    - Naming (files, classes, functions, constants, tests)
    - Public API style (REST/GraphQL/gRPC; URL casing; error format)
    - Persistence (ORM, migrations, transactions)
    - Comment/doc style

    Record only what you actually observe — do not guess. For each item the value is either the
    pattern or "none detected."

12. **Greenfield detection**: If no project files are found (empty repo or docs only), this is a
    greenfield project. Prompt the user for their tooling preferences in a **single prompt**:

    **Required** (always ask):
    - Language/runtime (TypeScript, Python, C#/.NET, Go, Rust, Java, Ruby, etc.)
    - Test framework (e.g., Jest vs Vitest vs Mocha, xUnit vs NUnit vs MSTest, pytest vs unittest)
    - Package manager (e.g., npm vs pnpm vs yarn, pip vs poetry vs uv)

    **Optional** (ask unless the user has already specified):
    - Linter (e.g., ESLint vs Biome, Ruff vs Flake8)
    - Formatter (e.g., Prettier vs Biome, Black vs Ruff format)
    - Directory structure (`src/` + `tests/`, co-located tests, etc.)
    - CI/CD platform (GitHub Actions, GitLab CI, or none)

    If the user says "pick defaults," choose the most common tooling for the language.
    Record all choices in the project profile output.

    Do NOT set up config files or install packages yet — that happens after the spec is approved.

## Output

**Step 1 — Write the file.** Use the file-edit tools declared in this prompt's frontmatter
(`edit`, `edit/createFile`, `edit/editFiles`, or the host runtime's equivalent write/create tool)
to write the profile to **`docs/project-profile.md`**, creating `docs/` if needed and
overwriting any existing version. Do not stop at "I would write…" — actually persist the file to
disk. This is the entire point of the prompt. If your runtime does not expose any of these
tools, stop and tell the user so they can run the prompt in a mode that has write access.

**Step 2 — Verify the file landed.** Re-read `docs/project-profile.md` to confirm contents.

**Step 3 — Confirm to the user.** Print verbatim:

> ✓ Wrote `docs/project-profile.md` (Tooling: N rows, Conventions: N rows, Reference Files: N
> entries). Future prompts will read this instead of re-detecting.

Then print the profile contents to chat so the user can review.

If you cannot write the file (permissions, sandbox, etc.), **stop** and tell the user — do not
silently continue. The whole toolkit relies on this file existing.

The file must contain three required sections — `Tooling`, `Conventions`, `Reference Files` —
plus an optional `Anti-patterns to avoid in this repo` section.

```markdown
## Project Profile

_Last updated: <YYYY-MM-DD>_

### Tooling

| Category          | Detected |
| ----------------- | -------- |
| Language          | ...      |
| Package manager   | ...      |
| Test framework    | ...      |
| Test command      | `...`    |
| Test directory    | ...      |
| Test file pattern | ...      |
| Linter            | ...      |
| Lint command      | `...`    |
| Lint fix command  | `...`    |
| Formatter         | ...      |
| Format command    | `...`    |
| Format fix cmd    | `...`    |
| Type checker      | ...      |
| Type check cmd    | `...`    |
| Build command     | `...`    |
| CI platform       | ...      |
| Source dir        | ...      |
| Specs dir         | ...      |

### Quality Gates Available

- [x] Tests: `<command>`
- [x] Lint: `<command>`
- [ ] Format: not detected
- [x] Type check: `<command>`
- [x] Build: `<command>`

### Conventions

> Sampled from `<file 1>`, `<file 2>`, `<file 3>`. Update this section if new patterns emerge.

| Convention area    | Pattern in this codebase                                 |
| ------------------ | -------------------------------------------------------- |
| Architecture style | ...                                                      |
| Module layout      | ...                                                      |
| Dependency wiring  | ...                                                      |
| Error handling     | ...                                                      |
| Validation         | ...                                                      |
| Async patterns     | ...                                                      |
| Logging            | ...                                                      |
| Configuration      | ...                                                      |
| Naming             | files: ..., classes: ..., functions: ..., constants: ... |
| Public API style   | ...                                                      |
| Persistence style  | ...                                                      |
| Comment style      | ...                                                      |
| Commit conventions | ...                                                      |
| Branch naming      | ...                                                      |

### Reference Files

When implementing new code, mirror the patterns in:

- Controller/handler example: `<path>`
- Service example: `<path>`
- Repository example: `<path>`
- Test example: `<path>`

### Anti-patterns to avoid in this repo

- (List any patterns the user explicitly rejects, or leave empty if none yet)

### Sources consulted

**Documentation:**

- `<path>` — what you used it for (e.g., `README.md` — setup commands, domain vocabulary)
- (or `none detected` if the project has no docs)

**Code samples:**

- `<path>` — layer / role
- `<path>` — layer / role

**Other signals:**

- `<path>` — e.g., `.github/workflows/ci.yml` — CI gate commands
- `<path>` — e.g., `package.json` scripts

### Known inconsistencies (optional)

- (Only populate if docs and code disagree; describe the conflict and the chosen resolution)
```

For each `Conventions` row, write the actual observed pattern or **"none detected"** — never
invent a convention that isn't present in the sampled files.

Saving to `docs/project-profile.md` means subsequent prompts (`/write-acceptance-tests`,
`/implement-from-spec`, `/run-quality-gates`, `/verify-spec-coverage`) can read it directly.
The `/implement-from-spec` prompt is required to re-read this file before writing any
production code.

Reference: `docs/atdd/project-detection.md`
