---
name: gp247-template-update
description: Updates a GP247 storefront template (theme) that is already installed on a site to a newer release (for example template T from v1 to v2) and reports the result. It probes the installation, checks the newest version in the GP247 library and whether this site may take it, finds which stores use the template and whether its folder holds local edits that an update would erase, then follows the right case — an online 1-click update of a free template, an online update of a paid template that needs a valid license for the new version, or new template files already copied over the old ones whose database update and public/ files are still pending. The default GP247Front template is routed to its own path (it moves with the gp247/front package). Always use this skill when the user wants to update, upgrade or check for a new version of an installed template or theme — for example "cập nhật template", "nâng cấp giao diện lên bản mới", "theme có bản mới chưa", "update template trả phí", "đã chép bản mới của template nhưng chưa áp dụng", "template báo Data update pending", "cập nhật GP247Front". Trigger on Vietnamese, Japanese, or English phrasing of this intent — the team usually writes in Vietnamese, so do not wait for an exact English keyword match. Do not use this skill to install, activate, disable or remove a template (use gp247-extension-lifecycle), to create a template (use gp247-template-create), or to update a plugin (use gp247-plugin-update).
---

# gp247-template-update — Update an installed template to its new release

## Purpose

A site already runs template **T** at version **v1**; the user wants **v2**, usually "the newest release".
Templates update through the same engine as plugins, with three cases:

| Case | When | What brings the new version | Who runs the data update |
| --- | --- | --- | --- |
| **A. Online, free** | The library offers a newer version of a free template | `gp247:ext-update --type=template` downloads, backs up, **deletes and replaces** `app/GP247/Templates/<Key>/` and `public/GP247/Templates/<Key>/`, runs the template's `update()`, restores the files if it fails | Core, in the same run |
| **B. Online, paid** | The same, for a paid template | As A, but the library sends the package only for a **license valid for the new version** | Core, in the same run |
| **C. Files already replaced** | The new template files are already in `app/GP247/Templates/<Key>/` (git pull, FTP, an extracted `.zip`), but the database and `public/GP247/Templates/<Key>/` (compiled CSS/JS, images) are still the old version | Already on disk | `gp247:ext-update --type=template --local` (or **Apply data update**, or `gp247:update`) |

What makes a template different from a plugin, and why this skill exists:

- **The update replaces the whole folder.** Any edit made directly in the template's files — a changed
  view, colour, image, compiled CSS — is **gone** after cases A/B (core keeps a backup copy, not a merge).
  Settings saved through the admin (the template's customize screen) live in the database and stay.
- **The template is live.** Every store whose template field names it shows the new version immediately.
- **`GP247Front` is not updated here.** The default template's views and assets come from the
  `gp247/front` / `gp247/shop` packages and move with `composer update` + `php artisan gp247:update`; files
  published into `app/GP247/Templates/GP247Front/` are frozen copies that block those fixes (step 2).

It is the operational form of `gp247-docs/extension/update-extension.md` and
`gp247-docs/cli/cli-templates.md` for templates.

**Never assume what the site's core offers.** Step 0 reads the running core and its commands; the site's
own `php artisan help gp247:ext-update` is the final word on any option.

## Output language

**English throughout** — commands, questions, progress notes and the final report, per the GP247
English-only rule. The user may write in Vietnamese, Japanese, or English; you respond in English. Never
translate command names, option flags, template keys or JSON envelope fields.

## When NOT to use

- **Installing, activating for a store, disabling or removing** a template — use
  `gp247-extension-lifecycle`.
- **Creating a template**, or porting a template to a newer package — use `gp247-template-create`.
- **Updating a plugin** — use `gp247-plugin-update`.
- **Updating GP247 itself** (core/front/shop/mcp) — `composer update` + `php artisan gp247:update`, see
  `gp247-docs/install-upgrade/update.md`. This is also how `GP247Front` gets its new version.

## Input

Ask only for what is missing:

1. **Template key** — the folder name under `app/GP247/Templates/` (= `configKey`, case-sensitive).
2. **Target** — the newest release by default. A specific older version cannot come from the library (it
   serves only its newest compatible release); it needs that version's files (case C).
3. **Local edits** — whether anyone edited the template's files directly on this site. Step 1 looks for
   evidence; the user's answer decides.
4. **Where the new files are**, only if the user already has them (a `.zip`, a folder, a `git pull`).

A paid template's license is a **secret**: use it in the command, never echo it back or write it into a
file or commit.

## Workflow

Run everything from the website root. Prefer `--json` (if `capabilities.json_output`) and parse the
envelope `{"ok", "command", "data", "warnings", "error": {"code", "message"}}` — some cores print a text
line before it, so parse the last line; always check the exit code.

0. **Probe the installation:**

   ```bash
   php <this-skill-dir>/scripts/gp247-probe.php
   ```

   - `bootstrapped: false` → report `bootstrap_error` and stop.
   - `commands` must contain `gp247:ext-update` and `gp247:ext-list`; otherwise use the admin **Template**
     screen and say so. `gp247:template-prune` / `gp247:template-publish` exist only with gp247/front's
     vendor-resident templates (`capabilities.template_vendor_views`).
   - `capabilities.ext_update_local` — `--local` exists (case C). `capabilities.ext_publish`,
     `capabilities.doctor` — re-copy and check static files.
   - Note `core`. From core **3.14.3** the update copies `public/` in case C and runs the data hook in a fresh
     process when needed; older cores do neither.

1. **Read the template's local state.**

   ```bash
   php artisan gp247:ext-list --type=template --json
   php artisan gp247:ext-update --type=template --key=<Key> --local --dry-run --json   # if ext_update_local
   git -C app/GP247/Templates/<Key> status --short 2>/dev/null                          # working copy? local edits?
   php artisan tinker --execute="dump(\GP247\Core\Models\AdminStore::query()->pluck('template','id')->all());"
   ```

   - `<Key>` is `GP247Front` → step 2, not the cases below.
   - Not installed (on disk only) → nothing to update; it needs installing (`gp247-extension-lifecycle`).
   - `<Key>` is in `data.pending` (the versions are only in the text output: run once without `--json` to
     see `Pending: <Key> (<from> -> <to>)`) → the new files are **already on disk**: **case C**;
     skip the online check, confirm (step 4), run case C. A template already in sync is under `data.skipped`.
   - **Stores using it** — the store ids whose template is `<Key>`; they all change at once. Say so in the plan.
   - **Local edits** — the folder is a git working copy (with or without uncommitted changes), or the user
     says files were edited, or files under `app/GP247/Templates/<Key>/` are newer than its `gp247.json`
     (`find app/GP247/Templates/<Key> -newer app/GP247/Templates/<Key>/gp247.json -type f`, a hint only).
     A **working copy** must never get the online update (it deletes the folder, `.git` and uncommitted
     work): update it with `git pull` (user's OK, clean tree) and case C. **Edited files** in a normal
     install: tell the user they will be erased, and offer the way to keep them (step 4).

2. **`GP247Front` — the default template.** Do not run `ext-update` on it. Its new version arrives with the
   packages:
   - `composer update` (as the site normally runs it) then `php artisan gp247:update` — the platform update;
     the storefront CSS/JS in `public/GP247/Templates/GP247Front/` refresh themselves.
   - Files published into `app/GP247/Templates/GP247Front/` **win over the package and never receive its
     fixes**. List them with `php artisan gp247:doctor` (row `template_source`) and hand back the ones nobody
     edited:

     ```bash
     php artisan gp247:template-prune GP247Front --dry-run    # lists files identical to the package copy
     php artisan gp247:template-prune GP247Front              # deletes only those, after the user agrees
     ```

     Prune keeps every edited file, files the package does not have, and the extension shell. Edited files
     stay frozen: compare each with the package copy
     (`vendor/gp247/{front,shop}/src/Views/templates/GP247Front/<path>`) and port the package's changes into
     it by hand, or delete it to take the package version.
   - Never run `vendor:publish --tag=gp247:front-view --force` or `--tag=gp247:shop-view-front --force` to
     "update" it: they overwrite the whole tree and freeze every file again.

   Report and stop; the rest of the workflow is for other templates.

3. **Check the newest version online** (cases A/B). The library needs the site's API License (`.env` has
   a non-empty `GP247_API_LICENSE`, `APP_URL` is the real domain); if missing, hand over to
   `gp247-extension-lifecycle` to register it.

   ```bash
   php artisan gp247:ext-search --type=template --keyword=<Key> --json     # newest version in the library, free or paid
   php artisan gp247:ext-check-update --type=template --force --json       # what THIS site may update to
   ```

   | `ext-search` | `ext-check-update` | Meaning | Next |
   | --- | --- | --- | --- |
   | `warnings` says the library is unreachable | (empty) | No connection — `ext-check-update` still says "No updates available" | Fix network / SSL / API License; do not report "up to date" |
   | version = local | empty | Up to date | Report it |
   | version > local | item `<Key>`, `require_license: false` | **Case A** | Step 4 |
   | version > local | item `<Key>`, `require_license: true` | **Case B** | Step 4 |
   | version > local | empty | Not offered to this site — usually the new version needs a newer core or gp247/front | Update GP247 first, then check again |
   | no item for the key (search matches the name) | empty | Not a library template (custom or bought elsewhere) | Case C with the files from its author |

4. **Confirm the plan** and wait for an explicit "yes": key, `<local> → <target>`, the case, the stores that
   switch to the new version, and for A/B: both template folders are **replaced**, every direct file edit is
   erased, backup in `storage/backups/extensions/Templates/<Key>/`.

   **If the template has local edits** (step 1), offer before updating:
   - keep a copy of the current folders outside `app/GP247/Templates/` (core's backup keeps only the newest
     3 per template), and after the update compare it with the new version to re-apply the edits that are
     still wanted; or
   - leave the template as it is (no update), or move the edits into a template of its own name
     (`gp247-template-create`) so later updates never touch them.

   **Other checks:**
   - **Database backup** — the online update undoes file changes on failure, not what the template's
     `update()` wrote. With the site's backup feature on, core takes a snapshot first; otherwise ask the user
     to back up the database (or use `gp247:backup-*` if `commands` has it).
   - **Requirements of the new version** — its `requireCore`, `requireComposerPackages` (always `gp247/front`,
     often `gp247/shop`) and `requireGp247Extensions` must be met, or the update is refused as not compatible.
   - **Write permission** on `app/GP247/Templates`, `public/GP247/Templates` and `storage/tmp` (A/B) or
     `public/GP247/Templates` (C on core 3.14.3+).
   - A busy storefront: suggest a quiet time — the stores render the new files the moment they are copied.

5. **Run the case.**

   **A — online, free**

   ```bash
   php artisan gp247:ext-update --type=template --key=<Key> --json
   ```

   Success: `data.updated` contains `<Key>`; `data.up_to_date` = nothing newer; otherwise `data.failed` /
   `error.code` — see `references/update-troubleshooting.md`. `data_update_pending` (core 3.14.3+): files are
   replaced, the data hook must run — run the case C command it names.

   **B — online, paid**

   ```bash
   php artisan gp247:ext-license --type=template --key=<Key> --json           # stored license and its status
   php artisan gp247:ext-license --type=template --key=<Key> --license=<L>    # only if the user gives a (new) license
   php artisan gp247:ext-update  --type=template --key=<Key> --json
   ```

   A refusal names the reason — license missing, expired, invalid, bound to another domain, not valid for
   this version — or says the template is **updated manually only**. Then the user renews or enters the
   license from the seller, or downloads the new version from the product page and continues with case C.
   Never try another license value on your own.

   **C — files already replaced (or about to be)**

   If the files are not on disk yet:
   1. Copy `app/GP247/Templates/<Key>/` and `public/GP247/Templates/<Key>/` aside (outside
      `app/GP247/Templates`, e.g. `storage/backups/manual/<Key>_<version>/`) — the only way back here.
   2. Replace the **whole** template folder with the new one (folder name = `configKey`; extract a `.zip`
      first — Import refuses an installed template). For a working copy: `git pull`.
   3. Check `app/GP247/Templates/<Key>/gp247.json`: `version` greater than the installed one, `requireCore`
      covering the probe's `core`.

   Then apply:

   ```bash
   php artisan gp247:ext-update --type=template --key=<Key> --local --dry-run          # expect: Pending: <Key> (<from> -> <to>)
   php artisan gp247:ext-update --type=template --key=<Key> --local --json
   ```

   - Core **3.14.3+** copies the template's `public/` (compiled CSS/JS) first; if that fails the data update
     does not run — fix the permission, run again.
   - **Older core**: also `php artisan gp247:ext-publish --type=template --key=<Key>` (if `ext_publish`;
     otherwise copy `app/GP247/Templates/<Key>/public/` into `public/GP247/Templates/<Key>/` by hand). Without
     it the stores run the new views with the old CSS.
   - A failure exits non-zero, keeps the template pending, changes no file; fix the cause and run again.
   - **No `ext_update_local`** (very old core): no command runs the data update for hand-copied files; the
     options are updating GP247 first, or the online update (A/B) for a library template.

6. **Verify.**

   ```bash
   php artisan gp247:ext-list --type=template --json                                    # version = target, active
   php artisan gp247:ext-update --type=template --key=<Key> --local --dry-run --json   # nothing pending
   php artisan gp247:doctor                                                              # if doctor: extension_assets, extension_data_pending
   ```

   Open the home page, a category, a product, the cart and checkout of **one store per template user**, in a
   private window, reloading with Ctrl+F5; purge a CDN if the site has one. Check the template's customize
   screen still shows the saved settings. Stale views or menus → `php artisan gp247:cache-rebuild`; after a
   manual copy, OPcache may hold old PHP — restart PHP-FPM / the web server.

7. **Report** in the Output format. Do not commit anything in the template folder; a `git pull` the user
   approved is the only git action this skill takes.

## Output format

Do not print a document. Give a short English report:

```
Template update on gp247/core <probe.core>:
- [x] <Key>: <old> → <new> (case A online free | B online paid | C files replaced) — data update applied, static files <copied by core | published>
- [-] <Key>: already up to date (<version>) | library version <v> needs a newer core / gp247/front
- [!] <Key>: <error.code / message> → <next step>
- GP247Front: <updated with the packages | prune: n files handed back, m edited files still frozen | not touched>
Stores on the new version: <store ids>
Local edits: <none found | kept in <path>, re-apply by comparing with the new version | user chose not to update>
Backup: <core snapshot | user backup | none — reason>; file backup: storage/backups/extensions/Templates/<Key>/<version>_<time> (A/B) | <manual copy path> (C)
To check: storefront pages per store with Ctrl+F5<; purge CDN><; restart PHP if OPcache>
```

## Examples

The user may write in Vietnamese, Japanese, or English; you always respond in English.

**Example 1 — free template from the library**
Input: "Cập nhật template ShopTheme lên bản mới nhất." → `ext-list`: installed 1.0.3, active; not a working
copy, no file newer than `gp247.json`; stores 1 and 2 use it. `ext-search` 1.1.0 free; `ext-check-update
--force` lists 1.0.3 → 1.1.0 ⇒ case A. Confirm (stores 1 and 2 switch, folder replaced), run
`gp247:ext-update --type=template --key=ShopTheme --json`, verify, check one page per store.

**Example 2 — paid template with edits on the server**
Input: "Update theme ProTheme." → `ext-check-update` lists it with `require_license: true` ⇒ case B. Several
views are newer than `gp247.json` and the user confirms they edited the header. Offer to save the current
folders under `storage/backups/manual/ProTheme_<version>/` and to compare afterwards; on "yes", save, check
the license with `ext-license`, update, then list the files that differ between the saved copy and the new
version so the user re-applies the header change.

**Example 3 — the default template**
Input: "Cập nhật GP247Front." → Not an `ext-update`: point to `composer update` + `php artisan gp247:update`.
`gp247:doctor` shows 38 files frozen in `app/GP247/Templates/GP247Front/`; `template-prune --dry-run` finds 35
identical to the package. With the user's OK prune them; report the 3 edited files that still block package
fixes.

**Example 4 — files copied by FTP**
Input: "Tôi đã upload bản mới của template lên, trang bị vỡ CSS." → Dry run lists the template pending
`2.0.1 -> 2.1.0` ⇒ case C. Run `--local`; on a core older than 3.14.3 also `ext-publish --type=template`.
Verify, reload with Ctrl+F5.

## Common mistakes

| Mistake | Why it hurts / how to avoid |
| --- | --- |
| Online update of a template with direct file edits, without telling the user | The whole folder is replaced; the edits are only in core's backup (3 newest kept). Find the edits first, offer a copy and a compare. |
| Online update (`ext-update` without `--local`, or the admin Update button) on a working copy | Deletes `app/…/<Key>` and `public/…/<Key>` with `.git` and uncommitted work. `git pull` + `--local`. |
| Running `ext-update` on `GP247Front` | It moves with the gp247/front package. `composer update` + `gp247:update`, then `template-prune`. |
| `vendor:publish --tag=gp247:front-view --force` to refresh GP247Front | Overwrites the whole tree and freezes every file against later fixes. Use `template-prune` / `template-publish --file=`. |
| Reporting "up to date" from `ext-check-update` alone | It says "No updates available" also when the library is unreachable or the release needs a newer core. Cross-check with `ext-search`. |
| Copying only the views and stopping | The database and the compiled CSS in `public/` stay old: broken styling, "Data update pending". Apply `--local` (+ `ext-publish` on core < 3.14.3). |
| Forgetting which stores use the template | They all change at once; check one page per store. |
| Forgetting `--type=template` | Commands default to `plugin`; the key is then not found. |
| Retrying a paid update with guessed or other licenses | Licenses are bound to a domain and product; ask the user, never print one. |
| Skipping the database backup because "the update rolls back" | Only files roll back. |
| Adding `--skip-pre-change` on your own | It skips the backup snapshot. Only when the user confirms their own backup. |
| Forgetting the browser / CDN / OPcache after a manual copy | The storefront seems unchanged or half-styled. Ctrl+F5, purge, restart PHP. |

## Bundled resources

- `scripts/gp247-probe.php` — step 0. Read-only; prints one JSON object (core version, `gp247:*` commands,
  capabilities). Identical copies ship with every gp247-* skill.
- `references/update-troubleshooting.md` — read when a step is refused or fails: every refusal and failure
  message, the next step, restoring from core's file backup, and comparing a saved copy with the new
  version.

---

## Skill info

| Field | Value |
| --- | --- |
| Lần cuối cập nhật / Last updated | `2026-11-19` |
| Skill repo | https://github.com/gp247net/gp247-skills |
| GP247 core repo | https://github.com/gp247net/core |
| source | https://github.com/gp247net/gp247-docs/blob/main/extension/update-extension.md · https://github.com/gp247net/gp247-docs/blob/main/cli/cli-templates.md |
