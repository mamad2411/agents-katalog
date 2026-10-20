---
name: google-style-java
description: >
  Apply Google's official Java style guide when writing, reviewing, or
  formatting Java code. Use this skill whenever the user asks to review Java
  code for style, asks about Java naming conventions, import ordering,
  annotation placement, Javadoc format, brace style, or whether code follows
  Google Java standards. Also triggers on: "is this idiomatic Java?", "clean
  up this Java file", "how do I write Javadoc?", "should I use this Java
  pattern?", "what's the Google way for Java exceptions?", "how should I
  format this Java class?", or any mention of google-java-format, Checkstyle
  in a Google-style context. Note: this guide covers Java; for Kotlin use
  the Kotlin style guide; for Android Java also check Android-specific rules.
---

# Google Java Style Guide

Google's Java style guide is precise and tooling-friendly — the companion
[`google-java-format`](https://github.com/google/google-java-format) tool
enforces it automatically. Key themes: 2-space indentation (not 4), K&R brace
style, Javadoc on every public API, and strict import ordering enforced by
`goimports`-equivalent tooling.

---

## Key Rules at a Glance

### File structure (in order)
1. License or copyright notice (if present)
2. Package statement
3. Import statements
4. Exactly one top-level class

### Import ordering (§3.3)
1. Static imports — all in one block, alphabetical
2. `android.*`
3. `com.*`
4. `junit.*`
5. `net.*`
6. `org.*`
7. `java.*`
8. `javax.*`
9. Same-project imports

No wildcard imports (`import java.util.*`) ever.

### Naming conventions

| Entity | Style | Example |
|---|---|---|
| Package | `lowercase.no.underscores` | `com.example.user` |
| Class / interface / enum | `UpperCamelCase` | `UserService` |
| Method | `lowerCamelCase` | `getUserById()` |
| Non-constant field | `lowerCamelCase` | `userName` |
| Constant (`static final`) | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Local variable | `lowerCamelCase` | `userCount` |
| Type parameter | Single letter or `UpperCamelCase` + `T` | `E`, `T`, `RequestT` |
| Test method | `methodName_scenario_expectedResult` | `parse_emptyInput_throwsException` |

**Acronyms**: treat as words — `XmlParser`, `HttpUrl`, not `XMLParser` or `HTTPUrl`.

### Braces — K&R style (§4.1)
```java
// Correct: opening brace on same line, closing brace on own line
if (condition) {
  doSomething();
} else {
  doOther();
}

// Wrong: Allman / Egyptian brackets with else on new line
if (condition)
{   // Bad
  doSomething();
}
else {  // Bad
  doOther();
}
```

Always use braces — even for single-statement `if`/`for` bodies.

### Formatting
- **Indentation**: 2 spaces (not 4 — common mistake coming from other Java styles).
- **Continuation indent**: +4 spaces (double the block indent).
- **Line length**: 100 characters column limit.
- **Column alignment**: Never align field assignments vertically with extra spaces.
- **One statement per line**.
- **Blank lines**: one blank line between consecutive class members (fields, constructors, methods).

### Javadoc (§7)
```java
/**
 * Returns the user with the given identifier.
 *
 * <p>This method queries the database and caches the result. Use
 * {@link #invalidateCache()} to clear the cache if needed.
 *
 * @param id the unique user identifier, must not be null
 * @param includeDeleted whether to include soft-deleted users
 * @return the matching user, or {@code Optional.empty()} if not found
 * @throws IllegalArgumentException if {@code id} is null or empty
 */
public Optional<User> findById(String id, boolean includeDeleted) { ... }
```

- Every `public` class, method, and field gets a Javadoc comment.
- First sentence ends with `.` and is the summary.
- `@param` and `@return` omitted only when "trivially obvious" (discouraged).
- Use `{@code ...}` for inline code, `{@link ...}` for references.

### Annotations
- Class-level annotations go one per line above the class declaration.
- Method annotations same — one per line.
- `@Override` is always used when overriding or implementing.

### Other rules
- No trailing whitespace.
- Every `switch` block needs a `default:` case.
- `long` literals use `L` suffix (uppercase): `100_000L`, not `100000l`.
- Underscores in numeric literals allowed for readability: `1_000_000`.
- `this.` optional but consistent per file.

---

## Mode: Reviewing Java Code

When asked to review Java code for Google style compliance, work through:

1. **Imports** — any wildcards? Correct ordering (static first, then by package group)?
2. **Indentation** — 2 spaces? Continuation lines +4?
3. **Braces** — K&R style? Always present even for single-line bodies?
4. **Naming** — correct casing per the table? Acronyms treated as words?
5. **Javadoc** — present on all public members? Correct tags? First sentence complete?
6. **Annotations** — one per line? `@Override` present where applicable?
7. **Line length** — any lines > 100 characters?
8. **Switch** — `default:` case present?
9. **Constants** — `static final` fields named `UPPER_SNAKE_CASE`?

For each issue:
- Cite the section (e.g. "§4.1 Braces", "§5.2 Naming")
- Show the problematic code and the corrected version

---

## Mode: Writing New Java Code

When writing new Java following Google style:

1. 2-space indentation throughout; +4 for continuation lines.
2. Imports: no wildcards; static first, then alphabetical by package group.
3. K&R braces: opening on same line, always use braces.
4. Line limit: 100 columns.
5. Javadoc on every `public` class, interface, enum, method, and field.
6. `@Override` on every method that overrides or implements.
7. One annotation per line, above the declaration.
8. Naming: UpperCamelCase classes, lowerCamelCase methods/fields, UPPER_SNAKE for constants.
9. Prefer `Optional<T>` over returning `null` for optional results.
10. Use `L` (uppercase) for long literals.

---

## When to Load the Full Guide

Load `references/full_guide.md` when:
- Answering questions about a specific rule not covered above
- Doing a comprehensive file-level review
- Questions about: generic type bounds, lambda style, try-with-resources format, `@SuppressWarnings`

The full guide is moderate in size. Use `references/TOC.md` to navigate to the relevant section quickly.

**Also see**: `google-style-common` for cross-language naming and comment philosophy.
