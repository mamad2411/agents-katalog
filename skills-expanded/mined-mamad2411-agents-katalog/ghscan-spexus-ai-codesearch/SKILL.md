# codesearch skill for AI coding agents

Use this skill when you need to search code semantically across indexed repositories.

## When to use

- Finding implementations: "where is the authentication middleware?"
- Understanding architecture: "how does the payment processing pipeline work?"
- Locating related code: "find all Kafka consumer handlers"
- Discovering patterns: "show me error handling examples"
- Finding tests: "tests for the user registration flow"
- Finding duplicates: "are there copy-pasted services across repos?"

## Prerequisites

`codesearch` must be installed and at least one repository indexed:

```bash
source /path/to/.venv/bin/activate
codesearch repo add /path/to/repo
codesearch index
```

## Commands

### Basic search

```bash
codesearch search "your semantic query"
```

### Search with filters

```bash
# By repository
codesearch search "query" --repo myapp

# By language
codesearch search "query" --lang python
codesearch search "query" --lang python --lang go

# By file path glob
codesearch search "query" --path "src/api/*"

# Limit results
codesearch search "query" --limit 5

# Minimum similarity threshold (0.0-1.0, higher = more relevant)
codesearch search "query" --threshold 0.5
```

### Output formats

```bash
# JSON (default when piped, best for parsing)
codesearch search "query" --format json

# Human-readable text (default in terminal)
codesearch search "query" --format text

# Compact: path:line score only
codesearch search "query" --format compact

# With context lines
codesearch search "query" --context 5

# No code snippets
codesearch search "query" --no-snippet
```

### JSON output schema

```json
[
  {
    "repo": "myapp",
    "path": "src/auth/middleware.py",
    "line": 42,
    "score": 0.82,
    "snippet": "class AuthMiddleware:\n    def process_request(self, request):\n        ...",
    "lang": "python"
  }
]
```

### Duplicate detection

```bash
# Find semantic duplicates across all indexed repos
codesearch duplicates --repo myapp

# Cross-file only (skip duplicates within the same file)
codesearch duplicates --repo myapp --cross-file-only

# Across multiple repos
codesearch duplicates --repo app --repo lib

# Filter by path
codesearch duplicates --path "*/utils/*"

# Adjust similarity threshold (default: 0.82)
codesearch duplicates --threshold 0.90

# JSON output
codesearch duplicates --repo myapp --format json
```

#### Duplicates JSON output schema

```json
[
  {
    "chunk_a": {
      "repo": "myapp",
      "path": "src/services/user_service.py",
      "line_start": 10,
      "line_end": 45,
      "snippet": "class UserService:\n    ...",
      "lang": "python"
    },
    "chunk_b": {
      "repo": "myapp",
      "path": "src/services/order_service.py",
      "line_start": 10,
      "line_end": 45,
      "snippet": "class OrderService:\n    ...",
      "lang": "python"
    },
    "similarity": 0.92
  }
]
```

### Index management

```bash
codesearch repo list                # list repos with chunk counts
codesearch index --status           # show index stats
codesearch index                    # incremental re-index
codesearch index --full             # full re-index
```

## Integration with Claude Code

### Option 1: MCP server (recommended)

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "codesearch": {
      "command": "/path/to/.venv/bin/codesearch",
      "args": ["mcp"]
    }
  }
}
```

Then use the `semantic_search` tool directly:

```
Use the semantic_search tool to find Kafka consumer handlers
```

### Option 2: CLI via Bash tool

```bash
codesearch search "kafka consumer handler" --format json --limit 5
```

Parse the JSON output to read relevant files.

## Workflow example

1. Search semantically for the area of interest:
   ```bash
   codesearch search "user registration validation" --format json --limit 3
   ```

2. Read the top results to understand the code:
   ```bash
   # Use the path and line from search results
   cat -n src/auth/registration.py | head -80
   ```

3. Search for related code (tests, callers):
   ```bash
   codesearch search "test registration" --lang python --limit 3
   codesearch search "calls register_user" --limit 5
   ```

## Tips

- **Be descriptive**: "HTTP request authentication middleware" works better than "auth"
- **Use filters**: `--lang` and `--path` narrow results significantly
- **Threshold**: start with 0.0 (default), increase to 0.3-0.5 to filter noise
- **Pipe to jq**: `codesearch search "query" | jq '.[0].path'` to extract fields
- **Re-index after changes**: `codesearch index` is incremental and fast
- **Multiple repos**: search spans all indexed repos by default, use `--repo` to narrow

## Supported languages

AST-aware chunking: Python, Java, JavaScript, TypeScript, Go, Rust, Ruby, PHP, Scala, C, C++, C#, Kotlin

Line-based fallback: YAML, TOML, SQL, Shell, Gradle, XML
