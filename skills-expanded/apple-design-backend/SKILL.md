---
name: apple-design-backend
description: "Use when reasoning about how Apple delivers and serves its experiences — the observable web delivery/infra (multi-CDN, mzstatic image-transform URLs, image formats, HLS adaptive video, caching, HTTP/2-3) and the reverse-engineered, INFERRED server-side architecture (CloudKit, APNs, StoreKit, Sign in with Apple, Private Cloud Compute, iCloud sync). Part of the apple-design family. Keywords: apple cdn, akamai, mzstatic, image transform url, srcset picture, HLS m3u8, http3 quic, cache-control immutable, content-hash fingerprint, frame-sequence delivery, createImageBitmap, KTX texture, video scrub, cloudkit, APNs push, StoreKit, sign in with apple, private cloud compute, icloud sync, conflict resolution, backend, infrastructure, reverse-engineered, inferred architecture."
---

# Apple Design — Delivery & (Inferred) Backend

> ⚠️ **Reverse-engineered, not official.** Apple does not publish its server architecture. The **delivery** layer here is mostly `[observed]` (real headers, DNS, URL shapes); the **backend architecture** is largely `[inferred]`/`[speculative]`. Developer-facing services (CloudKit, APNs, StoreKit, Sign in with Apple, PCC) are `[documented]`. Treat inference as analysis, never ground truth — and never repeat it to a user as fact.

## When to use
- Designing apple.com-grade asset delivery (CDN, responsive images, adaptive video, caching).
- Understanding the public Apple services a client app integrates with.
- Reasoning about a privacy-first, sync-capable backend "the Apple way."

## Core rules
- **Delivery (observed):** multi-CDN edge; an **image-transform service** (mzstatic `{W}x{H}{modifier}-{quality}.{fmt}` URL params) → serve `<picture>`/`srcset` per device; **content-hashed immutable** assets with long `Cache-Control`; **HLS** multi-bitrate video; HTTP/2-3, Brotli.
- **Public services (documented):** CloudKit (public/private/shared DBs, CKRecord, sync), APNs (HTTP/2 + JWT), Sign in with Apple (OIDC, rotating client secret, email relay), StoreKit 2 (JWS receipts, Server API + Notifications V2), Private Cloud Compute (stateless, verifiable, OHTTP-routed).
- **Privacy-by-architecture:** on-device first, end-to-end encryption as a tier, server never trusts client claims, data residency (China/GDPR). Replicate the *invariants*, not the guesswork.

## References
| File | Use for |
|---|---|
| `references/web-delivery-infra.md` | `[observed]` CDN/image-transform/HLS/caching/HTTP — with replication recipes |
| `references/inferred-backend-architecture.md` | `[documented]` public services + `[inferred]` server topology (banner-led, every claim labeled) |

## Common mistakes
- **Presenting inference as fact** (the #1 anti-pattern of this skill).
- Giant unoptimized images, no edge cache, mutable cached URLs, single-bitrate video.
- Server trusting client claims; no e2e/offline path; ignoring data residency.

**Related:** the page that consumes these assets → apple-design-web; how current apple.com delivers scroll-hero media specifically (video-first reverse-spec, content-hash asset URLs, KTX/WebGL textures, frame-sequence `createImageBitmap` decode + sliding window, video `keyint=5` scrub encoding, asset-sourcing IP guardrails) → `apple-design-web/references/media-assets-and-delivery.md`.
