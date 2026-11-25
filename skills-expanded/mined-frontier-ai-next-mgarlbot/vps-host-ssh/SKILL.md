---
name: vps_host_ssh
description: Run commands on the VPS host OS via preconfigured SSH from the mgarlbot container
triggers: [vps, ssh, host, remote server, install, apt, package, debian, ubuntu, systemd, root@, хост, на сервере, установи, apt, удалённ]
tools: [shell]
platform: all
---

## VPS host — always via `ssh`, never “bare” `apt` inside the bot container

When the user asks to **install a package on the VPS**, **run a command on the server**, **apt on the host**, etc. — **do not ask** for IP, login, or distro unless they volunteered it. Assume access is already wired.

### Fixed wrapper

Use **one `shell` invocation**:

```bash
ssh -F /data/.ssh/config vps 'REMOTE_COMMAND_HERE'
```

- Host alias **`vps`**, config **`/data/.ssh/config`**, keys and **`UserKnownHostsFile`** live on the mounted `/data` volume (on the host: mgarlbot data dir).

**Non-interactive apt** on Debian/Ubuntu:

```bash
ssh -F /data/.ssh/config vps 'DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y PACKAGE_NAME'
```

After install, verify: `ssh -F /data/.ssh/config vps 'command -v NAME || NAME --version'`.

### Do not confuse with the container

- `apt install` **without** `ssh ... vps` installs into the **container** (often fails without root). For the **host**, always prefix **`ssh -F /data/.ssh/config vps '...'`**.
- `docker` / `docker compose` against the **host daemon** — use the compose/socket setup on that machine, **not** this SSH wrapper, unless the user asked for OS-level edits on the host.

### Rules

- Never paste private keys or secret material from `~/.ssh`.
- Do not suggest destructive host commands (`rm -rf /`, disk wipe, etc.).
