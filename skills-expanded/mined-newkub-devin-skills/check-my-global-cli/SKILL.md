---
name: check-my-global-cli
description: Report installed CLI tools and commands to assess converting them into devin skills
argument-hint: "[scope]"
related:
  - learn
  - idea
  - suggest-next-action
  - report
  - run-test
  - search-skills

---

## Goal

Report the CLI tools installed on the machine and their commands to assess how suitable they are for conversion into devin skills.

## Scope

Use to survey installed CLI tools from `mise`, `scoop`, `winget`, and `bun` and report their commands, covering:

- List of installed tools
- Commands, subcommands, and options of each tool
- Usage frequency and complexity
- Suitability for conversion into skills

## Execute

### 1. Discover Installed CLI Tools

> Goal: Find all installed CLI tools

1. Check installed tools with `mise list`, `scoop list`, `winget list`, `bun --version`
2. Compile the tool list into a table (tool, version, manager)
3. Compare against `references/tool-map.md` — if an installed tool is missing from the map, add an action→tool→install→skill row

### 2. Learn Commands

> Goal: Explore each tool's commands and options

1. Run `/learn-from-cli` for each tool to see its subcommands, options, and output
2. Record commands, flags, argument types, and exit codes

### 3. Evaluate Conversion Candidates

> Goal: Assess which commands are worth converting into skills

1. Define the criteria:
   - Used often or has a repeating pattern
   - Has enough options/flags to warrant a guideline
   - Complex enough that a skill should assist
   - Shared across multiple projects or workspaces
2. Rank commands by priority: High, Medium, Low
3. Run `/report` to summarize the candidates

### 4. Suggest Next Action

> Goal: Present the next direction

1. If there are High priority commands → run `/idea-convert-my-global-cli-to-skills` to start converting
2. If information is insufficient → run `/learn-from-cli` further, or re-run `/check-my-global-cli`
3. If there are no candidates → run `/suggest-next-action` to find another direction

## Rules

### Report UX/UI

> Goal: Make the report easy to read, put key findings up top, and lead to action (my global cli)

1. Summarize key findings above the details (my global cli)
2. Use `/report` for multi-column comparison tables (my global cli)
3. Use `/report` for status/progress/logs reports
4. Use a "No." column first, ordered 1, 2, 3, ..., with clear headers, grouped/ordered by importance (my global cli)
5. Use the ✅ ❌ ⚠️ symbols for status indicators
6. Always run `/suggest-next-action` at the end of the report

### 1. Tool Coverage

- Cover all tools from `mise`, `scoop`, `winget`, `bun`
- Skip tools with no CLI interface or no `--help`
- Identify each tool's package manager

### 2. Command Analysis

- Record all commands, subcommands, and options
- Identify the flags that matter for common workflows
- Do not duplicate data from `/learn-from-cli`

### 3. Conversion Criteria

- High: used often + many flags + used across multiple projects or workspaces
- Medium: used occasionally or has few flags
- Low: rarely used or a simple command
- Use /deep-test cli if needed
- Use /run-test if needed


## Expected Outcome

- Table of installed CLI tools with versions
- Summary of commands, options, and flags
- List of commands suitable for conversion into skills, with priority
- Next-step suggestions, e.g. run `/idea-convert-my-global-cli-to-skills`
- An easy-to-read report with key findings at the top
- A clear next action
