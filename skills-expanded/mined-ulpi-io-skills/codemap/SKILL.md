---
name: codemap
version: 2.0.0
description: |
  Discover code by MEANING and DEPENDENCY structure, not by matching text — with the `codemap` CLI:
  hybrid vector+BM25 semantic search, symbol lookup, incoming/outgoing dependency tracing, file
  summaries, PageRank importance, afferent/efferent coupling, and cycle detection over an indexed
  repo. Only authoritative when the index exists and is fresh — a stale or empty index is called out,
  not trusted. Use for architecture-aware code discovery instead of plain text search.
allowed-tools:
  - Bash
  - Read
argument-hint: "[search query, symbol, file path, or analysis goal]"
arguments:
  - request
when_to_use: |
  Use when the user wants semantic search, symbol finding, dependency tracing, file summaries,
  coupling/importance ranking, or cycle detection. Examples: "where is auth handled", "find the
  UserService symbol", "what depends on this file", "show circular deps". Do NOT use when exact `grep`
  or `glob` is enough, or when the target is a precise syntactic shape rather than meaning (ast-grep);
  codemap answers architecture questions, not literal or structural pattern matches.
effort: high
---

<EXTREMELY-IMPORTANT>
`codemap` only helps when the repo is indexed and the command matches the question.

Non-negotiable rules:
1. Check `codemap --version` and `codemap status` before relying on results.
2. If the project has no codemap setup, ask before running `codemap init`.
3. Prefer the narrowest codemap command that answers the question.
4. Prefer machine-readable output when you need to interpret structured results.
5. Do not auto-edit Claude or project settings just to enable codemap.
</EXTREMELY-IMPORTANT>

# codemap

## Inputs

- `$request`: The search or analysis goal

## Goal

Use the `codemap` CLI to answer architecture and discovery questions with better signal than plain-text search when:

- intent is semantic rather than literal
- symbol lookup matters
- dependency direction matters
- file importance or coupling matters

## Step 0: Verify availability and index state

Check:

- `codemap --version`
- `codemap status`

If `codemap` is missing, tell the user to install it with `npm install -g @ulpi/codemap` and stop. Do not install it automatically.

If the repo is not configured:

- explain that `codemap init` creates project config
- ask before running `codemap init`
- once configured, run `codemap index`

If the repo is configured but stale, re-index with `codemap index`.

**Success criteria**: There is a working codemap index for the current repository.

## Step 1: Choose the right command

### Command Reference

| Command | What It Does | Key Flags |
|---------|-------------|-----------|
| `codemap search <query>` | Hybrid vector+BM25 code search | `-l N`, `--json` |
| `codemap symbols <query>` | Find functions, classes, types by name | `-l N`, `--json` |
| `codemap summary <file>` | File overview with symbols and size | `--json` |
| `codemap deps <file>` | Outgoing imports (what this file uses) | `--json` |
| `codemap dependents <file>` | Incoming imports (what uses this file) | `--json` |
| `codemap rank [file]` | PageRank importance scores | `-l N`, `--json` |
| `codemap coupling` | Afferent/efferent coupling and instability | `--module <path>`, `-l N`, `--json` |
| `codemap cycles` | Detect circular dependencies | `--json` |
| `codemap graph-stats` | Aggregate dependency graph statistics | `--json` |
| `codemap index` | Index project for search | `--full` |
| `codemap status` | Show index stats | `--json` |
| `codemap watch` | Live index updates on file change | `--debounce <ms>` |
| `codemap read <file>` | Read full source (or line range) | `--start`, `--end` |
| `codemap serve` | Start MCP server over stdio | |

### Quick Routing

| What You Want | Command |
|---------------|---------|
| Find code that does X | `codemap search "X"` |
| Find function/class named X | `codemap symbols "X"` |
| What does this file depend on? | `codemap deps <file>` |
| What depends on this file? | `codemap dependents <file>` |
| Most important files | `codemap rank` |
| Circular dependencies? | `codemap cycles` |
| Overview of a file | `codemap summary <file>` |
| Architecture health | `codemap coupling` |
| Project stats | `codemap graph-stats` |

Prefer `--json` when you need structured output rather than prose.

**Success criteria**: The command matches the actual question instead of overfetching.

## Step 2: Run the minimal useful codemap query

Start narrow:

- limited result count
- specific file or module when known
- one analysis dimension at a time

Then expand only if the first result set is clearly insufficient.

Rules:

- do not run every codemap command "just in case"
- do not use codemap when exact `grep` is simpler
- when file contents are needed after discovery, use `Read` on the concrete file paths returned

**Success criteria**: The answer uses codemap for discovery and `Read` only for the specific files that matter.

## Step 3: Report results in decision-friendly form

Summarize:

- what command was used
- why it was the right command
- the most relevant results
- any follow-up files worth opening

When there are no strong results, say that explicitly instead of inventing certainty.

**Success criteria**: The user can act on the result set without parsing raw codemap output.

## MCP Alternative

Codemap can also run as an MCP server, giving AI agents direct tool access without Bash:

```bash
claude mcp add codemap codemap serve
```

This exposes tools like `mcp__codemap__search_code`, `mcp__codemap__search_symbols`, etc. The CLI skill (this file) uses Bash commands. MCP gives agents native tool calls. Both work -- use whichever the agent setup prefers.

## Guardrails

- Do not auto-modify settings files to add permissions.
- Do not run `codemap init` without the user's approval when it would create new config.
- Do not treat stale or empty indexes as authoritative.
- Do not replace simple exact-match tools with codemap when text search is clearly enough.
- Do not add `disable-model-invocation`; this is a general discovery skill.

## Output Contract

Report:

1. codemap availability and index state
2. the command chosen
3. the most relevant hits or graph results
4. the next file(s) to open if deeper reading is needed
5. any limitations such as missing index or weak results
