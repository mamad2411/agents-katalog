# 13 — Security testing (bagian wajib dari testing, bukan tambahan)

Alat: `security-forge audit .` (secret, pola, SAST, dependency, docker, shell, izin),
`security-forge headers <url>`, `security-forge tls <host>`, `semgrep`, `bandit`,
`trivy`, `nuclei`, ZAP. Semua lokal & gratis.

## 1. OWASP Top 10 (2021) → cara menguji
| Risiko | Uji konkret |
|---|---|
| A01 Broken Access Control | matriks role×endpoint; IDOR (ganti id), akses langsung path admin, method override, tenant isolation |
| A02 Cryptographic Failures | TLS 1.2+ saja, HSTS, password hash (argon2/bcrypt cost), tidak ada data sensitif di URL/log, enkripsi at-rest |
| A03 Injection | SQLi (`' OR 1=1--`), NoSQL operator (`{"$gt":""}`), template (`{{7*7}}`), header/log injection, command injection |
| A04 Insecure Design | alur bisnis: harga negatif, qty 0, diskon ganda, refund berulang, race checkout |
| A05 Security Misconfiguration | header lengkap, debug mati, CORS terbatas, direktori listing mati, error tidak bocor stack trace |
| A06 Vulnerable Components | `trivy fs`/`trivy image` (HIGH/CRITICAL), lockfile dipin, tanpa dependency yatim |
| A07 Auth Failures | brute force (rate limit + lockout), credential stuffing, session fixation, token di localStorage vs cookie HttpOnly, logout mencabut sesi |
| A08 Integrity Failures | signature artefak, SRI untuk CDN, deserialisasi aman, CI supply-chain (pin action ke SHA) |
| A09 Logging Failures | login gagal tercatat, tidak ada PII di log, `trace_id` konsisten, alert untuk pola anomali |
| A10 SSRF | endpoint fetch URL eksternal: blokir 169.254.169.254, RFC1918, `file://`, redirect berantai |

## 2. OWASP API Top 10 → uji per endpoint
- BOLA/IDOR: akses objek milik user lain (paling sering bocor).
- Broken Auth: token tanpa expiry/audience salah, JWT `alg:none`, secret lemah.
- Excessive Data Exposure: response memuat field sensitif (`password_hash`, `nik`, `token`).
- Rate limiting & resource limits: 1000 request paralel, payload 100 MB.
- BFLA (function-level): user biasa memanggil endpoint admin.
- Mass assignment: kirim `{"role":"admin"}` → harus diabaikan/ditolak.
- SSRF, injection, improper inventory (endpoint lama/lupa dimatikan).
- Unsafe consumption of third-party API: validasi response pihak ketiga.

## 3. Matriks otorisasi (tulis sebagai test)
```python
ROLE_CASES = [("anon", 401), ("user", 403), ("staff", 200), ("admin", 200)]
@pytest.mark.parametrize("role,harap", ROLE_CASES)
def test_hapus_user(client, tokens, role, harap):
    r = client.delete("/users/2", headers=auth(tokens, role))
    assert r.status_code == harap
```
Sertakan juga: **tenant isolation** (user tenant A tidak boleh melihat data tenant B).

## 4. Uji abuse case (bukan cuma happy path)
- Diskon/promo dipakai berkali-kali, kode promo milik orang lain, negatif qty,
  harga diubah di client, upload file `.php`/`.svg` berisi script, nama file `../../etc/passwd`.
- Kuota & ekspor: unduh 1 juta baris → harus dibatasi.
- Enumeration: `/api/users/1..1000` tidak boleh membocorkan keberadaan.
- Password reset: token sekali pakai, expiry pendek, tidak bocor di response.
- Upload: MIME nyata (magic bytes), ukuran, ekstensi ganda, zip bomb, EXIF PII.

## 5. Pipeline (jalankan sebelum rilis)
```bash
security-forge audit .                 # secret + pola + sast + deps + docker + izin
security-forge report .                # simpan JSON+MD
security-forge image app:latest        # trivy image
security-forge headers https://staging.example.com
security-forge tls example.com
semgrep --config semgrep.yml --error --metrics=off .
gitleaks detect --no-git --redact
```
Gate: **0 HIGH/CRITICAL**, 0 secret nyata, 0 header wajib hilang, TLS 1.2+.
DAST (ZAP/nuclei) hanya pada lingkungan yang **boleh** diuji, dengan izin tertulis.

## 6. Privasi & kepatuhan
- Data pribadi: paling sedikit yang diperlukan; uji bahwa field yang tak dipakai tidak dikirim.
- Hak subjek data: ekspor & hapus akun benar-benar menghapus (termasuk backup policy).
- Retensi: log berisi PII terhapus otomatis sesuai kebijakan.
- Cookie: `Secure; HttpOnly; SameSite`, consent sebelum non-esensial.

## 7. Yang tidak boleh dilakukan AI
- Menyerang sistem tanpa izin (termasuk domain user lain).
- Menyimpan kredensial nyata dalam test/repo.
- Menonaktifkan pemeriksaan keamanan agar gate hijau.
- Menyebarkan data hasil scan (berisi PII/endpoint) ke layanan luar.
