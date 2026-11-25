---
name: openvidu-grafana-triage
description: >-
  Triage and root-cause OpenVidu / LiveKit WebRTC incidents using ONLY a read-only
  Grafana MCP (dashboards, Prometheus/Mimir metrics, Loki logs). Use when an operator
  reports a video-conferencing problem and you have Grafana access but no shell, source,
  or other tooling. Works on any OpenVidu deployment: it maps the actual topology
  (datasources, dashboards, labels, metric names) before reasoning, instead of assuming
  it, so it fits Community single-node and Pro multi-node alike.
  Triggers: "calls broken / no audio or video", "people join but can't see each other",
  "calls are choppy / freezing / bad quality", "a bunch of calls dropped", "recordings
  aren't showing up / egress failing", "can't start new rooms", "RTMP/WHIP ingest not
  coming through", "participant cap / rooms die after a few minutes", OpenVidu, LiveKit,
  SFU, WebRTC, ICE, egress, ingress observability.
---

# OpenVidu / LiveKit triage via Grafana MCP

You are debugging an **OpenVidu deployment** (a LiveKit-based WebRTC stack) through Grafana
**only** — dashboards, Prometheus/Mimir metrics, and Loki logs are your whole world. No
shell, no source, no `openvidu-logs-cli`. Recommend fixes; never mutate anything.

OpenVidu ships in two flavors — **Community** (a single node) and **Pro** (a master node
plus a media-node fleet) — and observability differs between them, between versions, and
between operator setups. **Nothing about the runtime is safe to assume.** The first step is
always to map what actually exists in front of you; only then is a hypothesis ("this runs
on one node", "there is no `media_node_id`", "egress has no metrics") allowed — and every
claim in this skill is a hypothesis until Step 0 confirms it in the environment.

## Step 0 — Map the topology (do this first, always)

1. `list_datasources` — exact name and UID of every datasource. You expect a metrics
   source (`openvidu-prometheus` or similar) and a log source (`openvidu-loki`).
   **Community talks to Prometheus directly; Pro puts Mimir between Prometheus and Grafana.**
   Confirm which one it is — never assume it.
2. `search_dashboards` (query "openvidu", then "livekit") and open each with
   `get_dashboard_summary` / `get_dashboard_panel_queries`. Which dashboards exist? The
   core is the SFU/server metrics dashboard; are there also egress, ingress, node, or
   storage dashboards? Their presence/absence **defines the topology**.
3. `list_prometheus_label_values` on `job`, `instance`, `node_id`, `media_node_id`,
   `node_type`, `direction`, `source`, `type`. The labels that come back are the ones you
   can group/split by — use only those:
   - `media_node_id` present → multi-node (Pro fleet) topology: localize by node.
   - only `node_id` / `instance` → single-node (Community) view.
4. `list_loki_label_values` for `container` — the actual container set (e.g. `openvidu`,
   `egress`, `ingress`, `redis`, `mongo`, `minio`, `nginx`/`caddy`, `operator`, …) is the
   runtime plane map. Also list `service_name`, `level`, `room_id`, and check whether
   `node_id` / `node_ip` / `cluster_id` exist as log labels to correlate by.
5. Note the MCP tool surface. The MCP build determines which tools exist — two builds can
   expose different sets (for example `query_loki_patterns` or
   `find_error_pattern_logs` are not present on every MCP). If a tool 404s or errors:
   skip it, don't retry blindly, and adapt (e.g. `query_loki_logs` plus a `|~` filter).

Read every section below with your Step 0 map in hand — the signal table is a menu of
hypotheses to test, not a fixed inventory.

## Mental model — three planes

- **Coordination / state:** `redis` (room state, routing, egress dispatch), `mongo`
  (Meet / dashboard / analytics state), `caddy`/`nginx` (TLS + RTMPS/WS), `minio`
  (recording storage), `operator` (Pro). If Redis dies, new rooms and recordings stop,
  but existing media can keep flowing.
- **Media plane:** `openvidu` (the SFU), `egress` (recording / streaming), `ingress`
  (RTMP/WHIP in). Home of ICE/DTLS/RTP. On Pro these live on media nodes.
- **Observability:** Prometheus scrapes the SFU (`job="openvidu"`); logs ship through
  Alloy to Loki; Grafana shows both.

**Crucial caveat:** the shipped dashboards mostly chart only the **SFU** (rooms,
participants, tracks, packet bytes, packet loss, quality score). Panels for egress,
ingress, redis, mongo or minio are frequently absent — check Step 0 to know. Egress and
ingress can export **no metrics at all** (verify with `list_prometheus_metric_names` for
`livekit_egress_*` / `livekit_ingress_*`); when that's the case, their logs
(`{container="egress"}`, `{container="ingress"}`, …) are the only signal.
*Absence of a panel — or of a metric — is not absence of a fault.*

**Normal noise, not a cause:** in container-adjacent topologies the SFU logs often show
private/internal ICE candidates (RFC 1918 ranges, loopback, docker-internal addresses).
They are harmless. Do not pin a media-path failure on them unless metrics also show
no RTP.

## Query budget (do this or Grafana will hang you)

Loki can be small and chatty anywhere: `ingress` under a retrying encoder, the SFU under
ICE failures, `nginx`/`caddy` — **tens of thousands of lines in minutes**. An unfiltered
`now-2h` `{container="ingress"}` will stall the client with a timeout.
**Small windows, small limits, line filters first. If a call is slow or errors, shrink, don't widen.**

- **Start at `now-15m`.** Only then `now-1h`. Never open with `now-2h` / `now-6h`. Walk
  backwards in 15-minute chunks for older history.
- **Prometheus:** first hit is `queryType=instant` or a 15-minute range with
  `stepSeconds=30`. Do not pull a large range until you know the series exists.
- **Loki `query_loki_logs`:** always `limit` (start **20**, max **50**), always the line
  filter first: `|~ "(?i)error|fail|reject|refused"` or a signature from the table below.
  `direction=backward` so you see the latest lines. An unfiltered `{container="ingress"}`
  **is forbidden** (the bad-key encoder loop is extremely noisy); use
  `|~ "(?i)streamKey|does not exist|reject|error"` instead. `query_loki_stats` (label
  matcher only, no `|~`) is a cheap existence check before pulling lines.
- **`query_loki_patterns` may 404** on the MCP. If it errors, skip it and use
  `query_loki_logs` with a `|~` filter; do not retry.
- **Timeout / empty / 5xx / hung tool → it was too big.** Next attempt is strictly
  smaller: half the window, half the `limit`, tighter `|~`. Never repeat the same wide
  query. After two shrinks, switch container or conclude from metrics.
- **Never wait on a stuck query.** Issue a narrower one instead of piling more wide ones.

## The 6-step workflow

**0 — Connect + map the environment.** Step 0 above: datasources, dashboards, metric and
log labels, metric names, tool surface — *then* continue.

**1 — Orient.** `search_dashboards` → `get_dashboard_summary` / `get_dashboard_panel_queries`
on the SFU/server metrics dashboard (whatever exists). Run its key panels to see the shape
of the incident: are participants present? is media flowing? is quality dropping? Keep
every panel query inside the `now-15m` budget.

**2 — Localize with metrics.** `query_prometheus` (instant first, then short range) on the
signal table below, restricted to the labels/metric names you verified in Step 0. If
`media_node_id` exists, localize per node; otherwise per `instance` / `node_id`. A series
that **disappeared or reset** is itself the signal (an SFU crash / restart / node loss).
**Before blaming the network:** when loss/jitter/RTT explode for **every participant at the
same instant**, check compute first — `go_sched_gomaxprocs_threads` (a step-down = quota
cut, not a box that shrank), `process_cpu_seconds_total` vs demand (flat-and-low = throttled,
not idle), and any cgroup/limit indicators. A synchronized collapse with a CPU step-down is
CPU starvation, not shaping.

**3 — Pivot to logs.** For the containers in your map: `list_loki_label_values`
(container first), then `query_loki_logs` scoped `{container="…"}` with a line filter
`|~ "(?i)…"`, `limit=20`, `startRfc3339=now-15m`. Optionally add `,level="error"` or
`,room_id="…"`, and group by `node_id` / `node_ip` when those labels exist.

**4 — Correlate.** Tie metric anomalies and log lines together by `room_id`, `node_id`,
and time windows.

**5 — Conclude.** State the **subsystem + the specific mechanism**, the supporting
evidence, and a **remediation that maps to a config / ops lever** verified against this
deployment (ports, limits, quota, image, topology). If metrics and logs are nominal, say
so — it may be a client-side issue, not a server fault. Optionally `generate_deeplink`
to return an Explore/panel URL.

## Signal table (hypotheses — confirm with your map before asserting)

Metrics are `livekit_*` in the metrics datasource you confirmed. Histograms, not gauges:
packet loss is `livekit_packet_loss_percent_sum` / `_count` / `_bucket`; quality is
`livekit_quality_score_bucket`. Split loss/jitter by `direction` before blaming a client.

| Symptom | Metric signal | Log signal (Loki) | Likely lever |
|---|---|---|---|
| **No media though people join (ICE/UDP)** | `livekit_participant_total` > 0 but `rate(livekit_packet_bytes[1m])` ≈ 0 | `{container="openvidu"} \|~ "(?i)ice\|candidate\|dtls"` → "Failed to ping without candidate pairs", DTLS `context deadline exceeded` | firewall/security-group blocking the RTC UDP/TCP range (defaults: UDP 50000–60000, TURN 443, ICE-TCP 7881); check the `rtc` config |
| **Congestion / one-way loss** | loss/jitter/RTT up on **one** `direction`; quality score down; participants stable; CPU not pinned | quality/NACK/PLI drops, no ICE failures | host/path impairment (`tc` shaping, uplink/host), **not** the subscriber's Wi-Fi (would not hit every subscriber at once) |
| **SFU CPU starvation (looks like congestion)** | loss on the **incoming** direction climbs hard (10–40%) while RTT (100s of ms) and jitter (100 ms+) explode **on every stream at once**; rooms stay up; quality score slides; no ICE failures; CPU **flatlines at a fixed fraction**, not "high and varying". **Decisive probe: `go_sched_gomaxprocs_threads` (GOMAXPROCS).** A **step-down in the middle of the incident** (e.g. 16→2 at the exact moment quality collapsed) = the CPU **quota/allocation was cut** (config/cgroup change) — restore it, don't resize the box. A CPU flat at a low fraction **from the start** with no step = genuinely undersized. Rule: **shaping degrades the outgoing path first (F2); starvation collapses the incoming path** (the SFU can't drain what arrives) with the loss spike landing on `direction="incoming"` while outgoing stays clean | SFU busy; no "connection is not possible" flood; no NAT errors; no "not enough CPU" egress errors | quota cut → restore it (compose/cgroup/orchestrator changed something at that instant); truly undersized → more compute; **not** a network problem |
| **SFU crash then recovery / node loss** | all `livekit_*` series drop or reset at one instant, then climb again; on multi-node a `media_node_id` / `instance` series may vanish with a participant step-down | `{container="openvidu"}` stops mid-line, then a fresh startup banner; Pro dereg: `\|~ "(?i)dead\|unregist\|remove.*node"` | already recovered; find why it died (OOM, restart, deregistration) |
| **Capacity / overload (fleet)** | per-`media_node_id` `livekit_participant_total` plateaus; `histogram_quantile` on `livekit_quality_score_bucket` drops; loss climbs | quality/drop warnings per node | add media nodes / reduce load |
| **Redis down (coordination)** | SFU metrics freeze (stop advancing); no new rooms | every service: `connection refused` on the Redis address in their config logs — an active reject means the process is down, not a timeout | start Redis; existing media keeps flowing |
| **Mongo down (state only)** | calls and metrics look healthy | `{container=~"openvidu.*\|meet.*\|dashboard"} \|~ "(?i)mongo"` connection errors; the `mongo` log dies out | restart MongoDB — the media plane does not need it |
| **Ingress RTMP/WHIP failing** | no ingress panels / no `livekit_ingress_*` (confirm in Step 0) | `{container="ingress"} \|~ "(?i)rtmp\|whip\|streamKey\|ingress does not exist"` — a bad key is a **client** config issue | fix the stream key / create the ingress via the API first; the pipeline can be fine |
| **Recordings fail mid-way (OOM/killed)** | no egress metrics (verify in Step 0); irrelevant otherwise | `{container="egress"} \|~ "(?i)killed\|oom\|panic\|gstreamer"` (`signal: killed`) | more memory / lower max concurrent recordings |
| **Recordings refused ("CPU exhausted")** | media metrics fine; no egress metrics | `{container="egress"}` `not enough cpu` / `can not accept request` `reason:"cpu"` `"not enough CPU"`. If **required CPUs ≫ available** (e.g. 100 vs 16) this is a **bad `cpu_cost` in `egress.yaml`**, not a hardware shortage — do **not** buy cores | restore the cost to a sane value / verify CPU entitlement |
| **Recordings not landing in storage** | silent on the metrics side | storage health: `{container="operator"} \|~ "(?i)minio"` → "Container 'minio' error"; or `{container="egress"} \|~ "(?i)upload\|s3\|minio\|denied"`; `minio` may disappear from the container label list | bring the storage back / check credentials and health |
| **License / evaluation cap (Pro)** | `livekit_participant_total` pinned at a low, stable ceiling; rooms cap | `{container=~"openvidu.*"} \|~ "(?i)eval\|license"` | install a valid license |
| **Nothing wrong on the server** | participants, bytes, loss, quality all nominal; no error burst in Loki | no new error pattern in the window | client-side issue; do not invent a cause |

## Guard / boundaries

- Read-only. Never call write/mutating tools. Never echo the service-account token.
- **Never assume — assert.** State that a metric, label, container, or datasource exists
  (or doesn't) only after seeing it (or its absence) in `list_prometheus_metric_names` /
  `list_prometheus_label_values` / `list_loki_label_values` / `list_datasources`.
  "X does not exist" is a finding only after a lookup, never before.
- Distinguish **server-side** from **client-side**; a nominal server is a valid outcome,
  not a failure to diagnose. Do not manufacture a cause.
- Metric **absence** (a reset series, a silent egress) is evidence too — report it.
- A loud error string can still mislead: "not enough CPU" against a config mismatch
  (`required: 100` / `available: 16` with a bad cost) is configuration, not hardware.
- **Shaping vs starvation look alike — separate them by direction and GOMAXPROCS.**
  Shaping (F2-style) degrades the **outgoing** path (loss/jitter/RTT up on `direction="outgoing"`,
  SFU idle). Starvation degrades the **incoming** path (the SFU can't drain what arrives) and
  shows a **step-down in `go_sched_gomaxprocs_threads`** at the collapse instant. Flat CPU
  alone is not a signal: an idle SFU has flat low CPU *and* clean metrics; a starved SFU has
  flat low CPU *and* a synchronized quality collapse.
- Never issue a query that can hang the session (see **Query budget**). A stuck Loki
  call is a failed investigation, not more evidence.