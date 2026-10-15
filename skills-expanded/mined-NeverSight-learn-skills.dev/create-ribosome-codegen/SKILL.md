---
name: create-ribosome-codegen
description: Creates a code generator for a specific prupose that supports input data using ribosome framework
---

# Create Code Generator Skill

## Purpose

Use this skill when the user asks you to create a code generator, template generator, source generator, scaffolding tool, or other program that produces source code or structured text.

The goal is to create a **working code generator**, not merely to generate the requested target code directly.

Ribosome is the primary code-generation technology used by this skill.

A typical result is a Ribosome `.dna` file that:

1. Accepts structured or configurable input.
2. Uses JavaScript, TypeScript, or Ruby as the control language.
3. Applies generation logic.
4. Produces source code, configuration, documentation, or other text as output.

The generated artifact is the output of the generator.

The generator itself is the primary deliverable.

---

# Core Objective

When the user asks for a code generator, think in terms of:

    User input
        ↓
    Generator logic
        ↓
    Ribosome DNA
        ↓
    Generated source code

Do not simply produce the final source code the generator is supposed to create.

Instead, create the program that can repeatedly generate that source code from input data.

For example, if the user asks:

"Create a generator that produces TypeScript API clients from an API definition."

The goal is not to return one TypeScript API client.

The goal is to create a Ribosome generator that:

- Accepts an API definition.
- Parses or consumes the definition.
- Determines the required models, methods, and types.
- Generates the TypeScript API client.
- Can be executed again with different API definitions.

---

# Generator-First Thinking

Always identify the following before implementing a generator:

1. What is being generated?
2. What input drives generation?
3. What parts of the output are dynamic?
4. What parts of the output are static?
5. What rules transform input into output?
6. What control language should the generator use?
7. What target language should be generated?
8. How should the generator be executed?
9. Where should generated output go?
10. How should the generator be tested?

The generator should be designed around these answers.

---

# Ribosome Mental Model

A Ribosome `.dna` file contains two overlapping programs.

## Control program

The control program performs the actual generation logic.

It contains:

- Variables
- Functions
- Loops
- Conditionals
- Data structures
- Parsing
- Input processing
- Transformations
- Naming logic
- Validation
- File handling

The control program uses JavaScript, TypeScript, or Ruby.

## Generated output

The generated output is represented by dot-prefixed lines.

For example:

    var name = "User";

    .export interface @{name} {
    .}

The generator's control code executes first.

The dot-prefixed lines become generated output.

---

# Primary Design Principle

Separate:

- Generator logic
- Generator input
- Generated output

Do not mix all three together unnecessarily.

A good generator should make it easy to understand:

- Where input comes from.
- How input is transformed.
- Which functions generate each output section.
- Where output is written.

---

# Choosing the Control Language

The supported control languages for this skill are:

- JavaScript
- TypeScript
- Ruby

Choose the control language based on the user's project and requirements.

## Default

If the user does not specify a control language and there is no surrounding project context, prefer JavaScript.

## Existing project

If the user's project is primarily Ruby, prefer Ruby.

If the project is TypeScript-based and provides a TypeScript execution mechanism for Ribosome, use TypeScript.

## TypeScript limitation

The supplied Ribosome documentation documents:

    ribosome.js

and:

    ribosome.rb

It does not document a dedicated:

    ribosome.ts

Do not invent a TypeScript executable.

When using TypeScript as the control language, rely on the project's documented TypeScript execution mechanism.

If no such mechanism exists, explicitly distinguish the TypeScript DNA source from the mechanism used to execute it.

---

# Choosing the Target Language

The target language is the language produced by the generator.

It is independent of the control language.

Examples:

- JavaScript generator → TypeScript
- JavaScript generator → SQL
- Ruby generator → C
- Ruby generator → JSON
- TypeScript generator → TypeScript
- JavaScript generator → YAML

Do not assume that the control language and target language are the same.

Always identify the target language before implementing generation logic.

---

# Generator Inputs

A generator should have a clear input model.

Possible inputs include:

- JSON
- YAML
- XML
- CSV
- Command-line arguments
- Configuration files
- Database schemas
- API specifications
- Source-code metadata
- Directory structures
- Environment configuration
- In-memory data

Prefer structured input.

For example:

    var models = [
        {
            name: "User",
            fields: [
                { name: "id", type: "number" },
                { name: "name", type: "string" }
            ]
        }
    ];

This is preferable to embedding the same information directly into output strings.

---

# Input Normalization

If the input format is complex, normalize it before generation.

Prefer this architecture:

    raw input
        ↓
    parsing
        ↓
    normalized model
        ↓
    generation
        ↓
    output

For example:

    const models = parseSchema(input);
    const normalizedModels = normalizeModels(models);

    generateModels(normalizedModels);

This keeps parsing concerns separate from code-generation concerns.

---

# Generator Architecture

For non-trivial generators, organize the implementation into these conceptual layers:

## 1. Input

Reads or receives source data.

## 2. Model

Converts source data into a generator-friendly representation.

## 3. Transformation

Applies naming, filtering, mapping, validation, and other rules.

## 4. Generation

Produces the target source code.

## 5. Output

Writes the generated source to stdout or files.

A useful architecture is:

    input()
      ↓
    parse()
      ↓
    normalize()
      ↓
    transform()
      ↓
    generate()
      ↓
    output()

Do not force every tiny generator to have all these layers. Use the structure appropriate to the complexity of the task.

---

# Generated Output Functions

Use helper functions to generate logical sections.

For example:

    function generateInterface(model) {
    .export interface @{model.name} {
    .    @{generateFields(model.fields)}
    .}
    }

For larger generators, prefer functions such as:

- `generateHeader`
- `generateImports`
- `generateTypes`
- `generateModels`
- `generateServices`
- `generateRoutes`
- `generateTests`

The names should describe the generated artifact.

---

# Keep Generation Logic Separate From Output

Avoid giant output blocks containing complicated business logic.

Prefer:

    function generateModel(model) {
        ...
    }

over:

    .very large generated block containing many conditionals and transformations

The control program should determine what is generated.

The dot-prefixed sections should primarily describe the resulting output structure.

---

# Basic Ribosome Output

Any line beginning with `.` is emitted to the generated output.

Example:

    for (var i = 0; i < 2; i++) {
    .Generated line
    }

Output:

    Generated line
    Generated line

The absence of `.` means the line is control-language code.

---

# Interpolation

Use:

    @{expression}

to insert a computed value into generated output.

Example:

    var name = "User";

    .interface @{name} {
    .}

Output:

    interface User {
    }

Use expressions for:

- Names
- Types
- Values
- Computed strings
- Generated blocks
- Function results

---

# Generated Blocks

A helper function can itself produce Ribosome output.

Example:

    function generateField(field) {
    .    @{field.name}: @{field.type};
    }

Then:

    fields.forEach(function(field) {
    .    @{generateField(field)}
    });

This is useful for reusable generated structures.

---

# Preserve Whitespace With `&{}`

Normal `@{}` interpolation trims whitespace around an embedded block.

Use:

    &{expression}

when whitespace must be preserved.

Use this primarily when generating:

- Preformatted content.
- External content.
- Whitespace-sensitive output.
- Multiline blocks where exact spacing matters.

Do not use `&{}` unless necessary.

---

# Nested Expressions

When the generator itself needs to generate another Ribosome DNA file, nested expressions can be used.

Ribosome supports:

    @1{...}
    @2{...}
    @3{...}
    ...
    @9{...}

Nested expressions are progressively reduced during compilation.

Use nested expressions when generating DNA that contains Ribosome expressions.

Do not manually construct multiple levels of escaping if nested expressions make the generator clearer.

---

# Escape Sequences

Ribosome provides:

    @{at}       → @
    @{amp}      → &
    @{slash}    → /

Use these when generated output contains literal Ribosome operators.

For example:

    .Literal @{at}{value}

can generate:

    Literal @{value}

This is particularly important when the target output is itself a Ribosome DNA file.

---

# Line Concatenation

By default, each dot-style line generates a separate output line.

Use `/+` to continue the current output line.

Example:

    .function foo( $
    ./+@{argument}
    ./+);

Use `/+` when the target language requires a single output line.

Typical uses include:

- Argument lists
- Imports
- Arrays
- Function parameters
- SQL lists
- Inline expressions

Do not use `/+` merely to reduce the number of lines in the DNA source.

---

# Separators

Use:

    ./!separate(", ")

before a loop when generated values require separators.

Example:

    .const values = [
    ./!separate(", ")
    values.forEach(function(value) {
    .    /+@{value}
    })
    ./+!
    .];

This avoids trailing separators.

Prefer `/!separate()` over manually checking whether an item is first or last.

Use it for:

- Arguments
- Imports
- Lists
- Object properties
- Enum values
- SQL columns
- Array elements

---

# Output Destinations

By default, Ribosome writes generated output to stdout.

Use:

    ./!output("generated.ts")

to redirect output to a file.

Use:

    ./!stdout()

to return output to stdout.

Use:

    ./!append("generated.ts")

to append output to an existing file.

Choose stdout by default unless the generator's purpose requires direct file creation.

---

# Multiple Generated Files

If the generator must create multiple files, design the output model explicitly.

For example:

    generateModelFiles(models)
    generateServiceFiles(services)
    generateTestFiles(tests)

Use `/!output()` when direct file generation is appropriate.

Do not create files implicitly unless that behavior is part of the generator's requirements.

---

# Including Generator Components

Use:

    ./!include("templates/models.dna")

to include another DNA file.

Use includes when a generator becomes large enough to benefit from decomposition.

Example:

    generator.js.dna
    templates/
        header.dna
        models.dna
        services.dna
        tests.dna

Then:

    ./!include("templates/header.dna")
    ./!include("templates/models.dna")
    ./!include("templates/services.dna")
    ./!include("templates/tests.dna")

Keep related generation logic together.

---

# Advanced Layout

Ribosome treats embedded multiline output as rectangular blocks.

This allows generated blocks to be inserted into surrounding output while maintaining alignment.

Prefer Ribosome's layout behavior rather than manually calculating indentation for every generated line.

This is especially useful for:

- Nested classes
- Interfaces
- Functions
- Configuration blocks
- Documentation
- SQL
- Generated declarations

---

# Alignment Operator

The `/=` operator aligns a line with the previous line.

Example:

    .        Generated block
    ./=Additional line

Use `/=` sparingly.

It is primarily useful when incorporating externally generated content whose indentation is unknown.

Do not use `/=` as a general formatting mechanism.

---

# Generated Tabs

Ribosome does not allow tabs in the input DNA source.

Use:

    ./!tabsize(4)

to convert appropriate leading spaces in generated output into tabs.

Use:

    ./!tabsize(0)

to disable generated tabs.

Follow the target project's formatting rules.

If the target project uses spaces, leave tab generation disabled.

---

# Naming and Transformation

A generator commonly needs to transform names.

For example:

    UserProfile
    user_profile
    user-profile

should not be manipulated repeatedly inside output expressions.

Instead, centralize naming transformations.

Example:

    function typeName(name) {
        ...
    }

    function propertyName(name) {
        ...
    }

    function fileName(name) {
        ...
    }

Then use those functions throughout generation.

This keeps naming conventions consistent.

---

# Validation of Input

A generator should validate required input before producing output.

Validate things such as:

- Required names.
- Required fields.
- Supported types.
- Duplicate names.
- Invalid identifiers.
- Missing relationships.
- Unsupported configuration.
- Conflicting options.

Fail early when the generator cannot produce valid output.

Do not silently generate broken source code.

---

# Validation of Generated Output

Generated code should be treated as a separate artifact that requires validation.

Whenever possible:

1. Generate the output.
2. Parse or compile it.
3. Run formatting or linting.
4. Run relevant tests.

For example:

    generator
        ↓
    generated TypeScript
        ↓
    TypeScript compiler
        ↓
    tests

A generator is not complete merely because the DNA file itself parses.

---

# Empty Collections

Always account for empty input collections.

For example:

    fields = []

should not result in malformed output such as:

    interface User {
        ,
    }

Use `/!separate()` for lists and conditional generation for optional sections.

---

# Optional Sections

Generate optional sections using control-language conditionals.

Example:

    if (model.generateTests) {
    .describe("@{model.name}", () => {
    .});
    }

Avoid emitting empty blocks unless the target language requires them.

---

# Determinism

Prefer deterministic output.

Given the same input, the generator should normally produce the same files.

Avoid unnecessary:

- Random values
- Current timestamps
- Environment-dependent ordering
- Unstable iteration
- Hidden global state

Deterministic generators are easier to:

- Test
- Review
- Cache
- Version-control
- Debug

---

# Generated Formatting

The generated code should follow the target project's conventions.

Consider:

- Indentation
- Quotes
- Semicolons
- Naming
- Imports
- Line endings
- Braces
- Blank lines
- Ordering

Do not let the formatting of the control program accidentally dictate target-code formatting.

The target output should be intentionally formatted.

---

# Generated Imports

When generating imports, use structured data and separators.

For example:

    var imports = [
        "import { User } from './User';",
        "import { Post } from './Post';"
    ];

    imports.forEach(function(line) {
    .@{line}
    });

For more complex imports, store structured information rather than already-rendered strings.

For example:

    {
        module: "./User",
        names: ["User", "UserInput"]
    }

Then generate the appropriate syntax.

---

# Generator Configuration

If the generator has configuration options, centralize them.

For example:

    const config = {
        outputDirectory: "./generated",
        generateTests: true,
        generateIndex: true
    };

Avoid scattering configuration checks throughout the generator.

Prefer passing configuration into generation functions.

---

# CLI Arguments

Ribosome passes command-line arguments through to the underlying control program.

Use command-line arguments when the generator should support CLI configuration.

For example, conceptually:

    ribosome.js generator.js.dna schema.json

The generator can inspect its control-language arguments and load the requested input.

Do not assume a specific CLI parsing library unless the project provides one.

---

# File Output

If direct file generation is required, use Ribosome's output commands.

For example:

    ./!output("generated/User.ts")
    ...
    ./!stdout()

Use configurable paths when possible.

Avoid hard-coded absolute paths.

Be careful with paths derived from user input.

---

# Multiple DNA Files

For a complex generator, use multiple DNA files.

A reasonable structure is:

    generator.js.dna
    lib/
        input.js
        model.js
        naming.js
    templates/
        header.dna
        model.dna
        service.dna
        test.dna

Use `/!include()` for DNA composition where appropriate.

Keep the architecture understandable.

---

# Distribution

Ribosome can compile a DNA generator into an RNA script.

For example:

    ribosome.rb --rna generator.rb.dna > generator.rb

This allows distribution of the generated RNA script without requiring Ribosome itself, assuming the necessary runtime is available.

If the user asks how to distribute the generator, consider whether distributing the DNA source or compiled RNA is more appropriate.

---

# Testing Strategy

A code generator should be tested at multiple levels.

## Unit tests

Test:

- Naming functions.
- Type mappings.
- Input normalization.
- Validation.
- Small generation helpers.

## Golden/output tests

Given a known input, compare generated output against expected files.

For example:

    fixture/input.json
    expected/User.ts
    expected/Post.ts

Then regenerate and compare.

## Syntax tests

Compile or parse generated source.

## Integration tests

Run the complete generator against realistic input.

---

# Golden Tests

Golden tests are particularly useful for code generators.

A typical pattern is:

    input
      ↓
    generator
      ↓
    generated output
      ↓
    compare with expected output

When output changes intentionally, update the golden fixtures.

When output changes unexpectedly, the diff provides a clear indication of the regression.

---

# Generator Error Messages

Errors should identify the problem in terms of the user's generator input.

Prefer:

    Model "User" contains duplicate field "id".

over:

    undefined is not a function

When possible, include:

- Input name.
- Location.
- Problem.
- Expected value.
- Actual value.

Good error messages make generators much easier to operate.

---

# Security

If the generator consumes untrusted input:

- Validate file paths.
- Avoid unsafe command execution.
- Avoid arbitrary evaluation of input.
- Sanitize generated identifiers.
- Prevent path traversal.
- Avoid writing outside intended output directories.

Do not treat source-generation input as automatically trusted.

---

# Generator Performance

Most generators do not require aggressive optimization.

Prefer clear code.

For large inputs:

- Avoid repeatedly reparsing data.
- Normalize once.
- Avoid quadratic searches where simple maps are sufficient.
- Avoid generating the same block repeatedly.
- Cache expensive transformations when useful.

Correctness and maintainability are more important than premature optimization.

---

# Generator Workflow

When creating a generator, follow this workflow.

## Step 1: Understand the requested artifact

Determine exactly what the generator should produce.

Examples:

- TypeScript classes
- API clients
- Database models
- SQL migrations
- React components
- Configuration files
- Documentation
- SDKs
- Infrastructure files
- Test suites

## Step 2: Define the input model

Determine what information the generator needs.

Examples:

    {
        name,
        fields,
        methods,
        options
    }

## Step 3: Define the output structure

Determine the generated files and their contents.

For example:

    generated/
        models/
            User.ts
            Post.ts
        services/
            UserService.ts
            PostService.ts
        index.ts

## Step 4: Define transformation rules

Determine:

- Naming.
- Type mapping.
- Filtering.
- Ordering.
- Optional sections.
- Relationships.
- Imports.
- Formatting.

## Step 5: Choose the control language

Prefer JavaScript unless project context indicates TypeScript or Ruby.

## Step 6: Implement the generator model

Create normalized input structures and helper functions.

## Step 7: Implement Ribosome output

Use dot-prefixed lines and Ribosome interpolation.

## Step 8: Handle edge cases

Consider:

- Empty input.
- Missing values.
- Duplicate values.
- Optional sections.
- Special characters.
- Reserved words.
- Invalid identifiers.
- Large inputs.

## Step 9: Validate generated code

Compile, parse, lint, format, or test the output whenever possible.

## Step 10: Provide execution instructions

Explain how to run the generator using the documented Ribosome command or project-specific integration.

---

# Decision Rules

When creating a generator:

## Prefer a generator over a static template

If the user needs dynamic output based on structured input, create a real generator.

## Prefer structured data over string parsing

Represent entities as objects, hashes, arrays, or equivalent structures.

## Prefer helper functions

Use functions for reusable generation patterns.

## Prefer `/!separate()`

Do not manually manage trailing commas when Ribosome can handle the separator.

## Prefer `@{}`

Use ordinary interpolation unless whitespace preservation is required.

## Prefer Ribosome layout

Do not manually calculate indentation for multiline generated blocks unless necessary.

## Prefer stdout by default

Only redirect to files when required.

## Prefer deterministic output

Stable output makes testing and review easier.

## Validate generated code

The generated artifact is the real product of the generator.

---

# Common Mistakes

Avoid these mistakes.

## Mistake: Generating the target code directly

Incorrect goal:

    "Here is the generated TypeScript class."

Correct goal:

    "Here is a Ribosome generator that generates TypeScript classes from model definitions."

## Mistake: Hard-coding all output

If every generated value is hard-coded, the result is effectively a static file rather than a useful generator.

## Mistake: Mixing input parsing with rendering

Keep parsing and normalization separate from output generation when complexity warrants it.

## Mistake: Manual separator handling

Prefer `/!separate()`.

## Mistake: Excessive string concatenation

Prefer dot-style output and Ribosome interpolation.

## Mistake: Ignoring empty collections

Ensure generated lists remain syntactically valid when empty.

## Mistake: Ignoring target-language syntax

The DNA may be valid while its generated output is invalid.

Always validate both.

## Mistake: Inventing Ribosome features

Use only documented Ribosome commands and syntax.

## Mistake: Assuming TypeScript has `ribosome.ts`

The supplied documentation does not define such a command.

---

# Quick Ribosome Reference

## Generated line

    .Generated line

## Interpolation

    .Name: @{name}

## Preserve whitespace

    .Content: &{content}

## Nested interpolation

    ..Generated @1{value}

## Escape `@`

    @{at}

## Escape `&`

    @{amp}

## Escape `/`

    @{slash}

## Concatenate output

    .First $
    ./+second
    ./+!

## Separator

    ./!separate(", ")
    for (...) {
    .    /+@{value}
    }
    ./+!

## Write to file

    ./!output("generated.txt")

## Restore stdout

    ./!stdout()

## Append

    ./!append("generated.txt")

## Include DNA

    ./!include("other.dna")

## Generated tab size

    ./!tabsize(4)

## Disable generated tabs

    ./!tabsize(0)

## Align with previous line

    ./=generated line

## Compile DNA into RNA

    ribosome.rb --rna generator.rb.dna > generator.rb

---

# Example Generator Architecture

A small generator might look conceptually like this:

    input data
        ↓
    normalize input
        ↓
    generate header
        ↓
    generate imports
        ↓
    generate models
        ↓
    generate services
        ↓
    generate tests
        ↓
    write output

A larger generator may use:

    generator.js.dna
        ↓
    input/
        ↓
    model/
        ↓
    transforms/
        ↓
    templates/
        ↓
    output/

The exact architecture should match the complexity of the generator.

---

# Final Checklist

Before delivering a code generator, verify:

- [ ] The deliverable is actually a generator, not merely generated code.
- [ ] The generator has a clear input model.
- [ ] The target language is identified.
- [ ] The control language is identified.
- [ ] Dynamic values are represented as structured data.
- [ ] Repeated generation logic uses helper functions.
- [ ] Ribosome dot syntax is used correctly.
- [ ] `@{}` is used for interpolation.
- [ ] `&{}` is used only when whitespace preservation is needed.
- [ ] `/+` is used only for intentional line concatenation.
- [ ] `/!separate()` is used for generated separators.
- [ ] `/!include()` is used for useful DNA composition.
- [ ] Output handling is intentional.
- [ ] Empty collections are handled.
- [ ] Optional sections are handled.
- [ ] Naming transformations are centralized.
- [ ] Generated output is deterministic where practical.
- [ ] Generated source is syntactically valid.
- [ ] The generator's own control code is valid.
- [ ] No undocumented Ribosome features were invented.
- [ ] TypeScript execution is not incorrectly described as `ribosome.ts`.
- [ ] Execution instructions are provided when useful.
- [ ] The generator can be reused with different input rather than producing only one fixed result.

---

# Final Principle

The purpose of this skill is to make the agent think like a **code-generator author**.

Do not ask:

    "What code should I output?"

Ask:

    "What generator should I build so that the requested code can be produced from appropriate input?"

Ribosome is the mechanism for implementing that generator.

The final result should be a reusable, maintainable, deterministic generator that transforms structured input into valid target code.

## Runnable Generator Contract

Every generated code generator must have an explicit input contract.

The generator must document:

- Generator file path.
- Control language.
- Required input data.
- Input format.
- How input is supplied.
- Required command-line arguments.
- Expected output.
- Output destination.
- Working-directory requirements.
- Required dependencies.

The generator should preferably accept structured input through a file when the input is non-trivial.

For example:

    ribosome.js generator.js.dna input.json > generated.ts

The generator must be written so that the execution command can be determined without modifying the generator after it has been created.

When creating a generator, always provide a minimal example input and the corresponding execution command.

## Generator Contract First

When given a generator created by the Create Code Generator Skill, first look for its documented input contract.

Use that contract to determine:

1. What data to provide.
2. How to serialize the data.
3. Which arguments to pass.
4. Where the output should be written.
5. How to validate the result.

If the generator was created according to the Runnable Generator Contract, do not redesign its input interface.


## Testing

To test the code generator ribosome has to be installed:                    

 ribosome (javascript)   https://raw.githubusercontent.com/sustrik/ribosome/804e945655a92847b1eb2934ae6f78d19366181e/ribosome.js
 ribosome (ruby)         https://raw.githubusercontent.com/sustrik/ribosome/804e945655a92847b1eb2934ae6f78d19366181e/ribosome.rb
 ribosome (python)       https://raw.githubusercontent.com/sustrik/ribosome/804e945655a92847b1eb2934ae6f78d19366181e/ribosome.py
