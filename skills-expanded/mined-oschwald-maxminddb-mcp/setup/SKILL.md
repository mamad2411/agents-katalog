---
name: setup
description: Check the MaxMindDB plugin connection and database configuration after installation, or troubleshoot missing databases and failed startup.
---

# Set up MaxMindDB

Use the MaxMindDB MCP tools for these checks. The server runs locally as a bundled
executable or a Docker container, depending on the package.

1. Call `list_databases`. If the tools are unavailable, check that the plugin is
   enabled in a local thread and that its OS and architecture match the computer.
   Use the client-specific setup instructions below. Docker-backed plugins need
   a running Docker engine.
   After correcting configuration, restart the server and use a new conversation.
2. Read `status`, `message`, and `update` from the result. If downloading, explain
   that tools are connected but databases are not ready. Check again when the
   user asks or after other setup work. Do not repeatedly poll or trigger another
   download. For an empty or error result, report the corrective action given by
   the server. An available database can still be tested if an update failed.
3. When a database is available, call `lookup_ip` for `8.8.8.8`, passing its exact
   filename as `database`. Prefer a GeoIP2 or GeoLite2 City, Country, or ASN
   database. If `found` is false, report that the lookup worked but this database
   has no matching record. Do not invent a location or network owner.
4. Report whether the server connected, which databases are available, and the
   sample lookup result. State any remaining setup step. Describe geolocation as
   database information, not a person's precise location or a live observation.

Keep license keys out of conversation and tool arguments. Do not read credential
files into the conversation, edit the installed plugin, or overwrite existing
configuration. For missing credentials, direct the user to configure them outside
chat using the [configuration guide](https://github.com/oschwald/maxminddb-mcp/blob/main/docs/configuration.md).
Checking setup does not require installing or updating a database through a tool.

## Client configuration

- **Claude:** For the universal plugin, direct the user to
  /plugin → Installed → MaxMindDB → Configure in Claude Code to configure the
  bundled MCP server. Its settings support downloads or an existing database
  folder. The shell command `claude plugin configure` does not edit bundled
  MCPB settings. If Cowork does not offer configuration, use the MCPB extension
  in Claude Desktop chat. Platform-specific release plugins use top-level
  plugin settings. MCPB extension settings are a separate installation.
- **ChatGPT and Antigravity:** These plugins use existing server configuration.
  The Antigravity repository plugin also requires `maxminddb-mcp` on PATH.
  If `MAXMINDDB_MCP_CONFIG` is set, the executable uses that file. Otherwise it checks
  `~/.config/maxminddb-mcp/config.toml`,
  `~/.config/maxminddb-mcp/GeoIP.conf`, then `/etc/GeoIP.conf`.
  See [client setup](https://github.com/oschwald/maxminddb-mcp/blob/main/docs/clients.md)
  and [config discovery](https://github.com/oschwald/maxminddb-mcp/blob/main/docs/configuration.md#config-discovery-and-defaults).
  A manually configured stdio server can pass environment settings.
- **Gemini:** Direct the user to `gemini extensions config maxminddb` to set the
  account ID and license key outside chat. Release extensions use a native
  executable. Git installs use Docker. Both default to City and ASN downloads.
- **Cursor:** Direct the user to Plugins → Configure for the account ID, license
  key, and editions. This plugin uses Docker and supports downloads only.
