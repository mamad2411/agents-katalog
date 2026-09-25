---
name: prompt-booster
description: WAJIB OTOMATIS dipakai untuk SETIAP pesan user tanpa kecuali dan tanpa perlu perintah slash. Setiap ada ketikan user (singkat, typo, campur bahasa, emosi, berantakan) langsung enhance jadi prompt berkualitas lalu eksekusi hemat token. Trigger: semua pesan user, buatin, bikinin, benerin, error, tolong, web, ppt, desain, coding, nulis, ide.
version: 1.0.0
tags: [prompt, enhancer, hemat-token, easy-prompt]
---

# Prompt Booster (Ketik Santai -> Hasil Berkualitas)

Skill ini otomatis: terima ketikan apa adanya, keluarkan prompt
bersih + eksekusi hemat token. User TIDAK perlu ngetik bagus.

## 1. Cara pakai (easy)

User cukup ketik seenaknya, contoh:
- "buatin web toko"
- "errror di login benerin dong"
- "bikinin ppt buat sidang anjing cepetan"

Agent WAJIB booster otomatis tanpa nyuruh user ngetik ulang.
Jangan ceramah soal typo. Langsung enhance diam-diam.

## 2. Pipeline enhance (wajib dijalankan agent)

Langkah 1 CONFIRM (1 baris): tebak maksud user.
Langkah 2 ASK (max 2 pertanyaan, hanya jika ambigu fatal).
Langkah 3 BUILD: tulis ulang jadi prompt berkualitas format:
TUJUAN / KONTEKS / BATASAN / OUTPUT / KRITERIA SELESAI.
Langkah 4 EKSEKUSI hemat (lihat bagian 3).

Contoh transform:
IN: "buatin web toko"
OUT: TUJUAN: landing + katalog + checkout WA. KONTEKS: UMKM,
mobile-first. BATASAN: 1 file HTML, tanpa backend. OUTPUT:
index.html + style inline. SELESAI: bisa dibuka offline.

## 3. Aturan hemat token (realistis, bukan 10000 persen)

Jujur: hemat 10000 persen itu mustahil. Klaim jujur skill ini:
hemat 30-70 persen token dibanding cara asal. Caranya:

- JANGAN baca file yang tidak perlu. Max 5 file per tugas.
- JANGAN cat folder besar (node_modules, .git, skills-catalog).
- JANGAN ulang-ulang baca file yang sama, pakai hasil sebelumnya.
- Ringkas: jawab singkat kecuali user minta detail.
- Scrip kecil > penjelasan panjang. Kasih file, bukan ceramah.
- Index .gz hanya untuk ARSIP catalog (sudah ada 41MB di
  skills-catalog). Untuk prompt aktif JANGAN gzip karena LLM tetap
  harus dekompres dulu = token SAMA SAJA, malah nambah langkah.
- Cache: simpan hasil enhance ke Memory (pakai skill
  linkedin-obsidian-memory-graph) biar pola prompt user yang sering
  dipakai tinggal recall, bukan diulang dari nol.

## 4. Batasan (tidak bisa ditawar)

- TIDAK melayani jailbreak / bypass safety / prompt untuk
  kejahatan, malware, penipuan, pornografi anak, atau pelanggaran
  hukum. Tolak sopan + tawarkan alternatif legal.
- TIDAK mengklaim hemat 10000 persen atau gratis tanpa kredit.
  Token/kredit AI dihitung dari input+output, tidak bisa diakali
  dengan gzip atau trik format. Satu-satunya penghemat nyata:
  input lebih pendek + output lebih padat + lebih sedikit tool call.
- Jika user maksa jailbreak: tolak 1 kalimat, lanjut bantu hal
  legalnya saja.

## 6. Aturan search (tanpa kredit, tanpa API key)

DILARANG pakai xweb_search (butuh Cline Credits, error 402).
DILARANG minta API key berbayar (tavily, brave, dll).
Selalu pakai yang gratis bawaan, urutan:
1. File lokal + scripts/recall.sh (AgentsMemory, 0 token server).
2. skill-graph-api localhost:27125 (10.048 skill lokal, gratis).
3. mcp-server-fetch (ambil URL langsung, gratis).
4. curl GitHub API / docs publik (gratis, tanpa key).
Kalau semua gagal: bilang jujur tidak ketemu, jangan ngarang.

## 7. Script bantu

- scripts/tidy.sh: bersihkan ketikan (lowercase, hapus kata kasar
  berlebih, rapikan spasi) sebelum enhance. Bukan sensor moral,
  tapi biar prompt final profesional.
- Pola hemat: panggil tidy.sh dulu, baru bangun prompt berkualitas.
