---
name: auth-ui-hemat-token
description: Bangun login/registrasi/landing/dashboard yang aman (cookie httpOnly, BFF Next) dan bebas ui-slop dengan token minimal. Trigger: login, register, registrasi, daftar, auth, cookie, sesi, security login, landing dashboard, ui slop, ui ux login.
version: 1.0.0
tags: [auth, nextjs, cookie, ui, anti-slop, hemat-token]
---

# Auth + UI hemat token

Urutan baca ≤2 KB. Jangan baca ulang file; `grep -n` lalu 40 baris sekitar hit.

## 1. Brief satu baris (wajib sebelum kode)
`siapa · 1 aksi utama · mood` — contoh: "penonton/penyelenggara · masuk · panggung malam, tenang".

## 2. Referensi (1 kali, bukan dari ingatan)
`dref <url-login-pembanding>` → buka `~/.agents/refs/<slug>/desktop-hero.png` dengan Read.
Ambil prinsip (grid, urutan field, posisi "Lupa"), bukan aset. Catat di `docs/REFERENSI.md`.

## 3. Pola auth aman (Next App Router + API terpisah)
```
Browser → /api/auth/* (route handler) → Bearer → backend
JWT hanya di cookie: httpOnly · SameSite=Lax · Secure + __Host- (prod) · Path=/
```
- Wajib: cek `Origin` = host (CSRF), rate limit login per IP+email, pesan gagal SERAGAM
  (anti-enumerasi), validasi ulang di server, `?next=` hanya path internal, `proxy.js` hanya
  cek cookie ada, validasi sungguhan di Server Component (`/me`), cookie basi → route `expired`
  yang menghapus cookie (Server Component tidak boleh set cookie → hindari loop redirect).
- Dilarang: token di `localStorage`, `NEXT_PUBLIC_` untuk URL backend privat, `resetToken` di response,
  tombol "masuk demo" tanpa kredensial.
- Template kerja: `lib/server/bff.js` + `app/api/auth/*` di proyek ShowTime (salin, jangan tulis ulang).

## 4. UI anti-slop (aturan keras)
- 1 headline, 1 CTA berwarna (gradien merek hanya di CTA). Judul warna solid.
- Tanpa kartu kaca-blur, tanpa 3 kartu fitur kembar, tanpa badge pujian, tanpa emoji ikon.
- Ikon: lucide 16–20px, stroke 1.75, hanya yang BERFUNGSI (mata=toggle, panah=kembali).
- Fakta di copy harus ada di kode. Tanpa "terbaik/tercepat/seamless".
- Label di atas input (bukan placeholder), "Lupa" sejajar label sandi, error di bawah field + fokus ke error pertama.
- State lengkap: default, fokus, error, loading, sukses, 429, 503, sesi berakhir, caps lock.
- Satu mode (gelap) bila diminta: hapus `data-theme`, toggle, dan `localStorage` tema sekalian.

## 5. Gerbang (jalankan, jangan klaim)
```sh
bash ~/.agents/skills-store/auth-ui-hemat-token/scripts/auth-smoke.sh http://localhost:3100
dcheck http://localhost:3100/login   # exit 1 = belum selesai
dcheck http://localhost:3100/registrasi
npx eslint .
```
Lalu Read `~/.agents/refs/<slug>/{desktop-hero,mobile}.png`.

## 6. Hemat token
- Tulis file besar sekali (heredoc), perbaiki dengan python/Edit kecil.
- Satu build + satu `dcheck` per putaran; jangan screenshot tiap tweak.
- Dokumen: PRD ringkas bertabel (kontrol → bukti uji), bukan esai.
