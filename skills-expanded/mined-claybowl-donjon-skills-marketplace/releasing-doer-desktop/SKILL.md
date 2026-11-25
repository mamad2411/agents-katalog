---
name: releasing-doer-desktop
description: "Cuts a new release of the Doer Electron desktop app (macOS arm64 + Windows x64) to Cloudflare R2. Use when bumping the version, triggering a desktop build, or shipping a new release. Trigger phrases: bump to X.X.X, ship desktop, release Doer, new version, cut a release. Repo: claybowl/doer."
---

# Releasing Doer Desktop

Pipeline: `desktop/package.json` version bump → `gh workflow run` → GitHub Actions builds Mac + Windows → uploads to Cloudflare R2 → `update-electron-app` serves updates.

**No git tags.** This pipeline uses `workflow_dispatch` only. Do NOT use `npm version` or create git tags.

## Pre-flight (run all, stop on failure)

```sh
# 1. Branch check — releases should come from main
git rev-parse --abbrev-ref HEAD

# 2. Dirty tree check
git status --porcelain

# 3. Recent CI status
gh run list --limit 3 --branch main --workflow=desktop-release.yml -R claybowl/doer --json status,conclusion,name

# 4. Required secrets
gh secret list -R claybowl/doer
# Must exist: S3_BUCKET, S3_ENDPOINT, S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY, DOER_UPDATE_URL
```

If dirty tree: commit or stash first. If secrets missing: tell Clay exactly which ones.

## Version bump

Edit `desktop/package.json` — change `"version"` field only. Do not touch root `package.json` or `server/package.json`.

```sh
# Verify the bump before committing
node -e "console.log(JSON.parse(require('fs').readFileSync('desktop/package.json','utf8')).version)"
```

Commit:
```sh
git add desktop/package.json
git commit -m "chore(desktop): bump version to X.X.X"
git push origin main
```

## Trigger the release

```sh
gh workflow run desktop-release.yml -R claybowl/doer -f dry_run=false
```

Get the run ID and watch it:
```sh
gh run list -R claybowl/doer --workflow=desktop-release.yml --limit 1
gh run watch <run-id> -R claybowl/doer
```

Expected duration: ~15 min (Mac ~3 min; Windows Squirrel build ~13 min).

## Verify artifacts

After both jobs show ✓:
```sh
gh run view <run-id> -R claybowl/doer
```

Should see both `doer-desktop-darwin-arm64` and `doer-desktop-win32-x64` artifacts.

R2 public URL pattern:
```
https://pub-89b7185033194502b2b07cdf3b1375aa.r2.dev/beta/<platform>/<arch>/<filename>
```

## Installing on Mac (unsigned app)

When a user gets "damaged or can't be opened":
```sh
xattr -cr /path/to/Doer.app && open /path/to/Doer.app
```

## Known gotchas — do not re-introduce

| Symptom | Root cause | Fix |
|---|---|---|
| `pnpm -F 'server...'` matches nothing on Windows | PowerShell passes single quotes literally | No quotes: `pnpm -F server... build` |
| `mkdir -p` / `cp -R` fails on Windows | POSIX-only commands | `node -e "require('fs').cpSync(...)"` |
| `@doer/desktop.nuspec` ENOENT | Scoped npm name → Squirrel treats `/` as path separator | `name: "doer-desktop"` in MakerSquirrel |
| `Authors is required` | Squirrel nuspec requires authors field | `authors: "Donjon Intelligence Systems"` in MakerSquirrel |
| R2 TLS `bad_record_mac` | S3 SDK + R2 + macOS Node quirk | presigned URL + curl in `upload-artifacts.mjs` |
| `packages field missing or empty` | `desktop/pnpm-workspace.yaml` missing `packages: ["."]` | Already fixed — do not remove that field |

## Dry run (local build only, no R2 publish)

```sh
gh workflow run desktop-release.yml -R claybowl/doer -f dry_run=true
# or locally from desktop/:
pnpm run make
```

## Linux (not yet implemented)

Plan is in project memory (`project_linux_desktop.md`): AppImage + deb makers, ubuntu-latest CI matrix. No auto-update support for Linux. Read that memory entry before starting.
