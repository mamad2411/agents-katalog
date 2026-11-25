---
name: huggingface
description: Standardized Hugging Face skill for MediaUse. Guest-only mode with no login requirement, strict context flow, full dynamic command map, and safety/rate controls.
---

# MediaUse Hugging Face Skill

Use Hugging Face discovery workflows in MediaUse with a guest-only, no-login flow for papers, models, datasets, and spaces.

## Scope

Use this skill when the task targets Hugging Face operations such as:

- Account: plugin health check
- Papers: top paper rankings, single paper detail
- Models: ranked model listing
- Datasets: ranked dataset listing
- Spaces: ranked space listing

Hugging Face in this plugin is guest-only. No login is required.

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

- .mediause/skills/huggingface/SKILL.md

## 2. Get and Configure MediaUse Key

### 2.1 Apply for key

1. Open https://mediause.dev/ in the user's browser.
2. Sign in to the user's account.
3. Open the Project settings.
4. Create or view the API key in the user's own secure environment; never paste it into chat, logs, terminal history, or a CLI command.

### 2.2 Configure key in CLI

```powershell
mediause manage key --json
```

## 3. Core Flow (Guest-Only, No Login)

Always follow this order:

First step on every run: execute install script once to auto-install/auto-upgrade the latest MediaUse CLI.

1. Discover site and commands.
2. Bind guest context with `use account huggingface:guest`.
3. Execute dynamic read actions.
4. Verify with trace/task.

Important constraints:

- Hugging Face plugin here only uses guest mode.
- Do not run `mediause auth login huggingface`.
- Do not require `mediause auth health` for this plugin flow.

### 3.1 Discover and plugin setup

```powershell
mediause plugin list --json
mediause plugin add huggingface --json
mediause huggingface -h
mediause huggingface get -h
mediause huggingface account -h
```

### 3.2 Bind guest context

```powershell
mediause use account huggingface:guest --json
```

If the page/session is challenged (for example unusual traffic), rerun with visible mode:

```powershell
mediause use account huggingface:guest --show --json
```

Risk reduction note:

- `--show` usually lowers repeated anti-bot interception risk in challenged sessions.

## 4. Hugging Face Dynamic Command Map (v1)

Source manifest:

- plugin: `plugin.huggingface`
- file: `crates/platforms/plugins/huggingface/manifest.yaml`

### 4.1 account.*

- `mediause huggingface account health --json`

### 4.2 get.top

Top upvoted Hugging Face papers.

```powershell
mediause huggingface get top [--limit <n>] [--all <bool>] [--date <YYYY-MM-DD>] [--period <daily|weekly|monthly>] --json
```

Notes:

- `--period` default is `daily`
- `--date` is for daily mode
- `--all true` ignores limit and returns full ranked set

### 4.3 get.models

Top Hugging Face models.

```powershell
mediause huggingface get models [--sort <downloads|likes|trending|created_at|last_modified>] [--search <text>] [--pipeline <tag>] [--limit <n>] --json
```

### 4.4 get.datasets

Top Hugging Face datasets.

```powershell
mediause huggingface get datasets [--sort <downloads|likes|trending|created_at|last_modified>] [--search <text>] [--limit <n>] --json
```

### 4.5 get.spaces

Top Hugging Face spaces.

```powershell
mediause huggingface get spaces [--sort <likes|created_at|last_modified>] [--search <text>] [--sdk <gradio|streamlit|docker|static>] [--limit <n>] --json
```

### 4.6 get.paper

Hugging Face paper detail by arXiv id.

```powershell
mediause huggingface get paper --id <arxiv_id> --json
```

Example ids:

- `1706.03762`
- `2401.06196`

## 5. Workflow Examples

### 5.1 Daily paper scan

```powershell
mediause plugin add huggingface --json
mediause use account huggingface:guest --json
mediause huggingface get top --period daily --limit 20 --json
mediause trace last --json
```

### 5.2 Weekly leaderboard and model follow-up

```powershell
mediause use account huggingface:guest --json
mediause huggingface get top --period weekly --limit 50 --json
mediause huggingface get models --sort downloads --search llama --limit 20 --json
mediause trace last --json
```

### 5.3 Dataset and space discovery

```powershell
mediause use account huggingface:guest --json
mediause huggingface get datasets --sort likes --search multilingual --limit 20 --json
mediause huggingface get spaces --sort likes --sdk gradio --limit 20 --json
mediause trace last --json
```

### 5.4 Paper deep read

```powershell
mediause use account huggingface:guest --json
mediause huggingface get paper --id 1706.03762 --json
mediause trace last --json
```

## 6. Operational Constraints (Mandatory)

### 6.1 Read-only and guest-only

- This plugin flow is read-only.
- Use `huggingface:guest` only.
- Do not attempt write actions or login flow for this plugin.

### 6.2 Frequency limits and spacing

Suggested limits:

- `get top/models/datasets/spaces`: <= 60 calls per minute
- `get paper`: <= 30 calls per minute

Minimum spacing:

- list/ranking calls: >= 1 second between calls
- single paper detail calls: >= 2 seconds between calls

If throttled or blocked:

1. Pause 30-60 seconds.
2. Retry with lower call frequency.
3. Re-bind guest context with `--show` if challenge is present.

### 6.3 Safety policy

- Do not bypass anti-bot or platform protections.
- Do not scrape credentials or session secrets.
- Respect Hugging Face usage policies and local regulations.

### 6.4 Output and error handling

- Prefer `--json` output for automation.
- Keep stable machine-readable handling for errors.
- On HTTP 429 or challenge pages, stop and retry with cooldown.

## 7. Execution Checklist

Before run:

Before every run, execute the install script once.

1. CLI installed via `npm install -g @mediause/cli` on Windows.
2. PATH updated and `mediause --version` works.
3. API key configured.
4. Plugin installed and help output verified.
5. Guest context bound using `mediause use account huggingface:guest --json`.

During run:

1. Use only read commands listed in this skill.
2. Keep request spacing and avoid burst loops.
3. Use `--show` only when challenge handling is needed.

After run:

1. Save outputs/logs.
2. Record retry/cooldown events.
3. Keep traffic conservative for repeated polling jobs.

## 8. Quick Command Reference

```powershell
# always run once before each workflow (auto-upgrade latest)
mediause --version
mediause --version

# discover
mediause plugin list --json
mediause plugin add huggingface --json
mediause huggingface -h
mediause huggingface get -h

# guest context
mediause use account huggingface:guest --json

# actions
mediause huggingface account health --json
mediause huggingface get top --period daily --limit 20 --json
mediause huggingface get models --sort downloads --limit 20 --json
mediause huggingface get datasets --sort likes --limit 20 --json
mediause huggingface get spaces --sort likes --limit 20 --json
mediause huggingface get paper --id 1706.03762 --json

# trace
mediause trace last --json
```

Skill Metadata
Maintainer: @mediause-demo
Last-Updated: 2026-08-22
Version: v2




