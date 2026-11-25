---
name: exivity-use
description: create, review, debug, and explain exivity use extractor scripts for rest apis, files, web pages, and odbc databases. use when a user asks for a .use extractor, wants help fixing http/json/csv/odbc logic, needs exivity-specific syntax, or wants generic integration code converted into correct use style. especially relevant for exivity data pipeline work involving public or encrypted variables, date parsing, response validation, json iteration, csv output, and saving extracted data to system/extracted.
---

# Exivity USE

Use this skill to produce real USE scripts, not pseudocode. Favor complete extractor scripts that can be pasted into `system/config/use/` with only endpoint names, credentials, SQL, or field names adjusted.

## Working style

1. Identify the source type: REST API, local file, web page, or ODBC.
2. Identify the runtime inputs and operator-editable settings.
3. Build the script in valid USE syntax with one statement per line.
4. Add Exivity-native handling for auth, HTTP headers, JSON access, loops, CSV output, and error termination.
5. When details are missing, make the smallest practical assumption, mark it with a comment, and keep the script executable.

## Non-negotiable USE rules

- Keep every statement on a single line. Do not use backslash as a line continuation.
- In `var` assignments, wrap USE function calls in parentheses: `var year = (@SUBSTR(${date}, 1, 4))`.
- In `if` expressions, quote string-valued variables when special characters may appear: `if ("${name}" == "")`.
- For `match`, always include at least one capture group in the regex.
- Treat missing JSON paths as `EXIVITY_NOT_FOUND` and handle optional fields explicitly.
- Use `public var` for operator-editable settings and `public encrypt var` for secrets that should appear in the GUI.
- Remember that `encrypt` and `encrypted` are preprocessor directives and encrypted values are machine-specific.
- Prefer `clear http_headers` before setting a fresh header set for a different request.
- Validate HTTP responses immediately after each request. If the task requires strict failure handling, terminate with error on non-success status.

## Preferred output patterns

### REST extractors

Default to this shape unless the user asks for something else:

1. Validate arguments.
2. Parse date parts with `@SUBSTR` when the script uses `yyyyMMdd` input.
3. Declare public variables for URLs and credentials.
4. Authenticate and extract token/header values.
5. Call data endpoints.
6. Loop over JSON or XML payloads with `foreach`.
7. Write CSV output using Exivity CSV commands.
8. Save the result under the expected `system/extracted/...` path.
9. Discard large buffers and terminate cleanly.

### ODBC extractors

Prefer:

- `set odbc_connect "..."` plus `buffer result = odbc_direct "${query}"` for direct connection strings.
- DSN form only when the user explicitly wants DSN-based access.
- Clear separation between query construction, query execution, and file save steps.

### CSV writing

- Prefer repeated `csv add_headers` or repeated `csv write_field` lines instead of trying to split a single statement over multiple lines.
- Use `csv fix_headers` after defining headers.
- If nested target directories may not exist, it is acceptable to write to `exported/` first and then `save` a file buffer into the final `system/extracted/...` destination.

## What to include in answers

When generating or repairing a USE script:

- Return a full `.use` script in a code block.
- Keep comments brief and practical.
- Preserve Exivity terminology such as buffer, foreach, environment, public variable, and extracted path.
- Explain only the tricky parts after the script, such as auth flow, JSON shape assumptions, or places the user must substitute values.

When reviewing a USE script:

- Call out exact syntax problems first.
- Then fix Exivity-specific logic issues such as multiline statements, incorrect function syntax, missing capture groups, unsafe `if` comparisons, or missing HTTP status validation.
- Prefer concrete corrected snippets over generic advice.

## Example user requests this skill should handle

- “Write a USE extractor for this REST API and save the csv into system/extracted.”
- “Convert this Python API integration into USE.”
- “Fix this extractor; Exivity says unbalanced parentheses.”
- “Review my ODBC extractor and make the variables public.”
- “Generate a USE script that authenticates, loops through JSON, and writes all fields to csv.”

## References to consult

- Read `references/use-syntax.md` for the distilled USE rules and gotchas.
- Read `references/use-patterns.md` for extractor patterns and repo/template guidance.
