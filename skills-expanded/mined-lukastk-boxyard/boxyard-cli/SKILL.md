---
name: boxyard-cli
description: Use the Boxyard CLI to manage, find, inspect, sync, include, exclude, group, rename, or copy boxes. Use when the user asks about boxyard command usage, Boxyard config files, locating box folders, rclone-backed storage, sync status, or shell/TUI helpers.
---

# Boxyard CLI Skill

Use this skill when the user wants to **use** Boxyard, not develop Boxyard itself.

Boxyard is a Python CLI for managing and syncing folders ("boxes") across local and remote storage using rclone or local storage. A box has data, metadata, optional sync configuration, group membership, and sync records.

## Where generated data should live

Generated data — including large outputs — generally belongs **inside** the box it relates to, not in some sibling directory chosen to dodge syncing. Do not move heavy outputs out of a box to keep it "small". The whole point of Boxyard is that syncing makes large boxes comfortable to live with: anything you don't want pushed can be excluded from sync via the box's `conf/.rclone_exclude` (see "Per-box sync configuration"), or the box itself can be excluded locally with `boxyard exclude`. Keep data colocated with its box and control sync with filters — don't fragment it to avoid sync.

## Before running commands

- If operating from this repository checkout, prefer:

  ```bash
  cd /path/to/boxyard && uv run boxyard ...
  ```

  If Boxyard is already installed in the environment, `boxyard ...` is also fine.

- Read-only commands are safe to run without confirmation: `--help`, `list`, `tree`, `path`, `which`, `box-status`, `yard-status`, `list-groups`, `owner`, `doctor`, `convert --dry-run`.
- Ask before running commands that can modify local or remote state: `init`, `new`, `sync`, `multi-sync`, `sync-missing-meta`, `include`, `exclude`, `delete`, `rename`, `sync-name`, `add-to-group`, `remove-from-group`, `add-parent`, `remove-parent`, `create-user-symlinks`, `copy`, `force-push`, `claim`, `release`, `discard-local`, `convert`.
- Be especially careful with:
  - `boxyard new --from PATH` / `-f PATH`: moves `PATH` into Boxyard unless `--copy` is supplied.
  - `boxyard exclude`: syncs first by default, then removes the local data copy.
  - `boxyard delete`: deletes a box.
  - `boxyard sync --sync-setting replace|force`: can overwrite data depending on direction/status.
  - `boxyard force-push --force`: destructively overwrites remote data from a local source folder.

## Configuration files and important paths

Default files and folders:

```text
~/.config/boxyard/config.toml          # main Boxyard config
~/.config/boxyard/boxyard_rclone.conf  # Boxyard's rclone config
~/.config/boxyard/default.rclone_exclude
~/.boxyard/                            # default boxyard_data_path
~/boxes/                               # default user_boxes_path; included box data appears here
~/box-groups/                          # default user_box_groups_path; group symlinks appear here
```

The config file controls the real locations. Important config keys:

```toml
default_storage_location = "..."
boxyard_data_path = "~/.boxyard"
user_boxes_path = "~/boxes"
user_box_groups_path = "~/box-groups"

[checkout_roots.bulk]
path = "~/large-boxes"

# Optional guarded root (both keys required together)
[checkout_roots.volume]
path = "/mnt/volume/boxes"
mount_target = "/mnt/volume"
filesystem_uuid = "..."
max_concurrent_rclone_ops = 3

[storage_locations.my-remote]
storage_type = "rclone" # or "local"
store_path = "boxyard"
```

Derived paths:

```text
<boxyard_data_path>/boxyard_meta.json          # cached local box index
<boxyard_data_path>/local_store/<storage>/     # local metadata/conf roots by storage location
<boxyard_data_path>/sync_records/              # local sync records
<boxyard_data_path>/sync_backups/              # local sync backups
<boxyard_data_path>/remote_indexes/            # cached remote index lookups
<boxyard_data_path>/placements/<box_id>.json # machine-local checkout placement
```

For a box with index name `<box_id>__<name>`:

```text
<configured-checkout-root>/<box_id>__<name>/                # authoritative local DATA path
<boxyard_data_path>/local_store/<storage>/<index>/           # local box root
<boxyard_data_path>/local_store/<storage>/<index>/boxmeta.toml
<boxyard_data_path>/local_store/<storage>/<index>/conf/
```

Remote/rclone stores use this layout under the storage location's `store_path`:

```text
boxes/<index>/data/          # plain boxes
boxes/<index>/data.restic/   # restic boxes: per-box repository (see "Storage format")
boxes/<index>/data.snapshot  # restic boxes: pointer to the current snapshot
boxes/<index>/boxmeta.toml
boxes/<index>/conf/
sync_records/<index>/<data|meta|conf>.rec
sync_backups/
```

The global CLI option for non-default config is:

```bash
boxyard --config /path/to/config.toml <command> ...
```

`boxyard init` uses `--config-path` and `--data-path` to create a config/data directory. The shell helper honors `BOXYARD_CONFIG_PATH`; normal Typer CLI commands should be given `--config` when using a non-default config.

`DEFAULT_BOX_GROUPS` can add default groups at runtime. It is parsed as a TOML list string, for example:

```bash
export DEFAULT_BOX_GROUPS='["ctx/mac", "work"]'
```

## How to find where boxes are

Use these patterns first.

### Find the box containing the current directory or any path

```bash
boxyard which
boxyard which --path /some/path
boxyard which --path /some/path --json
boxyard which --path /some/path --index-name
```

`which` searches every configured checkout root (including symlink-resolved paths) and reports the box name, id, index name, storage location, checkout root/state, authoritative local DATA path, and inclusion state.

### Get a box's data folder

```bash
boxyard path --box-name NAME --pick-first
boxyard path --box-id BOX_ID
boxyard path --box INDEX_NAME
```

`boxyard path` defaults to the **data** path. By default it filters to included boxes. Use `--all` when you need to select from included and excluded boxes.

### Get non-data paths for a box

```bash
boxyard path --box-name NAME --pick-first --path-option root
boxyard path --box-name NAME --pick-first --path-option meta
boxyard path --box-name NAME --pick-first --path-option conf
boxyard path --box-name NAME --pick-first --path-option sync-record-data
boxyard path --box-name NAME --pick-first --path-option sync-record-meta
boxyard path --box-name NAME --pick-first --path-option sync-record-conf
```

### Find checkout roots and actual local paths

Never reconstruct `user_boxes_path/<index_name>`: a box may be in any configured root. `user_boxes_path` is permanently the root named `default`; additional roots are `[checkout_roots.NAME]`. Use:

```bash
boxyard checkout-roots
boxyard list --show-status --show-checkout
boxyard list --checkout-root volume --output-format json
boxyard path --box INDEX_NAME
boxyard which --path /some/root/INDEX --json
```

Status markers are `●` included, `○` excluded, `!` root unavailable, `×` recorded checkout missing, and `↔` interrupted relocation. An unavailable root never falls back to default and its boxes remain in the catalog.

## Common discovery commands

```bash
boxyard list
boxyard list --show-status
boxyard list --output-format json
boxyard list --view groups --show-status
boxyard list --view tree --show-status
boxyard tree --show-status
boxyard list-groups --all --include-virtual
boxyard yard-status
```

Group filters support boolean expressions over group names:

```bash
boxyard list --group-filter 'work AND NOT archived'
boxyard path --group-filter 'ctx/mac OR ctx/linux' --pick-first
```

Other list filters:

```bash
boxyard list --include-group GROUP
boxyard list --exclude-group GROUP
boxyard list --children-of BOX
boxyard list --descendants-of BOX
boxyard list --parent-of BOX
boxyard list --ancestors-of BOX
boxyard list --roots
boxyard list --leaves
```

## Box selection options

Many commands accept one of:

```bash
--box INDEX_NAME       # full <box_id>__<name>
--box-id BOX_ID        # <timestamp>_<subid>
--box-name NAME        # defaults to contains matching for many commands
```

Name matching options:

```bash
--name-match-mode exact|contains|subsequence
--name-match-case
--pick-first           # available on `path`; use only when ambiguity is acceptable
```

With no `--box`/`--box-id`/`--box-name` at all, boxyard uses the box you are
standing in — anywhere under `<user_boxes_path>/<index_name>/...`. If the cwd is
not inside a box (or the box is not a candidate for that command, e.g. an
already-included box for `include`), it falls back to an fzf picker over the
candidates. Commands that destroy something — `delete`, `rename`, `copy`,
`force-push`, `sync-name` — refuse a bare invocation outright and always need
an explicit selector.

## Creating boxes

Create an empty box:

```bash
boxyard new --box-name NAME
```

Create from an existing folder, moving the folder into Boxyard:

```bash
boxyard new --from /path/to/folder
```

Copy from an existing folder instead of moving it:

```bash
boxyard new --from /path/to/folder --copy
```

Clone a git repo as a new box:

```bash
boxyard new --git-clone git@github.com:user/repo.git
```

Useful options:

```bash
boxyard new --box-name NAME --storage-location STORAGE
boxyard new --box-name NAME --group GROUP --group OTHER_GROUP
boxyard new --box-name NAME --parent PARENT_BOX
boxyard new --box-name NAME --no-initialise-git
boxyard new --box-name NAME --no-claim   # don't make THIS machine the write owner
```

`new` claims the box for the creating machine by default (see "Write ownership"). Pass `--no-claim` when creating a box here that will be worked on elsewhere, or the other machine's pushes will be refused.

A new box's storage format (`plain` or `restic`) is fixed at creation from the resolved sync policy — see "Storage format (plain vs restic) and `convert`".

Select local placement independently of remote storage:

```bash
boxyard new --box-name NAME --storage-location STORAGE --checkout-root ROOT
boxyard include --box-name NAME --checkout-root ROOT
boxyard relocate --box-name NAME --checkout-root OTHER_ROOT
boxyard relocate --box-name NAME --checkout-root ROOT --adopt-existing
boxyard relocate --box-name NAME  # recover the recorded destination after interruption
```

`exclude` remembers the preferred root; `include` without a root reuses it. `relocate` is locked, local-only, does no remote I/O, and is recoverable via `doctor`. Use `--adopt-existing` only for a pre-populated destination: Boxyard verifies every source entry is identical there, preserves destination-only content, then commits placement and removes the source.

## Syncing

Sync one box:

```bash
boxyard sync --box-name NAME
boxyard sync --box INDEX_NAME
boxyard sync --box-id BOX_ID
```

Sync only selected parts:

```bash
boxyard sync --box-name NAME --sync-choices meta
boxyard sync --box-name NAME --sync-choices conf
boxyard sync --box-name NAME --sync-choices data
```

Sync settings and direction:

```bash
boxyard sync --box-name NAME --sync-setting careful
boxyard sync --box-name NAME --sync-setting replace
boxyard sync --box-name NAME --sync-setting force
boxyard sync --box-name NAME --sync-direction push
boxyard sync --box-name NAME --sync-direction pull
```

Other sync commands:

```bash
boxyard multi-sync
boxyard multi-sync --storage-location STORAGE --max-concurrent 3
boxyard multi-sync --box INDEX_NAME --box OTHER_INDEX_NAME
boxyard multi-sync --due-only              # only boxes whose DATA cadence is due, most overdue first
boxyard multi-sync --skip-unchanged-meta   # one bulk remote listing; skip boxes whose boxmeta moved on neither side
boxyard multi-sync --skip-unchanged        # same, for META and (restic boxes only) DATA; a plain box's DATA is never skipped
boxyard sync --box-name NAME --sync-children   # also sync every descendant box afterwards
boxyard sync-missing-meta
boxyard box-status --box-name NAME
boxyard yard-status
```

Soft interruption is enabled by default for long operations: interrupt once or twice to stop after the current operation; repeated interrupts exit immediately.

### Sync policies (cadence)

`[sync_policies.NAME]` tables in `config.toml` set, per box group, how often a box is due and what storage format new boxes get. Every field is optional; an unset field means "not stated here", not "off".

```toml
[sync_policies.default]        # the floor every box falls back to (its `groups` are ignored)
storage_format = "plain"

[sync_policies.cold]
groups = ["archived"]          # applies to boxes in any of these groups
data_interval = "7d"           # whole number + s|m|h|d|w
meta_interval = "1d"
```

Resolution is per setting: the box's own `conf/sync.toml` (may set only `data_interval`, `meta_interval`, `storage_format`) beats matching group policies, which beat `default`. Two matching policies stating different values for one setting is a conflict (`doctor`: `sync-policy-conflict`); an unparseable `conf/sync.toml` is `unusable-box-sync-conf`. With no policies at all every box is always due, so `--due-only` changes nothing. `--due-only` selects on `data_interval`, measured from the last successful check that `multi-sync` records machine-locally under `<boxyard_data_path>/sync_checks/<index>/<part>.json`.

## Storage format (plain vs restic) and `convert`

A box's DATA is stored either as a **plain** rclone tree (`boxes/<index>/data/`) or as a per-box **restic** repository (`boxes/<index>/data.restic/`, plus a `boxes/<index>/data.snapshot` pointer naming the current snapshot). META and CONF are always plain. The format is recorded in the boxmeta as `storage_format` and is a fact about the box: it is stamped once at `new` from the resolved sync policy, and afterwards only `boxyard convert` changes it — a config edit never reformats existing boxes.

When no policy states a format, the **package default is `restic`** for rclone storage locations (`plain` for `local` ones). Lukas's rig pins `[sync_policies.default] storage_format = "plain"`, so his new boxes are plain; a config without that pin creates restic boxes, and `new` refuses to create one when no restic password is configured.

**Plain is right for almost every box.** Follow the global AGENTS.md "Box storage format" guidance: convert only for more than ~5,000 **directories** (directory count, not file count, drives plain sync cost), for >~1 GB of large files that get rewritten or re-snapshotted, or when encryption at rest / snapshot history is wanted.

```bash
boxyard convert -r INDEX_NAME --dry-run                   # read-only: local shape (counts excluded paths too)
boxyard convert -r INDEX_NAME --dry-run --estimate-size   # also measure what restic would store (reads the whole box, writes nothing remote)
boxyard convert -r INDEX_NAME                             # plain -> restic (prompts; -y skips)
boxyard convert -r INDEX_NAME --to-plain                  # restic -> plain
```

`convert` verifies a byte-identical restore (content, mode, symlinks) before the old copy is removed, and is resumable after an interruption. It refuses — before writing anything — for a box in a `local` storage location, a box not checked out on this machine, a box whose sync lock is held, or one with an interrupted DATA sync. **A machine on boxyard older than 0.7.0 cannot read a restic box**, so check `ssh-target <machine> boxyard --version` across the fleet first.

Restic boxes need, on every machine: the `restic` binary (`BOXYARD_RESTIC` points at an explicit one), and the repository password from `$BOXYARD_RESTIC_PASSWORD` or the config's `restic_password_command` (the rig uses `secret get BOXYARD_RESTIC_PASSWORD`). Machine-local state lives in `<boxyard_data_path>/restic_state/` (never synced), and backups go through the fixed symlink root `/tmp/boxyard-restic` so every machine records the same snapshot path. `doctor` reports `storage-format-mismatch` and `orphaned-snapshot`.

## Write ownership (`owner`, `claim`, `release`, `discard-local`)

A box can have a **write owner**: the single machine allowed to push its DATA/CONF. A box with
**no owner is unrestricted**, exactly as before this feature existed. **`boxyard new` claims
the box for the creating machine by default** — pass `--no-claim` when the box will be worked
on elsewhere; `boxyard include --read-only` includes a box without the nudge to claim it.
Ownership is recorded per box as `write_owner`
and compared against this machine's configured `machine_name` (configured, never derived
from the hostname, because hostnames are unreliable — one machine reports both
`lukas-pocket4` and `pocket4`).

```bash
boxyard owner --box-name NAME          # who may push this box (read-only; -o json too)
boxyard claim --box-name NAME          # make THIS machine the write owner
boxyard claim --all-included           # claim every box included here that has no owner
boxyard release --box-name NAME        # give up this machine's ownership
```

**If a sync is refused because another machine owns the box**, there are exactly two ways
out, and the error prints both:

```bash
boxyard claim --steal --box-name NAME  # take ownership from the current owner (prompts; -y to skip)
boxyard discard-local --box-name NAME  # throw away THIS machine's copy, take the remote's
```

`discard-local` is the destructive one, but not lossy: what it overwrites is kept under
the sync backups directory and the path is printed. Prefer `--steal` when this machine's
copy is the one you want to keep, `discard-local` when the remote's is.

**Ownership is also enforced on three commands that bypass sync entirely** and would
otherwise write to the remote unchecked: `force-push`, `rename --scope remote|both`, and
`delete`. Being refused by one of these is the gate working, not a bug — resolve it with
`claim`/`--steal` rather than reaching for a workaround.

## Health check (`doctor`)

`boxyard doctor` is a strictly read-only health check of the machine's whole boxyard state. It never mutates or auto-fixes anything, and exits 0 when healthy / 1 when there is any finding, so scripts and cron jobs can assert on it.

**Agents: run `boxyard doctor` whenever box state looks inconsistent** — e.g. a folder in `user_boxes_path` that `boxyard list` doesn't know about, `boxyard list` missing boxes that exist on another machine, group symlinks pointing nowhere, or errors mentioning boxmeta/sync records. Every finding comes with a one-line hint on how to fix it; apply the hints rather than improvising.

```bash
boxyard doctor                       # full check, including remote storage
boxyard doctor --no-remote           # offline: skip remote checks (stale-meta-mirror, tombstoned-box, diverged-box, write-denied, orphaned-snapshot, orphaned-remote-sync-backups)
boxyard doctor -o json               # machine-readable report
boxyard doctor -s STORAGE            # restrict the remote check to one storage location
```

Checks (33; `--no-remote` skips the six marked *remote*):

- **Registration and cache:** `unregistered-folder` (dirs — or stray files — in any checkout root not registered as boxes; the classic symptom of hand-creating folders instead of using `boxyard new`), `malformed-name` (names that don't parse as `<timestamp>_<subid>__<name>`; legacy formats are accepted), `broken-registration` (missing/invalid `boxmeta.toml` in the local store), `duplicate-box-id`, `stale-cache` (`boxyard_meta.json` disagrees with a fresh scan), `unknown-storage-location` (leftovers from removed/renamed storage locations), `tree-orphans` (parents referencing unknown box ids).
- **Group tree:** `dangling-symlinks` (group symlinks with missing targets), `group-tree-debris` (real files in the group tree, which break `create-user-symlinks` and thereby most mutating commands).
- **Sync state:** `orphaned-sync-records`, `interrupted-sync` (sync records left incomplete — the local copy may be incomplete; re-sync to recover), `diverged-box` (*remote*; both sides moved on independently, or a push never completed — sync refuses until resolved), `stale-meta-mirror` (*remote*; remote boxmetas not mirrored locally — what `sync-missing-meta` would fetch; a machine where that never runs silently hides newer boxes from `boxyard list`), `tombstoned-box` (*remote*; boxes deleted from another machine but still registered here), `orphaned-sync-backups` and `orphaned-remote-sync-backups` (the latter *remote*; backup dirs no sync record claims — may be a `discard-local` keepsake, never assume disposable).
- **Config and version skew:** `rclone-config` (missing rclone binary/remote sections/default exclude file), `unknown-config-keys` (typo, or config written for a newer boxyard), `unknown-boxmeta-keys` (box written by a newer boxyard; upgrade here), `machine-name-unset`.
- **Ownership:** `write-denied` (*remote*; another machine owns a box that has local changes here that can never be pushed), `stale-owner` (owner lacks a complete checkout, or looks renamed/retired), `unowned-box` (included here, unclaimed), `unpushed-meta-edit` (local `groups`/`parents`/`write_owner` edits not yet pushed).
- **Sync policies:** `sync-policy-conflict`, `unusable-box-sync-conf` (see "Sync policies").
- **Checkout roots:** `checkout-root-config` (overlapping/duplicate root paths), `checkout-root-unavailable`, `checkout-placement` (placement record missing/unloadable/contradicting what is on disk), `duplicate-checkout` (copies of one box in several roots), `interrupted-relocation` (recover with `boxyard relocate`).
- **Storage format:** `storage-format-mismatch` (box's actual format differs from what policy asks for; nothing converts automatically), `orphaned-snapshot` (*remote*; restic snapshots the pointer does not reach — usually a push that raced another machine; nothing is lost).

## Include, exclude, copy

Include an excluded remote box locally:

```bash
boxyard include --box-name NAME
boxyard include --interactive
```

Exclude a local copy while keeping the remote:

```bash
boxyard exclude --box-name NAME
boxyard exclude --interactive --show-sizes
boxyard exclude --box-name NAME --skip-sync
```

Copy a remote box to an arbitrary destination without adding it to Boxyard tracking:

```bash
boxyard copy --box-name NAME --dest ./NAME-copy
boxyard copy --box-name NAME --dest ./NAME-copy --meta --conf
boxyard copy --box-name NAME --dest ./NAME-copy --overwrite
```

## Groups and hierarchy

Groups:

```bash
boxyard add-to-group --box-name NAME GROUP [OTHER_GROUP ...]
boxyard remove-from-group --box-name NAME GROUP [OTHER_GROUP ...]
boxyard list-groups --box INDEX_NAME
boxyard list-groups --all --include-virtual
boxyard create-user-symlinks
```

Parent-child hierarchy:

```bash
boxyard add-parent --box-name CHILD --parent-name PARENT
boxyard remove-parent --box-name CHILD --parent-name PARENT
boxyard tree --show-status
boxyard list --view tree --show-status
```

## Rename, delete, and force operations

Rename:

```bash
boxyard rename --box-name OLD --new-name NEW --scope both
boxyard rename --box-name OLD --new-name NEW --scope local
boxyard rename --box-name OLD --new-name NEW --scope remote
```

Sync only the name between local and remote:

```bash
boxyard sync-name --box-name NAME --to-local
boxyard sync-name --box-name NAME --to-remote
```

Delete:

```bash
boxyard delete --box-name NAME
boxyard delete --box-name NAME --force   # needed when the box has children
```

Destructive force push:

```bash
boxyard force-push --box-name NAME --source /path/to/source --force
```

## Per-box sync configuration

Each box can have a `conf/` folder. Boxyard syncs `conf/` before `data/`, so filters travel with the box.

Special files:

```text
conf/.rclone_exclude  # exclude matching files (REPLACES the default list)
conf/sync.toml        # per-box sync policy override (see "Sync policies")
```

`conf/.rclone_include` and `conf/.rclone_filters` are recognised but currently **REFUSED**: an exclude file always applies, and boxyard will not combine rclone filter families (rclone applies them in an indeterminate order). A box that has either file fails its DATA sync until boxyard merges the three into one ordered filter list (ticket 43f05498). Express a box's scope in `conf/.rclone_exclude` alone.

If `conf/.rclone_exclude` is absent, Boxyard uses:

```text
~/.config/boxyard/default.rclone_exclude
```

If `conf/.rclone_exclude` exists it **REPLACES** `~/.config/boxyard/default.rclone_exclude` entirely — it does not extend it. So copy the default file's contents in and append to it; a one-line `.rclone_exclude` would start syncing `.venv/`, `node_modules/` and the like. The package default (written by `init`) is `.venv/`, `.pixi/`, `.trunk/`, `node_modules/`, `__pycache__/`, and `.DS_Store`; Lukas's rig deploys a longer list (36 entries).

## Shell helper

The repo includes a zsh helper:

```bash
source /path/to/boxyard/shell/boxyard.zsh
```

Default keybinding: `Ctrl+G` (`BOXYARD_WIDGET_KEY` can override it). Type a partial box name, press the keybinding, and it replaces the current word with a relative path to the selected box. It uses `boxyard-shell-helper search` and `fzf` for multiple matches.

Direct helper examples:

```bash
boxyard-shell-helper search TERM
boxyard-shell-helper search TERM --group GROUP
boxyard-shell-helper search TERM --included
boxyard-shell-helper search TERM --excluded
```

## Reference files in this repository

From this skill directory, the repository root is `../..`.

Read these for more context when needed:

- `../../README.md` — high-level usage and directory layout
- `../../src/boxyard/const.py` — default paths and constants
- `../../src/boxyard/config.py` — config model and derived paths
- `../../src/boxyard/_cli/main.py` — command definitions
- `../../src/boxyard/_cli/multi_sync.py` — `multi-sync`
- `../../src/boxyard/_models.py` — box path and metadata layout
- `../../src/boxyard/_shell_helper.py` — shell helper behavior
