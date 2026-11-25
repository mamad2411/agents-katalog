---
name: alidocs
description: Download a DingTalk / alidocs document — or a whole folder, or an entire knowledge base — from a shared link, to local disk. Also upload local files / sync a local directory tree up into an alidocs folder. Use this skill whenever the user gives an alidocs.dingtalk.com link and wants to fetch docs locally, or asks to push files up to alidocs.
---

# alidocs Skill

You move files between local disk and DingTalk / alidocs:

- **fetch / download** — give it a link and it mirrors that subtree: a single
  doc downloads just that doc, a folder downloads everything under it, and a
  knowledge-base overview link (`/i/spaces/<spaceId>/overview`) downloads the
  whole space.
- **push / sync** — give it a local path + an alidocs folder link and it
  uploads files/directories, preserving folder structure. `sync` is `push`
  with `--prune` enabled when the user asks for one-way mirroring.

## Tool

- `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/alidocs.py <subcmd>`

## Dependencies

```
pip install requests        # always
pip install oss2            # required for push/sync (OSS uploads)
pip install playwright && playwright install chromium   # only for online-doc export
```

Without `oss2` the upload commands (`push`, `sync`) fail with a clear install
hint. Without Playwright the download still works, but online docs are saved
as `.url` shortcuts (+ `.meta.json`) instead of exported files. The script
auto-detects Playwright; pass `--no-playwright` to force shortcut mode.

## Config

Credentials come from env or `~/.taku/alidocs.json` (legacy `~/.alidocs/config.json`
still read; override the dir with `TAKU_DIR`). The cookie is the full `Cookie:`
request header copied from a logged-in alidocs browser session.

```json
{
  "cookie": "cna=...; doc_atoken=...; XSRF-TOKEN=...; ...",
  "default_out_dir": "~/Downloads/alidocs",
  "use_playwright": true
}
```

- `cookie` (or `cookie_file`: path to a file holding the cookie) — required.
  The `a-token` is auto-extracted from the `doc_atoken` cookie.
- `default_out_dir` — where downloads go when `--out` isn't passed (default `~/Downloads/alidocs`).
- `use_playwright` — force on/off; omit to auto-detect.
- `space_id` — optional; auto-discovered from the link's page otherwise.

Do NOT prompt the user for the cookie inline — they put it in the config file
(`chmod 600`, it contains session tokens).

### Multiple accounts (profiles)

Instead of a flat config, the file can hold a `profiles` map for multiple
accounts (personal vs work, etc.) — same shape as the other taku plugins:

```json
{
  "default_profile": "personal",
  "default_out_dir": "~/Downloads/alidocs",
  "profiles": {
    "personal": { "cookie_file": "~/.taku/alidocs.personal.cookie" },
    "work":     { "cookie_file": "~/.taku/alidocs.work.cookie",
                  "default_out_dir": "~/Documents/work-alidocs" }
  }
}
```

- Pick a profile with `--profile NAME` or `ALIDOCS_PROFILE`; else
  `default_profile`, else the sole profile. A flat config (no `profiles`) is
  the implicit `default`.
- Top-level keys outside `profiles` are shared defaults merged into each profile.
- Pass `--profile` BEFORE the subcommand: `alidocs.py --profile work fetch ...`.

## Workflow — download

1. **Verify** the link + cookie resolve (cheap, no download):
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/alidocs.py check --url "<link>"
   # -> {"ok": true, "name": "...", "is_folder": true/false, "has_children": ...}
   ```
   If it errors with a 401/auth message, the cookie is stale — tell the user to
   refresh it in `~/.taku/alidocs.json`.

2. **Download**:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/alidocs.py fetch --url "<link>" [--out DIR]
   ```
   - No `--out` → goes to the configured `default_out_dir`.
   - Final stdout line is a JSON summary: `{"ok", "root", "out_dir", "playwright", "stats": {...}}`.

3. **Report** to the user: the output directory, and the `stats`
   (folders / files / exported / online_docs / skipped / errors). If
   `playwright` is false and there were `online_docs`, mention they were saved
   as `.url` shortcuts and how to enable full export.

## Workflow — upload / sync

1. **Pick a destination folder.** The user gives you a folder link
   (`/i/nodes/<folderUuid>`). The personal-space root is NOT addressable;
   if they don't have a folder yet, ask them to create one in the UI OR use
   `--create-dest <existing-link>::path/to/leaf` to auto-create one.

2. **Always do a dry-run first** for any non-trivial push so the user can
   review the plan:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/alidocs.py push \
       --src ./local/path --dest "<folder-link>" --dry-run
   ```
   Output prints one line per action with these markers:
   ```
     + dir    foo/                          ← create folder
     + file   foo/a.txt                     ← upload (new)
     ~ file   foo/b.txt   [size 1230→1450]  ← overwrite (in-place version bump)
     = file   foo/c.txt   [same size]       ← skip
     - file   foo/old.txt                   ← prune (only with --prune)
     ! file   foo/big.bin [12MB > max-size] ← warning, not uploaded
   ```

3. **Apply.** Drop `--dry-run`, add `--yes` if non-interactive:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/alidocs.py push \
       --src ./local/path --dest "<folder-link>" --yes
   ```
   - Default `--on-conflict` is `skip-if-same` (only overwrite if size differs).
     Force overwrite with `--on-conflict overwrite`; force a `(N)` duplicate
     with `--on-conflict rename`.
   - Add `--prune` to recycle remote files that have no local counterpart
     (soft-delete; recoverable from alidocs trash).
   - Excludes by default: `.*` `__pycache__` `node_modules` `*.pyc` `.DS_Store`.
     Override with `--exclude` (repeatable) and/or restrict with `--include`.
   - Final stdout line is JSON: `{"ok", "dest", "space_id", "dest_uuid", "stats": {...}}`.

4. **Sync.** `sync` is identical to `push` today (both default to
   `skip-if-same`). Use `sync --prune` when the user wants true one-way mirror.

## Notes

- Links accepted everywhere: a doc, a folder, or a whole knowledge base
  (`/i/spaces/<id>/overview`). Same command; no need to ask which.
- Download re-runs are idempotent (skip already-downloaded). Push re-runs
  with the default `skip-if-same` are also idempotent.
- Permission errors on a doc mean the account lacks 可查看/下载 rights —
  surface that, don't retry blindly.
- `.md`/`.docx`/`.txt` are uploaded as **binary attachments** (downloadable
  text), NOT converted to editable online docs. Server-side conversion via
  `/box/api/v2/import/document` requires an internal RPC bridge (`/r/Adaptor/...`)
  that isn't reachable from cookie-only HTTP auth on the public cloud — this
  is a known limitation; users who need an online `.adoc` should convert in
  the alidocs UI after upload.
- This skill writes files locally AND remotely. For destructive operations
  (`--prune`, `--on-conflict overwrite`) confirm with the user unless they
  explicitly passed `--yes`.
