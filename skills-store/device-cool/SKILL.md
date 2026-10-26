---
name: device-cool
description: WAJIB OTOMATIS dipakai tanpa slash saat user bilang panas, lemot, ngelag, kipas, RAM penuh, CPU tinggi, bersih, cache, atau minta dinginkan laptop. Menjalankan cek suhu + bersih cache aman + matikan plugin berat + lapor. Trigger: panas, lemot, cache, ram, cpu, kipas, dingin, bersih.
version: 1.0.0
tags: [cooldown, cache-cleaner, ram, cpu, obsidian-plugins]
---

# Device Cool (Anti-Panas M1 8GB)

Skill pasif + on-demand. Tidak ada daemon. Semua via script sekali jalan.

## Kapan jalan otomatis

User bilang panas/lemot/ngelag/kipas/RAM penuh/minta bersih/cache.
Agent langsung: cek -> bersih aman -> lapor singkat. Jangan ceramah.

## Scripts

- scripts/check.sh : suhu + RAM + CPU + top 10 proses + ukuran cache.
- scripts/plugin_audit.sh : daftar plugin Obsidian + tandai yang berat,
  matikan yang berat otomatis (default OFF: excalidraw, git).

## Aturan

Max baca 5 file. Jangan hapus folder vault/skills. Jangan kill proses
sistem (kernel, WindowServer). Tanya dulu sebelum kill browser/IDE.
Lapor selalu: suhu sebelum/sesudah, RAM bebas, space bebas.
