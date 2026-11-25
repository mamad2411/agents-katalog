---
name: arxiv
description: Standardized arXiv skill for MediaUse. Includes Windows install, key onboarding, strict context/auth flow, full arXiv dynamic command map, and safety/rate controls.
---

# MediaUse arXiv Skill

Discover arXiv research with a guest-only workflow for paper search, category recents, author lookups, and detailed paper retrieval.

## Scope

Use this skill when the task targets arXiv operations such as:

- Account: plugin health
- Search: papers by keyword
- Recent: latest submissions in a category
- Paper: full details for a specific paper ID
- Author: papers by a named author

arXiv is a public read-only repository. No login required. All operations are read-only.

## 1. Install MediaUse CLI

Install the MediaUse CLI in the user's own secure environment using the official npm package:

```powershell
npm install -g @mediause/cli
mediause --version
```

If the CLI is already installed, run the version check again to confirm it is available in PATH.

Current support status:

- Windows: supported
- Linux: not supported yet
- macOS: not supported yet

Recommended skill install path:

- .mediause/skills/arxiv/SKILL.md

## 2. Get and Configure MediaUse Key

### 2.1 Apply for key

1. Open https://mediause.dev/ in the user's browser.
2. Sign in to the user's account.
3. Open the Project settings.
4. Create or view the API key in the user's own secure environment; never paste it into chat, logs, terminal history, or a CLI command.

### 2.2 Safe key verification and configuration

Before any arXiv action, run a read-only verification check:

```powershell
mediause manage key --json
```

This command is used only to confirm whether a MediaUse API key is already configured in the local environment. Do not paste, echo, or print the secret value into chat, logs, terminal history, or the skill instructions. If the command shows no configured key, ask the user to configure it in their own secure local environment or through the MediaUse app; never instruct the model to embed the API key directly into a CLI command or copy it verbatim into a prompt.

## 3. Core Flow (Mandatory Order)

Always follow this order:

1. Discover site and commands.
2. Bind account context with `use account` (guest is the only mode for arXiv).
3. Execute dynamic site actions.
4. Verify with trace/task.

> arXiv is a fully public API 鈥?no login required. Always use `arxiv:guest` as the account context. Skip `auth health` for guest mode.

### 3.1 Discover and plugin setup

```powershell
mediause plugin list --json
mediause plugin add arxiv --json
mediause arxiv -h
mediause arxiv search -h
mediause arxiv get -h
mediause arxiv user -h
mediause arxiv account -h
```

### 3.2 Bind guest context

arXiv does not require login. Use guest mode.

```powershell
mediause use account arxiv:guest --show --json
```

Guest mode rules:

- All arXiv operations are read-only (`account health`, `search papers`, `get paper`, `get recent`, `user author`).
- No write operations exist for arXiv.
- If page shows `unusual traffic` or captcha, repeat with `--show` to manually resolve.

### 3.3 Auth health

Not required for guest mode. Skip this step for arXiv.

## 4. arXiv Dynamic Command Map (v1)

public arXiv API plugin with guest default account and read-only commands.

### 4.1 account.health

Check plugin/runtime health for current arXiv context.

```powershell
mediause arxiv account health --json
```

### 4.2 search.papers

Search papers by keyword across all fields (title, abstract, authors, etc.).

```powershell
mediause arxiv search papers --query "<query>" [--limit <n>] --json
```

- `--query` (required): keyword or phrase, e.g. `"attention is all you need"`
- `--limit`: max results, default `10`, max `25`

Columns returned: `id`, `title`, `authors`, `published`, `primary_category`, `url`

Example:

```powershell
mediause arxiv search papers --query "transformer language model" --limit 10 --json
mediause arxiv search papers --query "diffusion model image generation" --limit 5 --json
```

### 4.3 get.recent

List recent submissions in a specific category, sorted by submission date descending.

```powershell
mediause arxiv get recent --category <category> [--limit <n>] --json
```

- `--category` (required): arXiv category code, e.g. `cs.CL`, `cs.LG`, `math.PR`, `q-bio.NC`
- `--limit`: max results, default `10`, max `50`

Columns returned: `id`, `title`, `authors`, `published`, `primary_category`, `url`

Common categories:

| Category | Description |
|----------|-------------|
| `cs.CL` | Computation and Language (NLP) |
| `cs.LG` | Machine Learning |
| `cs.CV` | Computer Vision |
| `cs.AI` | Artificial Intelligence |
| `cs.CR` | Cryptography and Security |
| `math.ST` | Statistics Theory |
| `q-bio.NC` | Neurons and Cognition |
| `physics.comp-ph` | Computational Physics |

Example:

```powershell
mediause arxiv get recent --category cs.CL --limit 20 --json
mediause arxiv get recent --category cs.LG --limit 10 --json
```

### 4.4 get.paper

Get full details for a specific paper by arXiv ID.

```powershell
mediause arxiv get paper --id <id> --json
```

- `--id` (required): arXiv paper ID, e.g. `1706.03762` or `2303.08774`

Columns returned: `id`, `title`, `authors`, `published`, `updated`, `primary_category`, `categories`, `abstract`, `comment`, `pdf`, `url`

Example:

```powershell
mediause arxiv get paper --id 1706.03762 --json
mediause arxiv get paper --id 2303.08774 --json
```

### 4.5 user.author

List papers by a named author, newest first. Author name matching is fuzzy 鈥?try alternate spellings if no results.

```powershell
mediause arxiv user author --author "<author_name>" [--limit <n>] --json
```

- `--author` (required): author full name or initials, e.g. `"Yoshua Bengio"` or `"Y Bengio"`
- `--limit`: max results, default `20`, max `50`

Columns returned: `id`, `title`, `authors`, `published`, `primary_category`, `url`

Example:

```powershell
mediause arxiv user author --author "Yoshua Bengio" --limit 20 --json
mediause arxiv user author --author "Andrej Karpathy" --limit 10 --json
mediause arxiv user author --author "Y LeCun" --json
```

## 5. Workflow Examples

### Workflow A: Discover recent NLP papers and retrieve one in full

```powershell
# A1. Setup
mediause plugin add arxiv --json
mediause use account arxiv:guest --show --json

# A2. Browse recent submissions in cs.CL
mediause arxiv get recent --category cs.CL --limit 15 --json

# A3. Get full details and abstract for a specific paper
mediause arxiv get paper --id 2303.08774 --json

# A4. Verify
mediause trace last --json
```

### Workflow B: Keyword search and author follow-up

```powershell
# B1. Setup
mediause use account arxiv:guest --show --json

# B2. Search for a topic
mediause arxiv search papers --query "large language model reasoning" --limit 10 --json

# B3. Find more papers by the first author
mediause arxiv user author --author "Jason Wei" --limit 20 --json

# B4. Get full paper details
mediause arxiv get paper --id 2201.11903 --json

# B5. Verify
mediause trace last --json
```

### Workflow C: Monitor a research area daily

```powershell
# C1. Setup
mediause use account arxiv:guest --show --json

# C2. Pull recent AI papers
mediause arxiv get recent --category cs.AI --limit 50 --json

# C3. Pull recent ML papers
mediause arxiv get recent --category cs.LG --limit 50 --json

# C4. Search for a specific concept
mediause arxiv search papers --query "in-context learning" --limit 25 --json

# C5. Verify
mediause trace last --json
```

## 6. Operational Constraints (Mandatory)

### 6.1 Read-only

arXiv has no write operations. All commands are fetch-only. Do not attempt post, reply, or engage actions.

### 6.2 Frequency limits

arXiv public API has a soft rate limit. Apply pacing between repeated calls.

| Operation | Default limit | Minimum spacing |
|-----------|--------------|-----------------|
| `search papers` | max 25/call | >= 3 seconds between calls |
| `get recent` | max 50/call | >= 3 seconds between calls |
| `get paper` | 1/call | >= 1 second between calls |
| `user author` | max 50/call | >= 3 seconds between calls |

- Do not run bulk loops without delay (e.g. fetching 100+ papers in rapid succession).
- If you receive HTTP 429 or arXiv API errors, wait at least 30 seconds before retrying.

### 6.3 Content use constraints

- Do not republish paper abstracts or full text without proper attribution.
- Do not scrape arXiv to build competing paper indexes.
- Respect arXiv's [usage policies](https://info.arxiv.org/help/api/tou.html).

### 6.4 Failure handling

Always use `--json` for structured error output.

Common errors:

| Error | Cause | Action |
|-------|-------|--------|
| `No papers found` | Query too specific or wrong spelling | Broaden query or check spelling |
| `Paper <id> was not found` | Invalid arXiv ID format | Use format `YYMM.NNNNN` or `subj-class/YYMMNNN` |
| `Invalid arXiv category` | Category code typo | Check [arXiv category list](https://arxiv.org/category_taxonomy) |
| `arXiv API HTTP 4xx/5xx` | API error or rate limit | Wait 30s and retry |
| `unusual traffic` / captcha | Guest session flagged | Rerun `use account arxiv:guest --show --json` to resolve manually |

Recovery pattern:

```powershell
# On arXiv API error or unusual traffic
mediause use account arxiv:guest --show --json
mediause trace last --json
```

## 7. Quick Reference

```powershell
# always run once before each workflow (auto-upgrade latest)
mediause --version

# Install
mediause plugin add arxiv --json

# Context
mediause use account arxiv:guest --show --json

# Commands
mediause arxiv account health --json
mediause arxiv search papers --query "<query>" [--limit <n>] --json
mediause arxiv get recent --category <category> [--limit <n>] --json
mediause arxiv get paper --id <id> --json
mediause arxiv user author --author "<name>" [--limit <n>] --json

# Verify
mediause trace last --json
mediause task status --task-id <id> --json
```


Skill Metadata
Maintainer: @mediause-demo
Last-Updated: 2026-08-22
Version: v2


