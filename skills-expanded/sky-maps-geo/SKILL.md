---
name: sky-maps-geo
description: >-
  Harita ve konum: Türkiye il-ilçe-mahalle yapısı, adres seçimi, "bana en yakın" sorguları, şube
  bulucu, yol tarifi. "Harita ekle", "yakınımdaki", "adres seçimi" dendiğinde kullan.
---

# Sky · Harita & Konum

## Kütüphane seçimi

| İhtiyaç | Seçim |
|---|---|
| Ücretsiz/açık, vektör harita, güzel stil | **MapLibre GL** + OpenFreeMap / MapTiler / Protomaps karoları |
| Basit, hafif, raster yeter | **Leaflet** + OSM karoları (kullanım politikasına uy) |
| Google ekosistemi (Places, Street View) | Google Maps JS API (ücretli kota, API key kısıtla) |
| Tek işletme konumu | **Statik harita görseli + "Yol tarifi al" bağlantısı** (en hızlı, en ucuz) |

Tek bir adres için tam etkileşimli harita ~300KB JS demek; tıklanınca yükle ("Haritayı göster").

## Yol tarifi bağlantıları

```ts
const google = `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`;
const apple  = `https://maps.apple.com/?daddr=${lat},${lng}`;
const yandex = `https://yandex.com.tr/harita/?rtext=~${lat},${lng}`;   // Türkiye'de yaygın
```
"Haritada aç ▾" menüsüyle üçünü sunmak kullanıcıyı mutlu eder; iOS'ta Apple varsayılan.

## İşaretçiler

- 50+ işaretçi → **kümeleme** (`supercluster`); sayılı daireler, zoom'da açılır.
- Özel işaretçi: marka renginde, seçiliyken büyür; **liste ↔ harita senkron** (listede hover → işaretçi
  vurgulanır, tersi de) — bu "vay" dedirtir.
- Haritayı işaretçilere sığdır (`fitBounds` + padding); tek işaretçide zoom 15.
- Bilgi kartı: ad, adres, "Şimdi açık · 21:00'e kadar" rozeti, Ara / Yol tarifi.

## "Bana en yakın"

```sql
create extension if not exists postgis;
alter table branches add column geo geography(Point, 4326);
create index branches_geo on branches using gist (geo);
select id, name, st_distance(geo, st_makepoint($lng, $lat)::geography) as meters
from branches
where st_dwithin(geo, st_makepoint($lng, $lat)::geography, 20000)   -- 20 km
order by geo <-> st_makepoint($lng, $lat)::geography
limit 20;
```
PostGIS yoksa: lat/lng sınırlayıcı kutu ile kaba filtre + Haversine ile sırala.
Mesafeyi insanca göster: "350 m", "2,4 km".

## Konum izni UX'i

- Sayfa açılır açılmaz **isteme**. "📍 Konumumu kullan" butonu → tıklanınca `navigator.geolocation`.
- Reddedilirse: il/ilçe seçimi veya adres araması ile devam; hata metni suçlamasız.
- Kaba konum için IP tabanlı tahmin (ör. platform geo başlıkları) ile varsayılan şehir — izin istemeden.
- `enableHighAccuracy` yalnızca gerekiyorsa (pil).

## Geocoding ve Türkiye adresi

- Otomatik tamamlama: Google Places (ücretli, iyi), MapTiler geocoding, Nominatim/Photon (kendi sunucunda).
- **Türkiye adres yapısı:** İl → İlçe → Mahalle → Cadde/Sokak → No / Daire. Formda il/ilçe/mahalle
  **bağımlı select** (açık veri setleri) + serbest adres satırı + posta kodu. Kargo entegrasyonları bu yapıyı ister
  (bkz. `sky-tr-integrations`).
- Haritada iğneyi sürükleyerek konum düzeltme ("Teslimat noktasını işaretle") — kullanıcılar sever.
- Koordinatları 6 ondalık sakla; herkese açık gösterimde yuvarla (gizlilik).

## Şube bulucu kalıbı

```
┌ arama (adres/şehir) + "Konumumu kullan" ┐
│ liste (mesafeye göre)  │  harita         │   mobilde: liste/harita sekmesi
│ filtreler: açık şimdi, hizmet türü       │
└──────────────────────────────────────────┘
```
URL'de konum ve filtreler; her şubenin kendi SEO sayfası (`LocalBusiness` JSON-LD, bkz. `sky-seo`).

## Performans ve stil

- Harita `dynamic(..., { ssr: false })` + iskelet; görünür olunca yükle.
- Koyu tema için koyu harita stili — temayla birlikte değişsin.
- Mobilde `cooperativeGestures`: tek parmak sayfayı, iki parmak haritayı kaydırsın.
- Atıf (attribution) metnini kaldırma — lisans gereği. API anahtarlarını domain ile kısıtla.
