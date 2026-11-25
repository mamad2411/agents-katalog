---
name: hyzevm
description: Use when the task needs a computer of its own — a clean Linux machine to run code, install software, browse the web, fill forms, upload files or post content — via the HyzeVM CLI (`hyzevm`) or its MCP tools. Triggers: "give the agent a computer", "run this in a VM/sandbox", "open the browser and ...", "post/upload this video", "máquina virtual", "computador do agente", hyzevm.
---

# HyzeVM — your own Linux computer

HyzeVM gives you a real Linux VM (Debian 12, own kernel, root via `sudo`) that you control by CLI or MCP.
It runs locally on the user's machine. The user can watch the screen and take over at any time.

Prefer the MCP tools when they are available (`machine_*`, `browser_*`, `desktop_*`, `request_takeover`).
The CLI is the same thing: `hyzevm <command>`. Every command takes the machine name.

## 1. Pick or create a machine

```bash
hyzevm ls                                  # what exists (state: running / paused / stopped)
hyzevm create work                         # Debian 12, no extras, ready in ~10 s
hyzevm create work --template base         # + docker, node, python, git, build tools
hyzevm create web  --template desktop      # + screen, Chromium, ffmpeg (needed for browser/desktop)
hyzevm create web  --template desktop --always-on   # 24/7: restarts if it dies, never auto-pauses
```

- Reuse an existing machine when it fits; do not create one per command.
- Templates: `minimal` (default), `base`, `desktop`. Only `desktop` has a screen/browser.
- First use of `base`/`desktop` builds an image (minutes, once). Later creates take seconds.
- Names: letters, digits, `-`, `_`.

## 2. Run commands

```bash
hyzevm exec work -- 'sudo apt-get install -y ffmpeg && ffmpeg -version'
hyzevm exec work -- python3 script.py        # exit code = the command's exit code
hyzevm cp ./video.mp4 work:/home/agent/video.mp4     # host -> machine
hyzevm cp work:/home/agent/out.txt ./out.txt         # machine -> host
hyzevm files work /home/agent                        # list a dir / print a file
```

- You are user `agent` with passwordless `sudo`. Home is `/home/agent`.
- `exec` wakes a paused/stopped machine by itself — no need to start it first.
- Quote the remote command; it runs in `bash`. Background processes must be fully detached:
  `nohup cmd >/dev/null 2>&1 </dev/null &` (otherwise `exec` hangs waiting on its output).
- MCP: `machine_exec` (returns exit code, stdout, stderr), `machine_read_file`, `machine_write_file`.

## 3. Use the browser (desktop machines) — prefer snapshots over screenshots

```bash
hyzevm browser goto web https://example.com
hyzevm browser snapshot web           # page as text: [e1] button "Sign in" … plus visible text
hyzevm browser click web e3
hyzevm browser type  web e5 "hello" --submit
hyzevm browser press web ctrl+l
hyzevm browser scroll web down 5
hyzevm browser upload web e9 /home/agent/video.mp4   # path INSIDE the machine; cp it there first
hyzevm browser wait web "Upload complete"
```

Loop: **snapshot → act on a ref → snapshot again**. Refs (`e1`, `e2`…) are only valid for the
latest snapshot; if you get "referência não existe mais", snapshot again. The Chromium profile is
persistent: logins and cookies survive restarts and pauses.

Fall back to pixels only when the page has no useful structure (canvas, games):
`hyzevm desktop screenshot web -o s.png`, then `desktop click|move|drag|type|press|scroll web …`
(screen is 1280×800). MCP: `desktop_screenshot` returns the image.

## 4. Ask the human when you are blocked — never bypass

Stop and call for help on: CAPTCHA, 2FA/verification codes, "confirm it's you", payment/legal
confirmations, passwords you do not have, or any screen you do not understand.

```bash
hyzevm takeover request web --reason "CAPTCHA on Instagram login"   # notifies the user, prints a control link
hyzevm takeover wait web --timeout 600     # prints "devolvido" when they hand control back (exit 2 = still waiting)
```

MCP: `request_takeover`, then `takeover_wait` (call again while it says `esperando`). After it returns,
run `browser snapshot` — the page has changed. **Do not try to solve CAPTCHAs or evade verification.**

### Questions for decisions (not for blocked screens)

Before anything the user should decide — **publishing, deleting, paying, choosing between options, any
irreversible step** — ask first and wait. Use `ask` for a decision, `takeover` for a screen you cannot pass.

```bash
hyzevm ask send web "Post 'Tutorial 03' to Instagram now?" --options yes,no --wait 600   # prints the answer
hyzevm ask send web "Which caption?"          # prints an id; then: hyzevm ask wait web <id> --timeout 600
```

Exit code 2 = no answer yet (the question stays pending; keep waiting with `ask wait`). MCP: `ask_human`,
then `ask_wait`. With `--options`, only those answers are accepted. **Do not act until you have the answer;
if it is "no", stop.** The user answers in the app, or with `hyzevm ask ls` / `hyzevm ask answer <m> <id> <text>`.

### Declare irreversible actions (guard)

The user may set a guard on the machine (`hyzevm guard set <m> --require publish,delete,pay,upload`). Before
**publishing, deleting, paying, uploading, sending a message** — declare it and wait; proceed only on `aprovado`:

```bash
hyzevm approve web "Publish video 'Tutorial 03' on Instagram" --kind publish   # exit 0 = go ahead
```

Exit codes: 0 approved · 3 denied (do NOT do it) · 2 no answer yet (ask again / keep waiting) · 4 **dry-run**
(the user wants a rehearsal: do everything *except* the final action, then show what you would have done).
MCP: `approve_action`. Destructive commands (`rm -rf`, `mkfs`, `shutdown`…) and file uploads in the browser are
blocked by HyzeVM itself until the user approves, even if you forget to ask.

### Safety net for big tasks

Take a restore point before anything risky; the user can roll the whole disk back if it goes wrong:

```bash
hyzevm checkpoint save web before-bulk-upload     # works while the machine runs
hyzevm checkpoint ls web
```

MCP: `checkpoint_save`, `checkpoint_list`. Only run `checkpoint restore` (MCP `checkpoint_restore`) if the
user agreed: it reboots the machine and discards what came after the point.

## Accounts and profiles

One browser profile per social account keeps logins separate: `hyzevm --profile conta2 browser goto web https://…`
(MCP: the `profile` argument on any `browser_*` tool). Never log into an account the user did not give you.

## What you did (for the user)

Everything you run is logged with a timestamp: `hyzevm activity web`. The user can also watch the screen recording
(`hyzevm record auto web on`) and a daily summary (`hyzevm summary web`). Typed text is never logged, only its length.

## 5. Secrets

The user stores secrets once: `hyzevm vault set NAME`, `vault set-file ~/.config/x --from file`.
They appear in every machine as environment variables (`$NAME`, via `/etc/environment`) and files under
`$HOME`. Use them (`exec work -- 'curl -H "Authorization: $API_TOKEN" …'`); never print their values and
never write them to logs or files you hand back. `vault_list` shows names only.

## 6. Lifecycle, snapshots, ports

```bash
hyzevm pause work        # instant, 0% CPU, resumes in <1 s (use between tasks)
hyzevm stop work         # clean shutdown (disk kept)
hyzevm snapshot save work --name clean-base   # machine must be stopped
hyzevm create w2 --snapshot clean-base        # new machine from it (~15 s)
hyzevm port publish work 8000                 # guest :8000 -> http://127.0.0.1:PORT on the host
hyzevm volume create data1 --size-gb 10       # then: create … --volume data1  (mounted at /data/data1)
hyzevm rm work           # DELETES the machine and its disk
```

- Take a snapshot **before** risky or long work so you can start over from a clean copy.
- Idle machines auto-pause after 30 min (`auto-suspend`); a pause keeps memory and processes.
- Ask before `rm` unless you created that machine yourself in this task.

## 7. Posting/uploading content (typical flow)

1. `ls` → reuse the user's machine (a `desktop` one, usually logged in already). Otherwise create one and tell
   the user to log in once via `hyzevm view <name>` (their sessions then persist).
2. `cp` the file into the machine; verify with `exec … ls -lh`.
3. `browser goto` the site's upload page → `snapshot` → `upload` the file → fill fields with `type` → `click` publish.
4. Confirm with a final `snapshot` (look for the success text/link). Report the URL back.
5. Pace like a person: one post at a time, no rapid retries. If a login/verification appears → section 4.

## Gotchas

- `error: máquina "x" não existe` → `hyzevm ls`. `… sem tela` → the machine is not a `desktop` template.
- SSH not ready right after create/resume: retry after a few seconds (`exec` already waits up to 2 min).
- Wall clock after a long pause is corrected automatically; if timestamps matter, run `date` first.
- `hyzevm doctor` diagnoses the host (QEMU, firmware, ssh, acceleration) when nothing starts.
- You cannot see the screen unless you take a snapshot/screenshot — look before you act, verify after.
