---
name: mono-cli
description: CLI skill for mono — a growth platform for indie developers. Manage works, articles, Q&A, profiles, and image uploads from the terminal.
version: 0.1.2
---

# mono CLI

CLI tool for [mono](https://www.mono.style), a growth platform for indie developers (個人開発者のためのグロースプラットフォーム).

Manage works, articles, questions, profiles, and image uploads from the terminal or AI agents.

## Setup

```bash
# 1. Install
npm install -g @kyaukyuai/mono-cli

# 2. Create a token (Web Dashboard → Settings → API Tokens)

# 3. Login
mono auth login --pat mono_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 4. Verify
mono auth whoami --json
```

## Authentication

The CLI uses Personal Access Tokens (PAT). Token resolution order:

1. `--token <PAT>` flag
2. `MONO_TOKEN` environment variable
3. `~/.mono/config.json` saved value

## Invariants

- Always validate with `--dry-run` before mutations
- Confirm with the user before deletions
- Use `--fields` to limit response size on list operations
- Use `--json` for programmatic parsing
- Check `mono schema <resource>` before building payloads

## Commands

### Auth

```bash
mono auth login --pat <PAT>    # Save token
mono auth logout               # Remove token
mono auth whoami               # User info
```

### Works

```bash
# List
mono works list --json
mono works list --fields id,title,status --json

# Get
mono works get <id> --json

# Create (dry-run → execute)
mono works create --json-data '{"title":"My App","category":"Webアプリ","description":"A great app description here"}' --dry-run
mono works create --json-data '{"title":"My App","category":"Webアプリ","description":"A great app description here"}' --json
mono works create --json-file ./work.json --json
cat ./work.json | mono works create --json-stdin --json

# Update
mono works update <id> --json-data '{"title":"Updated Title"}' --json
mono works update <id> --json-file ./work.json --json

# Delete (requires --yes)
mono works delete <id> --dry-run
mono works delete <id> --yes --json
```

### Articles

```bash
# List
mono articles list --json
mono articles list --category tech --sort popular --limit 10 --json

# Get
mono articles get <id> --json

# Create
mono articles create --json-data '{"title":"Article Title","body":"Body text...","category":"tech"}' --json
mono articles create --json-file ./article.json --json

# Update
mono articles update <id> --json-data '{"title":"Updated Title"}' --json
mono articles update <id> --json-file ./article.json --json

# Delete (requires --yes)
mono articles delete <id> --dry-run
mono articles delete <id> --yes --json

# Publish / unpublish
mono articles publish <id> --json
```

### Questions (Q&A)

```bash
# List
mono questions list --json
mono questions list --sort-by popular --status open --tag javascript --json

# Get
mono questions get <id> --json

# Create
mono questions create --json-data '{"title":"Question title 10+ chars","body":"Question body 20+ characters required"}' --json
mono questions create --json-file ./question.json --json

# Update
mono questions update <id> --json-data '{"status":"solved"}' --json
mono questions update <id> --json-file ./question.json --json

# Delete (requires --yes)
mono questions delete <id> --dry-run
mono questions delete <id> --yes --json

# Answer
mono questions answer <id> --json-data '{"body":"Answer body 20+ characters required"}' --json
mono questions answer <id> --json-file ./answer.json --json
```

### Profile

```bash
# Get
mono profile get --json
mono profile get --fields name,bio,role --json

# Update
mono profile update --json-data '{"name":"New Name","bio":"Bio text"}' --json
mono profile update --json-file ./profile.json --json
```

### Upload

```bash
# Upload image → get URL
mono upload ./screenshot.png --json
# => { "url": "https://...", "fileName": "...", "size": 12345, "type": "image/png" }

# Validate only (no upload)
mono upload ./screenshot.png --dry-run
```

Supported formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.svg` (max 5MB)

### Schema Introspection

```bash
mono schema works            # All works operations
mono schema works.create     # Create operation only
mono schema articles         # All articles operations
mono schema questions        # All questions operations
mono schema profile          # Profile schema
```

## Global Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--json` | JSON output | false (human) |
| `--ndjson` | NDJSON output (lists) | false |
| `--fields <f1,f2>` | Field mask | all |
| `--dry-run` | Validate only (no API call) | false |
| `--base-url <url>` | Override API base URL | config |
| `--token <pat>` | Override token | config |
| `--verbose` | Debug output | false |
| `--timeout <ms>` | Timeout | 30000 |
| `--retry <n>` | Retry count | 0 |
| `--retry-wait <ms>` | Retry wait | 500 |
| `--print-curl` | Print curl command | false |
| `--quiet` | Minimize stdout | false |
| `--no-color` | Disable color output | false |

## Workflow Examples

### Safely create a work

```bash
# 1. Check schema
mono schema works.create

# 2. Dry-run validation
mono works create --json-data '{"title":"Portfolio Site","category":"Webアプリ","description":"A portfolio site built with Next.js"}' --dry-run

# 3. Create
mono works create --json-data '{"title":"Portfolio Site","category":"Webアプリ","description":"A portfolio site built with Next.js"}' --json
```

### Create and publish an article

```bash
# 1. Create draft
mono articles create --json-data '{"title":"Dev Log","body":"# Introduction\n\nContent...","category":"dev-log"}' --json

# 2. Publish
mono articles publish <id> --json
```

### Upload image and create a work

```bash
# 1. Upload image
mono upload ./screenshot.png --json
# => { "url": "https://...", ... }

# 2. Create work with the returned URL
mono works create --json-data '{"title":"My App","category":"Webアプリ","description":"A great app","thumbnailUrl":"https://..."}' --json
```

## Output Formats

- **human** (default): Table format, human-readable
- **json** (`--json`): Pretty-printed JSON for programmatic use
- **ndjson** (`--ndjson`): One JSON per line, for streaming

## Error Handling

Errors are output as JSON to stderr:

```json
{
  "error": "Authentication required. Please login with `mono auth login`.",
  "exitCode": 1
}
```

Exit codes:
- `0`: Success
- `1`: Error (auth, validation, API)
