---
name: google-style-common
description: >
  Cross-language Google style principles — naming, comments, formatting
  philosophy, and the "Google way" that applies across all languages.
  Use this skill when discussing general Google coding conventions that
  aren't specific to one language, when onboarding to a Google-originated
  project, or when another style guide skill refers you here for shared
  principles. Also triggers when the user asks "what does Google say about
  naming?" or "how does Google handle comments?" without specifying a language.
---

# Google Style — Common Principles

Google publishes separate style guides per language, but several core
philosophies run through all of them. This skill surfaces those cross-cutting
principles so language-specific skills can stay lean.

## Naming Philosophy

Google's naming rules are built on one idea: **names communicate intent to a
human reader, not a machine**. Prefer clarity over brevity.

| Concept | Google rule |
|---|---|
| Abbreviations | Only well-known ones (HTTP, URL). Spell out the rest. |
| Single-letter names | Only for loop counters and conventionally agreed vars (e.g. `i`, `x` in math) |
| Negated booleans | Avoid `isNotReady` — use `isReady` and invert the check |
| Acronyms in names | Treat as words: `getHtmlContent`, not `getHTMLContent` (except HTTP, URL in some guides) |
| Names to avoid | Confusing overloads of built-ins, names differing only by case |

## Comments Philosophy

- Write comments for **why**, not **what** — the code already shows what it does.
- A comment that paraphrases the code adds no value and becomes a maintenance burden when the code changes.
- Every public API (function, class, module) deserves a documentation comment; private implementation details need comments only when non-obvious.
- Use TODO comments for known issues: `TODO(username): fix this when X lands`.
- Keep comments up to date — stale, wrong comments are worse than no comments.

## Formatting Philosophy

- Consistent formatting within a project matters more than any particular style.
- Automated formatters (Black, gofmt, Prettier, clang-format) are preferred; they remove the argument entirely.
- **Line length**: 80 characters is the universal Google default. Some guides allow up to 100. Never go beyond 120.
- Indentation is always spaces, never tabs (except where the language mandates tabs, e.g. Go's gofmt).
- Trailing whitespace is never permitted.

## Error Handling Philosophy

- Never silently swallow errors.
- Propagate errors to callers rather than logging-and-continuing unless at an explicit isolation boundary.
- Use specific exception/error types; avoid catching the base `Exception` / `Error` broadly.
- Document what errors a function can raise in its docstring/JSDoc.

## Dependency & Import Philosophy

- Import only what you use.
- Organise imports in consistent blocks (stdlib → third-party → local).
- Avoid circular dependencies; they signal a structural problem.
- Prefer explicit full-path imports over implicit relative ones.

## Testing Philosophy

- Tests live close to the code they test.
- Each test case should test one behaviour, not a scenario with multiple unrelated assertions.
- Test names should describe the behaviour, not the method name (`test_returns_empty_list_when_no_items`, not `test_get_items`).
- Avoid testing implementation details; test observable behaviour.

## When to load a language-specific skill

This skill covers shared principles only. For language-specific rules, load:
- `google-style-python` — Python
- `google-style-typescript` — TypeScript
- `google-style-javascript` — JavaScript
- `google-style-go` — Go
- `google-style-java` — Java
- `google-style-cpp` — C++
- `google-style-shell` — Shell / Bash
- `google-style-markdown` — Markdown / documentation
