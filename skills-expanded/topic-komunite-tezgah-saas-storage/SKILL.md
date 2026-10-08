---
name: saas-storage
description: >
  SaaS uygulaması için Supabase Storage ile dosya depolama altyapısı kur.
  Bucket yapılandırması, RLS ile dosya güvenliği, dosya yükleme, görsel
  optimizasyonu ve plan bazlı depolama limitleri. Bu skill'i kullanıcı
  dosya yükleme, görsel, depolama, storage, upload veya profil fotoğrafı
  ile ilgili bir şey istediğinde kullan. "Dosya yükleme ekle", "profil
  fotoğrafı yükle", "storage kur" gibi ifadeler tetikler.
---

# SaaS Storage — Supabase Storage ile Dosya Depolama

Bu skill, bir SaaS uygulamasının dosya depolama katmanını Supabase Storage ile kurar. Profil fotoğrafları, kullanıcı tarafından yüklenen dokümanlar, ürün görselleri veya dışa aktarılan raporlar — dosya depolama çoğu SaaS'ta gerekli bir katmandır.

Supabase Storage, zaten veritabanı için kullandığın Supabase projesinin parçasıdır — ek servis hesabı veya yapılandırma gerektirmez. RLS ile dosya seviyesinde güvenlik, dahili görsel dönüştürme ve Dashboard'da görsel dosya yönetimi sunar. Ücretsiz katman: 1 GB depolama, 2 GB bandwidth/ay.

**Bağımlılık:** Bu skill **saas-launcher** orkestratör skill'inin opsiyonel bir fazıdır. Bağımsız olarak da kullanılabilir. Her SaaS'ta gerekmez — yalnızca dosya yükleme ihtiyacı varsa uygula.

**Bağlı skill'ler:**
- **saas-database** — Dosya metadata'sı (isim, boyut, tür, URL) veritabanında saklanır. Supabase Storage aynı projenin parçasıdır.
- **saas-auth** — Dosya erişimi kullanıcı kimliğine bağlıdır.
- **saas-api-security** — Yükleme endpoint'leri input validation ve rate limiting gerektirir.

---

## Supabase Storage Kurulumu

### Bucket Oluşturma

Supabase Storage'da dosyalar bucket'larda organize edilir. Her bucket bir klasör gibidir.

Önerilen bucket yapısı:
- `avatars` — Kullanıcı profil fotoğrafları (public)
- `uploads` — Kullanıcı dosyaları (private — RLS ile korunmalı)
- `exports` — Sistem tarafından üretilen dosyalar (private)

**Public vs. Private bucket:**
- Public: Dosya URL'si ile herkes erişebilir. Profil fotoğrafları, ürün görselleri için.
- Private: Erişim RLS politikalarına tabidir. Kullanıcı dokümanları, hassas dosyalar için.

### RLS Politikaları

Storage bucket'ları da veritabanı tabloları gibi RLS ile korunur:

- **Profil fotoğrafı yükleme:** Kullanıcı sadece kendi klasörüne (`avatars/{user_id}/`) yükleyebilsin
- **Dosya okuma:** Kullanıcı sadece kendi dosyalarını görebilsin
- **Dosya silme:** Kullanıcı sadece kendi dosyalarını silebilsin

Klasör yapısı ile RLS'i birleştir: `{bucket}/{user_id}/{dosya}` — bu sayede `auth.uid()` ile yol kontrolü yapılabilir.

---

## Dosya Yükleme Mimarisi

### Client-Side Yükleme (Küçük Dosyalar)

Supabase Storage client'ı ile doğrudan tarayıcıdan yükleme:
1. Kullanıcı dosya seçer
2. Client-side validation (tür, boyut)
3. Supabase Storage API'ye doğrudan yükleme
4. URL'yi veritabanına kaydet

**Avantaj:** Basit, sunucu yükü yok.
**Limit:** Maksimum dosya boyutu Supabase client'ta varsayılan 5 MB (yapılandırılabilir).

### Presigned URL ile Yükleme (Büyük Dosyalar)

Büyük dosyalar için sunucu üzerinden presigned URL oluştur:
1. Client → sunucuya yükleme isteği gönder (dosya adı, tür, boyut)
2. Sunucu validation yapar, presigned upload URL oluşturur
3. Client → presigned URL'ye doğrudan yükleme yapar
4. Sunucu → yükleme tamamlandığını doğrular, metadata'yı veritabanına kaydeder

**Avantaj:** Sunucu dosya içeriğini taşımaz, bandwidth tasarrufu. Büyük dosyalar desteklenir.

---

## Dosya Güvenliği

### Input Validation

Dosya yüklemede şu kontrolleri yap:

1. **Dosya türü kontrolü:** İzin verilen MIME türlerini belirle. Yalnızca beklenen türleri kabul et.
   - Profil fotoğrafı: `image/jpeg`, `image/png`, `image/webp`
   - Doküman: `application/pdf`, `text/plain`
   - **Yapma:** `*/*` veya tüm türlere izin verme

2. **Dosya boyutu kontrolü:** Maksimum boyut belirle.
   - Profil fotoğrafı: 5 MB
   - Doküman: 10-50 MB
   - **Yapma:** Sınırsız yüklemeye izin verme — depolama maliyeti ve DDoS riski

3. **Dosya adı temizleme:** Kullanıcının gönderdiği dosya adını güvenme. UUID ile yeniden adlandır. Orijinal adı metadata olarak sakla.

4. **Magic bytes kontrolü (ileri seviye):** MIME türü header'ı manipüle edilebilir. Dosyanın ilk byte'larını (magic bytes) kontrol ederek gerçek türünü doğrula.

### Rate Limiting

Yükleme endpoint'ine rate limit uygula:
- Kullanıcı başına dakikada 10 yükleme
- Kullanıcı başına günlük toplam boyut limiti (plan bazlı)

### Zararlı İçerik

- Yüklenen görselleri process et (resize/compress) — bu işlem gömülü zararlı kodları temizler
- Dokümanları kullanıcıya sunarken `Content-Disposition: attachment` header'ı ile indirmeye zorla, tarayıcıda açmaya değil
- Mümkünse ayrı bir domain'den servis et (XSS izolasyonu)

---

## Görsel Optimizasyonu

### Neden Önemli

Optimize edilmemiş görseller sayfa yükleme süresini katlar. 5 MB'lık bir profil fotoğrafı yerine 50 KB'lık optimizeli versiyon kullanıcı deneyimini dramatik iyileştirir.

### Supabase Image Transformation

Supabase Storage dahili görsel dönüştürme sunar. URL'ye parametre ekleyerek resize, format dönüşümü ve kalite ayarı yapılabilir.

Önerilen stratejiler:
- **Profil fotoğrafı:** 200x200px, WebP formatı
- **Thumbnail:** 300x200px, WebP formatı
- **Tam boyut:** Orijinal boyutta tut ama formatı WebP'ye dönüştür

### Next.js Image Optimization

Next.js'in `<Image>` bileşeni otomatik görsel optimizasyonu sağlar:
- Lazy loading (görünene kadar yükleme)
- Responsive srcset (ekran boyutuna göre uygun çözünürlük)
- WebP/AVIF format dönüşümü
- Blur placeholder

Storage URL'lerini `next.config.js`'te `remotePatterns`'a ekle — aksi halde Next.js dış domain görselleri optimize etmez.

---

## Plan Bazlı Depolama Limitleri

Her planda farklı depolama limiti tanımla:
- **Free:** 100 MB
- **Starter:** 1 GB
- **Pro:** 10 GB

Her yükleme öncesinde kullanıcının toplam depolama kullanımını kontrol et. Limit aşıldığında yüklemeyi reddet ve plan yükseltme öner.

Toplam kullanımı veritabanında bir sayaç olarak tut — her yükleme ve silme işleminde güncelle. Storage API'den her seferinde toplam boyut hesaplamak yavaş.

---

## Gotchas

- **Public bucket URL'si tahmin edilebilir.** Public bucket'ta dosya adı biliniyorsa herkes erişebilir. Hassas dosyaları public bucket'a koyma.
- **Silinen dosyanın URL'si cache'te kalabilir.** CDN cache süresi boyunca silinmiş dosyaya erişim mümkün olabilir. Hassas dosyalar için signed URL kullan.
- **Dosya adı çakışması.** Aynı ada sahip dosya yüklenirse üzerine yazılır. UUID ile benzersiz ad oluştur.
- **Depolama maliyeti birikir.** Silinmiş hesapların dosyaları hâlâ yer kaplar. Hesap silme akışında ilişkili dosyaları da temizle.
- **CORS hatası.** Client-side yükleme yapıyorsan Supabase Storage'da CORS ayarlarının doğru olduğundan emin ol.
- **Mobil yükleme boyutu.** Mobil cihazlardan yüklenen fotoğraflar orijinal çözünürlükte olabilir (10MB+). Client-side resize yap veya boyut limitini kullanıcıya net göster.
- **Backup'a dahil et.** Dosyalar veritabanından ayrı saklanır. Veritabanı backup'ı dosyaları kapsamaz — storage backup stratejini ayrıca planla.
