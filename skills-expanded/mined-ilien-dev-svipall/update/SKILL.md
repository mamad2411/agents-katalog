---
name: update
description: Update Svipall to the latest stable release in one step, through its existing installation channel, and refresh the skills copied by hand. Use when the user runs /svipall:update or asks to check for, install, or manage Svipall updates.
---

# Update Svipall

Asking to update is the consent: do not ask again. If the user only asked whether a newer version
exists, run `svipall update --check`, report `current` and `latest`, and stop.

## 1. Update

```bash
svipall update
```

It replaces the `svipall` and `svipall-mcp` binaries shared by every harness, through the channel
that installed them, and refreshes each Svipall skill copied by hand (`skills_refreshed`).
`~/.svipall` (configuration, profiles, cookies, cache, models, managed browser) is never touched.

If `installed` is false and `update_available` is still true, `note` says why:

- Another channel (Homebrew, Scoop, Cargo, npm, container): run `install_command`, then
  `svipall update` once more.
- Windows: the running executable cannot replace itself. Ask the user to close every harness
  running `svipall-mcp`, run `install_command` in PowerShell, then `svipall update` once more.
- `channel` is `unknown`: stop and say where the executable lives; never put a second copy on
  `PATH`.

No binary at all → offer the setup flow; an update is not an installation. A binary older than
1.0.5 answers `svipall update` with an error: read `tag_name` from
`https://api.github.com/repos/ilien-dev/svipall/releases/latest` and run that tag's installer with
`--version <tag> --prefix <directory of the current svipall> --yes` (`-Version`, `-Prefix`, `-Yes`
in PowerShell). The older `svipall update --install` spelling still works.

## 2. Check the dashboard port

The restarted `svipall-mcp` must bind the same dashboard port. Read `dashboard.port` from
`svipall doctor` and see who is listening on it:

| Platform | Command |
|---|---|
| Linux | `ss -ltnpH "sport = :PORT"` |
| macOS | `lsof -nP -iTCP:PORT -sTCP:LISTEN` |
| Windows | `Get-Process -Id (Get-NetTCPConnection -LocalPort PORT -State Listen).OwningProcess` |

Nobody, or `svipall-mcp`: nothing to do. Another program: name it and its PID, and ask whether to
move Svipall to a free port. On yes, set `dashboard_port = <port>` in `~/.svipall/config.toml`,
keeping every other key. On no, say the captcha dashboard cannot start until that program frees
the port.

## 3. End with the restart

Finish with the `note` the update printed: the user must close every session that uses Svipall
(Claude Code, Codex, Cursor, OpenCode...) and open it again, which is how the harness restarts
with the new version. A Claude marketplace refreshes the plugin files on its own.
