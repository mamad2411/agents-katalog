---
name: xiaohongshu
description: Standardized Xiaohongshu skill for MediaUse. Includes Windows install, key onboarding, strict context/auth flow, full Xiaohongshu dynamic command map, and safety/rate controls.
---

# MediaUse Xiaohongshu Skill

Create and operate Xiaohongshu content workflows with consistent setup, context handling, command execution, and compliance guardrails.

## Scope

Use this skill when the task targets Xiaohongshu operations such as:

- Publish: feed, repost, note boost
- Read: feed, detail, notifications
- User: profile, profile update, user feed, followers, following
- Reply: comment, sub-comment, private message
- Search: text, user, hot topics
- Engage: like, follow, collect
- Management/trace: manage task, trace last

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

- .mediause/skills/xiaohongshu/SKILL.md

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
mediause sites list --json
mediause sites add xiaohongshu --json
mediause xiaohongshu -h
mediause xiaohongshu post -h
```

### 3.2 Bind context before any read/write

`use account` must be executed successfully before any fetch/publish action.

`use account` argument format:

- `<platform:account_id>`
- `account_id` should be selected from `mediause auth list --json`.

```powershell
mediause auth list --json
mediause use account xiaohongshu:<account_id> --policy balanced --json
```

If challenge/risk prompts appear, reopen in visible mode:

```powershell
mediause use account xiaohongshu:<account_id> --policy balanced --show --json
```

`--show` usually lowers repeated interception risk in challenged sessions.

### 3.3 Auth health precondition

`auth health` is valid only after successful `use account`.

```powershell
mediause auth health --json
```

If `auth health` indicates not logged in/expired:

```powershell
mediause auth login xiaohongshu --json
mediause use account xiaohongshu:<account_id> --policy balanced --json
mediause auth health --json
```

### 3.4 Guest mode (optional, site-dependent)

If guest mode is supported by the current CLI/site runtime:

```powershell
mediause use account xiaohongshu:guest --json
```

Guest mode rules:

- Read-only (fetch/search/get/user read operations).
- Block all write operations (post/reply/engage/manage/note write intent).
- If write is required, switch to logged-in account context.

## 4. Xiaohongshu Dynamic Command Map (v1)

Source schema:

- plugin: `plugin.xiaohongshu`
- schema version: `v1`
- supported layer: `L3Bridge`

### 4.1 post.*

- `post feed` uses only one media argument: `--media`, which covers both image and video file paths.
- `mediause xiaohongshu post feed [--title <text>] [--text <text>] [--media <paths>] [--cover <cover_path>] --json`
- `mediause xiaohongshu post repost --id <post_id> [--text <text>] --json`

### 4.2 get.*

- `mediause xiaohongshu get feed [--limit <n>] [--type <type>] --json`
- `mediause xiaohongshu get detail --id <item_id> [--comments <bool>] --json`
- `mediause xiaohongshu get notif [--type <type>] --json`

### 4.3 user.*

- `mediause xiaohongshu user profile [--me <bool>] [--user-id <uid>] --json`
- `mediause xiaohongshu user profile-update [--bio <text>] [--name <text>] [--avatar <path>] --json`
- `mediause xiaohongshu user feed --user-id <uid> [--limit <n>] [--type <type>] --json`
- `mediause xiaohongshu user followers --user-id <uid> [--limit <n>] --json`
- `mediause xiaohongshu user following --user-id <uid> [--limit <n>] --json`

### 4.4 reply.*

- `mediause xiaohongshu reply comment --post-id <post_id> --text <text> --json`
- `mediause xiaohongshu reply sub --comment-id <comment_id> --text <text> --json`
- `mediause xiaohongshu reply message --user-id <uid> --text <text> --json`

### 4.5 search.*

- `mediause xiaohongshu search text --keyword <keyword> [--limit <n>] --json`
- `mediause xiaohongshu search user --query <query> [--limit <n>] --json`
- `mediause xiaohongshu search hot --json`

### 4.6 engage.*

- `mediause xiaohongshu engage like --id <item_id> [--type <type>] --json`
- `mediause xiaohongshu engage follow --user-id <uid> [--undo <bool>] --json`
- `mediause xiaohongshu engage collect --id <item_id> --json`

### 4.7 manage.*

- `mediause xiaohongshu manage task [--task <task_name>] [--note-id <note_id>] --json`

### 4.8 trace.*

- `mediause xiaohongshu trace last --json`

### 4.9 note.*

- `mediause xiaohongshu note boost --note-id <note_id> --json`

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

- Publish/manage/note boost: <= 3 per hour
- Reply/message: <= 20 per hour
- Follow/like/collect: <= 30 per hour
- Search/read: <= 60 per minute

Minimum spacing:

- Publish/manage/note boost: >= 20 minutes between actions
- Reply/message: >= 30 seconds between actions
- Follow/like/collect: >= 10 seconds between actions
- Read/search/get/user read/trace: >= 1 second between actions

Same-target guardrails:

- Repeated interaction on same target (same post_id/note_id/user_id): >= 60 seconds
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
mediause use account xiaohongshu:<account_id> --json
mediause auth health --json
mediause xiaohongshu search hot --json
mediause xiaohongshu post feed --title "娴犲﹥妫╅幒銊ㄥ礃" --text "<draft_text>" --media c:/tmp/a.png,c:/tmp/b.png --json
mediause trace last --json
```

### 6.1.1 Video publish with cover

```powershell
mediause use account xiaohongshu:<account_id> --json
mediause auth health --json
mediause xiaohongshu post feed --title "2026缁屾寧鎯? --text "娴犲﹥妫╅崚鍡曢煩" --media c:/tmp/a.mp4 --cover c:/tmp/cover.png --json
mediause trace last --json
```

### 6.1.2 Long article publish

```powershell
mediause use account xiaohongshu:<account_id> --json
mediause auth health --json
mediause xiaohongshu post feed --title "2026缁屾寧鎯? --text "娴犲﹥妫╅崚鍡曢煩" --json
mediause trace last --json
```

### 6.2 Monitor and engage

```powershell
mediause use account xiaohongshu:<account_id> --json
mediause auth health --json
mediause xiaohongshu get notif --type mention --json
mediause xiaohongshu reply comment --post-id <id> --text "received" --json
mediause trace last --json
```

### 6.3 Note boost flow

```powershell
mediause use account xiaohongshu:<account_id> --json
mediause auth health --json
mediause xiaohongshu note boost --note-id <note_id> --json
mediause xiaohongshu manage task --task note.boost --note-id <note_id> --json
mediause trace last --json
```

### 6.4 Read-only guest branch (if supported)

```powershell
mediause use account xiaohongshu:guest --json
mediause xiaohongshu search hot --json
mediause xiaohongshu get feed --limit 20 --json
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
6. If not logged in, run `mediause auth login xiaohongshu --json` and re-bind context.
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

# discover
mediause sites list --json
mediause sites add xiaohongshu --json
mediause xiaohongshu -h
mediause xiaohongshu post -h

# context + status
mediause auth list --json
mediause use account xiaohongshu:<account_id> --json
mediause auth health --json

# read action
mediause xiaohongshu search hot --json

# write action
mediause xiaohongshu post feed --title "hello" --text "hello" --json

# trace
mediause trace last --json
```

Skill Metadata
Maintainer: @mediause-demo
Last-Updated: 2026-08-22
Version: v2





