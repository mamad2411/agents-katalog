# 21 — Anti-pattern: 40 cara "hijau palsu" yang wajib ditolak

Setiap baris adalah pola yang harus **ditolak** saat review, beserta gantinya.

## Asersi & struktur test
1. `assert result` / `expect(x).toBeTruthy()` tanpa makna → asersi nilai konkret.
2. Test tanpa asersi (hanya memanggil fungsi) → tambahkan oracle.
3. `assert True` / `expect(true).toBe(true)` → hapus.
4. Test menangkap semua exception (`try/except: pass`) → biarkan gagal.
5. Satu test menguji 10 hal → pecah, satu alasan gagal.
6. Nama test `test_1`, `test_foo` → `<perilaku>_<kondisi>_<harapan>`.
7. Snapshot raksasa (10k baris) → uji field penting saja.
8. Snapshot di-`--update` otomatis saat CI → review diff dulu.
9. Menguji implementasi privat (state internal, class CSS) → uji perilaku.
10. Menguji mock, bukan kode (`expect(mock).toHaveBeenCalled`) sebagai satu-satunya asersi.

## Mock & data
11. Mock seluruh lapisan (service+DB+HTTP) → tidak ada yang diuji.
12. Mock yang tidak bisa gagal (MagicMock bebas) → pakai spec/type/schema.
13. Data uji dari produksi (PII) → generator/anonimisasi.
14. Test bergantung urutan eksekusi → isolasi data.
15. Test bergantung waktu nyata (`sleep`, `Date.now`) → fake clock.
16. Data global dibagi antar test → factory per test.
17. Test "lulus" karena data kosong (loop 0 iterasi) → assert jumlah > 0.
18. Mengubah data produksi saat test → hanya staging/sandbox.

## E2E
19. `waitForTimeout(3000)` → tunggu kondisi nyata.
20. Selector CSS/XPath struktural → role/label.
21. `retries: 3` untuk menutupi flake → perbaiki akar.
22. Satu e2e menguji 30 langkah → pecah per tujuan.
23. Login lewat UI di setiap test → storageState.
24. Hanya menguji happy path → tambah error/empty/permission.
25. Screenshot selalu lulus karena masking seluruh halaman → mask seperlunya.

## Gate & CI
26. `--no-verify`, skip hook → dilarang.
27. `continue-on-error: true` pada test → dilarang.
28. Menghapus test yang gagal → perbaiki atau karantina bertiket.
29. Menurunkan ambang coverage agar hijau → naikkan perlahan.
30. `--force` push ke branch bersama → dilarang.
31. Merge saat check `in_progress` → tunggu hijau.
32. Test dijalankan tapi hasilnya tidak diperiksa (`|| true`) → hapus `|| true`.
33. Coverage dinaikkan dengan file kosong/test tanpa asersi → tolak.

## Non-fungsional
34. Klaim "cepat" tanpa angka p95 → jalankan k6 dengan threshold.
35. Klaim "aman" tanpa scan → `security-forge audit` + trivy.
36. Klaim "a11y OK" hanya dari mata → axe/pa11y 0 violation.
37. Klaim "sudah diuji di mobile" tanpa device → playwright device profile.
38. Uji beban 5 detik lalu simpulkan → minimal 5–10 menit dengan metrik server.
39. Menyembunyikan error 500 dengan retry di client → perbaiki server.
40. Laporan "semua hijau" tanpa perintah/exit code → tidak dihitung.

## Cara cepat menilai sebuah test (30 detik)
- Bisa gagal? coba rusak kodenya sedikit (atau ubah ekspektasi) → harus merah.
- Gagal karena apa? pesan harus menunjuk perilaku, bukan `undefined is not a function`.
- Berapa lama? unit < 100 ms, integrasi < 1 s, e2e < 60 s.
- Butuh apa? tidak boleh jaringan luar/rahasia/urutan tertentu.

## Kalimat yang harus dihindari AI
- "Seharusnya sudah jalan." → jalankan.
- "Test-nya sudah lulus di lokal." → lampirkan exit code.
- "Saya skip test ini sementara." → perbaiki atau karantina bertiket.
- "Coverage sudah 100%." → tunjukkan asersi & mutasi.
- "Sudah dicek manual." → tunjukkan charter/checklist + bukti.
