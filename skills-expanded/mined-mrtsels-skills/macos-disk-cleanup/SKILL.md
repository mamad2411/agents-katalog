---
name: macos-disk-cleanup
description: Free macOS disk space (caches, leftovers, archive projects).
metadata:
  imported_from: hermes
---

# macOS Disk Cleanup

Systematic full-drive cleanup beyond `~/Library/Caches`: finding "invisible" space (APFS snapshots, sparse files, on-device AI models, container runtimes, uninstall leftovers) and archiving finished projects. Session-tested paths/commands: `references/systematic-cleanup.md`.

## Workflow (always follow this order)

1. **Recon**: `du -sh ~/* | sort -rh | head -40`, then drill into `~/Library/*`, `~/Library/Containers/*`, `/Applications/*`, `~/Library/Application Support/*`. Find files >500M: `find ~ -maxdepth 4 -type f -size +500M`.
2. **Classify**: safe caches (auto-rebuilt) vs user data (music library, photos, keynotes) vs gray zone (models, downloads).
3. **Confirm with user before irreversible deletes** — user may exempt specific items from the proposed list; execute exactly per exemptions.
4. **Execute** (pgrep first if anything might be running).
5. **Verify**: `df -h /` before/after, plus per-target checks.

## APFS gotchas (trust du, not ls)

- **Snapshots double-count**: `du -sh /System` can show 472G while the real system volume is ~13G (com.apple.os.update snapshot). Use `diskutil list` + `df -h /System/Volumes/Data` for the real picture.
- **Sparse files inflate ls**: Docker Desktop's `Docker.raw` shows 460G in `ls -lh` but actually occupies only ~1.1G (`du`). Sparse/APFS holes — do not panic, do not delete based on `ls`.

## Where "invisible" space hides

1. **Package caches** (safe, auto-rebuilt): `~/Library/Caches` (Homebrew, pip, colima, ms-playwright), `~/.cache/uv` (can be 8.8G!), `~/.npm` (npm cache clean --force + rm _cacache/_npx), `brew cleanup --prune=all`.
2. **Project datasets**: finished research projects often carry multi-GB gitignored datasets (e.g. `data/rico_local` 23G with a re-download script). Safe if gitignored + re-downloadable — confirm with user first.
3. **Apple Music offline downloads**: `~/Music/Apple Music Downloads` (subscription cache, can be 13G). Music library itself is user asset — never touch without explicit instruction.
4. **Chrome on-device AI models**: `~/Library/Application Support/Google/Chrome/OptGuideOnDeviceModel*` (4G+) + `optimization_guide_model_store` — cache cleaners never reach them. Quit Chrome (osascript), delete models + `Default/Service Worker/CacheStorage`, keep `Default/` user data.
5. **Apple container runtime**: `~/Library/Application Support/com.apple.container` (containerd-style: containers/buildkit, snapshots, content/blobs). Official `container image prune --all` needs `container system start` (heavy); with no daemon running (`pgrep containerization|vminit|buildkit|containerd`), deleting buildkit + `snapshots/*` + `content/blobs/*` is safe. Keep `kernels/`.
6. **Docker Desktop leftovers**: app uninstalled ≠ clean. Remaining: `~/Library/Containers/com.docker.docker` (VM disk), `/Library/PrivilegedHelperTools/com.docker.vmnetd` + `com.docker.socket`, LaunchDaemon plists, `docker context rm desktop-linux`. Full removal commands in references.
7. **Unused apps**: duplicates (iMovie vs FCP, CapCut vs VideoFusion, Telegram Lite/Swiftgram vs Telegram, ClashX vs Flclash+Shadowrocket), archived-project tools (NetBeans, NDI suite), iOS jailbreak/sideload tools, games.

## App removal: root-owned apps

App Store apps are **root-owned** (`drwxr-xr-x root`) — plain `rm -rf` fails with Permission denied on every file. Check ownership first (`ls -la /Applications | awk '{print $3, $NF}'`), then:

```bash
osascript -e 'do shell script "cd /Applications && rm -rf \"App Name.app\"" with administrator privileges'
```

Verify after: `for app in "..."; do [ -e "$app" ] && echo "still here: $app"; done` (no output = deleted).

## Archiving finished projects (reclaims space, keeps history)

1. **Commit + push uncommitted changes first** (`git add <specific paths>`, commit, push — never `git add .`).
2. **Multi-pushurl trap**: repos with a dead internal pushurl (e.g. ex-employer server) make `git push` exit non-zero even though GitHub push succeeded. Verify real state: `git log --oneline origin/main..HEAD` (empty = fully pushed). Check with `git config --get-regexp "remote\..*\.url|remote\..*\.pushurl"`.
3. **Archive**: `cd ~ && tar czf ~/Archives/<name>-<YYYYMMDD>.tar.gz --exclude='__pycache__' --exclude='.DS_Store' --exclude='.serena' <proj>` (background for multi-GB; gzip compresses `.git` poorly — already zlib'd).
4. **Verify archive**: `tar -tzf <archive> | wc -l` + grep key files (README/AGENTS/index.html).
5. **Delete originals**; leftover `.DS_Store` can cause "Directory not empty" — delete it separately.
6. **Before deleting the tarball later**: verify GitHub head commit matches archived state: `gh api "repos/<owner>/<repo>/commits?per_page=1" --jq '.[0].sha'` vs `git log -1`.
7. **Clean related leftovers**: container images, Docker contexts, app uninstalls, model caches (e.g. `~/.omlx` for oMLX).
8. For ex-employer projects: consider GitHub repo visibility (private) — check `gh repo view <repo> --json visibility` before assuming.

## Pitfalls

- `brew cleanup --prune=all` frees GBs the caches dir doesn't show (formula versions).
- `du` on deep dirs can time out — target subdirectories instead of `~/*`.
- Verify data directory is gitignored before trusting "re-downloadable" (check `.gitignore` for data/raw/processed).
- Trash check: `du -sh ~/.Trash` — sometimes overlooked.
- User preference: irreversible deletions need explicit confirmation; exempt items are honored exactly.
