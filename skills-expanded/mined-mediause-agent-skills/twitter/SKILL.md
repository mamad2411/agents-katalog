---
name: twitter
description: Standardized Twitter/X skill for MediaUse. Includes Windows install, key onboarding, strict context/auth flow, full Twitter/X dynamic command map, and safety/rate controls.
---

# MediaUse Twitter X Skill

Run Twitter/X read and write workflows in MediaUse with consistent setup, context binding, command routing, and safe pacing controls.

## Scope

Use this skill when the task targets Twitter/X operations such as:

- Account: health checks
- Search: post search and trending topics
- User: profile, feed, followers, following, likes
- Get: timeline, bookmarks, notifications
- List: list feed, list tweets, add/remove list members
- Post: publish and reply
- Engage: like, bookmark, follow, unfollow, unbookmark
- Moderate: delete, hide-reply, block, unblock
- Message: accept DM requests and send replies

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

- .mediause/skills/twitter/SKILL.md

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

First step on every run: execute install script once to auto-install or auto-upgrade the latest MediaUse CLI.

1. Discover site and commands.
2. Bind account context with use account.
3. Check status with auth health.
4. Execute dynamic site actions.
5. Verify with trace or task.

### 3.1 Discover and plugin setup

```powershell
mediause plugin list --json
mediause plugin add twitter --json
```

### 3.2 Bind context before any read or write

use account must be executed successfully before any read or write action.

use account argument format:

- <platform:account_id>
- account_id should be selected from mediause auth list --json.

```powershell
mediause auth list --json
mediause use account twitter:<account_id> --policy balanced --json
```

If challenge or risk prompts appear, reopen in visible mode:

```powershell
mediause use account twitter:<account_id> --policy balanced --show --json
```

### 3.3 Auth health precondition

auth health is valid only after successful use account.

```powershell
mediause auth health --json
```

If auth health indicates not logged in or expired:

```powershell
mediause auth login twitter --json
mediause use account twitter:<account_id> --policy balanced --json
mediause auth health --json
```

### 3.4 Guest mode

The manifest default account is guest, so guest context can be selected when your runtime supports it.

```powershell
mediause use account twitter:guest --json
```

Guest mode guardrails:

- Treat as read-only by default.
- Block all write actions such as post, engage, moderate, message, or list member changes unless switched to a logged-in account.

## 4. Twitter X Dynamic Command Map v1

Source schema:

- plugin: plugin.twitter
- schema Version: v2

### 4.1 account commands

- mediause twitter account health --json

### 4.2 search commands

- mediause twitter search posts --query <query> [--filter <top|latest|people|media>] [--limit <n>] --json
- mediause twitter search trending [--limit <n>] --json

### 4.3 user commands

- mediause twitter user profile --username <username> --json
- mediause twitter user feed --username <username> [--limit <n>] --json
- mediause twitter user followers --username <username> [--limit <n>] --json
- mediause twitter user following --username <username> [--limit <n>] --json
- mediause twitter user likes --username <username> [--limit <n>] --json

### 4.4 get commands

- mediause twitter get timeline [--type <for-you|following>] [--limit <n>] --json
- mediause twitter get bookmarks [--limit <n>] --json
- mediause twitter get notifications [--limit <n>] --json

### 4.5 list commands

- mediause twitter list feed [--limit <n>] --json
- mediause twitter list tweets --list_id <list_id> [--limit <n>] --json
- mediause twitter list add --list_id <list_id> --username <username> --json
- mediause twitter list remove --list_id <list_id> --username <username> --json

### 4.6 post commands

- mediause twitter post feed --text <text> --json
- mediause twitter post reply --url <tweet_url> --text <text> --json

### 4.7 engage commands

- mediause twitter engage like --url <tweet_url> --json
- mediause twitter engage bookmark --url <tweet_url> --json
- mediause twitter engage follow --username <username> --json
- mediause twitter engage unfollow --username <username> --json
- mediause twitter engage unbookmark --url <tweet_url> --json

### 4.8 moderate commands

- mediause twitter moderate delete --url <tweet_url> --json
- mediause twitter moderate hide-reply --url <tweet_url> --json
- mediause twitter moderate block --username <username> --json
- mediause twitter moderate unblock --username <username> --json

### 4.9 message commands

- mediause twitter message accept --query <query> [--max <n>] --json
- mediause twitter message reply --text <text> [--max <n>] [--skip_replied <true|false>] --json

## 5. Operational Constraints Mandatory

Apply these constraints for all actions to reduce account risk and keep behavior human-like.

### 5.1 Human-like pacing

- Never execute high-risk actions continuously.
- Add randomized delay between actions.
- Add longer cooldown after publish, moderation, and message actions.
- Mix read actions between write actions when possible.

### 5.2 Frequency limits and minimum spacing

Suggested limits:

- Publish actions: <= 3 per hour
- Reply and message actions: <= 20 per hour
- Follow, like, bookmark actions: <= 30 per hour
- Search and read actions: <= 60 per minute

Minimum spacing:

- Post operations: >= 20 minutes between actions
- Reply and message operations: >= 30 seconds between actions
- Engage operations: >= 10 seconds between actions
- Read and search operations: >= 1 second between actions

Same-target guardrails:

- Repeated interaction on same target: >= 60 seconds
- Repeated identical publish text: >= 24 hours default deny

If a limit is hit:

1. Pause at least 15 minutes.
2. Resume with read-only actions first.
3. Re-check session health before any write action.

### 5.3 Safety policy

- Do not bypass platform protections.
- Do not attempt credential scraping or session hijacking.
- Respect platform terms and local regulations.

### 5.4 Output and error handling

- Prefer --json output for machine workflows.
- Require structured error handling with stable fields or code when available.
- On blocked, rate-limit, risk prompt, or challenge pages, stop and return actionable next steps.

## 6. Workflow Examples

### 6.1 Discover to publish workflow

```powershell
mediause use account twitter:<account_id> --json
mediause auth health --json
mediause twitter search trending --limit 10 --json
mediause twitter post feed --text "Daily update" --json
mediause trace last --json
```

### 6.2 Monitoring and engagement workflow

```powershell
mediause use account twitter:<account_id> --json
mediause auth health --json
mediause twitter get notifications --limit 20 --json
mediause twitter engage like --url <tweet_url> --json
mediause twitter engage follow --username <username> --json
mediause trace last --json
```

### 6.3 Moderation workflow

```powershell
mediause use account twitter:<account_id> --json
mediause auth health --json
mediause twitter moderate hide-reply --url <tweet_url> --json
mediause twitter moderate block --username <username> --json
mediause trace last --json
```

### 6.4 Guest read-only workflow

```powershell
mediause use account twitter:guest --json
mediause twitter search posts --query "ai" --limit 10 --json
mediause twitter get timeline --type for-you --limit 20 --json
mediause trace last --json
```

## 7. Minimal Validation Checklist

Before run:

1. CLI installed and available in PATH; verify with mediause --version on Windows.
2. PATH updated and mediause --version works.
3. API key configured.
4. Account context bound via mediause use account <platform:account_id>.
5. mediause auth health --json checked after context bind.

During run:

1. Respect pacing and cooldown constraints.
2. Stop on anti-bot or risk prompts.
3. Keep write actions conservative.

After run:

1. Confirm result structure is parseable JSON.
2. Check trace output for diagnostics.
3. Record warnings and cooldown events.

## 8. Quick Command Reference

```powershell
# always run once before each workflow auto-upgrade latest
mediause --version
mediause --version

# discover
mediause plugin list --json
mediause plugin add twitter --json

# context and status
mediause auth list --json
mediause use account twitter:<account_id> --json
mediause auth health --json

# read actions
mediause twitter search posts --query "openai" --limit 5 --json
mediause twitter get timeline --type for-you --limit 10 --json
mediause twitter user profile --username openai --json

# write actions
mediause twitter post feed --text "hello" --json
mediause twitter engage like --url <tweet_url> --json

# trace
mediause trace last --json
```

Skill Metadata
Maintainer: @mediause-demo
Last-Updated: 2026-08-22
Version: v2


