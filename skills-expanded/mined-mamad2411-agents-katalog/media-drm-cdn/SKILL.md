---
name: media-drm-cdn
description: DRM and CDN delivery specialist. Owns Widevine / FairPlay / PlayReady license flow, key rotation, tokenized URLs, multi-CDN, and QoE / rebuffering analysis. Auto-invoked for DRM integration, CDN config, or playback-quality investigation.
---

# Media DRM & CDN

DRM that fails silently looks like broken video. A CDN that routes poorly looks like
broken video. From the viewer's seat the two are indistinguishable — so license flow
and delivery both have to be instrumented and bulletproof.

## When to reach for this

- Integrating Widevine / FairPlay / PlayReady or standing up a license server
- Designing key rotation, tokenized / signed URLs, session binding, or geoblocking
- Choosing single vs multi-CDN, configuring origin shield, or planning failover
- Investigating startup time, rebuffer ratio, or bitrate-served regressions

## Principles

1. **Package once for all three key systems.** CMAF + CENC in `cbcs` mode: FairPlay
   requires `cbcs`, and modern Widevine and PlayReady (4.0+) accept it — one encrypted
   asset set, no `cenc`/`cbcs` dual storage. Verify the oldest device floor you must
   support before committing; legacy PlayReady clients are the usual blocker.
2. **The license request is on the startup hot path.** Every millisecond of license
   latency is time-to-first-frame. Cache license-server responses where policy allows,
   keep the server geographically close to viewers, and alert on P99 — not average.
3. **Key policy by content class.** Per-title keys for VOD; periodic rotation for
   live and linear; separate keys per quality tier when enforcing HD/UHD entitlement
   via security level (e.g. Widevine L1 for UHD).
4. **Multi-CDN for live and tentpoles; single CDN with an exit plan for VOD.**
   Multi-CDN pays for itself in failover and negotiating leverage, but only with
   midstream switching and per-CDN QoE measurement actually wired up.
5. **Geoblock and entitle at the edge.** Signed URLs/cookies with short TTLs, session
   binding, and edge geo rules. Manifest-level flags are advisory, not enforcement.
6. **QoE is the product metric.** Instrument startup time, rebuffer ratio, and
   bitrate served end-to-end, segmented by CDN, region, and device — that
   segmentation is what turns "video is slow" into a routable fix.

## Platform → key system

| Platform | Key system | Notes |
|---|---|---|
| Chrome, Firefox, Edge (desktop), Android | Widevine | L1 (hardware) needed for HD/UHD policies on Android |
| Safari, iOS, tvOS | FairPlay | HLS only; `cbcs` mandatory |
| Edge (legacy), Xbox, many smart TVs | PlayReady | check SL2000 vs SL3000 for UHD |
| Smart TVs (Tizen, webOS) | Widevine and/or PlayReady | per-model variance; test on real devices |

Token checklist: short TTL (minutes, not hours), bound to session or IP range,
scoped to the asset path, rotated signing secret, and a revocation story for leaked
URLs.

## Pitfalls

- ClearKey or unencrypted "temporary" paths surviving into production
- License server uncached and single-region — adds 300+ ms to startup for distant viewers
- Geoblocking enforced only via manifest filtering; segment URLs remain fetchable directly
- Signed-URL TTL longer than the viewing session needs, or unsigned segment URLs behind a signed manifest
- Multi-CDN contracts signed but no per-CDN QoE measurement or midstream switch logic — failover exists on paper only
- Key rotation on live streams without aligning rotation boundaries to segment boundaries — decode errors at the switch

---
*Related: `media-transcode` (CMAF packaging upstream of encryption), `media-player`
(EME key-system selection, QoE capture), `media-live` (multi-CDN failover),
`media-cms-workflow` (rights driving entitlement) · domain agent: `media-architect` ·
output/ADR format: `playbook-conventions`*
