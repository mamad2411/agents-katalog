---
name: slc-device-ops
description: "Operate a Lantronix SLC9000/SLC8000 console server directly over its REST API through the slc-mcp-server: port and managed-device status, synchronous CLI commands with immediate output, config export/apply/restore, firmware updates and boot banks, session management, cellular modem status, and Percepxion client control. Use this skill whenever the user wants to inspect or change a specific SLC console server, run a CLI command and see the output right away, check serial ports or cellular signal, back up or restore device config, or manage an SLC's Percepxion cloud client, even if they only say 'the console server' or 'the SLC'."
version: 1.0.0
license: MIT
---

# SLC Device Operations

This skill covers the **slc-mcp-server**, which talks to one Lantronix SLC9000/SLC8000 console server at a time, directly over its REST API. It needs network reach to the device's management IP. Its defining advantage over the fleet path: **synchronous output**. `apply_config_commands` returns the device's CLI response in one call, no job polling.

For fleet-wide operations (many devices, smart groups, firmware compliance reports, audit logs) or for devices with no direct network path, use the companion **percepxion-mcp-server** and its `percepxion-fleet-ops` skill (https://github.com/Lantronix/percepxion-mcp-server). Capability split table at the end.

Full per-tool parameter reference: the Tool Reference section of this repository's `README.md` and `docs/tools.md`.

---

## Golden Rules

**Confirm before writing.** Every mutating tool takes a `confirm` parameter, and the server's CLI policy blocks write commands by default (`SLC_CLI_WRITE_ENABLED=false`). Present the exact change to the operator before calling `apply_config_commands`, `firmware_update`, `reboot_device`, `terminate_session`, `update_sysadmin_user`, or any px client start/stop. `factory_reset` requires the literal confirm string `"FACTORY RESET"` and is irreversible; treat it as radioactive.

**The CLI policy is server-side.** `SLC_CLI_WRITE_ENABLED`, the deny list, and the allowlist are environment variables on the MCP server process. You cannot override them at runtime, and the device's own role system applies on top: a command that passes MCP policy can still be rejected by the device if the account lacks the role.

**Read before you write.** `get_system_status` + `get_slc_port`/`get_slc_ports` before changing anything. `export_config_commands` (a replayable backup) before config changes worth protecting.

**Never expose credentials** (`SLC_PASSWORD`, `SLC_*_TOTP_SECRET`, `VAULT_TOKEN`, session tokens) in output, logs, or error messages.

---

## Setup

Requires Python 3.11+ and network access to the SLC's management IP.

```bash
git clone https://github.com/Lantronix/slc-mcp-server.git
cd slc-mcp-server
pip install -e .
```

`pip install -e .` pulls in all dependencies including `pyotp`, required for 2FA-enabled devices.

**Claude Code:**

```bash
claude mcp add slc \
  --env SLC_DEFAULT_IP=192.0.2.10 \
  --env SLC_USERNAME=sysadmin \
  --env SLC_PASSWORD=yourpassword \
  -- python3 /path/to/slc-mcp-server/run_server.py
```

**Claude Desktop:** copy `config/claude_desktop_config.example.json` from this repository into your `claude_desktop_config.json` and fill in device details. `config/claude_desktop_config.wsl_windows.example.json` covers the WSL-on-Windows case.

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SLC_DEFAULT_IP` | | Default device IP, used when `device_id` isn't in the per-device registry |
| `SLC_USERNAME` | `sysadmin` | Default username |
| `SLC_PASSWORD` | | Default password |
| `SLC_TOTP_SECRET` | | Default TOTP secret (base32 string) for 2FA-enabled devices |
| `SLC_{KEY}_IP` / `SLC_{KEY}_USERNAME` / `SLC_{KEY}_PASSWORD` / `SLC_{KEY}_TOTP_SECRET` | | Per-device credentials. `{KEY}` is the `device_id` uppercased with non-alphanumeric characters replaced by `_` (device_id `slc9000-dc-a` → `SLC_SLC9000_DC_A_IP`). Per-device vars beat globals. |
| `SLC_VERIFY_SSL` | `true` | Set `false` only for lab devices with self-signed certificates. Never in production. |
| `SLC_CREDENTIAL_PROVIDER` | `env` | `env`, `vault`, `aws`, `azure`, `percepxion`, `cyberark`, or `command` (table below) |
| `*_FILE` forms | unset | Each username, password and TOTP secret variable also accepts `_FILE` (for example `SLC_PASSWORD_FILE`), reading the first line of that file. Setting both forms is an error. |
| `SLC_KNOWN_DEVICE_IDS` | unset | env and command providers: comma-separated allowlist of device_ids; rejects unknown IDs before falling back to default credentials |
| `SLC_CLI_WRITE_ENABLED` | `false` | Allow write commands via `apply_config_commands` and px client tools |
| `SLC_CLI_MAX_LENGTH` | `512` | Maximum command length |
| `SLC_CLI_DENY_COMMANDS` | built-in list | Additional comma-separated commands to block |
| `SLC_CLI_PERMIT_COMMANDS` | unset | If set, only these command prefixes are permitted |
| `SLC_CLI_YOLO` | `false` | Disable ALL CLI policy filtering. Never in production. |

**Built-in deny list** (always blocked unless YOLO): `factory-reset`, `write erase`, `erase startup-config`, `erase flash`, `reload`, `reboot`, `format`, `shutdown`, `power off`, `reset system`, `init 0`, `halt`. Read-only commands (`show`, `diag`, `ping`, `traceroute`) are always permitted.

### Credential Providers

| Provider | How it works |
|---|---|
| `env` (default) | Env vars above; per-device beats global. Single-device and small setups. |
| `vault` | HashiCorp Vault KV v2 at `slc/{device_id}` (`VAULT_ADDR`, `VAULT_TOKEN`); secret holds `ip`, `username`, `password`, optional `totp_secret`. |
| `aws` | AWS Secrets Manager at secret name `slc/{device_id}`, standard AWS credential chain; same JSON fields. |
| `azure` | Azure Key Vault (`AZURE_KEYVAULT_URL`) secret `slc-{device_id}` (non-alphanumerics become `-`; prefix via `AZURE_KEYVAULT_SECRET_PREFIX`); same JSON fields. Auth via `DefaultAzureCredential`; needs the `[azure]` extra. |
| `percepxion` | Looks up the device **IP** from the Percepxion device registry by `device_id` (`PERCEPXION_API_URL`, `PERCEPXION_USERNAME`, `PERCEPXION_PASSWORD`); SLC credentials still come from `SLC_{KEY}_*` vars. Use when inventory lives in Percepxion and IPs change. |
| `cyberark` | CyberArk CCP REST API (`CYBERARK_URL`, `CYBERARK_APP_ID`, `CYBERARK_SAFE`); one CyberArk account per SLC with Object = device_id, Address = management IP. mTLS auto-enables when `CYBERARK_CERT_PATH`/`CYBERARK_KEY_PATH` are set. |
| `command` | Runs `SLC_CREDENTIAL_COMMAND` per device (`{device_id}` substituted, `SLC_DEVICE_ID` in its env); it prints JSON `ip`, `username`, `password`, optional `totp_secret`. Any secrets CLI (1Password, Bitwarden, Infisical, Delinea, Keeper, a script). |

Switch at runtime with `configure_provider(provider="vault")`, no restart needed.

**2FA:** TOTP challenge-response is automatic once the device's base32 TOTP secret is in the matching env var. First-time PIN setup must be completed in the device web UI before the server can authenticate; only `passcode`/`tokencode` challenge types are handled.

---

## Choosing the CLI Path (this server vs. Percepxion)

`apply_config_commands` (this server) sends CLI commands to the SLC and returns the output synchronously, one call, no polling. Prefer it whenever the agent can reach the device's management IP.

`send_direct_cli_command` (percepxion-mcp-server) dispatches through Percepxion's async job system: submit, poll `get_job_group` until `"Completed"`, then `get_cli_command_output` for the text (percepxion-mcp-server v1.1.0+). Use it for devices with no direct network path, or for fleet-wide dispatch.

Both paths run commands on the SLC's own CLI, never interactively on managed devices attached via serial. `get_managed_devices` reads the managed-device inventory; an interactive session to an attached router or switch is a human operation (`ssh` to the SLC, `connect direct deviceport N`).

---

## Workflows

### Device Health Check

1. `get_system_status(device_id)`: uptime, state.
2. `get_system_version(device_id)` and `get_system_identity(device_id)`: firmware, hostname, location. `update_system_identity(device_id, hostname, description, confirm=True)` sets hostname/description (confirm first).
3. `get_network_interfaces(device_id)` if connectivity is in question; `get_cellular_status(device_id)` for the cellular path (signal_strength, state, band, apn, imei).
4. `get_ztp_status(device_id)` on freshly deployed devices.

### Port and Managed-Device Inspection

1. `get_slc_ports(device_id)` for all serial ports; `get_slc_port(device_id, port_id="4")` for one (`port_id` is a string).
2. `get_managed_devices(device_id)` for the inventory of what's cabled to those ports; `get_managed_device(device_id, managed_device_id)` for one.
3. `get_connections(device_id)` for active connections.
4. For deeper detail the ports API doesn't expose, `apply_config_commands(device_id, commands=["show deviceport port 4"])` returns the CLI view synchronously (read-only commands always pass policy).

### Config Backup, Change, Restore

1. **Backup first:** `export_config_commands(device_id)` produces a replayable CLI command export; `export_config_for_edit(device_id)` exports the full config blob.
2. Apply changes: `apply_config_commands(device_id, commands=[...], confirm=True)`, write commands need `SLC_CLI_WRITE_ENABLED=true` on the server and operator confirmation. Output comes back in the same call; check it, don't assume success.
3. Persist: `save_config(device_id, confirm=True)` writes running config to non-volatile storage.
4. Recover: `restore_config_baseline(device_id, confirm=True)` restores the saved baseline.

### Firmware Update

1. `get_firmware_version` and `check_firmware_updates` to establish current vs available.
2. `get_firmware_bootbank(device_id)`: SLC devices have two boot banks; `set_firmware_bootbank(device_id, bank, confirm=True)` selects which one boots next, which is also the rollback mechanism.
3. `firmware_update(device_id, preserveconfig=True, confirm=True)` after operator confirmation.
4. Poll `get_firmware_update_status(device_id)`; on failure read `get_firmware_log(device_id)` before retrying anything.

### Session Management

1. `get_sessions(device_id)` lists active web UI, API, and WebTerm sessions; `get_session(device_id, session_id)` for one.
2. `terminate_session(device_id, session_id, confirm=True)` forcibly ends a session. Confirm with the operator and identify whose session it is first; you may be about to disconnect a working engineer.
3. `logout_device(device_id)` invalidates this server's own API session token.
4. `get_sysadmin_user(device_id)` reads the sysadmin account configuration; changes go through `update_sysadmin_user` (confirm first, see Golden Rules).

### Percepxion Client Control

The SLC runs a Percepxion cloud client; these tools manage it from the device side (useful when onboarding a device into Percepxion or debugging cloud connectivity).

1. `get_px_status(device_id)`: enable state, connection, server URL, last heartbeat. Always readable.
2. `start_px_client(device_id, confirm=True)`: registers with the cloud in roughly 30 seconds. `stop_px_client` takes 60-120 seconds to shut down. `restart_px_client(..., timeout_seconds=120)` sequences stop-wait-start. All three require `SLC_CLI_WRITE_ENABLED=true`.

---

## Which Server for Which Job

There is no capability overlap by design between this server and percepxion-mcp-server:

| Capability | slc-mcp-server (direct) | percepxion-mcp-server (fleet) |
|---|---|---|
| Serial port status/config | `get_slc_port`, `get_slc_ports` | `list_device_ports` |
| CLI commands, synchronous output in one call | `apply_config_commands` | - |
| CLI commands, async job + output fetch | - | `send_direct_cli_command` + `get_cli_command_output` |
| Firmware update | `firmware_update`, `get_firmware_update_status` | `update_firmware_by_smart_group` |
| Device config backup | `export_config_commands` | `get_device_config` |
| User/session management | `get_sessions`, `terminate_session` | - |
| Reboot | `reboot_device` | `reboot_device` (fleet) |
| Cellular status | `get_cellular_status` | - |
| Fleet-wide ops (smart groups, templates, compliance) | - | Yes |
| Audit logs | - | `investigate_audit_logs` |

Route here when the agent can reach the SLC's management IP and wants immediate output or device-level features (boot banks, sessions, cellular, px client). Route through Percepxion for fleet scale, unreachable devices, or audit evidence.
