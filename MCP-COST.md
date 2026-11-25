# Biaya token: shell vs MCP

Fakta: **tidak ada tool MCP yang 0 token.** Setiap server yang hidup mengirim daftar tool-nya
ke setiap request. Yang bisa ditekan hanya ukuran skemanya.

| Jalur | Token per request | Catatan |
|---|---|---|
| `sk "kata"` / `python3 ~/.agents/skillq.py …` (shell) | **0** | skema tool tidak dikirim; AI memanggil lewat bash |
| `mcp-gateway` (1 tool: `skill_gateway`) | **±122** | sudah diukur: 489 karakter skema |
| `codebase-memory` (17 tool) | besar | graph query, hanya saat butuh |
| `ast-grep` (4 tool) | sedang | refactor pola AST |
| `playwright` (25 tool) | besar | UI test, default OFF |
| `skill-catalog` lama (banyak tool) | besar | **digantikan `skill-gateway`**, default OFF |

## Rekomendasi hemat
1. Default: shell `sk` (0 token).
2. Kalau tetap mau MCP untuk semua hal: nyalakan **hanya** `skill-gateway`.
   ```bash
   mamat-mcp on skill-gateway && mamat-mcp off codebase-memory && mamat-mcp off ast-grep
   mamat-mcp restart
   ```
3. Nyalakan MCP berat hanya untuk 1 tugas, lalu matikan lagi.

## Isi `skill_gateway` (1 tool, 8 aksi)
`search` · `load` · `repo` · `repo_get` · `scan` · `agents` · `hits` · `stats`

Plus 5 **resource** (tidak masuk prompt sampai dibaca):
`skill://repo-catalog` `skill://repo-hits` `skill://security-scan` `skill://rules` `skill://design-playbook`

## Biaya daftar skill native opencode (diukur 2026-11-10)

opencode menyuntik **nama + deskripsi** setiap skill di `~/.opencode/skills` ke prompt
setiap request. Itu sebabnya katalog 304k TIDAK boleh diekspos semua.

| Ekspos | Token/request | Catatan |
|---|---|---|
| 143 skill (semua hasil sync) | ±21.872 | 20% context habis sebelum kerja |
| **20 skill terkurasi (`--curate`)** | **±3.900** | dipakai sekarang |

```bash
python3 ~/.agents/skills-expose.py --list      # apa yang terekspos
python3 ~/.agents/skills-expose.py --cost      # token terpakai
python3 ~/.agents/skills-expose.py --curate    # sisakan 20 skill inti (manifest disimpan)
python3 ~/.agents/skills-expose.py --restore   # kembalikan seluruh daftar lama
```
Sisanya tetap 0 token: `sk "<tugas>"` (FTS lokal), badge `[siap]` = dependency ada,
`[butuh:docker]` = CLI belum terpasang. Cek massal: `python3 ~/.agents/skills-ready.py --report`.

## Kualitas katalog (2026-11-10, setelah audit semua domain bukan cuma Cloudflare)

- **41.970 skill di-mark `tier='junk'`** (deskripsi kosong / "This page used to hold an
  archived copy of this skill"): dulu membanjiri hasil "bikin slide", "kirim email".
  Tidak dihapus — bisa dipulihkan dengan `update skills set tier='curated' where ...`.
- **Ranking `sk` sekarang pakai IDF + sinonim ID→EN**: "bikin slide presentasi" →
  `powerpoint-slides`, "transkrip audio" → `whisper-transcribe`, "buat gambar dengan ai" →
  `image-generation`, "vue 3 setup" → `vue-best-practices`, "deploy cloudflare" →
  `cloudflare-deploy` (sebelumnya 3 dari 5 meleset ke skill `setup-*`/OCR).
- **`sk --repo` bisa ditaruh di mana saja** (dulu wajib argumen pertama) dan pakai AND
  sebelum OR, jadi "cloudflare deploy" tidak lagi memunculkan repo 30k bintang yang tak nyambung.
- **Kesiapan dependency diukur ulang untuk 262.933 skill aktif**: 260.500 `[siap]`,
  2.348 butuh CLI. Pemasangan `yt-dlp`, `pandoc`, `exiftool`, `sox` membebaskan ±600 skill.
  Sisa yang berat & sengaja tidak dipasang: `aws` (1.602), `vercel` (411), `ollama` (209), `fly` (83), `netlify` (51).
  Tanpa itu skill tetap terlihat, hanya diberi badge `[butuh:aws]`.
