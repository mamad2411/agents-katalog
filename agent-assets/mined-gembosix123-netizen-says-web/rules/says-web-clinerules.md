# ATURAN KERJA PROFESIONAL - SISTEM SAYS 2.0

## 1. PENJIMATAN TOKEN & KOS (CRITICAL)
- JANGAN sesekali membaca atau mengimbas folder: /node_modules, /.git, /dist, /build.
- JANGAN memproses fail media besar seperti .png, .jpg, atau .mp4.
- Fokus pembacaan fail hanya pada folder `/src` atau fail konfigurasi spesifik yang diminta.
- Sebelum memulakan tugas besar, berikan ringkasan pelan kerja dan anggaran impak pada kod sedia ada.

## 2. PENGENDALIAN RALAT (ERROR HANDLING)
- Jika berlaku ralat (error), fokus hanya pada fail yang disebut dalam Stack Trace terminal.
- Gunakan log terminal yang diberikan oleh user untuk mencari punca ralat; jangan teka-teka (no trial and error).
- Jika tersekat (stuck) lebih daripada 3 kali pada masalah yang sama, BERHENTI dan minta input manual daripada user.

## 3. PIAWAIAN KOD (CODING STANDARDS)
- Gunakan Tailwind CSS untuk semua urusan penggayaan (styling).
- Kod mestilah bersih, modular (pecahkan komponen besar), dan mempunyai komen yang ringkas.
- Pastikan setiap fungsi baru tidak merosakkan (breaking changes) fungsi sedia ada.

## 4. INTEGRITI DATA & SECURITY
- JANGAN sesekali mengubah atau memadam fail `.env` tanpa kebenaran bertulis.
- Pastikan sambungan database menggunakan amalan terbaik dan sentiasa ditutup (close connection) jika perlu.