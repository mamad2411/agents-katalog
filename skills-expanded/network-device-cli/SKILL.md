---
name: network-device-cli
description: "Use when SSHing into a router, switch, or firewall CLI."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ssh, cisco, ios, network, legacy-crypto, cli]
---

# Network Device CLI (Cisco IOS and other appliances)

## When to Use

- The user gives a host + credentials and asks for a command (ping, show) to be
  run **on** the device — router, switch, firewall, appliance.
- An SSH attempt to network gear fails with `Permission denied` or
  `no acceptable kex algorithm`.
- You need device-side reachability (can the router reach 8.8.8.8?) rather than
  host-side.
- A request wants device config **changed** (interface, VLAN, route, ACL), not
  just read — see "Before a config change" below.
- You are rebuilding a device-inventory / automation workflow that must survive
  session resets — the inventory (hostname, ip, port, credentials, config_list,
  checkpoint) belongs on disk, never in the conversation.

Not for a Linux server over SSH — plain `ssh user@host` works there.

Network gear is not a Linux box. It runs an exec-mode CLI with paging, restricted
exec commands, and — on anything a few years old — SSH algorithms that modern
OpenSSH disables by default. Follow this order; each step fails in a way that
misdiagnoses as "wrong password" if you skip it.

## 1. Confirm reachability, then read the banner

```bash
ping -c1 -W2 <host>
ssh -v -o ConnectTimeout=10 -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null <user>@<host> exit 2>&1 \
  | grep -iE "remote software|kex: algorithm|Authentications that can continue"
```

`remote software version Cisco-1.25` plus `kex: algorithm: (no match)` means
legacy crypto, NOT bad credentials. Solve the crypto before you touch the
password — otherwise every auth attempt reports `Permission denied` and you burn
time guessing passwords that were right all along.

## 2. Force legacy algorithms per connection

Modern OpenSSH still *ships* these algorithms; it only stops offering them. So
the fix is flags on the invocation, not an install and not a config edit:

```
-o KexAlgorithms=+diffie-hellman-group14-sha1,diffie-hellman-group1-sha1,diffie-hellman-group-exchange-sha1 \
-o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa \
-o Ciphers=+aes128-cbc,3des-cbc -o MACs=+hmac-sha1 \
-o PreferredAuthentications=password -o NumberOfPasswordPrompts=1
```

Do **not** edit `/etc/ssh/ssh_config.d/*.conf` for this: it needs root, and it
weakens every future SSH connection instead of one. Keep the legacy flags inside
the invocation (or a `Host` block in `~/.ssh/config` scoped to that IP).

## 3. Password auth without sshpass/expect

`sshpass` is usually absent and installing it needs root. OpenSSH's own askpass
hook works fine and keeps the password out of `argv` and out of logs:

```bash
cat > /tmp/askpass.sh <<'EOF'
#!/bin/bash
printf '%s\n' "$SSH_PROBE_PW"
EOF
chmod +x /tmp/askpass.sh

SSH_PROBE_PW="$PW" SSH_ASKPASS=/tmp/askpass.sh SSH_ASKPASS_REQUIRE=force DISPLAY=:0 \
  ssh -tt <legacy flags> <user>@<host> '<command>'
```

`SSH_ASKPASS_REQUIRE=force` is what makes it work without `setsid`. Do not put
the password inline in the script or on the ssh command line.

## 4. Issue commands the way the device accepts them

- **One command per connection** on IOS. A single string with IOS arguments
  (`ping 8.8.8.8 repeat 5 timeout 2`) is rejected as
  `Line has invalid autocommand "…"` — exec mode takes the bare form only
  (`ping 8.8.8.8`, default 5 packets). For arguments, drive an interactive
  session instead of exec mode.
- **Hold the channel open.** With `< /dev/null` the session closes the moment
  auth completes and you get a truncated reply (a lone `!` from a 5-packet
  ping). Pipe a sleep into it instead:
  ```bash
  { sleep 25; } | ssh -tt <flags> <user>@<host> 'ping 8.8.8.8' 2>&1 | tr -d '\r'
  ```
- **`-tt`** allocates the PTY the CLI expects; without it IOS output arrives
  mangled or not at all. `tr -d '\r'` afterwards makes the output readable.
- **Paging:** `terminal length 0` as an exec command can drop the session.
  Prefer reading short `show` output, or set paging inside an interactive
  session only.

## 5. Report the device's own verdict

Quote the summary line verbatim — `Success rate is 100 percent (5/5),
round-trip min/avg/max = 8/36/91 ms`, `%SYS-5-CONFIG_I`, `state: up`. Do not
paraphrase into your own numbers, and do not claim success without the device's
line in the output.

## 6. Before a config change: plan, approval, checkpoint

Reading is cheap; writing is not. For anything that changes state:

1. Read first. Pull the running config and the relevant `show` output before
   proposing a diff — never configure from memory of what the device "should"
   look like.
2. Present the plan before touching the device, and stop there. Five blocks,
   in this order: (a) what changes and why, in one short reason; (b) the exact
   command list, verbatim; (c) the exact rollback command list; (d) the read-only
   command that will verify it afterwards plus the output/state you expect;
   (e) risk — which lines can cut you off, and why they do not here. A
   confirmation that has not seen all five is not approval. This applies even
   when the user asked for the change in the same message, and even for one line.
   If any line changes after approval, the old approval is void: re-present,
   re-ask.
3. Save the pre-change running config to a file, and write the rollback script
   before applying. `references/config-change-safety.md` has the checkpoint →
   apply → save → verify → rollback loop and the per-vendor command profiles.
   Where the `network-change-management` skill is installed, run its rollback
   generator: `rollback_gen <script> --existing-config <saved-config>` drafts
   the rollback — read it line by line and fill its
   `# TODO restore from snapshot:` entries before use.
4. Never send a command that can cut your own path back in: VTY/management
   interface, `access-class`, default route, the interface you are connected
   through.
5. Verify with the command promised in (d) once the change lands, and quote the
   device's own output line. The device echoing the config line is not
   verification; reading the resulting state back is.

A change is not "done" because the device echoed the line. Re-read the running
config and check the lines are actually present; a capture that shows no error is
weaker evidence than a captured config containing the line.

## 7. Persistent interactive session (OpenSSH)

One-shot OpenSSH suits a single `show`. For a session that enters `enable` with a
secret and then runs a dozen commands, hold one PTY open instead of spawning an
ssh per command — the engine's own technique, no paramiko, no Python:

```bash
SSH_ASKPASS=/tmp/askpass SSH_ASKPASS_REQUIRE=force setsid \
  ssh -tt -o KexAlgorithms=+diffie-hellman-group14-sha1 \
      -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa \
      -o Ciphers=+aes128-cbc -o MACs=+hmac-sha1 admin@10.0.0.5 < plan
```

- `SSH_ASKPASS` + `setsid` (no controlling tty) supplies the password without
  sshpass; `SSH_ASKPASS_REQUIRE=force` needs OpenSSH 8.4+.
- `-tt` forces the PTY so the device prints prompts; feed a paced plan of
  `delay<TAB>command` pairs on stdin — pause after connect, then one line at a
  time. Pacing replaces read-until-idle: gear that pauses mid-output otherwise
  gets the next command typed into the middle of the previous one.
- On a piped PTY the prompt is never a standalone line: the device prints it and
  the next command lands on the same line (`R2>show clock`). Parse prompts as a
  line *prefix* (`^[A-Za-z0-9_.-]{1,63}[>#]`), not a line suffix.
- Disable paging first (`terminal length 0`); a stray `--More--` cannot be
  answered from a pipe.
- `enable`: send `enable`, pause, send the secret, then confirm the prompt ends
  in `#`. Report the prompt you actually saw rather than assuming the enable
  succeeded.
- Keep the password out of `argv` — the askpass helper reads it from the
  environment.

`scripts/ios_session.sh` is this session shape as a runnable CLI (same flags as
the old paramiko version: `--host --user --password --secret --cmd --show-config
--paging`).

## Credential parsing pitfall

Credentials arrive as run-together prose: `user admin pass S3cr3t! secret en4ble!` is
user `admin`, **password `S3cr3t!`**, and `en4ble!` is the *enable secret* (privileged
exec password) — not a passphrase with spaces. Try the whole string, then the
single token, and report which one authenticated rather than silently using it.
A Cisco banner plus a rejected multi-word password is the signal that you split
the string wrong.

## Supporting files

- `scripts/legacy-ssh.sh` — wraps the flags, askpass, and hold-open stdin so a
  one-shot command works first try.
- `scripts/ios_session.sh` — persistent OpenSSH PTY session (enable, paging off,
  read running config) as a runnable CLI.
- `references/config-change-safety.md` — checkpoint → apply → save → verify →
  rollback loop, rollback-script rules, and per-vendor command profiles.
