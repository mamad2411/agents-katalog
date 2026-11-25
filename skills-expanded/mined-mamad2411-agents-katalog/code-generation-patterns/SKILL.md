---
name: code-generation-patterns
version: 1.0.0
min_mindforge_version: 0.3.0
status: stable
triggers: code generation, template engine, AST manipulation, scaffolding pattern, code mod, source transform, code generator, boilerplate generation, schema-to-code, type generation, code synthesis, metaprogramming
---

# Skill — Code Generation Patterns

## When this skill activates
Any task involving automated code generation, scaffolding, code mods, template
engines, AST transformations, or schema-to-code pipelines.

## Mandatory actions when this skill is active

### Before generating code
1. Determine the generation approach based on the use case.
2. Validate that generation is worthwhile (see "When NOT to generate" below).
3. Ensure generated output is clearly marked with a header comment.

### Approaches

**Template-based (Handlebars/EJS):**
- Best for: simple, repetitive file generation with known structure.
- Use when: the output varies only in names/values, not in structure.
- Tools: Handlebars, EJS, Mustache, Liquid.
- Pattern: define template → inject variables → write output file.

**AST-based (babel/ts-morph):**
- Best for: code transforms, refactors, and modifications to existing code.
- Use when: you need to understand code structure, not just text patterns.
- Tools: babel (JavaScript), ts-morph (TypeScript), jscodeshift (codemods).
- Pattern: parse source → traverse AST → apply transforms → print modified source.

**Schema-based (OpenAPI/GraphQL/JSON Schema):**
- Best for: generating clients, types, validators from a single source of truth.
- Use when: a schema already defines the contract and code must conform.
- Tools: openapi-generator, graphql-codegen, json-schema-to-typescript.
- Pattern: schema file → generator config → output typed client/types.

### Scaffolding

**Project generators:**
- Yeoman, create-* CLIs, degit for template repos.
- Include: directory structure, config files, CI setup, README template.
- Version your generator — breaking changes need migration paths.

**File generators:**
- Plop, Hygen for generating individual files within a project.
- Pattern: define prompts → apply template → write to correct directory.
- Keep templates co-located with the generator config.

### Code mods

**jscodeshift (JavaScript/TypeScript bulk refactors):**
- Write transform as a function: `(file, api) => api.jscodeshift(file.source)...`
- Test on a single file first, then run across codebase.
- Always commit before running a codemod (easy revert).

**ts-morph (TypeScript-aware transforms):**
- Full TypeScript compiler API access.
- Can add/remove/rename imports, functions, classes, types.
- Pattern: create Project → get SourceFiles → manipulate → save.

**Systematic process:**
1. Find all instances of the pattern to transform.
2. Write the transform function.
3. Dry-run with diff output.
4. Apply and verify tests still pass.

### When NOT to generate

- If it is simpler to write by hand (fewer than 3 instances).
- If generated code needs frequent manual edits (generator is wrong).
- If the template is harder to understand than the output.
- If the schema changes so frequently that regeneration becomes a bottleneck.
- If the team cannot maintain the generator long-term.

### Quality standards for generated code

- Generated files MUST have a header: `// THIS FILE IS AUTO-GENERATED. DO NOT EDIT.`
- Generated code must pass the same lint/format rules as hand-written code.
- Generator must be idempotent (running twice produces same output).
- Include a `regenerate` script in package.json for easy re-generation.
- Test the generator itself, not just the generated output.

## Self-check before task completion
- [ ] Did I follow the mandatory actions for this skill?
- [ ] Did I apply the patterns appropriate to the context?
- [ ] Did I verify the implementation meets the criteria above?
- [ ] Did I document decisions and trade-offs made?
