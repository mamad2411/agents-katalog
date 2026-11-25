---
name: parallel-branches
description: Runs several git branches side by side, each in its own worktree with its own dev server and port, so they can be compared in the browser. Use when the user wants to work on multiple tasks or branches at once, run different branches at the same time, check two branches in a browser together, open a CORS-free dev browser for a locally running app, or stop and clean up the servers and worktrees it started.
license: MIT
compatibility: Requires git and python3 (3.9 or newer). Chrome or Chromium is needed only for the dev-mode browser. Tested in CI on Linux, macOS and Windows; Windows has limits (see references/safety.md).
---

# parallel-branches

One script, `scripts/pb.py`, manages everything. It uses only the Python standard library. In the examples below, `PB` is shorthand for `python3 <this skill's directory>/scripts/pb.py`. When you run it, write the full path out in every command and do not put it in a shell variable: approval rules match the literal command text, so `python3 /full/path/pb.py up ...` can be pre-approved and `python3 $PB up ...` cannot. Run it from inside the user's repository, or pass `--repo <path>`.

## What it does

For each branch it creates a git worktree, copies or installs dependencies, picks a free port, starts the dev server detached, waits until the server answers, and records everything in `.git/parallel-branches/`. It can also open a separate Chrome profile with web security off for apps that hit CORS errors.

## Workflow

1. **Plan first, then stop and ask.** Run `PB up <branch> [<branch>...] --dry-run --json`. It shows, per branch, the detected stack, the exact start command, the install plan and the port. Show these to the user, including every line that starts `hook <event>:`, and say that a repository can supply its own commands and hooks through `.parallel-branches.json`, so they deserve a read. Then end your turn with the question. Do not run `PB up` without `--dry-run` in the same turn. A request like "get these running" is not approval of the commands; only a reply to your plan, or a message that explicitly says to go ahead with whatever plan you propose, is.
2. **Start.** Run `PB up <branch> [<branch>...]`. Add `--cmd '<command with {PORT}>'` when detection found nothing or the user wants a specific command. Add `--create` only if the user wants a new branch made from HEAD.
3. **Report.** Give the user one URL per branch. Quote any `WARNING` lines. Say how many servers are running; more than three or four will strain a laptop.
4. **CORS.** If the output says `CORS risk found`, or the user reports CORS errors, run `PB browser <branch>`. It opens a throwaway Chrome profile with web security off. Tell the user that web security is off in that window and that it only opens the app's own localhost URL. Also say what it does not fix: OAuth and OIDC redirect URIs (a login pinned to one port), `Origin` or CSRF checks, and cookies. It only removes CORS errors, so if the app's login still fails, that is why.
5. **Check later.** `PB status` lists branches, health and dev browsers. `PB status --json` is for parsing.
6. **Finish.** Ask before `PB down <branch>` or `PB down --all`. Ask again, separately, before `PB clean --yes`. Plain `PB clean` is a dry run and is safe.

## Branches with several services

Some branches need more than one process, such as a web front end plus an API. The repository describes them in `.parallel-branches.json` under `services`; see `references/stacks.md`. Then:

- `PB up --dry-run` lists every service with its own port and the exact command, in start order. Show all of them.
- A service starts only after the services it `depends_on` answer. If one fails, the ones already started are stopped again.
- `{url.NAME}` and `{ports.NAME}` in a command or env value become the other service's address, so the web app can find its API.
- The primary service (marked `primary`, otherwise the last listed) is the one whose URL you give the user. Mention the others too.
- `PB status` shows one row per service, as `branch:service`. `PB down` stops all of them.
- A service that calls another one on a different port is a CORS risk. Treat the `cross-service` warning the same way as any other CORS risk and offer `PB browser`.
- Passing `--cmd` ignores `services` and runs that single command.
- To pick up a code or config change in one service, use `PB restart BRANCH SERVICE`. It keeps the port, so URLs and `{url.NAME}` references stay valid.
- If `up` says the project looks like a monorepo, run `PB init`, show the user the suggested services and notes, and ask before `PB init --write`. It guesses commands from each app's stack and does not guess `depends_on` or which app calls which, so ask the user about those.

## Hooks

A repository can run its own commands at fixed points through `hooks` in `.parallel-branches.json`: `post_create`, `pre_start`, `post_start`, `pre_stop`, `pre_remove`, `post_remove`. They are how a branch gets its own database or seed data. See `references/hooks.md`.

- `PB up --dry-run` prints each hook with its ports and names filled in (`hook post_start: ...`). Hooks from the user's own config file show as `hook post_start (user): ...` and run in every repository, before the repository's. Show those too. They run in a shell, so show them to the user as part of the plan and wait for approval, like start commands.
- `post_create` and `pre_start` failing stops `up` before any server starts. `pre_remove` failing keeps that worktree (`PB clean --yes --no-hooks` removes it anyway, but ask first). `post_start`, `pre_stop` and `post_remove` failing is only reported (`WARNING hook ...`), and the branch still starts, stops or is removed.
- `down` and `clean` run the commands stored when the branch was started, not the current file. `PB clean` without `--yes` lists the `pre_remove` and `post_remove` commands it would run. Mention them when you ask before `PB clean --yes`.
- `--no-hooks` on `up`, `down` or `clean` skips them. Use it if the user does not trust the repository's hooks. `up --hook-timeout N` changes the per-command limit.
- `PB hook EVENT BRANCH` runs one stored hook of a tracked branch by hand (`--dry-run` shows it). Show the dry run and get approval first, as for any hook.
- `PB hooks [BRANCH] [-v]` shows what a branch stored, with values filled in and the last result of each (read only).
- With `"background_hooks": ["post_start"]` in the config, `post_start` runs detached: `up` returns once the servers are healthy, and the dry run marks it `(background)`. Check the result later with `PB hooks BRANCH`; `down` stops it if still running.
- A hook step written as an object of named commands runs them at the same time; the dry run shows it as `together: [name] ...`.
- `restart` runs no hooks.

## Commands

| Command | Purpose |
|---|---|
| `PB up BRANCH... [--cmd CMD] [--dry-run] [--no-install] [--no-hooks] [--browser] [--json]` | Create worktrees, install, start, health-check |
| `PB status [--json]` | Show branches, URLs, health, dev-browser endpoints |
| `PB browser BRANCH [--path /x] [--headless]` | Open a dev-mode browser for a running branch |
| `PB hooks [BRANCH] [-v] [--json]` | Show stored hooks with values filled in (read only) |
| `PB down BRANCH...` or `--all` `[--no-hooks]` | Stop only the processes this tool started, and close their dev browsers |
| `PB clean [--yes] [--force] [--no-hooks]` | Remove worktrees this tool created. Dry run without `--yes` |
| `PB restart BRANCH [SERVICE]` | Restart one service, or all of them, on the same ports |
| `PB init [--write]` | Suggest a `services` config for a monorepo. Printing writes nothing |
| `PB detect [PATH]` | Show the detected stack, config, install plan and any monorepo suggestion |

`{PORT}` and `{HMR_PORT}` in `--cmd` are replaced, and both are also exported as environment variables. `BROWSER=none` is always set so dev servers do not open a browser by themselves.

## Reading the results

- **`FAILED: ... exited with code N`**: the log tail is printed. Fix the cause or pass `--cmd`.
- **Low confidence stack** (Create React App, Go, an unknown Node project): only the `PORT` variable is set. If the server ignores it, the health check times out. Find the right port flag and pass `--cmd`.
- **`port N is answered by another process`**: something else owns the port. Use `--no-verify-owner` only for servers that daemonize on purpose, such as Docker.
- **`WARNING file:line url [other-local-port]`**: the app has a hardcoded URL that will not match the new port. A dev-mode browser does not fix lines marked auth/redirect: OAuth and OIDC redirect URIs, `Origin` checks and shared cookies are server-side or cookie problems. Tell the user plainly.
- **`WARNING copied database settings`**: separate ports do not isolate databases. This warning lists only file and variable names from copied env files, not values. It points to the per-branch hooks workaround in `references/stacks.md`; env values are not rewritten.
- **More than one stack found**: `detect` lists `alternatives`. Ask which one to run.

## Rules

- Never start servers (`PB up` without `--dry-run`) before the user has approved the plan you showed. The commands come from the repository and run in a shell on their machine.
- Never run `PB down`, `PB clean --yes` or `PB up` with hooks the user has not seen. Teardown hooks run commands stored from the repository config.
- Never kill a process this tool did not start. `down` checks a recorded start time before killing, and refuses if the PID was reused.
- Never open the user's real browser profile with web security off. Only `PB browser` does this, and it always uses an empty throwaway profile.
- Do not use `clean --force` without telling the user it removes uncommitted work.
- Do not edit tracked files to change ports. Pass the port through the command or environment.

## Attaching a browser agent

`PB browser` prints a DevTools endpoint such as `http://127.0.0.1:9222`. A Playwright-based agent can attach to it over CDP. The Claude in Chrome extension drives the user's own profile and cannot use this endpoint. Playwright MCP takes its endpoint when it starts, so attaching it to this browser means starting it with `--cdp-endpoint` (tested with `@playwright/mcp` 0.0.84).

## More detail

- `references/stacks.md`: supported stacks, install rules and the `.parallel-branches.json` format.
- `references/hooks.md`: hook events, variables, failure rules and the trust model.
- `references/browser-dev-mode.md`: what the dev-mode browser fixes and what it cannot.
- `references/safety.md`: what the tool touches and what to be careful about.
