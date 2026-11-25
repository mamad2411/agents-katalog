---
name: msu-statusline-config
description: "Claude Code only — a status line is a Claude Code concept and this skill does nothing on another CLI. Reads and changes what the MSU status line shows. Use when the user wants to turn a status-line segment on or off, change polling, title width, label, colours, icon, colour cycling or timestamp, or asks what their MSU status line is currently set to. Editing the settings file by hand is the same operation and belongs here too."
---

# msu-statusline-config

One file holds every setting: `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/msu-statusline.conf`,
written as `KEY=value`, one per line. A `#` at the start of a value or after whitespace
starts a comment; an embedded `#` such as `LABEL=C#Build` is literal. Newlines and
comment-opening `#` cannot be represented inside a value by adding shell quotes.

The status line reads that file as data — it parses the keys it knows and ignores
everything else, rather than executing it. So an unknown key is inert, not an error,
and a value never needs shell quoting.

## The keys

**Ask the script, never this file and never memory.**

```bash
bash "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/msu-statusline.sh" --config
```

That prints every key with the value **in force** — after the conf file has been read
and every value checked. No list of keys is written down here on purpose: one would be
a second source, and it would be a version behind the moment a segment is added.

Route the command through the launcher, as above, rather than through the plugin
directly: the launcher's path never changes, while the plugin's carries a version number
and moves on every update, so a command naming it is one `claude plugin update` from
being wrong. That is about commands — the ones you run and the ones you hand the user.

**Reading** is different. When a request names a behaviour rather than a key, what each
one governs is in the comment above it in the `# Defaults` block of
`${CLAUDE_PLUGIN_ROOT}/scripts/statusline.sh`, which is the same single source as
`--config`. `${CLAUDE_PLUGIN_ROOT}` is resolved for you and always current, so open it
there; the launcher has no such block.

The distinction between what is written and what is in force is the whole reason to ask
the script. A value the parser cannot use is replaced silently, and the render looks
perfectly healthy afterwards: `ICON_CYCLE=5m` becomes `0`, which pins the icon to one
colour for ever; `TIME=KST` becomes `local`; `COLOR=orange` becomes `none`;
`MAX_WIDTH=80px` becomes `72`. Reading the conf file would report the user's typo back
to them as if it had taken effect. `--config` reports what actually did.

## Changing something

1. Run `--config` for what is in force, and read the conf file for what was written.
   If the launcher is missing or `--config` fails, stop the edit and follow
   `msu-statusline-install` to repair it. A missing conf alone is normal: the script
   reports its defaults, and the first edit can create the file.
   A key absent from the file is at its default; that is not a problem to fix. Where the
   two disagree, inspect the parser before calling it a rejected value: whitespace,
   comments and `ICON_CYCLE=030` becoming `30` are normalisation; with duplicate keys,
   the last assignment wins. Tell the user about every rejected value,
   whether or not it is what they asked you to change — and change none of them
   they did not ask for. Offer the correction and let them take it; some have no correct
   answer to guess at, a `COLOR` the script does not know being one.
2. Show them what is set now, and apply what they asked for. When the request names no
   number — "a bit shorter", "less often" — pick one, say it was your pick, and give
   them the current value to push back against. Do not go hunting for a value that makes
   the render visibly change; see step 4. A key `--config` does not
   list cannot be set; say so and name the ones that can, rather than writing a line
   that will be ignored.
3. Write the file back, keeping the user's own comments and key order, appending
   anything new. Values are plain: `NOTICE=off`, not `NOTICE="off"`.
   For a repeated key, edit its last assignment, which is the one the parser uses.
   Validate the requested value against the script's guards first, and reject embedded
   newlines or comment syntax that would truncate it instead of writing a different value.

   If the change reaches `settings.json` — only `ICON_CYCLE` does — set the one field
   and leave the rest of `statusLine` alone. Assigning a new object there would drop a
   sibling the user had set, `padding` being the one that exists today, and keep the
   file's mode while you are at it: `mktemp` then `mv` quietly turns 0644 into 0600 on
   the file holding their permissions and hooks. `cp -p` the original onto the temporary
   file first and the mode comes with it; `msu-statusline-install` writes that idiom out.
4. Confirm twice, because the two answer different questions:

   ```bash
   CONFIG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
   bash "$CONFIG/msu-statusline.sh" --config              # did the value take?
   jq -n --arg dir "$PWD" '{model:{display_name:"Opus"},workspace:{current_dir:$dir}}' \
     | bash "$CONFIG/msu-statusline.sh"                  # what does it look like?
   ```

   The sample includes the model and workspace, just as the install preview does:
   a wrapped status line often needs them and prints nothing for `{}`. Use captured
   session JSON if the user's command needs more fields. Never leave stdin on a terminal,
   where a command reading it waits for input that never comes.

   The second renders the whole status line, so its first rows may be a status line that
   was already configured before this one was installed — that is the launcher replaying
   it, not this plugin. With a cold cache it also blocks for up to three seconds on a
   live fetch.

   **A render that looks unchanged is not a failed edit.** `MAX_WIDTH` only shows when a
   title is longer than it, so lowering 72 to 48 changes nothing until a longer notice
   arrives. Say that rather than lowering the number until something moves.
   If `--config` did not accept the requested value, the change is not complete: explain
   the fallback and correct only the requested key. `NOTICE=off` legitimately hides MSU;
   an empty render with it on needs the install skill's troubleshooting.

**`ICON_CYCLE` is the one key that can reach outside the conf file.** The colour is
computed from the clock at each redraw, and Claude Code redraws on every session event,
so at the default ten minutes nothing else is needed. Shorten it below a minute or so
and an idle session will visibly hold one colour; only then is
`statusLine.refreshInterval` in `settings.json` worth adding, set to the same number.

**`refreshInterval` is in seconds**, minimum 1 — the same unit as `ICON_CYCLE`, so the
same number means the same thing. Say the unit when you write it; read as milliseconds
it would re-run the status line thirty times a second, and nothing in `--config` or in
the rendered line would show it.

**Ask before adding it, rather than reporting it afterwards.** Every tick re-runs the
whole status-line command — including a status line the user configured before this
plugin existed and that this plugin only wraps. Spending someone else's command on an
ornament is their call. Set `ICON_CYCLE` either way; it is only the timer that waits.
If they already requested or approved the timer, proceed without asking again.

Read any existing `refreshInterval` before proposing a change. Keep it when its owner
is unknown; the wrapped command may depend on it. When returning to a slow cycle or
`0`, remove a timer this conversation established was added solely for the MSU icon,
or restore the earlier interval if it was recorded. Otherwise report the existing
timer and ask only if changing it is needed. Use the effective `ICON_CYCLE` from
`--config` for an approved timer, never an invalid or zero value from the conf file.

Changes apply to the next render — there is nothing to restart and no cache to clear.
A shorter polling interval takes effect immediately, because the interval is measured
against the cache file's age each time the status line runs.

## Worth telling the user

- **"The icon colour is not cycling" is usually not a cycling problem.** Check these
  two before touching `ICON_CYCLE`, because both freeze the colour while looking fine:
  `--config` reporting `ICON_CYCLE=0` (something non-numeric was written, and `0` means
  hold the first colour), and `ICON_TRUECOLOR=auto` on a terminal that advertises no
  24-bit support in `COLORTERM` or `TERM` — Terminal.app and a default tmux both handle
  it and advertise nothing, the icon falls back to the label's colour, and
  `ICON_TRUECOLOR=on` is the answer. The exact set the script accepts is the `case` it
  reads them in; do not go by a list written anywhere else, this one included. Otherwise the cycle is simply ten minutes long and nothing is wrong.
- **`MAX_WIDTH` counts the title, not the line.** The timestamp, the icon and the label
  sit outside it, so the row is around twenty columns wider than the number. It also
  does nothing at all outside a UTF-8 locale, where slicing would cut a multi-byte
  character in half and the script would rather leave the line long.
- **The warning is not configurable, on purpose.** Once polling has backed off all the
  way to the polling interval the line says so, in red, and says which kind of failure
  it was. A silent failure is the one thing this plugin cannot afford: the line would go
  on showing an old notice, or nothing, and look exactly like a quiet week. There is no
  key to switch that off — turn the segment off with `NOTICE=off` if it is unwanted.
- **The time is the reader's own, and the board's is not.** VERIFIED in the site's own
  code: its notice list is formatted with dayjs `.utc()`. So a reader outside UTC sees
  one time here and another on the page this line links to, for the same post. Say so
  if they ask why the two disagree; `TIME=utc` makes them agree.
- **Turning every segment off leaves an empty line, not a removed status line.** If
  they want it gone, that is `msu-statusline-uninstall`.
- **Polling less often is free; polling more often is not.** A poll is one request to
  the public notice board. With a cache it runs in the background; without one it can
  block a render for up to three seconds. Notices are posted on the order of days;
  anything under an hour buys nothing.

Installing and repairing belong to `msu-statusline-install`, removal to
`msu-statusline-uninstall`.
