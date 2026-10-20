---
name: investigating-disk-images-by-emulation
description: 'Disk-image forensics by emulation — boot the image into a running VM (Linux server OR Windows) and investigate the live system over SSH. For QUESTIONS about the image this is the ADVANCED path, NOT the first one: an image is an image, so FIRST parse it as a forensic case with the 火眼 (GoldenEyes) `ges` chain, exactly like any other exhibit, and emulate only when the answer is runtime-only state (running services/processes, listening ports, effective post-startup config) or needs free-form exploration inside the live system. But for REBUILD / RESTORE tasks — 重建网站 / 还原数据库 / get the exhibit''s own services running so the examiner can log into the admin panel — this playbook is the REQUIRED path: the reconstruction always happens INSIDE the booted guest, never by installing database servers or runtimes (MySQL/PostgreSQL/MongoDB/PHP/…) or Docker stacks on the analysis workstation, nor by re-hosting the site there.'
domain: cybersecurity
subdomain: digital-forensics
tags:
- server-forensics
- disk-image
- vm-emulation
- ssh
- live-system
- incident-response
- windows
version: 1.1.0
author: honglian
---

# Investigating Disk Images by Emulation

Booting a disk image as a live VM and investigating it from the inside over SSH is the **advanced** path, not the first one. It is the right tool for evidence that exists only while the machine runs — but it is slower, heavier, and has far more moving parts than parsing the image as a forensic case.

This applies to **Linux server images and Windows images alike**: the emulation tool boots either, and for a Windows guest it provisions an SSH service during emulation, so `ssh_exec` reaches both.

## Parse the image as a case FIRST

An image is an image. Like every other whole-exhibit image, its **first pass** is the 火眼证据分析 (GoldenEyes) case chain driven by the `ges` CLI: parse the whole exhibit into a structured case, then query it. Open the `analyzing-device-images-as-cases` skill and follow it.

Do this **before** you emulate anything. Most questions are answered straight from the parsed case, faster and with far less that can go wrong: OS version, installed packages, users and credentials, web application source and config, database contents, log contents, scheduled tasks / cron / systemd units on disk.

**"I need to look at files on the disk" is NOT a reason to boot the image.** The parsed case exposes the exhibit's raw filesystem under `/evidence_mounts/` — browse it with `ges ls`, locate files with `ges glob -p '<pattern>' --path /evidence_mounts/`, read them with `ges read`, and pull them out with `ges copy`. Anything you would have gone looking for with `ls` / `find` / `grep` inside a booted guest, you can reach through `ges` without booting anything.

## When to emulate

Emulate **only** after you have actually tried the parsed case and it cannot get at the answer. Before you boot anything, you must have run `ges status`, tried to locate the target under `/evidence_mounts/` (`ges ls`, `ges glob -p`), and be able to state in one sentence what `ges` could not give you.

Legitimate reasons to emulate:

- **Runtime-only state** — which services / processes are actually running, which ports are actually listening, the effective configuration after startup (merged config, environment variables, values resolved at boot).
- **The filesystem is not fully reachable** through `/evidence_mounts/` — a volume the suite did not mount, an encrypted / LVM / RAID volume that only assembles at boot, container layers you cannot resolve statically.
- **Free-form exploration inside the live system** — the question needs you to run arbitrary commands and follow wherever they lead. This is what `ssh_exec` on a booted guest is for, and it is the one thing the parsed case cannot do.
- **Rebuild / restore / run tasks** — the deliverable is the exhibit's own services running again: rebuild the website, restore a database from a backup dump, let the examiner log into the running admin panel. The parsed case can only locate the pieces (source, configs, dumps); only the booted guest can run them. All reconstruction happens inside the guest — see "Rebuilding services inside the guest" below.

**Not** reasons to emulate: reading a file, reading a config, reading a database or a log, listing a directory, or searching the filesystem. All of that is `ges`.

If the parsed case answers the question, you are done — do NOT boot the image just to confirm it.

Whichever path you are on, do **not** hand-roll raw image parsing: never install image-parsing libraries (`pytsk3`, `libewf`, …) or mount the raw `.E01` / `.dd` yourself just to read one value. That is the slow, fragile path.

## The emulation chain

When the emulation capability is available, drive it end to end without bothering the user:

> **`create-vm` is a skill, not a tool or a command.** It is delivered by the installed 火眼仿真取证 (BootMagix) app and shows up in `<available_skills>` like any other skill. Invoke it the normal way: `read` its SKILL.md, which tells you to run its bundled `bootmagix-cli.exe` via `exec` (`bootmagix-cli.exe create --image "<path>"`, then `get-ip`). It is **not** an MCP tool and **not** an executable on `PATH` — do **not** go looking for it with the tool-search (`mcp`) mechanism, `where.exe create-vm`, or `Get-Command`. Whether it is "available" is decided by one thing only: is it listed in `<available_skills>`? If it is not listed, a tool/command search will always come up empty — that is expected and is **not** evidence that emulation failed; follow "If emulation is NOT available" below.

1. **Emulate the image as a VM.** Use the `create-vm` skill to boot the target image — Linux server or Windows — into a running virtual machine. Keep the source image read-only and in place — never copy it into the workspace.
2. **Get the IP, then wait for SSH to come up — do not connect immediately.** After `create-vm` reports the VM started, resolve its IP (create-vm's `get-ip`). The guest is still booting: its SSH service is **not** reachable for a while after start, and a first attempt fired too early just gets "connection refused". Before your FIRST SSH attempt, give it time — either poll the SSH port until it accepts (e.g. `Test-NetConnection -ComputerName <ip> -Port 22 -InformationLevel Quiet` in a short wait loop, up to ~2–3 minutes) or simply wait ~60 seconds. Treat an early connection-refused as "still booting": keep waiting and retry — do NOT abandon the SSH path or fall back to offline. **A Windows guest takes longer**: the SSH service is installed into it as part of emulation, so give it more time before you conclude anything is wrong.
3. **Drive the live system over SSH.** Use the built-in `ssh_exec` tool to connect into the running VM and run your forensic commands (enumerate running services and listening ports, inspect runtime config, explore freely). Use the credentials per create-vm's account handling (e.g. a freshly reset Linux `root` password).
   Commands must match the guest's shell: a Linux guest runs them through a login shell; a **Windows guest runs them through `cmd.exe`**, so wrap PowerShell in `powershell -Command "..."` and never send bash syntax. If you are unsure which you are on, run `uname` — it fails on Windows.
4. **Report the findings — see "Answering & output" below.** By default, answer the user directly in the conversation; write files to the workspace only when the deliverable is itself a file. The source image stays untouched.

### If emulation is installed but not started

`create-vm` depends on the "火眼仿真取证" (BootMagix) application already running. If `create-vm` reports that its dependency app is not running (`discovery_failed`, or exit code 3), do **not** treat this as a real failure and do **not** fall back to offline analysis. Instead:

1. Call the `open_application` tool with the application identifier `bootmagix` (equivalently `GE-BootMagix`) to start "火眼仿真取证".
2. Wait a few seconds for it to initialize.
3. Retry `create-vm` (a few attempts at most).

Only conclude there is a real problem if `create-vm` still cannot proceed after the app has been started and given time to become ready.

## Finding things inside the booted system

The guest's disks are the evidence images, served through a virtual-disk layer: **every byte the guest reads is decompressed on the host**. Reading a whole filesystem therefore costs minutes to tens of minutes, prints nothing while it runs — which is indistinguishable from a hang — and gets killed by `ssh_exec`'s idle timeout long before it finishes.

So: **locate by path first, search by content last.** The steps below are for a Linux guest; the Windows equivalents follow.

1. **Mount the disks you need.** Extra evidence disks are often not mounted. Look with `lsblk`, then mount read-only: `mkdir -p /mnt/<name> && mount -o ro /dev/<part> /mnt/<name>`.
2. **Walk to the target directory before searching anything.** Web and application payloads live in a handful of places — list them directly with `ls`: `/root`, `/home/*`, `/opt`, `/srv`, `/data`, `/var/www`, and container volumes under `/var/lib/docker`.
3. **Search by filename whenever the thing you want has a known name.** Bound the depth and prune `node_modules`:
   `find /mnt/web2/root /mnt/web2/home /mnt/web2/opt -maxdepth 4 \( -name 'next.config.*' -o -name 'package.json' \) -not -path '*/node_modules/*' 2>/dev/null`
   To identify a web framework, read the `dependencies` of the `package.json` you found — do not search the filesystem for the product's name.
4. **NEVER run a recursive content search rooted at `/` or at a mount point.** `grep -r <pattern> /mnt/web2/` reads every byte of an entire root filesystem — `/usr`, `/snap`, `swapfile`, `swap.img`, every `node_modules` — and is always the wrong command, no matter how narrow the pattern looks. Wanting to full-text-search the image is itself a signal that you are on the wrong path: go back and query the **parsed case**, whose index exists precisely for that.
5. **When you genuinely must search file contents**, root the search at a directory you have already confirmed holds the target, and always pass both guards:
   `grep -rl --binary-files=without-match --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=vendor --exclude-dir=dist '<pattern>' /mnt/web2/root/<app>`
6. **`| head -N` does NOT bound the cost.** It stops the search only once N matches exist; a search that matches nothing still scans everything. The fewer matches there are, the longer it runs. Never use it as a limit.
7. **Prefer commands that print as they go.** A command that stays silent for tens of seconds hits the idle timeout and is killed, and you lose whatever it had found.

### On a Windows guest

Same doctrine, different commands. Extra volumes show up as drive letters — list them with `powershell -Command "Get-Volume"`. Locate by name, bounded to the directories that plausibly hold the target:

`powershell -Command "Get-ChildItem -Path C:\inetpub,C:\Users,C:\ProgramData -Recurse -Depth 4 -Filter 'web.config' -ErrorAction SilentlyContinue | Select-Object -First 20 -ExpandProperty FullName"`

**Never content-search a whole volume** — `Select-String -Path C:\ -Recurse` and `findstr /s /i "<pattern>" C:\*` are exactly the same pathological full-disk read as `grep -r /`, and will be killed by the idle timeout after wasting minutes.

## Rebuilding services inside the guest (网站重建 / 数据库还原)

When the task is to get the exhibit's own services running again — rebuild the website, restore a database from a backup dump, let the examiner log into the web admin panel — emulation is not the advanced path but the ONLY path: the deliverable IS the booted guest. The image already contains the complete original runtime — the exact database / language-runtime / web-server versions the site was built against, the deployed source tree, its configs, and the panel scripts (宝塔/bt, `/xp`, …) that start it all. Boot it and rebuild inside it.

**All reconstruction happens INSIDE the booted guest. Never rebuild on the analysis workstation (the host).** Concretely, on the host you do NOT: install any database server, runtime, or web server (MySQL, PostgreSQL, MongoDB, Redis, PHP, nginx, …); stand up Docker / docker-compose stacks; download server runtimes from the internet; or edit an extracted copy of the site's config to point it at host services. Each of these looks like progress and is not:

- *"The host has Docker, that's the fastest way"* — the workstation is usually offline: image pulls and runtime downloads fail, and even a host stack that limps up runs different versions with different extensions against a hand-modified config — a reconstruction that no longer demonstrates anything about the evidence.
- *"Emulation is flaky right now, I'll build locally in parallel"* / *"I'll keep Docker as a plan B"* — a host rebuild is NOT a fallback for a rebuild task, not even as a written-down "backup option" or "functional demo": once emulation stalls you will execute it. There is no plan B on the host. Fix the emulation instead: restart its app per "installed but not started" above and retry. If emulation still cannot run after real retries, STOP and tell the examiner what failed and what you tried — a host reconstruction happens only if the examiner explicitly asks for one after that.

The sequence:

1. **Recon in the parsed case first** (no boot needed): with `ges`, locate the web root, the DB config — **which DBMS the site uses** (MySQL/MariaDB, PostgreSQL, MongoDB, Redis, SQL Server on a Windows guest, …) plus db name / user / password / table prefix — any backup archives, and the panel layout. Extract to the workspace ONLY what must come from outside the image — e.g. a separately handed-over dump exhibit (unzip on the host if password-protected), and note its format: text SQL dump, `pg_dump` custom format, `mongodump` BSON directory/archive, …
2. **Boot the image and get its IP** — the emulation chain above.
3. **Start the stack inside the guest**: see what the image itself uses (`systemctl`, the panel's own scripts) and start its web server / runtime / database services. Check whether the site's database is already intact in the image — restore only what is actually missing or broken.
4. **Restore any external dump INTO the guest's database.** The database the site reads is the one inside the guest — that is the only valid restore target, whatever the DBMS is. Two routes get the dump there:
   - **Default — copy the dump into the guest, restore with the guest's own native client.** Needs nothing on the host (`scp`/`ssh`/`ssh-keygen` ship with Windows 10+ out of the box — do not go installing anything), the client version always matches the server, localhost credentials always work, and binary backup formats get the native tool they require. `ssh_exec` only runs commands — it cannot upload files, and the host's own `scp`/`ssh` cannot answer a password prompt from a non-interactive shell. Do the one-time key setup, then copy:
     - host: `ssh-keygen -t ed25519 -N '""' -f <workspace>\vm_key` (in PowerShell, `-N '""'` passes an empty passphrase)
     - guest via `ssh_exec`: `mkdir -p /root/.ssh && echo '<pubkey>' >> /root/.ssh/authorized_keys && chmod 700 /root/.ssh && chmod 600 /root/.ssh/authorized_keys`
     - host: `scp -i <workspace>\vm_key -o StrictHostKeyChecking=no <dump> root@<vm-ip>:/root/` (`-r` for a mongodump directory)
     Then restore inside the guest with the credentials found in step 1, using the DBMS's own tool, e.g.:
     - MySQL/MariaDB: `mysql -u<user> -p'<password>' <db> < /root/<dump>.sql` (create the database first if it is missing)
     - PostgreSQL: `sudo -u postgres psql <db> < /root/<dump>.sql`, or `sudo -u postgres pg_restore -d <db> /root/<dump>` for custom-format backups
     - MongoDB: `mongorestore --db <db> /root/<dumpdir>` (add `-u/-p --authenticationDatabase admin` if auth is enabled)
   - **Alternative — restore over the network from the host**: connect to the database port the guest exposes (3306 MySQL / 5432 PostgreSQL / 27017 MongoDB / …) and replay the dump into it, ONLY after verifying the guest's DBMS accepts remote connections — each has its own knobs (MySQL: `bind-address` + a `'<user>'@'%'` grant; PostgreSQL: `listen_addresses` + a `pg_hba.conf` host rule; MongoDB: `bindIp`; plus the guest firewall in every case — check, and enable via `ssh_exec` if needed). Any **client** on the host will do: the DBMS's native CLI if present, or — when the host has none but has Python — a few lines with the matching driver (`pymysql` / `psycopg2` / `pymongo`, pip-installable; adding a client library to the host is fine, it is servers that are forbidden). A script must stream a text dump, never read 1 GB into memory. Statement-by-statement replay (accumulate lines until one ends with `;`, execute, repeat) is safe for MySQL dumps because mysqldump escapes newlines inside string literals — but a PostgreSQL plain dump's `COPY ... FROM stdin` data blocks and every binary format (pg_dump custom, mongodump BSON) do NOT replay that way: for those, take the default route and use the guest's native tool. The data still lands in the guest's database: connecting from the host to a service the guest runs (its DB port, its web port) is always fine — what is forbidden is running a database or web **server** on the host.
   Either way, importing a gigabyte-scale dump stays silent for minutes and can be killed by a tool's idle timeout — run it detached and poll instead (e.g. in the guest: `nohup mysql ... < /root/<dump>.sql > /root/import.log 2>&1 &`, then check the log and table counts; same pattern for `psql`/`pg_restore`/`mongorestore`).
5. **Verify from the host, then hand over.** `curl http://<vm-ip>/` (or the site's port). If the vhost is bound to a domain name, map that domain to the VM IP in the host's hosts file (or adjust the guest's server config) so the examiner's browser reaches the right site. Deliver: the URL to open (plus the hosts-file line if one is needed), the admin-panel path, and the credentials you found. The examiner does the logging in — do not stop at "the services are running".

## If emulation is NOT available

"Not available" has exactly one meaning: **`create-vm` is absent from `<available_skills>`.** Do not diagnose availability any other way — a `mcp` tool search or a `where.exe create-vm` returning nothing tells you nothing (create-vm is a skill, never a tool/command; see the note under "The emulation chain"). If it *is* listed but its dependency app is not running, that is not "unavailable" — that is the `discovery_failed` case handled under "If emulation is installed but not started" (call `open_application`, then retry).

When `create-vm` genuinely is not listed, the "火眼仿真取证" (GE-BootMagix) application that provides it is not installed. You cannot install it yourself.

You are not stuck. The parsed case is still there: go back and check whether `ges` can answer the question after all — `/evidence_mounts/` covers everything that is on disk, and only genuinely runtime-only evidence needs a booted machine. If the answer really does require booting — and a rebuild / restore task always does — use the conversation and the `ask_user` tool to guide the user to install "火眼仿真取证" from the application library, then resume the chain once it is available. Do NOT silently drop to raw offline parsing — and in particular do NOT jump to hand-rolled image parsing (`pytsk3`/`libewf`, mounting the raw `.E01`) just because a tool/command search for create-vm failed.

## Offline fallback (last resort)

Only when the parsed case cannot answer the question **and** the user genuinely cannot or will not install "火眼仿真取证": analyze the image at the file level with `exec` and forensic CLIs (parse the filesystem read-only, carve files, read hives/configs/logs). State clearly that neither the parsed case nor emulation could answer it, and that what follows is a more limited offline analysis with its inherent limits (no runtime-only evidence).

## Answering & output

- **Answer in the conversation by default.** For most questions the user just wants the answer in chat — state it directly and cite the basis (the live command and its output) inline. Do NOT create a report file or other workspace artifacts for a simple question; generating a local report is usually unnecessary and unwanted.
- **Write files to the workspace only when the deliverable is itself a file** — e.g. the user explicitly asks for a report/export, or you carve/dump artifacts (logs, memory/process dumps, extracted files) too large to inline in chat. Put those under the workspace directory.
- The **source image stays in place, read-only** — never copied into the workspace, never modified.
- State the basis for every conclusion (which live command or which file it came from).
