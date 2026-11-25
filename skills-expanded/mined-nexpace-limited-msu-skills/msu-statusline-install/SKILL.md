---
name: msu-statusline-install
description: "Claude Code only — a status line is a Claude Code concept and this skill does nothing on another CLI. Puts the newest MSU Builder notice in the Claude Code status line, and repairs it. Use when the user asks to install, enable, set up, re-install or repair the MSU status line, wants MSU notices or announcements shown under the prompt or in the terminal, or reports that the MSU status line is blank, stale, or gone after an update. Wraps a status line that is already configured rather than replacing it. Taking it back out is `msu-statusline-uninstall`."
---

# msu-statusline-install

Wires the MSU status line into the user's own settings. Claude Code
reads `statusLine` from `settings.json` rather than from plugin config, so a plugin
cannot install one — this skill writes it on the user's behalf.

What lands where, all under `CONFIG` = `${CLAUDE_CONFIG_DIR:-$HOME/.claude}`:

| Path | What it is |
|---|---|
| `$CONFIG/msu-statusline.sh` | copy of `${CLAUDE_PLUGIN_ROOT}/scripts/launcher.sh`; what `settings.json` points at |
| `$CONFIG/msu-statusline.prev` | the status-line command that was configured before, verbatim |
| `$CONFIG/msu-statusline.conf` | the settings `msu-statusline-config` edits |
| `$CONFIG/msu-statusline.cache` | the last notice read, plus `.lock`, `.attempted` and `.failures` beside it |

`settings.json` points at the copy rather than into the plugin because the plugin
cache is versioned — a path into it would break on the next `claude plugin update`.
The launcher resolves the most recently installed copy itself, on every render, so an
update to the body of the status line is picked up with nothing to re-run. The launcher
*copy* is the exception: it is a file, not a resolution, and `claude plugin update` does
not touch it. Re-running this install is what refreshes it, and step 3 does that
unconditionally.

## Install

Everything below writes to `$CONFIG`, so assign it once in whatever shell you use:

```bash
CONFIG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
S=$CONFIG/settings.json
```

Two things hold for every write to `settings.json` in either direction. **Keep its file
mode** — the obvious atomic idiom, `mktemp` then `mv`, silently replaces a 0644 file
with a 0600 one, and this is the file holding the user's permissions and hooks. Clone
the mode by making the temporary file a copy of the original, which `cp -p` does and
`mktemp` cannot:

```bash
S=$CONFIG/settings.json
cp -p "$S" "$S.new" && jq '<the edit>' "$S" > "$S.new" && mv -f "$S.new" "$S" \
  || { rm -f "$S.new"; exit 1; }
```

`cp -p` first, then the redirect: `>` truncates the copy and leaves its mode alone, and
`mv` over the original is atomic, so a `jq` that fails writes nothing. On a machine with
no settings file the `cp` fails and there is no mode to keep — write the file directly
there. A failed edit stops the install; cleanup must not turn its exit status into
success. Check that `bash`, `jq` and `curl` are available before making changes.

And **leave a `statusLine` sibling you did not put there alone**, `padding` being the one
that exists today.

1. **Read `$CONFIG/settings.json`.** Create `$CONFIG` if it is not there, and treat a
   missing or empty file as `{}` — a first install has neither, and the JSON below is
   then the whole file rather than a patch. Initialise a missing or empty file to `{}`
   before running the `jq` edits; `jq` on empty input produces no document and exits
   successfully. Stop on malformed JSON, a non-object root or `statusLine`, or a
   non-string command, without replacing the file.
   Edit the file as JSON, never as text: it holds the user's permissions and hooks, and a bad
   patch costs them more than this feature. Parsing and re-serialising reflows the
   file — every value survives, the formatting may not, and that is fine.
2. **Preserve an existing status line.** If `.statusLine.command` is set and does
   **not** already mention `msu-statusline`, write it to `$CONFIG/msu-statusline.prev`
   — the decoded value of that JSON string, the shell command itself, because the
   launcher runs it with `bash -c`. Add no trailing newline: removal puts this file
   straight back into a JSON string, and a stray `\n` there is a command that no longer
   matches what the user had. If there is no existing command, remove any stale `.prev`
   from an earlier install: replaying it would resurrect a line the user has removed.

   ```bash
   jq -e 'type == "object"
     and (.statusLine == null or (.statusLine | type == "object"))
     and (.statusLine.command == null or (.statusLine.command | type == "string"))' \
     "$S" >/dev/null || exit 1
   if jq -e '.statusLine.command // "" | contains("msu-statusline")' "$S" >/dev/null; then
     : # Repair: keep the existing backup.
   elif jq -e '.statusLine.command // "" | length > 0' "$S" >/dev/null; then
     jq -j '.statusLine.command' "$S" > "$CONFIG/msu-statusline.prev" || exit 1
   else
     rm -f "$CONFIG/msu-statusline.prev" || exit 1
   fi
   ```

   `-j`, not `-r`. Both decode the string; `-r` adds the newline this step exists to
   avoid, and it is the spelling that comes to hand first.

   If `.prev` already exists and the current command is *not* ours, the user changed
   their status line since the last install: overwrite it, because the newer one is
   what they expect back.

   **If the current command does mention `msu-statusline`, this is a repair or a
   reinstall: leave `.prev` exactly as it is.** Writing the launcher's own command into
   `.prev` makes the launcher run itself, find `.prev` non-empty, and run itself again —
   unbounded recursion, two processes per level, on every status-line redraw.

   Match on `msu-statusline`, exactly as `msu-statusline-uninstall` does, and not on
   `msu-statusline.sh`: a command pointing straight into the plugin at
   `…/msu-statusline/<version>/scripts/launcher.sh` is this plugin's too, and the
   stricter spelling does not see it. The launcher refuses to replay a `.prev` naming
   itself, so a mismatch here costs the user's own status line rather than the machine —
   but it costs it silently, which is why the two skills have to match on the same thing.
3. **Copy the launcher**: `${CLAUDE_PLUGIN_ROOT}/scripts/launcher.sh` →
   `$CONFIG/msu-statusline.sh`, then make it executable.
4. **Point `settings.json` at it.** Set `.statusLine.type` and `.statusLine.command`
   and nothing else — assigning a whole new `statusLine` object would silently drop a
   sibling the user had set, such as `padding`. The two fields, not the block below as a
   template; on a machine with no settings file the block is a fragment, not a document.

   Store the command **literally**, `${CLAUDE_CONFIG_DIR:-...}` and all. It is written
   that way so it resolves when the status line runs; let a shell expand it while you
   build the string and you bake in today's absolute path instead.

   ```json
   "statusLine": {
     "type": "command",
     "command": "bash \"${CLAUDE_CONFIG_DIR:-$HOME/.claude}/msu-statusline.sh\""
   }
   ```

   No `refreshInterval`. Claude Code redraws the line on every session event *and* on
   that timer, so the timer earns nothing at the default ten-minute colour cycle — the
   events are already far more frequent. It is only worth adding for an `ICON_CYCLE`
   short enough that an idle session would visibly freeze the colour, under a minute or
   so, and then it costs a full re-run of this command on every tick, including any
   status line being wrapped.

5. **Create `$CONFIG/msu-statusline.conf` if it is absent** — never overwrite one that
   exists, it is the user's configuration. Ask the script for its contents rather than
   transcribing them from anywhere:

   ```bash
   if [ ! -e "$CONFIG/msu-statusline.conf" ]; then
     bash "$CONFIG/msu-statusline.sh" --config > "$CONFIG/msu-statusline.conf.new" \
       && mv "$CONFIG/msu-statusline.conf.new" "$CONFIG/msu-statusline.conf" \
       || { rm -f "$CONFIG/msu-statusline.conf.new"; exit 1; }
   fi
   ```

   The guard is in the block, not only in the sentence above it. Every other step here
   ships a block meant to be run as written, so one that skipped the check would take
   the user's settings on the next reinstall — the exact thing the sentence forbids.

   Redirecting straight onto the real name would leave an empty conf behind if the
   command failed — and step 5's own "never overwrite one that exists" would then
   protect that empty file from every future install. `--config` fails with a non-zero
   status and nothing on stdout when the plugin cannot be resolved, which is exactly the
   case this guards: no conf is written. Report the error and repair plugin resolution
   before continuing to step 6; the launcher prints its diagnostic on stderr.

   With no conf to read, that prints exactly the defaults in `KEY=value` form, which is
   the format the file takes. Do not assemble the list by reading the script: the keys
   are named once inside it and every other list — including any in this file — would be
   a second source that goes stale.
6. **Show the real line**, which also proves the whole chain works. Feed it a session
   JSON object rather than `/dev/null`: a wrapped status line usually reads one, and on
   empty input it prints nothing and makes this step look like a failure.

   ```bash
   jq -n --arg dir "$PWD" '{model:{display_name:"Opus"},workspace:{current_dir:$dir}}' \
     | bash "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/msu-statusline.sh"
   ```

   Expect the MSU line when `NOTICE=on` and a notice is cached, and above it the previous
   status line if step 2 saved one. A fetch without a cache waits up to three seconds;
   after a failure, the next eligible retry also waits until there is a cache. With a
   cache, later polls run in the background. `jq --arg` keeps the sample JSON valid
   even when the working directory contains quotes or backslashes.

   **`⚠ MSU statusline: plugin not found` means the launcher cannot see the plugin.** It
   resolves the newest `$CONFIG/plugins/cache/*/msu-statusline/*/`, which matches nothing
   when the plugin is a checkout rather than an installed copy. Point
   `MSU_STATUSLINE_ROOT` at the plugin directory in the environment that actually runs
   the status line, or install the plugin properly. A shell-only override proves only
   that shell's render; it does not configure future Claude Code sessions.

   **An empty render alone does not prove a wiring failure.** `NOTICE=off`, or a cold
   cache after a failed fetch, legitimately prints no MSU line. Check `--config`, the
   cache and `.cache.failures` before claiming success or a broken launcher. Consult
   the troubleshooting reference below if the expected line is missing.

Then report what actually rendered. Settings reload automatically and appear at the
next interaction with Claude Code; a new session is a fallback if the current one does
not update, not a requirement. If step 2 saved a command, its output renders above MSU.
This reload behaviour is documented in the
[Claude Code status-line guide](https://code.claude.com/docs/en/statusline).

## Removing it

Taking the line back out — restoring the status line that was there before, deleting
what the steps above wrote, and uninstalling the plugin — is
`msu-statusline-uninstall`. The order it insists on is real: uninstalling the plugin
first takes that skill away with it.

## When something looks wrong

A symptom and what it means — a blank line, a stale notice, a red warning, a link that
will not open — is in
[`references/troubleshooting.md`](references/troubleshooting.md). Read it when the
request is a symptom rather than an install.

Segments and how often the board is polled belong to `msu-statusline-config`.
