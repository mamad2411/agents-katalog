---
name: coregit
description: |
  Serverless Git backend for AI-native products. Use this skill when the user wants to create git repos, commit code, read files, diff branches, search code (full-text or AI semantic search), set up version control via API, or create LLM Wiki knowledge bases — without the git CLI. Handles user onboarding (signup, email verification, API key) entirely from the terminal.
metadata:
  author: coregit
  version: "1.0.0"
allowed-tools: Bash(cgt:*) Bash(curl:*) Bash(npx:*)
---

# Coregit

Coregit is a serverless Git hosting platform. Create repos, commit files, read code, diff branches, merge, cherry-pick, search — all via REST API. No git CLI needed.

- **API base:** `https://api.coregit.dev`
- **Dashboard:** `https://app.coregit.dev`
- **Docs:** `https://docs.coregit.dev`
- **SDK:** `npm install @coregit/sdk`
- **CLI:** `npm install -g @coregit/cli` (binary: `cgt`)

## When to use

- User asks to set up a git backend or version control for their app
- User wants to commit, read, or diff files via API (not git CLI)
- User mentions "coregit" by name
- User needs a serverless git repo for an AI agent workflow

## Onboarding a new user

If the user does not have a Coregit API key, run this flow:

### Step 1: Ask for email and name, send verification code

```bash
npx coregit-wizard@latest --email <USER_EMAIL> --name <USER_NAME>
```

This installs the CLI and skill, then sends a 6-digit verification code to the email. Ask the user to check their inbox.

### Step 2: Verify with code and get API key

```bash
npx coregit-wizard@latest --email <USER_EMAIL> --code <6_DIGIT_CODE>
```

This verifies the code, creates the account/org/API key, and stores credentials via `cgt auth login`. If the user already has an account, it creates a new key for their existing org.

### Step 3: Output summary

After setup, output a summary:
- Email and org slug
- Remind the user to save the API key (it is shown only once)
- Link to docs: https://docs.coregit.dev

## Using the CLI (preferred for agents — saves tokens)

After `cgt auth login`, all commands use stored credentials automatically. Output is JSON.

### Repositories

```bash
cgt repos create my-project
cgt repos list
cgt repos get my-project
cgt repos delete my-project
```

### Commit files

```bash
# From local files (path_in_repo:local_file)
cgt commit my-project -b main -m "feat: init" \
  -f src/index.ts:./index.ts -f README.md:./README.md

# Inline content (path:=content)
cgt commit my-project -b main -m "add config" \
  -f config.json:='{"port": 3000}'

# From stdin (JSON array)
echo '[{"path":"src/app.ts","content":"console.log(1)"}]' | cgt commit my-project -b main -m "add app"
```

### Read files

```bash
cgt tree my-project main              # list files
cgt blob my-project main src/app.ts   # read file (JSON)
cgt blob my-project main src/app.ts --raw  # raw content
```

### Branches

```bash
cgt branches create my-project feature-x --from main
cgt branches list my-project
cgt branches merge my-project feature-x
cgt branches delete my-project feature-x
```

### Diff & Compare

```bash
cgt diff my-project main feature-x --patch
cgt compare my-project main feature-x
```

### Commits

```bash
cgt log my-project --ref main --limit 10
```

### Search (full-text)

```bash
cgt search "TODO" --repos my-project --ref main
cgt search "function.*Async" --repos my-project --regex
```

`--ref` accepts branch name or commit SHA.

### Semantic search (AI-powered)

```bash
# 1. Index the repo
cgt index create my-project -b main

# 2. Check status (poll until "ready")
cgt index status my-project

# 3. Search by natural language
cgt semantic-search my-project "user authentication with password hashing" --ref main

# Search at a specific commit
cgt semantic-search my-project "auth logic" --ref 8b7d315321...
```

### Snapshots

```bash
cgt snapshots create my-project v1-backup -b main
cgt snapshots list my-project
cgt snapshots restore my-project v1-backup
```

### Workspace (execute commands)

```bash
cgt exec my-project "npm install && npm run build" -b main --commit --commit-message "build output"
```

### Clone with standard git

```bash
git clone https://ORGSLUG:cgk_live_...@api.coregit.dev/ORGSLUG/my-project.git
```

## REST API (alternative to CLI)

All requests require header `x-api-key: cgk_live_...`. Use the CLI above when possible — it's shorter and handles auth automatically.

<details>
<summary>curl examples (click to expand)</summary>

```bash
# Create repo
curl -X POST https://api.coregit.dev/v1/repos \
  -H "x-api-key: $COREGIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"slug": "my-project"}'

# Commit files
curl -X POST https://api.coregit.dev/v1/repos/my-project/commits \
  -H "x-api-key: $COREGIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"branch":"main","message":"init","author":{"name":"Agent","email":"a@a.dev"},"changes":[{"path":"app.ts","content":"console.log(1)"}]}'

# Search
curl -X POST https://api.coregit.dev/v1/search \
  -H "x-api-key: $COREGIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"TODO","repos":["my-project"],"ref":"main"}'

# Semantic search
curl -X POST https://api.coregit.dev/v1/repos/my-project/semantic-search \
  -H "x-api-key: $COREGIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"auth logic","ref":"main"}'
```

</details>

## Key API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /v1/repos | Create repo |
| GET | /v1/repos | List repos |
| POST | /v1/repos/:slug/commits | Commit files |
| GET | /v1/repos/:slug/commits | List commits |
| GET | /v1/repos/:slug/tree/:ref | List files |
| GET | /v1/repos/:slug/blob/:ref/:path | Read file |
| POST | /v1/repos/:slug/branches | Create branch |
| GET | /v1/repos/:slug/branches | List branches |
| POST | /v1/repos/:slug/branches/:name/merge | Merge |
| GET | /v1/repos/:slug/diff/:ref1/:ref2 | Diff |
| POST | /v1/repos/:slug/snapshots | Create snapshot |
| POST | /v1/repos/:slug/exec | Run shell command |
| POST | /v1/search | Cross-repo code search |
| POST | /v1/repos/:slug/semantic-search | AI semantic search |
| POST | /v1/repos/:slug/index | Trigger semantic index |
| GET | /v1/repos/:slug/index/status | Index status |

## LLM Wiki (knowledge bases)

Create persistent, version-controlled knowledge bases maintained by LLM agents. Based on the LLM Wiki pattern by Andrej Karpathy.

A wiki is a Coregit repo with 3 layers: `raw/` (immutable sources), `wiki/` (LLM-generated pages), and `schema.md` (agent instructions).

### Create a wiki

```bash
cgt wiki init my-research --title "AI Research" --description "Deep dive into transformers"
```

### Wiki operations

```bash
# List pages (with parsed frontmatter)
cgt wiki pages my-research
cgt wiki pages my-research --type concept --tag deep-learning

# Read a page
cgt wiki page my-research transformers.md
cgt wiki page my-research transformers.md --raw

# List and read raw sources
cgt wiki sources my-research
cgt wiki source my-research attention-paper.md --raw

# Browse wiki structure
cgt wiki index my-research        # content catalog (index.md)
cgt wiki log my-research          # activity log (log.md)

# Generate llms.txt for external LLM consumption
cgt wiki llms-txt my-research --format full

# Semantic search (searches both wiki pages AND raw sources)
cgt wiki search my-research "how does attention work" --scope all

# Knowledge graph (nodes, edges, tag clusters)
cgt wiki graph my-research

# Health stats (pages, sources, orphans, word counts)
cgt wiki stats my-research
```

### Ingest workflow (agent writes wiki pages via commits)

```bash
# 1. Add a source to raw/
cgt commit my-research -b main -m "add source" \
  -f raw/paper.md:./paper.md

# 2. Agent processes source → creates/updates wiki pages + index + log (atomic commit)
echo '[
  {"path":"wiki/transformers.md","content":"---\ntitle: \"Transformers\"\nsummary: \"...\"\ntags: [deep-learning]\ntype: concept\nsources: [raw/paper.md]\n---\n\nContent..."},
  {"path":"index.md","content":"# Index\n\n## Concepts\n- [Transformers](wiki/transformers.md): ..."},
  {"path":"log.md","content":"# Log\n\n## [2026-04-10] ingest | Paper\nCreated wiki/transformers.md."}
]' | cgt commit my-research -b main -m "ingest: paper"
```

### Wiki API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /v1/repos/:slug/wiki/init | Create wiki from template |
| GET | /v1/repos/:slug/wiki/pages | List pages with frontmatter |
| GET | /v1/repos/:slug/wiki/pages/:path | Read single page (parsed) |
| GET | /v1/repos/:slug/wiki/sources | List raw sources |
| GET | /v1/repos/:slug/wiki/sources/:path | Read raw source |
| GET | /v1/repos/:slug/wiki/index | Get index.md |
| GET | /v1/repos/:slug/wiki/log | Get log.md (parsed) |
| GET | /v1/repos/:slug/wiki/llms.txt | Auto-generated llms.txt |
| POST | /v1/repos/:slug/wiki/search | Semantic search (wiki + sources) |
| GET | /v1/repos/:slug/wiki/graph | Knowledge graph |
| GET | /v1/repos/:slug/wiki/stats | Wiki health stats |

## Important notes

- The API key is shown only once during onboarding. Always remind the user to save it.
- All file commits are atomic — multiple files in one API call.
- Use `parent_sha` in commit requests for conflict detection (returns 409 if branch moved).
- Snapshots are named restore points — create one before risky operations.
- LLM Wiki pages use YAML frontmatter (title, summary, tags, sources, type, related).
- Wiki writes use the standard commits API — wiki endpoints are read-only convenience layers.
- Full docs at https://docs.coregit.dev
- LLM Wiki guide: https://docs.coregit.dev/docs/guides/llm-wiki
- Agent onboarding guide: https://docs.coregit.dev/docs/getting-started/agent-onboarding
- TypeScript SDK: https://docs.coregit.dev/docs/getting-started/typescript-sdk
- API reference: https://docs.coregit.dev/docs/api-reference
