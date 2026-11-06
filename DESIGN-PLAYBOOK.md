# DESIGN-PLAYBOOK — standar UI/UX profesional untuk semua AI

> Dibaca sebelum menulis/mengubah UI, layout, komponen, landing page, atau design system.
> Tujuan: keluaran tidak terlihat seperti template AI. Ini doktrin + peta skill nyata di
> `~/.agents/skills-store/`. Cari skill dengan `sk "<tugas>"` atau `sk --design`.

## 1. Tujuh langkah wajib (jangan lompat)

1. **Brief** — tulis 1 baris: siapa pengguna, 1 aksi utama, suasana (mood) yang dituju.
   Tanpa brief → jangan sentuh kode.
2. **Referensi** — WAJIB riset visual dulu, bukan dari ingatan:
   `dref <url>` (= `python3 ~/.agents/scripts/design-read.py`) untuk Framer, Dribbble,
   Figma Community, situs produk apa pun, atau `dref gambar.png` untuk screenshot lokal.
   Lalu baca `~/.agents/refs/<slug>/notes.md` **dan** buka `desktop-hero.png` (+`mobile.png`)
   dengan tool Read — angka saja tidak menangkap komposisi. Ambil prinsip grid, density,
   tipografi, radius, kontras. Jangan copy aset/brand/teks.
3. **Design contract** — tentukan token dari satu sumber: palette (light+dark), skala tipe,
   spacing (kelipatan 4), radius, shadow, durasi/easing motion. Tulis di `DESIGN.md` proyek
   (scaffold: `cp ~/.agents/templates/DESIGN.md .`). Titik awal token bisa dari
   `dref <url> --tailwind` lalu dirapikan — jangan pakai angka hasil ukur mentah-mentah.
4. **Implementasi token-first** — tidak ada warna/ukuran hardcode di komponen. Semua lewat token.
5. **Semua state** — default, hover, focus-visible, active, disabled, loading, empty, error, success.
   Komponen tanpa state lengkap = belum selesai.
6. **Gate kualitas** — a11y + performa + anti-slop (bagian 4). Ukur dengan `dcheck <url>`
   (exit 1 = belum selesai; cek overflow 360–1440px, kontras, target sentuh, alt, heading,
   label, reduced-motion, drift skala tipe). Perbaiki, jangan hanya melaporkan.
7. **Bukti** — screenshot/ukur sebelum klaim selesai (`playwright`), laporkan angka/exit code.
   Wajib: `dcheck <url>` (gate) + `dvisual <url>` (bandingkan dengan baseline) + `dcopy` untuk
   teks yang tampil di UI. Ketiganya keluar dengan exit code — itu buktinya, bukan tangkapan layar saja.

## 2. Peta kapabilitas → skill lokal (semua path terverifikasi)

| Kapabilitas | Skill utama | Pendamping |
|---|---|---|
| **Baca referensi visual (Dribbble/Framer/Figma/screenshot)** | `design-reference` (`dref <url>`) | `visual-research`, `clearshot`, `design-context-extract` |
| **Visual craft (wajib, UI apa pun)** | `designing-frontend-interfaces` | `designing-user-experience`, `building-accessible-interfaces` |
| **Kritik sebelum kirim** | `dev-design-critique` | `design-review` |
| Arah desain / creative direction | `design-taste-frontend` | `refero-design`, `visual-identity-direction` |
| Anti-slop (wajib default) | `anti-ui-slop` | `design-taste-frontend` |
| Design system & token | `design-system` | `design-tokens`, `design-systems-architecture` |
| Layout & informasi arsitektur | `site-architecture` | `page-layout-builder`, `page-structure-patterns` |
| Landing page | `landing-page-conversion-audit` | `page-cro`, `copywriting` |
| CRO / konversi | `page-cro` | `landing-page-conversion-audit`, `signup-flow-cro` |
| Copywriting | `copywriting` | `content-humanizer` |
| Copy editing | `copy-editing` | `avoid-ai-writing` |
| Positioning & audience | `biz-brand-positioning` | `biz-stp`, `biz-swot` |
| Offer & pricing | `biz-pricing-strategy` | `pricing-strategy` |
| Persuasi (jujur, tanpa manipulasi) | `soc-cialdini` | — |
| Brand consistency & voice | `brand-voice` | `biz-brand-positioning` |
| Accessibility (WCAG 2.2 AA) | `accessibility` | `accessibility-auditing` |
| Performance / Core Web Vitals | `nextjs-performance` | `auditing-performance` |
| Motion & animation | `motion-foundations` | `motion-patterns`, `motion-engineering`, `micro-interaction` |
| Form & lead capture | `form-cro` | `react-forms` |
| Signup & onboarding | `signup-flow-cro` | `form-cro` |
| Gambar / aset visual | `imagegen-frontend-web` | `generating-images`, `ecommerce-image-workflow` |
| SEO & AI search | `seo` | `seo-audit`, `update-llms` (llms.txt) |
| Structured data / JSON-LD | `schema-markup` | `seo` |
| Analytics & consent | `analytics-tracking` | — (consent: tulis manual, hormati GPC) |
| Internasionalisasi | `i18n-frontend-implementer` | — |
| Blog & CMS | `content-strategy` | `content-management-systems` |
| Legal & privacy | — (belum ada skill lokal) | tulis draf + placeholder, bukan fakta karangan |
| E-commerce / checkout | — (belum ada skill lokal generik) | `shopify-*` hanya untuk Shopify |
| QA visual / screenshot | `playwright` | `design-review` |

Cara muat: untuk UI apa pun mulai dari `sk -l designing-frontend-interfaces` (craft visual +
rantai wajib `designing-user-experience` dan `building-accessible-interfaces`), lalu
`sk -l anti-ui-slop`. Maks 2 skill per tugas.

## 3. Aturan visual (non-negotiable)

- **Satu aksi utama per halaman.** CTA dominan jelas; navigasi tidak boleh bersaing.
- **Hierarki nyata:** 1 headline besar, maks 2 tingkat tipe untuk body; jangan semua sama berat.
- **Density disengaja:** pilih lapang ATAU padat, jangan campur acak. Spacing dari skala (4/8/12/16/24/32/48/64).
- **Tipografi bertanda tangan:** pilih 1 display + 1 text, batasi 2 keluarga. Line-height body 1.5–1.7,
  measure 60–75 karakter. Jangan pakai font default sistem sebagai "keputusan desain".
- **Warna:** 1 warna aksi, 1 netral dominan, 1 aksen. Kontras teks ≥ 4.5:1 (≥ 3:1 untuk teks besar).
  Dark mode bukan inversi otomatis — atur ulang token.
- **Kedalaman:** pilih satu bahasa visual (border, shadow, atau permukaan berlapis) dan pakai konsisten.
- **Gambar:** rasio tetap (cegah CLS), `alt` bermakna, hero dioptimalkan (AVIF/WebP, `priority`).
- **Motion:** hanya `transform`/`opacity`, 120–240 ms untuk mikro-interaksi, easing konsisten,
  WAJIB `prefers-reduced-motion: reduce` → matikan/ perkecil.
- **Target sentuh ≥ 24×24 px**, jarak antar target ≥ 8 px, focus-visible tidak boleh dihapus.

## 4. Gate sebelum kirim (ukur, jangan kira-kira)

| Gate | Ambang |
|---|---|
| Kontras teks | ≥ 4.5:1 (besar ≥ 3:1) — `dcheck`: gate `contrast` PASS |
| Responsive | tidak ada scroll horizontal 360/768/1024/1440 px — gate `overflow` PASS |
| Target sentuh | ≥ 24×24 px — gate `tap-target` PASS |
| Keyboard | semua interaktif reachable, urutan logis, Esc menutup overlay |
| Form | label terhubung, error spesifik + `aria-describedby`, bukan hanya warna |
| LCP | ≤ 2.5 s (gambar hero di-priority, bukan lazy) |
| INP | ≤ 200 ms (hindari handler berat; pecah kerja) |
| CLS | ≤ 0.1 (semua media punya dimensi) |
| Bundle | tidak ada library berat untuk 1 efek; cek ukuran sebelum tambah dependensi |
| Anti-slop | lolos `anti-ui-slop`: tanpa gradient ungu-biru default, tanpa emoji ikon acak, tanpa 3 kartu generik + shadow, tanpa copy "revolutionary/seamless" |

## 5. Pola yang dilarang (slop)

- Hero centered + gradient + badge "AI-powered" + 3 kartu fitur identik.
- Ikon emoji sebagai pengganti icon set; ikon beda gaya dalam satu halaman.
- Copy pujian diri tanpa bukti ("terbaik di industri") — ganti angka/nama nyata atau hapus.
- Animasi di semua elemen; parallax tanpa alasan; marquee tak terkendali.
- Teks abu-abu terang di atas putih (gagal kontras) demi "estetika".
- Dark mode sebagai afterthought (warna tabrakan, shadow tidak terbaca).
- Layout yang sama untuk semua halaman (template dipakai ulang tanpa penyesuaian konteks).

## 6. Definition of done UI

- [ ] Brief + referensi tertulis (link/screenshot) ada.
- [ ] Token satu sumber; tidak ada hardcode warna/ukuran.
- [ ] Semua state komponen ada.
- [ ] Light + dark diperiksa.
- [ ] Keyboard + screen-reader + reduced-motion diperiksa.
- [ ] LCP/INP/CLS diukur (Lighthouse/Playwright trace), bukan diasumsikan.
- [ ] Screenshot desktop + mobile dilampirkan di laporan.
- [ ] Copy sudah diedit (tanpa filler, tanpa AI tells).
- [ ] Lolos gate anti-slop; tidak ada item bagian 5.

## 7. Per tool

Pengecualian aturan hemat token: untuk tugas UI, **1–2 screenshot referensi wajib dibuka**
(`desktop-hero.png`, opsional `mobile.png`). Tanpa melihat gambar, "paham desain" cuma klaim.
Jangan buka 10 gambar sekaligus — pilih yang paling mewakili arah.

Aturan ini otomatis ikut ke semua AI CLI karena `RULES.md` disinkronkan lewat
`python3 ~/.agents/sync-rules.py` (Claude, Codex, Gemini, CodeBuddy, Cline, Copilot).
Kalau AI tidak punya akses file, jalankan `sk --design -n 15` untuk daftar skill dan
`sk -l <nama>` untuk memuat panduannya. `sk` sudah memetakan istilah Indonesia
(desain, tampilan, jelek, rapi → design, ui, slop, polished), jadi tanya pakai bahasa
sehari-hari tetap dapat skill yang benar.
