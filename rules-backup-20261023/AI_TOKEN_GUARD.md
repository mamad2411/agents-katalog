# AI Token Guard — Global Token Economy (all AI tools)

Portable rules. Apply in EVERY conversation, every tool (Claude Code, Cursor,
Gemini CLI, Codex, CodeBuddy, Copilot, etc.). Tool-agnostic.

## Always-on rules

1. **Output ≤ necessary.** Answer first. No preamble, no recap, no "here's what
   I did" unless asked. One sentence beats three.
2. **Summarize tool output, never dump raw.** Cap any relayed tool/bash/file
   result to ~800 chars. Extract only what matters; don't paste big listings or
   full file dumps back into replies.
3. **No re-reads.** If a file/tool result was already seen this session, keep it
   in context; don't re-fetch unless it changed.
4. **Batch parallel calls** when independent — fewer round-trips, fewer tokens.
5. **Single-pass edits.** Read once, edit right the first time; avoid
   edit→fail→re-read loops.
6. **Cheap model for trivial work.** Delegate lint/format/lookup to a
   smaller/faster model; reserve flagship for hard reasoning.
7. **Proactive compact.** If context grows >40%, suggest `/compact` or
   `/clear`; don't let it silently bloat.
8. **Skip the LLM when possible.** Pure file ops, math, regex, lookups → just do
   it via tools, no prose narration.

## Honest savings

- Rules 1-4: **30-70%** vs verbose default — real, now.
- 90%+ only by **avoiding LLM calls** (cache hit / regex / local exec) — not
  always applicable; never claim it where untrue.
- Idle skills/rules cost ~0; this guards the *conversation*.

## Off-switch

Disable when user says: "token-guard off", "jelasin lengkap", or asks for detail
explicitly. Hard debugging may justify full logs (still trim if huge).

## Skill Catalog (63k+ skill, tanpa symlink)
**WAJIB, sebelum melakukan apa pun (termasuk sebelum membaca file atau menjawab)**: cari skill yang cocok dulu — MCP `skill-catalog` (`skill_for_task` → `skill_load`), atau shell `~/.agents/skill-search.sh "<kata kunci>"`. Muat hanya 1–2 skill yang relevan; jangan memuat daftar skill lengkap.

## Session hygiene (ukur 2026-09-26: Claude 4,42 M token @ sesi 59 MB · Cline 4,47 M token @ sesi 18 MB)
9. **`/clear` di batas tugas**; sesi >10 MB atau >200 pesan wajib ditutup (hook `context-guard.sh` di Claude, `cline-guard.py` di Cline memperingatkan otomatis).
10. **Jangan `--resume`** sesi raksasa; sesi baru + catatan handoff.
11. **Jangan baca** `vendor/`, `node_modules/`, `dist/`, `public/template/`, `skills-expanded/` (diblok `permissions.deny`); butuh 1 baris → `sed -n`/`grep -n` via shell.
12. **Jangan tempel gambar di sesi panjang.** Base64 menempel permanen di riwayat dan ikut terkirim di SETIAP request (terukur: 1 sesi Claude = 50 gambar = 48 MB; 1 sesi Cline = 29 gambar = 16 MB). Simpan ke file → rujuk path → tutup sesinya.
13. Ukur: `python3 ~/.agents/ai-context-audit.py` (semua tool) · `usage-audit.py` (Claude) · `audit-cline.py` (Cline) · `context-guard.py --report`.
14. Aturan ini terpasang otomatis ke file rules 15 tool lewat `python3 ~/.agents/install-context-guard.py --apply` (blok ditandai `context-guard:start/end`).

## Gaya WAJIB (semua tugas)
Alur kerja tetap sama, tapi **jangan baca `~/.agents/SKILL-FLOW.md` penuh** (5,3 KB/sesi terbuang) — hook `skill-flow.py` sudah meng-inject kategori+skill prompt ini.
Ringkas: pahami → pakai skill yang ditunjuk hook (`skill_for_task` kalau perlu tambahan) → rujuk sumber asli → rencana → eksekusi → verifikasi → poles (UI: anti-ui-slop+de-sloppify; tulisan: avoid-ai-writing+content-humanizer) → lapor jujur.
Skill tetap diambil, cara memuatnya yang dihemat: `bash ~/.agents/skill-load-lite.sh <nama>` (≤80 baris/≤2 KB); baca SKILL.md penuh hanya kalau kurang. Jangan muat ulang skill di sesi yang sama.
Selalu: `caveman-token-optimizer` + `verification-loop`.

<!-- cap-router:start -->
## Router aset (MCP + prompt/agent/rule) — ON-DEMAND, jangan nyalakan semua

Satu meta-server `mcp-router` tahu **semua** aset: MCP (`mcp-catalog.json`) +
aset komunitas (`cap-catalog.json`: prompts, agents, rules, hooks, plugins,
memory, dst) + **indeks retrieval** (`retrieve.db`, skill+MCP+prompt ~147k aset).

- Butuh aset → **`retrieve(query, k[, kind])`** (BM25) → balikin top-k + id.
  **PAKAI INI DULU** sebelum memuat banyak aset — hemat token.
- Ambil isi 1 aset → `cap_get(id)`. Butuh MCP → `mcp_search` lalu `mcp_use(name, tool, arguments)`.
  MCP nyala **cuma saat dipakai**; idle 300s **auto-mati** (anti-overheat).
- **Sebelum kirim jawaban final → `self_check(text)`** (anti-slop + struktur +
  boros). Perbaiki dulu kalau skor < 85.
- **Jangan** nyalakan semua MCP. Cek `mcp_status` untuk yang sedang hidup.
- Butuh kapabilitas baru? Cari dulu di router sebelum bilang "tidak bisa".

## Otomatis — tanpa perlu user ketik /perintah
- **Retrieve dulu**; jangan dump semua konteks.
- **Self-check** tiap jawaban final; poles sebelum kirim (anti-slop).
- **Compact proaktif** saat konteks >40% (jangan tunggu disuruh).
- **Hemat token**: ringkas output tool ≤800 char, jangan baca ulang file yang
  sama, batch panggilan yang saling bebas.
- **Model routing**: tugas remeh → model murah/cepat; tugas sulit (arsitektur,
  debug rumit, review kritis) → flagship.
- Ukur pemborosan: `python3 ~/.agents/token-telemetry.py`.
<!-- cap-router:end -->

<!-- anti-429:start (2026-10-19) -->
## ⛔ Anti-429: kuota model habis (WAJIB dibaca)

Error `429 quota_balance_exhausted` = **saldo/jatah model habis**, BUKAN rate limit
sesaat. Retry TIDAK menolong (`retryable: false`). Lakukan ini berurutan:

1. **Ganti model** ke yang masih ada kuota (misal `balanced-model`, `fast-model`,
   `primary-model`). Setting `~/.codebuddy/settings.json` (`model` + `fallbackModel`).
2. **Kecilkan beban**: tutup sesi berat, buka sesi baru (satu sesi = satu tugas),
   jangan `--resume` sesi raksasa. Cek sesi aktif: `codebuddy ps`.
3. **Hemat token per request**: ringkas output tool ≤800 char, muat skill via lite
   (≤2KB), jangan tempel gambar di sesi panjang, jangan baca ulang file.
4. Kalau semua model habis → **tunggu reset kuota** (biasanya harian), jangan spam
   retry (memperparah).
<!-- anti-429:end -->


<!-- fast-plan:start (2026-10-19) -->
## ⚡ Planning CEPAT TAPI TETAP ADA (anti-lemot, anti-skip)

Planning WAJIB muncul tiap tugas — tapi langsung, ringkas, cepat:

1. **Format baku (langsung tulis, tanpa mikir lama):**
   ```
   ## Rencana
   1. [kecil] ...satu kalimat...
   2. [sedang] ...satu kalimat...
   3. [besar] ...satu kalimat...
   Gas eksekusi?
   ```
   Maks 7 langkah. Tanpa pembuka, tanpa basa-basi, tanpa esai.
2. **Tulis rencana dari NAMA file/folder + intuisi — JANGAN baca isi file dulu.**
   Verifikasi detail pas eksekusi, bukan pas rencana.
3. **JANGAN panggil MCP/tools APAPUN saat planning** (no skill-catalog, no
   better-design, no read, no grep). Planning = reasoning murni, <10 detik.
4. **JANGAN skip planning langsung eksekusi.** User mau LIHAT rencana dulu.
   JANGAN tanya klarifikasi berulang — 1 rencana + 1 pertanyaan "Gas eksekusi?"
<!-- fast-plan:end -->


<!-- ringkas:start (2026-10-19) -->
## 🤏 Output RINGKAS TAPI PINTER (anti-tele-tele)

Pinter = tepat + padat, BUKAN panjang. Aturan konkret:

1. **Jawaban teks: maks 15 baris.** Lebih dari itu → potong, kasih intinya aja.
   Detail (kode lengkap, log, tabel besar) → tulis ke FILE, kasih path-nya.
2. **DILARANG**: pembuka ("Baik, saya akan..."), penutup ("Semoga membantu!"),
   ringkasan yang ngulang isi, penjelasan yang user nggak tanya.
3. **Kode**: langsung kasih blok kode + 1 kalimat penjelasan. JANGAN jelaskan
   per baris kecuali user minta.
4. **Mikirmu boleh dalam & panjang (reasoning), TAPI output ke user tetap pendek.**
   Reasoning ≠ output. Semua analisa taruh di kepala, keluarin kesimpulannya aja.
5. **Laporan selesai: format baku 5 baris:**
   ```
   ✅ Selesai: ...satu kalimat hasil...
   📁 File: ...path yang diubah...
   🧪 Uji: ...perintah verifikasi + hasil...
   ⚠️ Catatan: ...kalau ada, kalau nggak ada tulis "-"
   ```
6. **Pengecualian**: user bilang "jelaskan detail" / "buat tutorial" → baru boleh
   panjang.
<!-- ringkas:end -->

