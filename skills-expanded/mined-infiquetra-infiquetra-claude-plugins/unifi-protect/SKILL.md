---
name: unifi-protect
description: Manage UniFi Protect cameras, liveviews, lights, sensors, chimes, and viewers via the UniFi Protect Integration API
---

# UniFi Protect Skill

Interacts with the UniFi Protect Integration API on a UniFi Dream Machine (UDM) to manage
surveillance cameras and related devices.

## Script

`./scripts/unifi_protect_client.py` — every command below invokes it.

## When to use this skill

Use it when the request is about UniFi Protect devices, for example:

- "show cameras" / "protect cameras" / "list protect devices"
- "camera snapshot"
- "unifi protect"
- "liveview"
- "protect lights" / "flood light"
- "protect sensors" / "door sensor"
- "protect chimes"
- "protect viewers"

## Environment Setup

```bash
export UNIFI_API_KEY="your-api-key"   # required (same key as unifi-network)
export UNIFI_HOST="192.0.2.1"         # required, no default
```

## Safety: Dry-Run by Default

All write operations require `--confirm` to execute. Without it the client prints the method,
URL, and body it would have sent, then exits without contacting the controller.

## Commands

Six resource groups, twenty-one actions. Anything not listed here is not implemented.

### Cameras
```bash
python unifi_protect_client.py cameras list
python unifi_protect_client.py cameras get --id <camera_id>
python unifi_protect_client.py cameras snapshot --id <camera_id> --output /tmp/snap.jpg
python unifi_protect_client.py cameras snapshot --id <camera_id>   # base64 JSON when --output is omitted
python unifi_protect_client.py cameras update --id <camera_id> --json '{"name":"Front Door"}' --confirm
```

### Liveviews
```bash
python unifi_protect_client.py liveviews list
python unifi_protect_client.py liveviews get --id <liveview_id>
python unifi_protect_client.py liveviews create --json '{"name":"Security","slots":[]}' --confirm
python unifi_protect_client.py liveviews update --id <liveview_id> --json '{"name":"Renamed"}' --confirm
python unifi_protect_client.py liveviews delete --id <liveview_id> --confirm
```

### Lights
```bash
python unifi_protect_client.py lights list
python unifi_protect_client.py lights get --id <light_id>
python unifi_protect_client.py lights update --id <light_id> --json '{"lightModeSettings":{"mode":"motion"}}' --confirm
```

### Sensors
```bash
python unifi_protect_client.py sensors list
python unifi_protect_client.py sensors get --id <sensor_id>
python unifi_protect_client.py sensors update --id <sensor_id> --json '{"name":"Garage Door"}' --confirm
```

### Chimes
```bash
python unifi_protect_client.py chimes list
python unifi_protect_client.py chimes get --id <chime_id>
python unifi_protect_client.py chimes update --id <chime_id> --json '{"volume":50}' --confirm
```

### Viewers
```bash
python unifi_protect_client.py viewers list
python unifi_protect_client.py viewers get --id <viewer_id>
python unifi_protect_client.py viewers update --id <viewer_id> --json '{"liveview":"<liveview_id>"}' --confirm
```

## Global Flags

```bash
--confirm       # execute a write operation instead of previewing it
--host HOST     # override UNIFI_HOST for one invocation
--verify-ssl    # enable TLS certificate verification (off by default; the UDM is self-signed)
```

## Not Implemented

Four capabilities were removed from the client in commit `8a14ad49` on 2026-03-17, when the
base URL moved to `/proxy/protect/integration/v1`. Do not offer them:

- Not implemented: camera `stream-url`.
- Not implemented: `ptz` control, including presets and patrol.
- Not implemented: `events` listing and retrieval.
- Not implemented: `nvr` info and bootstrap.
