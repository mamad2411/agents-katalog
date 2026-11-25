---
name: run-ribosome-codegen
description: Run an existing Ribosome code generator with input data and produce or validate its generated output.
---

# Run Ribosome Code Generator Skill

## Purpose

Use this skill when the user asks you to run, execute, invoke, test, or use an existing Ribosome code generator with some input data.

The goal is to:

1. Identify the Ribosome generator file.
2. Identify the control language used by the generator.
3. Prepare the required input data.
4. Pass the data to the generator using the appropriate mechanism.
5. Execute the generator.
6. Capture or locate the generated output.
7. Validate the result when appropriate.
8. Report the generated artifact or execution result clearly.

This skill is for **running an existing generator**, not creating a new generator.

To run the code generator ribosome has to be installed:

 ribosome (javascript)   https://raw.githubusercontent.com/sustrik/ribosome/804e945655a92847b1eb2934ae6f78d19366181e/ribosome.js
 ribosome (ruby)         https://raw.githubusercontent.com/sustrik/ribosome/804e945655a92847b1eb2934ae6f78d19366181e/ribosome.rb
 ribosome (python)       https://raw.githubusercontent.com/sustrik/ribosome/804e945655a92847b1eb2934ae6f78d19366181e/ribosome.py

---

# Core Mental Model

A Ribosome generator has two important parts:

    Ribosome generator
        +
    input data
        ↓
    generated output

For example:

    generator.js.dna
        +
    schema.json
        ↓
    generated TypeScript

The input data must be passed to the control program in a way that the generator expects.

Do not assume that every Ribosome generator accepts input in the same way.

First inspect the generator and determine its input contract.

---

# Supported Control Languages

Ribosome's documented control languages include:

- JavaScript
- Ruby
- Python

For this skill, generators may also use TypeScript when the project provides a TypeScript execution mechanism.

The supplied documentation explicitly documents:

    ribosome.js

for JavaScript and:

    ribosome.rb

for Ruby.

It does not document a dedicated:

    ribosome.ts

executable.

Do not invent a TypeScript execution command.

When a TypeScript generator is encountered, inspect the project for the mechanism it uses to execute TypeScript.

---

# First Step: Inspect the Generator

Before executing a Ribosome generator, inspect the generator source.

Determine:

- Control language.
- Expected arguments.
- Expected input files.
- Expected input format.
- Whether the generator reads stdin.
- Whether the generator reads files.
- Whether it writes to stdout.
- Whether it uses `/!output()`.
- Whether it uses `/!append()`.
- Whether it expects environment variables.
- Whether it requires additional files.
- Whether it uses `/!include()`.
- Whether it expects positional arguments.
- Whether arguments represent values, paths, or configuration.

Do not blindly pass data to a generator without understanding how it consumes that data.

---

# Determine the Input Contract

The most important question is:

    "How does this generator receive its data?"

Common patterns include:

1. Command-line arguments.
2. A JSON file path passed as an argument.
3. A YAML or other configuration file path.
4. Environment variables.
5. Standard input.
6. A fixed project file.
7. Multiple positional arguments.
8. A combination of arguments and files.

Inspect the control-language code to determine which pattern is being used.

---

# Command-Line Arguments

Ribosome passes command-line arguments through to the underlying control program.

For JavaScript:

    ribosome.js generator.js.dna arg1 arg2 arg3

For Ruby:

    ribosome.rb generator.rb.dna arg1 arg2 arg3

The arguments are passed unmodified to the program.

If the generator expects:

    process.argv

or equivalent JavaScript argument handling, provide the required arguments in the command.

For Ruby, inspect:

    ARGV

to determine the expected arguments.

---

# Passing a Data File

If the generator expects a path to an input file, pass the path as a command-line argument.

Example:

    ribosome.js generator.js.dna schema.json

The generator may then read:

    schema.json

using its control-language file APIs.

Do not assume that Ribosome automatically parses JSON, YAML, or other formats.

The generator itself is responsible for reading and parsing the input unless its implementation uses another mechanism.

---

# Passing Multiple Data Files

If the generator expects multiple positional arguments, pass them in the documented order.

Example:

    ribosome.js generator.js.dna models.json config.json output.json

Before running, verify what each argument means.

Do not reorder arguments based on guesswork.

---

# Passing Inline Data

If the generator expects raw values rather than a file path, pass those values directly.

Example:

    ribosome.js generator.js.dna User number

The exact arguments depend on the generator's implementation.

Do not assume that a JSON object can be passed directly as a shell argument unless the generator explicitly expects JSON text.

---

# JSON Data

When a generator expects JSON, determine whether it expects:

- A JSON file path.
- A JSON string.
- Parsed JSON from another input mechanism.

These are different.

## JSON file

Example:

    ribosome.js generator.js.dna schema.json

## JSON string

If the generator explicitly expects JSON text:

    ribosome.js generator.js.dna '{"name":"User","fields":[]}'

Be careful with shell quoting.

Prefer a file when the data is large or complex.

---

# Standard Input

Do not assume that Ribosome generators automatically consume stdin.

If the generator explicitly reads stdin, pipe data into it.

Example:

    cat schema.json | ribosome.js generator.js.dna

The exact behavior depends on the control program.

If the generator does not read stdin, piping data to it will not automatically make that data available.

---

# Output

By default, Ribosome writes generated output to stdout.

Example:

    ribosome.js generator.js.dna schema.json

The generated code can therefore be redirected using normal shell redirection:

    ribosome.js generator.js.dna schema.json > generated.ts

This is often the simplest way to run a generator that produces one output artifact.

---

# Generator-Controlled Output

A generator may use Ribosome's `/!output()` command.

For example, the DNA may contain:

    ./!output("generated.ts")

In that case, the generator itself controls the output destination.

When this is present:

- Do not assume stdout contains the generated artifact.
- Inspect the generator to determine where it writes.
- Check whether the output file was created.
- Report the generated file path.

---

# Returning to Stdout

A generator may use:

    ./!stdout()

to switch output back to stdout.

This means a single generator can write different portions of its output to different destinations.

Inspect the generator when output behavior is not obvious.

---

# Appending Output

A generator may use:

    ./!append("generated.txt")

This appends generated content to an existing file.

When executing such a generator:

- Be aware that previous output may already exist.
- Determine whether overwriting or appending is intended.
- Avoid repeatedly running the generator if doing so would create duplicate content.

If the user asks to regenerate from scratch, determine whether the target file should be removed or recreated first.

Do not delete existing files without explicit authorization when destructive behavior is involved.

---

# Included DNA Files

A generator may contain:

    ./!include("other.dna")

This means the generator depends on other DNA files.

Before execution:

- Ensure the included files exist.
- Preserve the expected relative paths.
- Run the generator from an appropriate working directory.
- Do not move the generator independently from its included files unless paths are known to remain valid.

---

# Working Directory

The working directory can matter because generators may use:

- Relative input paths.
- Relative output paths.
- `/!include()` paths.
- Relative file reads.
- Relative configuration files.

Before execution, determine the expected working directory.

If the generator references:

    templates/foo.dna

relative to its current working directory, execute it from the directory where that path resolves correctly.

Do not arbitrarily change the working directory.

---

# Input Preparation

When the user provides data in the conversation, determine how it should be supplied to the generator.

For example, if the user provides:

    {
      "name": "User",
      "fields": [
        { "name": "id", "type": "number" }
      ]
    }

and the generator expects a JSON file, create or provide the appropriate JSON input file if the execution environment supports file creation.

If the generator expects command-line arguments, translate the data into those arguments.

If the generator expects stdin, provide it through stdin.

Always follow the generator's actual input contract.

---

# Do Not Change the Generator Unnecessarily

When the task is to run an existing generator:

- Do not rewrite the generator.
- Do not change its control language.
- Do not modify its templates.
- Do not alter its output logic.
- Do not "fix" unrelated code.

If execution fails because of an actual bug in the generator, report the error and, if the user asks, help modify the generator separately.

---

# Validate Input Before Execution

Before running the generator, check that:

- Required input exists.
- Required fields exist.
- File paths exist.
- Data is valid for the expected format.
- Required arguments are present.
- Referenced files exist.
- The working directory is appropriate.

If the generator itself performs validation, allow it to produce its own errors as well.

---

# Shell Safety

When passing user-provided data through shell commands:

- Quote paths safely.
- Avoid unnecessary shell interpolation.
- Avoid constructing commands from untrusted strings when a direct process API is available.
- Be careful with characters such as spaces, quotes, `$`, `;`, `&`, and backticks.
- Prefer temporary input files for complex structured data.

Do not execute arbitrary commands embedded inside input data.

---

# Generated File Safety

When the generator writes files:

- Know which files it will modify.
- Avoid overwriting unrelated files.
- Avoid destructive cleanup unless explicitly requested.
- Check output paths before execution.
- Treat user-provided output paths carefully.

If the generator writes to an existing file, make the behavior clear.

---

# Execution Commands

## JavaScript

The documented command is:

    ribosome.js generator.js.dna

With arguments:

    ribosome.js generator.js.dna arg1 arg2

With an input file:

    ribosome.js generator.js.dna schema.json

With stdout redirected:

    ribosome.js generator.js.dna schema.json > generated.ts

---

# Ruby

The documented command is:

    ribosome.rb generator.rb.dna

With arguments:

    ribosome.rb generator.rb.dna arg1 arg2

With an input file:

    ribosome.rb generator.rb.dna schema.json

With stdout redirected:

    ribosome.rb generator.rb.dna schema.json > generated.rb

---

# TypeScript

Do not use:

    ribosome.ts

unless the user's project explicitly provides such a command.

The supplied documentation does not define it.

Instead:

1. Inspect the project for its TypeScript execution mechanism.
2. Determine how the TypeScript DNA generator is expected to be executed.
3. Use the documented project-specific command.
4. Do not invent a runtime command.

---

# RNA Execution

Ribosome can compile a DNA file into an RNA script.

For example:

    ribosome.rb --rna generator.rb.dna > generator.rb

The generated RNA program can then be executed using its underlying control-language runtime.

This can be useful when:

- Ribosome is unavailable at execution time.
- The generator is being distributed.
- The generator is compiled as part of a build process.

Do not compile to RNA unnecessarily when the goal is simply to run an existing DNA generator and Ribosome is already available.

---

# Capturing Generated Output

If the generator writes to stdout, capture it directly.

For example:

    ribosome.js generator.js.dna input.json > generated.ts

Then inspect:

    generated.ts

If the generator writes directly using `/!output()`, locate the file specified by the generator.

---

# Output Verification

After execution, verify:

1. The generator exited successfully.
2. The expected output exists.
3. The output is not empty unless empty output is expected.
4. The generated source is syntactically valid.
5. Expected sections are present.
6. No unexpected files were modified.
7. The output corresponds to the supplied input.

When practical, compile, parse, lint, or test the generated source.

---

# Generated Code Validation

The generator can succeed while still producing invalid target code.

Therefore, if possible:

    run generator
        ↓
    inspect generated files
        ↓
    compile/parse generated code
        ↓
    run tests

For example:

    ribosome.js generator.js.dna schema.json > generated.ts
    tsc --noEmit generated.ts

The exact validation command depends on the target project.

Do not invent project-specific commands if they are not available.

---

# Error Diagnosis

When execution fails, distinguish between:

## Ribosome error

Examples:

- Invalid DNA syntax.
- Unknown Ribosome directive.
- Invalid embedded expression.

## Control-language error

Examples:

- JavaScript exception.
- Ruby exception.
- TypeScript execution failure.
- Missing variable.
- Invalid function call.

## Input error

Examples:

- Missing file.
- Invalid JSON.
- Missing required property.
- Invalid command-line argument.

## Generated-code error

The generator ran successfully, but the resulting source is invalid.

Report which layer failed.

Do not describe a generated-code compilation error as a Ribosome execution error.

---

# Missing Input

If required input is missing, do not invent it.

Instead:

1. Inspect the generator to determine what is required.
2. Ask the user for the missing information if necessary.
3. If a default is explicitly defined by the generator, use it.
4. Do not silently substitute arbitrary values.

---

# Input Mapping

When the user provides structured data, map it to the generator's expected schema.

For example, if the generator expects:

    {
        "models": [...]
    }

and the user provides:

    [...]

determine whether the generator expects the array directly or whether it must be wrapped.

Do not assume compatibility merely because the data looks related.

---

# Multiple Runs

If the user asks to run the generator with multiple datasets:

    dataset1
    dataset2
    dataset3

run the generator independently for each dataset unless the generator explicitly supports batch input.

Keep outputs separate.

For example:

    output/
        dataset1/
        dataset2/
        dataset3/

Do not overwrite one generated result with another.

---

# Reproducibility

When possible, execution should be reproducible.

Use:

- Explicit input files.
- Explicit arguments.
- A known working directory.
- Stable configuration.
- Fixed output paths.

Avoid relying on hidden environment state.

---

# Execution Checklist

Before running:

- [ ] Generator file exists.
- [ ] Control language identified.
- [ ] Input contract understood.
- [ ] Required input is available.
- [ ] Required included DNA files exist.
- [ ] Working directory is correct.
- [ ] Output destination is understood.
- [ ] Existing files that may be modified are known.

During execution:

- [ ] Pass arguments in the correct order.
- [ ] Quote paths safely.
- [ ] Use the correct Ribosome executable.
- [ ] Do not invent undocumented commands.
- [ ] Capture stdout when appropriate.

After execution:

- [ ] Check exit status.
- [ ] Locate generated output.
- [ ] Verify expected files exist.
- [ ] Inspect generated output.
- [ ] Validate generated syntax when possible.
- [ ] Report errors at the correct layer.

---

# Quick Reference

## JavaScript generator

    ribosome.js generator.js.dna

## JavaScript with arguments

    ribosome.js generator.js.dna arg1 arg2

## JavaScript with input file

    ribosome.js generator.js.dna input.json

## JavaScript redirected to file

    ribosome.js generator.js.dna input.json > generated.ts

## Ruby generator

    ribosome.rb generator.rb.dna

## Ruby with arguments

    ribosome.rb generator.rb.dna arg1 arg2

## Ruby with input file

    ribosome.rb generator.rb.dna input.json

## Ruby redirected to file

    ribosome.rb generator.rb.dna input.json > generated.rb

## Compile Ruby DNA to RNA

    ribosome.rb --rna generator.rb.dna > generator.rb

## Redirect from inside DNA

    ./!output("generated.ts")

## Return to stdout

    ./!stdout()

## Append to a file

    ./!append("generated.ts")

## Include another DNA file

    ./!include("other.dna")

---

# Final Principles

When running a Ribosome code generator:

1. Run the generator, not the generated source.
2. Inspect the generator before deciding how to pass data.
3. Understand the generator's input contract.
4. Pass data using the mechanism the generator expects.
5. Do not assume Ribosome automatically parses input files.
6. Use command-line arguments when the generator expects arguments.
7. Use stdin only when the generator explicitly reads stdin.
8. Use input files when the generator expects file paths.
9. Understand whether output goes to stdout or is controlled by `/!output()`.
10. Preserve the generator's working-directory assumptions.
11. Preserve `/!include()` dependencies.
12. Do not modify the generator merely to make execution easier.
13. Do not invent undocumented Ribosome commands.
14. Do not assume a `ribosome.ts` executable exists.
15. Validate the generated artifact when practical.
16. Distinguish generator failures from generated-code failures.
17. Do not invent missing input.
18. Handle generated files carefully.
19. Prefer reproducible execution.
20. The objective is to successfully transform the supplied input into the artifact produced by the existing Ribosome generator.
