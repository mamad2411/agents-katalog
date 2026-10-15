---
name: liaison-entry
version: 0.1.0
description: "Liaison Cloud entries (a.k.a. proxies): create, list, update, enable/disable, delete the public-facing endpoints that expose a connector's applications to the internet. An entry binds an application to a public port (TCP) or domain (HTTP). Use this skill for intents like 'expose my app via a public URL', 'open port 8080 to the world', 'list my entries', 'take entry 10 offline'. Always read ../liaison-shared/SKILL.md first."
metadata:
  requires:
    bins: ["liaison"]
  cliHelp: "liaison proxy --help"
---

# liaison-entry

**CRITICAL — read [`../liaison-shared/SKILL.md`](../liaison-shared/SKILL.md) first.**

## Concept

An **entry** (internally also called "proxy") is a public-facing endpoint that routes traffic to one **application** behind a connector.

```
internet  →  liaison.cloud:<port>  →  Liaison Cloud routing  →  connector  →  application IP:port
   or
internet  →  https://<domain>/     →  Liaison Cloud routing  →  connector  →  application IP:port
```

Entries come in two flavours, decided by the application's `protocol`:

| Protocol | Public exposure | Configured via |
|----------|-----------------|----------------|
| `http` | Public HTTPS URL like `https://<label>-<user>.liaison.cloud` | `--domain-label` (auto-derived from `--name` if omitted) |
| `tcp` / `ssh` / `mysql` / `postgresql` / `redis` / `mongodb` / `rdp` | Public TCP port like `liaison.cloud:34567` | `--port` (or omit for auto-allocate) |

An entry has its own `status`:
- `running` — actively accepting traffic
- `stopped` — taken offline without deleting

## Access model (IMPORTANT — set user expectations)

Who can reach an entry **depends on protocol**, and this catches agents out:

| Protocol | Default access | To let other people in |
|---|---|---|
| `http` / https entries | **Owner-only**: anonymous visitors are 302-redirected to `liaison.cloud/dashboard/login`. Only the token owner sees the site after logging in. | `liaison proxy share <id>` → temporary share URL (see below) |
| `tcp` / `ssh` / `mysql` / `postgresql` / `redis` / `mongodb` / `rdp` | **Open to anyone** who can reach `liaison.cloud:<port>` (protect with app-level auth, e.g. SSH keys, DB passwords) | No share flow needed — just hand over host+port |

**There is currently no "permanent public" toggle for HTTP entries.** Do not tell the user "your site is live on the internet" without qualifying — say "live at `<url>` (you'll be asked to log in to liaison.cloud the first time)" for HTTP, or just "live at `liaison.cloud:<port>`" for TCP-like.

### Temporary share links (HTTP entries)

`liaison proxy share <id>` mints a short-lived share URL that bypasses the login gate for whoever opens it:

```bash
liaison proxy share 100057
# => {
#      "share_url":  "https://foo-user.liaison.cloud/s/SotmL3rsRhu9zyEGlyAW",
#      "access_url": "https://foo-user.liaison.cloud",
#      "expires_at": "2026-04-18 10:38:18"
#    }

# Send the guest to a specific path
liaison proxy share 100057 --redirect /admin

# Just grab the URL
liaison proxy share 100057 | jq -r .share_url
```

Rules:
- The `share_url` lives on the entry's **own hostname** (`<label>-<user>.liaison.cloud/s/<code>`), not on `liaison.cloud/s/...`. The `/s/<code>` endpoint seeds a Set-Cookie and 302s to the entry root.
- **Guests must follow the redirect with cookies enabled** — browsers do this automatically; `curl` needs `-L -c cookies.txt -b cookies.txt`.
- The link **expires server-side** (default ~1 hour from creation). There's no "revoke one link" — wait for expiry or rotate by minting a new one.
- Each open of `/s/<code>` seeds a cookie scoped to that one entry only — share URLs can't escalate to other entries.
- Minting a share requires you (the CLI owner) to already have access. You can't share entries you don't own.
- Only meaningful for `http` entries. TCP-style entries have no auth gate to bypass.

## Commands

All commands under `liaison proxy`. Aliases: `proxies`, `entry`, `entries`. (The CLI uses "proxy" internally for historical reasons; the user-facing dashboard says "entry".)

### List

```bash
liaison proxy list                      # all entries
liaison proxy list --name my-app        # name substring filter
liaison proxy list --page 2             # pagination
liaison proxy list -o table             # human-readable
```

**Response shape**:
```json
{
  "total": 2,
  "proxies": [
    {
      "id": 10,
      "name": "my-web",
      "protocol": "http",
      "domain": "myapp.example.com",
      "port": 0,
      "status": "running",
      "application_id": 5,
      "edge_id": 100017,
      "created_at": "..."
    }
  ]
}
```

### Get

```bash
liaison proxy get 10
```

### Create

`--name` and `--application-id` are required. Other flags depend on the protocol:

```bash
# HTTP entry → default label from --name (result: my-web-<user>.liaison.cloud)
liaison proxy create \
  --name my-web \
  --protocol http \
  --application-id 5

# HTTP entry → pick an explicit subdomain label
liaison proxy create \
  --name my-web \
  --protocol http \
  --domain-label marketing-site \
  --application-id 5

# TCP-style entry → expose on a server-allocated public port
liaison proxy create \
  --name my-ssh \
  --protocol ssh \
  --application-id 6
# server picks an available port and returns it in the response

# TCP-style entry → ask for a specific port
liaison proxy create \
  --name my-mysql \
  --protocol mysql \
  --port 13306 \
  --application-id 7
```

**Picking `--port`:**
- Leave it `0` (the default) for `tcp`-like protocols → server auto-allocates an available port
- Set a specific port only when the user asks for one (e.g. they have a firewall rule pinned to a port)
- For `http`, `--port` is ignored — use `--domain-label` instead

**Picking `--domain-label`:**
- Required server-side for `http` protocol. The CLI auto-derives it from `--name` when omitted, so most calls don't need it.
- It's the **short subdomain label** (e.g. `myapp`) — the server composes the full hostname as `<label>-<user>.liaison.cloud`.
- Passing a full FQDN here will be rejected; use `--domain` for a custom FQDN on top of the label.

**Picking `--domain` (optional BYO domain):**
- Only when the user owns a custom domain with DNS pointing at liaison.cloud's edge nodes.
- Without DNS the entry exists in the DB but no traffic reaches it.

### Update

Only pass the fields you want to change. Most useful for taking entries on/off:

```bash
liaison proxy update 10 --status stopped       # take offline
liaison proxy update 10 --status running       # bring back
liaison proxy update 10 --port 14000           # change auto-allocated port
liaison proxy update 10 --description "new"    # rename / re-describe
```

`--status` accepts the literal strings `running` and `stopped` (NOT integers — different from connector update which takes numbers/keywords).

### Share (HTTP entries only)

Mint a temporary share URL for an HTTP entry so a guest can view it without logging in. See **Access model** above for the full story.

```bash
liaison proxy share 100057                      # default JSON
liaison proxy share 100057 --redirect /admin    # guest lands on /admin after redirect
liaison proxy share 100057 | jq -r .share_url   # extract the URL for scripting
```

Response fields:
- `share_url` — the `/s/<code>` URL to send the guest (this is what you share)
- `access_url` — the entry's own URL (only useful for the owner post-bootstrap)
- `expires_at` — RFC3339 timestamp; after this the link 410's with "share link expired"

### Delete

**Requires `--yes`.**

```bash
liaison proxy delete 10 --yes
```

The associated application is left alone; only the public exposure is removed.

## Intent → command mapping

| User says | Command |
|-----------|---------|
| "Expose my web app" | First find the application id with `liaison application list`, then `liaison proxy create --name web --protocol http --application-id <id>` (label defaults to `web`). For a custom label: add `--domain-label marketing`. For a BYO domain with DNS already pointed: add `--domain example.com`. |
| "Open SSH access to my home server" | `liaison proxy create --name ssh --protocol ssh --application-id <id>` (port auto-allocated) |
| "What's my SSH port?" | `liaison proxy list -o table` then read the `PORT` column for the ssh entry |
| "Take entry 10 offline temporarily" | `liaison proxy update 10 --status stopped` |
| "Bring entry 10 back" | `liaison proxy update 10 --status running` |
| "Remove the public exposure for X" | `liaison proxy delete <id> --yes` (the application stays) |
| "Send this HTTP site to a friend" / "give someone temporary access" | `liaison proxy share <id>` — hand them `share_url` (~1h validity). Only meaningful for `http` entries. |
| "Is my site public?" | For `http`: **no** — it requires liaison.cloud login by default. Use `proxy share` for a temp link, or tell the user to log in themselves. For `tcp`/`ssh`/etc.: yes, anyone who can reach `liaison.cloud:<port>` can connect. |

## Common mistakes to avoid

- **Creating an entry without an application first.** Applications and entries are separate resources. If `liaison application list --edge-id <connector>` returns nothing, you need to `liaison application create ...` BEFORE creating the entry.
- **Setting `--port` for an `http` entry.** HTTP routes by hostname (label+domain), not port; `--port` is silently ignored. Use `--domain-label` instead.
- **Passing a full FQDN to `--domain-label`.** That field is the short label (e.g. `myapp`), not a hostname. Putting `myapp.liaison.cloud` here will be rejected. Use `--domain` for FQDNs.
- **Omitting the domain label entirely on http.** The server returns `DOMAIN_LABEL_REQUIRED (400)`. The CLI now auto-derives from `--name`, but if you override body manually make sure `domain_label` is set.
- **Confusing entry status with connector status.** They're independent. Stopping an entry takes ONE service offline; stopping a connector takes ALL services on that host offline.
- **Reusing `--port`.** Two entries can't bind the same public port. The server returns a clear error if you try.
- **Sharing the `--domain`** of a domain you don't actually control. The DNS still has to point at Liaison's edge nodes — otherwise the entry exists in the database but no real traffic ever reaches it.
