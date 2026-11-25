---
name: codex-autodl-remote
description: Set up AutoDL and similar temporary rented SSH/GPU servers as Codex remote projects from a local Mac. Use when the user needs Codex App or Codex CLI to work on files on an SSH server whose host, port, or path may change; when configuring ~/.ssh/config aliases, password-to-key login, reverse SOCKS proxy through a local VPN, remote Codex install/auth, copying local ~/.codex/auth.json to the server, or troubleshooting Codex SSH remote connection failures.
---

# Codex AutoDL Remote

Use this workflow to turn a temporary SSH server into a stable Codex remote project while keeping a fixed local alias such as `codex-gpu`.

Never paste or store SSH passwords, private keys, or `~/.codex/auth.json` contents in chat or config files. Copy files directly between the user's machines.

## Workflow

1. **Normalize the SSH host**
   - Use one stable alias, usually `codex-gpu`, even when the rented server host or port changes.
   - If given a raw command like `ssh -p 56590 root@connect.example.com`, use `scripts/update_ssh_config.py` to update `~/.ssh/config`:

```bash
python scripts/update_ssh_config.py --ssh "ssh -p 56590 root@connect.example.com" --alias codex-gpu
```

   - Add `--identity ~/.ssh/codex_gpu_ed25519` after key login is configured.
   - Confirm parsing without writing by adding `--dry-run`.

2. **Make SSH non-interactive for Codex App**
   - Codex App cannot reliably type SSH passwords in the background. Convert password login to key login:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/codex_gpu_ed25519 -C "codex-gpu" -N ""
ssh codex-gpu 'mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys' < ~/.ssh/codex_gpu_ed25519.pub
python scripts/update_ssh_config.py --ssh "ssh -p PORT USER@HOST" --alias codex-gpu --identity ~/.ssh/codex_gpu_ed25519
ssh -o BatchMode=yes codex-gpu 'echo ok'
```

   - If `BatchMode=yes` does not print `ok`, fix SSH before trying Codex App.

3. **Route remote network through the local Mac when needed**
   - If the server cannot access OpenAI/ChatGPT directly but the Mac can through a VPN such as QuickQ, use OpenSSH reverse dynamic forwarding from the Mac:

```bash
ssh -N -R 127.0.0.1:7891 codex-gpu
```

   - Keep that local terminal open. For a more resilient local tunnel:

```bash
while true; do ssh -N -R 127.0.0.1:7891 codex-gpu; sleep 3; done
```

   - In a separate SSH session on the server, export proxy variables:

```bash
export ALL_PROXY=socks5h://127.0.0.1:7891
export HTTP_PROXY=socks5h://127.0.0.1:7891
export HTTPS_PROXY=socks5h://127.0.0.1:7891
export all_proxy=socks5h://127.0.0.1:7891
export http_proxy=socks5h://127.0.0.1:7891
export https_proxy=socks5h://127.0.0.1:7891
```

   - Persist these exports in the remote `~/.bashrc`. If Codex App still starts without them, also put them in the remote `~/.profile` or `~/.bash_profile`.
   - Test network from the server:

```bash
curl -I https://api.openai.com
curl -I https://chatgpt.com/backend-api/ps/mcp
```

   - `HTTP/2 421`, `401`, `403`, `404`, or `405` means the host is reachable. `451` means the current VPN exit may be region-blocked for that endpoint; switch VPN nodes if Codex App remote fails.

4. **Install Codex on the server**
   - With proxy exports active, prefer the official installer:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
codex --version
```

   - If npm-managed Codex already exists, allow the installer to remove it when prompted.
   - If `codex` is not found in the current shell, run `export PATH="$HOME/.local/bin:$PATH"` and ensure the installer added that path to the remote shell startup file.

5. **Copy local Codex auth before remote login**
   - If the user already has a working local Codex login, copy the local auth file to the remote server before launching remote Codex:

```bash
ssh codex-gpu 'mkdir -p ~/.codex && chmod 700 ~/.codex'
scp ~/.codex/auth.json codex-gpu:~/.codex/auth.json
ssh codex-gpu 'chmod 600 ~/.codex/auth.json'
```

   - This avoids browser login friction on restricted remote networks. It is sensitive credential material; do not display its contents.
   - If remote Codex later fails at `https://auth.openai.com/oauth/token`, first test the network path:

```bash
curl -I --socks5-hostname 127.0.0.1:7891 https://auth.openai.com/oauth/token
```

   - `405`, `400`, `401`, or `403` means the auth host is reachable. If Codex still fails after that, treat the remote `~/.codex/auth.json` as expired or stale and copy the local file again.
   - Then verify:

```bash
ssh codex-gpu 'export PATH="$HOME/.local/bin:$PATH"; codex --version'
ssh codex-gpu 'export PATH="$HOME/.local/bin:$PATH"; codex'
```

6. **Create a stable remote project path**
   - For changing real project paths, keep a fixed symlink:

```bash
ssh codex-gpu 'mkdir -p ~/codex && ln -sfn /real/project/path ~/codex/current'
```

   - Use `~/codex/current` in Codex App. For a blank workspace, create it as a directory instead:

```bash
ssh codex-gpu 'mkdir -p ~/codex/current'
```

7. **Add the Codex App remote project**
   - In local Codex App, go to `Settings > Connections > SSH`.
   - Enable or add `codex-gpu`.
   - Choose the remote folder, for example `/root/codex/current` or `/root`.
   - Open a new remote thread and test: ask Codex to list the current directory and identify the machine.

## Rotation Checklist

When the rented server changes:

- Update `HostName` and `Port` for the same `Host codex-gpu`.
- Reinstall or verify the public key in `~/.ssh/authorized_keys`.
- Restart the local reverse SOCKS tunnel.
- Reinstall or verify remote `codex`.
- Copy `~/.codex/auth.json` again if the server is new.
- Recreate `~/codex/current`.
- Test `ssh -o BatchMode=yes codex-gpu 'echo ok'`.

## Troubleshooting

- **Codex App shows SSH connection failed**: Password login is not enough. Make `ssh -o BatchMode=yes codex-gpu 'echo ok'` pass.
- **`codex: command not found`**: Add `export PATH="$HOME/.local/bin:$PATH"` to the remote shell startup file and test a new SSH session.
- **Installer returns 503 or network errors**: Ensure the local reverse tunnel is running and proxy variables are exported on the server.
- **Codex fails at `auth.openai.com/oauth/token`**: Run `curl -I --socks5-hostname 127.0.0.1:7891 https://auth.openai.com/oauth/token`. If it returns `405`, the network is fine and the remote auth is probably expired; re-copy local `~/.codex/auth.json` to `codex-gpu:~/.codex/auth.json` and `chmod 600` it.
- **`codex_apps` MCP startup fails but CLI answers**: Treat it as an integration warning first. If App remote fails, test `https://chatgpt.com/backend-api/ps/mcp`; switch VPN exit nodes if it returns `451`.
- **`connect_to 127.0.0.1 port 7890 failed`**: That was fixed-port forwarding to a missing local proxy. Use reverse dynamic forwarding: `ssh -N -R 127.0.0.1:7891 codex-gpu`.
- **Long-running jobs**: Use `screen`, `tmux`, or the provider's daemon guidance on the remote server for training/jobs. The reverse SSH proxy tunnel itself must stay running on the local Mac because it borrows the Mac VPN exit.
