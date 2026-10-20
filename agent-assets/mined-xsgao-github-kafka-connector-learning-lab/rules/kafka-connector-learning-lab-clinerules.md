# Agent Directives

## Execution & Style
- **Ultra-Concise**: No introductory text, post-task filler, or detailed monologues.
- **Minimal Thinking**: Keep internal thoughts to 1 brief sentence before issuing tool calls.
- **Direct Output**: Immediately execute tools or output final answers.

## Terminal & Environment (Windows / PowerShell)
- **PowerShell Syntax**: Use native cmdlets (`Get-ChildItem`), NEVER CMD flags (e.g., `dir /s` will fail).
- **Single-Pass Discovery**: Never crawl folders step-by-step. Fetch relative file paths in one command (e.g., `Get-ChildItem -Recurse -Filter *.java -Name`).

## Technical Guidelines
- **Tool Priority**: Prefer native tools (`read_file`, `write_to_file`, `apply_diff`) over terminal commands.
- **Code Style**: Match repo naming/formatting; preserve comments for Kafka API calls.

## Custom Commands
- When the user says "run doc", read `.cline/workflow/doc-change.md` and execute the steps.
- When the user says "run style", read `.cline/workflow/review-style.md` and execute the steps.
- When the user says "run tests", read `.cline/workflow/review-tests.md` and execute the steps.
