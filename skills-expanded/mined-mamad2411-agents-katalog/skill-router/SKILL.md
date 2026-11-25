---
name: skill-router
description: WAJIB OTOMATIS dipakai tanpa slash untuk SETIAP pesan user. Router universal semua 3000+ skill: tebak maksud, cari skill cocok via graph-api + keyword, load max 2 skill, eksekusi. Trigger: semua pesan user.
version: 1.0.0
tags: [router, universal, auto]
---

# Skill Router (semua 3000+ skill, tanpa slash)

Aturan untuk agent, setiap pesan user:

1. Tebak maksud (1 baris, diam-diam).
2. Cari skill: scripts/route.sh "kata kunci" (graph-api 27125 +
   keyword folder skills/). Ambil max 2 skill paling cocok.
3. Baca SKILL.md skill itu (max 2 file), ikuti aturannya, eksekusi.
4. Jangan sebut nama skill ke user kecuali ditanya. User terima hasil.
5. Kalau tidak ada skill cocok: kerjakan langsung semampunya.

Batasan: max 2 skill per pesan. Max 5 file dibaca. Jangan load
katalog 3000 sekaligus (panas). Graph-api response cap 2000 chars.
