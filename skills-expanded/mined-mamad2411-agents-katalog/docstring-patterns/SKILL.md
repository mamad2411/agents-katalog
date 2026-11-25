---
name: "docstring-patterns"
description: "Documentation comment conventions by language: the documentation spectrum, when to document, docstring quality criteria, language-specific syntax, and common docstring patterns. Use when writing JSDoc, docstrings, rustdoc, or godoc."
---

# Docstring Patterns

> Language-specific documentation comment syntax, conventions, and best practices.

## Knowledge Base

### The Documentation Comment Spectrum

| Level | What to Document | Example |
|-------|-----------------|---------|
| Module/Package | Purpose, exports, usage overview | File header comment |
| Class/Interface | Responsibility, lifecycle, usage | Class docstring |
| Function/Method | Contract (inputs, outputs, errors) | Function docstring |
| Parameter | Semantic meaning beyond the type | @param annotation |
| Return Value | What it represents, edge cases | @returns annotation |
| Inline | Why this specific implementation | `//` comment |

### When to Document vs When Not To

**Always document:**
- Public API surface (exported functions, classes, types)
- Functions with side effects
- Functions that throw/return errors
- Non-obvious algorithms or business logic
- Configuration values and their valid ranges
- Deprecated functions (with migration path)

**Usually skip documentation for:**
- Self-explanatory getters/setters
- Trivial one-line utility functions (`isEmpty`, `capitalize`)
- Test functions (the test name is the documentation)
- Private functions called from only one place (document at the call site instead)

### Docstring Quality Criteria

1. **Standalone Summary**: The first line must make sense without reading the rest.
2. **No Type Echoing**: Do not say `@param name - The name (string)` when the type signature already shows `name: string`. Say `@param name - Display name shown in the sidebar, max 255 chars`.
3. **Active Voice**: "Creates a user" not "A user is created."
4. **Present Tense**: "Returns the count" not "Will return the count."
5. **Specific over Vague**: "Retries up to 3 times with exponential backoff" not "Handles retries."

### Language-Specific Conventions

**TypeScript/JavaScript (JSDoc/TSDoc):**
- Use `/** */` for documentation (not `//` or `/* */`)
- First line: imperative mood summary ("Creates", "Returns", "Validates")
- `@param name - Description` (TSDoc uses `-` after param name)
- `@returns Description`
- `@throws {ErrorType} When condition`
- `@example` with fenced code blocks
- `@deprecated Use {@link newFunction} instead`
- `@see {@link RelatedFunction}` for cross-references
- `@since 1.2.0` for API versioning
- `@internal` to mark non-public APIs

**Python (Google style):**
- Triple-quoted string immediately after function/class definition
- First line: imperative mood summary
- Sections separated by blank lines: `Args:`, `Returns:`, `Raises:`, `Example:`
- Indent section contents by 4 spaces
- Do not repeat type annotations that are in the signature (PEP 484)
- Use `Note:` for important caveats
- Use `Todo:` for documented technical debt

**Rust (rustdoc):**
- `///` for item documentation, `//!` for module documentation
- Markdown formatting (headers, code blocks, links)
- Code examples in `# Examples` section are compiled as tests
- Use `# Errors`, `# Panics`, `# Safety` sections as applicable
- `[`backtick links`]` auto-resolve to items in scope
- Mark unsafe code with `# Safety` section explaining invariants

**Go (godoc):**
- Comment directly above the declaration, no blank line between
- Start with the function name: `// FunctionName does X`
- Paragraphs separated by blank lines
- Code examples in `Example` test functions in `_test.go` files
- No special tags or annotations; godoc is plain prose
- Deprecated functions: `// Deprecated: Use NewFunction instead.`

### Common Docstring Patterns

**Builder/Options pattern:**
```typescript
/**
 * Creates a configured HTTP client instance.
 *
 * @param options - Client configuration. All fields are optional
 *   with sensible defaults.
 * @returns A configured client ready to make requests.
 *
 * @example Basic usage
 * ```ts
 * const client = createClient({ apiKey: "sk_test_123" });
 * ```
 *
 * @example Full configuration
 * ```ts
 * const client = createClient({
 *   apiKey: "sk_test_123",
 *   baseUrl: "https://api.staging.example.com",
 *   timeout: 5000,
 *   retries: 2,
 * });
 * ```
 */
```

**Overloaded functions:**
```typescript
/**
 * Fetches a resource by ID or by query.
 *
 * @param idOrQuery - Either a string ID for direct lookup,
 *   or a query object for filtered search.
 *
 * @example By ID
 * ```ts
 * const user = await fetch("usr_123");
 * ```
 *
 * @example By query
 * ```ts
 * const users = await fetch({ role: "admin", active: true });
 * ```
 */
```

## Patterns

1. **Document at the Interface**: Focus documentation effort on public APIs and module boundaries. Internal implementation can be lighter.
2. **Examples as Tests**: Rust doctests and Python doctests serve double duty -- they document AND verify. Prefer them over untested examples.
3. **Link Aggressively**: Cross-reference related functions, types, and external docs. IDEs make links clickable.
4. **Version Your API**: Use `@since` tags so consumers know when a function was added.
5. **Deprecation With Path**: Never deprecate without providing the replacement. `@deprecated Use X instead` not just `@deprecated`.

## Anti-Patterns

1. **Narrating the obvious**: `/** Gets the name. */ getName(): string` -- the function signature says everything.
2. **Stale documentation**: Docstrings that describe old behavior. Worse than no documentation.
3. **Parameter echo**: `@param userId - The user ID` -- this adds zero information. Say what it is used for.
4. **Missing error docs**: Documenting the happy path but not the exceptions. Errors are part of the contract.
5. **Comment rot**: Updating code without updating comments. Set up linting rules to detect stale TODOs.

## References

- [TSDoc Specification](https://tsdoc.org/)
- [JSDoc Reference](https://jsdoc.app/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide - Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [Rust API Documentation Guidelines](https://rust-lang.github.io/rfcs/1574-more-api-documentation-conventions.html)
- [Effective Go - Commentary](https://go.dev/doc/effective_go#commentary)
