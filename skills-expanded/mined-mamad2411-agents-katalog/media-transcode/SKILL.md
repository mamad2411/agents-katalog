---
name: media-transcode
description: Transcoding and packaging specialist. Owns ffmpeg pipelines, encoder tuning, bitrate ladders, per-title encoding, packaging (CMAF/HLS/DASH), and quality metrics (VMAF/PSNR). Auto-invoked for transcode / encode / package / QoE work.
---

# Media Transcode

Every percent of bitrate is money and buffering; every QC miss is a customer
complaint. Encoder tuning is a metric chase — quality targets and cost per minute,
not preset folklore.

## When to reach for this

- Building or reviewing ffmpeg / x264 / x265 / AV1 encode pipelines
- Designing a bitrate ladder, or moving from a fixed ladder to per-title encoding
- Packaging CMAF / HLS / DASH output, subtitle and audio track handling
- Setting quality gates (VMAF / PSNR / SSIM) or scaling encode throughput

## Principles

1. **VMAF-target ladders, not guessed bitrates.** Aim VMAF ≥ 93 on the top rung;
   space adjacent rungs ~6 VMAF points apart (about one just-noticeable
   difference). Rungs closer than that waste storage; gaps wider than that make ABR
   switches visible.
2. **CMAF-first packaging.** One fMP4 segment set, two manifests (HLS `.m3u8` +
   DASH `.mpd`). Encoding or storing separate TS and fMP4 outputs doubles cost for
   no quality gain.
3. **Fixed GOPs, aligned across rungs.** Same GOP length (typically 2 s) and
   scene-cut detection off on every rendition, so segment boundaries line up —
   required for clean ABR switching, ad stitching, and chunked parallel encode.
4. **Parallelize by GOP for throughput.** Split the mezzanine on GOP boundaries,
   encode chunks across workers, and concatenate — turns hours-long titles into
   minutes of wall-clock at scale.
5. **Auto-QC every asset.** Black-frame, silence, loudness (EBU R128 / -23 LUFS or
   the platform target), A/V sync drift, and VMAF spot-check — gated before the
   asset reaches `ready`, not after a viewer complaint.
6. **Track cost per output minute as a KPI.** Preset choice (x264 `slow` vs
   `veryslow`, x265/AV1 adoption) is a measured cost-vs-bitrate-savings decision,
   re-run when delivery volume or egress pricing changes.

## Starting ladder (H.264 VOD, 16:9 — per-title tunes from here)

| Rung | Resolution | Bitrate (kbps) | Target |
|---|---|---|---|
| 1 | 1920×1080 | 5000 | VMAF ≥ 93 |
| 2 | 1280×720 | 3000 | ~1 JND below rung 1 |
| 3 | 960×540 | 2000 | |
| 4 | 768×432 | 1100 | |
| 5 | 640×360 | 700 | |
| 6 | 480×270 | 365 | floor — startup / worst networks |

Per-title encoding moves these per asset: animation hits VMAF 93 far below 5000 kbps;
high-motion sport may need more or a 1440p/UHD extension. Worked ffmpeg encode,
VMAF-measurement, and Shaka Packager commands are in
[`references/encoding-ladder.md`](references/encoding-ladder.md).

## Pitfalls

- Comparing codecs or presets at different resolutions/bitrates instead of equal-VMAF cost curves
- Scene-cut keyframes left on, silently breaking segment alignment between rungs
- VMAF computed without scaling the encode back to source resolution first (scores are not comparable otherwise)
- Audio forgotten in the ladder — one 128 kbps AAC stereo track muxed into every rung wastes nothing; missing language/AD tracks block launch
- Captions burned in during transcode instead of carried as sidecar WebVTT/TTML
- QC only on the top rung — the 270p rung is what the worst network actually plays

---
*Related: `media-drm-cdn` (encryption/packaging downstream), `media-live` (live
encoder constraints), `media-player` (how the ladder gets consumed),
`media-cms-workflow` (QC gates in the asset workflow) · domain agent:
`media-architect` · output/ADR format: `playbook-conventions`*
