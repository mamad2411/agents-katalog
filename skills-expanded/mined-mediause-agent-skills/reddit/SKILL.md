---
name: reddit
description: Standardized Reddit skill for MediaUse. Includes Windows install, key onboarding, strict context/auth flow, full Reddit dynamic command map, and safety/rate controls.
---

# MediaUse Reddit Skill

Handle Reddit monitoring and interaction with standardized flows for feeds, search, thread reads, profile views, and engagement actions.

## Scope

Use this skill when the task targets Reddit operations such as:

- Account: health check
- Get: hot, popular, frontpage, subreddit feed
- Search: posts
- Read: item thread and comments
- User: profile, posts, comments
- Collection: saved, upvoted
- Engage: comment, save, upvote, subscribe

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

- .mediause/skills/reddit/SKILL.md

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

## 3. Core Flow (Mandatory Order)

Always follow this order:

First step on every run: execute install script once to auto-install/auto-upgrade the latest MediaUse CLI.

1. Discover site and commands.
2. Bind account context with `use account --show`.
3. Check status with `auth health`.
4. Execute dynamic site actions.
5. Verify with trace/task.

### 3.1 Discover and plugin setup

```powershell
mediause plugin list --json
mediause plugin add reddit --json
mediause reddit -h
mediause reddit get -h
```

### 3.2 Bind context before any read/write (show required)

`use account` must be executed successfully before any fetch/publish action.

`use account` argument format:

- `<platform:account_id>`
- `account_id` should be selected from `mediause auth list --json`.

For Reddit skill, always use visible mode with `--show`.

Reason:

- `--show` usually lowers repeated anti-bot/challenge interception risk for Reddit flows.

```powershell
mediause auth list --json
mediause use account reddit:<account_id> --policy balanced --show --json
```

### 3.3 Auth health precondition

`auth health` is valid only after successful `use account`.

```powershell
mediause auth health --json
```

If `auth health` indicates not logged in/expired:

```powershell
mediause auth login reddit --json
mediause use account reddit:<account_id> --policy balanced --show --json
mediause auth health --json
```

If page shows `unusual traffic`, captcha, or risk confirmation:

```powershell
mediause use account reddit:<account_id> --policy balanced --show --json
```

Complete verification manually, then rerun the action.

### 3.4 Guest mode (optional)

Manifest default account id is `guest`. Guest mode can be used only for read-only actions when the runtime supports unauthenticated `reddit:guest` context (that is, `mediause use account reddit:guest --show --json` succeeds):

```powershell
mediause use account reddit:guest --show --json
```

Guest mode rules:

- Read-only operations (`account/get/search/read/user/collection` fetch intents).
- Block write operations (`engage.comment`, `engage.save`, `engage.upvote`, `engage.subscribe`).
- If write is required, switch to a logged-in account context.

## 4. Reddit Dynamic Command Map (v1)

Source schema:

- plugin: `plugin.reddit`
- manifest: `crates/platforms/plugins/reddit/manifest.yaml`

### 4.1 account.*

- `mediause reddit account health --json`

### 4.2 get.*

- `mediause reddit get hot [--subreddit <name>] [--limit <n>] --json`
- `mediause reddit get popular [--limit <n>] --json`
- `mediause reddit get frontpage [--limit <n>] --json`
- `mediause reddit get subreddit --name <subreddit> [--sort <sort>] [--time <time>] [--limit <n>] --json`

### 4.3 search.*

- `mediause reddit search posts --query <query> [--subreddit <name>] [--sort <sort>] [--time <time>] [--limit <n>] --json`

### 4.4 read.*

- `mediause reddit read item --post-id <post_id> [--sort <sort>] [--limit <n>] [--depth <n>] [--replies <n>] [--max-length <n>] --json`

### 4.5 user.*

- `mediause reddit user profile --username <username> --json`
- `mediause reddit user posts --username <username> [--limit <n>] --json`
- `mediause reddit user comments --username <username> [--limit <n>] --json`

### 4.6 collection.*

- `mediause reddit collection saved [--limit <n>] --json`
- `mediause reddit collection upvoted [--limit <n>] --json`

### 4.7 engage.*

- `mediause reddit engage comment --post-id <post_id> --text <text> --json`
- `mediause reddit engage save --post-id <post_id> [--undo <bool>] --json`
- `mediause reddit engage upvote --post-id <post_id> [--direction <up|down|none>] --json`
- `mediause reddit engage subscribe --subreddit <name> [--undo <bool>] --json`

## 5. Operational Constraints (Mandatory)

Apply these constraints for all actions to reduce account risk and keep behavior human-like.

### 5.1 Human-like pacing

- Never execute high-risk actions continuously.
- Add randomized delay between actions.
- Add longer cooldown after write actions.
- Mix read actions between write actions when possible.

### 5.2 Frequency limits and minimum spacing

- Hard stop if operation rate is abnormally high.
- Stop immediately on repeated anti-bot challenge, login re-validation, or risk prompt.
- Do not run burst comment/upvote loops.

Quick policy matrix:

- `engage.comment`: <= 30/hour, >= 30s spacing
- `engage.save` / `engage.upvote` / `engage.subscribe`: <= 30/hour, >= 10s spacing
- `search/get/read/user/collection`: <= 60/min, >= 1s spacing
- same target (`post_id` / subreddit): >= 60s between repeated interactions
- same comment text: >= 24h (default deny)

If a limit is hit:

1. Pause at least 15 minutes.
2. Resume with read-only actions first.
3. Re-check session health before any write action.

### 5.3 Safety policy

- Do not bypass platform protections.
- Do not attempt credential scraping or session hijacking.
- Respect platform terms and local regulations.

### 5.4 Output and error handling

- Prefer `--json` output for machine workflows.
- Require structured error handling with stable fields/code when available.
- On blocked/rate-limit/risk prompt, stop and return actionable next steps.

## 6. Workflow Examples

### 6.1 Discovery and thread reading

```powershell
mediause use account reddit:<account_id> --show --json
mediause auth health --json
mediause reddit get popular --limit 20 --json
mediause reddit read item --post-id <post_id> --limit 30 --depth 3 --json
mediause trace last --json
```

### 6.2 Subreddit monitoring

```powershell
mediause use account reddit:<account_id> --show --json
mediause auth health --json
mediause reddit get subreddit --name "rust" --sort new --limit 20 --json
mediause reddit search posts --query "async" --subreddit "rust" --limit 10 --json
mediause trace last --json
```

### 6.3 Engagement workflow

```powershell
mediause use account reddit:<account_id> --show --json
mediause auth health --json
mediause reddit engage upvote --post-id <post_id> --direction up --json
mediause reddit engage comment --post-id <post_id> --text "Thanks for sharing" --json
mediause trace last --json
```

## 7. Execution Checklist

Before run:

Before every run, execute the install script once.

1. CLI installed via `npm install -g @mediause/cli` on Windows.
2. PATH updated and `mediause --version` works.
3. API key configured and verified.
4. Account context bound via `mediause use account reddit:<account_id> --show --json`.
5. If write actions are required, ensure logged-in account context is active.
6. Be ready to complete manual verification in the visible browser.
7. Pacing policy is enabled.

During run:

1. Respect delays and minimum spacing.
2. Stop on anti-bot/risk prompts.
3. Avoid repetitive burst loops.

After run:

1. Save logs and outcomes.
2. Record any risk warning and cooldown events.
3. Keep activity under conservative limits.

## 8. Quick Command Reference

```powershell
# always run once before each workflow (auto-upgrade latest)
mediause --version
mediause --version

# discover
mediause plugin list --json
mediause plugin add reddit --json
mediause reddit -h
mediause reddit get -h

# context + status (show required)
mediause auth list --json
mediause use account reddit:<account_id> --show --json
mediause auth health --json

# read actions
mediause reddit account health --json
mediause reddit get hot --subreddit "technology" --limit 20 --json
mediause reddit get popular --limit 20 --json
mediause reddit search posts --query "browser automation" --limit 10 --json
mediause reddit read item --post-id <post_id> --limit 20 --json
mediause reddit user profile --username <username> --json
mediause reddit collection saved --limit 20 --json

# write actions
mediause reddit engage upvote --post-id <post_id> --direction up --json
mediause reddit engage save --post-id <post_id> --json
mediause reddit engage subscribe --subreddit "technology" --json
mediause reddit engage comment --post-id <post_id> --text "Nice thread" --json

# trace
mediause trace last --json
```

Skill Metadata
Maintainer: @mediause-demo
Last-Updated: 2026-08-22
Version: v2




