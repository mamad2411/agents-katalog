---
name: netflix
description: Use when handling MediaUse Netflix Tudum tasks, including list/get/search actions with guest-first dynamic commands, multi-platform direct switching, and safe execution guardrails.
---

# MediaUse Netflix Skill

Run Netflix Tudum content discovery with guest-first dynamic commands, optional account context binding, and stable JSON-oriented execution.

## Scope

Use this skill when the task targets Netflix operations such as:

- Account health checks
- Content listing (home, shows, movies, trending, top10, recommend, comingSoon, leavingSoon, kDramas, anime, whatToWatch, podcasts)
- Tudum title/article retrieval
- What's New search and filtering

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

## 2. Configure API Key

```powershell
mediause manage key --json
```

Optional checks:

```powershell
mediause auth list --json
mediause auth health --json
```

## 3. Context Model (Netflix Guest-First)

Netflix manifest defaults to guest context (`default_account_id: guest`).

Preferred pattern for this plugin:

- Use dynamic direct commands with account selector
- Guest mode can run read flows directly
- Use `use account` only when you need explicit/visible session control

### 3.1 Direct dynamic commands (recommended)

```powershell
mediause netflix:guest list home --json
mediause netflix:guest get tudum --slug avatar-the-last-airbender --json
```

### 3.2 Explicit context binding (optional)

```powershell
mediause use account netflix:guest --json
mediause netflix list home --json
```

If manual observation or challenge handling is needed:

```powershell
mediause use account netflix:guest --show --json
```

## 4. Netflix Dynamic Command Map (from manifest)

Source schema:

- plugin: `plugin.netflix`
- manifest: `crates/platforms/plugins/netflix/manifest.yaml`

### 4.1 account.*

- `mediause netflix account health --json`

### 4.2 list.*

- `mediause netflix list home [--page <n>] [--limit <n>] --json`
- `mediause netflix list shows [--page <n>] [--limit <n>] --json`
- `mediause netflix list movies [--page <n>] [--limit <n>] --json`
- `mediause netflix list trending [--page <n>] [--limit <n>] --json`
- `mediause netflix list top10 [--region <code>] [--type <movies|tv>] [--page <n>] [--limit <n>] --json`
- `mediause netflix list recommend [--page <n>] [--limit <n>] --json`
- `mediause netflix list comingSoon [--page <n>] [--limit <n>] --json`
- `mediause netflix list leavingSoon [--page <n>] [--limit <n>] --json`
- `mediause netflix list kDramas [--page <n>] [--limit <n>] --json`
- `mediause netflix list anime [--page <n>] [--limit <n>] --json`
- `mediause netflix list whatToWatch [--page <n>] [--limit <n>] --json`
- `mediause netflix list podcasts [--page <n>] [--limit <n>] --json`

### 4.3 get.*

- `mediause netflix get tudum --slug <title_slug> --json`
- `mediause netflix get article --slug <article_slug> --json`

### 4.4 search.*

- `mediause netflix search whatsnew [--search <text>] [--type <movie|series>] [--genre <text>] [--language <text>] [--archive <value>] [--page <n>] [--limit <n>] --json`

Note:

- Manifest indicates `search whatsnew` requires visible account context (`use account netflix --show true`).
- If search fails due to verification/risk checks, run:

```powershell
mediause use account netflix:guest --show --json
```

## 5. Standard Workflows

### 5.1 Quick guest discovery

```powershell
mediause plugin add netflix --json
mediause netflix:guest list home --limit 20 --json
mediause netflix:guest list trending --limit 20 --json
mediause trace last --json
```

### 5.2 Get latest Netflix series information with comingSoon

```powershell
mediause plugin add netflix --json
mediause netflix:guest list comingSoon --limit 20 --json
```

Use this when you want the latest upcoming or newly surfaced Netflix series/movie information without needing an account-bound session.

### 5.3 Tudum title deep read

```powershell
mediause netflix:guest get tudum --slug avatar-the-last-airbender --json
mediause netflix:guest get article --slug avatar-the-last-airbender-season-2 --json
mediause trace last --json
```

### 5.3 What's New filtered search

```powershell
mediause use account netflix:guest --show --json
mediause netflix search whatsnew --search "sci-fi" --type series --language english --limit 20 --json
mediause trace last --json
```

## 6. Operational Constraints

- Prefer `--json` for all commands.
- Keep read operations paced (avoid burst loops).
- On CAPTCHA / unusual traffic / manual challenge:
  - Switch to visible context with `--show`.
  - Pause, complete verification, then retry.
- Do not declare or execute commands not present in the Netflix manifest.

## 7. Minimum Validation Checklist

Before run:

1. `mediause --version` works.
2. API key configured.
3. Plugin installed: `mediause plugin add netflix --json`.
4. Command help reachable: `mediause netflix -h`.

During run:

1. Use dynamic direct command for guest-first flows.
2. Use `--show` when search or verification requires visible context.
3. Keep intervals between repeated calls.

After run:

1. Inspect `mediause trace last --json`.
2. Record any challenge/risk event and applied recovery step.

Skill Metadata
Maintainer: @mediause-team
Last-Updated: 2026-08-22
Version: v2


