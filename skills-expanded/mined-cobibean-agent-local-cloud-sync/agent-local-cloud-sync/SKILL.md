---
name: agent-local-cloud-sync
description: Keep your agent's cloud host in sync with your laptop by auto-pulling the repo when you git push. Python 3 stdlib webhook listener + user-systemd service + HMAC-SHA256. No CI, no ngrok, no pip install. Built for vibe coders and agent builders who run one bot/agent/service on one droplet and just want push-to-deploy.
version: 1.0.0
author: Jacobi Lange (@cobi_bean)
license: MIT
metadata:
  tags: [agent, deployment, github, webhook, systemd, droplet, vps, auto-deploy, vibe-coding]
---

# Agent local ↔ cloud sync

A ~100-line Python listener + a user-systemd unit. When you `git push` to your tracked branch, the host fast-forwards within seconds. No extra dependencies, no ngrok, no CI runner.

Good fit for:
- A single VPS or droplet that tracks a repo.
- Agent/bot runtimes where the workspace repo is the source of truth (e.g. a Hermes or Claude Code agent runtime, a Discord bot, a content scheduler).
- Anything where "ssh in and `git pull`" is getting tedious.

Not a fit for:
- Multi-host deploys (use a CI runner with a deploy step).
- Anything that needs a build step beyond `git pull` (add a post-pull hook, or just use CI).

## How it works

1. GitHub POSTs `push` events to `http://<host>:<port>/webhook` with an `X-Hub-Signature-256` header.
2. Listener verifies HMAC-SHA256 against a secret file. 401 on mismatch.
3. On valid push to your tracked branch: `git -C <repo> pull --ff-only origin <branch>`.
4. Everything logs to `journalctl --user -u github-webhook`.

`ping` events and pushes to other branches return 200 with "ignored" and are logged.

## Prerequisites

- A Linux host you can SSH to as a user that can run `systemctl --user`. Root is fine. Non-root works with `loginctl enable-linger <user>`.
- Python 3.8+ (stdlib only — no `pip install`).
- The repo already cloned on the host with SSH or HTTPS auth that `git pull` can use non-interactively (deploy key, SSH agent, or stored credential).
- The host must be reachable from the public internet on the port you pick (default 9000). If you're behind a firewall/NAT, this recipe won't work without a tunnel.

## Install

```bash
# 1. Pick values
HOST=your-ssh-alias              # e.g. from ~/.ssh/config
REPO_PATH=/root/DEV/my-repo      # absolute path on the host
BRANCH=main
PORT=9000

# 2. Generate the HMAC secret on the host (only place it should exist in plaintext)
ssh "$HOST" "
  mkdir -p /root/.config/github-webhook /root/bin /root/.config/systemd/user
  python3 -c 'import secrets; print(secrets.token_hex(32))' > /root/.config/github-webhook/secret
  chmod 600 /root/.config/github-webhook/secret
"

# 3. Copy the script + unit
scp github_webhook.py "$HOST":/root/bin/github_webhook.py
scp github-webhook.service "$HOST":/root/.config/systemd/user/github-webhook.service

# 4. Edit the unit's Environment= lines to match your REPO_PATH / BRANCH / PORT, then:
ssh "$HOST" "
  chmod +x /root/bin/github_webhook.py
  systemctl --user daemon-reload
  systemctl --user enable --now github-webhook.service
"

# 5. Register the webhook with GitHub
SECRET=$(ssh "$HOST" 'cat /root/.config/github-webhook/secret')
IP=$(ssh "$HOST" 'curl -s -4 ifconfig.me')
gh api -X POST /repos/OWNER/REPO/hooks \
  -f name=web -F active=true -f 'events[]=push' \
  -f "config[url]=http://$IP:$PORT/webhook" \
  -f 'config[content_type]=json' \
  -f "config[secret]=$SECRET" \
  -f 'config[insecure_ssl]=0'
```

If you're not a `gh` user, configure the webhook manually: repo → Settings → Webhooks → Add webhook. Content type `application/json`, set the secret, events = "Just the push event".

## Verify

```bash
# Listener up?
ssh "$HOST" "curl -s http://127.0.0.1:$PORT/health"       # → ok

# External reach?
curl -s -m 5 "http://$IP:$PORT/health"                    # → ok

# GitHub ping delivered on hook creation?
ssh "$HOST" 'journalctl --user -u github-webhook -n 20 --no-pager'
# → "ping received"
```

End-to-end:
```bash
git commit --allow-empty -m "test webhook" && git push
sleep 4
ssh "$HOST" "cd $REPO_PATH && git rev-parse HEAD"         # matches your laptop HEAD
```

## Day-2 ops

```bash
# Tail logs
ssh "$HOST" 'journalctl --user -u github-webhook -f'

# Restart
ssh "$HOST" 'systemctl --user restart github-webhook'

# Rotate secret
NEW=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
ssh "$HOST" "echo '$NEW' > /root/.config/github-webhook/secret && chmod 600 /root/.config/github-webhook/secret && systemctl --user restart github-webhook"
HOOK_ID=$(gh api /repos/OWNER/REPO/hooks --jq '.[] | select(.config.url | contains("/webhook")) | .id')
gh api -X PATCH "/repos/OWNER/REPO/hooks/$HOOK_ID" -f "config[secret]=$NEW"

# Redeliver a past payload (repo → Settings → Webhooks → pick hook → Recent Deliveries)
```

## Security model

- **Secret is the only gate.** The webhook URL is public. An attacker without the secret can only trigger 401s.
- **With the secret** (if it leaks), an attacker can forge push payloads and force `git pull --ff-only`. That can't inject code — `--ff-only` refuses anything except fast-forwards of what GitHub actually has — but it can be noisy. Rotate the secret if the host is compromised.
- **No TLS in this recipe.** Payloads travel over plain HTTP. The HMAC protects integrity but not confidentiality. GitHub signs the body; there's nothing sensitive in a push event beyond ref + commit SHAs that are already public on a public repo. For private repos or extra paranoia, put the listener behind a reverse proxy (Caddy / nginx) with a Let's Encrypt cert and switch to HTTPS.
- **Runs as the SSH user.** The listener runs `git pull` with the same credentials the user has. If that's root, `git pull` runs as root. Fine for a single-tenant droplet — use a dedicated user if you want to narrow blast radius.

## If the host's public IP changes

```bash
IP=$(ssh "$HOST" 'curl -s -4 ifconfig.me')
HOOK_ID=$(gh api /repos/OWNER/REPO/hooks --jq '.[] | select(.config.url | contains("/webhook")) | .id')
gh api -X PATCH "/repos/OWNER/REPO/hooks/$HOOK_ID" \
  -f "config[url]=http://$IP:$PORT/webhook" \
  -f 'config[content_type]=json'
```

For a long-lived setup, use a reserved IP or a domain.

## Uninstall

```bash
# On the host
ssh "$HOST" '
  systemctl --user disable --now github-webhook.service
  rm /root/.config/systemd/user/github-webhook.service
  rm /root/bin/github_webhook.py
  rm -rf /root/.config/github-webhook
  systemctl --user daemon-reload
'

# On GitHub
HOOK_ID=$(gh api /repos/OWNER/REPO/hooks --jq '.[] | select(.config.url | contains("/webhook")) | .id')
gh api -X DELETE "/repos/OWNER/REPO/hooks/$HOOK_ID"
```

## Gotchas

- **Zsh glob error on `gh api`:** `config[url]=...` needs single quotes — bare brackets trigger glob expansion. Error looks like "no matches found".
- **Repeated fields:** `events[]=push` uses the repeated-field form — not a JSON array.
- **`ping` vs `push`:** GitHub fires `ping` immediately on hook creation. The listener returns 200 for it. Use this to confirm delivery without a real push.
- **"Everything up-to-date":** `git push` only triggers the webhook if there's a new commit. Use `git commit --allow-empty` to force a test push.
- **UFW:** If UFW is active, `ufw allow <PORT>/tcp`. And don't forget `ufw allow 22/tcp` before enabling UFW or you lose SSH.
- **Hostname/IP in unit file:** The unit doesn't care about the public IP — only GitHub does. If the host's IP changes, update the GitHub hook, not the unit.
