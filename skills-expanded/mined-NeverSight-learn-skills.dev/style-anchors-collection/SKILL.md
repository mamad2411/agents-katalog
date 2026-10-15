---
name: style-anchors-collection
description: Collects and documents exemplar code patterns as style anchors between technical requirements and implementation planning. Creates a reusable library of code examples with usage guidelines that implementation-planner references in task instructions to prevent architectural drift.
---

# Style Anchors Collection

Systematically identifies, documents, and organizes code examples that demonstrate approved patterns from technical requirements. Creates a structured library of style anchors used throughout implementation.

## Prerequisites

- Completed `technical-requirements.yaml`
- Optional: Access to existing codebase or reference repositories

## Purpose

Style anchors are concrete code examples that serve as templates for implementation. They prevent drift by:
- Establishing approved patterns before coding begins
- Providing specific file:line references instead of abstract descriptions
- Documenting when and how to use each pattern
- Creating a reusable pattern library for the project

## Collection Process

### Step 0: Determine Output Directory

If no directory was provided as a parameter, prompt the user:

> "Where should I create the style anchors? (This should be the same base directory as your requirements documents)"

Wait for user response. Store the provided path as `base_directory`.

### Step 1: Load Technical Context

1. Load `{base_directory}/requirements/technical-requirements.yaml`
2. Parse for key architecture patterns:
   - Architecture pattern (monolithic, microservices, etc.)
   - Technology stack (language, frameworks, libraries)
   - Testing strategy (TDD, frameworks)
   - Data model approach (database, schema patterns)
   - API patterns (REST, GraphQL, etc.)
   - Security patterns (auth, validation)

3. Identify pattern categories to collect anchors for (typical categories):
   - **Services** - Service layer patterns with dependency injection
   - **Testing** - Test structure, mocking, TDD patterns
   - **Validation** - Input/output validation, schema validation
   - **API** - Endpoint handlers, middleware, routing
   - **Data Access** - Database queries, ORM patterns, migrations
   - **Error Handling** - Error types, error propagation, recovery

### Step 2: Present Collection Plan

Display identified categories to the user:

```
## Style Anchors Collection

Based on your technical requirements, I'll collect code examples for these pattern categories:

1. Services (Effect.Service pattern with dependency injection)
2. Testing (Effect service testing with @effect/vitest)
3. Validation (Schema.Class validation patterns)
4. Error Handling (Tagged errors with Effect)

For each category, I'll ask you to provide:
- File path to exemplar code
- Line range (e.g., 10-50)
- What the pattern demonstrates
- When to use it

You can provide examples from:
- Your current codebase
- A reference repository (will link to it)
- Suggest "none" to skip a category
```

Ask: "Ready to begin collection?"

Wait for confirmation.

### Step 3: Interactive Collection

For each category identified:

**3.1. Ask for source file:**

```
## Category: [Category Name]

What file demonstrates your preferred [pattern description]?

Options:
1. Provide file path from current project (e.g., src/services/UserService.ts)
2. Provide URL to reference repository file
3. Type "none" to skip this category
4. Type "help" for guidance on what makes a good style anchor

Your answer:
```

**3.2. Ask for line range:**

```
What line range should I reference?

Format: Start-End (e.g., 10-50)
Or: Single line number (e.g., 25)
Or: "all" for entire file

Your answer:
```

**3.3. If file is accessible, read and display:**

```
## Code Preview

[Display the code from specified lines]

Does this look correct? (yes/no/adjust)
```

If "adjust", loop back to line range question.

**3.4. Ask what pattern demonstrates:**

```
What does this code example demonstrate?

Examples:
- "Service pattern with Effect.Service and dependency injection"
- "TDD test structure using it.effect from @effect/vitest"
- "Schema validation with proper error handling"

Your answer:
```

**3.5. Ask when to use:**

```
When should developers use this pattern?

Examples:
- "When creating any service class in the service layer"
- "When testing Effect-based services"
- "When validating external input data"

Your answer:
```

**3.6. Generate anchor ID:**

Create anchor ID from pattern name (kebab-case, e.g., `service-pattern`, `test-effect-services`)

**3.7. Confirm and continue:**

```
✓ Collected anchor: [anchor-name]

Continue to next category? (yes/no/review)
```

### Step 4: Generate Outputs

**4.1. Create directory structure:**

```bash
mkdir -p {base_directory}/artifacts/style-anchors
```

**4.2. Generate index.yaml:**

Create `{base_directory}/artifacts/style-anchors/index.yaml` with:
- Version and metadata
- Categories with collected anchors
- Anchor definitions with source references
- Usage matrix mapping patterns to task types
- Total count and collection date

**4.3. Generate individual .md files:**

For each collected anchor, create `{base_directory}/artifacts/style-anchors/[anchor-id].md` with:
- YAML frontmatter (id, name, category, tags, created date)
- Overview section
- Source reference
- Code example (from file if accessible)
- What it demonstrates
- When to use
- Pattern requirements (derived from best practices)
- Common mistakes to avoid (derived from best practices)
- Related anchors (cross-references)

**4.4. Populate pattern requirements and mistakes:**

Use knowledge from implementation-plan-best-practices to add:
- ✓ Pattern Requirements: 3-7 must-do items specific to the pattern
- ❌ Common Mistakes: 3-7 anti-patterns to avoid

### Step 5: Summary

Display collection summary:

```
## Style Anchors Collection Complete ✓

**Directory:** {base_directory}/artifacts/style-anchors/

**Collected Anchors:** [count]

📁 Categories:
  - Services: [n] anchors
  - Testing: [n] anchors
  - Validation: [n] anchors
  - Error Handling: [n] anchors

📄 Generated Files:
  ✓ index.yaml (master index with usage matrix)
  ✓ [anchor-1].md
  ✓ [anchor-2].md
  ✓ [anchor-3].md

These anchors will be automatically referenced by implementation-planner
when generating task instructions.

Next Step: Run /implementation-planner to generate milestones and tasks
```

## Output Formats

### index.yaml Structure

The master index file includes: `version`, `project`, `generated`, `technical_requirements_ref`, `categories` (each with id, name, description, anchors list), `anchors` (each with id, name, file, category, source reference, applies_to rules, tags), `usage_matrix` (mapping architecture patterns and task types to recommended anchors), and `meta` (counts and dates).

### Individual Anchor .md Structure

Each anchor file includes: YAML frontmatter (id, name, category, tags, created), and sections for Overview, Source Reference, Code Example, What This Demonstrates, When to Use, Pattern Requirements, Common Mistakes to Avoid, Related Anchors, and Test Coverage.

See **[references/output-spec.md](references/output-spec.md)** for the complete specification of both index.yaml and individual anchor files, including all fields, formatting rules, and usage matrix structure.

See **[references/example.md](references/example.md)** for a full example anchor document.

## Pattern Requirements and Mistakes Generation

### For Service Patterns:
**Requirements:**
- ✓ All service methods MUST return Effect types
- ✓ Use Effect.gen for async operations
- ✓ Fail with tagged errors, not throw
- ✓ Validate inputs with Schema.decode before processing
- ✓ Declare all dependencies in dependencies array

**Mistakes:**
- ❌ Using async/await instead of Effect.gen
- ❌ Throwing errors instead of Effect.fail
- ❌ Direct database access without dependency injection
- ❌ Skipping input validation
- ❌ Using any or type assertions on external data

### For Test Patterns:
**Requirements:**
- ✓ Use it.effect from @effect/vitest for Effect tests
- ✓ Provide all service dependencies in test setup
- ✓ Test both success and failure cases
- ✓ Use descriptive test names that explain behavior
- ✓ Follow TDD: write test first, then implementation

**Mistakes:**
- ❌ Using regular it() for Effect-based code
- ❌ Not providing required service dependencies
- ❌ Testing only happy path, ignoring errors
- ❌ Vague test names like "test 1" or "it works"
- ❌ Modifying tests to pass broken implementation

### For Validation Patterns:
**Requirements:**
- ✓ Use Schema.Class for all data validation
- ✓ Validate at system boundaries (user input, external APIs)
- ✓ Return validation errors, don't throw
- ✓ Include helpful error messages
- ✓ Never use type assertions on external data

**Mistakes:**
- ❌ Using type assertions instead of validation
- ❌ Throwing generic errors instead of validation errors
- ❌ Validating internal function arguments (trust internal code)
- ❌ Skipping validation on external input
- ❌ Using any type for external data

### For Error Handling Patterns:
**Requirements:**
- ✓ Use tagged errors (Effect.fail with custom error class)
- ✓ Include context in error objects (IDs, values)
- ✓ Propagate errors with Effect, don't catch and hide
- ✓ Define error types near where they're used
- ✓ Document expected errors in function signatures

**Mistakes:**
- ❌ Throwing errors instead of Effect.fail
- ❌ Using string error messages instead of typed errors
- ❌ Catching errors and ignoring them
- ❌ Generic error messages without context
- ❌ Not documenting what errors a function can produce

## Usage Matrix Generation

Map technical requirements to anchor recommendations:

**From architecture.pattern:**
- `effect-based-services` → service-pattern, test-pattern, error-handling
- `schema-validation` → validation-schema, api-validation
- `rest-api` → api-pattern, validation-schema, error-handling

**By task type:**
- `code` → primary pattern for layer + validation + error-handling
- `test` → test-pattern + pattern being tested
- `api` → api-pattern + validation-schema + error-handling
- `docs` → (no anchors typically needed)
- `config` → (no anchors typically needed)

## Best Practices

### What Makes a Good Style Anchor

1. **Concrete** - Real file paths, not abstract descriptions
2. **Specific** - Line numbers for precision (20-50 lines ideal)
3. **Complete** - Shows full pattern, not just snippet
4. **Current** - Reflects current best practices
5. **Exemplary** - Demonstrates pattern correctly

### Red Flags (When Collecting)

- Code example has TODOs or FIXMEs
- File uses deprecated patterns
- Code doesn't compile/run
- Example is too trivial (< 10 lines)
- Example is too complex (> 100 lines)
- No tests exist for the pattern

## Edge Cases

### No Existing Codebase

If user has no current codebase:

```
I notice you don't have an existing codebase. Would you like to:

1. Skip style anchor collection for now (can add later)
2. Reference external examples (Effect documentation, framework examples)
3. Create minimal example files as anchors

Which approach works best for your project?
```

### User Skips All Categories

```
No style anchors collected. This means:

⚠️  Implementation-planner will generate tasks WITHOUT concrete examples
⚠️  Risk of architectural drift increases
⚠️  Developers will need to infer patterns from requirements

Recommendation: Collect at least 1-2 anchors for critical patterns
(e.g., service pattern, test pattern)

Continue without anchors? (yes/no)
```

### File Not Accessible

If user provides file path that can't be read:

```
I can't access [file-path]. Would you like to:

1. Provide a different file path
2. Paste the code directly (I'll store it in the anchor)
3. Provide a URL to the file
4. Skip this anchor

Your choice:
```

## Integration with Implementation Planner

When implementation-planner runs:

1. **Load style anchors:**
   ```
   Read {base_directory}/artifacts/style-anchors/index.yaml
   ```

2. **For each task generated:**
   - Determine task type and file patterns
   - Query usage_matrix for recommended anchors
   - Filter anchors by applies_to rules
   - Include top 2-3 relevant anchors in task instructions

3. **Task instruction template:**
   ```yaml
   instructions: |
     ## Style Anchors
     Follow these patterns:
     - `[anchor-id]` ([file]) - [what it demonstrates]
     - `[anchor-id]` ([file]) - [what it demonstrates]

     See artifacts/style-anchors/[anchor-id].md for detailed examples.

     ## [rest of task instructions]
   ```

## Validation

After generation, validate:

- [ ] index.yaml is valid YAML
- [ ] All anchor IDs are unique
- [ ] All category references resolve
- [ ] All .md files exist for anchors in index
- [ ] All .md frontmatter matches index.yaml
- [ ] Source line ranges are valid format
- [ ] Usage matrix references valid anchors
- [ ] At least 1 anchor per category

## Usage

To collect style anchors:

```
/style-anchors-collection [base-directory]
```

If no directory is provided, auto-detect by looking for `requirements/technical-requirements.yaml` in the current directory.

If not found, prompt the user: "Where are your requirements documents located?"

Wait for the user to provide a path before proceeding. Store as `base_directory`.

The skill will:

1. Load technical requirements from `{base_directory}/requirements/technical-requirements.yaml`
2. Identify pattern categories to collect
3. Interactively collect anchors for each category
4. Generate `index.yaml` in `{base_directory}/artifacts/style-anchors/`
5. Generate individual `.md` files for each anchor
6. Display collection summary

## Examples

See **[references/example.md](references/example.md)** for a sample anchor document.
