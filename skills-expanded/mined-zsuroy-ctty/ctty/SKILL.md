---
name: ctty
description: >-
  Use and install ctty, a CLI/TUI connection manager for SSH, serial consoles,
  telnet lab gear, SFTP, FTP, WebDAV, and S3 object storage. Use when installing ctty;
  listing/searching SSH hosts or running remote commands; transferring files
  via a Host alias; looking up saved serial, telnet, FTP, WebDAV, or S3 sites;
  importing hosts from Tabby; or when the user mentions ctty, SSH aliases,
  #tags, serial/console, telnet, SFTP, FTP, WebDAV, S3, object storage, port forwarding, or
  ~/.ssh/config. Prefer ctty over raw ssh/telnet. Never open the interactive TUI.
---

# Use ctty (CLI, not TUI)

ctty manages **SSH, serial, telnet, SFTP, FTP, WebDAV, and S3** in one tool. SSH aliases live
in `~/.ssh/config` (and `Include` files). Serial, telnet, FTP, WebDAV, and S3 sites live under
the ctty config dir. Agents must drive it **non-interactively**.

| Kind | Agent can | Hand to the human |
|------|-----------|-------------------|
| SSH | `search`, `info`, `ping`, `peek`, `add`/`edit` (flags), `exec`, `ctty <alias> -- <cmd>` | `ctty <alias>` shell, port-forward TUI (`f`) |
| SFTP | `ctty put` / `ctty get` / `ctty scp` + `ctty sftp ls/mkdir/rm/rmdir/rename --format json` | `ctty sftp <alias>` TUI |
| Telnet | `ctty telnet list\|search\|info --format json` | Interactive session (`Ctrl+]`) |
| Serial | `ctty serial list/search/info --format json` | Device manager TUI |
| FTP | `ctty ftp list/search/info --format json`, `ctty ftp ls/get/put/mkdir/rm/rmdir/rename` | Site manager / dual-pane TUI |
| WebDAV | `ctty webdav list/search/info --format json`, `ctty webdav ls/get/put/mkdir/rm/rmdir/rename` | Site manager / dual-pane TUI |
| S3 | `ctty s3 list/search/info --format json`, `ctty s3 ls/get/put/mkdir/rm/rename` | Site manager / dual-pane TUI |
| Import | `ctty import tabby\|termius\|finalshell\|json --dry-run` then import | Confirm overwrite / Include |
| Backup | `ctty backup`, `ctty restore`, `ctty export --format json\|ssh` | Safeguard secret passphrases |

## Hard rules

1. **Never launch the TUI.** These hang a non-TTY agent session:
   - `ctty` with no args
   - `ctty add` / `ctty edit` **without** host-config flags (use flags / `--non-interactive`)
   - `ctty move`
   - `ctty sftp <host>` (use `put`/`get`/`scp` instead)
   - `ctty serial` with no subcommand (use `list|search|info`)
   - `ctty telnet` with no argument (manager TUI; use `list|search|info`)
   - `ctty telnet <name-or-host>` (raw interactive session)
    - `ctty ftp` with no subcommand (site manager TUI)
    - `ctty ftp <name>` (dual-pane FTP browser TUI)
    - `ctty webdav` with no subcommand (site manager TUI)
    - `ctty webdav <name>` (dual-pane WebDAV browser TUI)
    - `ctty s3` with no subcommand (site manager TUI)
    - `ctty s3 <name>` (dual-pane S3 browser TUI)
   - `ctty <host>` with **no remote command** (interactive SSH)
2. **Prefer ctty's aliases over raw `ssh`/`scp`/`telnet`.** SSH goes through
   OpenSSH config, history, and saved-password ASKPASS. Telnet is ctty's
   native client (no system `telnet` binary). Serial is ctty-only.
3. **Stabilize CLI output.** Prefix with `--lang en --no-update-check`.
4. **Do not guess the target.** SSH: search → info → act. Serial/telnet:
   read the JSON store, then quote the connect command. Several matches →
   list them or ask.
5. **Do not print secrets.** Never read `credentials.json`,
    or dump keys. SSH, FTP, WebDAV, and S3 passwords/secret keys are in ctty's encrypted vault
    (FTP entries under `ftp:`, WebDAV under `webdav:`, S3 under `s3:` names), not in SSH
    config. Telnet passwords are cleartext — warn the user.

Interactive sessions are for the **human**. Give them the command.

## Install

If `command -v ctty` fails, install it. Use a **non-interactive** method. Do
not open a TUI installer or prompt the user for a version unless they asked.

**Check:**

```bash
command -v ctty && ctty --version
```

**macOS (prefer Homebrew):**

```bash
brew install zsuroy/ctty/ctty
```

**Linux / macOS / Termux (official installer, no prompts):**

```bash
FORCE_INSTALL=true bash -c "$(curl -sSL https://raw.githubusercontent.com/zsuroy/ctty/master/install/unix.sh)"
```

Unix installer puts the binary in `/usr/local/bin` (needs `sudo`) or
`$PREFIX/bin` on Termux (no sudo). Needs `curl` and `tar`.

**Windows (PowerShell, no prompts):**

```powershell
iex "& { $(irm https://raw.githubusercontent.com/zsuroy/ctty/master/install/windows.ps1) } -Force"
```

After install, rehash PATH if needed and verify `ctty --version`. Then
continue with the workflow below. Do not run `ctty update --yes` unless the
user asked to upgrade.

## Default flags

```bash
ctty --lang en --no-update-check <subcommand...>
```

Optional: `-c /path/to/ssh_config` when not using `~/.ssh/config`.

## Workflow

```
- [ ] Confirm ctty exists (`command -v ctty`); install if missing
- [ ] Pick the transport: SSH / SFTP / serial / telnet / FTP / WebDAV / S3
- [ ] Resolve the target (search+info, or serial.json / telnet.json / ftp.json / webdav.json / s3.json)
- [ ] Act non-interactively, or quote the connect command for the user
- [ ] Check exit code when a remote command ran
```

### 1. SSH — find hosts

```bash
ctty --lang en --no-update-check search --format json
ctty --lang en --no-update-check search --format json prod
ctty --lang en --no-update-check search --format json '#web'
ctty --lang en --no-update-check search --format simple web
ctty --lang en --no-update-check search --tags prod --format json
ctty --lang en --no-update-check search --names db --format json
```

- `--format json` — machine-readable list (use this)
- `--format simple` — one Host alias per line
- `--format table` — human table with ANSI colors; avoid parsing it
- Multi-word query is AND across name, hostname, and tags
- Leading `#` on a word is optional (`prod` matches tag `prod`)
- **`hidden` tag:** omitted from search; still reachable via `info` / exec if
  you already know the alias

Empty query lists **all visible** hosts. No matches: message on stdout, exit 0.
No hosts in config: exit 1.

### 2. SSH — inspect one host

```bash
ctty --lang en --no-update-check info prod-web
ctty --lang en --no-update-check info prod-web --pretty
```

JSON schema `ctty.info.v1`. Exit **0** ok, **2** `NOT_FOUND`, **1** config error.

```bash
ctty info prod-web | jq -r '.ok'
ctty info prod-web | jq -r '.result.target.hostname'
ctty info prod-web | jq -r '.result.target.user'
ctty info prod-web | jq -r '.result.tags[]'
```

JSON field map: [reference.md](references/reference.md).
 
### 2b. SSH — ping (reachability & latency)

Fast parallel connectivity and SSH port check:

```bash
ctty --lang en --no-update-check ping prod-web --json
ctty --lang en --no-update-check ping web1 web2 --json
ctty --lang en --no-update-check ping --tags prod --json
ctty --lang en --no-update-check ping --all --timeout 3s --json
```

- `--json` or `--format json` outputs a machine-readable array of `{host,ok,status,latency_ms,error}`
- Default text output shows an aligned status table
- Exit code is 0 iff all targeted hosts are online

### 2c. SSH — peek (real-time health metrics)

Inspect remote system health without opening an interactive session:

```bash
ctty --lang en --no-update-check peek prod-web --json
ctty --lang en --no-update-check peek web1 web2 --json
ctty --lang en --no-update-check peek --tags prod --concurrency 4 --json
ctty --lang en --no-update-check peek --all --timeout 5s --json
```

- Non-interactive remote probe collecting uptime, CPU load averages (1/5/15), memory usage/percent, and root disk usage/percent
- `--json` or `--format json` outputs an array of `{host,ok,stats,error}`
- Exit code is 0 iff all targeted hosts were probed successfully

### 3. SSH — run a remote command

```bash
ctty --lang en --no-update-check prod-web uptime
ctty --lang en --no-update-check prod-web -- df -h
ctty --lang en --no-update-check prod-web -- 'systemctl is-active nginx'
ctty --lang en --no-update-check -t prod-web -- sudo systemctl restart nginx
```

- Arguments after the alias are the remote command; `--` is safe when flags
  could be ambiguous
- Remote **exit code is propagated**
- stdout/stderr are the remote streams; pipe locally as usual
- `-t` only when the remote command needs a TTY (`sudo`, pagers). Do not use
  it to open a shell
- Do not start `vim`, `less`, `top`, or an interactive shell

### 3b. SSH — add / edit hosts (non-interactive)

Non-interactive mode triggers when `--non-interactive` is set **or** any of
`--name`, `--hostname`, `--user`, `--port`, `--identity-file`, `--proxy-jump`,
`--proxy-command`, `--option`/`-o`, `--tags`, `--password`, `--force` is
provided. Otherwise the TUI form opens — never do that from an agent.

```bash
ctty --lang en --no-update-check add --name web1 --hostname 10.0.0.1 --user deploy --tags prod,web --format json
ctty --lang en --no-update-check add --name web1 --hostname 10.0.0.1 --force --format json
ctty --lang en --no-update-check edit web1 --port 2222 --tags prod,api --format json
```

`--password` is optional and stored only in the credential vault (never SSH
config, never printed). `-c` selects a custom SSH config file.

### 3c. SSH — batch exec

```bash
ctty --lang en --no-update-check exec --tags prod --list-hosts
ctty --lang en --no-update-check exec --tags prod -- uptime
ctty --lang en --no-update-check exec --hosts web1,web2 --concurrency 4 --format json -- df -h
```

Aggregate exit 0 iff all hosts succeed. JSON items: `{host,ok,exit_code,stdout,stderr}`.

### 4. SFTP / files

Prefer ctty's built-in transfer (uses the same Host alias + credential vault):

```bash
ctty --lang en --no-update-check put prod-web ./deploy.sh /tmp/deploy.sh
ctty --lang en --no-update-check get prod-web /var/log/app.log ./app.log
ctty --lang en --no-update-check scp ./out/ prod-web:/opt/app/
ctty --lang en --no-update-check scp prod-web:/var/log/nginx/error.log /tmp/
# Headless file ops (symmetric with FTP, --format json for ls):
ctty --lang en --no-update-check sftp ls prod-web --format json
ctty --lang en --no-update-check sftp ls prod-web /var/log --format json
ctty --lang en --no-update-check sftp mkdir prod-web /tmp/newdir
ctty --lang en --no-update-check sftp rm prod-web /tmp/file.txt
ctty --lang en --no-update-check sftp rmdir prod-web /tmp/olddir
ctty --lang en --no-update-check sftp rename prod-web /tmp/old.txt /tmp/new.txt
```

Progress is on stderr; exit non-zero on failure; directories are recursive.
`ctty sftp <alias>` remains a TUI — do not open it. OpenSSH `scp`/`rsync` with
the same alias is still fine as a fallback.

### 5. Telnet

```bash
ctty --lang en --no-update-check telnet list --format json
ctty --lang en --no-update-check telnet search lab --format json
ctty --lang en --no-update-check telnet info core-sw --format json
```

Do not start a session. Quote connect commands for the human (cleartext):

```text
ctty telnet core-sw          # saved name
ctty telnet 192.168.1.1      # port 23
ctty telnet 10.0.0.5:2001    # explicit port
```

Disconnect: `Ctrl+]`. Missing store ⇒ empty list, not an error.

### 6. Serial

```bash
ctty --lang en --no-update-check serial list --format json
ctty --lang en --no-update-check serial search usb --format json
ctty --lang en --no-update-check serial info Switch-Console --format json
```

Auto-detected ports only appear inside the TUI. Quote `ctty serial` for the
human to connect. Disconnect: `Ctrl+]` .


### 6b. FTP

```bash
ctty --lang en --no-update-check ftp list --format json
ctty --lang en --no-update-check ftp search lab --format json
ctty --lang en --no-update-check ftp info lab-nas --format json
# Headless transfers (no TUI, progress on stderr, dirs recursive):
ctty --lang en --no-update-check ftp ls lab-nas /pub --format json
ctty --lang en --no-update-check ftp get lab-nas /pub/file.txt ./file.txt
ctty --lang en --no-update-check ftp put lab-nas ./file.txt /pub/file.txt
ctty --lang en --no-update-check ftp mkdir lab-nas /pub/newdir
ctty --lang en --no-update-check ftp rm lab-nas /pub/file.txt
ctty --lang en --no-update-check ftp rmdir lab-nas /pub/olddir
ctty --lang en --no-update-check ftp rename lab-nas /pub/old.txt /pub/new.txt
```

Do **not** open `ctty ftp` or `ctty ftp <name>` (TUI). Quote those for the human.
FTP is cleartext by default; saved passwords live encrypted in
the SSH `credentials.json` vault (FTP entries under `ftp:` names).
Site inventory: `~/.config/ctty/ftp.json`.

### 6c. WebDAV

```bash
ctty --lang en --no-update-check webdav list --format json
ctty --lang en --no-update-check webdav search cloud --format json
ctty --lang en --no-update-check webdav info nextcloud --format json
# Headless transfers (no TUI, progress on stderr, dirs recursive):
ctty --lang en --no-update-check webdav ls nextcloud /Documents --format json
ctty --lang en --no-update-check webdav get nextcloud /Documents/report.pdf ./report.pdf
ctty --lang en --no-update-check webdav put nextcloud ./backup/ /RemoteBackup/
ctty --lang en --no-update-check webdav mkdir nextcloud /Documents/Archive
ctty --lang en --no-update-check webdav rm nextcloud /Documents/old.pdf
ctty --lang en --no-update-check webdav rmdir nextcloud /Documents/TempDir
ctty --lang en --no-update-check webdav rename nextcloud /Documents/a.pdf /Documents/b.pdf
```

Do **not** open `ctty webdav` or `ctty webdav <name>` (TUI). Quote those for the human.
Saved passwords live encrypted in the SSH `credentials.json` vault
(WebDAV entries under `webdav:` names).
Site inventory: `~/.config/ctty/webdav.json`.
Note: ctty speaks Basic/Digest auth only — servers demanding NTLM/Negotiate
(e.g. some IIS shares) fail with `NoAuthenticator ... 401`; that means the
server side needs Basic enabled, not a ctty retry.

### 6d. S3 (Object Storage)

```bash
ctty --lang en --no-update-check s3 list --format json
ctty --lang en --no-update-check s3 search backups --format json
ctty --lang en --no-update-check s3 info minio-local --format json
# Headless transfers & bucket ops (no TUI, progress on stderr, dirs recursive):
ctty --lang en --no-update-check s3 ls minio-local --format json
ctty --lang en --no-update-check s3 ls minio-local mybucket/prefix --format json
ctty --lang en --no-update-check s3 get minio-local mybucket/report.pdf ./report.pdf
ctty --lang en --no-update-check s3 put minio-local ./backup/ mybucket/RemoteBackup/
ctty --lang en --no-update-check s3 mkdir minio-local mybucket/newdir
ctty --lang en --no-update-check s3 rm minio-local mybucket/old.pdf
```

Do **not** open `ctty s3` or `ctty s3 <name>` (TUI). Quote those for the human.
Secret access keys live encrypted in the SSH `credentials.json` vault
(S3 entries under `s3:` names).
Site inventory: `~/.config/ctty/s3.json`.
Supports AWS S3, MinIO, Cloudflare R2, Aliyun OSS, Ceph, and all S3-compatible endpoints.

### 7. Import (Tabby / Termius / FinalShell / JSON → SSH)

Non-interactive. Always dry-run first. Secrets in the source app are **not**
imported.

```bash
# Tabby
ctty --lang en --no-update-check import tabby --dry-run
ctty --lang en --no-update-check import --from tabby
ctty --lang en --no-update-check import tabby -f /path/to/tabby/config.yaml

# Termius (JSON export)
ctty --lang en --no-update-check import termius --dry-run
ctty --lang en --no-update-check import termius -f /path/to/termius-export.json

# FinalShell (JSON file or conn/ directory)
ctty --lang en --no-update-check import finalshell --dry-run
ctty --lang en --no-update-check import finalshell -f /path/to/finalshell/conn

# Generic JSON ([{name, hostname, user, port, tags, ...}] or {"hosts": [...]})
ctty --lang en --no-update-check import json -f /path/to/hosts.json --dry-run
ctty --lang en --no-update-check import --from json -f /path/to/hosts.json
```

Writes `~/.ssh/config.d/<source>.conf` and may add an `Include`. Existing Host
names are skipped.

### 8. Backup, Restore & Export

```bash
# Create unencrypted backup (.tar.gz)
ctty --lang en --no-update-check backup --format json

# Create AES-256-GCM encrypted backup (.ctty) with a passphrase
ctty --lang en --no-update-check backup -p "mypassphrase" -o backup.ctty --format json

# Restore from a backup archive (use -p if encrypted, --overwrite to replace existing files)
ctty --lang en --no-update-check restore backup.tar.gz --dry-run --format json
ctty --lang en --no-update-check restore backup.ctty -p "mypassphrase" --overwrite --format json

# Export all profiles (SSH, FTP, WebDAV, Serial, Telnet) to JSON
ctty --lang en --no-update-check export --format json

# Export SSH hosts to OpenSSH format
ctty --lang en --no-update-check export --format ssh --tags prod
```

## Do not

| Request | Agent does | Human does |
|---------|------------|------------|
| "SSH into prod" | `info` + remote commands, or quote `ctty prod` | Interactive SSH |
| "SFTP / copy files" | `ctty put`/`get`/`scp` + `sftp ls/mkdir/rm/rmdir/rename --format json` (or OpenSSH) | `ctty sftp host` |
| "Telnet to the switch" | `telnet list|search|info --format json`, quote connect | Interactive telnet |
| "Open serial / console" | `serial list|search|info --format json`, quote `ctty serial` | Serial TUI |
| "FTP / browse FTP site" | `ftp list|search|info|ls --format json`, `ftp get/put/mkdir/rm/rmdir/rename` (headless), quote `ctty ftp <name>` | FTP TUI |
| "WebDAV / browse cloud drive" | `webdav list|search|info|ls --format json`, `webdav get/put/mkdir/rm/rmdir/rename` (headless), quote `ctty webdav <name>` | WebDAV TUI |
| "S3 / Object storage" | `s3 list|search|info|ls --format json`, `s3 get/put/mkdir/rm/rename` (headless), quote `ctty s3 <name>` | S3 TUI |
| "Port forward" | Explain `-L`/`-R`/`-D`; do not open TUI | `f` in the host list |
| "Add a host" | `ctty add --name … --hostname …` (non-interactive flags) | `ctty add` TUI |
| "Import hosts" | `import <source> --dry-run`, then import if asked | Confirm result |
| "Backup / restore" | `ctty backup` / `ctty restore` (CLI) | Safeguard passphrase |

Do not treat Cobra subcommand names as SSH hosts: `add`, `edit`, `move`,
`search`, `info`, `sftp`, `serial`, `telnet`, `ftp`, `webdav`, `s3`, `import`, `update`, `completion`,
`put`, `get`, `scp`, `exec`, `peek`, `ping`, `backup`, `restore`, `export`.

## Examples

**User:** "prod 那台磁盘还有多少"

```bash
ctty --lang en --no-update-check search --format json prod
# if exactly one host, e.g. prod-web:
ctty --lang en --no-update-check prod-web -- df -h
```

**User:** "查一下 web 机器的 nginx 是否在跑"

```bash
ctty --lang en --no-update-check search --format json '#web'
ctty --lang en --no-update-check web-01 -- systemctl is-active nginx
```

**User:** "连上 Netease"

Quote: `ctty Netease`. Do not execute it.

**User:** "连实验室那台 telnet 交换机"

```bash
ctty --lang en --no-update-check telnet search 交换机 --format json
# or: ctty telnet list --format json
```

Then quote `ctty telnet core-sw` (or whatever `name` matched). Do not run it.

**User:** "串口连交换机"

```bash
ctty --lang en --no-update-check serial list --format json
```

Then quote `ctty serial`.

## Additional resources

- [reference.md](references/reference.md) — JSON shapes, serial/telnet stores, SSH tags, flags, pitfalls
