---
name: msu-statusline-uninstall
description: "Claude Code only — a status line is a Claude Code concept and this skill does nothing on another CLI. Takes the MSU status line back out, restores whatever status line was there before it, and uninstalls the plugin when that is what was asked for. Use when the user wants to remove, uninstall, delete, disable or get rid of the MSU status line or the msu-statusline plugin, wants their old status line back, or asks what the install left on their machine."
---

# msu-statusline-uninstall

Removal is two layers, and they are not the same request. **Unwiring** takes the line
out of the user's `settings.json` and deletes what the install wrote. **Uninstalling**
removes the plugin from Claude Code. Unwiring alone stops the line.

Uninstalling alone does not. MEASURED: `claude plugin uninstall` empties the registry
and `enabledPlugins`, and leaves the version directory under `$CONFIG/plugins/cache/`
in place with a `.orphaned_at` marker and its scripts still executable — which is
exactly what the launcher globs for, so the line goes on rendering. `claude plugin
disable` leaves it just as intact. Neither one is a way to switch the status line off.

**Unwire first, always.** Uninstalling the plugin takes this skill with it, so the
order that looks equivalent ends with a status line still wired into the user's
settings and nothing left that knows how to remove it. Recovering means reinstalling
the plugin to get this skill back.

If the request does not say which layer it means, ask. "Remove the status line" is
usually the unwire; "uninstall the plugin" is both, in that order.

## What the install left

All under `CONFIG` = `${CLAUDE_CONFIG_DIR:-$HOME/.claude}`:

| Path | What it is | Removal |
|---|---|---|
| `settings.json` → `.statusLine` | what actually runs the line | restored or deleted, step 1–2 |
| `$CONFIG/msu-statusline.sh` | copy of the plugin's launcher | deleted, step 3 |
| `$CONFIG/msu-statusline.prev` | the status line configured before, verbatim — often absent | read by step 2, gone by step 3 if it was ever written |
| `$CONFIG/msu-statusline.conf` | the user's settings | kept unless they say otherwise, step 4 |
| `$CONFIG/msu-statusline.cache` | last notice read, with `.cache.lock`, `.cache.attempted` and `.cache.failures` beside it | deleted, step 3 |

That is the whole of what the install wrote. The plugin's own files sit elsewhere, under
`$CONFIG/plugins/cache/*/msu-statusline/`, put there by Claude Code rather than by the
install — step 6's business, not step 3's.

## Unwire

```bash
CONFIG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
S=$CONFIG/settings.json
```

Edit `settings.json` as JSON, never as text — this path *deletes* a key, which is the
easier one to get wrong, and the file holds the user's permissions and hooks. **Keep
its file mode** while you do: the obvious atomic idiom, `mktemp` then `mv`, silently
replaces a 0644 file with a 0600 one. Clone the mode by making the temporary file a
copy of the original, which `cp -p` does and `mktemp` cannot:

```bash
S=$CONFIG/settings.json
cp -p "$S" "$S.new" && jq '<the edit>' "$S" > "$S.new" && mv -f "$S.new" "$S" \
  || { rm -f "$S.new"; exit 1; }
```

`cp -p` first, then the redirect: `>` truncates the copy and leaves its mode alone, and
`mv` over the original is atomic, so a `jq` that fails writes nothing. A failed edit
stops removal before any launcher, backup or cache is deleted.

Parsing and re-serialising reflows the file — every value survives, the formatting may
not. Expect a whole-file diff on a file the user may well be watching, and say so rather
than letting them find it.

1. **Check the status line is still ours.** Match `.statusLine.command` against
   `msu-statusline`, not `msu-statusline.sh`: a command pointing straight into the
   plugin at `…/scripts/launcher.sh` is still this plugin's, and a stricter match would
   declare it the user's own and leave it running with no way to remove it.
   `msu-statusline-install` matches on the same spelling when it decides what to
   preserve, and the two have to agree.

   A missing or empty settings file has no command to remove: skip to step 3 without
   creating one. Stop on malformed JSON or a non-object root and keep the launcher and
   backup intact until the settings can be read safely.

   If it does **not** match, the user has changed their status line since installing.
   Leave `settings.json` alone and say why, then skip to step 3 — restoring would
   overwrite their newer choice.
2. **Put back what was there.** Which of the two branches below runs is the only real
   decision on this path. Make it with the file rather than by eye — an emptied `.prev`
   looks identical to a present one in a listing:

   ```bash
   PREV=$CONFIG/msu-statusline.prev
   if [ -e "$PREV" ] && [ ! -r "$PREV" ]; then
     echo 'Cannot read the saved status line; keep the backup and stop.' >&2
     exit 1
   fi
   previous=
   if [ -f "$PREV" ]; then
     previous=$(cat "$PREV") || exit 1
   fi
   case $previous in
     *msu-statusline*) echo 'Saved command points back to MSU; it cannot be restored.' >&2
                      echo delete ;;
     *[![:space:]]*) echo restore ;;
     *) echo delete ;;
   esac
   ```

   **Restore.** Set `.statusLine.command` to what the file holds, and set
   `.statusLine.type` to `"command"` rather than assuming it is already there — it is
   the only type a command status line has, and the user's original may have gone
   without it. Those two fields and no others: assigning a whole new `statusLine` object
   would eat a `padding` the user set, on this branch exactly as on the one below.
   Restore the file's bytes with `jq --rawfile c "$PREV"` and use `$c` for the command.
   Command substitution strips trailing newlines, including ones the user's original
   command deliberately contained. An older backup may include an extra newline; that
   is valid shell syntax and does not need guessing away.

   Keep `padding` and other siblings. Remove or restore `refreshInterval` only when the
   conversation records what `msu-statusline-config` changed, or the user has requested
   that change. **`.prev` holds only the command**, so an existing timer's ownership
   cannot be inferred from the backup. Keep an unknown timer and report that it remains;
   do not silently delete a schedule the user's own command may need.

   **Delete.** No file, whitespace only, or a saved command that still names
   `msu-statusline`: there is no usable previous command to put back. Restoring an MSU
   command would point at the launcher step 3 deletes; never run that backup as a test.
   Delete `.statusLine.type`, `.statusLine.command` and `.statusLine.refreshInterval` —
   a timer with no command left to re-run does nothing. Then delete `statusLine` itself
   only if nothing else is left inside it: a `padding` the user set is theirs, and
   deleting the object whole takes it with no word said.

   **Report what the backup proves.** A missing or emptied `.prev` only means no command
   is available now; it does not prove the user ever had one or that install lost it.
   If the backup was unusable, say why and offer to restore a command they can supply.

3. **Delete `$CONFIG/msu-statusline.sh` and `$CONFIG/msu-statusline.prev`.** Every file
   deletion is here rather than split across step 2, so the skip in step 1 reaches them
   too. `.prev` goes whichever branch ran, and whether it held a command or was emptied:
   an emptied one is a state the troubleshooting tells users to create, and it would
   outlive the thing that reads it. Delete the launcher copy whether or not it was the
   one being run — a command pointing into the plugin means the launcher here was
   already an orphan. A refresh may still be running: its lock is a **directory**, so
   `rm -f` cannot remove it, and deleting it before the writer finishes lets that writer
   recreate the cache after cleanup. After unwiring and deleting the launcher, allow
   up to ten seconds for the refresh's eight-second network budget, then remove an
   empty stale lock with `rmdir`. Stop and inspect a non-empty lock rather than recursively
   deleting it. Remove only the known cache files, including an interrupted `.cache.new`:

   ```bash
   rm -f "$CONFIG/msu-statusline.sh" "$CONFIG/msu-statusline.prev" || exit 1
   for attempt in 1 2 3 4 5 6 7 8 9 10; do
     [ -d "$CONFIG/msu-statusline.cache.lock" ] || break
     sleep 1
   done
   if [ -d "$CONFIG/msu-statusline.cache.lock" ]; then
     rmdir "$CONFIG/msu-statusline.cache.lock" || exit 1
   fi
   rm -f "$CONFIG/msu-statusline.cache" "$CONFIG/msu-statusline.cache.new" \
     "$CONFIG/msu-statusline.cache.attempted" "$CONFIG/msu-statusline.cache.failures" \
     || exit 1
   ```
4. **The conf file is the user's, so ask before deleting it.** Keep
   `$CONFIG/msu-statusline.conf` when only the status line is coming out — a reinstall
   picks their settings back up — and say it is still there. Offer to delete it when the
   plugin is going too; nothing else reads it.

   A request that already asks for all of it — "remove everything" — is
   that answer given in advance. Delete the conf and say you did, rather than offering
   the user a choice they have already made.
5. **Show that it worked**, and that the restored command actually runs. `bash -c`, not
   `sh -c`: the launcher ran it with bash, and on Debian and Ubuntu `/bin/sh` is dash,
   which would fail a command that was working perfectly a minute ago. Feed it a session
   JSON object rather than `/dev/null` — a status line that reads one prints nothing
   without it, and the step looks like a failure.

   ```bash
   CONFIG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
   jq -n --arg dir "$PWD" '{model:{display_name:"Opus"},workspace:{current_dir:$dir}}' \
     | bash -c "$(jq -r '.statusLine.command // empty' "$CONFIG/settings.json")"
   ```

   Expect the user's own status line and nothing else. For a command that needs more
   fields, use captured session JSON. Run this preview only after confirming the command
   is non-empty and no longer names MSU; it also applies to a newer command kept in step 1.

   **On the delete branch that command proves nothing** — `// empty` reduces it to
   `bash -c ""`, which cannot fail and would print nothing against a file you never
   touched. Ask for the command instead of for the object: a `padding` the user set
   keeps `statusLine` in the file quite legitimately, so its presence answers nothing.

   ```bash
   jq '.statusLine.command' "$CONFIG/settings.json"    # expect null
   ```

   If the settings file was missing or empty, report that directly instead of running
   `jq` against it and treating empty output as a parsed `null`.

   **Then say what changed and when.** Settings reload automatically at the next
   interaction with Claude Code; start a new session only if it has not updated.
   See the [Claude Code status-line guide](https://code.claude.com/docs/en/statusline).
   Their own status line is the whole of it again if the restore branch
   ran, or there is none at all if the delete branch did. `msu-statusline.conf` is still
   there only if step 4 kept it. State whether the plugin is still installed based on
   its actual state; unwiring does not install or enable a previously removed plugin.

**Leave `enabledPlugins` alone here.** Unwiring preserves the plugin's current install
and enablement state; step 6 lets the CLI remove the targeted entry itself.

## Uninstall the plugin

Only when that is what was asked for, and only after the unwire above.

6. **Uninstall it.** Read `claude plugin list --json` first for the actual plugin ID
   and installation scope. For the ordinary user-scope install from `msu-skills`, run

   ```bash
   claude plugin uninstall msu-statusline@msu-skills --scope user -y
   ```

   Use the reported marketplace suffix for a fork, and `--scope project` or
   `--scope local` from the corresponding project directory when that is where it was
   installed. Multiple scopes are separate installs: remove only the requested ones.
   If it is already absent, there is nothing to uninstall. `-y` permits the CLI's
   non-interactive path. Re-read the list to confirm that the targeted ID and scope are
   gone; its enabled entry is removed from that scope's settings, not necessarily the
   user settings file.

   That uninstall rewrites `settings.json` itself, in its own key order — a second
   reflow on top of step 2's. Expect it, and do not read it as an edit of yours that
   went wrong.

   **Leave the `msu-skills` marketplace alone.** The other plugins install from it, and
   removing it is a separate request with a much wider blast radius. Same for
   `enabledPlugins` entries that are not this plugin's.

   The version directory under `$CONFIG/plugins/cache/*/msu-statusline/` survives the
   uninstall, marked `.orphaned_at`. `claude plugin prune` does not take it — that
   removes auto-installed dependencies, and this is not one. Once step 1–3 have run,
   nothing points at it and it is inert; delete it by hand if the user wants the disk
   back, and say that a reinstall would fetch it again either way.
7. **Add to what step 5 already told them.** The plugin's skills go with it, this one
   included, and a reinstall is what brings them back. Whether the conf file survived is
   step 4's answer. Nothing else changes: step 5's message about the next interaction and about
   which status line is left standing still holds.

## Worth telling the user

- **Turning every segment off is not removal.** `NOTICE=off` and the rest leave an
  empty line still wired into `settings.json`. That is `msu-statusline-config`; this
  skill is what takes the line out.
- **A second status line that appeared at install is `.prev` working as intended**, not
  a bug to remove the plugin over. Emptying `$CONFIG/msu-statusline.prev` drops the old
  one and keeps the MSU line.
- **`⚠ MSU statusline: plugin not found` after an uninstall** means the plugin went
  first and the unwire never happened. The launcher copy is still in `settings.json`
  with nothing left to resolve. Run steps 1–3 by hand, or reinstall the plugin and use
  this skill.

Installing and repairing belong to `msu-statusline-install`; segments and polling to
`msu-statusline-config`.
