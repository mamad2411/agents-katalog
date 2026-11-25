---
name: bloomberg
description: Standardized Bloomberg skill for MediaUse. Includes Windows install, key onboarding, strict context/auth flow, full Bloomberg dynamic command map, and safety/rate controls.
---

# MediaUse Bloomberg Skill

Use this skill to read Bloomberg RSS feeds and parse Bloomberg article pages with a consistent MediaUse workflow.

## Scope

Use this skill when tasks target Bloomberg operations such as:

- Account: plugin health
- Feeds: list available RSS aliases
- Get: category top stories (`main`, `markets`, `economics`, `industries`, `tech`, `politics`, `businessweek`, `opinions`)
- Read: parse a Bloomberg article by URL (`read news`)

Bloomberg skill is read-focused. No publish/reply/engage write actions are defined.

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

- .mediause/skills/bloomberg/SKILL.md

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
2. Bind account context with `use account`.
3. Check status with `auth health` (for non-guest account).
4. Execute dynamic site actions.
5. Verify with trace/task.

### 3.1 Discover and plugin setup

```powershell
mediause plugin list --json
mediause plugin add bloomberg --json
mediause bloomberg -h
mediause bloomberg get -h
mediause bloomberg read -h
mediause bloomberg feeds -h
```

### 3.2 Bind context before any action

`use account` must succeed before `get/read/feeds` operations.

`use account` argument format:

- `<platform:account_id>`
- `account_id` should be selected from `mediause auth list --json`.

Bloomberg supports guest read mode in common cases:

```powershell
mediause auth list --json
mediause use account bloomberg:guest --policy balanced --json
```

### 3.3 Auth health precondition

`auth health` is valid only after successful `use account`.

For non-guest account:

```powershell
mediause auth health --json
```

If `auth health` indicates not logged in/expired:

```powershell
mediause auth login bloomberg --json
mediause use account bloomberg:<account_id> --policy balanced --json
mediause auth health --json
```

Guest mode notes:

- Prefer `bloomberg:guest` for read-only workflows.
- If bot checks or unusual traffic appear, reopen with visible browser for manual verification:

```powershell
mediause use account bloomberg:guest --policy balanced --show --json
```

Risk reduction note:

- A visible `--show` session often lowers repeated anti-bot/challenge interception risk.

## 4. Bloomberg Dynamic Command Map (v1)

Source schema:

- plugin: `plugin.bloomberg`
- manifest capability tree: `account`, `feeds`, `get`, `read`

### 4.1 account.health

```powershell
mediause bloomberg account health --json
```

### 4.2 feeds.list

List supported Bloomberg RSS aliases:

```powershell
mediause bloomberg feeds list --json
```

Expected aliases include:

- `main`
- `markets`
- `economics`
- `industries`
- `tech`
- `politics`
- `businessweek`
- `opinions`

### 4.3 get.* (RSS top stories)

All get actions support:

- `--limit <n>` (optional)

Commands:

```powershell
mediause bloomberg get main --limit 10 --json
mediause bloomberg get markets --limit 10 --json
mediause bloomberg get economics --limit 10 --json
mediause bloomberg get industries --limit 10 --json
mediause bloomberg get tech --limit 10 --json
mediause bloomberg get politics --limit 10 --json
mediause bloomberg get businessweek --limit 10 --json
mediause bloomberg get opinions --limit 10 --json
```

### 4.4 read.news

Read and parse a Bloomberg article page:

```powershell
mediause bloomberg read news --link "https://www.bloomberg.com/news/articles/..." --json
```

Parameters:

- `--link` (required): full Bloomberg article URL, or Bloomberg path resolvable by runtime

## 5. Workflow Examples

### 5.1 Daily macro monitoring

```powershell
mediause use account bloomberg:guest --json
mediause bloomberg get economics --limit 20 --json
mediause bloomberg get markets --limit 20 --json
mediause trace last --json
```

### 5.2 Category scan and article deep read

```powershell
mediause use account bloomberg:guest --json
mediause bloomberg get tech --limit 10 --json
mediause bloomberg read news --link "https://www.bloomberg.com/news/articles/<article-id>" --json
mediause trace last --json
```

### 5.3 Feed alias discovery then selective retrieval

```powershell
mediause use account bloomberg:guest --json
mediause bloomberg feeds list --json
mediause bloomberg get opinions --limit 10 --json
mediause trace last --json
```

## 6. Operational Constraints (Mandatory)

### 6.1 Read-only boundaries

Bloomberg skill command map is read-focused. Do not invent publish/reply/engage actions.

### 6.2 Frequency and pacing

Suggested limits:

- `get.*`: <= 60 calls per minute
- `read.news`: <= 20 calls per minute
- `feeds.list` / `account.health`: <= 20 calls per minute

Minimum spacing:

- `get.*`: >= 1 second
- `read.news`: >= 2 seconds
- `feeds.list` / `account.health`: >= 1 second

Same-target guardrail:

- Re-read same article URL: >= 10 seconds

If anti-bot, challenge page, or unusual traffic appears:

1. Stop burst requests.
2. Rebind context with `--show` and resolve manually.
3. Resume at reduced frequency.

### 6.3 Compliance

- Respect Bloomberg access controls and terms.
- Do not attempt bypass of paywall, bot checks, or authentication controls.
- Do not perform credential/session scraping.

### 6.4 Error handling

Always prefer `--json` output and inspect structured error fields.

Common recoverable patterns:

- `bloomberg.get.failed`: usually feed fetch/network/challenge issue
- `bloomberg.get.empty`: feed returned no parseable items
- `bloomberg.read.parse_failed`: page structure or access state mismatch
- `bloomberg.read.robot_page`: anti-bot/interstitial triggered

Recommended recovery sequence:

```powershell
mediause use account bloomberg:guest --show --json
mediause bloomberg account health --json
mediause bloomberg get main --limit 10 --json
mediause trace last --json
```

## 7. Quick Command Reference

```powershell
# discover
mediause plugin list --json
mediause plugin add bloomberg --json
mediause bloomberg -h

# context + status
mediause auth list --json
mediause use account bloomberg:guest --json
mediause auth health --json

# core actions
mediause bloomberg feeds list --json
mediause bloomberg get economics --limit 10 --json
mediause bloomberg read news --link "https://www.bloomberg.com/news/articles/<article-id>" --json

# trace
mediause trace last --json
```

Skill Metadata
Maintainer: @mediause-team
Last-Updated: 2026-08-22
Version: v2




