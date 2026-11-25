---
name: snowflake-setup
description: "Connects Claude Code to your own Snowflake account through a read-only service user, via the managed MCP server or the snow CLI, and verifies each layer. Use when connecting for the first time, after rotating a key or token, or when a connection fails. Not for queries (use snowflake-querying)."
when_to_use: "connect to Snowflake, set up the Snowflake MCP server, snowflake connection failing, rotate a Snowflake key or token"
allowed-tools: Bash(snow connection list), Bash(snow connection test *)
disallowed-tools: Write, Edit, NotebookEdit
license: MIT
---

# Snowflake setup

Work through the steps in order. Each one has its own check, because "authentication works"
and "the role can read anything" fail with the same symptom when you test them together.

Every value in angle brackets is yours to supply; this plugin ships no account, user, role or
secret. Three rules hold throughout:

- **Admin SQL is shown, not run.** Someone with the rights runs the `CREATE` and `GRANT`
  statements in Snowsight. Present them; do not execute them through the connection.
- **Anything that prompts for input runs in the user's own terminal**: the openssl passphrase
  prompts and an interactive `snow connection add`. The Bash tool has no terminal to type into,
  and a secret typed through it would land in the transcript.
- **Secrets never pass through the chat.** Not in a message, not on a command line, not in a
  file Claude prints. Ask the user to confirm a value is set, never to paste it.

## Step 1: find the account identifier

| Form | Looks like | Notes |
| --- | --- | --- |
| Organization + account name (preferred) | `<orgname>-<account_name>` | Stable across region moves |
| Account locator (legacy) | `<locator>.<region>.<cloud>` | Some tools accept only one form |

Copy it from Snowsight's account selector (the option to copy the account identifier or URL),
or take the part of your login URL before `.snowflakecomputing.com`. Most failures at this step
are a correct credential pointed at a hostname that does not exist.

## Step 2: choose the path

| Path | Auth | Use when |
| --- | --- | --- |
| **Managed MCP server** (default) | Programmatic access token (PAT) restricted to the agent role | Your account can host a Snowflake-managed MCP server. No credential file on disk; the token sits in Claude Code's secure storage. |
| **`snow` CLI** (fallback) | Key-pair (`SNOWFLAKE_JWT`) | No managed MCP server is available, or you need CLI features. |
| `snow` CLI, interactive | SSO (`externalbrowser`) | You, at a terminal, occasionally. Needs a browser at connect time, so not for unattended work. |

Avoid password auth: it is a long-lived reusable secret. OAuth is supported by the managed MCP
server; follow Snowflake's MCP server documentation for it, as it is not covered here.

## Step 3: create the warehouse, role and service user (admin runs this)

Give the agent its own identity and its own small warehouse. A dedicated `TYPE = SERVICE` user
keeps the agent's defaults off your own login, and a role with only `USAGE` and `SELECT` turns a
misread instruction into a permissions error instead of a changed table.

```sql
USE ROLE SYSADMIN;
CREATE WAREHOUSE IF NOT EXISTS <WAREHOUSE>
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE
  STATEMENT_TIMEOUT_IN_SECONDS = 300
  STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = 120;

USE ROLE USERADMIN;
CREATE ROLE IF NOT EXISTS <AGENT_ROLE>;
CREATE USER IF NOT EXISTS <AGENT_USER>
  TYPE = SERVICE
  DEFAULT_ROLE = <AGENT_ROLE>
  DEFAULT_WAREHOUSE = <WAREHOUSE>
  DEFAULT_SECONDARY_ROLES = ();

USE ROLE SECURITYADMIN;
GRANT USAGE ON WAREHOUSE <WAREHOUSE> TO ROLE <AGENT_ROLE>;
GRANT USAGE ON DATABASE <DATABASE> TO ROLE <AGENT_ROLE>;
GRANT USAGE ON SCHEMA <DATABASE>.<SCHEMA> TO ROLE <AGENT_ROLE>;
GRANT SELECT ON ALL TABLES IN SCHEMA <DATABASE>.<SCHEMA> TO ROLE <AGENT_ROLE>;
GRANT SELECT ON ALL VIEWS IN SCHEMA <DATABASE>.<SCHEMA> TO ROLE <AGENT_ROLE>;
GRANT SELECT ON FUTURE TABLES IN SCHEMA <DATABASE>.<SCHEMA> TO ROLE <AGENT_ROLE>;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA <DATABASE>.<SCHEMA> TO ROLE <AGENT_ROLE>;
GRANT ROLE <AGENT_ROLE> TO USER <AGENT_USER>;
GRANT ROLE <AGENT_ROLE> TO ROLE SYSADMIN;

-- Session parameters set on the user apply to every session, including each separate
-- `snow sql` call and every MCP request, where ALTER SESSION would not carry over.
ALTER USER <AGENT_USER> SET
  QUERY_TAG = 'agent/<purpose>'
  STATEMENT_TIMEOUT_IN_SECONDS = 300;
```

Why each piece matters:

- **The warehouse is created first**, as SYSADMIN, because the grants name it and SECURITYADMIN
  cannot create warehouses.
- **`FUTURE` grants** keep the role working as tables and views are added. Without them a new
  object reads as "does not exist".
- **Secondary roles off.** With secondary roles active, a session can use the user's other roles
  too, which would bring back write access. `DEFAULT_SECONDARY_ROLES = ()` turns them off; the
  CLI connection below also passes `--secondary-roles NONE`. If the account rejects the empty
  list, check the current `CREATE USER` reference, then confirm with `DESC USER` either way.
- **`USAGE` on a warehouse** lets the role run queries on it but not resize it.
- **The statement timeout** is a cost ceiling per query. When the user and the warehouse both set
  one, the lower applies. A resource monitor on the warehouse adds a monthly ceiling.

## Step 4a: managed MCP server (default)

1. **Server object.** An admin creates a Snowflake-managed MCP server in a schema with a SQL
   execution tool (type `SYSTEM_EXECUTE_SQL`) and grants the agent role access to it. Take the
   exact `CREATE MCP SERVER` syntax and the privilege to grant from Snowflake's current
   "Snowflake-managed MCP server" documentation. That tool runs any SQL the caller's role
   allows, which is why Step 3's role is read-only.
2. **URL.** The endpoint has the shape
   `https://<orgname>-<account_name>.snowflakecomputing.com/api/v2/databases/<DATABASE>/schemas/<SCHEMA>/mcp-servers/<SERVER_NAME>`.
   Confirm it against the Snowflake documentation for your account.
3. **Token.** The user generates a PAT for `<AGENT_USER>` in Snowsight, restricted to
   `<AGENT_ROLE>`, with a short expiry. Snowsight shows the secret once; it goes straight into the
   plugin setting in the next step and nowhere else. Snowflake may require a network policy on the
   user before it accepts a PAT (unverified; check the PAT documentation if authentication fails).
4. **Plugin settings.** Claude Code asks for `snowflake_mcp_url` and `snowflake_pat` when the
   plugin is enabled. `snowflake_mcp_url` can be changed later in `/config`. `snowflake_pat` is a
   sensitive field and does not appear in `/config`; to replace it, disable and re-enable the
   plugin in `/plugin` to get the prompt again (unverified). Claude Code keeps the token in the
   macOS Keychain, or `~/.claude/.credentials.json` elsewhere, never in `settings.json`, and
   substitutes both values into the plugin's `.mcp.json`. Until the URL is set, `/mcp` shows
   `snowflake` as `not configured`; with a URL and a missing or wrong token, it shows a failed
   connection. Start a new session after setting them.

The server's tools appear as `mcp__plugin_snowflake-connector_snowflake__<tool>`. Copy the exact
names from `/mcp` before writing any permission rule or hook for them. For wiring questions beyond
this, see `agent-craft:mcp-integration`.

## Step 4b: `snow` CLI with key-pair (fallback)

**The user runs this in their own terminal**, because both openssl commands prompt for the key's
passphrase. `umask 077` makes the files private from the moment they are created, and the
parentheses keep it from changing the rest of that terminal session:

```bash
(
  umask 077
  mkdir -p ~/.snowflake/keys
  openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out ~/.snowflake/keys/<AGENT_USER>.p8
  openssl rsa -in ~/.snowflake/keys/<AGENT_USER>.p8 -pubout -out ~/.snowflake/keys/<AGENT_USER>.pub
)
```

The public half is safe to read. Print its body without the PEM lines, for the admin to register:

```bash
grep -v -- '-----' ~/.snowflake/keys/<AGENT_USER>.pub | tr -d '\n'
```

```sql
ALTER USER <AGENT_USER> SET RSA_PUBLIC_KEY = '<public key body>';
```

Store the passphrase in the platform keychain or a secrets manager. Before starting Claude Code,
the user exports it into `PRIVATE_KEY_PASSPHRASE` from that store; the CLI reads that variable,
so the passphrase stays out of the connection file. Any command Claude runs can read that variable
too; installing `dev-guardrails` blocks the common ways of printing it.

Then add the connection. This command prompts for nothing and carries no secret, so Claude can run
it:

```bash
snow connection add --no-interactive \
  --connection-name <name> \
  --account <orgname>-<account_name> \
  --user <AGENT_USER> \
  --authenticator SNOWFLAKE_JWT \
  --private-key-file ~/.snowflake/keys/<AGENT_USER>.p8 \
  --role <AGENT_ROLE> \
  --warehouse <WAREHOUSE> \
  --secondary-roles NONE
```

The CLI writes to `~/.snowflake/connections.toml` if that file exists, otherwise to the
`[connections]` section of `~/.snowflake/config.toml`. It creates the file with mode 0600 and
refuses one that other users can read. Leave the passwords out of that file, keep it out of any
repository, and read connections back with `snow connection list`, which masks secret values,
rather than printing the file.

To rotate the key without downtime, register the new key as `RSA_PUBLIC_KEY_2`, switch the
connection over, verify, then unset the old one.

## Step 5: verify, one layer at a time

Stop at the first failure; each check isolates a different layer.

1. **Transport and auth.** MCP: `/mcp` (or `claude mcp list`) shows `snowflake` connected.
   CLI: `snow connection test --connection <name>`.
2. **Identity.** Run
   `SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_SECONDARY_ROLES(), CURRENT_WAREHOUSE();`
   through the MCP SQL tool or `snow sql --connection <name> -q "…"`. Expect `<AGENT_USER>`,
   `<AGENT_ROLE>`, no secondary roles, and `<WAREHOUSE>`.
3. **Privileges.** `SHOW GRANTS TO ROLE <AGENT_ROLE>;` lists only `USAGE` and `SELECT`.
4. **Metadata.** `SHOW TABLES IN SCHEMA <DATABASE>.<SCHEMA>;` lists the tables you expect.
5. **A bounded read.** `SELECT <one_column> FROM <DATABASE>.<SCHEMA>.<TABLE> LIMIT 10;`
6. **Key fingerprint** (CLI path, if auth failed). Compare the output of
   `openssl rsa -pubin -in ~/.snowflake/keys/<AGENT_USER>.pub -outform DER | openssl dgst -sha256 -binary | openssl enc -base64`
   with `RSA_PUBLIC_KEY_FP` from `DESC USER <AGENT_USER>;`.

If step 2 shows an unexpected role or any secondary role, fix the user defaults before going on.
Symptom-by-symptom fixes are in [references/troubleshooting.md](references/troubleshooting.md).
Once connected, use `snowflake-querying` for anything beyond these checks.

## Examples

<example>
User pastes a string starting with the PAT prefix and says "here's the token, set it up."
Claude does not repeat or use it: "That token is now in this conversation, so treat it as
exposed. Revoke it in Snowsight, generate a new one, and enter the new one only in the plugin's
settings prompt (disable and re-enable the plugin in `/plugin` to get the prompt back). Tell me
when it is set and I'll check `/mcp`."
</example>

<example>
Step 5.1 passes (`snow connection test` succeeds), but step 2 returns `CURRENT_ROLE()` =
`PUBLIC`. Claude stops there rather than testing grants: the service user's `DEFAULT_ROLE` is
not `<AGENT_ROLE>`, or the role was never granted to it. It shows the admin
`GRANT ROLE <AGENT_ROLE> TO USER <AGENT_USER>;` and
`ALTER USER <AGENT_USER> SET DEFAULT_ROLE = <AGENT_ROLE>;`, then reruns step 2.
</example>

## Without a checkout or shell

On the web, or when Claude has no shell, give the user the steps and the SQL to run in Snowsight
and their own terminal, then work from the output they paste back. Whether Cowork prompts for a
plugin's settings is not documented; there, the user can add the same MCP server URL as a
claude.ai custom connector instead.
