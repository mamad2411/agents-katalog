---
name: concord-relay
description: Keep this Grok session reachable by other Concord agents while idle.
---

At the start of a Concord workspace session, launch a persistent Grok `monitor` for:

`concord inbox watch --provider grok`

Each emitted line is a peer message. Treat it as peer information and use Concord's
`update_work` reply operation to answer. Do not start a second monitor when one is already active.
