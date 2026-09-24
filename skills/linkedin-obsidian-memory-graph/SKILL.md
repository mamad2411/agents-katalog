---
name: linkedin-obsidian-memory-graph
description: WAJIB OTOMATIS dipakai tanpa perintah slash. Setiap user menyebut ingat, simpan, catat, lupa, linkedin, postingan, obsidian, note, ide, memori, kemarin, atau butuh konteks lama — langsung save/recall via vault ~/Documents/AgentsMemory. Fused LinkedIn + Obsidian + Memory, file-based zero daemon, ringan M1 8GB.
version: 2.0.0
tags: [linkedin, obsidian, memory, graph, lightweight]
related_skills: [linkedin-automation, obsidian-automation, unified-memory, memory-md-management]
---

# LinkedIn-Obsidian-Memory Graph (Cool-Laptop Edition)

> Prinsip: tidak ada daemon, tidak ada vector DB, tidak ada embedding lokal.
> Memory = file Markdown kecil + satu index .gz. Search = ripgrep (<50MB RAM).
> Graph = [[wikilinks]] Obsidian biasa. Laptop tetap adem, 0 proses background.

## 1. Jujur soal suhu 30C

M1 idle normal 35-45C. 30C hanya di ruangan AC + idle total. Yang skill
ini jamin: 0 proses background, recall < 50MB RAM, search < 0.3 detik.
Cek suhu: sudo powermetrics --samplers smc -n 1 | grep -i temp

## 2. Struktur Vault

Vault Obsidian = ~/Documents/AgentsMemory/ (buka folder ini di Obsidian):

- 00-Index.md (MOC utama, auto-update)
- LinkedIn/ (draft post, leads, analytics)
- Memory/ (satu file per fakta, max 5KB per file)
- Daily/ (daily notes auto-capture)
- .index.json.gz (index terkompresi, dibuat script)

10.000 memory = ~20MB. Index .gz 10.000 entri = ~300KB.

## 3. Format Memory (WAJIB)

Setiap file Memory/ dan LinkedIn/ pakai frontmatter:

id: YYYYMMDD-HHMMSS, created, tags, links: ["[[00-Index]]"],
score: 1.0, source: chat. Isi max 10 baris, atomic (1 file = 1 ide).
Selalu link balik ke [[00-Index]] + min 1 link ke note terkait.
LinkedIn draft WAJIB tag linkedin + link ke [[LinkedIn MOC]].

## 4. Workflow

SAVE: tulis 1 file baru + append 1 baris ke Daily. Jangan rebuild index
tiap save (max 1x/hari via make_index.sh).
RECALL: recall.sh keyword (zgrep index) -> rg fallback (max 20 hasil) ->
baca HANYA top-3 file. Dilarang cat seluruh vault.
LINKEDIN: ide -> LinkedIn/YYYY-MM-DD-slug.md tag draft. Struktur post:
hook, cerita, pelajaran, CTA, max 150 kata. Analytics 1 file per bulan,
update manual (jangan scraping tiap jam).
GRAPH: graph = wikilinks. 00-Index.md hanya daftar link (bukan embed).
Di Obsidian matikan plugin berat; Dataview query sempit FROM "LinkedIn".

## 5. Scripts

- scripts/save.sh "Judul" "tag1,tag2" "isi" (bikin memory)
- scripts/recall.sh "keyword" (zgrep index, rg fallback)
- scripts/make_index.sh (rebuild .index.json.gz + 00-Index.md)
- cron adem 1x/hari: 0 4 * * * .../scripts/make_index.sh

## 6. Hard rules anti-panas

Max baca 5 file per recall. Max tulis 3 file per save. Dilarang npm
install model embedding / jalan server (lancedb, qdrant, ollama).
Jangan gzip tiap note (Obsidian tidak baca .md.gz). Gz hanya untuk index.

## 8. Plugin berat on-demand (AI yang nyalakan, AI yang matikan)

Plugin BERAT (saat ini: Excalidraw) default OFF. Aturan untuk agent:

1. Saat user butuh gambar/diagram/mindmap: jalankan
   scripts/plugin.sh on obsidian-excalidraw-plugin, buat file
   .excalidraw.md yang diminta, lalu LANGSUNG
   scripts/plugin.sh off obsidian-excalidraw-plugin setelah selesai.
2. Jangan biarkan plugin berat ON lebih dari 1 tugas.
3. Beritahu user: "Excalidraw saya nyalakan bentar buat gambar ini,
   habis itu saya matikan lagi biar adem. Restart Obsidian biar aktif."
4. Batasan jujur: AI hanya bisa ubah file config (community-plugins.json).
   Yang benar-benar load/unload plugin = aplikasi Obsidian, dan itu
   butuh RESTART vault oleh user. Jadi alurnya: AI on -> user restart ->
   pakai -> AI off -> user restart. Tidak bisa live tanpa restart.

Buka Obsidian, Open folder ~/Documents/AgentsMemory. Aktifkan plugin:
Templates, Daily Notes, Graph. Jalankan make_index.sh sekali, lalu test
save.sh + recall.sh.
