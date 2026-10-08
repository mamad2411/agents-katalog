# Create Library Skill

First, load the `create-skill` skill using the Skill tool before doing anything else. Follow its guidelines for writing effective skill descriptions, structuring SKILL.md, and using progressive disclosure.

Analyze a library codebase and create a comprehensive Claude skill documenting how to use it from a consumer perspective (i.e. a project that installs it as a dependency).

## Input

$ARGUMENTS — path to the library's repository on disk.

## Process

### 1. Explore the library thoroughly

Use an Explore agent to read the entire codebase. Specifically:

- **Package metadata**: composer.json, package.json, Cargo.toml, pyproject.toml, etc. — get the package name, language, and install command.
- **All source files**: read every file in src/, lib/, or equivalent source directory.
- **Public API surface**: identify all classes, functions, methods, traits, interfaces, and constants that a consumer would use.
- **Tests**: read all test files — these are the best source of real usage examples and edge cases.
- **README / docs**: read any existing documentation for context and intent.
- **Examples**: read any example files or directories.

The goal is to understand everything a consumer needs to know: how to define things, instantiate them, configure them, use their methods, handle errors, and work with common patterns.

### 2. Determine the skill name

Derive a kebab-case skill name from the package name. For example:

- `rexlabs/data-transfer-object` → `rexlabs-dto`
- `spatie/laravel-data` → `spatie-laravel-data`
- `lodash` → `lodash`

Use judgement to keep it short but recognizable.

### 3. Create the skill

Ask the user whether to create the skill.

#### Frontmatter (YAML)

- `name`: the kebab-case skill name
- `description`: max 1024 chars, third person. First sentence: what the skill provides. Then "Use when..." listing specific triggers — class names, import paths, function names, common keywords, file patterns. Be slightly "pushy" to ensure triggering. Include the full namespace/module path that would appear in imports.

#### Body (Markdown)

Write for another Claude instance. Include only what Claude wouldn't already know — procedural knowledge, library-specific patterns, non-obvious behavior.

Structure the body to cover (as applicable to the library):

1. **Overview** — one-liner on what it does, package name, install method
2. **Defining/configuring** — how to set up the library's core constructs (classes, config files, schemas, etc.)
3. **Creating instances** — constructors, factory methods, builders
4. **Core API** — the main methods/functions a consumer calls, with concise examples
5. **Configuration & options** — flags, options, settings, and what they do
6. **Type system / validation** — if the library validates, casts, or enforces types
7. **Nested / composed structures** — if things can be nested or composed
8. **Serialization / output** — toArray, toJSON, render, etc.
9. **Error handling** — what exceptions/errors are thrown and when
10. **Common patterns** — 3-5 real-world usage patterns showing idiomatic use
11. **Gotchas** — non-obvious behavior, common mistakes, important distinctions

Guidelines:

- Keep under 500 lines. If the library is very large, use reference files in a `references/` subdirectory and link from SKILL.md.
- Use concise code examples — prefer showing over explaining.
- Don't document things Claude already knows (basic PHP/JS/Python syntax, etc.).
- Don't add comments to examples unless the behavior is non-obvious.
- Use tables for reference-style info (flags, options, method signatures).
- Explain the "why" behind important distinctions rather than using MUST/NEVER.

### 4. Verify

After writing, verify:

- [ ] Description includes specific trigger keywords (namespaces, class names, method names)
- [ ] SKILL.md is under 500 lines
- [ ] Every major public API method/function is covered
- [ ] Concrete examples are included for each concept
- [ ] Common patterns section shows realistic use cases
- [ ] No time-sensitive info (version numbers that will go stale)
- [ ] No extraneous files (no README.md, CHANGELOG.md, etc.)

Present a summary to the user of what was created and what topics are covered.
