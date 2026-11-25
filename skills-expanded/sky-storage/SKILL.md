---
name: sky-storage
description: >-
  Dosya depolama: S3 / Cloudflare R2 / Supabase Storage / UploadThing seçimi, presigned URL ile
  doğrudan yükleme, çok parçalı (multipart) büyük dosya yükleme, erişim kontrolü (özel dosyalar
  için imzalı URL), dosya meta veri tablosu, MIME/boyut doğrulama, virüs taraması, yaşam döngüsü
  kuralları ve geçici yüklemelerin temizlenmesi, CDN, yedek ve maliyet. "Dosya yükleme",
  "belge saklama", "S3", "R2" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Dosya Depolama

## Seçim

| Durum | Seçim |
|---|---|
| Ucuz, çıkış (egress) ücretsiz, S3 uyumlu | **Cloudflare R2** (varsayılan) |
| Supabase projesi | **Supabase Storage** (RLS politikalı) |
| En hızlı kurulum, React bileşenleri hazır | **UploadThing** |
| AWS ekosistemi | S3 + CloudFront |
| Vercel'de basit | Vercel Blob |

Dosyaları asla uygulama sunucusunun diskinde veya DB'de (bytea) tutma.

## Doğrudan yükleme akışı

```
1. İstemci: POST /api/uploads { name, type, size }      → sunucu: yetki + tür/boyut kontrolü
2. Sunucu: files kaydı (status=pending) + presigned PUT URL (5 dk) döner
3. İstemci: dosyayı doğrudan R2/S3'e PUT eder (ilerleme çubuğu: XHR upload.onprogress)
4. İstemci: POST /api/uploads/:id/complete              → sunucu: HEAD ile var mı/boyut doğru mu → status=ready
5. (İsteğe bağlı) iş kuyruğu: görsel varyantları, virüs taraması, metin çıkarma
```
```ts
const key = `orgs/${orgId}/files/${crypto.randomUUID()}${ext}`;   // kullanıcı dosya adını anahtarda kullanma
const url = await getSignedUrl(s3, new PutObjectCommand({ Bucket, Key: key, ContentType: type, ContentLength: size }), { expiresIn: 300 });
```

## Meta veri tablosu

```
files  id, org_id, uploaded_by, key, original_name, mime, size_bytes, checksum, status (pending|ready|infected|deleted),
       width, height, created_at, deleted_at
```
Orijinal ad yalnızca gösterim/indirme adı için (`Content-Disposition: attachment; filename*=UTF-8''…` — Türkçe karakterli adlar doğru iner).

## Erişim kontrolü

- **Herkese açık** (ürün görseli, avatar): ayrı public bucket + CDN alan adı (`cdn.site.com`).
- **Özel** (fatura, kimlik belgesi, sağlık raporu): private bucket; indirme isteğinde yetki kontrolü → 60 sn'lik imzalı GET URL'ye yönlendir.
- Tahmin edilebilir anahtar kullanma; liste (ListBucket) izni istemciye asla.

## Doğrulama

- Tür: izinli liste (`image/jpeg, image/png, image/webp, application/pdf`); sunucuda **magic bytes** ile doğrula (`file-type`), istemcinin söylediği MIME'a güvenme.
- Boyut: presigned URL'de `ContentLength` sabitle; plan bazlı sınır.
- Görselleri yeniden kodla (EXIF temizliği, bkz. `sky-media`); SVG/HTML yüklemeyi reddet veya `attachment` olarak sun.
- Virüs taraması (belge kabul eden sistemlerde): ClamAV konteyneri veya servis; taranana kadar `pending`.

## Büyük dosyalar

- 100MB+ → **multipart upload** (5–100MB parçalar, paralel, yeniden denenebilir), duraklat/devam et (Uppy + `@uppy/aws-s3`).
- Sürükle-bırak, çoklu dosya, ilerleme, kalan süre — Uppy bunların hepsini güzelce verir.

## Yaşam döngüsü ve temizlik

- `pending` kalan (tamamlanmamış) yüklemeler 24 saat sonra silinir (cron + lifecycle kuralı "abort incomplete multipart").
- Silinen kayıtların dosyaları: soft delete → 30 gün → kalıcı silme işi.
- Org/hesap silinince toplu temizlik (prefix bazlı).
- Geçici dosyalar (export, PDF) `tmp/` öneki + 7 gün lifecycle.

## Maliyet ve yedek

- R2 egress ücretsiz; S3'te çıkış pahalı → CDN arkasına koy.
- Versiyonlama (yanlışlıkla silmeye karşı) kritik bucket'larda; ikinci bölgeye/sağlayıcıya replikasyon (bkz. `sky-deploy` yedek).
- Kullanıcı başına depolama kotası (bkz. `sky-metering-quotas`) ve panelde "Kullanılan alan: 1,2 GB / 5 GB".
