---
name: code-documentation
description: How to explain source code, generate inline comments, write Markdown documentation, summarize a file, or improve variable/function names — for JavaScript, TypeScript, Python, Java, C++, and Dart. Use this skill whenever the user asks what code does, wants it explained, wants comments or docs generated, wants a file summarized, or wants naming improved. Always preserve program logic exactly and never invent functionality not present in the code.
---

# Code Documentation

Five related but distinct tasks for helping a developer understand and document their own code. Pick the one the request maps to — don't blend them (e.g. don't add a naming table when the user only asked for an explanation).

Two rules apply to every task below:

- **Preserve logic.** Never change what the code does. Comments, renames, and docs describe behavior — they don't alter it.
- **Don't hallucinate.** Only describe behavior, parameters, return values, or edge cases that are actually present in the code shown. If something is ambiguous or determined elsewhere (e.g. an imported function's internals), say it's out of scope rather than guessing.

Keep every response concise — this is reference material for a working developer, not a tutorial.

## 1. Explain Code

Goal: help someone unfamiliar with the code understand it quickly.

Structure the explanation as:
1. **Purpose** — one to two sentences on what the code is for
2. **Step-by-step behavior** — in the order execution actually happens, not the order it's written if they differ (e.g. hoisted functions, async callbacks)
3. **Inputs and outputs** — parameters, return values, side effects (network calls, file writes, mutations), if any

Keep the whole explanation under ~200 words unless the user asks for more detail. Do not suggest improvements or point out bugs unless asked — this task is descriptive, not evaluative.

## 2. Generate Comments

Goal: add inline comments that help a future reader, without touching logic.

- Use the target language's normal comment convention:
  - JavaScript / TypeScript: `//` for lines, `/** */` (JSDoc) for functions
  - Python: `#` for lines, `"""docstring"""` for functions/classes
  - Java: `//` for lines, `/** */` (Javadoc) for methods/classes
  - C++: `//` for lines, `/** */` for functions/classes
  - Dart: `//` for lines, `///` (doc comments) for public members
- Comment the *why* or *non-obvious what* — skip comments on lines that are already self-explanatory (`i++`, simple assignments).
- Do not reformat, rename, reorder, or "clean up" the code while adding comments. The diff should be comments only.
- Return the full code in one code block, with nothing else around it (no preamble, no explanation) unless the user asks for one.

## 3. Generate Documentation

Goal: produce Markdown reference documentation for a function, class, or file.

Use exactly these sections, omitting any that don't apply:
- **Purpose** — what it does and why it exists, briefly
- **Parameters** — name, type (if determinable), and description for each
- **Returns** — type and description of the return value
- **Example usage** — a short, realistic call site

If a parameter's type isn't annotated and can't be inferred from usage, write "not specified" rather than guessing. Don't add a "Throws/Errors" section unless the code actually throws or the language's error handling is visible in the snippet.

## 4. Summarize File

Goal: a short, high-level orientation to an entire file — not a line-by-line walkthrough.

Write 3–5 sentences covering:
- What the file does overall
- Its key exports, functions, or classes (name-drop the important ones, not every helper)
- How it likely fits into a larger codebase (e.g. "this is a React hook consumed by form components", "this is an Express route handler")

If the file's role in the broader project isn't clear from the file alone, say so rather than inventing a narrative.

## 5. Improve Variable and Function Names

Goal: flag genuinely unclear names and suggest better ones — without renaming for style preference alone.

Return a Markdown table:

| Original | Suggested | Reason |
|---|---|---|
| `d` | `elapsedDays` | Single-letter name gives no indication of what it holds |

Rules:
- Only include names that are actually ambiguous, misleading, or too generic (`data`, `temp`, `x`, `flag`, `handleClick2`). If every name in the snippet is already clear, say so — don't force a table with weak suggestions.
- Suggested names must not collide with existing identifiers in the same scope.
- Do not suggest a rename that would require changing the function's public signature/API unless the user has indicated that's acceptable.
- This task never changes logic — it's a table of suggestions, not an edited file, unless the user explicitly asks you to apply the renames.

## Language coverage

These instructions apply uniformly across JavaScript, TypeScript, Python, Java, C++, and Dart. Adjust only:
- Comment/docstring syntax (see Task 2)
- Type reporting in documentation — include types for statically-typed languages (TypeScript, Java, C++, Dart) when visible; note "dynamically typed, inferred from usage" for plain JavaScript/Python where no annotation exists
- Idiomatic naming style (e.g. `camelCase` for JS/TS/Java/Dart, `snake_case` for Python)
