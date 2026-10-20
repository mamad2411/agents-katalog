---
name: coding-standard-writer
description: Write a coding standards document for a project using the coding styles inferred from provided file(s) or folder(s).
license: MIT
---

# Skill Name: coding-standard-writer

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

Dynamically generate a coding standards document based on the existing syntax, formatting, and conventions found in provided file(s) or folder(s).

## Core Process

1. **Ingest Targets**: Read the contents of the target `<file-path>` or `<folder-path>`.
2. **Analyze Syntax**: Parse indentation, variable naming (`camelCase`, `snake_case`), commenting styles, block nesting, and string quotation formats.
3. **Identify Majority Rules**: Tally occurrences of different styles; establish the majority as the standard.
4. **Handle Inconsistencies**: Report formatting inconsistencies and optionally fix them only when explicitly requested by the user; always verify changes using project-specific linting tools.
5. **Format Document**: Use a "minimal" or "verbose" template structure to compose the guidelines.
6. **Output Generation**: Write the result to a new file (e.g., `CONTRIBUTING.md`, `STYLE.md`) or inject it into the `README.md`.

## Core Principles

- **Empirical Inference**: Standards must be derived strictly from existing code, not assumed.
- **Template Adaptation**: Use "verbose" for comprehensive style guides and "minimal" for concise rule summaries.
- **Contextual Insertion**: When appending to `README.md`, locate the most logical insertion point (e.g., at the end or under a "Contributing" heading).

## WHEN TO USE

- When tasked with creating coding guidelines from existing code.
- To detect and fix formatting inconsistencies across multiple files.
- When generating `CONTRIBUTING.md`, `STYLE.md`, or `STYLEGUIDE.md`.

## WHEN NOT TO USE

- When the project already has an explicit, well-documented `CONTRIBUTING.md` or `.editorconfig` that should not be overwritten.
- To enforce rules that contradict the organization's global engineering standards.
- When generating general project documentation unrelated to coding style (use `docs-writer`).

## Common Pitfalls

- **Ignoring Edge Cases**: Establishing a "majority rule" based on a single small file, leading to a standard that conflicts with the rest of the massive codebase.
- **Overwriting Existing Rules**: Blindly generating a new `STYLE.md` that overrides a carefully curated, existing style guide without asking the user.
- **Opinionated Hallucinations**: Injecting Python conventions (like PEP 8) into a JavaScript project just because the LLM prefers them, rather than strictly empirical inference.

## Quick Start

1. Identify the reference file or folder.
2. Read the source contents to infer formatting patterns.
3. Generate the coding standard using a minimal or verbose markdown template.
4. Write to the designated output location.

## Diagnostics and Troubleshooting

- If file styles are extremely chaotic, prompt the user to choose a baseline reference file before generating the standard.

## Best Practices

- Fetch external style guides as supplemental reference only when explicitly requested, and do not let them override the codebase's existing majority conventions.
- If requested, generate a companion test file to enforce the newly defined standards.

## What to Avoid

- Overwriting existing documented standards without confirmation.
- Injecting subjective preferences that contradict the codebase's existing majority style.

## Coding Standards Templates

### `"m", "minimal"`

```text
    ```markdown
    ## 1. Introduction
    *   **Purpose:** Briefly explain why the coding standards are being established (e.g., to improve code quality, maintainability, and team collaboration).
    *   **Scope:** Define which languages, projects, or modules this specification applies to.

    ## 2. Naming Conventions
    *   **Variables:** `camelCase`
    *   **Functions/Methods:** `PascalCase` or `camelCase`.
    *   **Classes/Structs:** `PascalCase`.
    *   **Constants:** `UPPER_SNAKE_CASE`.

    ## 3. Formatting and Style
    *   **Indentation:** Use 4 spaces per indent (or tabs).
    *   **Line Length:** Limit lines to a maximum of 80 or 120 characters.
    *   **Braces:** Use the "K&R" style (opening brace on the same line) or the "Allman" style (opening brace on a new line).
    *   **Blank Lines:** Specify how many blank lines to use for separating logical blocks of code.

    ## 4. Commenting
    *   **Docstrings/Function Comments:** Describe the function's purpose, parameters, and return values.
    *   **Inline Comments:** Explain complex or non-obvious logic.
    *   **File Headers:** Specify what information should be included in a file header, such as author, date, and file description.

    ## 5. Error Handling
    *   **General:** How to handle and log errors.
    *   **Specifics:** Which exception types to use, and what information to include in error messages.

    ## 6. Best Practices and Anti-Patterns
    *   **General:** List common anti-patterns to avoid (e.g., global variables, magic numbers).
    *   **Language-specific:** Specific recommendations based on the project's programming language.

    ## 7. Examples
    *   Provide a small code example demonstrating the correct application of the rules.
    *   Provide a small code example of an incorrect implementation and how to fix it.

    ## 8. Contribution and Enforcement
    *   Explain how the standards are to be enforced (e.g., via code reviews).
    *   Provide a guide for contributing to the standards document itself.
    ```
```

### `"v", verbose"`

```text
    ```markdown

    # Style Guide

    This document defines the style and conventions used in this project.
    All contributions should follow these rules unless otherwise noted.

    ## 1. General Code Style

    - Favor clarity over brevity.
    - Keep functions and methods small and focused.
    - Avoid repeating logic; prefer shared helpers/utilities.
    - Remove unused variables, imports, code paths, and files.

    ## 2. Naming Conventions

    Use descriptive names. Avoid abbreviations unless well-known.

    | Item            | Convention           | Example            |
    |-----------------|----------------------|--------------------|
    | Variables       | `lower_snake_case`   | `buffer_size`      |
    | Functions       | `lower_snake_case()` | `read_file()`      |
    | Constants       | `UPPER_SNAKE_CASE`   | `MAX_RETRIES`      |
    | Types/Structs   | `PascalCase`         | `FileHeader`       |
    | File Names      | `lower_snake_case`   | `file_reader.c`    |

    ## 3. Formatting Rules

    - Indentation: **4 spaces**
    - Line length: **max 100 characters**
    - Encoding: **UTF-8**, no BOM
    - End files with a newline

    ### Braces (example in C, adjust for your language)

        ```c
        if (condition) {
            do_something();
        } else {
            do_something_else();
        }
        ```

    ### Spacing

    - One space after keywords: `if (x)`, not `if(x)`
    - One blank line between top-level functions

    ## 4. Comments & Documentation

    - Explain *why*, not *what*, unless intent is unclear.
    - Keep comments up-to-date as code changes.
    - Public functions should include a short description of purpose and parameters.

    Recommended tags:

        ```text
        TODO: follow-up work
        FIXME: known incorrect behavior
        NOTE: non-obvious design decision
        ```

    ## 5. Error Handling

    - Handle error conditions explicitly.
    - Avoid silent failures; either return errors or log them appropriately.
    - Clean up resources (files, memory, handles) before returning on failure.

    ## 6. Commit & Review Practices

    ### Commits
    - One logical change per commit.
    - Write clear commit messages:

        ```text
        Short summary (max ~50 chars)
        Optional longer explanation of context and rationale.
        ```

    ### Reviews
    - Keep pull requests reasonably small.
    - Be respectful and constructive in review discussions.
    - Address requested changes or explain if you disagree.

    ## 7. Tests

    - Write tests for new functionality.
    - Tests should be deterministic (no randomness without seeding).
    - Prefer readable test cases over complex test abstraction.

    ## 8. Changes to This Guide

    Style evolves.
    Propose improvements by opening an issue or sending a patch updating this document.
    ```
```

## References

- [C Style Guide](https://users.ece.cmu.edu/~eno/coding/CCodingStandard.html)
- [C# Style Guide](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- [C++ Style Guide](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [Go Style Guide](https://github.com/golang-standards/project-layout)
- [Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- [AngularJS App Style Guide](https://github.com/mgechev/angularjs-style-guide)
- [jQuery Style Guide](https://contribute.jquery.org/style-guide/js/)
- [JavaScript Style Guide](https://www.w3schools.com/js/js_conventions.asp)
- [JSON Style Guide](https://google.github.io/styleguide/jsoncstyleguide.xml)
- [Kotlin Style Guide](https://kotlinlang.org/docs/coding-conventions.html)
- [Markdown Style Guide](https://cirosantilli.com/markdown-style-guide/)
- [Perl Style Guide](https://perldoc.perl.org/perlstyle)
- [PHP Style Guide](https://phptherightway.com/)
- [Python Style Guide](https://peps.python.org/pep-0008/)
- [Ruby Style Guide](https://rubystyle.guide/)
- [Rust Style Guide](https://github.com/rust-lang/rust/tree/HEAD/src/doc/style-guide/src)
- [Swift Style Guide](https://www.swift.org/documentation/api-design-guidelines/)
- [TypeScript Style Guide](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)
- [Visual Basic Style Guide](https://en.wikibooks.org/wiki/Visual_Basic/Coding_Standards)
- [Shell Script Style Guide](https://google.github.io/styleguide/shellguide.html)
- [Git Usage Style Guide](https://github.com/agis/git-style-guide)
- [PowerShell Style Guide](https://github.com/PoshCode/PowerShellPracticeAndStyle)
- [CSS](https://cssguidelin.es/)
- [Sass Style Guide](https://sass-guidelin.es/)
- [HTML Style Guide](https://github.com/marcobiedermann/html-style-guide)
- [Linux kernel Style Guide](https://www.kernel.org/doc/html/latest/process/coding-style.html)
- [Node.js Style Guide](https://github.com/felixge/node-style-guide)
- [SQL Style Guide](https://www.sqlstyle.guide/)
- [Angular Style Guide](https://angular.dev/style-guide)
- [Vue Style Guide](https://vuejs.org/style-guide/rules-strongly-recommended.html)
- [Django Style Guide](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/)
- [SystemVerilog Style Guide](https://github.com/lowRISC/style-guides/blob/master/VerilogCodingStyle.md)

## Related Skills

- **docs-writer**: You MUST load this skill when writing or updating READMEs and Architectural Decision Records.
