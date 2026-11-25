---
name: weixin
description: Standardized Weixin Official Account skill for MediaUse. Includes Windows install, key onboarding, strict context/auth flow, full weixin dynamic command map, and safety/rate controls.
---

# MediaUse Weixin Skill

Run WeChat Official Account workflows in MediaUse with consistent setup, context binding, command routing, and safe pacing controls.

## Scope

Use this skill when the task targets Weixin Official Account operations such as:

- Account: health checks
- Search: article search via Sogou Weixin
- Get: drafts list and article extraction
- Post: create article draft

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

- .mediause/skills/weixin/SKILL.md

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
mediause plugin add weixin --json
```

### 3.2 Bind context before any read or write

use account must be executed successfully before any fetch or publish action.

use account argument format:

- <platform:account_id>
- account_id should be selected from mediause auth list --json.

```powershell
mediause auth list --json
mediause use account weixin:<account_id> --policy balanced --json
```

If challenge or risk prompts appear, reopen in visible mode:

```powershell
mediause use account weixin:<account_id> --policy balanced --show --json
```

### 3.3 Auth health precondition

auth health is valid only after successful use account.

```powershell
mediause auth health --json
```

If auth health indicates not logged in or expired:

```powershell
mediause auth login weixin --json
mediause use account weixin:<account_id> --policy balanced --json
mediause auth health --json
```

### 3.4 Guest mode

The manifest default account is guest, so guest context can be selected when your runtime supports it.

```powershell
mediause use account weixin:guest --json
```

Guest mode guardrails:

- Treat as read-only by default.
- Block all write actions such as post.create-draft unless switched to a logged-in account.

## 4. Weixin Dynamic Command Map (v1)

Source schema:

- plugin: plugin.weixin
- schema Version: v2

### 4.1 account.*

- mediause weixin account health --json

### 4.2 search.*

- mediause weixin search articles --query <query> [--page <n>] [--limit <n>] --json

### 4.3 get.*

- mediause weixin get drafts [--limit <n>] --json
- mediause weixin get article --url <url> --json

PowerShell URL note:

- Always wrap URL in single quotes when it contains &.

```powershell
mediause weixin get article --url 'https://weixin.sogou.com/link?...&type=2&query=codex' --json
```

### 4.4 post.*

- mediause weixin post create-draft --title <title> --content <content> [--author <name>] [--summary <text>] [--cover_image <path>] --json

## 5. Operational Constraints (Mandatory)

Apply these constraints for all actions to reduce account risk and keep behavior human-like.

### 5.1 Human-like pacing

- Never execute high-risk actions continuously.
- Add randomized delay between actions.
- Add longer cooldown after draft creation actions.
- Mix read actions between write actions when possible.

### 5.2 Frequency limits and minimum spacing

Suggested limits:

- Publish or draft actions: <= 3 per hour
- Reply or message-like actions: <= 20 per hour
- Follow or like-like actions: <= 30 per hour
- Search or read actions: <= 60 per minute

Minimum spacing:

- Post operations: >= 20 minutes between actions
- Reply or message operations: >= 30 seconds between actions
- Engage operations: >= 10 seconds between actions
- Read or search operations: >= 1 second between actions

Same-target guardrails:

- Repeated interaction on same target: >= 60 seconds
- Repeated identical publish text: >= 24 hours (default deny)

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
- On blocked, rate-limit, risk prompt, or captcha pages, stop and return actionable next steps.

## 6. Workflow Examples

### 6.1 Read workflow: article discovery to extraction

```powershell
mediause use account weixin:<account_id> --json
mediause auth health --json
mediause weixin search articles --query "codex" --page 1 --limit 5 --json
mediause weixin get article --url 'https://weixin.sogou.com/link?...&type=2&query=codex' --json
mediause trace last --json
```

### 6.2 Write workflow: create draft from prepared content

```powershell
mediause use account weixin:<account_id> --json
mediause auth health --json
mediause weixin post create-draft --title "Weekly Update" --content "Main content body" --author "Ops Team" --summary "Short digest" --json
mediause trace last --json
```

### 6.3 Guest workflow (read-only)

```powershell
mediause use account weixin:guest --json
mediause weixin search articles --query "ai" --limit 10 --json
mediause weixin get article --url 'https://weixin.sogou.com/link?...' --json
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
# always run once before each workflow (auto-upgrade latest)
mediause --version
mediause --version

# discover
mediause plugin list --json
mediause plugin add weixin --json

# context + status
mediause auth list --json
mediause use account weixin:<account_id> --json
mediause auth health --json

# read actions
mediause weixin search articles --query "ai" --limit 5 --json
mediause weixin get drafts --limit 10 --json
mediause weixin get article --url 'https://weixin.sogou.com/link?...&type=2&query=ai' --json

# write action
mediause weixin post create-draft --title "t" --content "c" --json

# trace
mediause trace last --json
```

Skill Metadata
Maintainer: @mediause-demo
Last-Updated: 2026-08-22
Version: v2


