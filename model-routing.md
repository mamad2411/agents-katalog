# Model & Provider Routing — rencana pakai (bukan tebakan)

Tujuan: tugas murah jangan pakai model mahal, tugas berat jangan pakai model lemah,
kuota jangan habis karena salah pilih. Semua bisa dicek ulang dengan bukti.

## 1. Tier tugas → varian auto

| Tier | Varian | Dipakai untuk | Jangan untuk |
|---|---|---|---|
| cepat | `smart/auto/quick` | rename, format, docs pendek, tanya singkat, 1 file <50 baris | debug lintas file, arsitektur |
| murah | `smart/auto/cheap` | grep/sed massal, scan, inventaris file, ringkasan data | apa pun yang butuh nalar |
| koding | `smart/auto/coding` | UI, frontend/backend, refactor, fix bug terarah, test | analisa arsitektur besar |
| nalar | `smart/auto/reasoning` | debug sulit, desain arsitektur, review kritis, riset | bulk edit (mahal & lambat) |
| kualitas | `smart/auto/best` | kode produksi, migrasi, uang/auth/IO, rilis | eksplorasi awal |

Aktifkan cepat: `mamat auto quick|coding|reasoning|best`
Alias tugas: `mamat auto ui` (→coding) · `mamat auto debug` (→reasoning) ·
`mamat auto bulk` (→cheap) · `mamat auto docs` (→quick) · `mamat auto produksi` (→best).

## 2. Urutan provider (fallback)

1. `smart/auto/*` — router utama (pilih model terbaik yang ada kuota).
2. `or-free/auto/*` — gratis, kualitas lebih rendah; pakai kalau kuota utama 0.
3. `opencode/<model>-free` — darurat (model gratis tunggal), konteks kecil.
4. Model eksplisit (`omniroute/xkiro/...`) — hanya kalau butuh model tertentu (mis. vision).

Aturan: **jangan** pindah provider di tengah tugas panjang tanpa alasan; catat alasan
pergantian di laporan (biar tidak jadi loop).

## 3. Kuota & 429

`429 quota_balance_exhausted` = kuota habis (bukan rate limit) → jangan retry.
Urutan: turun tier (`best`→`coding`→`cheap`) → pindah provider (`smart`→`or-free`) →
tutup sesi berat + sesi baru → tunggu reset. Cek: `mamat limit --days 3`.

## 4. Anggaran konteks per tier

| Tier | Target konteks | Alasan |
|---|---|---|
| quick/cheap | ≤25% | tugas kecil, konteks besar hanya menambah biaya |
| coding | ≤50% | butuh file terkait + riwayat edit |
| reasoning/best | ≤70% | boleh baca lebih banyak, tapi tetap ringkas output |

Konteks >60% → `/note` lalu sesi baru (jangan `--resume`).

## 5. Bukti, bukan klaim

- Pemakaian: `mamat audit --days 1` · `python3 ~/.agents/audit-opencode.py`
- Limit/429: `mamat limit --days 3`
- MCP (harus tetap on-demand): `python3 ~/.agents/mcp-guard.py --verbose`
- Hasil routing dinilai dari: biaya per tugas turun, 429 turun, hasil tetap lulus verifikasi.

## 6. Aturan MCP (tegas)

- MCP **hanya** nyala saat dipakai; idle >7 hari diparkir (`mcp-guard.py --apply`).
- Maksimal 2 MCP nyala. Butuh lain → `mamat-mcp on <nama>` → `mamat-mcp restart` → pakai
  → `mamat-mcp off <nama>`.
- Jangan pernah menyalakan MCP "untuk jaga-jaga". Kalau tidak dipakai, matikan.
