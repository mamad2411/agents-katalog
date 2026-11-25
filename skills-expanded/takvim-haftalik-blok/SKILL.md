---
description: Google Calendar'dan haftanın programını çekip boş blokları deep work ve solopreneur rutinleriyle doldurur
---

# Takvim Haftalık Blok Planlama

## Amaç

Google Calendar'daki mevcut etkinlikleri okuyup, boş zaman bloklarını solopreneur rutinleriyle (derin çalışma, pazarlama, satış, admin) yapılandırır. "Maker schedule" ilkesini otomatik uygular.

**Kategori**: Yapay Zeka ve Otomasyon
**MCP Gereksinimi**: Google Calendar MCP bağlı olmalı

## Süreç

### Adım 1: Haftanın takvimini çek

Google Calendar MCP `gcal_list_events` aracını kullan:
- Bu haftanın Pazartesi-Cuma etkinliklerini al
- Mevcut toplantı ve randevuları listele

### Adım 2: Boş blokları tespit et

Her gün için 09:00-17:00 arasındaki boş blokları bul. Minimum 90 dakikalık blokları işaretle — daha kısa bloklar "ara" olarak sayılır.

### Adım 3: Solopreneur zaman dağılımını uygula

Haftalık hedef dağılım:
- **%40 İnşa** (ürün geliştirme, kod, tasarım) → 16 saat
- **%30 Pazarlama** (içerik, SEO, sosyal medya) → 12 saat
- **%20 Satış** (müşteri iletişimi, teklifler, toplantılar) → 8 saat
- **%10 Yönetim** (faturalar, e-posta, planlama) → 4 saat

### Adım 4: Blokları ata

Kurallar:
- **Sabah 09:00-12:00** → Her zaman derin çalışma (İnşa veya Pazarlama). Toplantı koymayın.
- **Öğleden sonra 13:00-15:00** → Satış ve müşteri işleri
- **15:00-17:00** → Yönetim, e-posta, planlama
- **Pazartesi sabah** → Haftalık planlama (30 dk)
- **Cuma 16:00** → Haftalık değerlendirme (30 dk)

### Adım 5: Takvime yaz (onay ile)

Kullanıcıya önerilen haftalık bloklama planını göster. Onay alındıktan sonra Google Calendar MCP `gcal_create_event` ile blokları takvime ekle.

Her bloku şu formatta oluştur:
- Başlık: `[TÜR] Açıklama` (ör: `[DERİN ÇALIŞMA] Ürün geliştirme`)
- Renk kodu: İnşa=mavi, Pazarlama=yeşil, Satış=turuncu, Yönetim=gri

## Örnek Çıktı

```
📅 Haftalık Blok Planı — 21-25 Mart

Pazartesi:
  09:00-09:30  [PLANLAMA] Haftalık hedef belirleme
  09:30-12:00  [DERİN ÇALIŞMA] Ürün geliştirme
  13:00-14:00  ← Mevcut: Müşteri toplantısı
  14:00-15:30  [SATIŞ] Teklif hazırlığı
  15:30-17:00  [YÖNETİM] E-posta + faturalar

Salı:
  09:00-12:00  [DERİN ÇALIŞMA] Ürün geliştirme
  13:00-15:00  [PAZARLAMA] Blog yazısı
  15:00-17:00  [PAZARLAMA] Sosyal medya içerikleri

...

Özet:
  İnşa: 15 saat ✅ (hedef: 16)
  Pazarlama: 11 saat ⚠️ (hedef: 12)
  Satış: 8 saat ✅ (hedef: 8)
  Yönetim: 4 saat ✅ (hedef: 4)

Takvime ekleyeyim mi?
```
