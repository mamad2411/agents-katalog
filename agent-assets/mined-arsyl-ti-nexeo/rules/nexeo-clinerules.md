# ATURAN SISTEM (SYSTEM RULES) - MONOREPO & STRICT DOMAIN ISOLATION

Kamu adalah AI Autonomous Developer. Proyek ini sedang bertransisi menggunakan arsitektur **Turborepo Monorepo, Nuxt 3 (Frontend), Express.js (Backend), PostgreSQL, JSON DB, TypeScript, dan Vitest**.

WAJIB patuhi aturan ini sebelum melakukan tugas koding apa pun:

## 1. ATURAN ISOLASI KETAT (STRICT DOMAIN ISOLATION)
- Proyek ini memisahkan fitur berdasarkan domain (Video Player, Novel Scraper, YT Downloader) dalam struktur file dan state yang independen.
- **Kacamata Kuda:** Jika kamu diminta mengedit/menambah fitur di domain "Novel", kamu DILARANG KERAS membuka, merapikan, atau mengedit file yang berada di domain "Video" atau "Downloader". 
- Lakukan pengecekan `git diff` sebelum lapor selesai. Batalkan (revert) perubahan jika file di luar tugasmu ikut berubah.

## 2. TRANSISI TYPESCRIPT (GRADUAL TS)
- Saat membuat file baru, WAJIB gunakan TypeScript (`.ts` atau `<script setup lang="ts">`).
- Buat tipe data (`interface` atau `type`) yang jelas untuk setiap respons dari PostgreSQL maupun file database JSON agar tidak terjadi error *undefined*.
- Jika mengedit file `.js` lama, biarkan kecuali kamu ditugaskan untuk melakukan migrasi ke `.ts`.

## 3. VITEST & PENGUJIAN OTOMATIS
- **TDD Wajib:** Sebelum mengimplementasikan logika fitur baru atau memperbaiki bug, tulis file test Vitest terlebih dahulu.
- Jalankan `npm run test` di terminal secara mandiri. Perbaiki kodemu berdasarkan pesan error merah di terminal hingga pengujian LULUS (PASS).
- JANGAN merusak test milik domain lain (Regression Testing).

## 4. PEMISAHAN FILE (MODULARIZATION)
- Jangan gabungkan logika bisnis di dalam komponen UI (`.vue`). Pisahkan logika pemrosesan (terutama ekstraksi database JSON) ke dalam `composables/` (Nuxt) atau `utils/`.
- Backend Express harus memiliki *router* terpisah per domain, bukan digabung dalam satu `index.ts`.

## 5. UPDATE KONTEKS MEMORI
- Selalu baca `PROJECT_CONTEXT.md` dan `MIGRATION_PLAN.md` sebelum memulai tugas.
- Setelah satu fitur selesai dimigrasi atau ditambahkan, UPDATE `PROJECT_CONTEXT.md` agar peta arsitekturnya selalu mencerminkan kondisi terbaru.