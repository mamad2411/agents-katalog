---
name: setup-mulmoclaude
description: Interactively guide MulmoClaude setup following README instructions. Checks port conflicts, host dependencies (Docker / ffmpeg / claude CLI), and common pitfalls. Respond in the user's language.
allowed-tools: Read, Bash, Glob, Grep
---

# Setup MulmoClaude

Guide the user through MulmoClaude setup following README.md (Installation / Running the App sections). Claude handles checks and pitfall guidance.

## Step 1: Follow README setup

Read README.md Installation section and walk the user through it (`yarn install` → `.env`).

## Step 2: Port 5173 availability

```bash
lsof -i :5173 -sTCP:LISTEN
```

- **Available**: proceed
- **In use**: show PID and command. Suggest that MulmoClaude may already be running — skip to Step 4 browser open, or stop the process with `Ctrl+C`

## Step 3: Dependency check

Check each dependency below. **Install commands are NOT duplicated in this skill — README's `### Prerequisites` section is the single source of truth.** If something is missing, tell the user which dependency + which feature is affected, then point them to README's Prerequisites section.

| Dependency        | Detect                                                                               | Required for     | Skippable?                              |
| ----------------- | ------------------------------------------------------------------------------------ | ---------------- | --------------------------------------- |
| `claude` CLI auth | `claude --version` succeeds AND `~/.claude/.credentials.json` (or equivalent) exists | Agent loop       | No                                      |
| Docker running    | `which docker && docker info`                                                        | Sandbox mode     | Yes — if `.env` has `DISABLE_SANDBOX=1` |
| `ffmpeg` on PATH  | `which ffmpeg`                                                                       | Movie generation | Yes — if user doesn't generate videos   |

Docker-specific notes:

- If `which docker` is not found, point to README's Prerequisites + [Installing Docker Desktop](../../../README.md#installing-docker-desktop). Localized READMEs (`README.ja.md` / `README.zh.md` / `README.ko.md` / `README.es.md` / `README.pt-BR.md` / `README.fr.md` / `README.de.md`) have an equivalent section with a language-specific anchor — link to the one that matches the user's language
- If Docker is installed but not running, `open -a Docker` (macOS) and wait until the whale icon is steady

## Step 4: Start dev server

Ask the user to run `yarn dev` in a **separate terminal** (not as a background process — so they can `Ctrl+C` to stop).

> `[server] ... INFO  [server] listening port=3001` means ready. `[client] ➜ Local: http://localhost:5173/` alone means only the frontend is ready, backend is still starting.

Once ready, open `http://localhost:5173` and verify the General role is displayed.

## Common pitfalls

| Symptom                                  | Cause                                            | Fix                                              |
| ---------------------------------------- | ------------------------------------------------ | ------------------------------------------------ |
| `ERR_MODULE_NOT_FOUND: @mulmobridge/...` | `yarn install` not run or incomplete             | Re-run `yarn install`                            |
| `[sandbox] ... not found.`               | Host `claude` not authenticated or expired       | Run `claude` once to authenticate                |
| Movie generation hangs / silently fails  | `ffmpeg` not on PATH                             | Install ffmpeg (see README Prerequisites)        |
| Startup hangs silently                   | macOS TCC dialog hidden in background            | Check for Docker folder access permission dialog |
| `EADDRINUSE :5173`                       | Port conflict                                    | Stop the conflicting process                     |
| Vite stuck pending                       | Dependency re-optimization after lockfile change | `rm -rf node_modules/.vite && yarn dev`          |
