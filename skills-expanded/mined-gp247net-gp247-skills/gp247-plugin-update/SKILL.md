---
name: gp247-plugin-update
description: Updates a GP247 plugin that is already installed on a site to a newer release (for example plugin A from v1 to v2) and reports the result. It probes the installation, checks the newest version in the GP247 library and whether this site may take it, then follows the right case — an online 1-click update of a free plugin, an online update of a paid plugin that needs a valid license for the new version, or new source files already copied over the old ones (git pull, Composer, FTP, a .zip) whose database update and public/ files are still pending — guarding folders under development and explaining every refusal with the next step. Always use this skill when the user wants to update, upgrade or check for a new version of an installed plugin — for example "cập nhật plugin News", "nâng cấp plugin X lên bản mới", "plugin có bản mới chưa", "update plugin trả phí", "đã chép bản mới của plugin nhưng chưa áp dụng", "plugin báo Data update pending", "update all plugins". Trigger on Vietnamese, Japanese, or English phrasing of this intent — the team usually writes in Vietnamese, so do not wait for an exact English keyword match. Do not use this skill to install, enable, disable or uninstall a plugin (use gp247-extension-lifecycle), to update a template (use gp247-template-update), to create a plugin (use gp247-plugin-create), or to update gp247/core, front, shop or mcp themselves.
---

# gp247-plugin-update — Update an installed plugin to its new release

## Purpose

A site already runs plugin **A** at version **v1**; the user wants **v2**, usually "the newest release".
GP247 has exactly three ways to get there, and picking the wrong one either does nothing or deletes work:

| Case | When | What brings the new version | Who runs the data update |
| --- | --- | --- | --- |
| **A. Online, free** | The library offers a newer version of a free plugin | `gp247:ext-update` downloads, backs up, replaces `app/` and `public/`, runs the plugin's `update()`, restores the files if it fails | Core, in the same run |
| **B. Online, paid** | The same, for a paid plugin | As A, but the library sends the package only for a **license valid for the new version** | Core, in the same run |
| **C. Files already replaced** | The new source is already in `app/GP247/Plugins/<Key>/` (git pull, Composer, FTP, an extracted `.zip`), but the database and `public/GP247/Plugins/<Key>/` are still the old version | Already on disk | `gp247:ext-update --local` (or the admin **Apply data update** button, or `gp247:update`) |

This skill finds which case applies, checks the conditions before anything changes, runs it, verifies
the result and explains each refusal. It is the operational form of
`gp247-docs/extension/update-extension.md` for plugins.

**Never assume what the site's core offers.** Step 0 reads the running core and its commands; the
site's own `php artisan help gp247:ext-update` is the final word on any option.

## Output language

**English throughout** — commands, questions, progress notes and the final report, per the GP247
English-only rule. The user may write in Vietnamese, Japanese, or English; you respond in English. Never
translate command names, option flags, plugin keys or JSON envelope fields.

## When NOT to use

- **Installing, enabling, disabling or uninstalling** a plugin, or registering the site's API License —
  use `gp247-extension-lifecycle`.
- **Updating a template** — use `gp247-template-update` (a template update erases every direct edit in its
  folder, switches every store that uses it, and `GP247Front` moves with the gp247/front package).
- **Building a plugin** or preparing its next release — use `gp247-plugin-create` (or the payment /
  shipping create skills) and `gp247-docs/extension/create-plugin-update-safety.md`.
- **Updating GP247 itself** (core/front/shop/mcp) — `composer update` + `php artisan gp247:update`, see
  `gp247-docs/install-upgrade/update.md`. Do it first when the new plugin version needs a newer core.

## Input

Ask only for what is missing:

1. **Plugin key(s)** — the folder name under `app/GP247/Plugins/` (= `configKey`, case-sensitive), or
   "all plugins".
2. **Target** — the newest release by default. A **specific** older version cannot come from the library
   (it only serves its newest compatible release); it needs that version's files (case C).
3. **Where the new files are**, only if the user already has them (a `.zip`, a folder, a `git pull` they
   ran or want run).

A paid plugin's license is a **secret**: if the user gives one, use it in the command, never echo it back
or write it into a file or commit.

## Workflow

Run everything from the website root (where `artisan` lives). Prefer `--json` (if
`capabilities.json_output`) and parse the envelope
`{"ok", "command", "data", "warnings", "error": {"code", "message"}}`; always check the exit code.

0. **Probe the installation:**

   ```bash
   php <this-skill-dir>/scripts/gp247-probe.php
   ```

   - `bootstrapped: false` → report `bootstrap_error` and stop; artisan fails the same way.
   - `commands` must contain `gp247:ext-update` and `gp247:ext-list`; otherwise the core predates the CLI
     update — use the admin **Plugin** screen and say so.
   - `capabilities.ext_update_local` — `gp247:ext-update --local` exists (case C). Without it, case C has
     no data-update command: see case C in step 4.
   - `capabilities.ext_publish`, `capabilities.doctor` — re-copy and check static files.
   - Note `core` (the version compared with the plugin's `requireCore`). From core **3.14.3** the update
     also copies `public/` in case C and runs the data hook in a fresh process when another plugin had
     already loaded the plugin's code; older cores do neither.

1. **Read the plugin's local state.**

   ```bash
   php artisan gp247:ext-list --type=plugin --json
   php artisan gp247:ext-update --type=plugin --key=<Key> --local --dry-run --json   # if ext_update_local
   git -C app/GP247/Plugins/<Key> rev-parse --is-inside-work-tree 2>/dev/null        # working copy?
   ```

   - Not in the list, or **not installed** (files on disk only) → nothing to update; it needs installing
     (`gp247-extension-lifecycle`).
   - Read the dry run's JSON (some cores print a text line before it — parse the last line): `data.pending`
     lists the keys that would run (the versions are only in the text output: run once without `--json` to
     see `Pending: <Key> (<from> -> <to>)`); a plugin whose files and data already match is listed under `data.skipped`.
   - `<Key>` is in `data.pending` → the new files are **already on disk**: this is
     **case C**: skip step 2, confirm (step 3), then run case C in step 4. (`from` empty/`unknown` = a site installed before core recorded versions; the
     first apply clears it.)
   - The folder is a **git working copy** (or the user develops the plugin there) → **never** run the
     online update on it: it deletes the folder, `.git` and uncommitted work. The update for it is
     `git pull` (with the user's OK, on a clean tree) followed by case C.

2. **Check the newest version online** (cases A/B). The library needs the site's API License: `.env` has
   a non-empty `GP247_API_LICENSE` and `APP_URL` is the site's real domain. If not, stop and hand over to
   `gp247-extension-lifecycle` to register it (it writes `.env`).

   ```bash
   php artisan gp247:ext-search --type=plugin --keyword=<Key> --json        # newest version in the library, free or paid
   php artisan gp247:ext-check-update --type=plugin --force --json          # what THIS site may update to
   ```

   Read the two together:

   | `ext-search` | `ext-check-update` | Meaning | Next |
   | --- | --- | --- | --- |
   | `warnings` says the library is unreachable | (empty) | No connection — `ext-check-update` then says "No updates available" even though it could not ask | Fix the network / SSL / API License; do not report "up to date" |
   | version = local | empty | Up to date | Report it |
   | version > local | item `<Key>`, `require_license: false` | **Case A** | Step 3 |
   | version > local | item `<Key>`, `require_license: true` | **Case B** | Step 3 |
   | version > local | empty | The library does not offer it to this site — usually the new version needs a newer core (`requireCore`) | Update GP247 first (`gp247-docs/install-upgrade/update.md`), then check again |
   | no item for the key (search matches the name) | empty | Not a library plugin (custom or bought elsewhere) | Case C with the files from its author |

   `--force` bypasses the update cache (several hours); without it a just-published release may not show.

3. **Confirm the plan** in a few lines and wait for an explicit "yes": key, `<local> → <target>`, the case,
   what changes (A/B: both plugin folders are replaced, backup kept in
   `storage/backups/extensions/Plugins/<Key>/`; C: database update + static files), and anything found in
   the checks below. For several plugins, one line each.

   **Checks before changing anything:**
   - **Database backup** — the online update undoes file changes on failure but **not** what the plugin's
     `update()` already wrote. If the site's backup feature is on, core takes a snapshot first; otherwise
     ask the user to back up the database (or use `gp247:backup-*` if `commands` has it).
   - **Another plugin extends this one** (a Pro edition, an add-on — its `gp247.json`
     `requireGp247Extensions` lists `<Key>`) and the core is older than 3.14.3 → the update can run the old
     code's `update()` and fail. Update the extending plugin first if it has a new version, or disable it
     for the update and enable it afterwards.
   - **Write permission** on `app/GP247/Plugins`, `public/GP247/Plugins` and `storage/tmp` (A/B) or
     `public/GP247/Plugins` (C on core 3.14.3+). Without it core stops before touching any file.

4. **Run the case.**

   **A — online, free**

   ```bash
   php artisan gp247:ext-update --type=plugin --key=<Key> --json
   ```

   Success: `data.updated` contains `<Key>`. `data.up_to_date` = nothing newer. Anything else is in
   `data.failed` / `error.code` — see `references/update-troubleshooting.md`. `data_update_pending`
   (core 3.14.3+): the files are replaced but the data hook could not start in a child process — run the
   case C command it names.

   **B — online, paid**

   ```bash
   php artisan gp247:ext-license --type=plugin --key=<Key> --json           # stored license and its status
   php artisan gp247:ext-license --type=plugin --key=<Key> --license=<L>    # only if the user gives a (new) license
   php artisan gp247:ext-update  --type=plugin --key=<Key> --json
   ```

   The library sends the package only when the stored license covers the new version for this domain.
   A refusal names the reason — license missing, expired, invalid, bound to another domain, or not valid
   for this version — or says the plugin is **updated manually only**. Then the user renews or enters the
   license from the seller, or downloads the new version from the product page and continues with case C.
   Never try another license value on your own.

   **C — files already replaced (or about to be)**

   If the files are not on disk yet (the user has a `.zip` or folder, or asked for a `git pull`):
   1. Copy `app/GP247/Plugins/<Key>/` and `public/GP247/Plugins/<Key>/` aside (outside `app/GP247/Plugins`,
      e.g. `storage/backups/manual/<Key>_<version>/`) — the only way back on this path.
   2. Replace the **whole** source folder with the new one (the folder name must equal `configKey`; extract
      a `.zip` first — the admin Import refuses an installed plugin). For a working copy: `git pull`.
   3. Check `app/GP247/Plugins/<Key>/gp247.json`: `version` greater than the installed one, `requireCore`
      covering the probe's `core`.

   Then apply:

   ```bash
   php artisan gp247:ext-update --type=plugin --key=<Key> --local --dry-run          # expect: Pending: <Key> (<from> -> <to>)
   php artisan gp247:ext-update --type=plugin --key=<Key> --local --json             # runs the plugin's update('<from>')
   ```

   - Core **3.14.3+**: this copies the plugin's `public/` first; if that copy fails the data update does not
     run (fix the permission, run again).
   - **Older core**: `--local` does not copy static files — also run
     `php artisan gp247:ext-publish --type=plugin --key=<Key>` (if `ext_publish`; otherwise copy
     `app/GP247/Plugins/<Key>/public/` into `public/GP247/Plugins/<Key>/` by hand).
   - A failure exits non-zero, keeps the plugin pending and changes no file; fix the cause and run it again —
     re-running is the intended recovery.
   - **No `ext_update_local`** (very old core): there is no command to run the data update for files copied
     by hand. Say so; the options are updating GP247 first, or the online update (A/B) for a library plugin.

5. **Several plugins.** Online: `php artisan gp247:ext-update --type=plugin --all --json` updates every
   plugin the library offers; it exits 0 when **any** item succeeded, so read `data.failed`, and it skips
   nothing on its own — check first that none of them is a working copy (step 1). Files replaced by hand:
   `php artisan gp247:ext-update --type=plugin --all --local --json`. `php artisan gp247:update` also applies
   every pending plugin and template data update, but a failed one there is only a warning
   (`data.extension_data`).

6. **Verify.**

   ```bash
   php artisan gp247:ext-list --type=plugin --json                                   # version = target
   php artisan gp247:ext-update --type=plugin --key=<Key> --local --dry-run --json  # nothing pending
   php artisan gp247:doctor                                                           # if doctor: extension_assets, extension_data_pending
   ```

   Open a page that uses the plugin and reload with Ctrl+F5 (cached CSS/JS); purge a CDN if the site has
   one. If the admin shows stale menus or routes, `php artisan gp247:cache-rebuild`. If files were copied by
   hand and the site still runs the old code, PHP's OPcache holds it — restart PHP-FPM / the web server.

7. **Report** in the Output format. Do not commit anything in the plugin folder; a `git pull` the user
   approved is the only git action this skill takes.

## Output format

Do not print a document. Give a short English report (one line per plugin; `[x]` done, `[-]` nothing to
do, `[!]` refused or failed with the reason and the next step):

```
Plugin update on gp247/core <probe.core>:
- [x] <Key>: <old> → <new> (case A online free | B online paid | C files replaced) — data update applied, static files <copied by core | published>
- [-] <Key>: already up to date (<version>) | library version <v> needs a newer core
- [!] <Key>: <error.code / message> → <next step>
Backup: <core snapshot | user backup | none — reason>; file backup: storage/backups/extensions/Plugins/<Key>/<version>_<time> (A/B) | <manual copy path> (C)
State now: <version / pending / active per key from ext-list>
To check: reload pages with Ctrl+F5<; restart PHP if OPcache>
```

## Examples

The user may write in Vietnamese, Japanese, or English; you always respond in English.

**Example 1 — free plugin from the library**
Input: "Cập nhật plugin News lên bản mới nhất." → Probe; `ext-list`: News 3.0.6 installed, not a working
copy; dry run: nothing pending. `ext-search` shows 3.1.0 free; `ext-check-update --force` lists News 3.0.6 →
3.1.0, no license ⇒ case A. Confirm, then `gp247:ext-update --type=plugin --key=News --json`; verify 3.1.0,
nothing pending; report the backup folder.

**Example 2 — paid plugin, license expired**
Input: "Update plugin ProPlugin." → `ext-check-update` lists it with `require_license: true` ⇒ case B. The
update is refused: the license expired on its stated date. Report it with the two ways forward — renew and
run `gp247:ext-license --type=plugin --key=ProPlugin --license=<new>` then update again, or download the new version
from the product page and apply it as case C. Do not repeat any license value in the report.

**Example 3 — files already copied, data pending**
Input: "Tôi đã chép bản mới của plugin Booking lên server, admin báo Data update pending." → Dry run lists
Booking pending `1.4.2 -> 1.5.0` ⇒ case C, no download. Run `--local`; on core 3.14.3+ it copies `public/`
first; on an older core also `gp247:ext-publish --type=plugin --key=Booking`. Verify nothing pending, reload
with Ctrl+F5.

**Example 4 — new version exists but is not offered**
Input: "Plugin X có bản 2.0 rồi mà sao không thấy nút Update?" → `ext-search` shows 2.0, `ext-check-update
--force` lists nothing, library reachable ⇒ the release needs a newer core than the probe's `core`.
Report it; the next step is updating GP247 (`gp247-docs/install-upgrade/update.md`), then running this skill
again.

## Common mistakes

| Mistake | Why it hurts / how to avoid |
| --- | --- |
| Online update (`ext-update` without `--local`, or the admin Update button) on a folder under development | It deletes `app/…/<Key>` and `public/…/<Key>` with `.git` and uncommitted work. `git pull` + `--local`. |
| Reporting "up to date" from `ext-check-update` alone | It says "No updates available" also when the library could not be reached or the release needs a newer core. Cross-check with `ext-search` and its `warnings`. |
| Running the online update when the files are already new (case C) | It finds nothing newer in the library, or downloads over the files the user just placed. Dry-run `--local` first (step 1). |
| Copying only `app/` and stopping | The database and `public/` stay old: errors, old CSS/JS, "Data update pending". Always apply `--local` (and `ext-publish` on core < 3.14.3). |
| Merging the new files into the old folder | Files the new version removed linger and can still be loaded. Replace the whole folder. |
| Using the admin Import for the new `.zip` | Import is for new installs and refuses an installed plugin. Extract and follow case C. |
| Reading exit 0 of `ext-update --all` as "all updated" | It is non-zero only when every item failed. Read `data.failed`. |
| Treating `data_update_pending` as done | Files are replaced, the data update has not run. Run the `--local` command it names. |
| Retrying a paid update with guessed or other licenses | Licenses are bound to a domain and product; ask the user, never invent or reuse one, never print it. |
| Skipping the database backup because "the update rolls back" | Only files roll back; what `update()` wrote stays. |
| Adding `--skip-pre-change` on your own | It skips the backup snapshot. Only when the user confirms they have their own backup. |
| Updating a plugin that requires a newer core before updating GP247 | The library does not offer it, or install checks refuse it (`not compatible`). Update the platform first. |
| Forgetting OPcache or the browser cache after a manual copy | The site seems unchanged. Restart PHP; reload with Ctrl+F5; purge the CDN. |

## Bundled resources

- `scripts/gp247-probe.php` — step 0. Read-only; prints one JSON object (core version, `gp247:*` commands,
  capabilities). Identical copies ship with every gp247-* skill.
- `references/update-troubleshooting.md` — read when a step is refused or fails: every refusal and failure
  message of the update, what it means, the next step, and how to restore a plugin from core's file backup.

---

## Skill info

| Field | Value |
| --- | --- |
| Lần cuối cập nhật / Last updated | `2026-11-19` |
| Skill repo | https://github.com/gp247net/gp247-skills |
| GP247 core repo | https://github.com/gp247net/core |
| source | https://github.com/gp247net/gp247-docs/blob/main/extension/update-extension.md |
