---
name: oro-behat-testing
description: >
  When writing, debugging, or optimizing Behat acceptance tests for OroCommerce,
  you MUST use this skill to consult the testing knowledge base instead of relying on memory.
  
  Trigger scenarios:
  - Writing new .feature files or Behat step definitions
  - Creating behat.yml configuration (suites, contexts, elements)
  - Defining Elements for form field mapping
  - Writing Alice YAML fixtures for test data
  - Debugging failing Behat scenarios
  - Creating custom Context classes extending OroFeatureContext
  - Understanding which built-in Oro steps are available
  - Using Scenario Outlines, Background sections, or fixture tags
  - Writing ReferenceRepositoryInitializer classes
  - Understanding test isolation behavior between features/scenarios
  
  For any Behat test structure, Oro test framework patterns, step definitions,
  fixture loading, or element configuration, read documentation first.
---

# OroCommerce Behat Testing Knowledge Base

Local knowledge base for writing and maintaining Behat acceptance tests in OroCommerce projects.
**Consult documentation first, then write tests.**

---

## Available Documents (Task -> Document Mapping)

| Task Type | Document File | Lines | Key Content |
|----------|--------------|------|-------------|
| **Quick Start** | `references/README.md` | ~80 | Overview, file structure, running tests |
| **Feature Files** | `references/feature-files.md` | ~200 | Gherkin syntax, Background, Scenario Outline, tags, fixtures |
| **behat.yml Config** | `references/behat-yml.md` | ~150 | Suite config, contexts, elements, form mapping |
| **Custom Contexts** | `references/custom-contexts.md` | ~180 | Writing step definitions, traits, base classes, service access |
| **Fixtures & Data** | `references/fixtures.md` | ~150 | Alice YAML, inline tables, ReferenceRepositoryInitializer |
| **Built-in Steps** | `references/builtin-steps.md` | ~350 | OroMainContext, FormContext, GridContext, ConsoleContext |
| **Patterns & Tips** | `references/patterns.md` | ~150 | Common patterns, anti-patterns, debugging, test isolation |
| **Additional Contexts** | `references/additional-contexts.md` | ~180 | EmailContext, ImportExportContext, ACLContext, WysiwygContext, CommerceMainContext, BrowserTabContext |
| **Advanced Features** | `references/advanced-features.md` | ~180 | Watch mode, multi-session, secrets, VariableStorage, page objects, iFrame support, CLI options |

---

## Usage Rules

### 1. Identify Task Type -> Select Document

```
Task examples -> Document mapping:

"Write a new .feature file"              -> feature-files.md + builtin-steps.md
"Define an Element in behat.yml"         -> behat-yml.md (Elements section)
"Create test fixtures"                   -> fixtures.md
"Write a custom step definition"         -> custom-contexts.md
"Find the right built-in step"           -> builtin-steps.md
"Use Scenario Outline with Examples"     -> feature-files.md (Scenario Outline section)
"Debug a failing test"                   -> patterns.md (Debugging section)
"Understand test isolation"              -> patterns.md (Isolation section)
"Create a ReferenceRepositoryInitializer"-> fixtures.md (Initializer section)
"Map form fields to an Element"          -> behat-yml.md (Elements section)
"Test email notifications"              -> additional-contexts.md (EmailContext)
"Test CSV import/export"                -> additional-contexts.md (ImportExportContext)
"Set role permissions in test"          -> additional-contexts.md (ACLContext)
"Login as buyer on storefront"          -> additional-contexts.md (CommerceMainContext)
"Fill WYSIWYG editor field"             -> additional-contexts.md (WysiwygContext)
"Test multi-user workflow"              -> advanced-features.md (Multiple Sessions)
"Mock external service in test"         -> advanced-features.md (@behat-test-env)
"Pass data between steps"              -> advanced-features.md (VariableStorage)
"Discover available references"         -> advanced-features.md (CLI Options)
```

### 2. Read Documents (By Section, Avoid Full Loading)

For documents over 200 lines, use offset + limit to read only relevant sections.

```
// CORRECT: Read specific section only
read({ filePath: ".../references/builtin-steps.md", offset: 10, limit: 80 })

// WRONG: Loading full 350 lines (wastes context)
read({ filePath: ".../references/builtin-steps.md" })
```

`README.md` (~80 lines) is the only document safe to fully load.

### 3. Cross-Reference When Needed

```
Writing a new feature file?
  1. feature-files.md    -> Structure, tags, outlines
  2. builtin-steps.md    -> Available steps to reuse
  3. fixtures.md         -> Test data setup

Debugging a failure?
  1. patterns.md         -> Common failure causes
  2. custom-contexts.md  -> Step definition details
  3. behat-yml.md        -> Configuration issues
```
