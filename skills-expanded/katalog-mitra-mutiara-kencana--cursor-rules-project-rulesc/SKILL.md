---
description: Aturan utama untuk project website katalog
alwaysApply: true
---

# Project: Website Katalog Produk

## Tech Stack
- Gunakan HANYA HTML, CSS, dan JavaScript vanilla (murni)
- JANGAN gunakan framework seperti React, Vue, Next.js, atau library seperti jQuery, Bootstrap, Tailwind CDN kecuali diminta secara eksplisit
- Tidak perlu build tool (webpack, vite, dll) — project harus bisa langsung dibuka via Live Server

## Struktur File
- index.html di root folder
- CSS di folder /css (misalnya css/style.css)
- JavaScript di folder /js (misalnya js/script.js)
- Gambar/aset di folder /assets/images
- Data produk (kalau ada) disimpan di file JS terpisah, misalnya js/data.js, dalam bentuk array of objects

## Coding Style
- Gunakan nama variabel dan fungsi dalam bahasa Inggris, comment boleh bahasa Indonesia
- HTML: gunakan semantic tags (header, main, section, footer, nav) bukan div semua
- CSS: gunakan class naming yang konsisten (BEM style lebih disukai: block__element--modifier)
- JavaScript: gunakan const/let, hindari var; gunakan arrow function untuk konsistensi
- Selalu responsive (mobile-friendly), gunakan CSS Flexbox/Grid, bukan float atau table layout

## Perilaku AI
- Sebelum generate kode besar, jelaskan singkat rencana/pendekatan yang akan diambil
- Kalau mengubah file yang sudah ada, jangan hapus kode yang tidak relevan dengan request
- Berikan komentar singkat di kode yang kompleks/tidak jelas, karena user masih belajar
- Kalau ada beberapa cara untuk implementasi, pilih cara yang paling mudah dipahami pemula, bukan yang paling "clever" atau ringkas