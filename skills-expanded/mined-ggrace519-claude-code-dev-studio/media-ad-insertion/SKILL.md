---
name: media-ad-insertion
description: Ad insertion — SSAI (server-side stitching), CSAI (client-side), VAST / VMAP / VPAID, SCTE-35 markers, ad-break pacing, viewability, and verification. Auto-invoked when designing ad pipelines, debugging stitch glitches, or improving fill / revenue.
---

# Media Ad Insertion

Ads are the revenue engine for AVOD/FAST — and the #1 source of viewer abandonment
when they glitch. The hard part is the seams: marker conditioning, decisioning,
stitching, and the QoE of every transition.

## When to reach for this

- Choosing or implementing SSAI vs CSAI for a surface, or wiring an ad server (GAM, FreeWheel, Magnite)
- Debugging stitch glitches: bitrate drops, init-segment reloads, black frames at break boundaries
- Conditioning SCTE-35 cue-out / cue-in markers through the encoder and origin manifest
- Wiring viewability (OMID), completion tracking, IVT filtering, or consent-aware decisioning

## Principles

1. **Match the ad to the content.** Same codec, same ladder rungs, same segment
   duration. Mismatches force init-segment reloads and visible bitrate drops at the
   stitch — the single biggest drop-off moment in ad-supported playback.
2. **Condition SCTE-35 upstream, not in the player.** Markers belong in the
   transcoder and the origin manifest. Players should see clean HLS/DASH with
   discontinuity tags, never raw cue messages.
3. **Keep ad-start latency under 200 ms.** Pre-fetch the next pod during content
   playback; resolve VAST in parallel with manifest generation. Latency over 500 ms
   is visible and painful.
4. **Verify every impression.** OMID-measured viewability, completion quartiles, and
   ad-start events. Without verification, revenue is guesswork and fraud is invisible.
5. **Design every branch a fallback.** Empty VAST, lost bid, creative 404 — each
   needs a deterministic outcome (house ad, slate, or immediate content resume).
   Never leave the viewer on black.
6. **Respect consent signals in the decisioning path.** The TCF v2 / GPP / CCPA
   string determines personalized vs contextual request — or no ad request at all in
   some jurisdictions. Encode this server-side in decisioning, not in the client.

## SSAI vs CSAI

| Factor | SSAI (manifest stitching) | CSAI (client SDK, e.g. IMA) |
|---|---|---|
| Ad blockers | Resistant — ads are in the stream | Blockable |
| CTV / FAST / linear | Default choice | SDK support uneven across TV OSes |
| Interactivity (click, companions) | Limited | Native VAST/VPAID support |
| Stitch QoE | Owned by you — bitrate-match or suffer | Player handles the transition |
| Per-session targeting | Needs per-session manifest + token flow | Built into the SDK request |
| Verification | Server beacons + client OMID bridge needed | OMID in-SDK, simpler |

Hybrid is common: SSAI for CTV/FAST, CSAI for web where the IMA SDK is solid.

## Pitfalls

- Ad creatives transcoded once at a single bitrate instead of the full content ladder
- Missing `EXT-X-DISCONTINUITY` / DASH period boundaries at stitch points — decoder stalls
- VAST resolution serialized after the break starts instead of pre-fetched
- Frequency caps and competitive separation enforced only in the ad server config, unverified in logs
- Consent handled client-side only, so server-side SSAI requests leak personalized signals
- No IVT filtering — fill rate looks great until the demand partner claws back revenue

---
*Related: `media-live` (SCTE-35 in live pipelines), `media-transcode` (ad creative
ladders), `media-player` (break-transition QoE), `media-drm-cdn` (tokenized ad
segments) · domain agent: `media-architect` · output/ADR format: `playbook-conventions`*
