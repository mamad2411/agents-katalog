---
name: gp247-extension-lifecycle
description: Installs, enables, disables, upgrades, and uninstalls existing GP247 extensions — both plugins and templates — from the command line using the `gp247:ext-*` command family, and reports each result. It probes the installation first and uses only the commands and options the site's gp247/core actually has. Always use this skill when the user wants to manage the lifecycle of an already-built extension — install a plugin from a `.zip`, an extracted folder, or a marketplace key; enable or disable it; update one or all to a new release; apply the data update after files were changed by git or composer; re-publish its static files; uninstall or purge it; register the site's API license to connect the GP247 library; set a paid license; or list / check what is installed and what has updates — for example "cài plugin News", "gỡ plugin X", "bật/tắt template", "cập nhật license plugin". Trigger on Vietnamese, Japanese, or English phrasing of this intent — the team usually writes in Vietnamese, so do not wait for an exact English keyword match. Do not use this skill to update an installed plugin or template to a newer release (use gp247-plugin-update / gp247-template-update), to CREATE or scaffold a NEW plugin (use gp247-plugin-create) or a new template (use gp247-template-create), or to update the GP247 platform packages (core/front/shop) themselves after `composer update` — that is `gp247:update`, documented in gp247-docs `install-upgrade/update`.
---

# gp247-extension-lifecycle — Install, upgrade & remove GP247 extensions from the CLI

## Purpose

Drive the full lifecycle of an **already-built** GP247 extension (a plugin or a template) with the
`gp247:ext-*` command family — install, enable, disable, update, apply data updates, re-publish assets,
uninstall/purge, license, and inspect. The CLI runs the **same** engine as the admin buttons, so behavior
is identical, but scriptable and usable on servers with no admin access.

This skill picks the correct command, checks the current state first, guards the destructive operations,
and reports a clear per-item result. It is the operational counterpart to
`gp247-docs/cli/cli-extensions.md`.

**Never assume what the site's core offers.** The command family grows between core releases. Step 0
reads the site's actual commands and options; the site's own `php artisan help <command>` is the final
word on any flag — this skill and its matrix are a guide to it, not a substitute.

## Output language

**English throughout** — the commands you run, the questions you ask, progress notes, and the final
status report are all in English, per the GP247 English-only rule. The user may write in Vietnamese,
Japanese, or English (see the trigger note in the description); you respond in English. Never translate
command names, option flags, extension keys, or JSON envelope fields.

## When NOT to use

- **Creating / scaffolding a NEW plugin** — use `gp247-plugin-create`. This skill only manages extensions
  that already exist as a `.zip`, an on-disk folder, or a marketplace item.
- **Creating a NEW storefront template** — use `gp247-template-create`.
- **Updating an installed plugin or template to a newer release** — checking the newest version, the online update of a
  free or paid plugin, or applying new files copied over the old ones — use `gp247-plugin-update`, which
  covers each case and its failures in depth. For a template, use `gp247-template-update`.
- **Updating the GP247 platform itself** (core/front/shop/mcp) after `composer update` — that is
  `gp247:update`, not an extension operation; see `gp247-docs/install-upgrade/update.md`. (It also applies
  pending extension data updates — see step 3.)
- **Only explaining** how the lifecycle works with no intent to run it — answer directly or point at
  `gp247-docs/cli/cli-extensions.md`.

## Input

What operation the user wants, on which extension. Determine four things before running anything —
ask only for the ones that are genuinely missing:

1. **Operation** — install · enable · disable · update · apply data update · re-publish assets ·
   uninstall · license · list/check.
2. **Type** — `plugin` (default) or `template`. The `gp247:ext-*` commands that act on extensions take
   `--type=plugin|template` (`ext-register-license` takes no option at all).
3. **Target** — the extension **key** (e.g. `News`), or, for install, a **source**: a `.zip` (`--file=`),
   an extracted **folder** (`--dir=`), or a marketplace **key** (`--key=`).
4. **Paid?** — a paid marketplace install also needs `--paid` and a `--license=<key>`. Treat the license
   value as a **secret**: never echo it back, never write it to a doc or commit. It is stored in
   `admin_config`, never in `.env`. Do not confuse it with the site's free **API License**
   (`GP247_API_LICENSE` in `.env`), which every library download needs — see step 2.

Run every command from the **website root** (where `artisan` lives). If the user did not say `plugin` vs
`template` and the key is ambiguous, ask; otherwise default to `plugin`.

## Workflow

Do the steps in order. Prefer `--json` so you parse the envelope
(`{"ok":..., "command":..., "data":..., "warnings":[], "error":{"code","message"}}`) instead of scraping
text, and check the **exit code** on every run (its meaning per command is in the matrix).

0. **Probe the installation** with the bundled read-only script and keep its JSON:

   ```bash
   php <this-skill-dir>/scripts/gp247-probe.php
   ```

   - `commands` lists the `gp247:*` commands this site has. **Only run a command that is in the list.**
     If the operation needs one that is missing (e.g. `gp247:ext-publish`, `gp247:ext-register-license`),
     tell the user their core does not have it and give the admin-screen alternative instead of
     improvising a substitute.
   - `capabilities.ext_update_local` — whether `gp247:ext-update --local` exists (apply a data update
     without downloading); `capabilities.json_output` — whether `--json` is accepted.
   - Before using any option you are not sure of, run `php artisan help gp247:<command>` and follow it.
   - `bootstrapped: false` → the app cannot boot (see `bootstrap_error`); artisan commands will fail the
     same way — report that and stop.

1. **Confirm the plan in one line.** Restate operation + type + target key(s). For a **destructive**
   operation, state the impact and get an explicit "yes" before running:
   - `ext-uninstall` without `--only-data`, and `--purge` — **delete the extension's folders**
     `app/GP247/<Plugins|Templates>/<Key>` and `public/GP247/<Plugins|Templates>/<Key>`;
   - `ext-update` from the library — **deletes and replaces** those two folders with the downloaded release
     (a backup is kept, see below);
   - a paid `ext-install` — spends a license.

   **If the extension folder is a working copy** (it contains `.git/`, or the user is developing it):
   never run `ext-update` from the library or a plain `ext-uninstall` on it — the folder, its `.git` and
   any uncommitted work are deleted. Update it with `git pull` then `ext-update --local` (step 3); remove
   its data with `ext-uninstall --only-data`.

   Also confirm before `ext-register-license`: it writes `.env` and binds the license to the domain in
   `APP_URL`.

2. **Check current state first** with a read-only command (no marketplace call, safe to run anytime):

   ```bash
   php artisan gp247:ext-list --type=plugin --json
   ```

   This shows, per local extension, whether it is **installed** (has an `admin_config` row — *not* merely
   present on disk), **active**, its version (from its `gp247.json`), and whether an update is cached as
   available. It does **not** show a pending data update; for that run
   `php artisan gp247:ext-update --type=<t> --local --all --dry-run` or `gp247:doctor`
   (`extension_data_pending`). For library updates, also run
   `php artisan gp247:ext-check-update --type=<t>` (add `--force` to bypass the cache).

   **Library connection** — needed only when a command must reach the GP247 library: `ext-install --key`
   for an extension that is **not on disk**, `ext-update` without `--local`, `ext-search`,
   `ext-check-update --force`. Check that `.env` has a non-empty `GP247_API_LICENSE` and that `APP_URL` is
   the site's **real domain** (not `http://localhost`). If the license is missing and
   `gp247:ext-register-license` is available, register it once (after confirming, step 1):

   ```bash
   php artisan gp247:ext-register-license
   ```

   If `.env` is not writable the command exits non-zero (`env_write_failed`) and prints the key for the
   user to paste into `.env` — do not repeat the key in your report. Also check the target's
   `gp247.json` prerequisites: install only **checks** `requireCore`, `requireComposerPackages` (run
   `composer require` first) and `requireGp247Extensions` (install those extensions first).

3. **Run the operation.** Pick the command from the table; full options, exit codes and failure codes are
   in `references/command-matrix.md`.

   | Operation | Command | Notes |
   | --- | --- | --- |
   | List local | `gp247:ext-list --type=<t>` | Cache-only, no API call. |
   | Register API License | `gp247:ext-register-license` | Once per site, before any library download. Needs the real `APP_URL`. |
   | Search marketplace | `gp247:ext-search --type=<t> --keyword=<kw> [--free] [--page=N]` | Browse the catalog. |
   | Install from zip | `gp247:ext-install --type=<t> --file=<path.zip>` | Offline. Refused if the key is already on disk. |
   | Install from folder | `gp247:ext-install --type=<t> --dir=<parent>` | `<parent>` contains `<Key>/gp247.json`. Refused if the key is already on disk. |
   | Install by key | `gp247:ext-install --type=<t> --key=<K>` | On disk → installed in place (its `public/` is copied first); else fetched from the library. |
   | Install paid by key | `gp247:ext-install --type=<t> --key=<K> --paid --license=<L>` | **One key at a time**. |
   | Enable | `gp247:ext-enable --type=<t> --key=<K>` | Refused if not installed. |
   | Disable | `gp247:ext-disable --type=<t> --key=<K>` | Refused if not installed, or a template still in use. |
   | Update from library | `gp247:ext-update --type=<t> --key=<K>` / `--all` | **Replaces the folders** (backup kept). Never on a working copy. From gp247/core 3.14.3, when the extension's code was already loaded in that process (another plugin uses it), the data hook runs in a child process (`--local`); if none can start, the item fails with `data_update_pending` and names the `--local` command to run — run it. |
   | Apply data update (files changed by `git pull` / composer / copy) | `gp247:ext-update --type=<t> --key=<K> --local` / `--all` (`--dry-run` to preview) | If `capabilities.ext_update_local`. Downloads nothing; runs the extension's `AppConfig::update()` when its `gp247.json` version is newer than the version core recorded. From gp247/core 3.14.3 it first copies the extension's `public/` to `public/GP247/...` (copy fails ⇒ the hook does not run, item failed) and finishes a library update left pending. Admin equivalent: "Apply data update" on the extension list. |
   | Uninstall | `gp247:ext-uninstall --type=<t> --key=<K>` | Runs the extension's `uninstall()`, removes its config **and deletes its folders**. `--only-data` keeps the folders. |
   | Purge on-disk-only | `gp247:ext-uninstall --type=<t> --key=<K> --purge` | For a not-installed-but-on-disk item; deletes the folders. |
   | License | `gp247:ext-license --type=<t> --key=<K> [--license=<L>] [--delete]` | Set / show / remove a paid license. |
   | Re-publish static files | `gp247:ext-publish --type=<t> --key=<K>` / `--all` | If the command exists. Copies an installed extension's `public/` to `public/GP247/...` again. The repair for `gp247:doctor` → `extension_assets` (missing files; from gp247/core 3.14.3 also outdated files). On core older than 3.14.3, run it after `ext-update --local` when the files were replaced by hand — that core's `--local` does not copy `public/`. |

   `gp247:update` (platform update) also runs `ext-update --local --all` for plugins and then templates;
   a failed data hook there is only a **warning** (exit 0) listed in `data.extension_data` — check it.

4. **Several items.** `ext-install`, `ext-enable`, `ext-disable`, `ext-uninstall` and `ext-publish`
   accept **multiple keys** — repeat the flag (`--key=A --key=B`) or comma-separate (`--key=A,B`);
   `ext-install` likewise takes multiple `--file`/`--dir`. `ext-update --key` and `ext-license --key` take
   **one** key (use `--all` for every update). Items run **one at a time and independently**, results are
   reported per item (`data.succeeded` / `data.failed`), and the route/config cache is rebuilt **once at
   the end**. A paid remote install must be **one `--key` at a time** — `--paid` with more than one key is
   refused up front (`paid_multi_not_allowed`).

5. **Verify.** Re-run `gp247:ext-list --type=<t> --json` to confirm the installed/active/version state
   matches what the user asked for. Single operations rebuild the cache themselves; run
   `php artisan gp247:cache-rebuild` only if the admin still shows stale routes/menus.

6. **Report** per the Output format. State exactly what ran, what changed, and — for any refusal — the
   `error.code`, the per-item message from `data.failed`, and the concrete next step.

**Lifecycle invariants** (why the refusals happen — details in `references/command-matrix.md`):
- **"Installed" means a DB `admin_config` row exists**, not that files are on disk. `ext-install --key` on
  an installed extension is refused before anything is downloaded; `ext-enable` / `ext-disable` /
  `ext-uninstall` treat a not-installed extension as an error.
- **Install vs update vs reinstall:** to refresh an installed extension use `ext-update` (library) or
  `git pull` + `ext-update --local` (working copy); to reinstall, `ext-uninstall --only-data` then
  `ext-install --key`.
- **Guards apply from CLI exactly as in admin:** a template that is in use or is the default cannot be
  disabled or removed; an extension listed in `GP247_PROTECTED_PLUGINS` / `GP247_PROTECTED_TEMPLATES`
  cannot be uninstalled (disabling it is still allowed).
- **`--only-data` and `--purge` are mutually exclusive** on `ext-uninstall` (`conflicting_options`).

## Output format

Do not print a document. Run the operations, then give a short English status report in this shape
(one line per item; mark `[x]` done, `[!]` refused/failed, and give the reason + next step on failure):

```
Extension lifecycle — <operation> (<type>) on gp247/core <probe.core>:
- [x] <Key>: <what happened> (version <v>, active=<yes/no>)
- [!] <Key>: refused — <error.code>: <message from data.failed> → <next step>
State now (gp247:ext-list): <installed/active/version per affected key>
Cache: <rebuilt by the command | ran gp247:cache-rebuild | not needed>
```

## Examples

The user may phrase the request in Vietnamese, Japanese, or English; you always respond in English.

**Example 1 — install a bundled plugin by key**
Input: "Cài plugin News." → Probe: `gp247:ext-install` available. `gp247:ext-list --type=plugin --json`
shows `News` on disk but not installed, so run `php artisan gp247:ext-install --type=plugin --key=News`.
Because its files are on disk, this is a **local** install (same as the admin "Install" button): no
library call and no API License needed. The install enables the plugin, so no `ext-enable` is needed.

**Example 2 — update everything, then remove one plugin**
Input: "Nâng cấp tất cả plugin rồi gỡ hẳn plugin OldBanner." → Check none of the plugin folders is a
working copy (`.git/`). Run `php artisan gp247:ext-check-update --type=plugin --force`, then
`php artisan gp247:ext-update --type=plugin --all` — it exits 0 even when some items failed, so read
`data.failed`. For the removal, confirm the destructive intent, then
`php artisan gp247:ext-uninstall --type=plugin --key=OldBanner` (removes config **and** folders). If
`OldBanner` is on disk but not installed, plain uninstall is refused — use `--purge`.

**Example 3 — a developer pulled new plugin code** (a plugin update: `gp247-plugin-update` handles it in
depth; the core of it is below)
Input: "Tôi vừa git pull plugin News, cập nhật giúp." → The folder is a working copy, so **not** the
library update. Probe: `ext_update_local` true. Run
`php artisan gp247:ext-update --type=plugin --key=News --local --dry-run`, show what would apply, then run
it without `--dry-run`. A failure exits non-zero and keeps the update pending; nothing is rolled back.

**Example 4 — fresh site, free + paid edition from the library**
Input: "Cài MultiVendor và MultiVendorPro từ thư viện cho site mới." → Neither is on disk, so both are
downloaded. Check `GP247_API_LICENSE`/`APP_URL`; if the license is missing, confirm and run
`php artisan gp247:ext-register-license`. The paid edition requires the free one and needs its own
license, so run **two commands**, free first:
`php artisan gp247:ext-install --type=plugin --key=MultiVendor`, then (after confirming the paid install)
`php artisan gp247:ext-install --type=plugin --key=MultiVendorPro --paid --license=<L>`. Report both items
without echoing `<L>`.

## Common mistakes

| Mistake | Why it hurts / how to avoid |
| --- | --- |
| Running a command or option the site's core does not have | It fails with "command not defined" / "option does not exist". Check the probe's `commands` and `php artisan help <command>` first. |
| `ext-update` (library) or plain `ext-uninstall` on a folder under development | Both delete `app/…/<Key>` and `public/…/<Key>` — the `.git` and uncommitted work go with them. Use `git pull` + `ext-update --local`, and `ext-uninstall --only-data`. |
| Treating "files on disk" as "installed" | "Installed" = an `admin_config` row exists. A bundled on-disk plugin still needs `ext-install`. |
| `ext-install --file/--dir` for a key that is already on disk | Refused. Use `ext-install --key=<K>` to install the folder in place, or remove the folder first. |
| `ext-install` on an already-installed key | Refused. To refresh use `ext-update`; to reinstall, `ext-uninstall --only-data` first. |
| Reading exit 0 of `ext-update --all` as "all updated" | It is non-zero only when **every** item failed. Read `data.failed`. |
| Ignoring the warnings of `gp247:update` | A failed extension data hook is only a warning there. Check `data.extension_data` and re-run `ext-update --local` for the failed key. |
| Treating `data_update_pending` as done | The files are replaced but the data hook has not run (no child process allowed). Run the `--local` command the message names, or the admin "Apply data update" button. |
| Assuming `--only-data` leaves the extension's tables | It runs the extension's own `uninstall()`, which may drop its tables. Only the folders are kept. |
| Combining `--only-data` and `--purge` | Refused (`conflicting_options`). |
| `--paid` with several `--key` values | Refused (`paid_multi_not_allowed`). Install paid items one key at a time. |
| Forgetting `--type=template` for templates | Defaults to `plugin`; the template key is then not found. |
| Downloading by `--key` before the site has an API License | Fails with a library error plus a hint. Run `gp247:ext-register-license` once, then retry. |
| Registering the API License while `APP_URL` is `http://localhost` | The license binds the wrong domain; every later library call is refused. Set the real domain first. |
| Expecting `ext-install` to install composer packages or required extensions | It only checks them. `composer require` / install the dependency first. |
| Echoing / committing a paid `--license` | It is a secret. Never print it back or write it into a doc/commit. |
| Using this skill to run `gp247:update` for a platform update | That updates core/front/shop/mcp. Different doc (`install-upgrade/update`). |

## Bundled resources

- `scripts/gp247-probe.php` — step 0. Read-only; prints one JSON object (core version, `gp247:*`
  commands, capabilities). Identical copies ship with every gp247-* skill.
- `references/command-matrix.md` — read at step 3: per-command options and exit codes, the install-source
  decision, the uninstall matrix, the update backup, batch semantics, and the `error.code` values.

---

## Skill info

| Field | Value |
| --- | --- |
| Lần cuối cập nhật / Last updated | `2026-11-19` |
| Skill repo | https://github.com/gp247net/gp247-skills |
| GP247 core repo | https://github.com/gp247net/core |
| source | https://github.com/gp247net/gp247-docs/blob/main/cli/cli-extensions.md |
