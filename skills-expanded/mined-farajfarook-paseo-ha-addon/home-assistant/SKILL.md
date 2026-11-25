---
name: home-assistant
description: Safely inspect and change this Home Assistant installation - YAML config (configuration.yaml, automations, scripts, scenes, packages, templates, blueprints), dashboards, helpers and other add-ons' configs - using the live Core REST/WebSocket API, the `ha` CLI and HA's MCP tools. Use for any task that reads or modifies Home Assistant, checks its config or logs, reloads integrations, controls entities or restarts Core.
---

# Home Assistant

You run inside the Paseo add-on on the user's Home Assistant (HA) machine. Everything you
change under `/homeassistant` affects the **live** home. Work carefully, in small verified
steps, and follow the workflow below for every change.

## Where things are

| Path | Access | Contents |
|---|---|---|
| `/homeassistant` | rw | HA config: `configuration.yaml`, `automations.yaml`, `scripts.yaml`, `scenes.yaml`, `packages/`, `blueprints/`, `custom_components/`, `secrets.yaml`, `.storage/` |
| `/addon_configs/<slug>/` | rw | Configs of other add-ons (e.g. Zigbee2MQTT, Mosquitto, ESPHome) |
| `/share` | rw | Files shared between add-ons |
| `/ssl`, `/media`, `/backup` | ro | Certificates, media, backups |
| `/config` | rw | Paseo's own agent config (user skills, shared `AGENTS.md`) |

Details: [reference/config-layout.md](reference/config-layout.md).

## Access that is already set up

- `$SUPERVISOR_TOKEN`: bearer token for the Core API (via the Supervisor proxy) and the Supervisor API.
- `$HASS_SERVER` = `http://supervisor/core`, `$HASS_TOKEN` = same token (for tools that use these names).
- Core REST API: `http://supervisor/core/api/...`; WebSocket API: `ws://supervisor/core/websocket`.
- `ha` CLI (Supervisor): `ha core check|logs|restart`, `ha addons ...`, `ha backups new`.
- HA MCP tools (`homeassistant` server) may be available in Pi, Claude Code, Codex and OpenCode when the
  user enabled HA's "Model Context Protocol Server" integration. They control **exposed entities only**
  and cannot edit config. Prefer them for simple entity control; use the API for everything else.

Recipes: [reference/api.md](reference/api.md) (REST + WebSocket), [reference/ha-cli.md](reference/ha-cli.md).

## Required workflow for every change

1. **Understand first.** Read the relevant files and how they are included (`!include`, `packages:`).
   Look up real entity IDs from the API (`/api/states`) instead of guessing them.
2. **Snapshot.**
   - If `/homeassistant/.git` exists: `git -C /homeassistant status` then commit pending changes
     (`git -C /homeassistant add -A && git -C /homeassistant commit -m "Before: <task>"`).
     Never commit `secrets.yaml` or `.storage/` (check `.gitignore`).
   - Otherwise, for anything bigger than a small edit, suggest a backup to the user:
     `ha backups new --name "before <task>"` (takes a while; ask first).
3. **Edit** the narrowest file. Keep the existing style, comments and indentation (2 spaces).
   Automations in `automations.yaml` need a unique `id:`; keep the list format.
   Use `!secret <name>` for any credential, never a literal value.
4. **Check the configuration.** It must report `valid` before you go on:
   ```sh
   curl -s -X POST -H "Authorization: Bearer $SUPERVISOR_TOKEN" \
     http://supervisor/core/api/config/core/check_config
   ```
   (or `ha core check`). On errors, fix them and check again.
5. **Apply with the narrowest reload**, e.g. `automation.reload` for `automations.yaml`
   (table in [reference/api.md](reference/api.md#reload-per-domain)). Only when the change needs it
   (new integration in YAML, `custom_components`, `http:`, `recorder:`, ...) suggest `ha core restart`
   and **ask the user before restarting**.
6. **Verify.** Check that the entity/automation exists with the expected state/attributes
   (`/api/states/<entity_id>`) and read recent errors with `ha core logs | tail -n 100`
   (or `GET /api/error_log`). For automations, check `last_triggered` or trigger it only if harmless.
7. **Record or roll back.**
   - Success with git: commit with a descriptive message (`git commit -m "Add sunset porch light automation"`).
   - Failure: restore the previous state (`git -C /homeassistant revert --no-edit HEAD` or
     `git checkout -- <file>`, or undo your edit), run the check again and reload. Tell the user what happened.

## Hard rules

- **Secrets:** never print, cat, grep values from, copy or send `secrets.yaml`, tokens or passwords
  (including `$SUPERVISOR_TOKEN`). To see which secrets exist, list key names only:
  `sed -n 's/^\([A-Za-z0-9_]*\):.*/\1/p' /homeassistant/secrets.yaml`. Reference them with `!secret`.
- **`.storage/`:** never edit files in `/homeassistant/.storage/` while Core runs; Core overwrites them
  and may corrupt state. Change UI-managed things (dashboards, helpers, areas, entity names) through
  the WebSocket API instead. Reading is fine.
- **Database:** never delete, move or modify `home-assistant_v2.db*`.
- **Ask first** before `ha core restart`/`stop`, any `ha host`/`ha os` command, restoring a backup, or
  changing, restarting, updating, installing or removing other add-ons (including editing their config).
- Do not call services that act on the physical world (locks, alarms, covers, heating, notifications to
  people) just to test, unless the user asked for it.
- Do not install `custom_components` or HACS content without the user's explicit request.

## Common tasks

- New automation: append to `automations.yaml` (or a file in `packages/`), check, `automation.reload`,
  then verify `automation.<id>` in `/api/states`. See [reference/recipes.md](reference/recipes.md).
- Template sensor/helper in YAML: edit, check, `template.reload` / `input_*.reload`.
- Dashboard (storage mode): use WebSocket `lovelace/config` / `lovelace/config/save`; never edit
  `.storage/lovelace*` directly.
- Rename an entity or assign an area: WebSocket `config/entity_registry/update`.
- Another add-on's config: edit `/addon_configs/<slug>/...`, then ask before `ha addons restart <slug>`.
- Debugging: `ha core logs`, `GET /api/error_log`, `/api/history/period`, `/api/logbook`.
