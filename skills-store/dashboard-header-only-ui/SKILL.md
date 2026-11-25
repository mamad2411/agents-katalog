---
name: dashboard-header-only-ui
description: Bangun dashboard penonton tanpa sidebar (header + dropdown akun) di Next App Router dengan BFF cookie httpOnly, replika desain acuan. Trigger: dashboard header, tanpa sidebar, dropdown akun, karusel konser, kartu poster, bookmark optimistik, BFF pass-through.
version: 1.0.0
tags: [nextjs, dashboard, bff, ui, ticketing]
---
# Dashboard header-only (pola ShowTime customer)
1. **Gerbang:** `proxy.js` cek cookie → `(group)/layout.js` Server Component panggil `/me` → role salah `redirect`, 401 → `/api/auth/expired`.
2. **Data:** Server Component `getData(path)` (cookie→Bearer). Aksi klien (bookmark, notifikasi) lewat `app/api/<area>/[...path]/route.js` ber-**allowlist** (metode+regex), cek Origin untuk non-GET, biner (PDF) di-stream.
3. **Komponen:** Header (client: dropdown role=menu, Esc, ↑↓/Home/End, fokus item pertama via effect — bukan ref callback), Carousel (client, scroll-snap, panah hanya bila ada isi tersembunyi), Card/Row = *stretched link* (`absolute inset-0` + tombol `z-10`), Poster placeholder (gradien dari hash; inisial dari judul sebelum " — "), BookmarkButton optimistik + rollback.
4. **Jebakan nyata:** `useEffect(()=>setX())` kena lint → pakai state turunan; kolom grid tetap melebihi 768px → pakai breakpoint `xl`; `input[type=date]` ikut locale OS → tampilkan teks sendiri + input transparan di atasnya; endpoint QR backend = JSON dataURL, bukan gambar.
5. **Gerbang:** `scripts/customer-smoke.sh` + uji klik Playwright + cek overflow 360/768/1024/1440 + bandingkan screenshot dengan acuan.
