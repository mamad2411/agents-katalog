---
name: home-assistant
description: Manage Home Assistant via ha-mcp (API) and SSH (config-level). Covers automations, dashboards, entity registry, and log analysis.
user-invocable: true
---

# Home Assistant Management

## Environment

- HA URL: http://homeassistant.local:8123
- SSH host: `homeassistant` (hassio@homeassistant.local, key auth, see ~/.ssh/config)
- Internal API (from within HA container): http://172.30.32.1:8123
- Token env var on HA: `source /config/.env` (contains HA_URL and HA_TOKEN)
- MCP server: ha-mcp (user-scoped, always available)

## Tool Selection

Use **ha-mcp** for:
- Listing, creating, editing, enabling/disabling automations
- Controlling entities and calling services
- Querying entity states and device info
- Creating and managing helpers (input_boolean, input_number, etc.)
- Dashboard operations supported by the API

Use **SSH** for:
- Reading/writing YAML config files directly
- Editing `.storage` files (entity registry, device registry, core.config_entries)
- Log analysis and debugging
- Supervisor operations (restart, reload, check, update)
- Anything ha-mcp can't do or when you need to see raw config

**Default to ha-mcp.** Only SSH when the API can't do what's needed.

## Key File Paths (via SSH)

```
/config/configuration.yaml       # Main config
/config/automations.yaml         # All automations
/config/scripts.yaml             # Scripts
/config/scenes.yaml              # Scenes
/config/customize.yaml           # Entity customizations
/config/.storage/                # Internal registries
/config/.storage/core.entity_registry    # Entity IDs, names, disabled status
/config/.storage/core.device_registry    # Device info
/config/.storage/core.config_entries     # Integration configs
/config/.storage/lovelace.dashboards     # Dashboard registry
/config/.storage/lovelace              # Default dashboard config
```

## SSH Command Patterns

```bash
# Read a config file
ssh homeassistant 'cat /config/automations.yaml'

# Edit a file (write via heredoc or sed)
ssh homeassistant 'cat > /tmp/patch.yaml << "PATCH"
<content>
PATCH
'

# HA CLI (built into HA OS)
ssh homeassistant 'ha core check'          # Validate config
ssh homeassistant 'ha core restart'        # Full restart
ssh homeassistant 'ha core logs'           # Core logs
ssh homeassistant 'ha supervisor logs'     # Supervisor logs
ssh homeassistant 'ha addons logs core_ssh' # Add-on logs

# REST API via curl (from inside container)
ssh homeassistant 'source /config/.env && curl -s -H "Authorization: Bearer $HA_TOKEN" http://172.30.32.1:8123/api/states' | python3 -m json.tool

# Reload specific domains (no restart needed)
ssh homeassistant 'source /config/.env && curl -s -H "Authorization: Bearer $HA_TOKEN" -X POST http://172.30.32.1:8123/api/services/automation/reload'
ssh homeassistant 'source /config/.env && curl -s -H "Authorization: Bearer $HA_TOKEN" -X POST http://172.30.32.1:8123/api/services/script/reload'
ssh homeassistant 'source /config/.env && curl -s -H "Authorization: Bearer $HA_TOKEN" -X POST http://172.30.32.1:8123/api/services/scene/reload'
ssh homeassistant 'source /config/.env && curl -s -H "Authorization: Bearer $HA_TOKEN" -X POST http://172.30.32.1:8123/api/services/homeassistant/reload_core_config'
```

## Automation Management

### Creating automations
- Prefer ha-mcp for creating automations — it handles YAML syntax and ID generation.
- For complex automations or bulk edits, SSH into `/config/automations.yaml`.
- Every automation needs a unique `id` (use lowercase with underscores, e.g. `kitchen_motion_light`).
- Always specify `mode:` explicitly (`single`, `restart`, `queued`, `parallel`).

### Editing automations
1. Try ha-mcp first.
2. If editing YAML directly via SSH:
   - Read the full file first: `ssh homeassistant 'cat /config/automations.yaml'`
   - Make targeted edits — never regenerate the entire file.
   - Validate: `ssh homeassistant 'ha core check'`
   - Reload: use the automation reload curl command above (no restart needed).

### Debugging automations
1. Check if it's enabled: query state via ha-mcp or `ssh homeassistant 'source /config/.env && curl -s -H "Authorization: Bearer $HA_TOKEN" http://172.30.32.1:8123/api/states/automation.<id>'`
2. Check logs: `ssh homeassistant 'ha core logs' | grep -i automation`
3. Trigger manually via ha-mcp or: `ssh homeassistant 'source /config/.env && curl -s -H "Authorization: Bearer $HA_TOKEN" -X POST http://172.30.32.1:8123/api/services/automation/trigger -d "{\"entity_id\": \"automation.<id>\"}"'`
4. Check trace: HA UI → Settings → Automations → click automation → Traces tab

### Best practices
- Prefer native triggers/conditions over Jinja2 templates where possible.
- Use `choose:` for branching logic instead of multiple automations.
- Use `input_boolean` helpers for conditional enable/disable rather than removing automations.
- Use `trigger.id` with `choose:` when an automation has multiple triggers.
- Set `max_exceeded: silent` on automations that may fire frequently.

## Dashboard / Lovelace Management

### Via SSH
Dashboard configs live in `/config/.storage/lovelace` (default) and `/config/.storage/lovelace.dashboards` (custom dashboards).

```bash
# Read default dashboard
ssh homeassistant 'cat /config/.storage/lovelace' | python3 -m json.tool

# Read dashboard registry
ssh homeassistant 'cat /config/.storage/lovelace.dashboards' | python3 -m json.tool
```

### Editing dashboards
- For simple changes, use ha-mcp if it supports the operation.
- For direct edits via SSH:
  1. Stop HA core first if editing `.storage` files: `ssh homeassistant 'ha core stop'`
  2. Back up the file: `ssh homeassistant 'cp /config/.storage/lovelace /config/.storage/lovelace.bak'`
  3. Edit the JSON.
  4. Start HA core: `ssh homeassistant 'ha core start'`
- For YAML-mode dashboards defined in `configuration.yaml`, edit the YAML file and reload.

### Best practices
- Use sections view (`type: sections`) for new dashboards — it's the modern default.
- Prefer `type: tile` cards for entity control.
- Group cards by area/room.
- Use `type: conditional` to show/hide cards based on state.

## Entity Registry Operations

The entity registry lives at `/config/.storage/core.entity_registry`. It's a JSON file.

### Reading
```bash
# Full registry
ssh homeassistant 'cat /config/.storage/core.entity_registry' | python3 -m json.tool

# Find a specific entity
ssh homeassistant 'cat /config/.storage/core.entity_registry' | python3 -c "
import json, sys
data = json.load(sys.stdin)
for e in data[\"data\"][\"entities\"]:
    if \"kitchen\" in e.get(\"entity_id\", \"\").lower():
        print(json.dumps(e, indent=2))
"
```

### Modifying (rename, disable, delete)
**This requires stopping HA core to prevent the registry being overwritten on shutdown.**

```bash
# 1. Stop HA core
ssh homeassistant 'ha core stop'

# 2. Back up
ssh homeassistant 'cp /config/.storage/core.entity_registry /config/.storage/core.entity_registry.bak'

# 3. Modify (use python3 to parse, edit, and write JSON)
ssh homeassistant 'python3 << "SCRIPT"
import json
with open("/config/.storage/core.entity_registry") as f:
    data = json.load(f)
for e in data["data"]["entities"]:
    if e["entity_id"] == "light.old_name":
        e["entity_id"] = "light.new_name"
        # Also update unique_id if needed
with open("/config/.storage/core.entity_registry", "w") as f:
    json.dump(data, f, indent=2)
SCRIPT'

# 4. Start HA core
ssh homeassistant 'ha core start'
```

### Disabling an entity
Same stop/edit/start pattern. Set `"disabled_by": "user"` on the entity. Set to `null` to re-enable.

## Log Analysis and Debugging

### Reading logs
```bash
# Recent core logs
ssh homeassistant 'ha core logs' | tail -200

# Follow logs in real-time (ctrl-c to stop)
ssh homeassistant 'ha core logs --follow'

# Supervisor logs
ssh homeassistant 'ha supervisor logs' | tail -100

# Filter for specific integration
ssh homeassistant 'ha core logs' | grep -i 'zwave\|zigbee\|mqtt\|<integration>'

# Filter for errors/warnings only
ssh homeassistant 'ha core logs' | grep -iE '(error|warning|exception|traceback)'
```

### Common debugging patterns
1. **Automation not firing**: Check logs for the automation ID, verify trigger entity exists, check conditions, manually trigger to test.
2. **Entity unavailable**: Check integration logs, verify device is online, check config entries in `.storage/core.config_entries`.
3. **Integration failing**: `ssh homeassistant 'ha core logs' | grep -i <integration_name>` — look for auth errors, connection timeouts, API changes.
4. **Performance issues**: `ssh homeassistant 'ha core logs' | grep -i 'took too long\|timeout\|slow'`

### Checking HA info
```bash
ssh homeassistant 'ha core info'      # Version, running state
ssh homeassistant 'ha supervisor info' # Supervisor version, channel
ssh homeassistant 'ha host info'       # OS info, hostname
ssh homeassistant 'ha network info'    # Network config
```

## Safety Rules

1. **Always read before writing.** Never generate a full config file from scratch — read the existing one and make targeted edits.
2. **Validate before restart.** Run `ha core check` before any restart.
3. **Prefer reload over restart.** Use domain-specific reload endpoints when possible (automations, scripts, scenes). Only restart for `configuration.yaml` changes.
4. **Back up before .storage edits.** Always `cp` the file before modifying it.
5. **Stop core before .storage writes.** HA overwrites `.storage` files on shutdown — if you edit while running, your changes will be lost.
6. **Never store tokens in plain files** other than `/config/.env`.
7. **Test automations after changes.** Trigger manually and check logs to verify behavior.
8. **Preserve formatting.** When editing YAML, maintain existing indentation and comment style. When editing JSON `.storage` files, maintain the structure.
