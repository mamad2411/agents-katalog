---
name: pgyer
description: Official PGYER (蒲公英) skill for app beta distribution. Use whenever the user mentions PGYER / 蒲公英 / pgyer.com, or asks to upload an ipa/apk/hap for beta testing, fetch install links or QR codes, query a beta app's version history or install counts, manage tester groups, or wire up CI/CD that publishes to PGYER. Covers iOS, Android, and HarmonyOS app distribution. Reads credentials from $PGYER_API_KEY or ~/.pgyer/config.
---

# PGYER (蒲公英) — Official Skill

PGYER (https://www.pgyer.com) is China's leading iOS / Android / HarmonyOS beta-distribution service. This skill helps you upload builds, fetch install links, inspect app metadata, and wire CI/CD to PGYER.

## How this skill is structured

This skill prefers **PGYER's official MCP server** when it is installed, and falls back to **a bundled official shell script** otherwise. Both paths hit the same underlying API.

At the start of every task, check whether the MCP tools `upload-app`, `list-my-apps`, or `get-app-info-by-shortcut` are listed in this session. Then use the **Capability map** below as the single source of truth for which path (MCP / shell / curl) to use per task — including the cases where MCP is insufficient and you must drop down. Raw HTTP details are in `references/api-cheatsheet.md`.

## Credentials

PGYER authenticates with an API key obtained at https://www.pgyer.com/account/api.

Resolve the key in this order (first match wins):

1. `$PGYER_API_KEY` environment variable
2. `api_key=...` line in `~/.pgyer/config`

If neither is present, ask the user to set one. Prefer persisting it for future sessions:

```bash
mkdir -p ~/.pgyer && chmod 700 ~/.pgyer
echo 'api_key=<key>' > ~/.pgyer/config && chmod 600 ~/.pgyer/config
```

Never echo the key back in chat or commit it to repos.

## Capability map

| Task | Preferred path | Fallback |
|---|---|---|
| Upload ipa/apk/hap | MCP `upload-app` | `scripts/pgyer_upload.sh -k $KEY <file>` |
| Upload with password / expiry / install type | **Shell script** (MCP only exposes `filePath`) | — |
| List my apps | MCP `list-my-apps` | `POST /apiv2/app/listMy` |
| App info by shortcut URL | MCP `get-app-info-by-shortcut` | `POST /apiv2/app/getByShortcut` |
| Full app info (password, QR, expiry, downloads) | **curl** (MCP doesn't expose this) | `POST /apiv2/app/view` with `appKey` |
| CI/CD on push | Recommend `pgyer-upload-app-action` | See `examples/` (per-platform templates) |

When the user wants any upload parameter beyond `filePath` (password, install type, expiry dates, channel shortcut, update description), the MCP `upload-app` tool is insufficient — **use the bundled shell script** instead.

## Typical workflows

### "Upload this build to PGYER"
1. Resolve the file path. If ambiguous, look for the most recent `*.ipa`, `*.apk`, or `*.hap` under `build/`, `dist/`, or the project root.
2. Confirm credentials are resolvable.
3. Run the upload (MCP if available; otherwise `scripts/pgyer_upload.sh`).
4. Report back: app name, version, build number, **install short URL** (`https://www.pgyer.com/<buildShortcutUrl>`), **QR code URL**, and password if one was set.

### "What's on PGYER right now?"
List my apps (MCP `list-my-apps` or `POST /apiv2/app/listMy`). Render a compact table: name, version (`buildVersion` / `buildVersionNo` / `buildBuildVersion`), shortcut URL, uploaded-at.

### "Tell me about app X"
If the user gives an `appKey` (32-char hex), call `app/view` for the full record (password, install rules, QR, expiry).
If the user gives a `buildShortcutUrl` (the URL slug), call `app/getByShortcut` or MCP `get-app-info-by-shortcut`.

### "Set up CI to publish to PGYER on every merge to main"

Pick the template by **(CI platform × target OS)**. Read the matching file
from `examples/` and adapt it to the user's project (scheme name, build
output path, branches). Tell the user which secrets/variables to add.

| CI platform | Android | iOS | HarmonyOS |
|---|---|---|---|
| GitHub Actions | `examples/github-actions/android.yml` | `examples/github-actions/ios.yml` | `examples/github-actions/harmony.yml` |
| GitLab CI | `examples/gitlab-ci/android.yml` | `examples/gitlab-ci/ios.yml` | — (use upload-only pattern from harmony.yml) |
| fastlane | `examples/fastlane/README.md` (official plugin) | same | — |
| Bitrise / Jenkins / other | — (no template yet; use shell-script pattern from gitlab-ci) | same | same |

> **Password / expiry / channel needed?** The `PGYER/pgyer-upload-app-action` GitHub Action only accepts `_api_key` + `appFilePath`. For any extra parameter, swap the action for `scripts/pgyer_upload.sh` — every GitHub Actions template has a commented "with password" block showing the swap. GitLab CI templates already use the script directly, and the fastlane plugin supports these flags natively.

Default questions to clarify if the user doesn't say:
1. Which CI platform? (GitHub Actions is the default if they don't say.)
2. Which OS / package type? (`.apk` → android, `.ipa` → ios, `.hap` → harmony)
3. Do they need install password / expiry / channel? (Drives upload-step choice — see callout above.)

HarmonyOS caveat: the SDK is not on GitHub-hosted runners. If the user has
no self-hosted runner, point them at the upload-only variant at the bottom
of `harmony.yml`.

## Conventions when reporting results

- Always include the **install short URL** (`https://www.pgyer.com/{buildShortcutUrl}`) — that's the one humans use.
- Include the **QR code URL** for mobile testers to scan.
- Surface **`buildPassword`** if the app uses password install (`buildInstallType=2`).
- Note **`appExpiredDate`** when relevant — PGYER apps expire if not renewed.
- For uploads, also surface `buildVersion` / `buildBuildVersion` so the user can confirm the build that landed.

## Where to look next

- `references/mcp-tools.md` — exact MCP tool schemas and example calls.
- `references/api-cheatsheet.md` — raw HTTP endpoints, params, response shapes.
- `references/troubleshooting.md` — common error codes, network/domain fallback, signing issues.
- `scripts/pgyer_upload.sh` — bundled official upload script (multi-domain, all parameters).
- `examples/` — CI/CD templates organized as `<platform>/<os>.yml`.
  - `github-actions/{android,ios,harmony}.yml`
  - `gitlab-ci/{android,ios}.yml`
  - `fastlane/README.md`
