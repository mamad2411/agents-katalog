---
name: douyinv2
description: Standardized douyinv2 skill for MediaUse. Includes Windows install, key onboarding, strict context/auth flow, full douyinv2 dynamic command map, and safety/rate controls.
---

# MediaUse Douyinv2 Skill

Operate Douyinv2 creator tasks with a structured login, context binding, and command map for publishing and account operations.

## Scope

Use this skill when the task targets douyinv2 operations such as:

- Account: health check
- User: profile, videos
- Content: videos, drafts, draft, delete, publish, update
- Metadata: activities, collections, hashtag, location
- Insights: stats

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

- .mediause/skills/douyinv2/SKILL.md

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
mediause plugin add douyinv2 --json
mediause douyinv2 -h
mediause douyinv2 content -h
```

### 3.2 Bind context before any read/write

`use account` must be executed successfully before any fetch/publish action.

`use account` argument format:

- `<platform:account_id>`
- `account_id` should be selected from `mediause auth list --json`.

Manifest default account id is `guest`, but write actions require a logged-in account.

By default, `use account` keeps the browser hidden. Use `--show` only when you need to inspect the page or manually resolve a challenge.

```powershell
mediause auth list --json
mediause use account douyinv2:<account_id> --policy balanced --json
```

### 3.3 Auth health precondition

`auth health` is valid only after successful `use account`.

```powershell
mediause auth health --json
```

If `auth health` indicates not logged in/expired:

```powershell
mediause auth login douyinv2 --json
mediause use account douyinv2:<account_id> --policy balanced --json
mediause auth health --json
```

If page shows `unusual traffic`, captcha, or risk confirmation:

```powershell
mediause use account douyinv2:<account_id> --policy balanced --show --json
```

Risk reduction note:

- In challenged sessions, `--show` usually lowers repeated interception risk.

Complete verification manually, then rerun the action.

### 3.4 Guest mode (optional)

Guest mode can be used for read-only actions when runtime allows:

```powershell
mediause use account douyinv2:guest --json
```

Guest mode rules:

- Read-only (account/user/content-read/metadata/insights fetch operations).
- Block all write operations (`content.draft`, `content.delete`, `content.publish`, `content.update`).
- If write is required, switch to logged-in account context.

## 4. Douyinv2 Dynamic Command Map (v1)

Source schema:

- plugin: `plugin.douyinv2`
- manifest: `crates/platforms/plugins/douyinv2/manifest.yaml`

### 4.1 account.*

- `mediause douyinv2 account health --json`

### 4.2 user.*

- `mediause douyinv2 user profile --json`
- `mediause douyinv2 user videos --sec-uid <sec_uid> [--limit <n>] [--with-comments <bool>] [--comment-limit <n>] --json`

### 4.3 content.*

- `mediause douyinv2 content videos [--limit <n>] [--page <n>] [--status <status>] --json`
- `mediause douyinv2 content drafts [--limit <n>] --json`
- `mediause douyinv2 content draft --video <path_or_url> --title <title> [--caption <text>] [--cover <path_or_url>] [--visibility <value>] --json`
- `mediause douyinv2 content delete --aweme-id <aweme_id> --json`
- `mediause douyinv2 content publish --video <path_or_url> --title <title> --schedule <iso_datetime> [--caption <text>] [--cover <path_or_url>] [--visibility <value>] [--allow-download <bool>] [--collection <id_or_name>] [--activity <name>] [--poi-id <poi_id>] [--poi-name <poi_name>] [--hotspot <text>] [--no-safety-check <bool>] [--sync-toutiao <bool>] --json`
- `mediause douyinv2 content update --aweme-id <aweme_id> [--reschedule <iso_datetime>] [--caption <text>] --json`

### 4.4 metadata.*

- `mediause douyinv2 metadata activities --json`
- `mediause douyinv2 metadata collections [--limit <n>] --json`
- `mediause douyinv2 metadata hashtag --action <action> [--keyword <text>] [--cover <cover>] [--limit <n>] --json`
- `mediause douyinv2 metadata location --query <query> [--limit <n>] --json`

### 4.5 insights.*

- `mediause douyinv2 insights stats --aweme-id <aweme_id> --json`

## 5. Operational Constraints (Mandatory)

Apply these constraints for all actions to reduce account risk and keep behavior human-like.

### 5.1 Human-like pacing

- Never execute high-risk actions continuously.
- Add randomized delay between actions.
- Add longer cooldown after draft/publish/update/delete actions.
- Mix read actions between write actions when possible.

### 5.2 Frequency limits and minimum spacing

- Hard stop if operation rate is abnormally high.
- Stop immediately on repeated anti-bot challenge, login re-validation, or risk prompt.
- Do not run burst publish loops.

Suggested limits:

- Draft/publish/update/delete: <= 3 per hour
- Metadata/search-like fetch actions: <= 60 per minute
- General read actions: <= 60 per minute

Minimum spacing:

- Draft/publish/update/delete: >= 20 minutes between actions
- Metadata/search-like fetch: >= 1 second between actions
- General read actions: >= 1 second between actions

Same-target guardrails:

- Repeated write on same `aweme_id`: >= 60 seconds
- Repeated identical publish title/caption: >= 24 hours (default deny)

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

### 6.1 Content publish workflow

```powershell
mediause use account douyinv2:<account_id> --json
mediause auth health --json
mediause douyinv2 metadata collections --limit 20 --json
mediause douyinv2 content publish --video c:/tmp/a.mp4 --title "閸愬懎顔愰弽鍥暯" --schedule "2026-05-20T09:00:00+08:00" --caption "閸欐垵绔烽弬鍥攳" --json
mediause trace last --json
```

### 6.2 Creator analytics workflow

```powershell
mediause use account douyinv2:<account_id> --json
mediause auth health --json
mediause douyinv2 content videos --limit 20 --json
mediause douyinv2 insights stats --aweme-id <aweme_id> --json
mediause trace last --json
```

### 6.3 Guest read-only workflow (if supported)

```powershell
mediause use account douyinv2:guest --json
mediause douyinv2 metadata activities --json
mediause douyinv2 user videos --sec-uid <sec_uid> --limit 10 --json
mediause trace last --json
```

## 7. Execution Checklist

Before run:

Before every run, execute the install script once.

1. CLI installed via `npm install -g @mediause/cli` on Windows.
2. PATH updated and `mediause --version` works.
3. API key configured and verified.
4. Account context bound via `mediause use account douyinv2:<account_id> --json`.
5. If write actions are required, use logged-in account instead of guest.
6. If manual verification may be needed, be ready to rerun `use account` with `--show`.
7. Pacing policy is enabled.

During run:

1. Respect delays and minimum spacing.
2. Stop on anti-bot/risk prompts.
3. If `unusual traffic` appears, rerun `mediause use account douyinv2:<account_id> --show --json` and complete verification manually.
4. Avoid repetitive burst loops.

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
mediause plugin add douyinv2 --json
mediause douyinv2 -h
mediause douyinv2 content -h

# context + status
mediause auth list --json
mediause use account douyinv2:<account_id> --json
mediause use account douyinv2:<account_id> --show --json
mediause auth health --json

# read actions
mediause douyinv2 account health --json
mediause douyinv2 user profile --json
mediause douyinv2 user videos --sec-uid <sec_uid> --limit 20 --json
mediause douyinv2 content videos --limit 20 --json
mediause douyinv2 metadata activities --json
mediause douyinv2 insights stats --aweme-id <aweme_id> --json

# write actions
mediause douyinv2 content draft --video c:/tmp/a.mp4 --title "hello" --json
mediause douyinv2 content publish --video c:/tmp/a.mp4 --title "hello" --schedule "2026-05-20T09:00:00+08:00" --json
mediause douyinv2 content update --aweme-id <aweme_id> --caption "hello" --json
mediause douyinv2 content delete --aweme-id <aweme_id> --json

# trace
mediause trace last --json
```

Skill Metadata
Maintainer: @mediause-demo
Last-Updated: 2026-08-22
Version: v2





