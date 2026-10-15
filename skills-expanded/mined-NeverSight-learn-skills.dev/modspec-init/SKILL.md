---
name: modspec-init
description: Generate modspec spec files and Gherkin features from an existing codebase. Use for brownfield adoption — analyze existing code structure and create specs that reflect the project's modules and their dependencies. Add --interactive to get some verification and chance to chat it out 
license: MIT
metadata:
  author: modspec
  version: "1.0"
---

# modspec-init — Brownfield Spec Generator

You are helping the user generate modspec specification files from an existing codebase. This is for **brownfield adoption** — the project already has code and you need to create specs that reflect its current structure.

## Goal

Analyze the existing codebase and generate:
1. **Spec files** (`.md` with YAML frontmatter) for each identifiable module
2. **Feature files** (`.feature` with Gherkin scenarios) for each module's public interface (optional)

## Process

### Step 1: Analyze the codebase

Examine the project structure to identify modules. Look for:

- **Package/directory boundaries**: Distinct directories or packages that represent separate concerns
- **Entry points**: Main files that serve as the module's public surface
- **Export patterns**: What does each module expose to others?
- **Import patterns**: What does each module consume from others?
- **Configuration boundaries**: Separate config, shared state, dependency wiring

### Step 2: Identify dependencies

For each module, determine:
- Which other modules it imports from or depends on
- Which specific functionality (features) it uses from each dependency
- Whether the dependency is direct or transitive

### Step 3: Identify features (public interface)

For each module, identify the features it provides — its public API surface:
- Capabilities it exposes to other modules or external consumers
- Endpoints or interfaces it serves
- Events or notifications it emits
- Commands or operations it handles
- Data it stores or retrieves

Name features in **kebab-case**: `user-login`, `data-storage`, `api-routing`.

### Step 4: Generate spec files

Create a spec directory (default: `spec/`) and generate one `.md` file per module:

```markdown
---
name: module-name
description: Brief description of what this module does
group: logical-group
tags: [relevant, tags]
depends_on:
  - name: other-module
    uses: [feature-a, feature-b]
features: features/module-name/
---

# Module Name

Brief description and any design notes.
```

### Step 5: Generate feature files (optional)

If the user requests features, create a `features/` directory with subdirectories per module:

```gherkin
Feature: feature-name-in-kebab-case
  Description of what this feature provides.

  Scenario: Key behavior description
    Given some precondition
    When an action occurs
    Then expected outcome
```

## Guidelines

### Technology-agnostic specs or not

**This is critical unless requested explicitly by the user.** Specs must describe modules and features at a high level of abstraction, independent of any specific programming language, framework, or technology. The spec captures **what** a module does and **why**, never **how** it does it.

- **No language-specific terms**: Don't reference classes, functions, decorators, hooks, middleware, or any language construct. Describe capabilities and responsibilities instead.
- **No framework references**: Don't mention Express, Django, React, Rails, Spring, etc. Describe the architectural role.
- **No implementation details**: Don't reference file extensions, import paths, specific libraries, ORMs, or drivers. Describe the concern being addressed.
- **Describe intent, not mechanism**: "Provides persistent data storage and retrieval" not "PostgreSQL connection pool and query interface". "Verifies caller identity" not "JWT token validation middleware".

The spec should remain valid even if the project is rewritten in a completely different language or framework.

If the user explicitly mentions to keep the tech stack as part of the spec, then make sure concepts, and modularity is reflected as part of the specs including the bootstrap 

### Module granularity

- **Right-sized**: Each spec should represent a meaningful unit that could be developed, tested, and reasoned about independently.
- **Not too granular**: Don't create a spec per file. Group related files into a single module spec.
- **Not too broad**: Don't lump unrelated concerns together. A "utils" spec is a code smell — break it into focused modules.

### Naming

- Spec names: **kebab-case**, matching the module/directory name where possible
- Feature names: **kebab-case**, describing the capability (e.g., `data-storage`, not `DatabaseClass`)
- File names: Match the spec/feature name (e.g., `data-storage.feature`, `auth.md`)

### Groups

Assign groups based on architectural layers or domains:
- `foundation` — bootstrap, configuration, shared primitives
- `infrastructure` — data persistence, caching, messaging, external integrations
- `domain` — core business logic modules
- `interface` — APIs, user-facing endpoints, external service contracts
- `presentation` — UI components, pages, layouts
- Or use domain-specific groupings that match the project

### Feature identification heuristics

Examine the code to identify capabilities, then **abstract them** into technology-neutral feature names:

| What you see in code | Feature name (tech-agnostic) |
|---------|----------------------|
| Functions that create user records | `user-creation` |
| A health-check route/endpoint | `health-reporting` |
| Code that runs queries against a data store | `data-querying` |
| Code that wraps multiple operations atomically | `transactional-operations` |
| Event emission on order completion | `order-lifecycle-events` |
| Schema migration files | `schema-evolution` |

### Dependency detection heuristics

| What you see in code | Dependency (tech-agnostic) |
|---------|----------------|
| Module imports another module's data layer | Direct: uses data-persistence module |
| Dependency injection of an auth component | Direct: uses identity module |
| Network calls to another module's endpoints | Indirect: uses interface module |
| Reading configuration from environment/files | Infrastructure: depends on configuration module |
| Shared type definitions or contracts | Structural: depends on contracts module |

### Example output

For a project with auth, data storage, API, and configuration concerns:

**spec/configuration.md:**
```markdown
---
name: configuration
description: Manages application settings and environment-specific values
group: foundation
tags: [config, environment]
depends_on: []
features: features/configuration/
---

# Configuration

Loads, validates, and provides application settings to all modules. Ensures required values are present and well-formed before the application starts.
```

**spec/data-storage.md:**
```markdown
---
name: data-storage
description: Persistent data storage and retrieval
group: infrastructure
tags: [data, persistence]
depends_on:
  - name: configuration
    uses: [settings-access]
features: features/data-storage/
---

# Data Storage

Provides a reliable interface for persisting and retrieving application data. Manages connection lifecycle and ensures data integrity.
```

**spec/auth.md:**
```markdown
---
name: auth
description: Identity verification and session management
group: domain
tags: [auth, security, identity]
depends_on:
  - name: data-storage
    uses: [data-querying, transactional-operations]
  - name: configuration
    uses: [settings-access]
features: features/auth/
---

# Auth

Verifies user identity, manages credentials, and maintains session state. Controls access to protected resources.
```

**features/data-storage/data-querying.feature:**
```gherkin
Feature: data-querying
  Retrieve stored data by various criteria.

  Scenario: Retrieve records matching a filter
    Given the data store contains records
    When a query is submitted with filter criteria
    Then only matching records are returned

  Scenario: Handle invalid queries gracefully
    Given a connected data store
    When a malformed query is submitted
    Then a descriptive error is returned without exposing internals
```

## Interactive workflow if user specified --interactive

1. Ask the user which directory to analyze (or use the current project root) - Default: ./spec and ./features in current root
2. Present the identified modules and their dependencies for review - Default: Accept
3. Ask if they want feature files generated too - Default: Yes
4. Generate the files
5. Suggest running `modspec ./spec/` to visualize the result
6. Iterate — the user may want to adjust groupings, split/merge modules, or refine features
