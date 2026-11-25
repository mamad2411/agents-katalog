---
name: agent-voice-mobile-bridge
description: Drive an Android phone (running WakeHermesClaw for Android) through its opt-in Mobile Bridge HTTP API. Use whenever Hermes needs to list installed apps, read the clipboard, fetch device info, or otherwise reach Android capabilities the user has explicitly enabled.
---

# WakeHermesClaw — Mobile Bridge skill

The WakeHermesClaw for Android app exposes a small HTTP service called the
**Mobile Bridge** that Hermes can call to interact with the user's
phone. Use this skill whenever a task requires reaching into Android.

## When to use this skill

- The user mentions their phone, an installed app, the clipboard, etc.
- A previous tool call returned a hint that an Android-side action is
  needed (e.g. "open Settings", "what apps do I have installed").

## When NOT to use this skill

- The user is asking about a remote desktop, a different device, or
  a service unrelated to their phone. The bridge is phone-only.
- The action is destructive (e.g. delete contacts, send SMS) and the
  user has not explicitly granted that capability group in WakeHermesClaw.

## How to call it

```python
from mobile_bridge import MobileBridge, MobileBridgeError

bridge = MobileBridge()  # reads AGENT_VOICE_BRIDGE_URL / _TOKEN

# 1) Discover what the user has enabled.
manifest = bridge.get_manifest()
allowed = {cap["name"] for cap in manifest["capabilities"]}

# 2) Refuse early if the requested capability is not in the allowlist.
if "apps.list" not in allowed:
    raise MobileBridgeError("apps.list is not enabled in WakeHermesClaw settings")

# 3) Execute. `execute` raises if the bridge replied status=failed,
#    surfacing the structured error (unsupported_capability, approval_required, …)
apps = bridge.execute("apps.list")
```

Always read `/manifest` once at the start of a session and trust it —
the user can toggle capability groups at any time. If you see
`approval_required` in an error, tell the user to look at their phone
and confirm the prompt.
