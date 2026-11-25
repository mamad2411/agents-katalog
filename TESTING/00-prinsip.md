# 00 — Prinsip dasar testing (baca sebelum menulis test apa pun)

## 1. Oracle: dari mana kamu tahu hasilnya benar?
Test tanpa oracle = teater. Pilih salah satu, sebutkan di komentar/nama test:

| Oracle | Contoh | Kapan |
|---|---|---|
| Spesifikasi eksplisit | `total = subtotal + pajak - diskon` | aturan bisnis |
| Invarianti | saldo tidak negatif; stok ≥ 0; urutan id naik | sistem stateful |
| Kontrak | schema OpenAPI/Pact/gRPC proto | antar layanan |
| Golden/snapshot | HTML/JSON/CSV pembanding | format stabil |
| Diferensial | implementasi baru vs lama, hasil harus sama | refactor/rewrite |
| Metrik | p95 < 200 ms, error rate < 0.1% | non-fungsional |
| Properti | untuk semua input valid, `decode(encode(x)) == x` | parser/serializer |
| Referensi pihak ketiga | hitung ulang dengan library lain | rumus kritis |

## 2. Data uji
- **Bangun data sendiri per test** (factory/fixture), jangan bergantung pada data produksi.
- Data harus deterministik: waktu di-freeze (`freezegun`, `clock` palsu), acak di-seed.
- Pisahkan: **valid**, **batas** (0, -1, maks, panjang tepat), **tidak valid**, **jahat**
  (unicode, emoji, NUL, 10 MB, SQL/HTML injection, path traversal).
- PII: jangan pernah pakai data pelanggan nyata. Pakai generator (Faker) + anonimisasi.
- Bersihkan setelah test (transaksi rollback / truncate / temp dir), jangan saling ganggu.

## 3. Batas & kasus tepi yang WAJIB dicoba
`""` · spasi saja · `null`/`None`/`undefined` · angka 0, negatif, sangat besar, desimal
panjang · tanggal 29 Feb, DST, timezone beda, tahun 2038 · unicode/RTL/emoji/gabungan
diakritik · string 1 karakter dan 100k karakter · daftar kosong dan 1 juta item ·
duplikat · urutan terbalik · konkurensi (2 request bersamaan) · retry/timeout ·
izin salah (403) · sesi kedaluwarsa · token dicabut · media type salah · body tidak ada.

## 4. Flaky: kebijakan keras
- Flaky = **bug** (di test atau di kode), bukan "nasib".
- Dilarang: `retry` global, `sleep`, `waitForTimeout`, menaikkan timeout sebagai solusi.
- Perbaiki: tunggu kondisi nyata (`expect(...).toBeVisible()`, polling predicate),
  hilangkan ketergantungan urutan, seed acak, isolasi data, matikan animasi.
- Karantina maksimal 7 hari dengan tiket; setelah itu perbaiki atau hapus.

## 5. Lingkungan
| Lingkungan | Untuk | Aturan |
|---|---|---|
| lokal | unit/integrasi | cepat, tanpa jaringan luar |
| CI | semua gate | deterministik, paralel, tanpa rahasia nyata |
| staging | e2e, performa, UAT | data sintetis, sama topologi dengan prod |
| produksi | smoke, synthetic, canary | read-only/khusus, jangan pernah uji destruktif |

Test tidak boleh bergantung pada internet. Bila perlu, pakai mock server lokal
(MSW, `responses`, WireMock, `prism`).

## 6. Format laporan bug (wajib untuk semua AI)
```
Judul: [area] perilaku salah dalam 1 kalimat
Lingkungan: commit/versi, OS, browser, URL/env
Langkah: 1..N (bisa diulang siapa pun)
Hasil: aktual (tempel output/screenshot)
Harapan: sesuai spesifikasi (kutip sumbernya)
Dampak: pengguna/uang/data — P1..P4
Bukti: log, request-id, test yang gagal
Dugaan: file:baris (kalau ada)
```

## 7. Taksonomi lengkap jenis test (untuk memilih, bukan menghafal)
**Berdasarkan tingkat:** unit, component, integration, contract, system, e2e, acceptance.
**Berdasarkan tujuan:** functional, regression, smoke, sanity, exploratory, usability,
accessibility, i18n/l10n, compatibility, install/upgrade, recovery, failover, DR,
concurrency, idempotency, data-integrity, migration, backup/restore.
**Non-fungsional:** performance (load/stress/soak/spike/scalability), security
(SAST/DAST/SCA/secrets/authz/fuzz), reliability/chaos, observability, maintainability,
portability, privacy/compliance (GDPR/UU PDP), cost.
**Teknik desain kasus:** equivalence partitioning, boundary value, decision table,
state transition, pairwise/combinatorial, cause-effect, error guessing, property-based,
mutation, differential, fuzz, model-based, risk-based.
**Level otomasi:** manual, scripted, automated, self-healing, synthetic monitoring.

## 8. Definition of Done untuk test
- [ ] Ada nama jelas (`test_<perilaku>_<kondisi>_<harapan>`).
- [ ] Gagal bila perilaku salah (sudah dibuktikan).
- [ ] Cepat (< 100 ms unit, < 1 s integrasi).
- [ ] Tidak bergantung jaringan/urutan/data global.
- [ ] Assertion spesifik (bukan `assert result`).
- [ ] Satu alasan gagal per test.
