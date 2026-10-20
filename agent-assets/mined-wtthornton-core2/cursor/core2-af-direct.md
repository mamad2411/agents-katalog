---
description: Hard rule — Core2 talks to AgentForge directly; no host middleware
alwaysApply: true
---

# Core2 ↔ AgentForge (HARD RULE)

Canonical product vision: `docs/firmware/VISION.md` (if conflict, VISION wins).

## Ownership

- This agent **owns Core2 only** (`C:\code\Core2`). Firmware, Core2 docs, Core2 Linear project.
- **Do not** implement or patch AgentForge, TappsMCP, or other sibling repos from this workspace.
- Missing AF APIs → file Linear issues on **AgentForge Platform** for AF design/implementation. Do not build a workaround host service in Core2.

## Architecture (locked)

- The **M5Stack Core2 device talks directly to AgentForge** over the network (HTTP/SSE).
- **Forbidden:** host/PC middleware that polls AF and pushes state to the brick (`af_bridge`, serial NDJSON ops bus, LAN `/v1/state` bridge, “keys stay on the PC”).
- USB serial is for **flash / debug logs only**, not the product data path.
- Secrets needed for AF (base URL, Bearer) live in **device** config (`secrets.h` / future NVS) — never a required always-on PC process.

## If AF cannot supply data

1. Document the gap in Core2 design docs.
2. Open / update Linear on **AgentForge Platform** with the consumer contract (endpoints, auth, payload).
3. Wait or stub UI with honest “no API” state — **do not** resurrect host bridge middleware.
