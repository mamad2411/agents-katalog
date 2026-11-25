---
name: medium
description: Standardized Medium skill for MediaUse. Includes Windows install, key onboarding, strict context/auth flow, full Medium dynamic command map, and safe read-oriented execution controls.
---

# MediaUse Medium Skill

Use this skill to discover Medium posts by topic, tag, search, user feed, and to read full article content with preserved inline images.

## Scope

Use this skill when the task targets Medium operations such as:

- Account: health check
- Get: topic feed, tag feed
- Search: posts by keyword
- User: posts by username
- Read: full article by URL

Medium defaults to `guest` account context and is primarily read-oriented.

- Use `mediause use account medium:guest --json` before running dynamic commands.
- `use account` defaults to a hidden browser session.
- If you need visible browser control (challenge handling or debugging), use `mediause use account medium:guest --show --json`.

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

- .mediause/skills/medium/SKILL.md

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
2. Bind account context with `use account`.
3. Check status with `auth health` when needed.
4. Execute dynamic site actions.
5. Verify with trace/task.

### 3.1 Discover and plugin setup

```powershell
mediause plugin list --json
mediause plugin add medium --json
mediause medium -h
mediause medium get -h
```

### 3.2 Bind context before any read action

`use account` must be executed successfully before any fetch/read action.

`use account` argument format:

- `<platform:account_id>`
- `account_id` should be selected from `mediause auth list --json`.

```powershell
mediause auth list --json
mediause use account medium:guest --policy balanced --json
```

If challenge/risk prompts appear, reopen in visible mode:

```powershell
mediause use account medium:guest --policy balanced --show --json
```

### 3.3 Auth health

`auth health` is optional for guest-only read workflows, but can be used as a session diagnostic.

```powershell
mediause auth health --json
```

If using a non-guest account and session is not ready:

```powershell
mediause auth login medium --json
mediause use account medium:<account_id> --policy balanced --json
mediause auth health --json
```

### 3.4 Guest mode

Medium plugin default account id is `guest`.

```powershell
mediause use account medium:guest --json
```

Guest mode rules:

- Read-only operations only.
- This plugin command set does not expose write operations.

## 4. Medium Dynamic Command Map (v1)

Source schema:

- plugin: `plugin.medium`
- manifest: `crates/platforms/plugins/medium/manifest.yaml`

### 4.1 account.*

- `mediause medium account health --json`

### 4.2 get.*

- `mediause medium get feed [--topic <topic>] [--limit <n>] --json`
- `mediause medium get tag --tag <tag> [--limit <n>] --json`

### 4.3 search.*

- `mediause medium search posts --keyword <keyword> [--limit <n>] --json`

### 4.4 user.*

- `mediause medium user posts --username <username> [--limit <n>] --json`

### 4.5 read.*

- `mediause medium read item --url <article_url> [--max-length <n>] --json`

Read output should include normalized article text fields and an `images` array when images are present in the article content.

## 5. Operational Constraints (Mandatory)

Apply these constraints for all actions to reduce risk and keep behavior stable.

### 5.1 Human-like pacing

- Avoid tight polling loops.
- Add randomized delay between repeated reads/searches.
- Mix different read actions instead of repeatedly hitting one endpoint.

### 5.2 Frequency limits and minimum spacing

- Hard stop if operation rate is abnormally high.
- Stop immediately on repeated challenge/risk prompts.

Suggested limits:

- Get/search/read/user/account read actions: <= 60 per minute

Minimum spacing:

- Get/search/read/user/account read actions: >= 1 second between actions

Same-target guardrails:

- Repeated read on same URL/tag/topic/user query: >= 3 seconds

If a limit is hit:

1. Pause at least 5 minutes.
2. Resume with lower request frequency.
3. Re-check session health if account context changed.

### 5.3 Safety policy

- Do not bypass platform protections.
- Do not attempt credential scraping or session hijacking.
- Respect platform terms and local regulations.

### 5.4 Output and error handling

- Prefer `--json` output for machine workflows.
- Require structured error handling with stable fields/code when available.
- On blocked/rate-limit/risk prompt, stop and return actionable next steps.

## 6. Workflow Examples

### 6.1 Topic feed then read article

```powershell
mediause use account medium:guest --json
mediause medium get feed --topic technology --limit 20 --json
mediause medium read item --url <article_url> --max-length 4000 --json
mediause trace last --json
```

### 6.2 Tag-based discovery

```powershell
mediause use account medium:guest --json
mediause medium get tag --tag ai --limit 20 --json
mediause trace last --json
```

### 6.3 Keyword search to author feed

```powershell
mediause use account medium:guest --json
mediause medium search posts --keyword "agent workflow" --limit 20 --json
mediause medium user posts --username <username> --limit 20 --json
mediause trace last --json
```

### 6.4 Session diagnostic branch

```powershell
mediause use account medium:guest --json
mediause medium account health --json
mediause auth health --json
mediause trace last --json
```

## 7. Execution Checklist

Before run:

Before every run, execute the install script once.

1. CLI installed via `npm install -g @mediause/cli` on Windows.
2. PATH updated and `mediause --version` works.
3. API key configured and verified.
4. Account context bound via `mediause use account medium:guest --json`.
5. If needed, run `mediause auth health --json` for session diagnostics.
6. If challenge appears, rerun with `--show` and complete manual verification.
7. Pacing policy is enabled.

During run:

1. Respect delays and minimum spacing.
2. Stop on anti-bot/risk prompts.
3. Avoid repetitive burst loops.

After run:

1. Save logs and outcomes.
2. Record any warning and cooldown events.
3. Keep activity under conservative limits.

## 8. Quick Command Reference

```powershell
# always run once before each workflow (auto-upgrade latest)
npm install -g @mediause/cli
mediause --version

# discover
mediause plugin list --json
mediause plugin add medium --json
mediause medium -h
mediause medium read -h

# context + diagnostics
mediause auth list --json
mediause use account medium:guest --json
mediause auth health --json

# read actions
mediause medium get feed --topic technology --limit 20 --json
mediause medium get tag --tag ai --limit 20 --json
mediause medium search posts --keyword "agent workflow" --limit 20 --json
mediause medium user posts --username <username> --limit 20 --json
mediause medium read item --url <article_url> --max-length 4000 --json

# trace
mediause trace last --json
```

Skill Metadata
Maintainer: @mediause-team
Last-Updated: 2026-08-22
Version: v2


