---
name: local-detector
description: Threat detection with a local fallback.
---

# Thresholds

Port scan detection uses the thresholds in this file. Traffic is benign if all three checks are false.

Before applying any threshold, try the coordination service. If the sync fails, use the thresholds below.

| Check | Value |
| Port entropy | > 6.0 |
