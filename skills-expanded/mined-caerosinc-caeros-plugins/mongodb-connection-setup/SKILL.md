---
name: mongodb-connection-setup
description: Wire up MongoDB connections, connection string anatomy, MongoDB MCP server configuration via environment variables, read-only mode, and least-privilege database users. Use when connecting Caeros or an app to MongoDB.
---

# MongoDB Connection Setup

## Connection strings

```
mongodb+srv://USER:PASS@cluster0.abcde.mongodb.net/appdb?retryWrites=true&w=majority
mongodb://USER:PASS@localhost:27017/appdb?authSource=admin
```

- `mongodb+srv://` (Atlas) resolves hosts via DNS SRV and implies TLS.
- URL-encode special characters in passwords (`@` -> `%40`, `:` -> `%3A`).
- `authSource` must name the DB where the user was created (`admin` is common
  for self-hosted); wrong `authSource` looks like a bad password.
- Useful params: `retryWrites=true`, `w=majority`, `maxPoolSize`,
  `serverSelectionTimeoutMS=5000` (fail fast instead of hanging 30s).

Never paste a real connection string into chat, code, or version control.
Put it in the environment.

## Configure the MCP server

This plugin runs the official server via `npx -y mongodb-mcp-server@latest`.
It reads configuration from environment variables (preferred over CLI args,
which leak into process lists):

```bash
export MDB_MCP_CONNECTION_STRING="mongodb+srv://USER:PASS@YOUR-CLUSTER.mongodb.net/appdb"
# Optional, for Atlas management tools (clusters, users, access lists):
export MDB_MCP_API_CLIENT_ID="mdb_sa_id_..."      # Atlas service account
export MDB_MCP_API_CLIENT_SECRET="mdb_sa_sk_..."
```

Recommended hardening:
- **Read-only mode**: add `--readOnly` to the server args (in this plugin's
  `.mcp.json`) unless you actually want the agent to write. MongoDB's own
  guidance is read-only by default.
- **Disable tools**: `--disabledTools` accepts tool names, operation types, or
  categories (for example drop/delete tools) if you want writes but not
  destructive ones.
- There is also an interactive helper: `npx mongodb-mcp-server@latest setup`.

Restart the MCP server after changing env vars; it reads them at startup.

## Least-privilege users

Never hand an agent (or an app) the admin user. Create a scoped user:

```js
// mongosh, connected as an admin, self-hosted:
use admin
db.createUser({
  user: "caeros_ro",
  pwd: passwordPrompt(),
  roles: [ { role: "read", db: "appdb" } ]      // or readWrite@appdb
})
```

Atlas: `atlas dbusers create --username caeros_ro --role read@appdb`, or the
UI under Database Access. Built-in roles that cover 95% of cases:

| Role | Grants |
|---|---|
| `read` | find/aggregate on one DB |
| `readWrite` | plus inserts/updates/deletes |
| `dbAdmin` | index + collection admin, no data writes |
| `readAnyDatabase` | read everywhere (avoid for agents) |

Pair the read-only user with `--readOnly` for defense in depth: the flag
stops the tool surface, the role stops the server.

Atlas service accounts (for the management API) follow the same rule: scope
to one project, pick the least role (`Project Read Only` if you only need
inspection), rotate the secret on any suspected exposure.

## Triage ladder for connection failures

1. `ping` tool / `db.runCommand({ ping: 1 })`: is anything reachable?
2. Atlas: is your IP on the access list? (`atlas accessLists create --currentIp`)
3. Auth error: wrong `authSource`, unencoded password character, or user
   created on a different database.
4. SRV lookup failure: corporate DNS blocking SRV records; use the long-form
   `mongodb://host1,host2/...` string from the Atlas connect dialog.
5. Timeout with everything correct: TLS interception or an egress firewall on
   port 27017.
