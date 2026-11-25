---
name: testing-forge
description: Testing aplikasi web, API, mobile, CLI, data/ML dan infra lengkap ala QA/QC: unit, integrasi, kontrak, e2e Playwright, a11y, performa k6, security, manual UAT, dan CI. Pakai untuk rencana testing, review test, scaffold test, audit jenis test yang belum ada.
---

# testing-forge — cara benar menguji aplikasi (semua AI)

Dokumen kanonik: `~/.agents/TESTING.md` + detail di `~/.agents/TESTING/*.md` (13 file).
CLI: `testing-forge` (0 token, tanpa MCP).

## Perintah
```bash
testing-forge matrix                 # 14 lapisan x 37 jenis x 13 teknik = 6.734 kombinasi
testing-forge layers                 # daftar lapisan + dokumen + alat
testing-forge show e2e               # ringkas 1 lapisan + checklist
testing-forge plan --stack web --risk high
testing-forge generate tests-web w1  # 8 file playwright+vitest+axe+k6, 4 test lulus
testing-forge generate tests-api a1  # pytest+httpx+hypothesis+schemathesis+locust
testing-forge generate tests-cli|tests-lib|tests-data|tests-ml|tests-infra <dir>
testing-forge audit <dir>            # lapisan test yang belum ada (bukan coverage baris)
testing-forge selftest               # cek katalog internal (exit != 0 bila rusak)
```

Lapisan: unit · integrasi · kontrak · e2e · visual · a11y · i18n · performa ·
security · data · ml · infra · manual · ci.

## Tiga aturan yang tidak bisa dilanggar
1. **Bukti, bukan klaim** — "selesai" = perintah test dijalankan, exit code 0, output ditempel.
2. **Test yang tidak bisa gagal = tidak ada test** — buktikan pernah merah, lalu hijau.
3. **Jangan melemahkan gerbang** — tanpa `--no-verify`, skip permanen, atau hapus test.

## Alur 7 langkah
1. Petakan risiko (3–7) → 2. pilih lapisan termurah yang menangkap risiko →
3. tentukan oracle → 4. tulis test gagal dulu (red) → 5. implementasi sampai hijau →
6. uji negatif & batas → 7. catat bukti (perintah + exit code + ringkasan).

## Venv alat Python (sudah siap)
`~/.agents/test-venv/bin/pytest` · `hypothesis` · `schemathesis` · `locust` (httpx ikut).

## Larangan (lihat TESTING/21-antipattern.md — 40 pola hijau palsu)
`assert True`, `try/except: pass`, `waitForTimeout`, `retries: 3` untuk flake,
`|| true` pada test, coverage dinaikkan tanpa asersi, mock seluruh sistem.
