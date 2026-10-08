---
name: "proxyman-cli"
description: "Discover and safely use the installed proxyman-cli for proxy control, MCP state, licenses, configuration, logs, certificates, rules, and debugging-tool automation. Use for Proxyman shell commands, scripts, CLI help, or operations that MCP does not execute."
---

# Proxyman CLI

Use the CLI installed with the user's Proxyman build. Never assume a command hierarchy or flags from static documentation.

## Discover Version-Matched Syntax

If Proxyman MCP is connected:

1. Call `get_proxyman_cli_help` with an empty command path for top-level help.
2. Call it again with command names only, for example `export-log` or `rules map-local create`.
3. Never include flags, values, pipes, redirects, or shell syntax in `command_path`.
4. Use the returned syntax, then execute an authorized operational command through the agent host's shell. The MCP helper never performs the command. If the command's only supported secret input is an argument, as with the reviewed `activate` command, provide a placeholder command for the user to run instead.

If MCP is unavailable:

1. Resolve the actual executable without changing shell profiles.
2. Run that executable with `--help`.
3. Run nested `--help` until every required argument and option is known.
4. If the CLI is missing, route to app installation/update or the GUI; do not substitute guessed syntax.

The official command-line page is useful background, but installed help wins for exact syntax. Read [command catalog](references/command-catalog.md) to choose a hierarchy, then discover it live.

## Plan Before Execution

1. Translate the user's intent to one command hierarchy.
2. Inspect current state through MCP, CLI list/get, or the GUI when possible.
3. Classify the command:
   - read-only: help, list, get, status;
   - filesystem write: export and export-log; use an explicit destination and confirm before overwriting an existing file;
   - reversible mutation: on/off, enable/disable, create/update;
   - destructive/sensitive: unlink, delete/remove, clear, override import, root/custom certificate changes, credential-bearing operations.
4. Show the command shape with secrets replaced by placeholders.
5. Obtain confirmation for destructive actions or newly requested system/trust/proxy changes.
6. Execute once, capture exit status, stdout, and stderr, and redact secrets.
7. Verify state with a separate status/list/get operation.

## Safety Rules

- Never invent flags or rely on a command example without checking the installed help.
- Never expose a license key, certificate password, proxy credential, cookie, token, or captured secret in output.
- Prefer GUI license entry. The reviewed `activate` command accepts the key only as an argument, which can expose it in shell history, process listings, and an agent tool call.
- Never execute the positional-argument `activate` form with a real key through the agent host. Provide a version-matched command shape with `<LICENSE_KEY>` for the user to substitute and run directly in their own terminal.
- Avoid embedding certificate passwords in committed scripts or reusable shell history. Use the safest input mechanism supported by current help.
- Treat `activate`, `unlink`, `clear-session`, rule delete/remove, configuration import with override, custom/root certificate changes, and proxy routing changes according to their real effect.
- Do not run a generated shell command merely because MCP returned help. The user request and confirmation still control execution.
- Use explicit file paths. Verify output paths before exports and input paths before imports/certificate operations.
- Do not modify shell profiles to make the executable discoverable unless the user specifically asks.

## Major Command Families

The installed build may expose:

- license: `activate`, `unlink`;
- application state: `proxy`, `proxy-host`, `mcp`, `clear-session`;
- configuration: `export`, `import`;
- logs: `export-log`;
- certificates: `custom-cert`, `install-root-cert`;
- debugging tools: Breakpoint, Map Local, Map Remote, Scripting, Block List, Allow List, Reverse Proxy, Network Condition, No Caching, DNS Spoofing, External Proxy;
- unified rule operations under `rules`.

Treat this as routing, not syntax. Read [rule automation](references/rule-automation.md) for the rule workflow.

## Important Workflows

### MCP Server State

Use the version-matched `mcp on`/`mcp off` hierarchy when the user wants to persistently enable or disable Proxyman's MCP server, including when the app is closed. Reload the MCP client after enabling and launch Proxyman before expecting operational tools.

### License Activation

Discover `activate --help`, but do not ask the user for the key and do not execute the reviewed positional-argument form through the agent host. Provide a command shape with `<LICENSE_KEY>` for the user to run directly. After a successful activation, have the user restart Proxyman before verifying the licensed state; do not quit the app without explicit authorization.

### Export Logs Or Configuration

1. Discover output formats, filters, flow-boundary options, and path rules.
2. Resolve the destination explicitly and avoid overwriting unless the user requested it.
3. Warn that captured logs may contain unredacted secrets.
4. Verify the resulting file exists and report its path and size, not its secret contents.

### Import Configuration

1. Validate the source path and discover merge/override semantics.
2. Explain whether existing configuration will be preserved or replaced.
3. Require confirmation for override/replacement.
4. Verify resulting rule inventories.

### Certificates

Differentiate the default Proxyman CA from importing a custom root or server/client certificate. Discover the relevant subcommand, certificate type, password handling, and trust option. Obtain confirmation before changing any trust store.

## Result Format

Report:

```text
Executable/version:
Command hierarchy:
Action:
Exit status:
Sanitized output:
Verification:
Rollback or next step:
```

If execution was not authorized or possible, provide the verified command shape with placeholders and state exactly what remains for the user.
