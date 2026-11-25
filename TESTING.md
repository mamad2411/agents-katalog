# TESTING — aturan testing kanonik (semua AI: Claude, opencode, Codex, Gemini, Cursor)

Berlaku untuk **semua** tugas: web, API, CLI, lib, data/ML, infra, mobile, desktop.
CLI pendamping: `testing-forge` (matrix/plan/show/generate/audit) — 0 token, tanpa MCP.
Baca file ini dulu; detail per lapisan ada di `~/.agents/TESTING/` (buka hanya yang relevan).

---

## 1. Tiga aturan yang tidak bisa dilanggar

1. **Bukti, bukan klaim.** "Selesai" = perintah test dijalankan, exit code **0**, output
   ditempel. Tanpa itu, tulis "belum diuji".
2. **Test yang tidak bisa gagal = tidak ada test.** Wajib ada bukti test pernah **merah**
   (mutasi / ubah ekspektasi / revert fix) lalu hijau. Test yang selalu lulus tanpa asersi
   atau yang menelan exception adalah sampah — hapus atau perbaiki.
3. **Jangan melemahkan gerbang.** Dilarang: `--no-verify`, `-k 'not ...'`, skip permanen,
   raise coverage palsu, mock seluruh sistem, atau hapus test agar CI hijau.

---

## 2. Alur testing yang benar (7 langkah, urut)

1. **Petakan risiko** (5 menit): apa yang bisa membuat uang/data/reputasi rusak?
   Tulis 3–7 risiko → tiap risiko minimal 1 test.
2. **Pilih lapisan** yang paling murah tapi masih menangkap risiko itu (lihat §3).
3. **Tentukan oracle**: dari mana tahu hasilnya benar? (spesifikasi, invarianti,
   snapshot, kontrak OpenAPI, data pembanding, metrik).
4. **Tulis test yang gagal dulu** (red) → jalankan → lihat pesan gagal yang jelas.
5. **Implementasi/ perbaiki** sampai hijau. Jalankan seluruh suite terkait.
6. **Uji negatif & batas**: input kosong, maksimum, unicode, waktu, konkurensi,
   permission salah, jaringan putus, disk penuh.
7. **Catat bukti**: perintah, ringkasan hasil, commit/file yang berubah. Lampirkan
   ke laporan dengan format 4 baris (✅/📁/🧪/⚠️).

Untuk tugas besar, urutannya: unit/integrasi → kontrak → e2e happy path → security →
performa → a11y → regresi visual. Jangan pernah mulai dari e2e (lambat, rapuh, mahal).

---

## 3. Piramida + trofi (pakai trofi untuk web modern)

| Lapisan | Porsi | Kecepatan | Contoh |
|---|---|---|---|
| Unit (pure logic) | ~50% | ms | validasi harga, parser, reducer |
| Integration/component | ~30% | <1 s | komponen + MSW, handler + DB in-memory |
| Contract | ~10% | <5 s | OpenAPI schema, Pact |
| E2E (browser nyata) | ~10% | <60 s/skenario | 3–10 alur kritis saja |
| Non-fungsional | sesuai risiko | menit | aksesibilitas, performa, keamanan |

E2E bukan tempat mengejar coverage. Satu alur uang = wajib e2e; 50 varian tombol = unit.

---

## 4. Pemilihan cepat (tanya → lapisan)

| Gejala / kebutuhan | Wajib jalankan |
|---|---|
| logika/rumus/kondisi baru | unit + property (boundary) |
| render komponen, state, form | component (Testing Library) |
| endpoint baru / berubah | contract + API test + authz matrix |
| UI berubah rupa | visual regression + a11y |
| query/database | integrasi DB nyata (container) + plan query |
| upload/auth/pembayaran | e2e + security abuse case + idempoten |
| klaim "cepat/tahan beban" | load test k6 + anggaran p95 |
| deploy/container/k8s | smoke rilis + probe + rollback |
| migrasi data | up+down + rekonsiliasi jumlah/checksum |
| model ML | holdout eval + drift + fairness |

---

## 5. Standar minimum per jenis proyek (gate rilis)

| Jenis | Wajib sebelum bilang selesai |
|---|---|
| web (frontend) | lint + typecheck + unit/component + e2e 1 alur kritis + axe 0 violation serius + `dcheck` |
| api/backend | lint + type + unit + integrasi DB + kontrak schema + authz negatif + secret scan |
| cli | unit + snapshot output + exit code + stdin/pipe + `--help` |
| lib/package | unit + API publik stabil + type test + build konsumen (smoke import) |
| data/ML | schema data + uji nol/kontrak + holdout metric + idempoten pipeline |
| infra/server | `nginx -t`/`compose config`/`kubeconform` + smoke + rollback + `security-forge audit` |

`project-forge verify <dir>` menjalankan sebagian ini; `testing-forge audit <dir>`
menunjukkan **jenis test** yang belum ada (bukan coverage baris).

---

## 6. Perintah harian (0 token)

```bash
testing-forge matrix                 # peta jenis test × lapisan + jumlah kombinasi
testing-forge plan --stack web --risk high
testing-forge generate tests-web w1              # playwright+vitest+axe+k6 (4 test lulus)
testing-forge generate tests-api a1              # pytest+httpx+hypothesis (10 test lulus)
testing-forge audit .                            # apa yang belum diuji
security-forge audit .                           # keamanan (bagian dari testing)
dcheck <url> · dvisual <url> · dref <url>        # UI: a11y, visual, referensi nyata
project-forge verify .                           # gate proyek
```

Test tools yang sudah ada di mesin ini (jangan install ulang): `k6`, `ab`, `playwright`,
`node/npx`, `curl`, `jq`, venv `~/.agents/test-venv/bin/{pytest,schemathesis,locust}` (+hypothesis, httpx). Detail: `~/.agents/TESTING/20-alat-matrix.md`.

---

## 7. Aturan khusus untuk subagent & AI

- Subagent **test-automator**: baca `TESTING.md` + `10-unit-integrasi.md` + `11-kontrak-api.md`
  + `12-e2e-browser.md`; keluaran wajib: file test + perintah + exit code.
- Subagent **verify**: hanya menjalankan, tidak menambal. Laporkan exit code apa adanya,
  sertakan 5 baris terakhir output yang gagal.
- Subagent **review**: cari **test yang tidak menguji** (asersi kosong, mock berlebihan,
  snapshot raksasa, `except: pass`, `assert True`), plus celah edge case.
- Subagent **security-auditor**: `security-forge audit .` dulu, baru analisis manual.
- Semua AI: kalau test gagal, **jangan** mengubah test agar lulus kecuali ekspektasi memang
  salah — sebutkan alasannya di satu baris.
- Jangan tulis test yang butuh layanan berbayar/rahasia. Pakai fake/MSW/container lokal.

---

## 8. Indeks detail

| File | Isi |
|---|---|
| `TESTING/00-prinsip.md` | oracle, test data, flaky, lingkungan, format bug, taksonomi |
| `TESTING/10-unit-integrasi.md` | unit, component, integrasi DB/queue, mock yang benar |
| `TESTING/11-kontrak-api.md` | OpenAPI/Pact, REST/GraphQL/gRPC/WS, authz, fuzz, property |
| `TESTING/12-e2e-browser.md` | Playwright, selector, POM, auth, cross-browser, visual, mobile/PWA |
| `TESTING/13-security.md` | OWASP Top10/API10, authz, bisnis-logic, SAST/DAST/SCA, secret |
| `TESTING/14-performa.md` | load/stress/soak/spike, k6, anggaran, profiler, CWV, DB |
| `TESTING/15-a11y-i18n.md` | WCAG 2.2 AA, keyboard, screen reader, i18n/RTL, format |
| `TESTING/16-data-db-ml.md` | migrasi, transaksi, backup/restore, ETL, ML eval/drift |
| `TESTING/17-infra-deploy-chaos.md` | container, k8s, smoke, rollback, DR, chaos |
| `TESTING/18-manual-uat-regresi.md` | exploratory charter, SFDPOT, UAT, regresi, bug report |
| `TESTING/19-ci-gate-policy.md` | gate per risiko, waktu, flake quarantine, coverage, rilis |
| `TESTING/20-alat-matrix.md` | semua alat + perintah + apa yang dibuktikan |
| `TESTING/21-antipattern.md` | 40 cara "hijau palsu" yang harus ditolak |

Jumlah kombinasi yang bisa dibentuk (jenis test × lapisan × platform × risiko × data)
dihitung `testing-forge matrix` — ribuan jalur; pilih yang **menutup risiko**, bukan semua.
