---
name: shell-operations
description: Use the shell tool for general command-line work in the current environment, including inspecting files and directories, reading and writing text files, searching content, running local programs, checking system state, transforming data, and fetching external read-only HTTP resources. Use when Codex needs to accomplish a task through the operating system or command-line tools rather than only reasoning in text.
---

# Shell Commands

Use `shell` whenever the task is best handled by actually running commands in the current environment.

This skill is not limited to code work. Use it for general command-line execution, workspace inspection, text processing, system checks, local tooling, and safe external retrieval.

## Core Rules

1. Start from the current environment.
Use the provided OS, shell, and working directory before probing further.

2. Match commands to the active shell.
On Windows, prefer PowerShell-native commands. On Linux and macOS, prefer POSIX-compatible commands.

3. Prefer doing over guessing.
If a question can be answered by running a command safely, run the command.

4. Keep commands small and purposeful.
Use the narrowest command that can answer the question or complete the step.

5. Prefer safe reads before writes.
Inspect first, then change only what is necessary.

6. Describe real outcomes.
If a command succeeds, summarize the useful result. If it fails, explain what failed and why it matters.

## When To Use This Skill

Use `shell` for tasks like:

- listing, locating, reading, or editing files
- searching text across notes, configs, docs, or source code
- checking logs, process state, environment variables, or system info
- running local programs, scripts, tests, or project commands
- converting, filtering, or summarizing command-line output
- checking installed tools and versions
- fetching public read-only data over HTTP when needed
- verifying whether something exists or works in the current environment

## Command Selection

### Windows PowerShell

Prefer these forms:

- List files: `Get-ChildItem -Force`
- Read file: `Get-Content -Path 'path\\to\\file'`
- Write file: `Set-Content -Path 'path\\to\\file' -Value 'content'`
- Append file: `Add-Content -Path 'path\\to\\file' -Value 'content'`
- Search text: `rg -n "pattern" .`
- PowerShell fallback search: `Select-String -Path '.\\*' -Pattern 'pattern' -Recurse`
- Find files: `Get-ChildItem -Recurse -File`
- Show environment: `Get-Location`, `$PSVersionTable`, `Get-ChildItem Env:`
- Show processes: `Get-Process`
- HTTP fetch: `curl.exe <url>` or `Invoke-WebRequest -UseBasicParsing <url>`

### POSIX Shell

Prefer these forms:

- List files: `ls -la`
- Read file: `cat 'path/to/file'` or `sed -n '1,160p' 'path/to/file'`
- Write file: `printf 'content\n' > 'path/to/file'`
- Append file: `printf 'content\n' >> 'path/to/file'`
- Search text: `rg -n "pattern" .`
- Fallback search: `grep -RIn 'pattern' .`
- Find files: `find . -type f`
- Show environment: `pwd`, `uname -a`, `env`
- Show processes: `ps`
- HTTP fetch: `curl <url>`

## External Retrieval

When the task depends on external facts, docs, API responses, or webpage content and no dedicated web tool exists, try a read-only HTTP request through `shell` first.

Preferred order:

- Windows: `curl.exe`, then `Invoke-WebRequest`
- POSIX: `curl`

Use this for:

- checking public documentation
- reading public APIs
- verifying remote metadata or status pages
- downloading small text responses for inspection

Do not claim the task cannot be done until a reasonable read-only fetch has been attempted, unless the user explicitly forbids network access.

## General Workflows

### Inspect

Use this when you need to understand the current environment or workspace.

1. List relevant files or directories
2. Read only the most informative items first
3. Summarize the useful structure or state

### Search

Use this when you need to find text, files, references, settings, or patterns.

1. Search broadly with `rg` when available
2. Narrow to the most relevant matches
3. Read the surrounding context
4. Report only the useful hits

### Execute

Use this when the task requires actually running a program or command.

1. Identify the smallest command that advances the task
2. Run it with the right shell syntax
3. Capture the important output
4. Decide whether another step is needed

### Diagnose

Use this when something is failing or behaving unexpectedly.

1. Reproduce or inspect the failure
2. Find the strongest signal in the output
3. Form the likeliest explanation from evidence
4. Suggest the next fix or check

### Transform

Use this when command-line tools can reshape text or data faster than manual reasoning.

Examples include:

- filtering lines
- counting matches
- extracting values
- sorting or deduplicating output
- combining small command results into a concise answer

## Common Mistakes

Avoid these:

- probing with multiple incompatible shells when one environment hint is already available`r`n- mixing PowerShell syntax with POSIX syntax
- assuming aliases behave the same across environments
- refusing to try a safe command when verification is possible
- using very broad or noisy commands when a smaller one is enough
- rewriting large files when a small targeted update would work
- claiming external retrieval is impossible before trying a read-only fetch

## Response Expectations

After using `shell`:

- summarize the useful result instead of dumping raw output
- mention the command outcome when it affects the conclusion
- explain failures in plain language
- keep multi-step summaries compact and ordered
