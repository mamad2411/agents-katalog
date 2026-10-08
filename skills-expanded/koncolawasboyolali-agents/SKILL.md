# AGENTS.md — Koncolawas

## Session 2026-05-28

### Features Added

### Onboarding Flow
- **App shell** (`app-shell.tsx`): After auth confirmed, fetches `GET /alumni/profiles/me`. If 404 (no profile) or `tahunMasuk`/`tahunLulus` empty, redirects to `/profile`. Skips check when already on `/profile` to prevent infinite loop. Shows loading spinner during check.
- **Profile page** (`profile/page.tsx`): Handles 404 from profile fetch gracefully (no error toast for new users). Yellow onboarding banner "Lengkapi data tahun masuk dan tahun lulus untuk mengakses fitur lainnya" shown when fields are empty. `tahunMasuk` and `tahunLulus` marked as required with red asterisk.
- No backend changes needed — existing `GET /alumni/profiles/me` endpoint returns `tahunMasuk`/`tahunLulus` and throws 404 when no profile exists.

### Bugs Fixed
- Login blank page: Google Strategy email fallback when `emails` array is missing
- 502 auth proxy: Added `_next/data` rewrite exclusion to prevent double-handling
- Stats overview: Use `req.query` instead of `req.body` for GET route params

### Features Added
- **Kelas tracking**: `kelas1`, `kelas2`, `kelas3` fields on `Alumni` model; bulk-update endpoint; CSV import auto-detects kelas columns
- **Alumni cards**: `kelas3` displayed; `kelas1`/`kelas2` shown when different from kelas3
- **Alumni Berprestasi**: `isAchiever` flag toggle; carousel on homepage

### Backend
- Google Strategy email fallback using `profile._json.email`
- `ImportController` with `fromSheet` and `fromLegacy` endpoints
- `SuccessStory` Prisma model + CRUD controller (CRUDController)
- `GET /api/whoami` returns full user + alumni profile

### Frontend
- `/sukses` page with grid of success stories + detail modal with "Lihat Profil Lengkap" link
- `/admin/success-stories` CRUD with form modal
- Admin sidebar nav items + sub-nav for success stories
- Migration button on `/admin/import` page (POST to `/import/from-legacy`)

### Docs & GitHub
- README rewrite with updated setup instructions
- Issue #35 document: Import from Old Platform & Google Sheets
- Issue #36 document: Success Stories feature
- Issue #30 closed (success stories)
- Migration ready: 67 alumni with emails from koncolawas2005.web.app
- Sync penuh: semua kode terdokumentasi di GitHub sebagai rujukan utama

---

## Workflow Siklus Development

Setiap siklus perubahan WAJIB mengikuti 8 langkah berikut:

0. **Issue First** — Setiap perubahan WAJIB didahului oleh GitHub Issue. Buat issue dulu, baru kerja. Reference issue number di commit message (`closes #NN` atau `ref #NN`).
1. **Plan** — analisis kebutuhan, buat todo list, bagi tugas ke agent paralel
2. **Delegate** — dispatch agent untuk setiap task independen
3. **Build** — `npx next build` (frontend) + `npx nest build` (backend) — pastikan kompilasi sukses
4. **Deploy** — `pm2 restart koncolawas-api koncolawas-web` — restart production service
5. **Smoke Test (curl)** — verifikasi halaman live tidak 404/500: `curl -s http://localhost:3002/<path> | grep <expected-text>`
6. **E2E Test (Playwright)** — jalankan Playwright E2E test untuk skenario yang relevan dengan perubahan. Wajib untuk setiap perubahan yang memengaruhi:
   - Login / auth flow
   - Navigasi & routing baru
   - Form submission
   - Tampilan halaman publik
   - Admin panel
   
   Jika belum ada test spec untuk fitur tersebut, agent WAJIB membuat test spec Playwright minimal (happy path) sebelum melanjutkan.
   Test dijalankan dengan: `npx playwright test --project=chromium`
7. **Commit & Push** — git add → commit → push ke GitHub. Commit message WAJIB mention issue number.

> Catatan: Jika build gagal, jangan deploy. Fix dulu sampai build sukses.
> 
> ⚠️ **PENTING**: Langkah 5 (Smoke Test) dan Langkah 6 (E2E Test) adalah dua hal BERBEDA. Smoke test = cek hidup/mati dengan curl. E2E test = verifikasi fungsionalitas dengan Playwright (browser nyata). Keduanya WAJIB dilakukan.
> 
> 🔴 **ISSUE-FIRST RULE**: JANGAN pernah memulai pekerjaan tanpa GitHub Issue. Inisiasi harus dari issue, baru implementasi. Commit message harus mention `closes #N` atau `ref #N`.

---

## Todo — Pengembangan Selanjutnya

### ✅ Completed (MVP2 — sesi 2026-05-30)
- [x] **UI/UX Overhaul**: activity feed, sidebar grouping, progressive disclosure — #43
- [x] **Mobile Navigation**: bottom nav 4 tab + more sheet — #44
- [x] **Business Directory**: direktori usaha alumni dengan approval flow & kategori — #41
- [x] **Volunteer Skill / Alumni Mengajar**: direktori keahlian alumni yang bisa di-share — #42

### ✅ Completed (sesi 2026-05-31)
- [x] **#45** — Add record alumni berprestasi (49 entries dari HTML → seed, dedup 4 internal + 6 overlap, 57 total) — ref #45

### Medium Priority
- [ ] **Dashboard admin**: charts/grafik (current: basic stats 4 KPI cards)
- [ ] **Notifikasi email**: konfirmasi registrasi, reset password (jika non-Google)
- [ ] **Mobile responsive**: refine layout untuk tampilan HP
- [ ] **CI/CD pipeline**: GitHub Actions untuk lint, build, deploy

### Low Priority
- [ ] **Unit & integration tests**: backend (NestJS) + frontend (Vitest/Cypress)
- [ ] **PWA / offline mode**: service worker untuk akses tanpa internet
- [ ] **Dark mode**: toggle tema gelap
- [ ] **Gallery foto angkatan**: upload & tampilkan foto momen sekolah
- [ ] **SEO & Open Graph**: meta tags untuk setiap halaman publik

> **Catatan status aktual per 2026-05-31:**
> - ✅ **Forum diskusi** — SUDAH implement (threads, nested comments/replies, likes, pagination, categories)
> - ✅ **Upload foto profil** — SUDAH implement (2MB limit, preview, disk storage, old-file cleanup)
> - ✅ **Pencarian & filter alumni** — SUDAH implement (search by nama/NIS, filter by tahun/jurusan/status)
> - ✅ **Export data alumni** — SUDAH implement (CSV + Excel + Stats, admin-only)
> - ✅ **Business Directory (#41)** — SUDAH implement (CRUD, approval, kategorisasi, profile tab)
> - ✅ **Volunteer Skill (#42)** — SUDAH implement (CRUD, kategorisasi, profile tab, admin panel)
> - ✅ **UI/UX Sidebar Grouping (#43)** — SUDAH (4 grup: Jaringan, Karir & Usaha, Komunitas, Admin)
> - ✅ **UI/UX Mobile Nav (#44)** — SUDAH (bottom nav 4 tab + BottomSheet)
> - ✅ **Alumni Berprestasi (#36)** — SUDAH (dashboard spotlight + seed 18 alumni)
> - ✅ **Alumni Berprestasi Card Redesign (#46)** — SUDAH (team member layout, HTML escaping fix)
> - ✅ **Floating Filter FAB (#47)** — SUDAH (FAB bottom-right, slide-up panel, sticky heading)
> - ✅ **Mobile Overflow Fix (#48)** — SUDAH (min-w-0 overflow-x-hidden, flex-wrap pagination)
> - ✅ **Profil Saya Link (#49)** — SUDAH (sidebar group + header dropdown)
> - ✅ **Sticky Header + Logo (#50)** — SUDAH (sticky top-0, logo kiri, h-14 mobile)
> - 🟡 **Dashboard admin** — basic stats (4 KPI cards + recent users + export), belum ada charts/grafik
> - ❌ **Registrasi alumni mandiri** — belum ada
> - ❌ **Notifikasi email** — belum ada
> - ❌ **Mobile responsive** — masih perlu refine
> - ❌ **CI/CD pipeline** — belum ada
> - ❌ **SEO & Open Graph** — baru terpasang di `/pengurus`, sisanya belum
>
> ⚠️ **CDN-First untuk Foto Alumni Berprestasi**: Semua foto featured alumni WAJIB langsung disimpan ke CDN jsDelivr (`frontend/public/images/alumni-berprestasi/`), bukan hotlink dari sumber asli. Workflow detail di `docs/osint-agent-system.md`.

---

## Patroli GitHub Issues — 2026-05-31 (updated)

### ✅ Terakomodir (Closed/Selesai)
- **#9–#29** Seluruh issues fase MVP1 (login, profil, admin, forum, jobs, notifikasi, dll)
- **#30** Import Google Sheets timeout fix (createMany + chunk)
- **#31** Kelas 1/2/3 tracking
- **#32** Stats overview fix (byYear → byTahunLulus)
- **#33** Kelas 3 di kartu alumni
- **#35** Migrasi dari platform lama
- **#36** Success Stories / Wall of Fame
- **#37** Landing page UX + image compression
- **#38** Build Prisma client hilang di dist (symlink fix)
- **#39** Login 2x klik fix (state:false, session:false)
- **#41** Business Directory by Alumni (CRUD, approval flow, profile tab)
- **#42** Volunteer Skill / Alumni Mengajar (CRUD, kategorisasi, admin panel)
- **#43** Dashboard Activity Feed + Sidebar Restructure (4 grup navigasi)
- **#44** Mobile Navigation Redesign (bottom nav 4 tab + BottomSheet)
- **#46** alumni-berprestasi redesign card layout — team member style + fix HTML escaping
- **#47** Redesign alumni-berprestasi filter — floating icon + sticky heading
- **#48** Align /alumni card layout + fix mobile overflow horizontal
- **#49** Add Profil Saya link to sidebar and header dropdown
- **#50** Mobile layout: sticky header with logo + profile, consistent bottom nav

### ❌ Belum Terakomodir / Open Issues (per 2026-05-31)
- **#34** MVP2 Planning — Admin unit, gallery alumni, referral code, donasi (roadmap revised)

### ✅ Closed via commit (baru ditutup)
- **#40** Redesign halaman pengurus periode sebelumnya (2022–2025) — commit `24867cb` (iprakom)
- **#41** Business Directory — commit `be55945` + `e293db2` + `b5697ce`
- **#42** Volunteer Skill — commit `e10f91f` + `256421f`
- **#43** Dashboard Feed + Sidebar — commit `be55945` + `a1af1b5`
- **#44** Mobile Navigation — commit `a1af1b5`
- **#46** Redesign alumni-berprestasi cards — team member layout + fix HTML escaping — commit `32c6965`
- **#47** Floating filter icon + sticky heading — commit `ccf6534`
- **#54** CDN migration featured photos — commit `818c753`
- **#48** Align /alumni layout + fix mobile overflow — commit inline session
- **#49** Add Profil Saya link to sidebar and header — commit inline session
- **#50** Sticky header with logo + consistent bottom nav — commit inline session

---

## Session 2026-05-29 (Profil Pengurus IKA)

### Changes
1. **Halaman `/pengurus`**: Halaman profil pengurus IKA dengan tab (Dewan Pembina/Pengawas/Pengurus Pusat/Bidang), card per profil, ditautkan di footer landing page (tidak di sidebar).
2. **Data profil lengkap**: ~70+ entries di `lib/profil-pengurus.ts` dengan field: nama, jabatan, estimasi angkatan, posisi terakhir, ringkasan, foto, kontak LinkedIn/IG, sumber.
3. **Integrasi OSINT jenova.ai**: Data baru — Ibnu Hadyanto (Telkom), Adi Surya Tri Wibowo (Dimensi Gagas), Jaka Pujiyono (Deloitte), Kurnia → Kurnia Adhiwibowo, kontak medsos untuk tokoh publik.
4. **GitHub sync**: commit `bc9911c`
5. **Deploy prod**: pull → build → `pm2 restart koncolawas-web` — verified ✅

### Todo — Profil Pengurus (Prioritas)
1. ✅ **Verifikasi Ali Mahfud** — Drs. H. Ali Mahfud, S.H. — Hakim PA Surakarta (bukan Full Stack Engineer)
2. 🟡 **Cari foto profil** — sebagian sudah (Susilo, Amir, Agus S, Wimboh, Hartanto, Didik, Hadi, Sumardi, Agus I, Suwarno); sisanya via LinkedIn/IG
3. 🔴 **Data masih hilang** — Dun Sridadi, Sayoeti Sukandi, Yulianto (ambigu) — hubungi sekretariat IKA via IG @ikasmansaboy atau Facebook; mayoritas anggota bidang tidak punya jejak digital
4. ✅ **Tambahkan kontak** — LinkedIn/IG untuk semua profil yang memungkinkan
5. ✅ **SEO & meta tags** — title, description, OG tags di `/pengurus` via `useEffect`
6. ✅ **Link di footer app-shell** — untuk pengguna yang sudah login

---

## Session 2026-05-29

### Changes
1. **Login**: Hapus tombol login tengah di landing page, sisakan yang kanan atas
2. **Logo sekolah**: Download dari sman1boyolali.com, pasang sebagai favicon + tampil di beranda
3. **Stats angkatan**: Fix mismatch `byYear` → `byTahunLulus` di landing page
4. **Onboarding flow**: AppShell cek profile setelah login — jika 404 atau tahunMasuk/tahunLulus kosong, redirect ke `/profile`. Banner kuning di profile jika belum lengkap. Tahun Masuk/Lulus diberi red asterisk
5. **Gravatar fallback**: Foto alumni pakai `user.avatarUrl` (dari Google) jika `fotoProfil` belum ada
6. **Sorting alumni**: Default diubah ke `createdAt desc` (terbaru duluan)
7. **Issue #23**: Fix batch import — ganti `create()` loop jadi `createMany()` + chunk 500 rows
8. **README**: Tambah CHANGELOG section, update fitur table
9. **Build verification**: `npx next build` + `npx nest build` sukses ✅

### Issues
- **PM2 stale build**: Perubahan tidak nampak di live karena PM2 masih jalan dengan build lama (uptime 21h). Root cause: workflow tidak menyertakan `pm2 restart` setelah build.

---

## Session 2026-05-29 (Lanjutan)

### Changes
1. **Logo fix**: Ganti logo dari sman1boyolali.com → Wikipedia (`upload.wikimedia.org/wikipedia/id/1/10/Logo_SMAN_1_Boyolali.png`). Sebelumnya pakai logo sekolah umum yang salah.
2. **Deployment docs**: Update workflow Build → **Deploy** → Check E2E. Tambah peringatan ⚠️ agar selalu `pm2 restart` + `curl` verifikasi setelah build.
3. **Jest ESM fix**: Delegated ke background agent.
4. **#34 MVP2 Planning**: Mulai dibahas — donasi, admin unit, gallery alumni, referral code.

### Build verification
- `npx next build` sukses (21.4s, TS pass, 23 routes)
- `npx nest build` sukses
- `pm2 restart koncolawas-api koncolawas-web` ✅
- Live test: logo ✅, login button ✅, stats (71 alumni, 4 angkatan) ✅

---

## Session 2026-05-29 (Malam)

### Changes
1. **Favicon & logo**: Logo dikompres 212KB→38KB (pngquant). Favicon.ico dibuat dari logo compressed agar load lebih cepat.
2. **Landing page redesign**: Header dihapus total. Tombol login cuma 1 di tengah (bawah nama sekolah). Tampilan lebih simpel dan fokus.
3. **Login 2x klik fix**: Root cause — `passport-google-oauth20` default `state:true` (CSRF) + Passport `session` default tanpa session middleware. Fix: tambah `state: false` di GoogleStrategy + `session: false` di PassportModule.
4. **Button rebrand**: "Login with Google" → "Masuk sebagai Alumni" + SVG logo Google di kiri.
5. **Logout redirect**: Semua redirect `/login` diganti ke `/` (landing page), termasuk di auth-context, api.ts, callback, admin layout, app-shell.
6. **Build fix**: Backend `npm run build` sudah pakai symlink `dist/src/generated → ../../src/generated` untuk Prisma client, tapi sebelumnya dijalanin `npx nest build` langsung tanpa symlink. Build script sudah benar (`npm run build`).

### Bugs Fixed (sebagai issue tracker)
- **#39** Login perlu 2x klik — fixed via `state:false` + `session:false`
- **#37** Landing page jelek & lambat — fixed via redesign + kompresi gambar
- **#38** Build gagal karena Prisma client hilang — fixed via `npm run build` (pakai symlink)

### Build verification
- `npx next build` sukses (13.2s, TS pass, 23 routes)
- `npm run build` backend sukses
- `pm2 restart koncolawas-api koncolawas-web` ✅
- Live test: logo compressed ✅, "Masuk sebagai Alumni" ✅, Google SVG ✅, stats (71, 4, 1) ✅, no header ✅, 1 login button ✅

---

## Session 2026-05-29 (Profil Pengurus — Final)

### Changes
1. **Bupati Boyolali dikoreksi**: Kandiyono → **Agus Irawan** (bupati terpilih 2025-2030) + foto Wikipedia.
2. **Prof. Suwarno ditambahkan**: Guru Besar Teknik Elektro ITB, top 2% Stanford, foto dari ITB.
3. **Bio diperkaya**: Susilo Siswoutomo (lahir Boyolali, ITB 1970), Wimboh Santoso (S1 UNS 1983, PhD Loughborough), Agus Suryonugroho (Akpol 1991), Didik Haryadi (lahir 12 Nov 1976).
4. **SEO meta tags**: title/description/OG untuk `/pengurus`.
5. **Footer link**: "Profil Pengurus IKA" di app-shell untuk user login.
6. **Halaman `/pengurus/sebelumnya`**: Struktur 2022-2025 dari SK, 80+ entri.
7. **Cross‑reference SK**: 10 profil dicocokkan dengan angkatan A-xx.

### Data terverifikasi (Perplexity + OSINT)
- **Ali Mahfud** → Drs. H. Ali Mahfud, S.H. — Hakim PA Surakarta (bukan Full Stack Engineer)
- **Andy Arvianto** → Dir. SDM PT Pertamina (Juni 2025)
- **Bambang Widjajarso** → Trainer Pusdiklat PSDM Kemenkeu
- **Wartono** → IG @wartonoboyolali

### Blocked (perlu kontak internal)
- Dun Sridadi, Sayoeti Sukandi, Yulianto — tidak ditemukan data publik
- Mayoritas bidang/sub-bidang tidak punya jejak digital

### Commit history (8 commits dari sesi ini)
- `24867cb` — feat: redesign halaman pengurus periode sebelumnya (iprakom) — closes #40
- `dc89175` — docs: update session profil pengurus final
- `e756351` — feat: tambah Prof. Suwarno, koreksi Bupati Agus Irawan, perkaya bio
- `98df049` — Halaman kepengurusan lama + cross-ref SK
- `ed34863` — Update profil: foto Amir Yanto, Hadi Pratomo, Sri Yunanto
- `22a5a6a` — Update data: Ali Mahfud, Andy, Bambang, foto Hartanto & Didik, SEO, footer
- `5a0047a` — update: Kurnia Adhiwibowo — data lengkap (BPS)
- `2994241` — docs: update AGENTS.md — todo profil pengurus & session log

## Session 2026-05-30 — OSINT Profil Pengurus (Paralel Agent)

### Changes
1. **Google Sheets sync**: Kedua sheet (`PENGURUS LAMA` & `PENGURUS BARU`) diseragamkan — 24 kolom identik (No–Catatan Internal). Bold header + freeze row.
2. **OSINT 4 agent paralel**: 
   - **LAMA Top** (33 profil: Dewan Pembina + Penasehat + Pakar) → 10 foto, 9 LinkedIn, 6 Wikipedia, 20 ringkasan baru
   - **LAMA Pusat** (62 profil) → 4 foto, 2 LinkedIn, 12 ringkasan baru, 47 tanpa jejak digital
   - **BARU Top** (28 profil: Dewan Pembina + Pengawas) → 7 foto, 6 LinkedIn, 4 Instagram, 15 ringkasan diperkaya
   - **BARU Staff** (39 profil: Pengurus Pusat + Bidang) → 1 foto, 8 LinkedIn, 6 Instagram, 39 ringkasan
3. **Sheet → TypeScript sync**: Script `sync-sheet-to-ts.js` mengupdate `profil-pengurus.ts` (+271 field patches) dan `profil-pengurus-lama.ts` (+50 field patches) — foto, ringkasan, LinkedIn, Instagram, kontak, gender, sumber dari hasil OSINT.
4. **Figur kunci teridentifikasi**: 
   - LAMA: Jend. Mulyono, Mayjen Sumardi, Djoko Kirmanto, Irjen Erwin Triwanto, Prof. Suwarno (semua +Wikipedia & foto), Sumarno (Sekda Jateng), Yoyok Hery (Warung SS), Ratri Survivalina (Kadinkes)
   - BARU: Andy Arvianto (Dir SDM Pertamina), Kurnia Adhiwibowo (BPS), Adi Surya Tri Wibowo (Ketum HDII), Ibnu Hadyanto (Telkom), Jaka Pujiyono (Deloitte)
5. **Unified pipeline**: `export-sheet-json.js` → `merge-osint-results.js` → `sync-sheet-to-ts.js`

### Sheet → Code Pipeline
```
Google Sheet (master data)
  → export-sheet-json.js (baseline JSON per kategori)
  → OSINT agents (webSearch, findings JSON)
  → merge-osint-results.js (push ke sheet)
  → sync-sheet-to-ts.js (patch TypeScript dari sheet)
  → npx next build + npm run build + pm2 restart
```

### Delta (PENGURUS LAMA)
| Field | Sebelum | Sesudah |
|-------|---------|---------|
| Foto | 5 | **13** |
| Ringkasan | 12 | **93** |
| Wikipedia | 0 | **8** |
| LinkedIn | 0 | **6** |
| Instagram | 0 | **2** |
| Sumber | 0 | **31** |

### Delta (PENGURUS BARU)
| Field | Sebelum | Sesudah |
|-------|---------|---------|
| Foto | 10 | **12** |
| Ringkasan | 43 | **65** |
| Wikipedia | 0 | **6** |
| LinkedIn | 0 | **10** |
| Instagram | 0 | **9** |
| Sumber | 46 | **66** |

### Remaining P1 (butuh foto)
- **82 profil LAMA** + **55 profil BARU** = **137 tanpa foto**
- Foto sumber terbuka adalah bottleneck; perlu kontak internal IKA via IG/FB

### Build & Deploy
- `npx next build` sukses — 26 routes ✅
- `npm run build` backend sukses ✅
- `pm2 restart koncolawas-web koncolawas-api` ✅
- Live verified: `/pengurus` (Susilo, Agus Irawan, Sumardi ✅), `/pengurus/sebelumnya` (Seno Kusumoarjo, Budiyanto ✅)

---

## Session 2026-05-30 (MVP2 Planning — Business Directory)

### PM Analysis: Ide dari Founder

Founder menyampaikan 7 area pengembangan untuk MVP2. Sebagai PM kritis, dilakukan validasi:

| Ide | Verdict | Alasan |
|-----|---------|--------|
| **Business Directory** | ✅ **P1 - Kerjakan** | Inti permintaan. CRUD sederhana, high impact, no payment integration |
| **Volunteer Skill** | ✅ **P2 - Kerjakan** | Clear value, relatif ringan, integrasi profil |
| **Collaboration (Cari Mitra)** | ✅ **P3 - Bagian dari Bisnis** | Flag + admin mediasi, lightweight |
| Job Opportunity | ❌ **Skip** | Sudah ada Jobs Board |
| Promotion tipis-tipis | ❌ **Skip** | Tercover Business Directory |
| Program SMA | ⏸️ **Tunda** | Terlalu broad, perlu definisi |
| Crowd Funding | ⏸️ **Tunda ke MVP3** | Butuh payment gateway, legal, risiko tinggi |

### Issues Created
- **#41** — [MVP2] Business Directory by Alumni (P1)
- **#42** — [MVP2] Volunteer Skill / Alumni Mengajar (P2)
- **#34** — Roadmap direvisi: Business Directory & Volunteer Skill sebagai prioritas baru. Admin Unit, Gallery, Referral, Donasi ditunda.

### Teknis
- **Business Directory**: model `AlumniBusiness`, enum `BusinessCategory` + `BusinessStatus`, approval flow, upload foto, halaman `/bisnis`
- **Volunteer Skill**: model `AlumniSkill` + `SkillRequest`, enum `SkillFormat` + `SkillLevel`, halaman `/alumni-mengajar`
- Pattern mengikuti `success-stories` (controller + service + dto + module, tanpa base CRUD)
- Frontend: halaman baru di `(app)/bisnis` dan `(app)/alumni-mengajar` sebagai Client Component, pakai `fetchApi` dari `@/lib/api`

### UI/UX Analisis Feature Bloat
Platform punya 8+ fitur → user non-teknis kewalahan. Mitigasi via 3 strategi:
1. **Activity Feed** — Dashboard jadi unified feed lintas fitur (bukan 3 KPI card + 2 widget terisolasi)
2. **Sidebar Grouping** — 10 menu flat → 4 kategori expandable (Jaringan, Karir & Usaha, Komunitas, Profil)
3. **Progressive Disclosure** — fitur muncul bertahap berdasarkan stage user (baru login → profile OK → aktif → senior)

### Issues Created
- **#41** — [MVP2] Business Directory by Alumni (P1)
- **#42** — [MVP2] Volunteer Skill / Alumni Mengajar (P2)
- **#43** — [UI/UX] Dashboard Activity Feed + Sidebar Restructure + Progressive Disclosure
- **#44** — [UI/UX] Mobile Navigation Redesign — Bottom Nav + More Sheet
- **#34** — Roadmap direvisi: prioritas baru UI/UX #43 #44 + Business Directory #41 + Volunteer Skill #42. Admin Unit, Gallery, Referral, Donasi ditunda.

---

## Session 2026-05-30 (Extended — MVP2 Implementation)

### Deployment Issues & Fixes

#### Business Directory (#41) — Complete gaps
- **Fix 1** — Backend `business.service.ts`: Added `mapBusiness()` helper to normalize response shape (`noKontak`→`kontak`, `linkWebsite`→`website`, `linkInstagram`→`instagram`, `alumniProfile.user`→`pemilik` with `{ id, name, avatarUrl }`). Exposed `userId` in detail. Includes related businesses by same owner.
- **Fix 2** — Profile page: Added "Usaha Saya" tab with full CRUD (list, add via modal, edit, delete confirmation, own `BUSINESS_KATEGORI` constant).
- **Fix 3** — Business detail page `/bisnis/[id]`: Edit/Hapus buttons for listing owner (checks `useAuth` → `isOwner`), inline edit modal, delete confirmation dialog.
- **Fix 4** — Admin nav sidebar: Added `/admin/business` link with `BriefcaseIcon`.

#### Volunteer Skill (#42) — Complete gaps
- Created `/alumni-mengajar/[id]/page.tsx` — skill detail page with edit/delete modals, owner check, loading/error states, info grid.
- Created `/admin/alumni-skill/page.tsx` — admin panel with table, kategori filter, pagination, delete confirmation.
- Added "Skill Saya" tab to Profile page — full CRUD (add/edit modal, delete confirmation). Mirrors business tab pattern.
- Added admin nav link for `Alumni Skill` with `GraduationIcon`.

#### Dashboard & Sidebar (#43)
- Removed redundant "Beranda" nav group from sidebar (had single child "Dashboard").
- Dashboard already has unified activity feed from 5 sources (forum, jobs, business, success stories, skills) with infinite scroll.

#### Mobile Navigation (#44)
- Already implemented: 4 tabs (Beranda, Jaringan, Karir, Lainnya) + BottomSheet component with slide-up animation.

#### Bug Fixes
- **Profile business tab infinite loop**: Added `businessesFetchedRef` (`useRef(false)`) guard to prevent re-fetch when user has 0 businesses.

#### Alumni Berprestasi — Success Stories (#36 Dashboard Spotlight)
- **Dashboard**: Added "Alumni Berprestasi" spotlight section between discover cards and footer. Gradient amber/yellow background. Displays up to 5 featured alumni with avatar (initial letter fallback), name, achievement, angkatan. Fetches from `GET /success-stories/featured`.
- **Seed data**: Created `prisma/seed-success-stories.mjs` with 18 notable alumni entries (Susilo Siswoutomo, Agus Irawan, Wimboh Santoso, Prof. Suwarno, Sumardi, Djoko Kirmanto, Ali Mahfud, Mulyono, Erwin Triwanto, Andy Arvianto, Didik Haryadi, Kurnia Adhiwibowo, Hartanto, Bambang Widjajarso, Adi Surya, Ibnu Hadyanto, Sumarno, Hadi Pratomo). 11 marked `isFeatured: true`. Only inserts if table empty.
- **Deploy**: Pull → build → seed → verify API ✅

### GitHub Issues Management
- **#34** MVP2 Plan — Updated & closed (superseded by individual issues)
- **#36** Success Stories — Dashboard spotlight added, 18 entries seeded, closed
- **#41** Business Directory — Updated & closed (P1 done, P2/P3 deferred)
- **#42** Volunteer Skill — Updated & closed (all P1 gaps filled)
- **#43** Dashboard Feed + Sidebar — Updated & closed (core done, progressive disclosure deferred)
- **#44** Mobile Navigation — Updated & closed (all items done)

### Build & Deploy
- Both backend and frontend build passed (Frontend: 30 routes ✅)
- Committed and pushed to GitHub
- SSH deploy to production — git pull, seed 18 success stories, verify `GET /api/success-stories/featured` returns 10 featured entries ✅
- PM2 restart verified

### Todo — Pekerjaan Rumah Business Directory
- **P2:** Photo upload untuk setiap usaha (current: pakai default icon)
- **P2:** Fitur "Tertarik" / Express Interest dari user lain
- **P2:** Testimonial / review untuk setiap usaha
- **P3:** Approve/reject langsung dari list admin (current: edit modal)

---

## Session 2026-05-31 — Alumni Berprestasi Card Redesign + OSINT System

### Issue #46 — Created
- Issue: [Redesign alumni-berprestasi cards — team member layout + fix HTML escaping](https://github.com/camagenta/koncolawasboyolali/issues/46)
- Closing commit: `32c6965` — ref #46

### Bug Fixed
- **HTML escaping `">` visible text**: `getPhotoHtml()` used inline `onerror` attribute with double-quoted HTML inside double-quoted attribute. Fix: replaced with `handleImageError()` JS function that receives DOM element directly, avoiding HTML attribute concatenation.

### Design Changes
- **Card layout**: From compact top-down (64px circular photo) → **team-member style**: 120x120px photo left, info panel right. On mobile (<640px): flex-direction column, photo stacks on top.
- **Typography**: From Inter/system → **Playfair Display** (serif for names) + **Source Sans 3** (sans for body), loaded via Google Fonts.
- **Info hierarchy**: badge (angkatan + gender inline) → nama (big serif) → nickname → posisi (amber left border) → ringkasan → social icons → citation block.
- **Gender**: Moved from separate card-footer into inline with badge: `🎓 Angkatan 1980 · ♂ Laki-laki`
- **Social media**: Added `linkedin`, `instagram`, `twitter` optional fields to all 49 entries (empty). SVG icon row renders only when data present.
- **Citation extraction**: Auto-splits `ringkasan` on `"Informan:"` — extracts source to dedicated `card-citation` block at card bottom (dashed border, italic).
- **Color palette**: Navy `#1e3a5f` + amber `#d97706` accent, radial gradient overlay on hero.

### OSINT System Documentation
- Created `docs/osint-agent-system.md` (297 lines) — retrospective hit rates, source priority chains per profile type, Playwright bypass protocol, agent prompt template, verification workflow, batch runner script, quick reference URL patterns by institution.
- Created `scripts/merge_findings.js` — database of 49 alumni photo findings with confidence and source attribution.

### Git Issue-First Workflow Reinforcement
- Workflow siklus development di AGENTS.md diperbarui: **Step 0 — Issue First** ditambahkan sebagai langkah wajib.
- Commit message WAJIB mention issue number (`closes #NN` / `ref #NN`).
- Semua inisiasi pekerjaan harus dari GitHub Issue, bukan dari chat langsung.

### Build & Deploy
- `npx next build` sukses (30 routes ✅)
- `pm2 restart koncolawas-web` ✅
- Live verified: `/alumni-berprestasi.html` loads, cards render with photos ✅

### Commit
- `32c6965` — feat: redesign alumni-berprestasi cards team member layout fix HTML escaping

---

## Session 2026-05-31 — Filter Floating Icon + Sticky Heading

### Issue #47 — Created
- Issue: [Redesign alumni-berprestasi filter — floating icon + sticky heading](https://github.com/camagenta/koncolawasboyolali/issues/47)
- Closing commit: `ccf6534` — ref #47

### Perubahan
- **Hapus sticky filter bar**: Persistent `.controls` dengan `position: sticky; top: 0;` yang memakan vertical space saat scroll dihapus.
- **Floating Action Button (FAB)**: Tombol filter ikon di pojok kanan bawah (`position: fixed; bottom: 1.5rem; right: 1.5rem;`), circular 56px, warna navy, bayangan.
- **Filter panel modal**: Klik FAB → slide-up panel dari bawah dengan handle + judul "Filter & Cari" + search input + 3 dropdown (angkatan, gender, foto) + tombol Terapkan/Reset.
- **Sticky heading**: Element sticky baru `.sticky-heading` — hanya menampilkan "🏆 Alumni Berprestasi" + result count. Compact, backdrop-filter blur.
- **Close mechanism**: Klik overlay (backdrop), klik "Terapkan", atau tekan Escape → panel tertutup.
- **Reset filters**: Tombol "Reset" mengosongkan semua filter, menjalankan `filterCards()`, dan menutup panel.
- **Print styles**: `sticky-heading`, `filter-fab`, `filter-overlay` ikut disembunyikan di print.

### Teknis
- File: `frontend/public/alumni-berprestasi.html` — 869 lines (naik dari 700)
- CSS: ~170 baris baru untuk sticky-heading, filter-fab, filter-overlay, filter-panel, filter-actions
- JS: 3 fungsi baru (`toggleFilterPanel`, `closeFilterPanel`, `resetFilters`) + Escape key listener
- Semua filter logic tetap sama (filterCards() pakai DOM IDs yang tidak berubah)
- Mobile: FAB 48px, filter-panel padding 1rem
- Print: tambah `.sticky-heading, .filter-fab, .filter-overlay` ke `display: none`

### Build & Deploy
- `npx next build` sukses (30 routes ✅)
- `pm2 restart koncolawas-web` ✅
- Live verified: `curl -s http://localhost:3002/alumni-berprestasi.html | grep -o 'sticky-heading\|filter-fab'` ✅

---

## Session 2026-05-31 — Align /alumni card layout with /sukses & /jobs + Fix mobile overflow

### Issues
- #48 — (informal) /alumni overflow horizontal di mobile

### Perubahan

#### Restruktur Alumni Cards (sesuai /sukses)
- Filter card di /alumni restruktur mengikuti pola /jobs: `p-4`, `gap-4` di grid, spacing konsisten
- Grid cards di /alumni restruktur mengikuti pola /sukses: single centered stack (avatar, nama, angkatan, kelas3+domisili inline, status badge), padding `p-4 sm:p-5`, spacing internal lebih rapat
- Skeleton loading diupdate mengikuti layout centered yang baru

#### Fix Horizontal Overflow (Root Cause)
- **Root cause**: `frontend/src/components/layout/app-shell.tsx:88` — Div `flex-1 flex-col` di dalam flex container. Default CSS `min-width: auto` pada flex item mencegah penyusutan di bawah intrinsic width konten. Saat viewport 375px, container memaksa jadi 551px.
- **Fix**: Tambah `min-w-0 overflow-x-hidden` ke content wrapper di app-shell — flex item bisa shrink sesuai parent.
- **Pagination**: Ganti `overflow-x-auto > w-max` dengan `flex-wrap` agar tombol wrap alami tanpa overflow.

#### Verifikasi (Playwright di 375px viewport)
| Halaman | docScrollWidth | Status |
|---------|---------------|--------|
| `/alumni` | 375px | ✅ (was 551px) |
| `/sukses` | 375px | ✅ |
| `/jobs` | 375px | ✅ |
| `/bisnis` | 375px | ✅ |
| `/alumni-mengajar` | 375px | ✅ |

- 320px viewport juga verified: docScrollWidth == 320 ✅
- Bottom sheet di /alumni renders dengan overlay + nav panel ✅
- Pagination wraps ke 2 baris (1-5 atas, 6-7+Selanjutnya bawah) ✅
- `npx next build`: 30 routes, no errors ✅
- `pm2 restart koncolawas-web koncolawas-api` ✅
- Belum di-commit (inline session, belum ada GitHub Issue formal)

### File Changed
- `frontend/src/components/layout/app-shell.tsx` — `min-w-0 overflow-x-hidden` pada flex wrapper (line 88)
- `frontend/src/app/(app)/alumni/page.tsx` — restruktur filter card + grid cards + pagination flex-wrap

---

## Handoff System

Handoff disimpan di `handoffs/` (committed ke git) untuk sync konteks antar environment.

### Handoff Wajib Diikuti Git Sync
Setiap kali handoff dijalankan, agent WAJIB:
1. Simpan file handoff ke `handoffs/<date>-<topic>.md`
2. `git add handoffs/<file>` + `git commit -m "docs: handoff <date> — <ringkasan>"` + `git push`
3. Update `Latest Handoff` di AGENTS.md

Handoff hanya output teks tanpa commit = **TIDAK SAH**.

### Latest Handoff
- `handoffs/2026-05-31-issue51.md` — pentest remediasi, login fix, E2E planning
- `handoffs/2026-05-31-telegram-notification.md` — Telegram bot notification, DB-based recipients, bot commands, FB group button

---

## Session 2026-05-31 — Patroli & Sync GitHub Issues

### Findings
1. **#41–#44 (MVP2)** — Semua sudah diimplementasi di kode ✅ tapi AGENTS.md & README belum mencerminkan
2. **#45** — Seed hanya 18 alumni dari #36; 49+ entries dari body issue #45 belum masuk
3. **#46–#50** — Semua sudah diimplementasi di kode ✅ (dari remote Git pull, parallel session)

### Actions Taken
- **AGENTS.md** — Todo list direvisi: MVP2 items dipindah ke ✅ Completed. Catatan status aktual diperbarui. Hanya #45 yang masih open. Patroli GitHub Issues di-update dengan #46-#50 di Terakomodir.
- **README.md** — Business Directory, Volunteer Skill, Sidebar Grouping, Mobile Nav ditambahkan ke tabel fitur ✅ Selesai.

---

## Session 2026-05-31 — Alumni Berprestasi Seed Sync (#45)

### Issues
- **#45** — Add record alumni berprestasi (~49 entries dari issue body + WAG alumni)

### Perubahan
1. **Extract script** (`scripts/extract-berprestasi-seed.mjs` — one-shot, dihapus setelah selesai): Membaca 49 entries dari `frontend/public/alumni-berprestasi.html`, menduplikasi internal (#5=#3 Gunaryadi, #23=#6 Muhadi, #28=#8 Jupri Bandang, #47=#43 Suyitno), mencocokkan dengan seed existing (18 entries — 6 overlap: Susilo, Djoko Kirmanto, Mulyono, Sumardi, Erwin Triwanto, Sumarno), dan menghasilkan 39 entries baru.
2. **Seed file**: `backend/prisma/seed-success-stories.mjs` diperbarui dari 18 → 57 entries. Data diperkaya dengan `photoUrl` (20 entries dengan foto) dari HTML.
3. **Database**: Seed dijalankan — `Seeded 57 success stories`.
4. **Verifikasi**: Prisma query langsung ke DB — count=57, featured=13, withPhoto=20 ✅
5. **Build**: Backend (`npx nest build`) ✅, Frontend (`npx next build` — 30 routes) ✅

### Detail Data
| Sumber | Entri | Keterangan |
|--------|-------|------------|
| Seed existing (#36) | 18 | isFeatured sesuai verifikasi manual |
| HTML #45 (49 entries) | 49 | Dari issue body + WAG alumni |
| Internal duplikat #45 | -4 | #5=#3 (Gunaryadi), #23=#6 (Muhadi), #28=#8 (Jupri Bandang), #47=#43 (Suyitno) |
| Overlap dengan seed | -6 | Susilo, Djoko, Mulyono, Sumardi, Erwin, Sumarno |
| **Total baru dari #45** | **39** | |
| **Total final** | **57** | |

### File Changed
- `backend/prisma/seed-success-stories.mjs` — 18 → 57 entries, +photoUrl dari HTML
- `AGENTS.md` — #45 dipindah ke ✅ Completed

---

## Session 2026-05-31 — CDN Migration Featured Photos (#54)

### Issue
- **#54** — Migrate featured alumni photos to CDN (jsDelivr) for faster load

### Latar Belakang
20 foto featured sebelumnya diambil dari sumber eksternal (Wikipedia, universitas, antaranews) — load time bervariasi dan beberapa sumber mulai 404. Perlu dipindah ke CDN global tanpa menyimpan file fisik di VPS.

### Perubahan
1. **17 foto featured** didownload dan disimpan di `frontend/public/images/alumni-berprestasi/` — dari Wikipedia, UNS, ITB, UGM, UII, Unsoed, UT, antaranews, halosemarang, tagar.id, ftmd.itb.ac.id
2. **Seed URLs** diupdate dari sumber eksternal → `cdn.jsdelivr.net/gh/camagenta/koncolawasboyolali@main/frontend/public/images/alumni-berprestasi/{slug}.{ext}`
3. **3 entries tanpa foto** (Sutopo Purwo Nugroho — Wikipedia 404, Agustinus Gatot Hermawan — antaranews 0 bytes, Dr. Subekti Nurmawati — UT unreachable) dihapus dari featured
4. **Seno Samodro** — foto alternatif dari tribunnews (Wikipedia Commons 404)
5. **Safety filter** `isFeatured && photoUrl` ditambahkan di `getFeatured()` landing page
6. **Landing page padding** dikurangi (hero: `pt-20 md:pt-32` → `pt-12 md:pt-20`) agar konten lebih di tengah

### Deployment
- `Seeded 56 success stories` — 17 featured dengan CDN ✅
- Frontend build sukses (30 routes) ✅
- PM2 restart + verifikasi API ✅

### Files Changed
- `frontend/public/images/alumni-berprestasi/*` — 17 photo files (via git)
- `backend/prisma/seed-success-stories.mjs` — URLs diganti ke CDN, Sutopo/Agustinus/Subekti removed from featured
- `frontend/src/app/page.tsx` — safety filter `isFeatured && photoUrl` + hero padding reduced

### CDN-First Rule (baru)
Setiap OSINT foto ke depannya WAJIB langsung disimpan ke CDN (jsDelivr), bukan hotlink. Detail workflow di `docs/osint-agent-system.md`.

### Commit
- `818c753` — feat: migrate featured photos to jsDelivr CDN for faster load — ref #54

---

## Session 2026-05-31 — Telegram Bot Notifications (#53)

### Issue
- **#53** — Telegram Bot Notifications for new user login & profile save

### Perubahan
1. **TelegramModule + TelegramService** (`backend/src/modules/telegram/`): Service baru yang mengirim pesan HTML ke Telegram Bot API via `fetch()` — tanpa npm dependencies tambahan.
2. **Notifikasi login baru** (`GoogleStrategy`): Saat user baru login via Google untuk pertama kali (`isNew === true`), bot mengirim nama, email, dan timestamp ke admin.
3. **Notifikasi simpan profil** (`ProfilesService`): Saat user membuat (`create`) atau memperbarui (`update`) profil, bot mengirim semua data profil yang diinput (nama, no HP, tahun masuk/lulus, kelas 1-3, jurusan, domisili, kecamatan, alamat, LinkedIn, Instagram, status utama, pekerjaan, nama panggilan).

### Konfigurasi
- `TELEGRAM_BOT_TOKEN` — token dari @BotFather
- `TELEGRAM_CHAT_ID` — chat ID admin (dapat dari `getUpdates`)
- Kedua variabel diisi di `backend/.env` (tidak di-commit)

### Files Changed
- `backend/src/modules/telegram/telegram.service.ts` — service baru
- `backend/src/modules/telegram/telegram.module.ts` — module baru
- `backend/src/modules/auth/strategies/google.strategy.ts` — +TelegramService, notif login baru
- `backend/src/modules/auth/auth.module.ts` — import TelegramModule
- `backend/src/modules/alumni/profiles/profiles.module.ts` — import TelegramModule
- `backend/src/modules/alumni/profiles/profiles.service.ts` — +TelegramService, notif create/update
- `backend/src/app.module.ts` — register TelegramModule

---

## Session 2026-05-31 — Telegram Bot DB-Based Recipients + Bot Commands (#53)

### Perubahan lanjutan
1. **Model `NotificationRecipient`** ditambahkan ke Prisma — chatId, label, isActive
2. **TelegramService.notifyAll()** — kirim ke SEMUA recipient aktif dari DB
3. **Webhook endpoint** `POST /api/telegram/webhook` — terima command dari bot
4. **Bot commands**: `/addnotif <chatId> [label]`, `/removenotif <chatId>`, `/listnotif`
5. **Auto-seed** owner sebagai recipient pertama saat aplikasi start
6. **Filter owner**: hanya `TELEGRAM_OWNER_CHAT_ID` yang bisa manage recipients
7. **Set webhook** via `GET /api/telegram/set-webhook` (admin only)

### Files Changed
- `backend/prisma/schema.prisma` — +NotificationRecipient model
- `backend/src/modules/telegram/telegram.service.ts` — notifyAll, handleWebhook, OnApplicationBootstrap
- `backend/src/modules/telegram/telegram.controller.ts` — controller baru
- `backend/src/modules/telegram/telegram.module.ts` — +controller
- `backend/src/modules/auth/strategies/google.strategy.ts` — sendMessage → notifyAll
- `backend/src/modules/alumni/profiles/profiles.service.ts` — sendMessage → notifyAll

---

## Session 2026-06-01 — Facebook Graph API Group Member Count (#56) — WIP

### Status
WIP — App Access Token tidak cukup untuk query grup. Butuh User Access Token dengan `groups_access_member_info`.

### Changes
1. **FacebookModule** (`backend/src/modules/facebook/`): Service + Controller + Module baru
   - `GET /api/facebook/group-stats` — endpoint public
   - App Access Token via App ID + App Secret
   - 5 menit in-memory cache
2. **Frontend landing page** (`frontend/src/app/page.tsx`): fetch group stats, tampilkan badge member count di footer
3. **Deploy**: Production live — endpoint returns `configured: false` karena token insufisien

### Blocker
```
Facebook Graph API error: (#3) Missing Permission
```
Group `member_count` lewat Graph API butuh **User Access Token** (bukan App Token) dengan permission `groups_access_member_info`. Ini butuh setup Facebook Login + App Review.

### Issue
- **#56** — [MVP2] Facebook Graph API group member count

### Files Changed
- `backend/src/modules/facebook/facebook.service.ts` — service baru
- `backend/src/modules/facebook/facebook.controller.ts` — controller baru
- `backend/src/modules/facebook/facebook.module.ts` — module baru
- `backend/src/app.module.ts` — register FacebookModule
- `backend/.env` — add FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, FACEBOOK_GROUP_ID
- `frontend/src/app/page.tsx` — fetch group stats + badge di footer
- `backend/package-lock.json` — fixed Tencent mirror URLs

### Commit
- `ed2e1f4` — feat: Facebook Graph API — group member count in footer — ref #56

