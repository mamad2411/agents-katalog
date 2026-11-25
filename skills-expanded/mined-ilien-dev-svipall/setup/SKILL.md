---
name: setup
description: Install and configure Svipall on this machine — detect or install the binary, verify the MCP server answers, offer the browser download, and optionally make Svipall the preferred way this user reaches the web. Use when the user runs /svipall:setup, asks to set up or install Svipall, or when a Svipall MCP tool fails because the server is not there.
---

# Set up Svipall

Work through the steps in order. **Never run an install command, and never write to the user's
files, without showing exactly what you are about to do and getting a yes.** Nothing here is
urgent enough to justify surprising someone.

Report at the end: what changed, and how to undo it.

## 1. Is it already here?

```bash
svipall --version
```

- **It answers** with a JSON object → note the `version` and `target`, then compare it with the
  latest version before installing or changing this plugin's integration.
- **Command not found** → step 2.

For 1.0.5 and newer, run `svipall update --check`. For an older binary, read the latest stable
`tag_name` from `https://api.github.com/repos/ilien-dev/svipall/releases/latest`. State the current
version and latest version even when they are equal.

If a newer release exists, show the detected installation channel, the exact update command, and
ask the user to choose between these outcomes before writing any integration:

- **Update the shared installation** — replace the user-owned `svipall` and `svipall-mcp` binaries
  used by all harnesses on this machine, preserve `~/.svipall` and its data, then continue setup.
  Harnesses with a running MCP server must restart afterwards.
- **Keep the current version** — do not change either binary; continue installing this plugin and
  use the version already present.

Installing the plugin is not consent to update the shared binaries. If the user chooses update,
follow `../update/SKILL.md`; the old-binary fallback must use the existing installation channel.
Then run `svipall --version` again and continue with the version actually installed. If the latest
release cannot be checked, say why and ask whether to continue setup with the current version.

## 2. Install the binary

Work out the platform (`uname -s`/`uname -m`, or `$env:OS` on Windows), then show the user the
matching command from this table and ask before running it.

| Platform | Command |
|---|---|
| macOS / Linux | `curl -fsSL https://raw.githubusercontent.com/ilien-dev/svipall/main/install.sh \| sh` |
| Windows | `irm https://raw.githubusercontent.com/ilien-dev/svipall/main/install.ps1 \| iex` |
| Any, prefers a container | `docker pull ghcr.io/ilien-dev/svipall:latest` |

Homebrew, Scoop, winget, the AUR and npm are **not published yet**, so never suggest them: the user
gets `No package found matching input criteria` and concludes the tool is broken.

After a script install, `svipall --version` may still fail in **this** shell because PATH was
changed for new shells only. Try the absolute path the installer printed (`~/.local/bin/svipall`,
or `%LOCALAPPDATA%\Programs\svipall\svipall.exe`) before concluding anything went wrong, and tell
the user to open a new terminal.

If the user chose Docker, the MCP command is
`docker run -i --rm -v svipall-home:/data ghcr.io/ilien-dev/svipall:latest` — see step 4.

## 3. Check the installation

```bash
svipall doctor
```

It returns one JSON object. `ok: true` means there is nothing to do. Otherwise walk `problems[]`
and relay each `message` with its `fix`, in the object's own words. Two you will meet often:

- `no_browser` — offer `svipall browser install`. **Say that it downloads about 190 MB** and wait
  for a yes. Only the plain http tier works without it, so any page behind a challenge stays
  blocked; that is a real limitation to state, not a detail to skip.
- `dashboard_port_busy` — usually a `svipall-mcp` already running. Harmless; say so.

## 4. Wire up the MCP server

This plugin already ships an MCP entry that runs `svipall-mcp` from PATH, so if step 1 or 2
succeeded there is normally nothing to do. Confirm it by calling any Svipall MCP tool — for
instance `web_status`.

If the tools are not there:

- **The binary is not on PATH for the process that launched Claude Code.** Register it by absolute
  path instead: `claude mcp add -s user svipall -- /absolute/path/to/svipall-mcp`
- **Docker install.** `claude mcp add -s user svipall -- docker run -i --rm -v svipall-home:/data ghcr.io/ilien-dev/svipall:latest`

Either way, tell the user to restart Claude Code afterwards.

## 5. Offer: prefer Svipall for web access (optional)

Ask, do not assume. This writes to the user's **global** memory, which affects every project they
open.

> "Want Claude to reach for Svipall instead of the built-in web fetch, in every project? It adds
> one import line to `~/.claude/CLAUDE.md` and a file next to it. `/svipall:uninstall` removes
> both."

On yes:

1. Copy the plugin's `memory/SVIPALL.md` to `~/.claude/svipall/SVIPALL.md`, creating the directory.
   That file is at `../../memory/SVIPALL.md` relative to this skill — resolve it from this file's
   own path, not from the working directory. If you cannot find it, fetch
   `https://raw.githubusercontent.com/ilien-dev/svipall/main/plugins/svipall/memory/SVIPALL.md`
   instead of writing your own version of it. Overwriting the destination is fine — it is ours.
2. Read `~/.claude/CLAUDE.md` (create it empty if absent). **Ask a second time before writing, and
   ask in plain words.** Assume the user has never seen a memory file: three lines of markup shown
   on their own tell them nothing, so the block alone is not a question anybody can answer. Say,
   before showing it:

   - **what that file is** — the standing instructions Claude Code reads at the start of every
     session, in every project on this machine;
   - **what the line does** — `@svipall/SVIPALL.md` pulls in the page you just copied next to it,
     which is what tells Claude to reach the web through Svipall instead of the built-in fetch;
   - **what it does not do** — nothing else in the file is read, moved or rewritten, and no project
     of theirs changes;
   - **how to undo it** — `/svipall:uninstall`, or delete the marked block by hand; a dated backup
     of the file is kept either way.

   Then show the block and the full path it goes into:

   ```
   <!-- BEGIN SVIPALL -->
   @svipall/SVIPALL.md
   <!-- END SVIPALL -->
   ```

   Offer the two choices as outcomes, never as a bare yes/no: *add it — Claude prefers Svipall for
   web access everywhere*, against *skip it — Svipall stays installed and usable, Claude just will
   not reach for it on its own*.

3. Copy `~/.claude/CLAUDE.md` to `~/.claude/CLAUDE.md.bak-<YYYYMMDD-HHMMSS>` first.
4. If the markers are already present, replace what is between them. Otherwise append the block.
   Never add a second copy, and never touch anything outside the markers.

## 6. Offer: strict mode (default: no, and say so)

Step 5 already makes Claude prefer Svipall. Strict mode only covers the case where it forgets, and
it does so with a hard refusal: the hook **denies** `WebFetch` and `WebSearch` outright, with no
fallback. So if the Svipall MCP server is ever not answering — not installed on that machine, not
on PATH, failed to start — the session has no web access at all, not even the built-in one.

Recommend against it on a fresh install, in as many words, and offer it anyway:

> "There is also a strict mode: Claude Code's own `WebFetch` and `WebSearch` stop working, declined
> with a pointer to the Svipall tool that replaces them. I would leave it off for now — if
> Svipall ever fails to start, a strict session has no way to reach the web at all. The line above
> is already enough to make Claude prefer Svipall. You can turn this on later with one file."

Put the warning in the choices too, not only in the prose above them — somebody who reads nothing
but the two labels must still see it: *leave it off — Claude prefers Svipall anyway, and the
built-in fetch stays as a backstop*, against *turn it on — the built-in fetch stops working, even
on a day Svipall does not start*.

Turn it on without hesitation if the user asks for it, and say the same thing if they turn it on
after using Svipall for a while — by then they know it starts.

On yes, create the empty marker file `~/.svipall/claude_strict`. Deleting it turns strict mode off
again, immediately, with no restart. Leave it alone if the user did not ask.

## 7. Say what happened

List, plainly: the binary and where it landed, whether the browser was installed, whether the
memory block was added, whether strict mode is on, and that `/svipall:uninstall` reverses the last
three. If anything was left undone — a `doctor` problem the user declined to fix — say that too
rather than reporting success.
