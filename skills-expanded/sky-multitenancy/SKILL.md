---
name: sky-multitenancy
description: >-
  SaaS çok kiracılı yapı (org/takım/çalışma alanı): veri modeli (organizations, memberships,
  invitations), rol ve izin matrisi, davet akışı (e-posta + bağlantı), org değiştirici, aktif
  org'u URL'de/alt alan adında taşıma, kiracı izolasyonu (RLS, repository filtresi), sahiplik
  devri, üye çıkarma, org bazlı faturalandırma, özel alan adı ve org silme. "Takım özelliği",
  "çalışma alanı", "ekibini davet et", "çok kiracılı" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Çok Kiracılı (Org/Takım)

## Veri modeli

```
organizations  id, name, slug UNIQUE, plan, owner_id, logo_url, created_at
memberships    org_id, user_id, role (owner|admin|member|viewer), created_at  PK(org_id,user_id)
invitations    id, org_id, email, role, token_hash, invited_by, expires_at, accepted_at
```
- İlk kayıtta kişisel org otomatik oluşur ("Ayşe'nin çalışma alanı" yerine "Ayşe — Kişisel"; ek sorununu önler).
- Her kiracı verisi tablosunda `org_id` + indeks.

## Roller

| Yetki | owner | admin | member | viewer |
|---|---|---|---|---|
| Veriyi görme | ✓ | ✓ | ✓ | ✓ |
| Veri oluşturma/düzenleme | ✓ | ✓ | ✓ | |
| Üye davet/çıkarma | ✓ | ✓ | | |
| Faturalandırma | ✓ | ✓* | | |
| Org silme, sahiplik devri | ✓ | | | |
Matris kodda tek yerde (bkz. `sky-auth` RBAC). Org'da her zaman en az bir owner.

## İzolasyon (en kritik konu)

- Tüm sorgular `org_id` filtresi: repository katmanında zorunlu parametre veya Postgres RLS
  (`using (is_member(org_id))`, bkz. `sky-supabase`).
- ID ile erişimde de üyelik kontrolü (`/api/projects/:id` → projenin org'una üye mi?). Yoksa **404**.
- Test: "A org kullanıcısı B org kaydına erişemez" testi her kaynak için (bkz. `sky-testing`).
- Arama indeksi, cache anahtarları, dosya yolları, webhook'lar da org bazlı.

## Aktif org

- URL'de: `/o/[slug]/…` (paylaşılabilir, sekmelerde farklı org) — önerilen.
- Alt alan adı: `acme.sky.app` (B2B'de prestij; proxy'de çözümle, wildcard DNS + sertifika).
- Son kullanılan org çerezde; girişte oraya yönlendir.

## Org değiştirici (insanların sevdiği)

Sidebar üstünde: logo + ad ▾ → org listesi (rol rozeti), "Yeni çalışma alanı oluştur", ⌘K ile hızlı geçiş.
Geçişte sayfa aynı alt yola gider (`/o/acme/ayarlar` → `/o/beta/ayarlar`).

## Davet akışı

1. Admin e-posta(lar) + rol girer (toplu yapıştırma: virgül/satır ayrımlı).
2. Token (DB'de hash), 7 gün geçerli; e-posta: "Ayşe seni Acme Kliniği'ne davet etti" + buton.
3. Bağlantı: hesabı varsa giriş → kabul; yoksa kayıt (e-posta önceden dolu) → kabul.
4. Bekleyen davetler listesi: yeniden gönder, iptal et.
5. Alternatif: **davet bağlantısı** (rol + süre + kullanım sınırı) ve **alan adı ile otomatik katılım**
   ("@acme.com.tr adresli herkes member olarak katılabilir").
Davet kabul edilince ekibe bildirim: "Mehmet katıldı 🎉".

## Üye yönetimi

- Üye listesi: avatar, ad, e-posta, rol (select), son aktif, "Çıkar".
- Kendini çıkarma = "Ayrıl"; son owner ayrılamaz (önce devret).
- Çıkarılan üyenin oturumları o org için geçersiz; oluşturduğu veriler org'da kalır.
- Sahiplik devri: yeni owner onay e-postası ile kabul eder.

## Faturalandırma

- Abonelik **org'a** bağlı, kullanıcıya değil (bkz. `sky-payments`).
- Koltuk (seat) bazlı plan: üye eklemede orantılı ücret uyarısı ("Bu üye aylık faturana ₺99 ekler").
- Plan limitleri (üye sayısı, proje sayısı) → `sky-metering-quotas`.

## Org silme

Owner, org adını yazarak onaylar → 30 gün bekleme (geri alınabilir) → veriler silinir/anonimleşir,
abonelik iptal, faturalar yasal süre saklanır. Dışa aktarım önerilir (bkz. `sky-import-export`).
