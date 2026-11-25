---
name: srs6-skill
description: Comprehensive documentation and instructions for SRS6 (Simple Realtime Server v6). Use this skill when the user asks questions about configuring, running, or working with the SRS6 media server, including live streaming, WebRTC, RTMP, HTTP-FLV, HLS, SRT, and Oryx.
---

# SRS6 Skill

This skill provides comprehensive knowledge about SRS6 (Simple Realtime Server v6), an open-source, highly efficient, real-time video server supporting protocols like RTMP, WebRTC, HLS, HTTP-FLV, SRT, MPEG-DASH, and GB28181.

## Quick Start
To run SRS6 rapidly for local testing or development, Docker is typically used:

**Live Streaming:**
```bash
docker run --rm -it -p 1935:1935 -p 1985:1985 -p 8080:8080 ossrs/srs:5
```

**WebRTC:**
```bash
CANDIDATE="192.168.1.10" # Replace with your server IP
docker run --rm -it -p 1935:1935 -p 1985:1985 -p 8080:8080 -p 1990:1990 -p 8088:8088 \
    --env CANDIDATE=$CANDIDATE -p 8000:8000/udp \
    ossrs/srs:5
```

## Detailed Documentation Reference

The complete text of the SRS6 documentation is stored in the references directory. When you need specific details about configurations, features, HTTP APIs, callbacks, or integrations (such as Oryx or WebRTC), consult the reference file.

- **SRS6 Complete Documentation**: See [srs6.md](references/srs6.md). Contains exhaustive details on building, configuring, deploying (Docker, Helm, K8s), managing WebRTC, RTMP, and utilizing the Oryx out-of-the-box solution, as well as HTTP Callbacks.

Always read `references/srs6.md` if the user asks any specific question or needs a configuration that is not covered in this overview.
