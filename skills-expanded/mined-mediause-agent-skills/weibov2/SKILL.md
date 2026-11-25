---
name: weibov2
description: Standardized weibov2 skill for MediaUse. Includes Windows install, key onboarding, strict context/auth flow, full weibov2 dynamic command map, and safety/rate controls.
---

# MediaUse weibov2 Skill

Execute weibov2 social workflows with guided auth context, dynamic command routing, and safe pacing controls.

## Scope

Use this skill when the task targets weibov2 operations such as:

- Publish: feed, repost
- Read: feed, detail, notifications
- User: profile, profile update, user feed, followers, following
- Reply: comment, sub-comment, private message
- Search: text, user, hot topics
- Engage: like, follow, collect

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

- .mediause/skills/weibov2/SKILL.md

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
3. Check status with `auth health`.
4. Execute dynamic site actions.
5. Verify with trace/task.

### 3.1 Discover and plugin setup

```powershell
mediause plugin list --json
mediause plugin add weibov2 --json
mediause weibov2 -h
mediause weibov2 post -h
```

### 3.2 Bind context before any read/write

`use account` must be executed successfully before any fetch/publish action.

`use account` argument format:

- `<platform:account_id>`
- `account_id` should be selected from `mediause auth list --json`.

```powershell
mediause auth list --json
mediause use account weibov2:<account_id> --policy balanced --json
```

If challenge/risk prompts appear, reopen in visible mode:

```powershell
mediause use account weibov2:<account_id> --policy balanced --show --json
```

`--show` usually lowers repeated interception risk in challenged sessions.

### 3.3 Auth health precondition

`auth health` is valid only after successful `use account`.

```powershell
mediause auth health --json
```

If `auth health` indicates not logged in/expired:

```powershell
mediause auth login weibov2 --json
mediause use account weibov2:<account_id> --policy balanced --json
mediause auth health --json
```

### 3.4 Guest mode (optional, site-dependent)

If guest mode is supported by the current CLI/site runtime:

```powershell
mediause use account weibov2:guest --json
```

Guest mode rules:

- Read-only (fetch/search/get/user read operations).
- Block all write operations (post/reply/engage write intent).
- If write is required, switch to logged-in account context.

## 4. weibov2 Dynamic Command Map (v1)

Source schema:

- plugin: `plugin.weibov2`
- schema version: `v1`
- supported layer: `L3Bridge`

### 4.1 post.*

- `mediause weibov2 post feed [--title <text>] [--text <text>] [--media <paths>] --json`
- `mediause weibov2 post repost --id <post_id> [--text <text>] --json`

### 4.2 get.*

- `mediause weibov2 get feed [--limit <n>] [--type <type>] --json`
- `mediause weibov2 get detail --id <item_id> [--comments <bool>] --json`
- `mediause weibov2 get notif [--type <type>] --json`

### 4.3 user.*

- `mediause weibov2 user profile [--me <bool>] [--user-id <uid>] --json`
- `mediause weibov2 user profile-update [--bio <text>] [--name <text>] [--avatar <path>] --json`
- `mediause weibov2 user feed --user-id <uid> [--limit <n>] [--type <type>] --json`
- `mediause weibov2 user followers --user-id <uid> [--limit <n>] --json`
- `mediause weibov2 user following --user-id <uid> [--limit <n>] --json`

### 4.4 reply.*

- `mediause weibov2 reply comment --post-id <post_id> --text <text> --json`
- `mediause weibov2 reply sub --comment-id <comment_id> --text <text> --json`
- `mediause weibov2 reply message --user-id <uid> --text <text> --json`

### 4.5 search.*

- `mediause weibov2 search text --keyword <keyword> [--limit <n>] --json`
- `mediause weibov2 search user --query <query> [--limit <n>] --json`
- `mediause weibov2 search hot --json`

### 4.6 engage.*

- `mediause weibov2 engage like --id <item_id> [--type <type>] --json`
- `mediause weibov2 engage follow --user-id <uid> [--undo <bool>] --json`
- `mediause weibov2 engage collect --id <item_id> --json`

## 5. Operational Constraints (Mandatory)

Apply these constraints for all actions to reduce account risk and keep behavior human-like.

### 5.1 Human-like pacing

- Never execute high-risk actions continuously.
- Add randomized delay between actions.
- Add longer cooldown after publish/profile-change actions.
- Mix read actions between write actions when possible.

### 5.2 Frequency limits and minimum spacing

- Hard stop if operation rate is abnormally high.
- Stop immediately on repeated anti-bot challenge, login re-validation, or risk prompt.
- Do not run burst publish loops.

Suggested limits:

- Publish: <= 3 per hour
- Reply/message: <= 20 per hour
- Follow/like/collect: <= 30 per hour
- Search/read: <= 60 per minute

Minimum spacing:

- Publish (post): >= 20 minutes between actions
- Reply/message: >= 30 seconds between actions
- Follow/like/collect: >= 10 seconds between actions
- Read/search/get/user read: >= 1 second between actions

Same-target guardrails:

- Repeated interaction on same target (same post_id/user_id): >= 60 seconds
- Repeated identical publish text: >= 24 hours (default deny)

Suggested soft limits per account 10-minute window:

- High-risk actions: <= 3 in 10 minutes
- Medium-risk actions: <= 8 in 10 minutes
- Low-risk actions: <= 20 in 10 minutes

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

### 6.1 Hot-topic to publish

```powershell
mediause use account weibov2:<account_id> --json
mediause auth health --json
mediause weibov2 search hot --json
mediause weibov2 post feed --text "<draft_text>" --media c:/tmp/a.png --json
mediause trace last --json
```

### 6.2 Monitor and engage

```powershell
mediause use account weibov2:<account_id> --json
mediause auth health --json
mediause weibov2 get notif --type mention --json
mediause weibov2 reply comment --post-id <id> --text "received" --json
mediause trace last --json
```

### 6.3 Read-only guest branch (if supported)

```powershell
mediause use account weibov2:guest --json
mediause weibov2 search hot --json
mediause weibov2 get feed --limit 20 --json
mediause trace last --json
```

## 7. Execution Checklist

Before run:

Before every run, execute the install script once.

1. CLI installed via `npm install -g @mediause/cli` on Windows.
2. PATH updated and `mediause --version` works.
3. API key configured and verified.
4. Account context bound via `mediause use account <platform:account_id>`.
5. `mediause auth health --json` checked after context bind.
6. If not logged in, run `mediause auth login weibov2 --json` and re-bind context.
7. Pacing policy is enabled.

During run:

1. Respect risk-based delays and minimum spacing.
2. Stop on anti-bot/risk prompts.
3. Avoid repetitive write-action bursts.
4. In guest mode, allow read-only actions only.

After run:

1. Save logs and outcomes.
2. Record any risk warning and cooldown events.
3. Keep account activity under conservative limits.

## 8. Quick Command Reference

```powershell
# always run once before each workflow (auto-upgrade latest)
mediause --version
mediause --version

# discover
mediause plugin list --json
mediause plugin add weibov2 --json
mediause weibov2 -h
mediause weibov2 post -h

# context + status
mediause auth list --json
mediause use account weibov2:<account_id> --json
mediause auth health --json

# read action
mediause weibov2 search hot --json

# write action
mediause weibov2 post feed --text "hello" --json

# trace
mediause trace last --json
```

Skill Metadata
Maintainer: @mediause-demo
Last-Updated: 2026-08-22
Version: v2


