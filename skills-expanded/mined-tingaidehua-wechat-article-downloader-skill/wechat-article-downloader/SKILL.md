---
name: wechat-article-downloader
description: Download, filter, analyze, and export WeChat public-account (微信公众号) articles from mp.weixin.qq.com. Use for one public article, an account's latest N articles, an exact publication date, or a date range; export HTML, Markdown, PDF, DOCX, JSON, CSV, TXT, or MHTML; guide the user through local credential capture when account history requires their signed-in WeChat session; diagnose parser/provider rule changes; or run the localhost control console.
license: MIT
---

# WeChat Article Downloader

Use the bundled provider-based CLI. Do not automate the upstream desktop EXE and do not ask the user to paste credentials into chat.

## Locate the CLI

Resolve this `SKILL.md` directory as `skill_root`, then use:

```powershell
$cli = Join-Path $skill_root "scripts\wechat-download.ps1"
```

If dependencies are missing, run once:

```powershell
& (Join-Path $skill_root "scripts\bootstrap.ps1")
```

Run `& $cli --json doctor` before the first download. Use `--json` for agent calls so paths and error codes are unambiguous.

## Choose the Workflow

- One explicitly named article: use `article`. It needs no credential.
- “这个公众号最新 N 篇”: use `account --latest N`.
- “某年某月某日”: normalize to `YYYY-MM-DD`, then use `account --date`.
- A date interval: use `account --since ... --until ...`.
- The user asks for overview or UI: use `web --open`.
- An existing workflow returns `AUTH_REQUIRED`: follow Local Authorization.
- Parser/history behavior changed: read `references/protocol-principles.md` before modifying code.

Never silently interpret “最新文章” as every historical article. If the count is omitted and context does not establish one, ask for a count; otherwise use the exact user-provided count.

## Download One Article

```powershell
& $cli --json article "https://mp.weixin.qq.com/s/..." `
  --formats "html,md,pdf"
```

Optional:

- `--output <directory>`
- `--assets` or `--no-assets`
- formats: `html,md,pdf,docx,json,csv,txt,mhtml`

After success, inspect the returned `manifest.json` and requested output files. If the user asked for analysis, read the exported Markdown/JSON and provide the analysis after the download; do not claim analysis from the title alone.

## Download Account History

Use any public article from that account as `sample_url`.

```powershell
& $cli --json account "<sample_url>" --latest 3 --formats "md,pdf"
& $cli --json account "<sample_url>" --date 2026-07-16 --formats "html,pdf"
& $cli --json account "<sample_url>" --since 2026-07-01 --until 2026-07-31 --formats "md,pdf"
```

Useful options:

- `--credential default`
- `--max-pages 30`
- `--output <directory>`
- `--assets` / `--no-assets`

Treat `--since` and `--until` as inclusive dates in `Asia/Shanghai`.

## Local Authorization

Account history is a credential-bound WeChat capability. Never request or expose `key`, `uin`, `pass_ticket`, `appmsg_token`, `poc_token`, Cookie, or a complete authenticated request URL in chat.

First return safe guidance:

```powershell
& $cli --json auth guide "<sample_url>"
```

Then tell the user:

1. Run the following command locally in their Windows desktop session.
2. Copy the generated account-home URL into WeChat's File Transfer Assistant.
3. Open that URL inside WeChat while signed in.
4. Leave the capture command running until it reports success.

```powershell
& $cli auth capture "<sample_url>" --alias default --watch-seconds 120
```

The scanner reads only recent local WeChat cache candidates, validates them against the read-only history endpoint, and stores only an accepted credential in Windows Credential Manager. It never prints values.

If automatic capture cannot find a candidate, offer the local hidden-prompt fallback:

```powershell
& $cli auth import default
```

Before the fallback, the user may explicitly choose a broader recent temporary-file scan:

```powershell
& $cli auth capture "<sample_url>" --include-temp
```

Explain that `--include-temp` additionally scans recently modified files under `%LOCALAPPDATA%\Temp`; never enable it silently.

Do not accept secrets through agent input as a workaround. After authorization, rerun the original `account` command.

Inspect redacted status with:

```powershell
& $cli --json auth status
```

Delete only when the user explicitly requests it:

```powershell
& $cli auth delete default --yes
```

## Interpret Results

- `ok: true`: report the manifest and requested files.
- `ok: false` with per-article failures: report partial success and failed titles.
- `AUTH_REQUIRED`: guide local re-capture; credentials are normally short-lived.
- `REMOTE_ERROR`: retry once after respecting the configured interval, then report the endpoint-layer failure.
- `EXPORT_ERROR`: preserve successfully written HTML/Markdown and report the missing local exporter.
- No articles for a date and `history_scan.complete: true`: report that the queried history contained no matching date.
- `history_scan.truncated: true`: report the result as inconclusive and offer a larger validated `--max-pages`; never claim the date had no article.

Use output manifests as the source of truth. Prefer clickable absolute file links in the final response.

## Web Console

```powershell
& $cli web --open
```

The console is loopback-only and deliberately cannot import, display, or delete credentials. It exposes status, metrics, data sources, processing pipeline, bounded jobs, history, configuration, security posture, and the CLI/Web parity ledger.

## Safety and Scope

- Download only content the user is authorized to access.
- Do not bypass CAPTCHAs, paywalls, deleted/private content, or access controls.
- Do not perform comments, likes, reads inflation, or other write actions.
- Keep request rate at or above the configured one-second minimum.
- Do not publish captured caches, authenticated URLs, credentials, or upstream EXE resources.
- Network access is restricted to `https://mp.weixin.qq.com` and allowlisted HTTPS WeChat/Tencent media CDNs.
