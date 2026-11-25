---
name: modspec
description: Spec-driven development workflow for modspec projects. Use whenever you author specs, edit them, or implement code in a modspec project — every code change MUST flow through spec/feature update first, then red/green TDD against the feature suite. Replaces the previous modspec-fix and modspec-implement skills.
license: MIT
metadata:
  author: modspec
  version: "2.0"
---

# modspec — Spec-Driven Development Workflow

This skill defines the **complete workflow** for working in a modspec project: authoring specs, editing them, and implementing code. modspec uses markdown spec files with YAML frontmatter to define modules, their dependencies, and links to Gherkin `.feature` files. The features are the **executable contract** for the implementation.

## The contract — MUST ALWAYS

When this skill is loaded, every code change in the project follows the same flow, no exceptions:

1. **Phase 1 — Update the spec and features first.** If the requested change isn't already covered by an existing scenario, the spec or `.feature` file gets edited *before* any source code is touched.
2. **Phase 2 — Red/green TDD against the feature suite.** New or modified scenarios must fail first, then implementation makes them pass, then the full feature suite is run to check for regressions.

This is strict on purpose. Specs are an investment in **regeneration**: detailed, current specs let the same behavior be reproduced repeatedly from the spec alone. Skipping Phase 1 lets the source of truth drift; skipping Phase 2 lets the implementation diverge from the spec. Either break breaks the regeneration property.

> If the user requests a code change that isn't covered by an existing scenario — even a "small" one — **stop and update the spec/feature first**. Do not negotiate the workflow down to "just do this one quickly." The user invested in this workflow specifically to keep specs load-bearing.

## Test runner contract

modspec does not prescribe a runner — the choice (cucumber, vitest-cucumber, jest-cucumber, behave, custom, etc.) and the wiring (where step defs live, file extensions, discovery mechanism) are decided per project. What is non-negotiable is the contract the runner must uphold:

- The runner MUST treat the project's `features/` directory as its source of truth — every `.feature` file is part of the executable contract.
- A scenario with no matching step definition is **red** (pending or failing — the agent's signal to write the stub and the implementation).
- Tests that assert behavior not described in any `.feature` file are forbidden — that signal is "go to Phase 1 and add a scenario," not "skip the spec."
- `src/` code that contradicts a passing scenario is the bug, not the scenario.

When entering a project, read its `package.json` / test config to learn how the project wired its runner. Match that convention; do not impose a different one.

## Project structure

The shape below is illustrative. `spec/`, `features/`, and `src/` are conventional; the rest (test entry, step definition layout) is per-project.

```
project/
├── spec/                       # Spec markdown files (one per module)
│   ├── auth.md
│   └── persistence.md
├── features/                   # Gherkin .feature files (one subdir per spec)
│   ├── auth/
│   │   └── user-login.feature
│   └── persistence/
│       └── data-storage.feature
├── src/                        # Implementation (one module per spec)
└── test/                       # Runner-specific — see project's test config
```

---

## Phase 1 — Update the spec and features

Use this phase when the user asks to add, change, or remove behavior.

### 1.1 Understand the request
- *What* is being added/changed/removed? (spec, feature, scenario, dependency)
- *Which module* owns it? If unclear, present candidates — don't guess.

### 1.2 Find the right spec
- Named explicitly by the user → use that
- Fits an existing spec's responsibility → use the best fit (match by `description`, `group`, existing features)
- Represents a new concern not covered by any spec → create a new spec

### 1.3 Read current state before changing
Read the target spec, all its existing feature files, and any specs that depend on it. This prevents duplicate features, conflicting scenarios, and broken dependency contracts.

### 1.4 Make the changes
- **Add a feature** → new `.feature` file in `features/<spec>/`. Add the `features` field to spec frontmatter if missing.
- **Add a scenario** → append to the existing `.feature` file, matching the surrounding step phrasing and detail level.
- **New spec** → create the spec, the features dir, wire `depends_on` in both directions.
- **Modify dependencies** → update `depends_on`. If new `uses` references don't exist yet, offer to add them as scenarios.
- **Remove a feature/spec** → check downstream `uses` first. Warn the user about broken contracts before deleting.

### 1.5 Show what changed
Summarize files created/modified/deleted. Flag downstream specs that may need attention.

### Phase 1 rules
- Don't change features without asking — specs are owned by the user.
- Match existing style (step phrasing, scenario detail, naming).
- Check downstream before removing.

---

## Phase 2 — Implement red/green

Use this phase to make the (now-updated) feature scenarios pass.

### 2.1 Read the spec
- What is this module responsible for? (`description`, body)
- What does it depend on? (`depends_on` and `uses`)
- Where do its features live? (`features` field)

If implementing multiple specs, walk the dependency graph: start with specs that have no `depends_on` (roots) and work down. The features a spec `uses` from a dependency must already pass before that spec is implemented.

### 2.2 List the scenarios
Read every `.feature` file in the spec's features directory. Each `Scenario:` is a concrete behavior the implementation must satisfy. List them out — that's the implementation checklist.

### 2.3 Red — confirm scenarios fail
Run the feature suite. Every scenario for this spec must fail because the implementation doesn't exist yet. If a scenario passes before code is written, investigate — either the test setup is wrong or the feature is already implemented elsewhere.

### 2.4 Green — implement one scenario at a time
1. Pick the simplest scenario first.
2. Write the minimum code to make it pass.
3. Run the feature → confirm green.
4. Move to the next scenario.
5. Refactor only after all scenarios in a feature pass.

**Do not** add functionality that isn't described in a scenario. If something seems missing → return to Phase 1, add a scenario, then implement.

### 2.5 Verify dependency contracts
If the spec declares `uses` against a dependency, the implementation must actually consume those features. If it doesn't, either the implementation is wrong or the spec needs updating — flag it and return to Phase 1 if the user agrees.

### 2.6 Run the full feature suite
After implementing one spec, run *all* features — not just the one you worked on. Implementation of one spec must not break another's.

### Phase 2 rules
- Features are the contract. A passing suite means the implementation is correct; a failing scenario means the implementation is wrong (not the feature).
- If a feature seems wrong → stop, ask the user, return to Phase 1 if they confirm a change.
- Never silently skip or disable a scenario.
- Step definitions must be thin — they translate Gherkin to calls into `src/`. No business logic in step definitions.

---

## Reference: spec file format

Each spec is a `.md` file inside the spec directory with YAML frontmatter and an optional markdown body.

### Frontmatter fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | **Yes** | `string` | Unique identifier. How other specs reference it in `depends_on`. |
| `description` | No | `string` | Short summary. Shown in the graph info panel. |
| `group` | No | `string` | Logical grouping. Specs in the same group are visually clustered. |
| `tags` | No | `string[]` | Tags for filtering and categorization. |
| `depends_on` | No | `array` | Dependencies. Supports simple strings and objects with `uses`. |
| `features` | No | `string` | Relative path to the directory containing this spec's `.feature` files. |

A file without a `name` is silently skipped.

### Minimal spec
```markdown
---
name: bootstrap
---
```

### Full spec
```markdown
---
name: persistence
description: SQLite database layer for local storage
group: infrastructure
tags: [database, storage]
depends_on:
  - name: bootstrap
    uses: [project-scaffolding, health-endpoint]
features: features/persistence/
---

# Persistence

This spec covers the database abstraction layer.

## Decisions
- Use SQLite for local-first storage
- Migrations managed via versioned SQL files
```

The markdown body renders in the side panel when a node is clicked. Use it for design rationale, API notes, decisions, or anything useful that isn't a scenario.

### Dependency format

`depends_on` supports two forms that can be mixed:

**Simple:**
```yaml
depends_on:
  - bootstrap
  - config
```

**Rich (with feature references):**
```yaml
depends_on:
  - name: bootstrap
    uses: [project-scaffolding, health-endpoint]
  - name: persistence
    uses: [data-storage]
```

The `uses` array references `Feature:` names declared in the parent spec's `.feature` files. This creates a traceable contract between modules and shows up as a labeled edge in the graph.

### Dependency rules
- Matched **case-insensitively** against other specs' `name`.
- A reference to a non-existent name is silently ignored.
- Cycles are allowed but visualized as cycles.
- Roots (no `depends_on`) appear at the top in tree layout.

### Groups
Specs sharing a `group` value are clustered with a colored hull. Use them for domain organization (`infrastructure`, `data`, `api`, `ui`).

---

## Reference: Gherkin feature files

Feature files use standard Gherkin. They live in the directory referenced by `features:`. Feature names are the **public interface** of a spec — other specs declare which features they `uses`.

### Structure
```gherkin
@optional-tag
Feature: feature-name-in-kebab-case
  Optional description text.

  Scenario: First scenario name
    Given some precondition
    When an action is performed
    Then an expected outcome occurs
    And another assertion

  Scenario: Second scenario name
    Given a different setup
    When something else happens
    Then verify the result
```

### Rules
- One `Feature:` per file (first one is used).
- Feature names **must be kebab-case**: `Feature: data-storage`, not `Feature: Data Storage`.
- Same kebab-case applies to `uses` references.
- Steps use `Given`, `When`, `Then`, `And`, `But`.
- File extension must be `.feature`.
- Filename should match feature name: `data-storage.feature`.

### Step definitions
- Location, language, and file convention are decided per project — match what's already there.
- Steps are thin — they translate Gherkin to calls into `src/`. No business logic in steps.

---

## Reference: CLI

```bash
modspec ./spec/                       # Dev server with live reload (default)
modspec ./spec/ -y                    # Auto-create spec dir if missing
modspec ./spec/ --port 4000           # Custom port
modspec ./spec/ --output graph.html   # Static HTML export
```

| Flag | Description |
|------|-------------|
| `--output`, `-o` | Save HTML to path instead of serving |
| `--port` | Dev server port (default 3333) |
| `-y`, `--yes` | Auto-create spec dir if missing |
| `--help`, `-h` | Show help |

The dev server watches spec and feature files for changes and pushes updates to the browser in real time.
