---
name: media-engineer
description: Media Engineer Skill
category: backend
tags:
- backend
- media
---
## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Pipeline & Protocol Strategy

**BEFORE processing a single frame:**

1.  **Protocol Selection**
    - Live Streaming? WebRTC (Sub-second latency) or LL-HLS (2-5s latency).
    - VOD (On Demand)? HLS (Apple) and DASH (Everyone else).
    - **Rule:** Do not invent your own protocol. Use standards.

2.  **Adaptive Bitrate (ABR) Planning**
    - Define the "Ladder": 1080p, 720p, 480p, 360p.
    - **Cost/Quality Balance:** High bitrates = High CDN costs. Optimize CRF (Constant Rate Factor).
    - **Constraint:** What is the minimum bandwidth of your target user?

3.  **Storage & CDN Architecture**
    - Origin Store (S3/GCS) vs Edge Delivery (Cloudfront/Fastly).
    - **Caching:** Video segments are immutable. Cache them aggressively.
    - **Egress Costs:** Calculate this NOW. Video bandwidth is the #1 startup killer.

### Phase 2: Encoding & Packaging

**The heavy lifting:**

1.  **Transcoding Pipeline**
    - Use FFmpeg or cloud services (AWS MediaConvert/Mux).
    - **Container Formats:** fMP4 or TS?
    - **Audio:** AAC is standard, but check opus for low latency.

2.  **DRM & Content Security**
    - **Encryption:** ClearKey? Widevine (Android/Chrome)? FairPlay (Apple)? PlayReady (Windows)?
    - **Token Authentication:** Secure the CDN URLs so users can't hotlink your streams.

3.  **Player Integration (The Client)**
    - Don't build a player from scratch. Use ExoPlayer (Android), AVPlayer (iOS), or Video.js (Web).
    - **Hook up the Analytics:** You need to know when buffering happens.

### Phase 3: Playback Quality (QoE)

**Ensuring it plays smooth:**

1.  **Buffer Strategy**
    - How much to buffer before starting? (Fast start vs Stability).
    - **Re-buffering Ratio:** Keep this under 1%.
    - **Startup Time:** Goal is < 2 seconds.

2.  **Seek & Scrub Performance**
    - Enable "Byte-Range Requests" for fast seeking.
    - Generate "Trick Play" tracks (thumbnails for scrubbing).

3.  **Cross-Device Testing**
    - Test on Low-End Androids (Hardware decoding limits).
    - Test on Cellular Networks (Packet loss).

### Phase 4: Monitoring & Scale

**Keeping the stream alive:**

1.  **QoE Metrics (Quality of Experience)**
    - Monitor: Bitrate switches (Are users downgrading?), Error rates, Startup time.
    - **Alerts:** "Rebuffering spike in region US-East."

2.  **Live Event Handling**
    - **Thundering Herd:** 100k users joining at once.
    - Pre-warm the Load Balancers/CDN.

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "I'll just serve the MP4 file directly." (Buffering nightmare).
- "We don't need DRM, nobody will steal this." (Copyright strike risk).
- "I'll run FFmpeg on the web server." (CPU explosion).
- "Latency of 30 seconds is fine." (Not for interactive apps).
- "I'll test it on my office Gigabit wifi." (Unrealistic).

**ALL of these mean: STOP. Return to Phase 1.**

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Protocol** | HLS/WebRTC, CDN | Architecture defined, costs estimated |
| **2. Encode** | FFmpeg, DRM, ABR | Multi-bitrate streams working |
| **3. Playback** | ExoPlayer/AVPlayer, Buffer | Fast startup, smooth seek |
| **4. Ops** | QoE Metrics, Scaling | <1% Rebuffer rate |

## 🛠️ Modern Media Stack (2026)

### Video Encoding
- **FFmpeg 7:** Universal encoder (H.264, H.265, AV1)
- **Cloud:** AWS MediaConvert, Mux, Cloudinary
- **Hardware:** NVENC (NVIDIA), QuickSync (Intel)
- **Codec Choice:** H.264 (compatibility), AV1 (efficiency, +30% savings)

### Streaming Protocols
- **LL-HLS:** Low-latency HLS (Apple), 2-5s latency
- **DASH:** Dynamic Adaptive Streaming (MPEG)
- **WebRTC:** Sub-second latency, peer-to-peer
- **RTMP:** Legacy push to server (OBS, streaming software)

### CDN & Storage
- **CDN:** Cloudflare Stream, AWS CloudFront, Fastly
- **Origin:** S3, GCS, Azure Blob
- **Edge Caching:** Aggressive (immutable segments)

### Player SDKs
- **Web:** Video.js, HLS.js, Shaka Player
- **iOS:** AVPlayer (native), VLCKit
- **Android:** ExoPlayer (Google), VLCPlayer

## 🤖 AI-Powered Media Processing (2026)

### AI Enhancement Tools
- **Background Removal:** Remove.bg API, Rembg (local)
- **Upscaling:** Topaz Video AI, Real-ESRGAN
- **Auto-Captioning:** OpenAI Whisper, AssemblyAI
- **Content Moderation:** OpenAI Moderation API, AWS Rekognition
- **Scene Detection:** PySceneDetect, FFmpeg scene filter

### Use Cases
- **Auto-generate subtitles:** Whisper API (99% accuracy)
- **Thumbnail selection:** ML picks best frame
- **Content safety:** Auto-flag NSFW content
- **Quality enhancement:** AI upscale 480p → 1080p

## 🌐 WebCodecs API (Browser-Native)

### When to Use
- **Browser video editors:** No FFmpeg download
- **Real-time effects:** Filters, overlays
- **Custom encoding:** Precise control

### Example
```javascript
const encoder = new VideoEncoder({
  output: (chunk) => { /* save encoded data */ },
  error: (e) => console.error(e)
});

encoder.configure({
  codec: 'vp9',
  width: 1920,
  height: 1080,
  bitrate: 2_000_000
});

// Encode frames
encoder.encode(videoFrame);
```

### Benefits
- **No server:** Encode in browser (privacy, cost)
- **Low latency:** 10x faster than WASM FFmpeg
- **Support:** Chrome 94+, Edge 94+, Safari 17+

## 📊 Quality of Experience (QoE) Metrics

### Critical Metrics
| Metric | Target | Why |
|--------|--------|-----|
| **Startup Time** | <2s | User drops off after 3s |
| **Rebuffer Rate** | <1% | Each rebuffer = 5% abandonment |
| **Bitrate Switches** | <3/min | Too many = poor ABR logic |
| **Error Rate** | <0.1% | Playback failures |

### Monitoring
- **Mux Data:** Video analytics platform
- **Datadog RUM:** Real user monitoring
- **Custom:** Send events to Amplitude/Mixpanel

### Alerts
- **Rebuffer spike:** >2% in last hour
- **Startup time:** p95 >3s
- **CDN errors:** >1% failure rate
