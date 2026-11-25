# 19 — Gate CI & kebijakan rilis

## 1. Gate bertingkat menurut risiko
| Risiko perubahan | Gate wajib |
|---|---|
| Rendah (teks, style) | lint, typecheck, unit terkait |
| Sedang (fitur, endpoint) | + integrasi, kontrak, regresi P1, secret scan |
| Tinggi (uang, auth, migrasi, infra) | + e2e alur kritis, authz matrix, security audit, performa baseline, migrasi up/down |
| Kritis (rilis besar) | + UAT, chaos 1 skenario, backup/restore, rollback teruji |

## 2. Urutan job CI (cepat → lambat, gagal cepat)
1. `lint` + `format check` (< 1 menit)
2. `typecheck` (< 2 menit)
3. `unit` (paralel per paket)
4. `integrasi` (container DB/Redis)
5. `kontrak` (schema/OpenAPI lint)
6. `security` (`security-forge audit`, `gitleaks`, `trivy fs`)
7. `e2e` (playwright, 3–10 skenario)
8. `performa` (k6 smoke load, threshold)
9. `build` + `image scan`
10. `deploy staging` → `smoke` → promosi manual

## 3. Anggaran waktu & aturan
- Total PR ≤ 15 menit; rilis ≤ 30 menit. Lewat itu → pisahkan/paralelkan.
- Tidak ada `continue-on-error` pada gate wajib.
- Test yang lambat (> 2 menit) dipisah ke job terjadwal, bukan dihapus.
- Cache dependency, tapi **jangan** cache hasil test.
- Kegagalan harus menampilkan: perintah, exit code, 20 baris log relevan, artefak (trace/screenshot).

## 4. Coverage & mutasi
- Baris: 70–85% (naik bertahap, jangan turunkan ambang).
- Modul uang/authz/migrasi: 100% cabang.
- Mutasi (`mutmut`/`stryker`) dijalankan mingguan pada modul kritis; target kill ≥ 60%.
- Coverage tidak boleh naik dengan test tanpa asersi.

## 5. Flake quarantine
- Deteksi: test sama gagal-lulus tanpa perubahan kode (≥2× dalam 14 hari).
- Tindakan: tandai `quarantine` + tiket + pemilik, **maksimal 7 hari**.
- Dilarang: `retries: 3` global untuk menyembunyikan flake.
- Setelah diperbaiki: hapus tanda karantina, pastikan 20 run berturut hijau.

## 6. Rilis: checklist pra-terbang
- [ ] Semua gate hijau di commit yang akan dirilis (bukan di commit lain).
- [ ] Changelog + versi + migrasi data terdaftar.
- [ ] Feature flag untuk perubahan berisiko (bisa dimatikan tanpa deploy).
- [ ] Rollback sudah pernah diuji (bukan hanya tertulis).
- [ ] Smoke suite siap + dashboard/alert dipantau 30 menit pertama.
- [ ] Rencana komunikasi bila gagal (siapa, di mana).

## 7. Canary & promosi
1. 5% trafik → pantau error rate, p95, log aneh (10 menit).
2. 25% → 50% → 100% dengan kriteria angka yang sama.
3. Gagal kriteria → rollback otomatis/manual, catat penyebab.

## 8. Bukti yang harus dilampirkan AI
```
🧪 Uji: <perintah> → exit 0 · <ringkasan: 42 pass, 0 fail>
📊 Gate: lint ✅ type ✅ unit ✅ kontrak ✅ security ✅ e2e 3/3 ✅ perf p95 180ms ✅
```
Tanpa ini, statusnya "belum diuji" — bukan "selesai".

## 9. Larangan
- Menghapus/menonaktifkan test, `skip`, atau ambang coverage agar hijau.
- `git push --no-verify`, `--force` ke branch bersama.
- Merge saat check masih merah/`in_progress`.
- Menyimpan kredensial/artefak berisi PII di CI.
