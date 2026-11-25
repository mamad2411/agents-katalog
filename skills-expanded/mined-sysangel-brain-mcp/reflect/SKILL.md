---
name: reflect
description: Kick off the brain's full consolidation pass in the background and
  return immediately; safe to /clear right after. Use when asked to "reflect" or
  "consolidate memory", or when the SessionStart brief says a reflect is due.
  Fire-and-forget; the pass itself runs headless.
---

# reflect

Fire-and-forget. Your only job is to start a headless Claude Code run of
/reflect-run and get out of the way. The pass takes 10+ minutes and must not
hold the session hostage. Do not do any consolidation work yourself, and do
not read the store.

Single-flight is the server's job: /reflect-run's first step claims the
hosted reflect lease (`reflect_claim`), so a second launch exits on its own
instead of double-reflecting. The headless run uses this machine's Claude
Code sign-in to the `brain` MCP server.

Run exactly one of these, then stop.

The headless pass reads untrusted transcript text, so the brain tools are an
explicit list of what `/reflect-run` calls. That includes `memory_set_status`
(the pass retires contradicted and duplicate memories) and excludes every
`device_token_*` tool, so a minted token cannot land in `reflect.log`.

Windows (PowerShell):

```powershell
$log = Join-Path $HOME ".config\brain\reflect.log"
New-Item -ItemType Directory -Force (Split-Path $log) | Out-Null
Start-Process -WindowStyle Hidden -FilePath "claude" -ArgumentList @(
  "-p", "/reflect-run", "--model", "opus",
  "--permission-mode", "acceptEdits",
  "--allowedTools", "mcp__brain__reflect_claim,mcp__brain__reflect_complete,mcp__brain__reflect_window,mcp__brain__reflect_sessions,mcp__brain__session_episodes,mcp__brain__summary_write,mcp__brain__get_episode,mcp__brain__recall,mcp__brain__remember,mcp__brain__memory_update,mcp__brain__memory_set_status,mcp__brain__state_get,mcp__brain__state_write,mcp__brain__proposal_write", "Bash(hostname)"
) -RedirectStandardOutput $log
```

macOS or Linux:

```sh
mkdir -p ~/.config/brain
nohup claude -p "/reflect-run" --model opus \
  --permission-mode acceptEdits \
  --allowedTools "mcp__brain__reflect_claim,mcp__brain__reflect_complete,mcp__brain__reflect_window,mcp__brain__reflect_sessions,mcp__brain__session_episodes,mcp__brain__summary_write,mcp__brain__get_episode,mcp__brain__recall,mcp__brain__remember,mcp__brain__memory_update,mcp__brain__memory_set_status,mcp__brain__state_get,mcp__brain__state_write,mcp__brain__proposal_write" \
  "Bash(hostname)" \
  >> ~/.config/brain/reflect.log 2>&1 &
disown
```

`nohup` + `&` + `disown` (or `Start-Process`) lets the run survive this CLI
exiting, so /clear or closing the terminal does not kill the pass.

Then report about three lines:

- consolidation kicked off in the background;
- the log path (`~/.config/brain/reflect.log`);
- safe to /clear now.

For a foreground full pass (to watch it, or to debug the consolidation
itself) invoke **/reflect-run** directly instead.
