---
name: validasi-konten
description: Validate quiz content quality from two POVs — Guru TKJ (curriculum alignment, technical accuracy, Bloom taxonomy, distractor-as-real-misconception, indicator coverage) and Siswa TKJ (term familiarity, lab/real-world relatability, cognitive load, engagement, mental navigation) — plus a cross-POV Content Coherence check that ensures image, description, question, and options stay on one topic (catches "image about X but question about Y" disconnects). Operates on cli/content/data/prod/chapter-*.json. Produces a machine-readable JSON report at .claude/skills/validasi-konten/reports/latest.json with per-question dimension scores (0-2) and aggregate approval percentage. Use this skill when the user asks to validate, validasi, cek konten, audit kebenaran materi, periksa kelayakan soal, sudut pandang guru TKJ, sudut pandang siswa, akurasi teknis, sesuai kurikulum, taksonomi Bloom, miskonsepsi siswa, kesinkronan antar elemen soal, alur kerangka soal, atau apakah istilah sudah familiar buat anak SMK TKJ. Different from refine-quiz-questions: refine = cara penulisan (PUEBI/SPOK/feel); validasi-konten = kebenaran, kelayakan, & koherensi konten untuk audiens. Read-only by default; never edits chapter files. Never touches pretest.json, achievements.json, image-assignments.json, upload-manifest.json, or studyMaterial field.
user-invocable: true
---

# Validasi Konten — Two-POV Audit

A read-only auditor that scores each quiz question through two lenses simultaneously: a TKJ teacher checking pedagogical/technical correctness, and a TKJ student checking whether the question is actually fair, familiar, and engaging for them. The output is a structured JSON report consumable by humans and by the `/loop-validate-refine` orchestrator.

## Scope

| Aspect | Detail |
|--------|--------|
| Reads | `cli/content/data/prod/chapter-*.json`, `image-assignments.json` |
| Writes | `.claude/skills/validasi-konten/reports/latest.json` (and timestamped copy) |
| Never edits | Any chapter content. Validation is read-only. To apply fixes, hand off to `refine-quiz-questions`. |
| Never touches | `pretest.json`, `achievements.json`, `upload-manifest.json`, `studyMaterial` field |
| Difference vs refine | refine = penulisan (bahasa, struktur, voice); validasi = kebenaran & kelayakan untuk audiens |

## Files at a glance

| Resource | Purpose | Read it... |
|----------|---------|------------|
| `references/quick-card.md` | Rubric utama: 10 dimensi + skor 0-2 + tabel miskonsepsi umum | Always — primary reference |
| `references/deep/kurikulum-smk-tkj.md` | CP/ATP SMK TKJ untuk "Media dan Jaringan Telekomunikasi" — pemetaan ke chapter/level | Hanya saat menilai G1 (curriculum alignment) borderline |
| `references/deep/miskonsepsi-tkj.md` | Daftar miskonsepsi umum siswa TKJ per topik (TCP/IP, WLAN, IP addressing, dll.) | Hanya saat menilai G4 (distractor as real misconception) borderline |
| `scripts/prescan.py` | Pre-compute mechanical signals (term first-occurrence, sentence length, distinct concepts per level) | Phase 2 opening |
| `reports/latest.json` | Output report — overwritten setiap run; juga ditulis sebagai `<timestamp>.json` untuk history | Phase 4 |

## The 11 dimensions

Each question scored on **11 dimensions, 0-2 each**. Per-question max = 22. Approval % = `(score / 22) * 100`. Dimension definitions and 0/1/2 anchors are in `references/quick-card.md`.

### POV Guru TKJ (Ahli Materi)

| Code | Dimension | What it asks |
|------|-----------|--------------|
| **G1** | Curriculum Alignment | Apakah konsep yang diuji termasuk elemen CP "Media dan jaringan telekomunikasi" pada mata pelajaran "Dasar-Dasar Teknik Jaringan Komputer dan Telekomunikasi" (Fase E SMK TKJ)? |
| **G2** | Technical Accuracy | Apakah pernyataan & kunci jawaban benar secara teknis (definisi, fungsi, standar terbaru)? |
| **G3** | Bloom Level Match | Apakah level kognitif soal (C1-C4) sesuai dengan `difficulty` level (easy/medium/hard)? |
| **G4** | Distractor as Real Misconception | Apakah tiap distraktor mencerminkan miskonsepsi nyata siswa, bukan asal salah? |
| **G5** | Indicator Coverage | Dalam satu level, apakah soal-soal menyentuh aspek konsep yang beragam, atau menumpuk di satu sudut saja? |

### POV Siswa TKJ (Penjelajah)

| Code | Dimension | What it asks |
|------|-----------|--------------|
| **S1** | Term Familiarity | Apakah semua istilah teknis di soal sudah pernah muncul di `studyMaterial` chapter ini atau sebelumnya? |
| **S2** | Real-world Relatability | Apakah skenario soal terhubung dengan dunia siswa (Wi-Fi sekolah, warnet, HP, lab, kabel LAN)? |
| **S3** | Cognitive Load | Apakah panjang & jumlah informasi baru per soal masih masuk akal (≤2 istilah baru, kalimat ≤20 kata)? |
| **S4** | Engagement | Apakah konteks deskripsi membuat siswa penasaran, atau terasa seperti soal ujian biasa? |
| **S5** | Mental Navigation Clarity | Setelah baca deskripsi+pertanyaan, apakah siswa tahu jenis jawaban yang dicari, atau bingung? |

### Cross-POV — Content Coherence (C)

| Code | Dimension | What it asks |
|------|-----------|--------------|
| **C1** | Content Coherence | Apakah `image (jika ada) → description → question → opsi` semua membahas satu konsep yang sama, tanpa drift topik atau loncat istilah? Catches kasus seperti "gambar three-way handshake tapi pertanyaan tiba-tiba tentang IP routing", atau "deskripsi pakai istilah Wi-Fi tapi pertanyaan loncat ke standar 802.11 tanpa jembatan". |

## Non-scored flags

Beberapa concern dicatat ke report **tanpa memengaruhi approval %**. Ini adalah informasi untuk human reviewer, bukan target perbaikan otomatis.

| Flag | Kondisi | Kenapa tidak di-skor |
|------|---------|----------------------|
| `image_in_english` | `imageLink != null` pada satu soal | Gambar saat ini dirender dengan label bahasa Inggris. Mengganti gambar ada di luar scope refine (refine tidak menyentuh aset gambar). Cukup catat sebagai utang teknis untuk pipeline image-asset terpisah. |

Flag muncul di field `flags[]` di tiap soal. Tidak masuk ke `flagged_for_refine` (karena refine tidak bisa fix-nya).

## Phases

### Phase 1 — Plan

1. Read each `chapter-*.json` in scope and `image-assignments.json` once.
2. Print a scope summary: chapters, levels, total questions.
3. **If the user gave explicit scope** ("Penuh", "chapter 2", "level 3"), proceed. Only ask if ambiguous.

### Phase 2 — Prescan + Score

**Step 2a — Run prescan**:

```bash
python .claude/skills/validasi-konten/scripts/prescan.py --json > /tmp/validasi-prescan.json
```

Prescan emits mechanical signals only:
- `term_first_occurrence`: per chapter, kata teknis yang muncul pertama kali di soal mana (signal untuk S1)
- `sentence_lengths`: panjang rata-rata kalimat per soal (signal untuk S3)
- `distinct_concepts_per_level`: jumlah konsep berbeda yang disinggung (signal untuk G5)
- `option_register_variance`: panjang & register opsi per soal (signal untuk G4)

Treat prescan output as input data for your scoring, not as findings themselves.

**Step 2b — LLM scoring per question**.

For each question, assign `0/1/2` to each of the 11 dimensions. Use the rubric in `references/quick-card.md`. Anchors:

- **0** — fail: hard problem, soal sebaiknya direvisi
- **1** — partial: ada concern tapi soal masih layak; perlu penghalusan
- **2** — pass: tidak ada concern di dimensi ini

Borderline (G1/G4) → consult `references/deep/`. Borderline (S1/S2) → re-check prescan signals. Borderline (C1) → cek apakah image filename, description hook, question stem, dan opsi semua merujuk ke konsep yang sama; satu disconnect → 1, dua atau lebih → 0.

**Step 2c — Aggregate**.

```
question_score = sum(11 dimensions) / 22 * 100
level_score    = mean of question_scores in level
chapter_score  = mean of level_scores
overall_score  = mean of chapter_scores
```

### Phase 3 — Write report

Write to `.claude/skills/validasi-konten/reports/latest.json` AND `.claude/skills/validasi-konten/reports/<YYYYMMDD-HHMM>.json` with this exact schema:

```json
{
  "schema_version": 1,
  "generated_at": "2026-04-26T10:30:00",
  "scope": ["chapter-1-tcp-ip.json", "chapter-2-wlan.json"],
  "approval_pct": 87.5,
  "threshold": 90,
  "passed": false,
  "summary": {
    "total_questions": 50,
    "questions_below_threshold": 12,
    "key_check_count": 2,
    "flag_counts": {
      "image_in_english": 14
    },
    "by_dimension_avg": {
      "G1": 1.9, "G2": 1.7, "G3": 1.8, "G4": 1.4, "G5": 1.6,
      "S1": 1.5, "S2": 1.3, "S3": 1.7, "S4": 1.2, "S5": 1.8,
      "C1": 1.6
    }
  },
  "chapters": [
    {
      "file": "chapter-1-tcp-ip.json",
      "score_pct": 89.0,
      "levels": [
        {
          "level": 1,
          "score_pct": 92.0,
          "questions": [
            {
              "qidx": 0,
              "question_preview": "Kepanjangan TCP/IP adalah...",
              "score_pct": 95.0,
              "scores": {
                "G1": 2, "G2": 2, "G3": 2, "G4": 2, "G5": 2,
                "S1": 2, "S2": 1, "S3": 2, "S4": 2, "S5": 2,
                "C1": 2
              },
              "concerns": [
                {"dim": "S2", "note": "Konteks belum menyentuh kehidupan siswa — masih definisi murni."}
              ],
              "flags": [],
              "key_check": false
            }
          ]
        }
      ]
    }
  ],
  "flagged_for_refine": [
    {
      "file": "chapter-2-wlan.json",
      "level": 2,
      "qidx": 3,
      "score_pct": 65.0,
      "failed_dims": ["G4", "S1", "S4"],
      "suggestion_hint": "Distractor B & D bukan miskonsepsi nyata; istilah 'beamforming' belum diperkenalkan; deskripsi flat."
    }
  ],
  "key_checks": [
    {
      "file": "chapter-1-tcp-ip.json",
      "level": 3,
      "qidx": 2,
      "issue": "G2 — pernyataan tentang TTL keliru: TTL bukan time-to-live dalam detik tapi hop count."
    }
  ]
}
```

**Critical**: `approval_pct`, `passed`, and `flagged_for_refine` are the fields the loop reads. Never omit them.

### Phase 4 — Human-readable summary

After writing the report, print a Markdown summary:

```markdown
# Validasi Konten — Report

**Approval**: 87.5% (threshold 90%) → ❌ belum lulus
**Total soal**: 50 | **Di bawah threshold**: 12 | **KEY-CHECK**: 2

## Per dimensi (rata-rata 0-2)
| G1 | G2 | G3 | G4 | G5 | S1 | S2 | S3 | S4 | S5 |
|----|----|----|----|----|----|----|----|----|----|
| 1.9| 1.7| 1.8| 1.4| 1.6| 1.5| 1.3| 1.7| 1.2| 1.8|

## Soal di bawah threshold (top 5)
- chapter-2-wlan.json L2 Q3 — 65% — fail: G4, S1, S4 — distraktor non-miskonsepsi + istilah baru + deskripsi flat
- ...

## KEY-CHECK (perlu keputusan manual)
- chapter-1-tcp-ip.json L3 Q2 — pernyataan TTL teknis keliru

## Catatan tambahan (non-skor)
- 14 soal masih memakai gambar berlabel Bahasa Inggris (`image_in_english`) — di luar scope refine, perlu pipeline image-asset terpisah

Report tersimpan: `.claude/skills/validasi-konten/reports/latest.json`
```

**Stop here**. Do not invoke refine. Validasi-konten is read-only — fixes are a separate session via `refine-quiz-questions` or via `/loop-validate-refine`.

## Modes

- **Default**: Phase 1-4 above (read-only audit + report).
- **`--loop-mode`**: invoked by `/loop-validate-refine`. Skip Phase 4 prose summary; just write the JSON report and print a one-line confirmation `validasi-konten: report written, approval=XX.X%, passed=true|false`. The orchestrator parses this line.

When the user prompt includes the literal string `loop-mode`, run in loop-mode.

## Output discipline

- Indonesian for human-facing text; preserve technical English terms verbatim (TCP/IP, WLAN, SSID, dst.).
- Skor harus integer 0/1/2. No half-points, no overall judgments outside the rubric.
- `concerns` field menjelaskan WHY skor < 2, satu kalimat per concern.
- `suggestion_hint` di `flagged_for_refine` boleh menyebut rule code refine-quiz-questions (M3, V1, dst.) untuk handoff yang mulus.

## Common pitfalls

- **Treating refine concerns as validasi concerns**: PUEBI typo bukan urusan validasi. Fokus pada *isi*, bukan tata tulis. Hand off ke refine.
- **Scoring without reading studyMaterial**: untuk S1, kamu wajib cek `studyMaterial.content` chapter ini dan sebelumnya — istilah baru di soal yang BELUM ada di studyMaterial = S1 < 2.
- **Bloom mismatch undetected**: easy level (`difficulty: "easy"`) yang berisi soal C4 analisis = G3 fail. Gampang terlewat kalau cuma baca soalnya.
- **Auto-applying fixes**: skill ini tidak edit. Kalau tergoda untuk "sekalian benerin", stop — itu pekerjaan refine-quiz-questions.
- **Skewed sample for G5**: jangan menilai indicator coverage dari satu soal — selalu dari level penuh.
- **C1 vs refine K8 overlap**: refine-quiz-questions K8 cek "image keyword muncul di deskripsi" (mekanik). C1 jauh lebih luas — apakah image, description, question, opsi semua satu konsep secara substansi. Soal bisa lulus K8 (deskripsi sebut keyword image) tapi gagal C1 (pertanyaan loncat ke topik lain di akhir). Nilai C1 secara substansi, bukan pencocokan kata.
