---
name: overleap
description: Bidirectional real-time sync between an Overleaf project and a local directory using the `overleap` Node.js CLI. Use when the user mentions Overleaf, overleap, "sync my Overleaf project", "edit Overleaf locally", "pull / push Overleaf", "compile Overleaf to PDF from CLI", or asks Claude to edit `.tex` files that should reflect on Overleaf in real time. Also use when the user wants to set up or refresh their Overleaf session cookie for the CLI. Authentication uses an `OVERLEAF_COOKIE` value, stored in a per-project `.env` file or in the environment.
---

# overleap

Bidirectional real-time sync between an Overleaf project and a local directory via the `overleap` CLI (Node.js, [github.com/Axect/overleap](https://github.com/Axect/overleap)).

`overleap` connects to Overleaf with the same Socket.IO + OT protocol the browser editor uses. Local edits are streamed to the server as OT operations; remote edits land on disk through atomic writes. Once a project is just local files, **anything that can edit a file can edit Overleaf** — Neovim, VS Code, scripts, and Claude.

## Trigger conditions

Invoke this skill when the user says any of:

- "sync my Overleaf project" / "start overleap" / "edit Overleaf locally" → `overleap sync` workflow (see **Sync workflow**)
- "list my Overleaf projects" / "what projects do I have on Overleaf" → `overleap projects`
- "compile this on Overleaf" / "build the PDF via Overleaf" / "compile this paper" *while in an overleap-synced directory* → `overleap compile` (do **not** run `pdflatex` / `latexmk` locally inside the sync dir — see **Path & file rules** below for why)
- "set up overleap" / "configure overleap" / "save my Overleaf cookie" / `overleap` exits with `OVERLEAF_COOKIE is required` → **Setup flow**
- "refresh the Overleaf cookie" / "my Overleaf session expired" → **Cookie refresh** in `references/cookie-setup.md`
- The user asks Claude to edit `.tex` / `.bib` / `.sty` files in a directory that already has `.env` with `OVERLEAF_COOKIE` → assume sync is the intended flow; check whether a sync daemon is already running before starting one

## Prerequisites

1. **Node.js >= 18** and **git** (the dependency `socket.io-client` is fetched from a GitHub fork).
   ```bash
   node --version    # must be >= 18
   git --version
   ```
2. **`overleap` CLI installed**. Verify:
   ```bash
   command -v overleap && overleap --help | head -5
   ```
   If it is not on PATH, first inspect read-only the documented existing user-scoped installation and environment: the user's PATH and Node/npm prefix or nvm configuration, and any documented checkout (e.g. `~/Documents/Project/AI_Project/overleap`). Check for a usable existing binary or `node bin/overleap.js ...` entry point before declaring the CLI missing. Do not expose credential values during inspection.
   If no usable installation exists, give the exact manual command for the user's setup, e.g.:
   ```bash
   npm install -g overleap
   ```
   Do not install automatically, use sudo, or retrieve credentials as prerequisite repair. The explicit user-supplied cookie setup below is unchanged. Block only the operation requiring the missing prerequisite and finish independent authorized work.
3. **A valid Overleaf session cookie** in one of:
   - `OVERLEAF_COOKIE` environment variable
   - `.env` file in the working directory or in `--dir` (key: `OVERLEAF_COOKIE`)
   - `--cookie` / `-c` flag (least preferred — appears in process listings)

   See `references/cookie-setup.md` for how the user extracts the cookie from the browser.

## Setup flow (skill-orchestrated)

Run this when the user wants to start using overleap on a new machine, in a new project directory, or after their session expires.

1. **Verify prerequisites** (Node 18+, git, and a usable `overleap` installation). Before declaring one missing, inspect the documented existing user-scoped installation and environment read-only as described above. If it is genuinely unavailable, report what is missing and the exact manual command needed; do not install automatically, use sudo, or retrieve credentials as prerequisite repair. Pause only dependent operations and finish independent authorized work; follow the unchanged cookie rules below when setup is authorized.
2. **Decide the local sync directory**. Prefer the user's chosen folder for the Overleaf project (e.g. `~/Papers/quantum-draft`). Confirm before creating it.
3. **Create the `.env` file** inside that directory. Ask the user to paste their cookie with this exact caveat:
   > Your Overleaf session cookie grants full access to your account. It will be saved at `<dir>/.env`. Only paste it here if you trust this terminal and session transcript. Add `.env` to `.gitignore` immediately. Get it from browser DevTools → Application → Cookies → overleaf.com → copy the full cookie string (or just `overleaf_session2`). Detailed steps: see `references/cookie-setup.md`.
4. After the user replies with the cookie, write the file with `0600` permissions and append `.env` to `.gitignore`:
   ```bash
   bash scripts/init_env.sh <dir>
   ```
   The script reads the cookie from stdin (so the value never appears in argv / shell history) and refuses to overwrite an existing `.env` unless `--force` is passed.
5. **Smoke-test** with a non-destructive call:
   ```bash
   cd <dir> && overleap projects
   ```
   On success, you'll see a numbered project list. On failure with `OVERLEAF_COOKIE is required` or auth errors, surface the message verbatim and offer to re-run setup.

**Do not** echo the cookie back, log it, or paste it into commit messages. If you must reference it, say "the cookie you provided".

**Do not** run setup unprompted. Triggers are: explicit user request, or a blocked operation that returned `OVERLEAF_COOKIE is required` / `401` / `403`.

## Commands

| Command | What it does | Long-running? |
|---|---|---|
| `overleap projects` | List projects available to the logged-in account | No, returns immediately |
| `overleap sync` | Start bidirectional real-time sync daemon | **Yes — never exits until Ctrl+C** |
| `overleap compile` | Trigger remote LaTeX compilation, download `output.pdf` | No (waits for the compile to finish, ~5–60s) |

### Common flags

| Flag | Env var | Meaning |
|---|---|---|
| `--project`, `-p` | `OVERLEAF_PROJECT_ID` | Project number (from `projects` list), fuzzy name match, or 24-char Overleaf ID |
| `--dir`, `-d` | `OVERLEAF_DIR` | Local directory (default: cwd) |
| `--cookie`, `-c` | `OVERLEAF_COOKIE` | Session cookie (prefer `.env` over `-c`) |
| `--url`, `-u` | `OVERLEAF_URL` | Server URL (default: `https://www.overleaf.com`) |

Project selection:
- `-p 64a1b2c3d4e5f6...` — direct 24-hex Overleaf project ID. **The only form Claude uses in non-interactive calls.** `overleap projects` prints the ID next to each name.
- `-p "quantum"` — fuzzy match by name (must be unique; otherwise overleap re-prompts)
- `-p 3` — pick the 3rd project from the list. Interactive use only: see below.
- omit `-p` — interactive numbered list (requires a TTY)

## Project identity safety (mandatory)

Project numbers follow the **last-modified** order of the list. Any write, including your own sync a minute earlier, reorders it, so `-p 5` names a different project on the next call. Observed 2026-10-20: an upload to project 5 moved it to 2, and a verification pull with `-p 5` joined a collaborator's project instead; the shell redirect `> sync.log` inside that directory was uploaded as a new document and streamed line by line until it was deleted.

1. Resolve the project once with `overleap projects`, then always pass the **24-hex ID**. Also write `OVERLEAF_PROJECT_ID=<id>` into the sync directory's `.env`.
2. Check the first output line (`Selected:` / `Matched:` / `[daemon] Connected to project:`) against the intended name before any local write. If it differs, stop the daemon at once.
3. Since the 2026-10-20 overleap change, the first sync writes `.overleap-project` and later `sync`/`compile` in that directory refuse any other project. A fresh directory has no binding yet, so rule 1 is what protects it.
4. **Never redirect output, write logs, or create scratch files inside a sync directory.** Send logs to `/tmp` or the service log. `.log` and LaTeX build artifacts are now ignored, but any other file type (`.txt`, `.md`, `.pdf`, `.json`) is still uploaded.
5. Verification pulls go into a new empty directory under `~/scratch`, by ID, with the log outside it. Delete the directory afterwards.
6. If something was uploaded to the wrong project: restart sync in that same directory by ID, wait for `Initial sync complete`, delete the file locally, and confirm `[local→remote] Deleted <file>` in the log. If the log shows nothing, recreate the file, wait a few seconds, and delete it again. Tell the user; Overleaf History keeps the create/delete record.

## Sync workflow

`overleap sync` is a **long-running daemon** that connects via Socket.IO and never exits until you signal it (`SIGINT` / `SIGTERM`). This has consequences for how Claude should run it.

**Never invoke `overleap sync` as a foreground Bash call from Claude** — the tool will block until timeout, you cannot do further work, and if/when the harness times out the daemon is killed mid-edit.

Pick **one** of the patterns below depending on the user's setup. Default to (1) when in doubt, because it gives the user the most control.

### Pattern 1 — User runs sync in their own terminal (recommended default)

Tell the user the exact command to run in a separate terminal pane and wait for them to confirm it's running:

```bash
cd <dir>
overleap sync -p <project number or name>
```

While that daemon is running, Claude edits `.tex` files in `<dir>` directly with `Edit` / `Write`. Each save propagates to Overleaf within ~150 ms (debounced). To stop, the user hits Ctrl+C in that terminal.

This is the safest pattern: the user sees the live log (connection state, OT acks, conflict resyncs) and can intervene immediately.

### Pattern 2 — Run sync under `pueue` (per the user's global rule)

The user's `CLAUDE.md` already mandates `pueue` for long-running tasks. For overleap, create a per-project group and queue the daemon:

```bash
# One-time, per project
pueue group add overleap-<project-shortname>

# Start the daemon
pueue add -g overleap-<project-shortname> -- bash -c 'cd <dir> && overleap sync -p <id-or-num>'

# Inspect live log
pueue log <task-id> -f

# Stop cleanly (SIGINT)
pueue kill -s SIGINT <task-id>
```

Use this when the user explicitly asks for a background daemon, or when sync should outlive the current shell. **Always** confirm with the user before queueing — and never kill a pueue task belonging to another project (per the global rule).

### Pattern 3 — Background via Claude's `run_in_background`

Acceptable for short demos within a single Claude session, but the daemon dies when the session ends. Only use when the user explicitly wants it:

```bash
# Bash tool with run_in_background: true
cd <dir> && overleap sync -p <id-or-num>
```

Always tell the user this daemon is tied to the session lifetime.

### Editing while sync is running

- Edit files normally. `overleap` debounces local writes (~150 ms) and only sends OT ops once content is stable, so rapid `Edit` calls are safe.
- For new files: just create them in `<dir>`. They auto-upload (text → as Overleaf docs, binary → multipart upload).
- For deletes: `rm` in `<dir>`. Server-side delete is sent.
- For binary files (images, PDFs included as figures), uploads are throttled to 3 concurrent and retried once on transient HTTP errors.
- If the daemon log shows `Disconnected: <reason>`, it auto-reconnects with exponential backoff (1 → 30 s). No manual action needed unless the cookie expired (see cookie refresh in `references/cookie-setup.md`).

### Stopping sync

- Pattern 1: user hits Ctrl+C in their terminal.
- Pattern 2: `pueue kill -s SIGINT <task-id>`.
- Pattern 3: `KillBash` on the background shell (or end the session).

Never `kill -9` — the daemon needs SIGINT/SIGTERM to send `leaveDoc` notifications, clear debounce timers, stop the watcher, and disconnect the socket cleanly. SIGKILL leaks inotify watches and leaves the server thinking you're still connected. Note that even SIGINT does not force-flush in-flight edits — a change still inside the 150 ms debounce window at shutdown is dropped, so save and wait ~200 ms before stopping if you care about the last keystroke.

## Compile workflow (`overleap compile`)

One-shot remote LaTeX compile + PDF download. Safe to run as a regular foreground Bash call.

```bash
cd <dir> && overleap compile -p <id-or-num>
```

- Output is written to `<dir>/output.pdf` (overwrites any existing file with the same name).
- If compilation fails server-side, the script prints `[compile] Compilation failed:` and points to the log. Surface the message verbatim and offer to inspect the log via the Overleaf web UI.
- `compile` does **not** require sync to be running — it goes through the REST endpoint with the cookie + CSRF token.
- **Always prefer `overleap compile` over local `pdflatex` / `latexmk` / `bibtex` when the directory is an overleap sync target.** Local compile leaks `.aux` / `.log` / `.bbl` / `.fls` / `.fdb_latexmk` / `.synctex.gz` artifacts back to Overleaf — see Path & file rules.

## Project listing (`overleap projects`)

Safe, one-shot, non-destructive. Useful as a connectivity / auth smoke test:

```bash
cd <dir> && overleap projects
```

Output is a numbered table of `name [accessLevel] lastUpdated`. The number is what `-p N` consumes.

## Path & file rules

- `overleap` always operates relative to `--dir` (or cwd). Never run sync from `~` or any directory containing unrelated files — it will try to upload everything that's not in `IGNORE_PATTERNS`.
- The watcher ignores common noise (`.git/`, `node_modules/`, dotfiles handled by chokidar defaults, plus the patterns in `overleap/src/constants.js`). Still, **start sync in a clean directory** dedicated to that one Overleaf project.
- Do not put `.env` (with the cookie) in the same directory committed to git without first ensuring it's in `.gitignore`. The setup script does this automatically.
- **Do not run local LaTeX compilation inside the sync directory.** `pdflatex` / `latexmk` / `bibtex` / `biber` / `xelatex` produce `.aux`, `.log`, `.bbl`, `.bcf`, `.blg`, `.toc`, `.out`, `.fls`, `.fdb_latexmk`, `.synctex.gz`, and `.pdf` artifacts. Since the 2026-10-20 change `IGNORE_PATTERNS` skips `.log`, `.aux`, `.out`, `.fls`, `.fdb_latexmk`, `.synctex(.gz)`, `.xdv`, `.blg`, `.bcf`, `.run.xml`, `.toc`, `.lof`, `.lot`, `.nav`, `.snm`, `.vrb`, but **`.bbl` and the compiled `.pdf` are still uploaded**, and installations older than that change upload everything. Real consequences seen in the past: duplicate bibliography rendering on the server, conflicting compile state, noisy collaborator diffs, accidental `output.pdf` overwrite. Use **`overleap compile`** for PDF generation (server-side, returns `output.pdf` only — see Compile workflow above), or **copy `.tex` files to a separate scratch directory** for local compile testing and never touch them in the sync dir while compiling. If you've already leaked artifacts, clean them up via the Overleaf web UI's file panel or, if the project is git-tracked, `git rm` and let overleap propagate the deletes.

## Failure modes & how to react

| Symptom | Likely cause | Action |
|---|---|---|
| `OVERLEAF_COOKIE is required` | No cookie in env, `.env`, or flag | Run setup flow |
| `HTTP 401` / `HTTP 403` from `projects` or compile | Cookie expired or revoked | Re-extract cookie from browser, re-run `init_env.sh --force` |
| `Disconnected: ...` in sync log, repeating | Network blip or session expired | If brief, ignore — auto-reconnect handles it. If persistent, check cookie freshness. |
| `inotify watcher limit reached` | Linux `fs.inotify.max_user_watches` too low | Daemon prints the exact `sysctl` command — surface it to the user; they need sudo to apply |
| Compile fails with no PDF | LaTeX error on Overleaf side | Open the project in the browser and inspect the log; overleap surfaces only `success/failure` |
| `Multiple matches for "<query>":` followed by an interactive prompt | Fuzzy `-p` match was ambiguous; in a non-TTY context the prompt fails immediately with `Input stream closed` or `Invalid selection` | Re-run with the 24-char Overleaf ID from `overleap projects` (not the list number, which shifts) |
| `<dir> is bound to project "<name>" (<id>), but the selected project is <id2>. Refusing to continue.` | `-p` resolved to a different project than the one this directory was first synced with (usually a stale list number) | Do not delete `.overleap-project` to get past it. Re-run with the bound ID printed in the message; only delete the binding when the user wants the directory re-pointed |
| `Connected to project:` names a project you did not intend | Numeric `-p` after the list reordered, in an unbound directory | Stop the daemon immediately. Do not write anything in the directory. Follow rule 6 of Project identity safety if anything was uploaded |
| Local file overwritten unexpectedly | Two writers (Claude + collaborator) racing | Sync engine uses OT to merge, but if a collaborator deletes a file you just created, the server wins. Restore from git or Overleaf history. |
| Mysterious duplicate bibliography on Overleaf, or `.aux` / `.log` / `.bbl` / `.fls` / `.fdb_latexmk` files appearing in the project | Local LaTeX compile (`pdflatex`, `latexmk`, etc.) was run inside the sync directory and the build artifacts uploaded | Stop the local compile. Move it to a scratch directory outside `--dir`. Clean up the leaked artifacts on Overleaf via the web UI's file panel (or `git rm` if the project is git-tracked). For PDF output, prefer `overleap compile` instead. |

For deeper context on the protocol, OT version tracking, and edge cases the upstream project has fixed, see `references/sync-internals.md`.

## Related references

- `references/cookie-setup.md` — step-by-step browser instructions for extracting / refreshing `OVERLEAF_COOKIE`, including which cookie value(s) actually matter
- `references/sync-internals.md` — what the sync daemon does on the wire (OT, debouncing, binary uploads, reconnection), useful for diagnosing weird sync behavior
- `references/long-running-patterns.md` — concrete recipes for running `overleap sync` under `pueue`, in `tmux`, or in the background, with stop/restart commands
