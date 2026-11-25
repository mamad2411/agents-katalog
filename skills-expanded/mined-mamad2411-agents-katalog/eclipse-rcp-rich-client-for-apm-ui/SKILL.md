---
name: eclipse-rcp-rich-client-for-apm-ui
description: Build a desktop-class APM / observability client on Eclipse RCP + ZEST/GEF for high-throughput real-time visualization that HTTP + JSON browsers struggle with
category: apm
version: 1.0.0
source_type: extracted-from-git
source_url: https://github.com/kjuhwa/scouter
source_ref: master
source_commit: 126bb19f07d1fe4fe915eb408c381e2c140cc94c
source_project: scouter
version_origin: extracted
tags: [rcp, eclipse, desktop, apm, visualization]
confidence: medium
---

# Eclipse RCP APM Client

Apply when your observability UX demands thousands of points per second, native OS widgets, and direct binary streams — where a browser SaaS dashboard would fall over or feel laggy.

## Pattern

1. **Eclipse RCP shell** — product definition + feature + plugin structure. Use Tycho for reproducible builds.
2. **Direct TCP** — client opens long-lived TCP to the collector, speaks the binary wire protocol. No servlet, no JSON.
3. **Local cache** — maintain in-memory rolling window (5min / 1h / 24h) so the UI doesn't re-query the server on every scroll/zoom.
4. **ZEST / GEF** — for waterfall trace and topology graphs. SWT charts for XLog scatter.
5. **Perspective per role** — DBA, dev, ops each get a preset perspective (preconfigured views).

## Evidence

- `scouter.client/`
- `scouter.document/client/How-To-Use-Client.md`
- `scouter.document/tech/Developer-Guide.md`

## Trade-offs

- Desktop install friction (Windows / macOS / Linux build per release).
- Hard to onboard new users; browser-first dashboards (Grafana, scouter-paper) are easier.
- But: real-time drill-down performance is genuinely better, and works offline/air-gapped.

## Related knowledge

- `rcp-desktop-client-design-rationale-vs-saas-web` (decision)
