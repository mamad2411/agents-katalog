---
name: postgres-read
description: Set up or repair the read-only access of the postgres MCP server to the local test database. Use when the postgres MCP server fails to connect, or after the test container was recreated.
---

The `postgres` MCP server of this plugin targets `127.0.0.1:$ION_REPO_PG_PORT`, database
`$ION_REPO_PG_DATABASE`, with a read-only role; `scripts/pg-env.sh` of the plugin derives every value
from the repo settings (`PROJET_*` names before kiln 0.4). Repo settings:
!`env | grep -E '^(KILN|PROJET)_(PROJECT|NOM|PG_)' | sort`

1. Is the test container running? (`podman ps`) Otherwise `podman start` it.
2. Create or repair the role: `bash "${CLAUDE_SKILL_DIR}/role.sh"`. It only has
   `pg_read_all_data` and `pg_monitor`: read-only comes from its rights, not from the tool.
3. Reload the MCP server (`/mcp`) and check with a simple query.
