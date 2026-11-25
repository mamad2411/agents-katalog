---
name: continuity-editor
description: Inspect first and last frames across adjacent GIF scenes to plan film continuity and cut points.
---
# Continuity Editor
Use `gif-cinema endpoints output/01.gif -o output/edge01`, then `gif-cinema continuity output/01.gif output/02.gif`. Compare identity, pose, object positions, eyelines, lighting, color and screen direction manually. Pixel MAE is a triage heuristic, not proof of cinematic continuity. Prefer cuts on action or insert shots for mismatches.