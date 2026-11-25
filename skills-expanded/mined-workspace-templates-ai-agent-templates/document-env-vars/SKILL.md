---
name: document-env-vars
description: Finds every environment variable your code reads and writes an example env file plus a table of what each one does.
disable-model-invocation: true
---

Document the environment variables used by: $ARGUMENTS (whole project if empty).

1. Search for reads in every language present: `process.env`, `import.meta.env`, `os.environ`, `os.getenv`, `ENV[`, `System.getenv`, `std::env::var`, and config loaders such as dotenv or pydantic settings. Also search Dockerfiles, compose files, CI workflows and shell scripts.
2. For each variable record: name, file and line of first use, whether code fails without it (required) or falls back to a default, the default value, and the expected type or format.
3. Mark likely secrets by name (KEY, TOKEN, SECRET, PASSWORD, DSN). Leave their example value empty or as a clear dummy value such as `changeme`.
4. Read existing .env files only to learn names. Never print or copy actual values.
5. Write `.env.example` grouped by area with a comment above each line, and a Markdown table with the columns Name, Required, Default, Purpose.

Show the table and the file contents, list variables found in code but missing from the old .env.example, and ask before creating or overwriting anything.
