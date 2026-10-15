---
name: restart-terminal
description: Rebuild the .NET terminal host, restart it, and wait for /healthz. Use after any C# change under apps/terminal, or when asked to "restart the terminal host".
---

# Restart terminal host

1. `dotnet test` - don't restart on a red suite.
2. `bun run build:terminal` (needs the VS Installer directory on PATH for `vswhere.exe`).
3. Stop the running host process (`jobpilot.exe` or the `dev:terminal` task), then start the
   new build.
4. Poll `http://localhost:4102/healthz` until it responds; report success or the failing step.
