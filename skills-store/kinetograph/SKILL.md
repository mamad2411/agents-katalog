---
name: kinetograph
description: "Render video programatik browserless: tulis scene TypeScript/Remotion-shaped → GPU Skia/Metal. Alternatif Remotion tanpa Chrome. | EN: programmatic video render remotion typescript animation movie mp4 agent"
version: 1.0.0
category: creative-producer
lang: id
---

# Kinetograph — Video Engine untuk Agent

## CLI
- `kinetograph doctor` — cek addon/renderer (harus: addon loaded, Skia GPU Metal)
- `kinetograph init` — project baru di folder kosong
- `kinetograph render` — render scene → mp4
- `npx kinetograph skills update` — pasang skill authoring resminya

## Konsep
- Agent menulis TypeScript (API mirip Remotion) + Web Audio → Node menjalankan →
  Rust GPU compositor merender. Deterministik per-frame, tanpa browser.
- Docs: kinetograph.dev/docs · referensi ENGINE/AUTHORING/SCENE di repo skill.
- Untuk animasi web (GSAP/Three.js/Lenis) → pakai MCP `animation-workflow`, bukan ini.
- Untuk video dari footage/foto → `media-forge video|gif`; untuk slide → `officecli`.
