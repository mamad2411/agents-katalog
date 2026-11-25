---
name: liaison-application
version: 0.1.0
description: "Liaison Cloud applications: register, list, update, delete the IP+port backend services that sit behind a connector. An application is just metadata — it points at an existing TCP/HTTP service on the connector's host network so an entry can route traffic to it. Use this skill for intents like 'register my SSH server with connector X', 'list applications behind connector 100017', 'change application 5's port'. Always read ../liaison-shared/SKILL.md first."
metadata:
  requires:
    bins: ["liaison"]
  cliHelp: "liaison application --help"
---

# liaison-application

**CRITICAL — read [`../liaison-shared/SKILL.md`](../liaison-shared/SKILL.md) first.**

## Concept

An **application** is the description of a backend TCP/HTTP service reachable from a connector. It is purely metadata — you are NOT installing anything; you are telling Liaison "this connector can reach an SSH service at 127.0.0.1:22; here's a name for it".

Required fields when creating one:
- `name` — human label
- `protocol` — what kind of traffic it speaks (one of: `tcp`, `http`, `ssh`, `rdp`, `mysql`, `postgresql`, `redis`, `mongodb`)
- `ip` — backend address as seen from the connector's host (commonly `127.0.0.1` or a private LAN address)
- `port` — backend port number
- `edge_id` — the connector this app sits behind

Once an application exists, the user typically creates an **entry** (see `liaison-entry`) to expose it publicly.

## Commands

All commands under `liaison application`. Aliases: `app`, `applications`, `apps`.

### List

```bash
liaison application list                       # all apps
liaison application list --edge-id 100017      # only apps behind connector 100017
liaison application list --name redis          # name substring filter
liaison application list -o table              # human-readable
```

**Response shape**:
```json
{
  "total": 4,
  "applications": [
    {
      "id": 5,
      "name": "ssh",
      "protocol": "ssh",
      "ip": "127.0.0.1",
      "port": 22,
      "edge_id": 100017,
      "created_at": "2026-04-12 10:00:00"
    }
  ]
}
```

### Get

```bash
liaison application get 5
```

### Create

ALL of `--name`, `--ip`, `--port`, `--edge-id` are required. `--protocol` defaults to `tcp` but you should set it explicitly when known.

```bash
liaison application create \
  --name my-ssh \
  --protocol ssh \
  --ip 127.0.0.1 \
  --port 22 \
  --edge-id 100017
```

**Picking the right `--ip`:**
- For services running on the connector's own host: `127.0.0.1`
- For services on the connector's LAN (NAS, router, another VM): the LAN address (e.g. `192.168.1.50`)
- For services on the public internet from the connector's perspective: the public IP (rare — usually defeats the purpose of having a connector)

**Picking the right `--protocol`:**
- `http` → if the entry will be a public HTTP/S URL
- `tcp` → if you want a public raw TCP port (works for any TCP-based service)
- `ssh`/`mysql`/`postgresql`/`redis`/`mongodb`/`rdp` → use these only if you want the dashboard UI to show protocol-aware connection helpers; they all behave like `tcp` on the wire

### Update

Only pass the fields you want to change.

```bash
liaison application update 5 --port 2222
liaison application update 5 --ip 192.168.1.10 --name my-ssh-renamed
```

### Delete

**Requires `--yes`.** Note that any entries pointing at this application will become orphaned — delete or update those first if you care.

```bash
liaison application delete 5 --yes
```

## Intent → command mapping

| User says | Command |
|-----------|---------|
| "Register the local SSH server with connector 100017" | `liaison application create --name ssh --protocol ssh --ip 127.0.0.1 --port 22 --edge-id 100017` |
| "What apps are behind my connector?" | `liaison application list --edge-id <id> -o table` |
| "Move app 5 to port 2222" | `liaison application update 5 --port 2222` |
| "Delete the redis backend" | `liaison application list --name redis` → confirm id → `liaison application delete <id> --yes` |

## Common mistakes to avoid

- **Forgetting `--edge-id`**. The CLI requires it; the API can't create an app that doesn't belong to a connector.
- **Using `localhost` instead of `127.0.0.1`**. The connector resolves these on its host — `localhost` may resolve to IPv6 `::1` and break IPv4-only services. Use `127.0.0.1` unless you know the service binds IPv6.
- **Pointing at the WRONG host**. The IP is from the **connector's** point of view, not from the cloud or your laptop.
- **Creating an application but no entry**. The application alone is not reachable — it just exists as metadata. The user must also create an entry (see `liaison-entry`) to expose it.
