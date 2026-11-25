---
name: sky-media
description: >-
  Görsel ve video işleme: yükleme akışı (önizleme, kırpma, döndürme, sıkıştırma), avatar
  kırpıcı, sharp ile sunucu dönüşümleri (AVIF/WebP, boyutlar), BlurHash/LQIP yer tutucu,
  EXIF temizliği (konum gizliliği), görsel CDN'leri, video (HLS, Mux, poster, otomatik
  oynatma kuralları), galeri/lightbox ve Instagram tarzı deneyimler. "Fotoğraf yükleme",
  "avatar", "galeri", "video oynatıcı" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Görsel & Video

## Yükleme akışı (insanların sevdiği sürüm)

1. **Seç / sürükle / yapıştır / kameradan çek** (`<input type="file" accept="image/*" capture="environment">` mobilde).
2. **Anında önizleme** (`URL.createObjectURL`) — sunucuyu bekleme.
3. **Kırp / döndür** (avatar için daire maske, kapak için 16:9) — `react-easy-crop`.
4. **İstemcide sıkıştır** (`browser-image-compression`, maks 2048px, kalite 0.82) → 8MB → 400KB.
5. **İmzalı URL ile doğrudan depolamaya** (bkz. `sky-storage`), ilerleme çubuğu, iptal butonu.
6. Sunucu doğrular (gerçek MIME — magic bytes, boyut), **yeniden kodlar**, varyantları üretir.
7. Bulanık yer tutucudan net görsele yumuşak geçiş.

Çoklu yüklemede her dosya ayrı kart: küçük resim, ilerleme, hata + tekrar dene, sürükleyerek sırala.

## Sunucu dönüşümü (sharp)

```ts
const img = sharp(buffer, { failOn: "error" }).rotate();          // EXIF yönüne göre döndür
const meta = await img.metadata();
const variants = await Promise.all([320, 640, 1280, 2048].filter((w) => w <= (meta.width ?? 0)).map(async (w) => ({
  w, avif: await img.clone().resize({ width: w }).avif({ quality: 55 }).toBuffer(),
  webp: await img.clone().resize({ width: w }).webp({ quality: 78 }).toBuffer(),
})));
// .rotate() + yeniden kodlama EXIF'i (GPS konumu dahil) siler — gizlilik için şart
```
- Varyantları `/{id}/{w}.{fmt}` ile sakla; `<img srcset>` veya `next/image` loader'ı.
- Animasyonlu GIF → MP4/WebM'e çevir (10× küçük).
- SVG yüklemesine izin verme (XSS) ya da sanitize et.
- Ağır işi kuyruğa at (bkz. `sky-jobs`).

## Yer tutucular

- **BlurHash / ThumbHash**: yüklemede hesapla, DB'de kısa string; istemcide çiz.
- `next/image` `placeholder="blur"` + `blurDataURL`.
- Dominant renk arka planı en ucuz yer tutucu.
- `aspect-ratio` her zaman (CLS sıfır).

## Görsel CDN'leri

Cloudinary / imgix / Cloudflare Images / Bunny Optimizer: URL parametresiyle boyut/format
(`?w=640&fm=avif`), otomatik format seçimi, yüz odaklı kırpma (`gravity=face`) — avatar için harika.
Düşük trafikte maliyet-etkin; yüksek trafikte maliyeti hesapla.

## Avatar deneyimi

- Yoksa **baş harfli renkli avatar** (isimden deterministik renk, kontrastlı metin).
- Daire kırpıcı + zoom kaydırıcısı; önizleme 3 boyutta (32/64/128).
- Yüklendiği anda tüm uygulamada güncellenir (cache-busting `?v=updatedAt`).

## Galeri ve lightbox

- Izgara: masonry (CSS `columns`) ya da sabit oranlı kareler.
- Lightbox (`yet-another-react-lightbox` / PhotoSwipe): kaydırma jesti, pinch zoom, klavye okları, Esc,
  URL'de `?foto=3` (paylaşılabilir), arka plan kaydırma kilidi, odak tuzağı.
- Paylaşılan öğe geçişi: küçük resimden büyüğe büyüyerek açılma (View Transitions / Framer `layoutId`).
- Bir sonraki/önceki görseli önceden yükle.

## Video

- Arka plan videosu: `<video autoplay muted loop playsinline poster=…>`; `prefers-reduced-motion`'da durdur; `saveData`'da poster göster.
- Kullanıcı videosu: **Mux / Cloudflare Stream / Bunny Stream** — HLS, uyarlanabilir bitrate, otomatik küçük resim, imzalı oynatma.
- Oynatıcı: `media-chrome` / Vidstack; altyazı (`<track kind="captions" srclang="tr">`), hız, tam ekran, klavye.
- YouTube gömme: **lite embed** (`lite-youtube-embed`) — tıklanana kadar sadece küçük resim (~500KB tasarruf).

## Erişilebilirlik ve gizlilik

- Anlamlı görsellerde `alt` (yüklemede iste), dekoratiflerde `alt=""`.
- EXIF konumunu **her zaman** temizle; kullanıcı fotoğrafı ev konumunu sızdırabilir.
- Kişi içeren fotoğraflarda KVKK: açık rıza bağlamı (ör. etkinlik galerisi).
- Otomatik oynayan sesli medya yok.
