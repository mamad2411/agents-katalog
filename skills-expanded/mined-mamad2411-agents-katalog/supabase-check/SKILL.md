---
name: supabase-check
description: Mandatory verification gate for any change that touches a Supabase-backed table (new/changed migration, or a service function calling the Supabase REST API) — confirms the migration is actually applied to the real project and that real requests (headers/payload) work, since mocked unit tests can pass while the real Authorization/header/payload is wrong. Called from `verify`'s gate 3, never standalone-skipped when DB code changed. Never writes/edits implementation code.
---

# Supabase Check — canlı şema/veri doğrulama, kod yazmaz

## Why this exists
KURAL: `app/interviews/service.py` içindeki 4
fonksiyonda `Authorization` header'ı gerçek token yerine literal `"******"`
yazılmıştı. Tüm unit testler (mock'lu `httpx`) yeşildi, `verify` skill'i de bunu
yakalayamadı — çünkü mock'lu testler asla gerçek Supabase'e gerçek bir istek
atmıyor. Bug ancak kullanıcı gerçek API anahtarlarıyla uçtan uca canlı test
istediğinde ortaya çıktı: RLS açık bir Supabase projesinde geçersiz/eksik
`Authorization`, 401 değil, sessizce boş sonuç (`200 + []`) döndürüyor — yani
"testler yeşil" ile "özellik gerçekten çalışıyor" arasında mock'lu bir test
piramidinde görünmez bir uçurum var, özellikle veritabanına dokunan kodda.

Bu skill o uçurumu kapatır: **veritabanı şemasını değiştiren veya veritabanına
yeni bir okuma/yazma yolu ekleyen her değişiklik**, gerçek Supabase projesine
karşı en az bir kez fiilen doğrulanmadan "tamamlandı" sayılamaz.

## Ne zaman zorunlu
Aşağıdakilerden biri doğruysa bu skill **atlanamaz**, `verify`'ın bir gate'i
olarak koşulmalıdır:
- Yeni bir migration dosyası eklendi/değiştirildi (`supabase/migrations/*.sql`).
- Yeni bir tablo/kolon/RLS politikası kullanan yeni bir servis fonksiyonu
  yazıldı (`httpx.get/post/patch/delete` ile `{settings.supabase_url}/rest/v1/...`
  çağıran her fonksiyon).
- Mevcut bir servis fonksiyonunun Supabase'e giden isteğinin header'ı,
  parametreleri veya payload şekli değişti.

Sadece mock'lu unit test yazıldıysa (implementasyon dosyası hiç değişmediyse)
bu skill gerekmez — tetikleyici, gerçek bir `httpx` çağrısı içeren kod
değişikliğidir, test dosyası değişikliği değil.

## Precondition
- `.env`'de `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` (gerçek proje,
  mock değil) kullanılabilir olmalı.
- Değişikliğin hangi migration/fonksiyonlara dokunduğu bilinmeli (`code_diff.md`
  veya `git diff` üzerinden).

## Steps

### 1. Şema gerçekten uygulanmış mı — doğrula, varsayma
Migration dosyasının repoda var olması, Supabase projesine uygulandığı
anlamına gelmez (bu proje `supabase db push` kullanmıyor, elle SQL Editor'den
uygulanıyor). Her yeni/değişen kolon için gerçek REST sorgusuyla kontrol et:

```python
import httpx
r = httpx.get(f"{SUPABASE_URL}/rest/v1/<tablo>", headers={...},
               params={"select": "<yeni_kolon1>,<yeni_kolon2>", "limit": "1"})
# 200 -> kolon var; 400 + PGRST205/42703 -> kolon/tablo YOK, migration
# uygulanmamış. Kullanıcıya SQL'i verip Dashboard > SQL Editor'den
# çalıştırmasını iste -- kendi başına psql/doğrudan DB bağlantısı deneme
# (DNS/IPv6 sorunları, DB şifresi gerekliliği gibi engellerle karşılaşabilir,
# SQL Editor daha güvenilir bir yol).
```
Eksikse: SQL'i kullanıcıya göster, "Dashboard > SQL Editor > Run" ile
uygulamasını iste, sonra tekrar doğrula. Kendi başına bağlanmaya çalışma
(bağlantı stringi/şifre genelde eksik veya IPv6-only olur).

### 2. Gerçek isteğin header/payload'ını doğrula (asıl bug bu kategoriden çıktı)
Değişen her servis fonksiyonu için, gerçek bir kayıt üzerinde gerçek bir
çağrı yap (aşağıdaki adım 3'ün parçası olarak) VE ayrıca statik olarak
kontrol et:
```bash
grep -n '"Authorization"' app/interviews/service.py
```
Her satırın `f"Bearer {settings.supabase_service_role_key}"` (veya ilgili
gerçek token ifadesi) olduğunu, literal bir maskeli/placeholder string
(`"******"`, `"<token>"`, `"REDACTED"` vb.) OLMADIĞINI doğrula. Bu, Copilot
authoring çağrılarında tekrar eden bilinen bir hata deseni (KAN-17'de,
sonra KAN-20'de tekrar görüldü) — kod incelemesinde atlanması kolay çünkü
söz dizimi geçerli, sadece değer yanlış.

### 3. En az bir gerçek uçtan uca çağrı çalıştır
Gerçek bir test kaydı (kullanıcı/mülakat/vb.) oluştur, değişen endpoint'i
gerçek bir HTTP isteğiyle çağır (dev sunucusu `preview_start` ile ayakta),
yanıtı VE Supabase'deki gerçek satırı (REST ile `select`) karşılaştır.
Mock'lu testlerin doğruladığı "çağrı yapıldı mı" değil, "gerçek veri gerçekten
okunuyor/yazılıyor mu" sorusuna cevap arıyorsun.

### 4. Temizlik
Oluşturduğun test kullanıcı/kayıtları sil (`DELETE` ile REST üzerinden veya
`auth.admin` endpoint'i ile kullanıcı silme). Dev sunucusunu durdur
(`preview_stop`). Geçici scratch dosyalarını temizle.

### 5. Rapor
`verify_report.md`'ye (veya ilgili görevin raporuna) şunu ekle: hangi
tablo/kolonun/fonksiyonun canlıda doğrulandığı, gerçek istek/yanıt örneği
(hassas veri maskelenmiş), bulunan varsa düzeltilen sorun.

## The one rule that can't bend
Bu skill kod yazmaz/düzeltmez — sadece doğrular. Bir sorun bulunursa (eksik
migration, yanlış header, vb.) düzeltme `code-copilot`'a (implementasyon) veya
kullanıcıya (migration'ı SQL Editor'den çalıştırma) devredilir, burada `Edit`
kullanılmaz.
