---
name: zimaboard-media-server
description: Building a low-power, high-performance media streaming server on ZimaBoard using Plex or Jellyfin.
---

# ZimaBoard Media Server (Plex / Jellyfin)

The ZimaBoard is an excellent candidate for a home media server. Unlike Raspberry Pis, its Intel x86 architecture natively supports Intel Quick Sync Video (QSV), enabling efficient hardware transcoding for 4K media without overwhelming the CPU.

## 1. Storage Configuration
Media servers require vast amounts of storage.
- Connect large 3.5" HDDs using the dual SATA ports and a Y-cable power adapter.
- In CasaOS, format the drives via the Storage Manager.
- Create a dedicated folder structure on the drive:
  - `/DATA/Media/Movies`
  - `/DATA/Media/TV Shows`

## 2. Installing the Media Server
You can install either Plex or Jellyfin directly from the CasaOS App Store.
1. Open the App Store and search for "Jellyfin" or "Plex".
2. Click **Install**.
3. **Important**: Before completing the setup, edit the container settings to map your storage drives.
   - Bind the Host path (e.g., `/DATA/Media/`) to the Container path (e.g., `/media`).

## 3. Enabling Hardware Transcoding
Hardware transcoding is critical for converting 4K video to lower resolutions on the fly for mobile devices or remote viewing.
1. In the CasaOS container settings, ensure the device `/dev/dri` is passed through to the container.
2. **Jellyfin Setup**:
   - Go to Dashboard > Playback.
   - Set Hardware Acceleration to `Intel QuickSync (QSV)` or `VAAPI`.
   - Enable decoding for H264, HEVC, and AV1 (if supported by your specific ZimaBoard model).
3. **Plex Setup**:
   - Go to Settings > Transcoder.
   - Check "Use hardware acceleration when available". *(Note: Plex requires a Plex Pass subscription for hardware transcoding).*

## 4. Performance Monitoring
- Transcoding operations should barely impact CPU utilization. Check the CasaOS CPU widget while a movie is transcoding. If the CPU is pegged at 100%, hardware acceleration is not configured correctly.
- The ZimaBoard's passive cooling means it will remain completely silent, even during heavy streaming sessions.
