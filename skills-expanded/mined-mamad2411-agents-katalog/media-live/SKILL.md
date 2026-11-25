---
name: media-live
description: Live-streaming pipeline — ingest (SRT / RTMP / RIST / WebRTC), transcoding, low-latency delivery (LL-HLS, LL-DASH, WebRTC), redundancy, failover. Auto-invoked when designing live pipelines, debugging glass-to-glass latency, or planning failover for tentpole events.
---

# Media Live

Live is unforgiving: every second of downtime is subscribers, sponsors, and
reputation, and there is no re-run. The pipeline — ingest, transcode, packaging,
delivery — matters exactly as much as the failover paths and the runbook the NOC
uses when it breaks mid-event.

## When to reach for this

- Designing a live pipeline: ingest protocol (SRT / RIST / RTMP / WebRTC-WHIP), transcoder, origin, CDN
- Debugging glass-to-glass latency or choosing LL-HLS / LL-DASH / WebRTC delivery
- Planning redundancy and failover — dual encoder, hot-hot origin, multi-CDN — for a tentpole event
- Building DVR / start-over / live-to-VOD clip-out, or the capacity plan for projected peak concurrents

## Principles

1. **Two redundant paths from day one.** Dual encoder, dual origin (hot-hot),
   multi-CDN. Retrofitting failover into a live path is a multi-week project you
   cannot do the month before a tentpole event.
2. **Pick the protocol per use-case, not globally.** WebRTC for sub-second
   interactivity (betting, watch-along); LL-HLS / LL-DASH with CMAF chunked transfer
   for 2–5 s broadcast-like delivery; standard HLS/DASH (~15–30 s with 4–6 s
   segments) where scale beats latency. Prefer SRT or RIST over RTMP for
   contribution — they recover loss, RTMP does not.
3. **GOP-align everything.** Encoder IDRs, segment boundaries, SCTE-35 ad markers —
   a fixed GOP (typically 2 s, scene-cut detection off) across all renditions.
   Misaligned GOPs cause stitch artifacts and DVR glitches that are brutal to debug
   mid-event.
4. **Synchronize redundant paths by PTS.** Hot-hot origins must emit identical
   segment numbering for the same input time; seamless player-level failover needs
   interchangeable segments — otherwise every switch is a rebuffer.
5. **Build the runbook with the NOC and rehearse it.** Alerts (encoder drop, origin
   5xx, CDN error spike), automated responses, manual escalation tree, and a
   break-glass dark path — exercised end-to-end at least once before any tentpole.
6. **Post-mortem every event.** Concurrent-viewer curve, rebuffer incidents, error
   waterfalls, per-CDN performance — fed into the next event's capacity plan, not a
   forgotten wiki page.

## Latency vs scale: delivery selection

| Delivery | Glass-to-glass | Audience scale | Use when |
|---|---|---|---|
| WebRTC | < 1 s | thousands–low hundreds of thousands | interactivity is the product |
| LL-HLS / LL-DASH | 2–5 s | millions (CDN-friendly) | "broadcast parity" sports / news |
| Standard HLS/DASH | ~15–30 s | effectively unbounded | latency secondary; cheapest, most robust |

## Tentpole pre-flight checklist

- [ ] Both encoder paths verified on real contribution links; standby takes over without operator action
- [ ] Origin failover and per-CDN switch tested with fault injection, not just configured
- [ ] CDN capacity reserved against *peak* concurrent projection (not average), per region
- [ ] DVR window sized and origin storage provisioned for the full event duration
- [ ] Rehearsal completed: encoder kill, origin 5xx flood, CDN degradation — each with timed recovery
- [ ] NOC staffed, escalation tree current, break-glass procedure printed (it works when dashboards don't)

## Pitfalls

- Redundant origins with divergent segment numbering — failover "works" but every viewer rebuffers
- Latency tuned by shrinking segments alone instead of CMAF chunked transfer — kills CDN cache efficiency
- DVR window promised in product UX longer than origin retention actually configured
- SCTE-35 markers inserted off GOP boundaries, breaking downstream ad stitching
- Capacity planned from a previous event's average concurrents, not this event's projected peak
- Runbook written but never rehearsed — the first execution is during the incident

---
*Related: `media-transcode` (encoder/ladder details), `media-drm-cdn` (multi-CDN,
key rotation on live), `media-ad-insertion` (SCTE-35 decisioning), `media-player`
(low-latency playback tuning) · domain agent: `media-architect` · output/ADR format:
`playbook-conventions`*
