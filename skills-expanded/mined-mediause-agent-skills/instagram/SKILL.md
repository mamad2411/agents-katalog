---
name: instagram
description: Standardized Instagram skill for MediaUse. Includes Windows install, key onboarding, strict context/auth flow, full Instagram dynamic command map, and safety/rate controls.
---

# MediaUse Instagram Skill

Run Instagram read/write workflows in MediaUse with a consistent setup, context binding flow, command execution map, and safety pacing constraints.

## Scope

Use this skill when the task targets Instagram operations such as:

- Account: health checks
- Search: users
- Get: explore feed, saved items
- User: profile, feed, followers, following
- Engage: follow, unfollow, like, unlike, save, unsave, comment
- Collection: create, delete
- Post: note, feed, reel, story
- Download: media link resolution

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

- .mediause/skills/instagram/SKILL.md

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
mediause plugin add instagram --json
mediause instagram -h
mediause instagram post -h
```

### 3.2 Bind context before any read/write

`use account` must be executed successfully before any read/write action.

`use account` argument format:

- `<platform:account_id>`
- `account_id` should be selected from `mediause auth list --json`.

```powershell
mediause auth list --json
mediause use account instagram:<account_id> --policy balanced --json
```

If challenge/risk prompts appear, reopen in visible mode:

```powershell
mediause use account instagram:<account_id> --policy balanced --show --json
```

`--show` usually lowers repeated interception risk in challenged sessions.

### 3.3 Auth health precondition

`auth health` is valid only after successful `use account`.

```powershell
mediause auth health --json
```

If `auth health` indicates not logged in or expired:

```powershell
mediause auth login instagram --json
mediause use account instagram:<account_id> --policy balanced --json
mediause auth health --json
```

### 3.4 Guest mode

Instagram manifest currently includes `default_account_id: guest`, so guest context can be selected when your runtime supports it.

```powershell
mediause use account instagram:guest --json
```

Guest mode guardrails:

- Treat as read-only by default.
- Block all write actions (post/engage/collection write intent) unless you explicitly switch to a logged-in account.

## 4. Instagram Dynamic Command Map (v1)

Source schema:

- plugin: `plugin.instagram`
- schema version: `v1`

### 4.1 account.*

- `mediause instagram account health --json`

### 4.2 search.*

- `mediause instagram search users --query <query> [--limit <n>] --json`

### 4.3 get.*

- `mediause instagram get explore [--limit <n>] --json`
- `mediause instagram get saved [--limit <n>] [--collection <name>] --json`

### 4.4 user.*

- `mediause instagram user profile --username <username> --json`
- `mediause instagram user feed --username <username> [--limit <n>] --json`
- `mediause instagram user followers --username <username> [--limit <n>] --json`
- `mediause instagram user following --username <username> [--limit <n>] --json`

### 4.5 engage.*

- `mediause instagram engage follow --username <username> --json`
- `mediause instagram engage unfollow --username <username> --json`
- `mediause instagram engage like --username <username> [--index <n>] --json`
- `mediause instagram engage unlike --username <username> [--index <n>] --json`
- `mediause instagram engage save --username <username> [--index <n>] --json`
- `mediause instagram engage unsave --username <username> [--index <n>] --json`
- `mediause instagram engage comment --username <username> --text <text> [--index <n>] --json`

### 4.6 collection.*

- `mediause instagram collection create --name <name> --json`
- `mediause instagram collection delete --target <name_or_id> --json`

### 4.7 post.*

- `mediause instagram post note --content <text> --json`
- `mediause instagram post feed --media <path_or_paths> [--text <text>] --json`
- `mediause instagram post reel --video <path> [--text <text>] --json`
- `mediause instagram post story --media <path_or_paths> --json`

### 4.8 download.*

- `mediause instagram download media --url <instagram_url> --json`

## 5. Operational Constraints (Mandatory)

Apply these constraints for all actions to reduce account risk and keep behavior human-like.

### 5.1 Human-like pacing

- Never execute high-risk actions continuously.
- Add randomized delay between actions.
- Add longer cooldown after publish and profile-change actions.
- Mix read actions between write actions when possible.

### 5.2 Frequency limits and minimum spacing

Suggested limits:

- Publish actions: <= 3 per hour
- Reply/comment/message-like interactions: <= 20 per hour
- Follow/like/save actions: <= 30 per hour
- Search/read actions: <= 60 per minute

Minimum spacing:

- Publish (post): >= 20 minutes between actions
- Comment/reply: >= 30 seconds between actions
- Follow/like/save: >= 10 seconds between actions
- Read/search/get/user read: >= 1 second between actions

Same-target guardrails:

- Repeated interaction on the same target: >= 60 seconds
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

- Prefer `--json` output for machine workflows.
- Require structured error handling with stable fields/code when available.
- On blocked/rate-limit/risk prompt, stop and return actionable next steps.

## 6. Workflow Examples

### 6.1 Explore to publish

```powershell
mediause use account instagram:<account_id> --json
mediause auth health --json
mediause instagram get explore --limit 20 --json
mediause instagram post feed --media c:/tmp/a.jpg --text "hello" --json
mediause trace last --json
```

### 6.2 User discovery and engagement

```powershell
mediause use account instagram:<account_id> --json
mediause auth health --json
mediause instagram search users --query "fashion" --limit 10 --json
mediause instagram engage follow --username <username> --json
mediause trace last --json
```

### 6.3 Guest read-only branch

```powershell
mediause use account instagram:guest --json
mediause instagram get explore --limit 20 --json
mediause instagram search users --query "photography" --limit 10 --json
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
6. If not logged in, run `mediause auth login instagram --json` and re-bind context.
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
mediause plugin add instagram --json
mediause instagram -h
mediause instagram post -h

# context + status
mediause auth list --json
mediause use account instagram:<account_id> --json
mediause auth health --json

# read action
mediause instagram get explore --limit 20 --json

# write action
mediause instagram post feed --media c:/tmp/a.jpg --text "hello" --json

# trace
mediause trace last --json
```

Skill Metadata
Maintainer: @mediause-demo
Last-Updated: 2026-08-22
Version: v2




