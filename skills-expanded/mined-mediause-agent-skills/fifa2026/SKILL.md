---
name: fifa2026
description: Standardized fifa2026 skill for MediaUse. Includes Windows install, key onboarding, strict context/auth flow, full fifa2026 dynamic command map, and safe read-oriented execution controls.
---

# MediaUse FIFA 2026 Skill

Use this skill to run FIFA 2026 data discovery workflows in MediaUse, including player lookup, team lookup, group lookup, and detailed stats retrieval.

## Scope

Use this skill when the task targets `fifa2026` operations such as:

- Search player by name
- Search team by name
- Search group by letter/country (`query` optional)
- Get player details
- Get team details and roster preview
- Get player recent match stats
- Get team recent match stats
- Compare two teams by ranking, form, and key players
- Predict a match with structured probability output

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

- .mediause/skills/fifa2026/SKILL.md

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

1. Run install script once to ensure latest CLI.
2. Discover site and commands.
3. Bind account context with `use account`.
4. Check status with `auth health` when needed.
5. Execute dynamic site actions.
6. Verify with trace/task.

### 3.1 Discover and plugin setup

```powershell
mediause plugin list --json
mediause plugin add fifa2026 --json
mediause fifa2026 -h
mediause fifa2026 search -h
mediause fifa2026 get -h
mediause fifa2026 compare -h
mediause fifa2026 predict -h
```

### 3.2 Bind context before commands

`use account` must be executed successfully before search/get actions.

`use account` argument format:

- `<platform:account_id>`
- `account_id` can be selected from `mediause auth list --json`.

```powershell
mediause auth list --json
mediause use account fifa2026:guest --json
```

If you need to watch page behavior (for challenge/manual checks):

```powershell
mediause use account fifa2026:guest --show --json
```

Risk reduction note:

- For site-backed actions (`search/get/compare/predict`), prefer binding with `--show`.
- A visible session usually lowers Cloudflare/challenge interception risk versus fully hidden runs.

### 3.3 Auth health precondition

For `fifa2026` read workflows, `guest` is typically sufficient. If a non-guest account is used, check:

```powershell
mediause auth health --json
```

If health indicates login expired:

```powershell
mediause auth login fifa2026 --json
mediause use account fifa2026:<account_id> --json
mediause auth health --json
```

## 4. FIFA 2026 Dynamic Command Map (v1)

Source schema:

- plugin: `plugin.fifa2026`
- manifest: `crates/platforms/plugins/fifa2026/manifest.yaml`

### 4.1 search.*

- `mediause fifa2026 search player --name <text> [--limit <n>] --json`
- `mediause fifa2026 search team --name <text> [--url <url>] [--limit <n>] --json`
- `mediause fifa2026 search group [--query <text>] [--url <url>] [--limit <n>] --json`

`search group` query behavior:

- No `query`: return all groups.
- Letter query: supports values like `a`, `b`, `c`, or `a,b,c`.
- Country query: supports values like `brazil`, and returns matched group.

### 4.2 get.*

- `mediause fifa2026 get player --url <url> --json`
- `mediause fifa2026 get team --url <url> [--player-limit <n>] --json`
- `mediause fifa2026 get player-stats --url <url> [--limit <n>] --json`
- `mediause fifa2026 get team-stats --url <url> [--limit <n>] --json`

### 4.3 compare.*

- `mediause fifa2026 compare teams --team_a_url <url> --team_b_url <url> [--competition_url <url>] [--recent_limit <n>] [--player_limit <n>] --json`

`compare teams` parameter notes:

- `team_a_url`, `team_b_url`: required squad URLs.
- `competition_url`: optional competition context, defaults to World Cup stats page.
- `recent_limit`: optional recent match window, default `10`.
- `player_limit`: optional top player comparison depth, default `5`.

### 4.4 predict.*

- `mediause fifa2026 predict match --home_url <url> --away_url <url> [--competition_url <url>] [--recent_limit <n>] [--player_limit <n>] [--neutral_site <true|false>] --json`

`predict match` parameter notes:

- `home_url`, `away_url`: required squad URLs.
- `competition_url`: optional ranking/group context URL.
- `recent_limit`: optional form window size, default `10`.
- `player_limit`: optional squad strength feature depth, default `5`.
- `neutral_site`: optional venue flag, default `true`.

## 5. Operational Constraints (Mandatory)

Apply these constraints for stable and safe execution.

### 5.1 Read-oriented pacing

- Avoid burst loops on repeated navigation.
- Add short delay between repeated fetches.
- Stop and retry later if anti-bot/challenge appears.

### 5.2 Suggested limits and spacing

Suggested limits:

- Search/get actions: <= 60 per minute

Minimum spacing:

- Search/get actions: >= 1 second between actions

Same-target guardrails:

- Repeated request to same URL/query: >= 2 seconds

If a limit is hit or challenge repeats:

1. Pause at least 5 minutes.
2. Rebind context with `use account --show`.
3. Resume with lower frequency.

### 5.3 Safety policy

- Do not bypass platform protections.
- Do not attempt credential/session hijacking.
- Respect platform terms and local regulations.

### 5.4 Output and error handling

- Prefer `--json` output.
- Require structured error handling.
- On blocked/risk/challenge, stop and return actionable next steps.

## 6. Workflow Examples

### 6.1 Group overview (all groups)

```powershell
mediause use account fifa2026:guest --show --json
mediause fifa2026 search group --json
mediause trace last --json
```

### 6.2 Group lookup by letters

```powershell
mediause use account fifa2026:guest --show --json
mediause fifa2026 search group --query "a,b,c" --json
mediause trace last --json
```

### 6.3 Group lookup by country

```powershell
mediause use account fifa2026:guest --show --json
mediause fifa2026 search group --query "brazil" --json
mediause trace last --json
```

### 6.4 Player to stats drill-down

```powershell
mediause use account fifa2026:guest --show --json
mediause fifa2026 search player --name "marta" --limit 5 --json
mediause fifa2026 get player --url <player_url> --json
mediause fifa2026 get player-stats --url <player_url> --limit 5 --json
mediause trace last --json
```

### 6.5 Team comparison

```powershell
mediause use account fifa2026:guest --show --json
mediause fifa2026 compare teams --team_a_url <team_a_url> --team_b_url <team_b_url> --json
mediause trace last --json
```

### 6.6 Match prediction

```powershell
mediause use account fifa2026:guest --show --json
mediause fifa2026 predict match --home_url <home_team_url> --away_url <away_team_url> --neutral_site true --json
mediause trace last --json
```

## 7. Execution Checklist

Before run:

1. Run `npm install -g @mediause/cli` once to auto-install/upgrade latest CLI.
2. PATH updated and `mediause --version` works.
3. API key configured and verified.
4. Account context bound via `mediause use account <platform:account_id> --show` (recommended for lower interception risk).
5. If using non-guest account, `mediause auth health --json` checked.

During run:

1. Respect spacing and retry limits.
2. Stop on repeated challenge pages.
3. Avoid repeated burst requests to same target.

After run:

1. Save logs and outcomes.
2. Record challenge/risk events and cooldowns.
3. Keep activity under conservative limits.

## 8. Quick Command Reference

```powershell
# always run once before each workflow (auto-upgrade latest)
mediause --version
mediause --version

# discover
mediause plugin list --json
mediause plugin add fifa2026 --json
mediause fifa2026 -h
mediause fifa2026 search -h
mediause fifa2026 get -h
mediause fifa2026 compare -h
mediause fifa2026 predict -h

# context + status
mediause auth list --json
mediause use account fifa2026 --show --json
mediause use account fifa2026:guest --show --json
mediause auth health --json

# key workflows
mediause fifa2026 search group --json
mediause fifa2026 search group --query "a,b,c" --json
mediause fifa2026 search group --query "brazil" --json
mediause fifa2026 search team --name "brazil" --json
mediause fifa2026 get team --url <team_url> --json
mediause fifa2026 get team-stats --url <team_url> --json
mediause fifa2026 compare teams --team_a_url <team_a_url> --team_b_url <team_b_url> --json
mediause fifa2026 predict match --home_url <home_team_url> --away_url <away_team_url> --json

# trace
mediause trace last --json
```

Skill Metadata
Maintainer: @mediause-demo
Last-Updated: 2026-08-22
Version: v2


