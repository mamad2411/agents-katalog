---
name: controlling-mijia-smart-home
description: Controlled local Xiaomi Mijia smart-home operations through the installable mijiactl CLI. Use this skill whenever the user asks an agent to install, configure, diagnose, list, inspect, or operate Xiaomi/Mijia devices, rooms, homes, scenes, MIoT properties, or MIoT actions, including natural-language requests such as turning on a light, starting an appliance, or running a scene, while keeping auth tokens hidden and respecting safety policy.
---

# Controlling Mijia Smart Home

Use `mijiactl` for every device operation. Do not call `mijiaAPI` directly, do not compose ad hoc Python snippets, and do not read or print `auth.json`.

## Install Check

If `mijiactl` is not available, read `references/setup.md` and tell the user to install the runtime:

```powershell
Invoke-RestMethod https://raw.githubusercontent.com/stg609/mijia-control-skill/master/scripts/install-mijiactl.ps1 | Invoke-Expression
```

Then run:

```powershell
mijiactl setup
```

Do not read or generate auth files manually. `mijiactl login` is the only supported authorization flow.

If the user asks to uninstall, remove, clean up, or stop using this Skill/runtime, read `references/setup.md` and offer the uninstall commands. Explain that normal uninstall keeps auth/config/cache, while `-PurgeData` deletes local auth, policy, capability cache, and snapshot cache.

## Required Flow

1. Run `mijiactl setup` or `mijiactl doctor` when setup, login, dependency, or policy state is unknown.
2. Run `mijiactl version` when the user asks what is installed or whether an update succeeded.
3. Follow `data.next_steps` exactly. If auth is missing or expired, run `mijiactl login` and have the user scan the QR code in Mijia.
4. Run `mijiactl config init` if policy config is missing.
5. Run `mijiactl devices --json` before selecting a device for property/action control. This uses a local 3-day snapshot cache by default.
6. Run `mijiactl homes --json` before running scenes. This also uses a local 3-day snapshot cache.
7. If the model is new or a property/action is unknown, run `mijiactl info --model <model> --json`.
8. Use only these commands for control:
   - `mijiactl get --did <did> --prop <name>`
   - `mijiactl set --did <did> --prop <name> --value <value>`
   - `mijiactl action --did <did> --action <name>`
   - `mijiactl action --did <did> --action <name> --arg <value>` for MIoT actions with input parameters; repeat `--arg` in the same order shown by `info`
   - `mijiactl scene list --home-id <home_id>`
   - `mijiactl scene run --id <scene_id> --home-id <home_id> --confirm <token>`

For natural-language device requests, map the user's wording to exactly one device from `devices --json`, then inspect that device's model with `info` before choosing a property or action. If more than one device plausibly matches, show candidates and ask the user to choose. Do not paste the full device or capability JSON to the user unless they explicitly ask for it; summarize only the matched device, candidates, command outcome, and any required confirmation token.

If the user asks to refresh, rescan, rediscover, sync, or update Mijia devices, homes, rooms, or scenes, use explicit refresh commands:

- `mijiactl devices --refresh --json`
- `mijiactl homes --refresh --json`
- `mijiactl scene list --home-id <home_id> --refresh`

Also refresh when the user says a device was renamed, added, removed, moved to another room, or the cached result looks wrong. Normal control commands should not force refresh; `mijiactl` will reuse fresh snapshots and automatically refresh snapshots older than 3 days.

For washers and other appliances, do not treat `on=true` as "start". Starting a program requires an MIoT action such as `start-wash`, and usually requires confirmation.

For speakers and other devices with parameterized actions, inspect the action's `in` list from `info` and pass each value with `--arg`. Example: if `play-text` has `in: [1]`, use `mijiactl action --did <did> --action play-text --arg "text to speak"`.

All command output is JSON:

```json
{"ok": true, "error": null, "data": {}}
```

or:

```json
{"ok": false, "error": {"code": "ERROR_CODE", "message": "...", "data": {}}, "data": null}
```

## Safety Rules

- Treat `ok: false` as authoritative. Branch on `error.code`; do not infer success from partial prose.
- If a command returns `POLICY_BLOCKED`, stop. Do not suggest bypassing the policy.
- If a command returns `CONFIRMATION_REQUIRED`, show the confirmation token and wait for explicit approval. Then rerun with `--confirm <token>`.
- If a command returns `AMBIGUOUS_DEVICE`, show candidates and ask the user to choose. Do not execute against multiple fuzzy matches.
- If a command returns `DEVICE_OFFLINE`, stop.
- If a command returns `AUTH_MISSING`, `AUTH_EXPIRED`, or `DEPENDENCY_MISSING`, return to the setup flow in `references/setup.md`.
- Never expose values from `auth.json`, Xiaomi account cookies, service tokens, `ssecurity`, `deviceId`, or `userId`.
- Scenes require confirmation by default.

For policy details, read `references/safety.md`.
